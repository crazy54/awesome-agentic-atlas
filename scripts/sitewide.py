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


# THE THEMES. Two, and one choice that is not a theme.
#
# Light and Dark, and "System", which stores nothing and lets the operating system's light/dark preference
# pick. The design language is NEUMORPHISM (soft UI), and it is one rule applied everywhere: every surface on
# the page is the same colour as the page, and it is told apart from the page only by light. A box that is
# raised casts a dark shadow down and to the right and catches a highlight up and to the left; a box that is
# pressed in has the same pair inside it, reversed. Nothing has a visible border, nothing is translucent, and
# there is no second surface colour for a panel to be "on": the header, the cards, the chips and the search
# box are all `--surface`, and the shadows are the only thing that makes them objects.
#   * Raised: cards, panels, menus, chips and buttons at rest. Hover lifts them a little (`--raise-hi`).
#   * Pressed in: search boxes, inputs, selects, code wells, progress tracks, and the active tab, chip or nav
#     item (`--press`). A control being clicked is pressed in for as long as it is held.
#   * The accent is Archie's lime, and it is rationed, the way the references ration theirs: glows, the
#     active state, progress, key numbers and the one primary button. Body text, headings and lines are the
#     neutral inks. The lime is deepened to an olive (`--bar`, `--link`) in light wherever it is text,
#     because the lime itself is 1.6:1 on the light base.
#   * Dark is a cool charcoal (refs: charcoal or navy-charcoal soft UI). Light is the same idea on a cool
#     grey-white, with navy-graphite ink.
#
# There used to be a third theme, High contrast, and before that a glass design with a field of colour behind
# frosted panels. Both are gone. What high contrast was for is not: a reader whose system asks for more
# contrast (`prefers-contrast: more`), or forces its own colours (`forced-colors: active`), gets the
# strengthening below automatically, in either theme -- no soft shadows (which carry no contrast), real 3:1
# edges in their place, stronger text, underlined links and a 3px focus ring. A stored "contrast" is migrated
# silently to "dark" (see HEAD_THEME), which is the half it was.
#
# The lime fill is its own pair of tokens, `--act` and `--onact`. `--bar` is drawn as text in a dozen rules --
# eyebrows, counts, the inverted badge -- so in light it has to be the deep olive, and an olive button is a
# drab one. The primary button is not text, so it takes `--act`, which is the real lime in both themes, with
# graphite ink on it at 8.8:1 or better and a 1px `--act-edge` drawn as an inset shadow so the lime has an
# edge on the light base without the box growing. `--act-hi` is its hover. `--glow` is the lime's light.
#
# ONE COPY. The three stylesheets (the catalogue's inline `<style>`, `pages.css`, `detail.css`) take
# `THEME_CSS`, every page family's `<head>` takes `HEAD_THEME`, and `tests/theme_test.py` measures this file.
THEMES = ("light", "dark")

# The colour tokens, per theme. Opaque hex, every one, because WCAG contrast is a ratio between two colours.
#   --surface  the base: the page, and every surface on it
#   --plane    the same base, kept as its own name because a hundred rules say "a panel" with it
#   --band     the same base again: chips, inputs and rows used to be a step off the plane, and in soft UI a
#              step is a shadow, not a colour. Kept so those rules keep meaning what they say.
#   --title    headings: the ink. Titles are not an accent any more.
#   --grid     an etched line: table rules and separators, the only lines left
PALETTE = {
    "dark": {
        "surface": "#24272D", "plane": "#24272D", "band": "#24272D", "ink": "#E8EAED", "ink2": "#C9CDD3",
        "muted": "#A3AAB4", "title": "#E8EAED", "grid": "#33373E", "link": "#C9E46B", "bar": "#B7D63C",
        "good": "#72D6A3", "warn": "#F49A8A", "off": "#A3AAB4", "onbar": "#15171A",
        "act": "#A4C812", "act-hi": "#B9DD2E", "act-edge": "#C4E04A", "onact": "#15171A",
        "accent-sky": "#8DC8E0", "accent-mint": "#72D6A3", "accent-gold": "#DFB86E",
        "accent-coral": "#F49A8A", "accent-violet": "#BCAEF2"},
    "light": {
        "surface": "#E3E7ED", "plane": "#E3E7ED", "band": "#E3E7ED", "ink": "#1C2431", "ink2": "#323C4C",
        "muted": "#4E5868", "title": "#1C2431", "grid": "#CDD3DC", "link": "#3A5A00", "bar": "#3B5C00",
        "good": "#0E6340", "warn": "#9E3726", "off": "#4E5868", "onbar": "#FFFFFF",
        "act": "#A4C812", "act-hi": "#B6D93A", "act-edge": "#5E7A00", "onact": "#1C1B1B",
        "accent-sky": "#1C5C77", "accent-mint": "#0E6340", "accent-gold": "#74500C",
        "accent-coral": "#9E3726", "accent-violet": "#57479A"},
}

# THE LIGHT, per theme: the shadow pairs that make the surfaces objects. Kept under the name `GLASS`, with the
# same keys, because `theme_test.py` composites `panel` and `panel-hi` over the field to measure text -- they
# are now the opaque base (alpha 1), so the measurement is the plain ratio against `--surface`.
#   panel / panel-hi  a static panel and a floating one (the pinned bar, a menu, a dialog): both the base,
#                     opaque, because soft UI has no translucency
#   pools             the field's lighting, as (colour, peak alpha): one soft highlight from the top left,
#                     which is where every surface's own highlight comes from
#   edge / ctl-edge   border colours for the borders the layout already has. Transparent: soft UI draws no
#                     outlines, the shadows are the edge. The strengthened modes put real ones back.
#   raise / -sm / -hi extruded: cards and panels; chips and buttons; a hovered control, lifted a little more
#   press             pressed in: a well (inputs, code, tracks) or a control held down or switched on
#   press-sm          a shallow well for the small things inside dense rows (tags, forge badges)
#   press-act         the lime button, held down
#   glow              the accent's light, for the active state and the one primary action
#   fog               Archie's fog prank (`html[data-fog]`, archie.js): every pane goes milky for 1.6 s
GLASS = {
    "dark": {
        "panel": ("#24272D", 1), "panel-hi": ("#24272D", 1),
        "pools": (("#FFFFFF", .028),),
        "edge": "transparent", "ctl-edge": "transparent",
        "raise": "9px 9px 20px rgba(0,0,0,.55),-7px -7px 18px rgba(255,255,255,.045)",
        "raise-sm": "4px 4px 9px rgba(0,0,0,.5),-3px -3px 8px rgba(255,255,255,.05)",
        "raise-hi": "7px 7px 15px rgba(0,0,0,.58),-5px -5px 12px rgba(255,255,255,.065)",
        "press": "inset 4px 4px 9px rgba(0,0,0,.55),inset -3px -3px 8px rgba(255,255,255,.045)",
        "press-sm": "inset 2px 2px 4px rgba(0,0,0,.5),inset -1px -1px 3px rgba(255,255,255,.05)",
        "press-act": "inset 3px 3px 6px rgba(0,0,0,.38),inset -2px -2px 5px rgba(255,255,255,.28)",
        "glow": "0 0 18px rgba(164,200,18,.38)",
        "fog": ("#3A3E45", .9), "bdf": "none"},
    "light": {
        "panel": ("#E3E7ED", 1), "panel-hi": ("#E3E7ED", 1),
        "pools": (),  # its one pool is a white highlight, which only lifts the base away from the ink
        "edge": "transparent", "ctl-edge": "transparent",
        "raise": "10px 10px 22px rgba(150,162,182,.55),-10px -10px 22px rgba(255,255,255,.9)",
        "raise-sm": "4px 4px 9px rgba(150,162,182,.55),-4px -4px 9px rgba(255,255,255,.95)",
        "raise-hi": "7px 7px 14px rgba(146,158,178,.6),-6px -6px 13px rgba(255,255,255,1)",
        "press": "inset 4px 4px 9px rgba(150,162,182,.55),inset -4px -4px 9px rgba(255,255,255,.9)",
        "press-sm": "inset 2px 2px 4px rgba(150,162,182,.55),inset -2px -2px 4px rgba(255,255,255,.95)",
        "press-act": "inset 3px 3px 6px rgba(60,80,0,.35),inset -2px -2px 5px rgba(255,255,255,.45)",
        "glow": "0 0 16px rgba(120,150,0,.32)",
        "fog": ("#FFFFFF", .84), "bdf": "none"},
}

# The field: the base, with one soft pool of light at the top left, where the highlights come from. Fixed to
# the window and static, so it is depth rather than decoration, and there is nothing to ask a reader who
# asked for reduced motion to stop. Each pool's peak alpha is the one `GLASS[...]["pools"]` names.
WASH = {
    "dark": "radial-gradient(1400px 900px at 12% -10%,rgba(255,255,255,.028),transparent 70%)",
    "light": "radial-gradient(1400px 900px at 12% -10%,rgba(255,255,255,.5),transparent 70%)",
}

# What the strengthened modes lift the secondary inks and the lines to, per theme. Text 7:1 and lines 3:1
# on the base, which is what high contrast used to promise; `theme_test.py` measures them.
STRONG = {
    "dark": {"ink": "#FFFFFF", "ink2": "#F2F3F5", "muted": "#DADDE2", "grid": "#8A919C", "link": "#E3F59A",
             "edge": "#8A919C", "ctl-edge": "#C3C8CF"},
    "light": {"ink": "#000000", "ink2": "#141A24", "muted": "#262E3B", "grid": "#69717E", "link": "#2A4300",
              "edge": "#69717E", "ctl-edge": "#4E5868"},
}


def _rgba(colour: str, alpha: float) -> str:
    h = colour.lstrip("#")
    return f"rgba({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)},{alpha:g})"


def _tokens(theme: str) -> str:
    g = GLASS[theme]
    glass = {"panel": _rgba(*g["panel"]), "panel-hi": _rgba(*g["panel-hi"]), "fog": _rgba(*g["fog"]),
             "bdf": g["bdf"]}
    glass |= {k: g[k] for k in ("edge", "ctl-edge", "raise", "raise-sm", "raise-hi", "press", "press-sm",
                                "press-act", "glow")}
    return ("".join(f"--{k}:{v};" for k, v in PALETTE[theme].items())
            + "".join(f"--{k}:{v};" for k, v in glass.items()) + f"--wash:{WASH[theme]};")


def _strong(theme: str) -> str:
    return "".join(f"--{k}:{v};" for k, v in STRONG[theme].items())


# The soft light switched off: no field, no shadows. Shared by the modes that ask for it; the edges they need
# in the shadows' place come from `_strong` (more contrast) or the system (forced colours).
_SOLID = "--panel:var(--plane);--panel-hi:var(--plane);--bdf:none;--wash:none;"
_FLAT = "--raise:none;--raise-sm:none;--raise-hi:none;--press:none;--press-sm:none;--press-act:none;--glow:none;"

THEME_CSS = (
    "/* THE THEMES. Written by `THEME_CSS` in scripts/sitewide.py, which explains every value; do not edit the\n"
    "   copy in a generated file. Dark is on `:root`, so it needs no attribute to be true -- it is the floor a\n"
    "   reader with JavaScript off gets. */\n"
    ":root{color-scheme:dark;" + _tokens("dark")
    # The structural half: one typeface, the same in both themes, and the soft UI's two radii.
    + '--ui:"Geist","Segoe UI",system-ui,-apple-system,Helvetica,Arial,sans-serif;'
    '--mono:"Geist Mono",ui-monospace,"Cascadia Mono",Consolas,"Liberation Mono",monospace;'
    '--r-card:20px;--r-ctl:14px}\n'
    "html[data-theme=light]{color-scheme:light;" + _tokens("light") + "}\n"
    # ARCHIE'S FOG PRANK: every pane goes milky. After the themes, so it wins over both at the same weight.
    "html[data-fog]{--panel:var(--fog);--panel-hi:var(--fog);--surface:var(--fog);--bdf:blur(34px) saturate(.6)}\n"
    "@media (prefers-reduced-transparency:reduce){:root,html[data-theme]{" + _SOLID + "}}\n"
    "@media (prefers-contrast:more){:root{" + _SOLID + _FLAT + _strong("dark") + "}"
    "html[data-theme=light]{" + _SOLID + _FLAT + _strong("light") + "}}\n"
    "@media (forced-colors:active){:root,html[data-theme]{" + _SOLID + _FLAT + "}}\n"
    + r"""/* Paint only, below this line: no rule here may size or place a box (see the note in sitewide.py). */
/* THE FIELD, on every page family: fixed to the window and behind everything. A pseudo-element of <body>
   at z-index -1 paints over the canvas (which wears the body's --surface) and under every box. */
body::before{content:"";position:fixed;inset:0;z-index:-1;background:var(--wash);pointer-events:none}
/* Type, on every page family: Geist, rendered greyscale so light-on-dark text does not bloom, and titles in
   the neutral ink -- the accent is not spent on them any more. */
body{-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}
:where(h1,h2):where(:not(.ph *)){color:var(--title)}
/* The focus ring, for every page family: the accent, 2px, clear of the control so it never sits on the
   control's own shadows. `:focus-visible` so a click does not leave a ring on the chip that was pressed. */
:focus-visible{outline:2px solid var(--bar);outline-offset:3px;border-radius:6px}
::selection{background:color-mix(in srgb,var(--act) 42%,transparent);color:var(--ink)}
/* THE CONTROLS, on every page family. Raised at rest, lifted a little on hover, pressed into the surface
   while held and while switched on. `html` in front so these outrank each family's own `.chip{...}`, which
   sets the size these leave alone. Switched on is the lime ink plus the well: two cues rather than one. */
html .chip{background:var(--surface);border-color:transparent;box-shadow:var(--raise-sm);
  transition:box-shadow .16s ease,color .16s ease}
html .chip:hover{box-shadow:var(--raise-hi);color:var(--ink)}
html .chip:active{box-shadow:var(--press)}
html .chip[aria-pressed=true],html .chip[aria-current]{background:var(--surface);box-shadow:var(--press)}
:where(.chip[aria-pressed=true],.chip[aria-current]){color:var(--bar)}
/* The primary button, on every page family that has one: the lime, extruded, with its light around it. An
   inset shadow is its edge rather than a border, so the box is the size it always was. */
html .cta{border-radius:999px;transition:box-shadow .16s ease,background .16s ease;
  box-shadow:inset 0 0 0 1px var(--act-edge),inset 0 1px 0 rgba(255,255,255,.35),var(--raise-sm),var(--glow)}
html .cta:hover{background:var(--act-hi);filter:none;
  box-shadow:inset 0 0 0 1px var(--act-edge),inset 0 1px 0 rgba(255,255,255,.35),var(--raise-hi),var(--glow)}
html .cta:active{box-shadow:inset 0 0 0 1px var(--act-edge),var(--press-act)}
/* Every text field and select on the site is a well. */
html :is(input[type=search],input[type=text],input:not([type]),textarea,select){background-color:var(--surface);
  border-color:transparent;box-shadow:var(--press)}
@media (prefers-reduced-motion:reduce){html :is(.chip,.cta){transition:none}}
/* MORE CONTRAST: the soft light is off (it carries no contrast), so real edges go back where it was, and
   the things that are not colours. Links are underlined, so a link is not told from text by its hue alone
   (WCAG 1.4.1) -- except the ones drawn as a pill or a button, whose shape already says "press me". */
@media (prefers-contrast:more){
  html .chip,html .cta,html :is(input,textarea,select){outline:1px solid var(--ctl-edge);outline-offset:-1px}
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
  .cta,.chip{outline:1px solid ButtonText;outline-offset:-1px}
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
.btags{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 14px;font:600 11px/1 var(--mono)}
.btags .btag{display:inline-flex;align-items:center;gap:6px;min-height:24px;padding:4px 10px;border-radius:999px;
  color:var(--ink);background:var(--surface);border:1px solid transparent;text-decoration:none;
  letter-spacing:.01em;box-shadow:var(--raise-sm);transition:box-shadow .16s ease}
.btags .btag:hover{box-shadow:var(--raise-hi);text-decoration:none}
.btags .btag:active{box-shadow:var(--press)}
.btags .btag b{font-weight:600}
.btags .btag .bv{color:var(--muted);font-weight:500}
.btags .btag .bico{color:var(--muted);font:400 12px/1 "Atlas Icons",var(--mono)}
.btags .btag .bico:empty{display:none}
.bdot{width:7px;height:7px;flex:none;border-radius:50%;background:var(--off);box-shadow:var(--press-sm)}
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
