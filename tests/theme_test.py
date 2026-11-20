"""Contrast and consistency tests for the site's two themes, which live in `scripts/sitewide.py`.

The page's colours are custom properties declared twice -- on `:root` for dark and on
`html[data-theme=light]` -- in one constant, `sitewide.THEME_CSS`, that every page family's stylesheet starts
with. Every ratio the comments beside them quote is arithmetic on two hex values, and a comment is not a test:
an earlier palette's comments correctly recorded that its cyan measured 2.53:1 on white, and nothing in the
repository would have noticed if someone had used it there anyway. So this file does the arithmetic. There is
no rendering, no browser and no cache involved, so the whole of it runs from a cold checkout in milliseconds.

THE GLASS is what makes the arithmetic harder than it was. A panel is a translucent fill over whatever is
behind it, and text on it is read against the composite, not against the fill. So every text token is held
to 4.5:1 against the EFFECTIVE background, worst case, as well as against the three opaque backdrops:

  * a static panel (`--panel`) over the field's worst point: the base colour with every pool of colour in
    `WASH` at its peak, stacked -- darkest in light, lightest in dark;
  * a floating panel (`--panel-hi`: the pinned bar, menus, dialogs) over pure black in light and pure white
    in dark, because anything can scroll under it, a screenshot included;
  * the bare field at its worst point, for text drawn straight on the page;
  * Archie's fog prank (`--fog`) over the field's worst point.

Compositing is sRGB, which is what a browser does with a `background` over a backdrop. The blur is ignored:
it can only average the backdrop towards the field, which is never worse than the worst point.

The part worth explaining is the role map. A token's minimum depends on how the CSS uses it -- 4.5:1 for
text, 3:1 for a focus ring or an icon -- and the roles are not guessable from the names: `--warn` is text in
four rules and a chip fill in a fifth. So the roles are read out of the stylesheets rather than hardcoded,
by looking for `color:var(--x)`, `background:var(--x)` and the stroke properties. If a future edit starts
filling with `--good`, the `--onbar` pair appears on its own. A hardcoded map would go stale exactly the way
the prose did.

High contrast is not a theme any more. What it promised -- text 7:1, lines 3:1 -- is now what the
`prefers-contrast: more` block lifts both themes to, and this file holds that block to those floors.

Run: python tests/theme_test.py
"""
from __future__ import annotations

import re
import struct
import sys
from pathlib import Path

PAGE = Path(__file__).resolve().parent.parent / "scripts" / "19_pages.py"
SRC = PAGE.read_text(encoding="utf-8")
SCRIPTS = PAGE.parent
sys.path.insert(0, str(SCRIPTS))
import sitewide  # noqa: E402  -- after the path insert, which is what makes it importable

ok = bad = 0


def check(name: str, got, want) -> None:
    global ok, bad
    if got == want:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}\n  got  {got!r}\n  want {want!r}")


def true(name: str, got) -> None:
    check(name, bool(got), True)


def atleast(name: str, got: float, floor: float) -> None:
    global ok, bad
    if got >= floor:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}\n  got  {got:.2f}:1\n  want >= {floor:.2f}:1")


# ---------------------------------------------------------------- the arithmetic
def _chan(v: float) -> float:
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


def luminance(hexcolour: str) -> float:
    h = hexcolour.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * _chan(r) + 0.7152 * _chan(g) + 0.0722 * _chan(b)


def ratio(a: str, b: str) -> float:
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def _rgb(h: str) -> list[int]:
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def over(top: str, alpha: float, under: str) -> str:
    """`top` at `alpha` composited over the opaque `under`, in sRGB, as the browser does."""
    t, u = _rgb(top), _rgb(under)
    return "#" + "".join(f"{round(alpha * t[i] + (1 - alpha) * u[i]):02X}" for i in range(3))


# Three fixed points, so a sign error in the formula above cannot pass silently. These are the values
# WCAG's own examples give, and they bracket the range: identical, maximal, and one in between that is
# easy to get wrong because both channels are mid-range. And one for the compositing.
check("black on white is 21:1", round(ratio("#000000", "#FFFFFF"), 2), 21.0)
check("a colour on itself is 1:1", round(ratio("#777777", "#777777"), 2), 1.0)
check("#767676 on white is the 4.54:1 WCAG AA boundary", round(ratio("#767676", "#FFFFFF"), 2), 4.54)
check("white at 50% over black is mid grey", over("#FFFFFF", .5, "#000000"), "#808080")

# ---------------------------------------------------------------- parse the two blocks
# Out of the CSS a reader is served, not out of `sitewide.PALETTE`: the dict is what the blocks are built
# from, and the blocks are what the browser reads, so a bug in the builder is caught here as well. Hyphens
# allowed in the name, so `--act-edge` and the accents are measured too.
TOKEN = re.compile(r"--([a-z0-9-]+)\s*:\s*(#[0-9a-fA-F]{3,6})\s*;")
RGBA = re.compile(r"--([a-z0-9-]+)\s*:\s*rgba\((\d+),(\d+),(\d+),([\d.]+)\)\s*;")
THEME_CSS = sitewide.THEME_CSS


def raw(selector: str, src: str = THEME_CSS) -> str:
    i = src.index(selector)
    return src[i + len(selector):src.index("}", i)]


def block(selector: str) -> dict[str, str]:
    """The opaque colour declarations of one theme block in `THEME_CSS`, by selector."""
    return {k: v.upper() for k, v in TOKEN.findall(raw(selector))}


def glass(selector: str) -> dict[str, tuple[str, float]]:
    """The translucent fills of one theme block, as (hex, alpha)."""
    return {k: ("#%02X%02X%02X" % (int(r), int(g), int(b)), float(a))
            for k, r, g, b, a in RGBA.findall(raw(selector)) if k in ("panel", "panel-hi", "fog")}


SETS = {"dark": block(":root{"), "light": block("html[data-theme=light]{")}
FILLS = {"dark": glass(":root{"), "light": glass("html[data-theme=light]{")}
DARK, LIGHT = SETS["dark"], SETS["light"]

# Pinned, because every assertion below iterates these and an empty dict passes all of them.
check("there are exactly two themes", sorted(SETS), sorted(sitewide.THEMES))
check("dark declares twenty-three colour tokens", len(DARK), 23)
for name, T in SETS.items():
    # Same names, not merely the same number. `var(--x)` with no fallback resolves to nothing when the token
    # is missing, so a token absent from one block renders as an unstyled element in that theme only -- the
    # failure that is hardest to see, because the theme you are looking at is fine.
    check(f"{name} declares exactly dark's tokens", sorted(T), sorted(DARK))
    check(f"{name}'s published block is sitewide.PALETTE, value for value",
          T, {k: v.upper() for k, v in sitewide.PALETTE[name].items()})
    check(f"{name}'s published glass is sitewide.GLASS, fill for fill",
          FILLS[name], {k: (v[0].upper(), v[1]) for k, v in sitewide.GLASS[name].items()
                        if k in ("panel", "panel-hi", "fog")})
    for tok in ("edge", "ctl-edge", "raise", "raise-sm", "raise-hi", "press", "press-act", "bdf", "wash"):
        true(f"{name} declares --{tok}", f"--{tok}:" in raw(":root{" if name == "dark" else "html[data-theme=light]{"))

BACKDROPS = ("surface", "plane", "band")


# The field's pools, parsed back out of the gradients a reader is served, so the worst point this file
# measures against is the field that is drawn rather than a list somebody kept beside it.
def pools(theme: str) -> list[tuple[str, float]]:
    out = []
    for r, g, b, a in re.findall(r"rgba\((\d+),(\d+),(\d+),([\d.]+)\)", sitewide.WASH[theme]):
        out.append(("#%02X%02X%02X" % (int(r), int(g), int(b)), float(a)))
    return out


for name in SETS:
    # Per colour, the strongest pool `WASH` draws in it: two pools of one colour overlap nowhere at their
    # peaks, so the strongest of each, stacked, is the worst any point on the field can be.
    peak = {}
    for colour, alpha in pools(name):
        if colour != "#FFFFFF":
            peak[colour] = max(alpha, peak.get(colour, 0))
    check(f"{name}: GLASS names each pool colour WASH draws, at its peak alpha",
          sorted(sitewide.GLASS[name]["pools"]), sorted(peak.items()))


def worst_field(theme: str) -> str:
    """The field's worst point for text: every coloured pool at its peak, stacked over the base."""
    c = SETS[theme]["surface"]
    for colour, alpha in sitewide.GLASS[theme]["pools"]:
        c = over(colour, alpha, c)
    return c


def effective(theme: str) -> dict[str, str]:
    """Every effective background text can sit on in this theme, by name."""
    T, G, f = SETS[theme], FILLS[theme], worst_field(theme)
    far = "#000000" if theme == "light" else "#FFFFFF"
    return {"field": T["surface"], "field@pools": f,
            "panel@pools": over(*G["panel"], f), "panel@field": over(*G["panel"], T["surface"]),
            "panel-hi@worst": over(*G["panel-hi"], far), "fog@pools": over(*G["fog"], f),
            **{b: T[b] for b in BACKDROPS}}


true("the field's worst point in light is darker than its base", luminance(worst_field("light")) < luminance(LIGHT["surface"]))
true("the field's worst point in dark is lighter than its base", luminance(worst_field("dark")) > luminance(DARK["surface"]))
true("--plane is the static glass over the bare field, to within two steps a channel",
     all(abs(a - b) <= 2 for t in SETS for a, b in zip(_rgb(SETS[t]["plane"]),
                                                     _rgb(over(*FILLS[t]["panel"], SETS[t]["surface"])))))

# ---------------------------------------------------------------- roles, read from the CSS
# Every stylesheet a page family is served, as text: the catalogue's template, the two other generators'
# stylesheets, the homepage's own rules, the local and models pages, and the shared constants. The question
# is only which tokens appear after `color:` and which after `background:`, so text is enough.
STYLES = "\n".join([SRC, THEME_CSS, sitewide.BUILDTAGS_CSS]
                   + [(SCRIPTS / f).read_text(encoding="utf-8")
                      for f in ("20_landing.py", "22_detail.py", "31_home.py", "32_local.py", "41_models_page.py",
                                "mark.py", "osicons.py")]
                   + [(SCRIPTS.parent / "docs" / "assets" / f).read_text(encoding="utf-8")
                      for f in ("archie.js", "atlas-admin.js")])


def used_as(prop: str) -> set[str]:
    return set(re.findall(rf"(?<![\w-]){prop}\s*:\s*var\(--([a-z0-9-]+)\)", STYLES))


AS_TEXT = used_as("color")
AS_FILL = used_as("background") | used_as("background-color")
# A translucent mix into `transparent` is a halo, not a boundary -- a 14% tint around a status dot -- and it
# has no second colour to be a ratio against, so it is not a stroke. It is stripped before the stroke roles
# are read; a solid `var(--x)` in the same declaration is still counted.
HALOS = re.sub(r"color-mix\(in srgb,\s*var\(--[a-z0-9-]+\)\s*\d+%,\s*transparent\)", "", STYLES)
AS_STROKE = set(re.findall(r"(?:outline|border|border-color|box-shadow)[^;{}]*var\(--([a-z0-9-]+)\)", HALOS))
AS_STROKE |= set(re.findall(r"fill\s*:\s*var\(--([a-z0-9-]+)\)", HALOS))

# The map has to have found something, or every assertion below vacuously passes -- the failure mode this
# whole file exists to avoid. These are the ones the stylesheets certainly use each way.
true("the role map found text tokens", {"ink", "muted", "link", "title"} <= AS_TEXT)
true("the role map found fill tokens", {"act", "act-hi", "warn", "good", "panel", "panel-hi"} <= AS_FILL)
true("the role map found stroke tokens", {"bar", "act-edge"} <= AS_STROKE)
true("--onbar and --onact are ink on a fill", {"onbar", "onact"} <= AS_TEXT)

ACT_FILLS = {"act", "act-hi"}
NOT_COLOURS = set(BACKDROPS) | {"onbar", "onact", "grid", "act-edge"}
FILL = sorted((AS_FILL & set(DARK)) - NOT_COLOURS - ACT_FILLS)
# Every colour token that is not a backdrop, an ink-on-a-fill, a hairline or a fill only is held to the text
# floor whether or not a rule draws it as text today -- the team's `tokens.md` tells the other streams the
# accents are usable as text, and this is what makes that true rather than hoped.
TEXT = sorted(set(DARK) - NOT_COLOURS - ACT_FILLS)
true("every token drawn as text is in the text set", (AS_TEXT & set(DARK)) - NOT_COLOURS - ACT_FILLS <= set(TEXT))

# ---------------------------------------------------------------- the assertions
BODY, LINE, NONTEXT = 4.5, 1.15, 3.0


def audit(name: str, T: dict[str, str]) -> None:
    """Every ratio the site owes a reader, for one theme."""
    E = effective(name)
    # Every text token, on every background it can land on, the glass's worst cases included. Which
    # background a given rule uses is not tracked, and deliberately: the same span appears in a card on the
    # field and in the pinned bar over a screenshot. Requiring all of them is the honest reading.
    for tok in TEXT:
        for b, colour in E.items():
            atleast(f"{name}: --{tok} as text on {b} ({colour})", ratio(T[tok], colour), BODY)
    for tok in FILL:
        atleast(f"{name}: --onbar as ink on filled --{tok}", ratio(T["onbar"], T[tok]), BODY)
    for tok in sorted(ACT_FILLS):
        atleast(f"{name}: --onact as ink on filled --{tok}", ratio(T["onact"], T[tok]), BODY)
    atleast(f"{name}: --act as text on --onact (the count badge inverts)", ratio(T["act"], T["onact"]), BODY)
    # Rings, borders and icons: not text, so 3:1 -- WCAG 1.4.11 -- on every background, glass included.
    # --act-edge is the lime button's only edge in light, where the lime itself is 1.7:1 on the glaze.
    for tok in sorted((AS_STROKE & set(T)) - set(BACKDROPS) - {"grid", "ink", "onbar", "onact"}):
        for b, colour in E.items():
            if tok == "act-edge" and b.startswith(("panel-hi", "fog")):
                continue  # the lime button is never on a floating panel or in the fog's own prank frame
            atleast(f"{name}: --{tok} as a stroke on {b}", ratio(T[tok], colour), NONTEXT)
    # Hairlines that separate two panels rather than carrying meaning. 1.15 is calibrated, not chosen: an
    # earlier palette shipped for months with its worst border pair at 1.168, and a selected row that
    # vanished into its own background measured 1.05.
    for b in BACKDROPS:
        atleast(f"{name}: --grid is visible on --{b}", ratio(T["grid"], T[b]), LINE)
    atleast(f"{name}: --plane is distinguishable from --surface", ratio(T["plane"], T["surface"]), 1.03)


for name, T in SETS.items():
    audit(name, T)

# THE STRENGTHENED MODES. `prefers-contrast: more` turns the glass off (solid --plane panels, no field) and
# lifts the inks and the lines; what high contrast used to promise is what it is held to: every text pair
# 7:1 (WCAG AAA 1.4.6), every line 3:1 on the solid backdrops.
for name, T in SETS.items():
    S = T | {k: v.upper() for k, v in sitewide.STRONG[name].items() if k in T}
    for tok in ("ink", "ink2", "muted", "link"):
        for b in BACKDROPS:
            atleast(f"{name}, more contrast: --{tok} as text on --{b}", ratio(S[tok], S[b]), 7.0)
    for tok in ("grid", "bar"):
        for b in BACKDROPS:
            atleast(f"{name}, more contrast: --{tok} as a line on --{b}", ratio(S[tok], S[b]), NONTEXT)
    for tok in ("edge", "ctl-edge"):
        atleast(f"{name}, more contrast: --{tok} is a solid 3:1 line", ratio(sitewide.STRONG[name][tok], T["plane"]), NONTEXT)
MORE = THEME_CSS[THEME_CSS.index("@media (prefers-contrast:more){:root{"):]
MORE = MORE[:MORE.index("}}") + 2]
for tok in ("--panel:var(--plane)", "--panel-hi:var(--plane)", "--bdf:none", "--wash:none", "--raise:none",
            "--press:none"):
    true(f"more contrast sets {tok} in both themes", MORE.count(tok) == 2)
RT = raw("@media (prefers-reduced-transparency:reduce){:root,html[data-theme]{")
for tok in ("--panel:var(--plane)", "--panel-hi:var(--plane)", "--bdf:none", "--wash:none"):
    true(f"reduced transparency sets {tok}", tok in RT)
FC = raw("@media (forced-colors:active){:root,html[data-theme]{")
true("forced colours drop the glass and the shadows", "--bdf:none" in FC and "--raise:none" in FC)
SUP = THEME_CSS[THEME_CSS.index("@supports not ((backdrop-filter:blur(1px))"):]
true("a browser with no backdrop filter gets the opaque panel", "--panel:var(--plane)" in SUP[:SUP.index("}}")])
# The order is load-bearing: each switch-off block restates the theme selectors at the same weight, so it
# only wins by coming after them, and the fog prank has to come before them so a reader who asked for solid
# panels never sees it.
iL = THEME_CSS.index("html[data-theme=light]{")
iF = THEME_CSS.index("html[data-fog]{")
true("the fog prank comes after both themes and before every switch-off block",
     iL < iF < min(THEME_CSS.index(x) for x in ("@supports not", "@media (prefers-reduced-transparency",
                                                 "@media (prefers-contrast:more){:root{", "@media (forced-colors")))
true("the fog thickens the panels and the blur", all(t in raw("html[data-fog]{") for t in ("--panel:var(--fog)", "--panel-hi:var(--fog)", "--bdf:blur(")))

# The brief, pinned. Archie is warm white ceramic, near-black graphite and a bright lime. Light is glass on
# his egg-shell; dark is a dark grey with his egg-shell for the text and his lime for titles, accents and
# lines. These catch the real regression a pass like this is for -- a palette whose every ratio still clears
# while the colours have quietly stopped being his.
r, g, b_ = _rgb(LIGHT["surface"])
true("light's field is a warm glaze, not stark white", r > b_ and LIGHT["surface"] != "#FFFFFF")
check("light's glass is white glass", FILLS["light"]["panel"][0], "#FFFFFF")
true("light's pools are his iris light and his lime",
     {c for c, _ in sitewide.GLASS["light"]["pools"]} == {"#DCF55E", "#A4C812"})
true("dark's page is a dark, dark grey (neutral, near-black)",
     luminance(DARK["surface"]) < 0.015 and max(_rgb(DARK["surface"])) - min(_rgb(DARK["surface"])) <= 2)
check("dark's text is his egg-shell", DARK["ink"], "#EBE5DA")
check("dark's titles and accent are his lime", (DARK["title"], DARK["bar"]), ("#A4C812", "#A4C812"))
true("dark's lines are lime-tinted", (lambda c: c[1] > c[0] > c[2])(_rgb(DARK["grid"])))
true("dark's field has at most a faint lime glow", all(a <= 0.1 for _, a in sitewide.GLASS["dark"]["pools"]))
check("the primary button is Archie's lime in light and dark", (LIGHT["act"], DARK["act"]), ("#A4C812", "#A4C812"))
check("no two themes share a --surface", len({T["surface"] for T in SETS.values()}), 2)

# ---------------------------------------------------------------- the structural tokens
ROOT_RAW = raw(":root{")
true("--ui is the embedded Geist, then the font stack the page shipped with",
     '--ui:"Geist","Segoe UI",system-ui,-apple-system,Helvetica,Arial,sans-serif;' in ROOT_RAW)
true("--mono is the embedded Geist Mono, then the platform monospaces", '--mono:"Geist Mono",ui-monospace,' in ROOT_RAW)
for tok in ("--ui:", "--mono:"):
    true(f"light does not restate {tok[:-1]}, so it cannot change the layout", tok not in raw("html[data-theme=light]{"))
true("both themes declare their colour-scheme, so native controls follow them",
     all("color-scheme:" in raw(s) for s in (":root{", "html[data-theme=light]{")))
true("the field is one fixed layer behind everything, shared by every page family",
     'body::before{content:"";position:fixed;inset:0;z-index:-1;background:var(--wash);pointer-events:none}'
     in THEME_CSS)
for f in ("19_pages.py", "20_landing.py", "22_detail.py"):
    true(f"{f}'s body no longer paints the wash itself", "background-image:var(--wash)" not in (SCRIPTS / f).read_text(encoding="utf-8"))

# BLUR IS RATIONED, and this is where it is counted. `backdrop-filter` is the costly property, so it may sit
# on a bounded set of large surfaces and never on a rule that draws once per row or card. And never on
# `.subbar`: on a phone it holds the fixed filter sheet, and a backdrop filter makes an element the
# containing block of its fixed descendants -- measured dragging the closed sheet 330px up the page.
BLURRED = set()
for f in ("19_pages.py", "20_landing.py", "22_detail.py", "31_home.py", "32_local.py", "41_models_page.py"):
    css = re.sub(r"/\*.*?\*/", "", (SCRIPTS / f).read_text(encoding="utf-8"), flags=re.S)
    for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        if re.search(r"(?<![\w-])backdrop-filter\s*:\s*var\(--bdf\)", body):
            BLURRED |= {s.strip() for s in sel.strip().split("\n")[-1].split(",")}
ALLOWED = {"header", ".bar", ".setmenu", "footer", "dialog#pal", "dialog#exp", "dialog#mapdlg", ".hero",
           ".daily", ".dsold", ".dancemenu", ".updbar"}
check("the backdrop filter is on the bounded set of large surfaces and nothing else", sorted(BLURRED - ALLOWED), [])
true("...and the check found them", {"header", ".bar", ".hero"} <= BLURRED)
true(".subbar is glass without the blur", ".subbar" not in BLURRED)
for per_item in (".cx", ".mcard", ".lxtile", ".dsc", ".dcard", ".pick", "tr", ".chip", ".bychip", ".lxs"):
    true(f"{per_item} is never blurred", per_item not in BLURRED)

# ---------------------------------------------------------------- paint only
# Both redesigns were held to "the layout does not move", and the shared rules in `THEME_CSS` are applied to
# every page of the site at once -- so a property that sizes or places a box, written there, would move every
# page at once. Read the rules after the marker and refuse any declaration that is not paint. `outline`,
# `box-shadow`, colours, radii, `text-decoration`, `background`, `backdrop-filter` and the
# `forced-color-adjust` switch are paint; a border width, a padding or a font weight are not. The one
# exception is the field's own `body::before`, which is a fixed, out-of-flow layer of nothing: its
# `position` and `inset` place a pseudo-element that has no box in anybody's layout.
PAINT_ONLY = THEME_CSS[THEME_CSS.index("Paint only, below this line"):]
PAINT_ONLY = PAINT_ONLY.replace(
    'body::before{content:"";position:fixed;inset:0;z-index:-1;background:var(--wash);pointer-events:none}', "")
DECLS = [d.split(":")[0].strip() for body in re.findall(r"\{([^{}]*)\}", re.sub(r"/\*.*?\*/", "", PAINT_ONLY, flags=re.S))
         for d in body.split(";") if ":" in d]
LAYOUT = re.compile(r"^(width|height|min-|max-|margin|padding|display|position|top|left|right|bottom|inset|"
                    r"gap|grid|flex|font-size|font-weight|font$|line-height|letter-spacing|border(-width)?$|"
                    r"border-(top|right|bottom|left)(-width)?$|float|transform|zoom|scale|translate)")
check("THEME_CSS's shared rules change paint only, never a box",
      sorted({d for d in DECLS if LAYOUT.match(d) and d not in ("forced-color-adjust",)}), [])
true("...and the check found the rules it reads", {"outline", "box-shadow", "text-decoration"} <= set(DECLS))
MORE_RULES = THEME_CSS[THEME_CSS.index("@media (prefers-contrast:more){\n"):]
true("more contrast underlines links", "a{text-decoration:underline" in MORE_RULES)
true("more contrast's focus ring is 3px", ":focus-visible{outline:3px solid" in MORE_RULES)
true("more contrast marks a pressed control with an outline as well as a fill", "[aria-pressed=true]{outline:" in MORE_RULES)
true("more contrast draws no art behind the masthead's words", ".mhart{background:none" in MORE_RULES)
FORCED = THEME_CSS[THEME_CSS.index("@media (forced-colors:active){\n"):]
true("forced colours keep a focus ring in the system's Highlight", ":focus-visible{outline:3px solid Highlight" in FORCED)
true("forced colours keep a pressed control's state", "[aria-pressed=true]{outline:2px solid Highlight" in FORCED)
true("forced colours keep the swatches as previews", ".thsw{forced-color-adjust:none}" in FORCED)
true("nothing anywhere still styles a contrast theme", "data-theme=contrast" not in STYLES)
true("titles take --title at zero weight, so a heading with its own colour keeps it",
     ":where(h1,h2):where(:not(.ph *)){color:var(--title)}" in THEME_CSS)

# ---------------------------------------------------------------- one copy
# The palette used to be copied by hand into three generators and compared byte for byte. It is one constant
# now, and the claim to hold is that nothing has grown a copy back: each generator drops `THEME_CSS` in, and
# none of them declares a colour token of its own.
true("19_pages.py drops THEME_CSS into the catalogue",
     '.replace("__THEMECSS__", pagemin.strip_css(sitewide.THEME_CSS))' in SRC and "__THEMECSS__\n" in SRC)
true("19_pages.py drops HEAD_THEME into the catalogue's head",
     '.replace("__HEADTHEME__", sitewide.HEAD_THEME)' in SRC and "__HEADTHEME__" in SRC[:SRC.index("<style>")])
for follower in ("20_landing.py", "22_detail.py"):
    text = (SCRIPTS / follower).read_text(encoding="utf-8")
    true(f"{follower} starts its stylesheet with THEME_CSS", '""" + sitewide.THEME_CSS + """' in text)
    true(f"{follower}'s HEAD_THEME is sitewide's", "HEAD_THEME = sitewide.HEAD_THEME" in text)
for f in ("19_pages.py", "20_landing.py", "22_detail.py", "31_home.py", "25_collections.py", "19d_discover.py",
          "32_local.py", "41_models_page.py"):
    text = (SCRIPTS / f).read_text(encoding="utf-8")
    check(f"{f} declares no palette token of its own",
          re.findall(r"--(?:surface|plane|band|ink|bar|link|act|title|panel|edge|raise|press|wash):[#r]", text), [])
# And nothing anywhere still names the skin axis, except the head script deleting its key.
SKIN_WORDS = re.compile(r"data-skin|dataset\.skin|atlas-skin|atlas-unlock")
# `30_v2.py` is the one exception, and it is not the site's theme: it is the `/v2/` design prototype, a beta
# page outside the sitemap with its own self-contained skin picker, kept as the record of a layout study.
for path in sorted(list(SCRIPTS.glob("*.py")) + list((SCRIPTS.parent / "docs" / "assets").glob("*.js"))):
    if path.name == "30_v2.py":
        continue
    text = path.read_text(encoding="utf-8")
    if path.name == "sitewide.py":
        text = text.replace('localStorage.getItem("atlas-skin")', "").replace('localStorage.removeItem("atlas-skin")', "")
        text = text.replace('localStorage.getItem("atlas-unlock")', "").replace('localStorage.removeItem("atlas-unlock")', "")
        text = text.replace("delete root.dataset.skin", "")
        text = re.sub(r"#[^\n]*", "", text)        # the comments that explain the migration
    check(f"{path.name} names no skin", SKIN_WORDS.findall(text), [])

# ---------------------------------------------------------------- the pre-paint script
# The head script sets `theme-color` before any stylesheet is parsed, so it cannot read a computed value and
# carries --plane as literals -- the one place a palette value is written twice, and a re-theme that misses it
# leaves the browser chrome on the old palette for the first frame.
HEAD = sitewide.HEAD_THEME
for name, T in SETS.items():
    true(f"the pre-paint script's {name} literal is its --plane", f'{name}: "{T["plane"]}"' in HEAD)
true("the <meta> theme-color is dark's --plane, matching the data-theme=dark floor",
     re.search(r'name="theme-color"[^>]*content="([^"]+)"', HEAD).group(1).upper() == DARK["plane"])
true("the head script accepts the two themes and nothing else", 'if (t !== "light" && t !== "dark")' in HEAD)
true("the head script no longer asks the OS for contrast: that is the stylesheet's job now",
     "prefers-contrast" not in HEAD)
# THE MIGRATIONS. Both old skin keys removed, and the `theme` key -- which already records the light or dark
# half a skin reader was wearing -- untouched; and a stored "contrast" rewritten to "dark", once, before the
# validity check, so it is stored rather than merely worn.
true("the migration removes the old skin key", 'localStorage.removeItem("atlas-skin")' in HEAD)
true("...and the old unlock key", 'localStorage.removeItem("atlas-unlock")' in HEAD)
true("...and does not delete the reader's light/dark choice", 'removeItem("theme")' not in HEAD)
true("a stored high contrast is rewritten to dark, its half",
     'if (t === "contrast") localStorage.setItem("theme", t = "dark");' in HEAD
     and HEAD.index('t === "contrast"') < HEAD.index('if (t !== "light"'))
true("<html> carries data-theme=dark as its floor and no skin",
     '<html lang="en" data-theme="dark" data-view=' in SRC)

# ---------------------------------------------------------------- the after-paint resolution
JS = sitewide.THEME_JS
true("atlasTheme is a hoisted function declaration", JS.startswith("function atlasTheme() {"))
true("...memoised, so every caller shares one", "if (atlasTheme.api) return atlasTheme.api;" in JS)
true("System is stored as no value at all", 'if (c === "system") localStorage.removeItem("theme")' in JS)
true("it accepts the two themes", 'return t === "light" || t === "dark";' in JS)
true("it migrates a stored contrast too, for the pages whose head script is a release older",
     'if (t === "contrast") { try { localStorage.setItem("theme", t = "dark"); } catch (e) {} }' in JS)
true("it follows the OS light/dark preference, for a reader on System",
     'matchMedia("(prefers-color-scheme: light)").addEventListener("change", on)' in JS
     and 'if (api.choice() === "system")' in JS)
true("it repaints the browser chrome from the computed --plane", 'getPropertyValue("--plane")' in JS)

# ---------------------------------------------------------------- the menu
# `SETTINGS_MENU` in 19_pages.py, which 31_home.py imports. Three buttons, in the order they are drawn.
MENU = re.findall(r'<button type="button" class="thb" data-choice="(\w+)"(.*?)</button>', SRC, re.S)
check("the menu offers System, Light and Dark, in that order", [c for c, _ in MENU], ["system", "light", "dark"])
check("their labels", [re.sub(r".*</span>", "", m, flags=re.S).strip() for _, m in MENU], ["System", "Light", "Dark"])
WANT_SWATCH = {"system": [LIGHT["surface"], DARK["surface"], DARK["act"]],
               "light": [LIGHT["surface"], LIGHT["act"], LIGHT["link"]],
               "dark": [DARK["surface"], DARK["act"], DARK["link"]]}
for choice, markup in MENU:
    check(f"{choice}'s swatch is its own colours", re.findall(r"background:(#[0-9A-F]{6})", markup), WANT_SWATCH[choice])
check("the markup presses exactly one choice, System", [c for c, m in MENU if 'aria-pressed="true"' in m], ["system"])
SETJS = SRC[SRC.index("SETTINGS_JS = "):SRC.index('}"""', SRC.index("SETTINGS_JS = "))]
true("the settings script carries atlasTheme with it, for the homepage that inlines it",
     SETJS.startswith("SETTINGS_JS = sitewide.THEME_JS + "))
true("a button stores its choice", "atlasTheme().set(t.dataset.choice)" in SETJS)
true("pressed marks the reader's choice, not the theme being worn",
     't.setAttribute("aria-pressed", String(t.dataset.choice === choice))' in SETJS)
true("...and exposes its repaint, for Archie's pranks and the other tabs", "window.atlasPaintSettings = paintSettings" in SETJS)
true("the menu no longer carries a second light/dark toggle", 'id="theme"' not in SRC[SRC.index("SETTINGS_MENU = "):SRC.index("DEPLOYMENT_BADGE")])
true("the command palette reads its Theme group off the menu's buttons",
     'for (const t of document.querySelectorAll(".thb"))\n    add("Theme",' in SRC)
true("the menu is hidden by the attribute, which also takes it out of the a11y tree",
     '<div class="setmenu" id="setmenu" hidden>' in SRC)
true("a pressed theme carries a tick as well as a border", '.thb[aria-pressed=true]::after{content:"\\2713"' in SRC)

# ---- AND THAT AN OPEN PANEL IS VISIBLE, which is not the same claim as being displayed -----------------
#
# The first version of this shipped with the panel painting under the pinned bar: `header` is a stacking
# context at z-index 10, `.bar` is 20, and two thirds of the panel landed in the bar's band. `display:block`
# and `aria-expanded="true"` were both true of it. Neither is a claim about whether a reader can see the
# control, and an assertion on either would have gone on passing forever.
zof = lambda sel: int(re.search(r"z-index:(-?\d+)", raw("\n" + sel, SRC)).group(1))
HDRZ, BARZ, SETZ = zof("header{"), zof(".bar{"), zof("header.setopen{")
check("an open settings panel outranks the pinned bar, so it is visible and not merely displayed",
      (BARZ < SETZ, BARZ, SETZ), (True, BARZ, SETZ))
check("...and the masthead's own rule is untouched, so a closed menu stacks exactly as it always did",
      (HDRZ < BARZ, HDRZ, BARZ), (True, HDRZ, BARZ))
check("...and one rule declares it, toggled from one place, in step with the attribute",
      (SRC.count("header.setopen{"), SRC.count('classList.toggle("setopen", open)'),
       'add("setopen"' in SRC or 'remove("setopen"' in SRC),
      (1, 1, False))

# ---------------------------------------------------------------- can this file go red
# A harness that cannot fail is decoration. Perturb one value and confirm the same arithmetic rejects it.
check("sanity: the undeepened lime would NOT pass as text on light's glaze",
      ratio("#A4C812", LIGHT["surface"]) >= 4.5, False)
check("sanity: ...and is the 1.5:1 the comment in sitewide.py quotes",
      round(ratio("#A4C812", LIGHT["surface"]), 1), 1.5)
check("sanity: dark's captions would NOT pass on a dark glass as thin as light's, over white",
      ratio(DARK["muted"], over(FILLS["dark"]["panel"][0], .52, "#FFFFFF")) >= 4.5, False)
check("sanity: light's muted ink would NOT pass on the pinned bar if it were the static glass",
      ratio(LIGHT["muted"], over(*FILLS["light"]["panel"], "#000000")) >= 4.5, False)

# ---------------------------------------------------------------- the copies that are not CSS
# `23_og.py` renders a social card as a standalone document with no stylesheet to inherit from, so its colours
# are a dict -- which is also the card cache's signature, so a palette edit re-renders the cards. Every value
# in it has to be a dark-theme value.
OG = (SCRIPTS / "23_og.py").read_text(encoding="utf-8")
palette_source = OG[OG.index("PALETTE = {"):OG.index("}\n", OG.index("PALETTE = {")) + 2]


def norm(h: str) -> str:
    h = h.lstrip("#").upper()
    return "#" + ("".join(c * 2 for c in h) if len(h) == 3 else h)


og_hex = {norm(h) for h in re.findall(r'"(#[0-9a-fA-F]{3,6})"', palette_source)}
true("the OG card's palette object was found", len(og_hex) >= 5)
for h in sorted(og_hex):
    true(f"the OG card's {h} is a dark-theme value", h in set(DARK.values()))
true("the OG card is drawn on dark's page colour", DARK["surface"] in og_hex)

# `24_pwa.py` writes the manifest and copies the installed-app icons. The manifest's two colours are dark's
# --plane, the same value as the page's theme-color, so an installed window's chrome does not change colour
# between the launch frame and first paint.
PWA = (SCRIPTS / "24_pwa.py").read_text(encoding="utf-8")
MARK = (SCRIPTS / "mark.py").read_text(encoding="utf-8")


def tup(name: str) -> str:
    m = re.search(rf"^{name} = \((0x[0-9A-Fa-f]{{2}}), (0x[0-9A-Fa-f]{{2}}), (0x[0-9A-Fa-f]{{2}})\)$", PWA, re.M)
    return "#%02X%02X%02X" % tuple(int(g, 16) for g in m.groups()) if m else "NOT FOUND"


check("24_pwa.py's PLANE is dark --plane", tup("PLANE"), DARK["plane"])
true("the manifest's two colours are PLANE, so they match the page's theme-color",
     PWA.count('"#%02x%02x%02x" % PLANE') == 2)


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    true(f"{path.name} is a PNG", data[:8] == b"\x89PNG\r\n\x1a\n" and data[12:16] == b"IHDR")
    return struct.unpack(">II", data[16:24])


# THE CURRENT ARCHIE, EVERYWHERE THE FIRST ONE WAS
#
# The first Archie -- a black robot in pixel shades with a gold globe -- was drawn in five places: the
# catalogue's `atlas-byte.png`, the vector mark `mark.py` put top-left on every page, its port in `30_v2.py`,
# `favicon.svg`, and the installed icons `24_pwa.icon()` drew from primitives. The owner retired him for the
# 3D Archie, and every one of those now comes from `art/brand/build.py`, cut from the owner's renders in
# `.github/readme/`. The shades' path is the fingerprint: it is the one shape every copy of the old drawing
# carried verbatim, and nothing else on the site draws it.
SHADES = "M11 22h17v4h4v-4h21v14h-4v4H34v-4h-4v4H15v-4h-4z"
ROOT = SCRIPTS.parent
for gen in ("mark.py", "30_v2.py", "24_pwa.py", "19_pages.py"):
    text = (SCRIPTS / gen).read_text(encoding="utf-8")
    true(f"{gen} no longer draws the first Archie's shades", SHADES not in text)
    true(f"{gen} no longer names the first Archie's art", "atlas-byte.png" not in text)
true("the first Archie's art is gone from docs/assets/", not (ROOT / "docs" / "assets" / "atlas-byte.png").exists())
FAVICON_SVG = (ROOT / "docs" / "favicon.svg").read_text(encoding="utf-8")
true("favicon.svg is no longer the shades-and-globe vector", SHADES not in FAVICON_SVG)
true("...it is Archie's tile, embedded", 'href="data:image/png;base64,' in FAVICON_SVG)
true("mark.py points at the tile art/brand/build.py writes", 'ASSET = "assets/archie-mark.webp"' in MARK)
true("...and that file exists", (ROOT / "docs" / "assets" / "archie-mark.webp").exists())
true("the catalogue's mascot is the new bust", 'src="__UP__assets/archie-bust.webp"' in SRC)
true("...and that file exists", (ROOT / "docs" / "assets" / "archie-bust.webp").exists())

# The installed icons: `24_pwa.py` copies them from `art/brand/` byte for byte, at the sizes the manifest and
# the apple-touch link declare. A committed `docs/` icon that differs from its source is one `24_pwa.py` did
# not write, which is how the old globe could survive a change to the art.
for name, px in (("icon-192.png", 192), ("icon-512.png", 512), ("icon-maskable-512.png", 512),
                 ("apple-touch-icon.png", 180)):
    src, out = ROOT / "art" / "brand" / name, ROOT / "docs" / name
    true(f"art/brand/{name} exists", src.exists())
    if src.exists():
        check(f"art/brand/{name} is {px}px square", png_size(src), (px, px))
        true(f"docs/{name} is the art/brand copy", out.exists() and out.read_bytes() == src.read_bytes())
true("docs/favicon.ico is the art/brand copy",
     (ROOT / "docs" / "favicon.ico").read_bytes() == (ROOT / "art" / "brand" / "favicon.ico").read_bytes())

# THE OTHER CHANNEL
#
# Everything above is about colour. The five platform verdicts also carry a mark -- `✓ ? ✗ – ·` -- and that
# mark is the channel that survives a red/green deficiency, a greyscale print and a pasted export. It is the
# same kind of claim as the ratios above and checkable the same way: by arithmetic on the source rather than
# by reading the comment beside it, which is this file's whole reason for existing.
#
# It is here rather than in `probe.mjs` because of what the subject is. `probe.mjs` asserts on
# `docs/index.html`, which is the *last published* page -- on a clean checkout it can be older than the
# generator beside it, so a legend added to `19_pages.py` today is absent from it until a daily rebuild
# commits one, and asserting the new shape there reddens CI for the lifetime of that gap. The subject of a
# drift check is the generator, so the generator is what it reads.
#
# Three places say what the marks mean and no generator keeps them in step, which is exactly the drift
# `osicons.py` exists to prevent for the platform icons: the `VERDICT` map, the `.vkey` legend in the body,
# and the prose in `listMarkdown()` and `listHTML()`. A mark added to one and not the others ships a legend
# that explains four of five.
VERDICT_BLOCK = re.search(r"const VERDICT = \{(.*?)\n\};", SRC, re.S)
true("the VERDICT map is where this file expects it", bool(VERDICT_BLOCK))
VERDICT = re.findall(r'^\s*"?([A-Za-z-])"?\s*:\s*\["(.)",\s*"([^"]+)"\]',
                     VERDICT_BLOCK.group(1) if VERDICT_BLOCK else "", re.M)
# Pinned to five rather than "at least one", because the regex above is the only thing standing between
# this section and passing vacuously: a map it cannot parse yields no marks, no marks collide, and every
# assertion below is trivially true. A sixth verdict is meant to fail here and be added on purpose.
check("all five verdicts parse out of it", len(VERDICT), 5)

# The one that had a real defect. `a` and `-` both drew `–`, in the same `--off` colour at the same `.75`
# opacity, so "the platform question does not apply to this project" and "we could not tell either way" were
# the same cell in every channel a reader has. Not a 1.4.1 colour failure -- 1.4.1 is about colour being the
# *only* channel, and here there was none at all. 220 of 6,470 cells, and no row carries both, so it is a
# defect met only when comparing two projects, which is how it survived this long.
MARKS = [glyph for _, glyph, _ in VERDICT]
check("each verdict has a mark of its own", sorted(MARKS), sorted(set(MARKS)))
# A mark can only be the channel if it is there without the stylesheet, which a pasted export is.
true("no verdict mark is blank", all(glyph.strip() for glyph in MARKS))

# The `<dt>`s are `aria-hidden` and the words beside them are the accessible text, so a screen reader reads
# five verdicts rather than five symbol names. Read as pairs rather than by position: a legend listing the
# right five marks against the wrong five sentences is the failure worth catching, and position cannot see it.
KEY = re.search(r'<details class="vkey">(.*?)</details>', SRC, re.S)
true("the page body carries a verdict legend", bool(KEY))
# Keyed on the class rather than on the mark, and that is the load-bearing choice. `class="vY"` is what
# colours the entry, and it is the same class the cells carry, so reading the legend through its class is what
# proves the swatch a reader is shown is the colour they will meet in the table. Matching on the mark alone
# passed a legend whose `·` was labelled `class="vz"` -- no such rule, so it would have rendered unstyled
# beside four coloured siblings while this file called it correct. Found by mutating the legend and watching
# nothing fail, which is the only way to learn that about an assertion.
LEGEND = {key: (glyph, re.sub(r"\s+", " ", words).strip().lower()) for key, glyph, words in
          re.findall(r'<dt aria-hidden="true" class="v(.)">(.)</dt><dd><b>([^<]+)</b>',
                     KEY.group(1) if KEY else "")}
check("the legend has an entry per verdict, keyed by the same class the cells use",
      sorted(LEGEND), sorted(key for key, _, _ in VERDICT))
# `aria-hidden` on every one of them, because the words beside the mark are the accessible text. A `<dt>`
# that lost it makes a screen reader read the symbol and then the sentence explaining the symbol.
check("every legend mark is hidden from the accessibility tree",
      len(re.findall(r"<dt ", KEY.group(1) if KEY else "")), len(LEGEND))
for key, glyph, words in VERDICT:
    got_glyph, got_words = LEGEND.get(key, ("", ""))
    check("the legend draws " + key + " with the mark VERDICT gives it", got_glyph, glyph)
    # `VERDICT` holds a fragment ("stated support"); the legend holds a sentence ("Stated support."). Prefix
    # rather than equality, so the legend may say more than the fragment can while still starting from it.
    true("the legend describes " + glyph + " in the words VERDICT uses (" + words + ")",
         got_words.startswith(words.lower()))

# The exports are the third place, and were the only one for a long time: the gloss lived in these two
# functions and nowhere a reader on the page could see it. They also carried the substantive error the legend
# was written to fix -- they glossed `–` as "not applicable" and omitted "not established", which is 180 of
# the 220 dash cells, so the meaning documented was the rarer of the two.
for fn in ("listMarkdown", "listHTML"):
    body = SRC[SRC.index("function " + fn + "("):]
    body = body[:body.index("\n}")]
    check(fn + "()'s legend names all five marks",
          [glyph for glyph in MARKS if glyph not in body], [])
    # The marks are compared and the words are not, which is the deliberate half. The export gloss is one
    # line inside a document about something else, so it abbreviates -- "stated" for "stated support",
    # "no evidence" for "no evidence of support" -- and requiring `VERDICT`'s exact fragments here would
    # force that line to grow every time a fragment did. What must not drift is the pair the marks cannot
    # distinguish on their own, because that is where this legend was actually wrong: it glossed the dash
    # as "not applicable" and left "not established" unsaid, and 180 of the 220 dash cells are the latter.
    for phrase in ("not established", "not applicable"):
        true(fn + "() distinguishes the two quiet verdicts: " + phrase, phrase in body)

# ---------------------------------------------------------------------------------------------------
# ABOVE THE FOLD
#
# At 375x760 the first result's *name* used to sit at y=740 with one pixel of it showing: a masthead of
# 335 and a filter bar of 165, then 226px of screenshot and star-count inside the card before the name
# it belongs to. Two changes bought it 82px and put the name, its repo link, Save and all five platform
# verdicts on screen. The measurements and the reasoning are in the comments beside both.
#
# This is asserted here, off the generator's source, and not in `cards-check.mjs` -- which measures real
# layout at 375 and is the obvious home for it. `tests/run.mjs` serves `cards-check.mjs` the *committed*
# `docs/`, so a layout assertion about a rule added today fails until a build lands, which is the trap
# `probe.mjs` fell into over the verdict legend. Source is the only subject available on a cold checkout.
#
# Both changes fail silently if undone, which is why they are worth the assertions:
#
#   * the art and the column it sits in are sized by two rules on purpose. Re-merged into the one rule
#     they used to share, the column shrinks with the art and the "Atlas Byte" name tag wraps to two
#     lines -- and gets *taller*, giving back the pixels the change was for.
#   * the card-order rules repeat the cards block's selectors exactly, so they win on source order and
#     nothing else. Moved up beside the masthead rules -- where they look like they belong -- they lose
#     to the block they are meant to outrank, the order reverts, and no rule anywhere looks wrong.

def media_block(src: str, opener: str, nth: int = 0) -> str:
    """The text inside the nth occurrence of `opener`, brace-matched rather than regexed."""
    at = -1
    for _ in range(nth + 1):
        at = src.index(opener, at + 1)
    depth, start, i = 1, at + len(opener), at + len(opener)
    while depth and i < len(src):
        if src[i] == "{":
            depth += 1
        elif src[i] == "}":
            depth -= 1
        i += 1
    return src[start:i - 1]


# The exact string, which cannot collide with `@media(max-width:640px),(max-height:560px)` -- the filter
# sheet's query, a different block with a different job.
PHONE = "@media(max-width:640px){"
check("the phone query is emitted exactly twice: the masthead, then the card order", SRC.count(PHONE), 2)
MASTHEAD = media_block(SRC, PHONE, 0)
CARD = media_block(SRC, PHONE, 1)

COLUMN = re.search(r"\.atlas-byte-wrap\{width:(\d+)px\}", MASTHEAD)
ART = re.search(r"\.atlas-byte\{width:(\d+)px", MASTHEAD)
true("the phone masthead sizes the mascot's column", bool(COLUMN))
true("...and sizes its art by a separate rule", bool(ART))
true("the art is smaller than its column, or the name tag wraps and costs more than the art saved",
     bool(COLUMN and ART) and int(ART.group(1)) < int(COLUMN.group(1)))
# The floor the whole masthead budget is measured against: two of these stacked under the art are 88 of
# the column's 149px, and they are a tap target before they are a layout problem. Matched with the padding
# it is declared with, because the shorter string also occurs in prose -- the first version of this line
# passed off a copy of the rule inside the comment that explains it, and went on passing when the rule
# itself was deleted. A source-reading test can be satisfied by the source's own description of itself.
true("the mascot's buttons keep a 44px tap target on a phone",
     "header button{min-height:44px;padding:0 14px}" in SRC)

for cell, row in (("pj", "2"), ("rk", "3"), ("st-c", "3")):
    found = re.search(r"html\[data-view=cards\] :where\(#out\) td\." + re.escape(cell) + r"\{grid-row:(\d)", CARD)
    check("the phone card puts td." + cell + " on grid row " + row, found and found.group(1), row)

DESKTOP_PJ = SRC.index("html[data-view=cards] :where(#out) td.pj{grid-column")
true("the phone card order is emitted after the cards block whose selectors it repeats",
     SRC.index(PHONE, DESKTOP_PJ + 1) > DESKTOP_PJ)

# Untouched on purpose. These carry two attributes and outrank the phone rules at every width, so a reader
# who turned the screenshots off keeps the order that was designed for not having them -- rank, then name.
check("the screenshots-off card order is left as it was",
      [re.search(r"html\[data-view=cards\]\[data-index-screenshots=off\] :where\(#out\) td\." + c + r"\{grid-row:(\d)",
                 SRC).group(1) for c in ("rk", "st-c", "pj")],
      ["1", "1", "2"])

# ---------------------------------------------------------------------------------------------------
# THE SECOND TABLE
#
# `render()` used to emit one <table> and nothing else, and the whole stylesheet was written against that. The
# comparison panel (JFH-186) is the second one, and the two blocks that turn a row into a card -- the 640px
# query and the cards view, which is the *default* view -- select bare `thead`, `table`, `tbody`, `tr` and `td`.
# Both reached into the panel. Measured at 375px with four projects pinned, before this was fixed: the thead had
# zero height, the cells were laid out by `grid-template-columns:1fr auto` in alternating 249/71px pairs,
# `min-width:0` had collapsed every column, and the scroller had nothing left to scroll.
#
# Here rather than in `cards-check.mjs`, which measures real layout in a real browser and is the instrument that
# ought to own this, for the reason the section above gives: `tests.yml` serves the *committed* `docs/` and
# regenerates nothing, so a browser harness reads the last published stylesheet. It cannot see a rule added to
# the generator today, in either direction -- it would neither fail on the defect nor confirm the fix. What is
# checkable without a build is the source, so that is what this reads. `cards-check.mjs` has the layout
# assertions too -- table display, the column floor, the sticky rail, the phone scroller, and the same layout
# in both views -- and they measure whatever build it is pointed at, which on CI is the last one published.
#
# Every assertion from here down reads the source with its comments stripped out, by the same
# `scripts/pagemin.py` that strips them out of the page a reader is served. The reason is a defect this
# repository has already shipped once: a source-reading test can be satisfied by the source's own comment. Half
# of what is checked below -- `CMP_MAX`, `BY_NWO`, `FLAGS["index.compare"]`, `min-width:0`, and the cards-view
# selectors this section is entirely about -- is *named in the prose beside the code*, at length and on purpose,
# because that prose is where the reasoning lives. So a substring test against the raw file would pass on the
# explanation of the rule after the rule itself had been deleted. Stripping first makes these tests read what
# the browser reads.
# Each region is stripped by the stripper for its own language, and not the whole file by both: `19_pages.py` is
# Python, so `strip_js` run over it would meet triple-quoted strings and `https://` inside them with rules
# written for JavaScript. The two regions below are genuine CSS and genuine JavaScript, which is what these
# functions are for.
sys.path.insert(0, str(PAGE.parent))
import pagemin  # noqa: E402  -- after the path insert, which is what makes it importable

CSS = pagemin.strip_css(SRC[SRC.index("<style>"):SRC.index("</style>")])
PRINT = CSS[CSS.index("@media print{"):]

# Pinned, not "at least one", for the same reason as the verdict map above: if the panel's block is ever
# renamed, none of these substring tests can match, nothing collides, and every assertion below passes by
# finding nothing. A count is what makes the section fail rather than go quiet.
CMP_RULES = re.findall(r"^#cmp[^{]*\{", CSS, re.M)
atleast("the comparison panel's rules are where this file expects them", len(CMP_RULES), 17)

# An id and not the `.cmp` class every other component on this page is styled by. `html[data-view=cards]
# tr:hover td` is the strongest thing either view block reaches for, at (0,2,2); one id beats all of it, so the
# panel holds regardless of where the block sits and regardless of what is added to the cards view later. A
# class would tie with `html[data-view=cards] td` and be decided by source order, which is a fix that works
# until somebody moves a block.
true("the panel is styled through an id, so no view rule can outrank it",
     "#cmp{display:none}" in CSS and not re.search(r"^\.cmp[ .{\[]", CSS, re.M))
# Belt as well as braces: the block also sits after both view blocks, so it wins ties too. Cheap to assert and
# it documents the ordering for anyone who moves it back up beside `.shared`, where it reads like it belongs.
true("the panel's block comes after the two blocks that would recast its table",
     CSS.index("#cmp{display:none}") > CSS.rindex("html[data-view=cards]"))

# The actual defect was the two view blocks laying this table out as cards: they selected bare table
# elements, and the panel restated five display types to take them back. The fix is at the source now --
# both blocks reach their table through `:where(#out)` -- so what is asserted is that source. Every selector
# in either block that names a table element names it inside `#out`. Read off every comma-separated part,
# since `html[data-view=cards] td.shot,html[data-view=cards] td.hide` half-scoped is the likely regression.
TABLE_EL = re.compile(r"(?:^|[\s>+~])(?:table|thead|tbody|tr|td|th)(?![\w-])")
VIEW_SELECTORS = [part.strip() for n in range(2)
                  for rule in re.findall(r"(?:^|[{}])\s*([^{}@/]+)\{", media_block(CSS, PHONE, n))
                  for part in rule.split(",")]
VIEW_SELECTORS += [part.strip() for rule in re.findall(r"^\s*(html\[data-view=cards\][^{]*)\{", CSS, re.M)
                   for part in rule.split(",")]
REACHING = [x for x in VIEW_SELECTORS if TABLE_EL.search(x)]
atleast("the view blocks' table-element selectors were found at all", len(REACHING), 40)
check("every one of them is scoped to the results table",
   [x for x in REACHING if ":where(#out) " not in x], [])
# `:where()` and not a plain `#out`, and the difference is the whole of why the scoping changed nothing it
# was not meant to. `#out td` is (1,0,1), which beats `.shot{display:none}` and the density rules' `td`
# padding -- measured, that put screenshots back on every phone in table view. `:where(#out) td` is (0,0,1),
# the weight `td` always had, so every contest these rules take part in comes out as it did before.
check("...through :where(), which leaves every one of their weights as it was",
   [x for x in REACHING if re.search(r"(?<!:where\()#out ", x)], [])
# 148px is what makes the scroller a scroller: four of them plus the 104px label rail is 696px, so a 375px
# phone has real width to swipe, where automatic table layout would squeeze four columns into the box.
true("the panel's cells carry a width floor",
     re.search(r"^#cmp td\{[^}]*min-width:1\d\dpx", CSS, re.M) is not None)
# The row labels are what make four columns usable at 375px, and a sticky cell with a transparent background
# has the cells sliding under it show through.
true("the row labels are sticky and opaque",
     re.search(r"^#cmp tbody th\{[^}]*position:sticky[^}]*background:var\(--", CSS, re.M) is not None)
# Table view stripes alternate rows, and tints and underlines the row under the pointer, all against
# `tbody tr` in general. Those are about a list being scanned; a comparison whose cells change as the mouse
# crosses them is harder to read. The underline is a box-shadow, and for as long as only the fill was
# cancelled, table view still ruled a line under the hovered row of the matrix.
true("no view's row paint reaches the panel",
     re.search(r"^#cmp tbody td\{[^}]*background:transparent", CSS, re.M) is not None
     and re.search(r"^#cmp tbody td\{[^}]*box-shadow:none", CSS, re.M) is not None)

# PAPER
#
# The panel is the one thing on this page that is more use printed than on screen: four projects in columns is
# what somebody carries into the meeting where the choice is made. So it must survive the print sheet, and
# every affordance built for swiping has to go -- paper has no horizontal scroll, and an affordance that
# cannot be used there is not merely inert, it pushes content off the edge.
#
# Measured on a sheet of A4 less the 14mm margins, 182mm or about 673 CSS px, with four projects pinned:
# releasing `overflow-x` alone left the table asking for 971px with its last column ending 992px from the
# left -- 319px past the edge, nothing to clip it and nothing to say so. Releasing the 148px floor as well
# still left it at 971px, because an auto layout sizes columns to content. `table-layout:fixed` is what
# bounds it, and after it the table measures 631px with none of its 52 cells spilling.
# Read as selector lists rather than by substring: the hide list is one rule with fourteen selectors in it, and
# a substring test on it passes for `#cmp .unpin` when what is actually written is `#cmp .unpinned`.
HIDDEN_IN_PRINT = {sel.strip() for group in re.findall(r"([^{}]+)\{display:none\}", PRINT)
                   for sel in group.split(",")}
true("the panel itself stays on the sheet", "#cmp" not in HIDDEN_IN_PRINT)
for control in ("#cmp .ch .sp", "#cmp .unpin", ".pin", "#setmenu"):
    true("printing drops a control nobody can press: " + control, control in HIDDEN_IN_PRINT)
true("printing releases the horizontal scroller",
     re.search(r"#cmp \.scroll\{[^}]*overflow-x:visible", PRINT) is not None)
true("printing bounds the table to the sheet rather than to its content",
     re.search(r"#cmp table\{[^}]*table-layout:fixed", PRINT) is not None)
true("printing releases the swipe-width floor that put it 319px off the page",
     re.search(r"#cmp td\{[^}]*min-width:0", PRINT) is not None)
true("printing unsticks the row labels, which have nothing left to stay in front of",
     re.search(r"#cmp tbody th\{[^}]*position:static", PRINT) is not None)
# Percentages and not pixels, so pinning two projects gives each of them half the sheet rather than a quarter
# of it and three columns of white space. Measured: 274px each at two pinned, 137px each at four.
true("the label rail's printed width is a share of the sheet, not a fixed one",
     re.search(r"#cmp thead th:first-child\{width:\d+%\}", PRINT) is not None)


# WHAT PINNING IS NOT
#
# The pinned set lives in `state`, which is where every filter lives, and it is not a filter. Three things
# depend on that and none of them is enforced by anything but this section. `match()` reading `state.cmp`
# would silently turn Compare into a filter; `rescue()` offering to drop it would invite the reader to throw
# away the comparison to widen a search; `viewTitle()` naming it would put it in the exported Markdown's
# title, where it is not a claim about what the table holds.
def body_of(fn: str) -> str:
    """One top-level function, cut at its closing brace in column 0, with its comments stripped."""
    body = SRC[SRC.index("function " + fn + "("):]
    return pagemin.strip_js(body[:body.index("\n}")])


for fn in ("match", "rescue", "viewTitle"):
    true(fn + "() does not treat the comparison as a filter", "state.cmp" not in body_of(fn))
# `set()` does `Object.assign(state, patch, {shown: PAGE_SIZE})`, so anything routed through it throws the
# reader back to row 1 of the results. That is right for a filter and wrong for pinning a project nine screens
# down: the whole point is that the reader keeps their place. `toggleSave` already made this argument; this is
# the second control to need it, and neither is protected by anything except not doing it.
true("set() leaves the pinned set alone", "cmp" not in body_of("set"))
true("pinning does not route through set(), which would scroll the reader back to the top",
     "set(" not in re.sub(r"\bnew Set\(", "", body_of("togglePin")))

# The cap is one named constant. Written as a literal in each of the five places that need it -- the button's
# `disabled`, its accessible name, the refusal `say()`, the hash cap and the "pin N more" copy -- it drifts,
# and the failure is silent in the direction that matters: a cap of 4 with copy that says 3.
true("the cap is a named constant", re.search(r"^const CMP_MAX = \d+;", SRC, re.M) is not None)
for fn in ("pinBtn", "pinLabel", "togglePin", "readHash", "paintCompare"):
    true(fn + "() takes the cap from CMP_MAX rather than repeating it", "CMP_MAX" in body_of(fn))

# Pinned keys resolve through `BY_NWO`, which is built from every row, and never through `HITS`, which holds
# only what survived the current filter. This is the difference between "the selection survives a filter
# change" -- one of the four things this feature promises -- and a comparison that empties itself when the
# reader narrows the search that found the projects in the first place.
for fn in ("readHash", "paintCompare"):
    true(fn + "() resolves pinned keys against every row, not the filtered ones",
         "BY_NWO" in body_of(fn) and "HITS" not in body_of(fn))
# And the hash is not trusted: a hand-edited `cmp=` can name rows that do not exist and more than the cap.
true("readHash() drops pinned keys that name no row", "BY_NWO.has" in body_of("readHash"))
true("readHash() caps a hand-edited link at CMP_MAX", ".slice(0, CMP_MAX)" in body_of("readHash"))

# The difference test compares the string the reader is shown, not the value behind it. Two pushes 9 and 11
# days apart both render "1mo ago", and a `≠` on two cells that read identically does not teach the reader
# that the marks mean something -- it teaches them the marks are noise. `since()` wraps `sinceText()` in a
# span with a `title`, so comparing its output would compare two different ISO dates inside two identical
# words. The split exists for this, and `since()` being built from `sinceText()` is what stops them drifting.
true("since() is built from sinceText(), so the mark and the words cannot disagree",
     "sinceText(iso)" in body_of("since"))
true("the last-push row's difference test compares the rendered words",
     re.search(r'\["Last push", r => \(\{html: since\(r\.pushed\), key: sinceText\(r\.pushed\)\}\)\]',
               body_of("cmpFields")) is not None)
# The platform rows key on the verdict word and not on the letter, so the two dash states -- which `VERDICT`
# now draws with different marks but which both mean "we could not tell you" -- do not read as a difference.
true("the platform rows key on the verdict's words, not its letter",
     re.search(r"key: v\[1\]", body_of("cmpFields")) is not None)

# Two channels for the mark, never one, which is the same claim the verdict legend above makes and is checked
# the same way. The bar on the label cell is colour; the `≠` is not. Somebody comparing four things at once is
# doing it because holding them in their head is not working, and a cue they cannot perceive is not a cue.
DIFFERS = body_of("cmpTable")
true("a differing row is marked by something that is not colour", '<span class="dx"' in DIFFERS)
true("the mark is hidden from the accessibility tree", 'class="dx" aria-hidden="true"' in DIFFERS)
true("and the words beside it are the accessible text", '<span class="sr">, these differ</span>' in DIFFERS)
true("a differing row is also marked by colour, for the readers the glyph is not for",
     re.search(r"^#cmp tr\.differs th\{[^}]*border-left:\dpx solid var\(--warn\)", CSS, re.M) is not None)
# Deliberately no mark on the rows that agree: "these four all run on Linux" is not a finding, and drawing it
# would put twelve marks on screen to say nothing. Asserted so that adding one is a decision, not a drift.
true("the rows that agree are not marked at all", 'class="differs"' in DIFFERS and
     DIFFERS.count('<span class="dx"') == 1)

# The matrix keeps real table semantics, which is the whole reason the panel is a <table> and the reason the
# CSS above had to be fought for. `scope` on both axes is what lets a screen reader answer "what is this
# cell?" with "obra/superpowers, Licence" rather than reading a number with no referent -- and it is exactly
# what a `display:block` recast destroys, silently, while every glyph stays on screen.
# Both column headings are named, not just "a `scope=col` appears somewhere". Written as one test on the
# corner cell it passed with the four project headings stripped of their axis, which is the half that matters:
# the corner is a courtesy, and the project names are what every cell in the panel is relative to. Found by
# deleting the attribute and watching nothing fail.
true("the project column headings declare their axis",
     re.search(r"""<th scope="col"><a href="' \+ detailURL\(""", DIFFERS) is not None)
true("the empty corner cell declares its axis and is named for a screen reader",
     '<th scope="col"><span class="sr">What is being compared</span>' in DIFFERS)
check("nothing else in the panel claims to be a column heading", DIFFERS.count('scope="col"'), 2)
true("the row labels declare their axis", '<th scope="row">' in DIFFERS)

# Off, the feature leaves nothing behind. `app_flags_test.py` asserts that every index flag has *a* branch;
# what matters here is which two functions carry it, because those are the only two entry points: no buttons
# to press, and a `#cmp=` link in a shared URL ignored rather than half-honoured.
for fn in ("pinBtn", "readHash"):
    true(fn + '() is gated on FLAGS["index.compare"]', 'FLAGS["index.compare"]' in body_of(fn))


# ─── THE CONSTELLATION (JFH-298) ─────────────────────────────────────────────────────────────────────────
#
# Read the same way and for the same reason as everything above: stripped source, because the browser
# harnesses serve the committed `docs/` and cannot see a rule added to the generator today. And with an extra
# reason of its own. Every assertion below pins something whose failure mode is a *plausible picture*: a map
# drawn from misread bytes, or from a stale index, does not throw and does not look broken. It looks like an
# answer. There is no visual regression test that can catch a constellation of the wrong 1,294 projects,
# because the right one and the wrong one are both dot clouds.
LOADMAP = body_of("loadMap")

# One guard for three binaries, borrowed and not repeated. `xy.bin` and `near.bin` are addressed by row
# ordinal exactly as `docs.bin` is, so an index built against a different `data.json` positions every dot
# confidently and wrongly. "live" is the only state in which the row count *and* the `nwo` fingerprint have
# both been checked; a copied guard is a guard that can drift out of agreement with the one it was copied
# from, which is the failure this shape exists to make impossible rather than merely unlikely.
true("loadMap() waits on the semantic index's own guard", "semanticReady()" in LOADMAP)
true("loadMap() decodes only when that guard came back live", 'SEM_STATE !== "live"' in LOADMAP)
true("loadMap() does not compute a second fingerprint",
     "subtle" not in LOADMAP and "sha" not in LOADMAP.lower())
# And `loadSemantic()` is reached only through `semanticReady()`. It is idempotent but was not *joinable*: a
# second caller arriving mid-`Promise.all` returned instantly from the `SEM_STATE` guard with nothing loaded,
# so a reader who opened the map while the search fetch was in flight got "the semantic index is loading" and
# a map that stayed off. Two occurrences: the declaration, and the one call inside the memo.
check("loadSemantic() is called only through semanticReady()", pagemin.strip_js(SRC).count("loadSemantic("), 2)

# Byte order, stated. A typed-array view over a raw `ArrayBuffer` reads it in the *platform's* order; the
# stage writes little-endian. `docs.bin` gets away with a bare `Int8Array` because one byte has no order --
# these are int16 and uint16 and do. Every machine anyone will read this on agrees today, which is what makes
# the assumption invisible: on a big-endian reader every coordinate and every neighbour would be a different,
# in-range, entirely wrong number. Asserted as both halves, because `getInt16(off)` without the `true` is the
# same defect written more legibly.
true("xy.bin is decoded through DataView, not a typed-array view over the buffer",
     "getInt16(" in LOADMAP and "new Int16Array(" not in LOADMAP)
true("near.bin is decoded through DataView too", "getUint16(" in LOADMAP)
check("every 16-bit read states little-endian", LOADMAP.count(", true)"), LOADMAP.count("getInt16(") + LOADMAP.count("getUint16("))

# Both files are sized against the corpus before a byte of either is read, and neighbour ordinals are bounds
# checked. An out-of-range ordinal indexes `x` as `undefined`, and a canvas discards a line to NaN in silence
# -- so a corrupt neighbour list would quietly draw fewer edges instead of failing, and the map would look
# thinner rather than wrong.
true("xy.bin's length is checked against the row count", "rows * 4" in LOADMAP)
true("near.bin's length is checked against rows and the neighbour count", "rows * n * 2" in LOADMAP)
true("a neighbour ordinal past the end of the corpus is refused", "v >= rows" in LOADMAP)
true("a degenerate layout is refused rather than drawn", "no extent" in LOADMAP)

# One scale for both axes, which is the stage's decision: `xy.bin` quantises x and y against a single
# `xy_scale` so that the layout's aspect ratio survives the quantisation. Normalising each axis to the stage
# separately would undo that -- the picture would fill the box, and every distance a reader is invited to read
# off it would be stretched in one direction. Silent, and it would look better, which is the danger.
check("one shared scale, applied to both axes", LOADMAP.count("SEM.xys / 32767"), 1)
true("neither axis is rescaled on its own",
     re.search(r"getInt16\(i \* 4, true\) \* s, b = dv\.getInt16\(i \* 4 \+ 2, true\) \* s", LOADMAP) is not None)

# The animation checks the preference in JavaScript. The stylesheet's blanket `prefers-reduced-motion` rule
# has no reach into a `requestAnimationFrame` loop -- it can stop a transition and cannot stop a camera.
true("the fly-to honours reduced motion in JavaScript, not by stylesheet",
     "prefers-reduced-motion" in body_of("mapFly"))
true("the fly-to also survives a browser with no requestAnimationFrame",
     "requestAnimationFrame" in body_of("mapFly"))

MAPPAINT = body_of("mapPaint")
# The map holds no state. It lights `HITS`, so every chip, the search box, a shared `#list=` and the saved set
# reach it for free and *cannot* disagree with it. A `state.map` would be a second copy of the truth.
true("the map draws whatever the table is drawing", "HITS" in MAPPAINT)
true("the map keeps no filter of its own", "state.map" not in pagemin.strip_js(SRC))
true("render() repaints the map on its way out", "mapRepaint()" in body_of("render"))
# Labels are sorted before they are capped. Capping first takes the first twelve rows in the reader's current
# sort order and labels the biggest of *those*: on "Name (A–Z)" the map would name the biggest project whose
# name starts with an early letter, which is a wrong answer that looks like a right one.
true("the labelled rows are sorted by size before the cap applies",
     MAPPAINT.index(".sort((a, b) => (b.stars || 0)") < MAPPAINT.index("drawn >= cap"))
true("the label cap is a named constant", re.search(r"^const MAP_LABELS = \d+;", SRC, re.M) is not None)
# ...and it is a ceiling on a stage-relative number, not the number itself. Twelve plates on a 375px map cover
# the dots they name. Asserted as both halves, because a floor with no ceiling names 30 projects on a desktop
# and a ceiling with no floor names none on a small one.
true("the label cap scales with the stage, between a floor and MAP_LABELS",
     re.search(r"Math\.max\(\d+, Math\.min\(MAP_LABELS, Math\.round\(w \* h / \d+\)\)\)", MAPPAINT) is not None)
# A canvas clips instead of wrapping, so a label placed right of a dot near the right edge is a word that
# stops with no ellipsis to say it stopped. Flipped to the other side, and dropped if neither side fits.
true("a label that would run off the canvas is flipped, then dropped rather than clipped",
     "box[0] + box[2] > w" in MAPPAINT and "box[0] < 0" in MAPPAINT)
# The camera follows the answer in both directions. Widening back to every row while the camera sat on a
# nine-row neighbourhood showed one dense corner of the atlas as if it were the atlas.
true("clearing a filter flies the camera back to the whole layout",
     re.search(r"mapFly\(box \? mapFrameOn\([^)]*\)\s*:\s*mapFrameOn\(MAP\.x0, MAP\.y0, MAP\.x1, MAP\.y1",
               body_of("mapRepaint")) is not None)
# Canvas colour parsing is not CSS colour parsing in one respect that matters: a string the canvas cannot
# parse is *ignored*, silently, and the previous fill is used. Space-separated `hsl(H S% L%)` is valid CSS and
# not accepted by every canvas implementation, so every colour built for a 2D context here is comma syntax.
# The failure is a picture drawn entirely in one colour, with nothing in the console.
true("canvas colours are built in comma syntax, which every 2D context parses",
     re.search(r'"hsl\(" \+ [A-Za-z0-9_.\[\]()]+ \+ " ', pagemin.strip_js(SRC)) is None)

# The readout is placed where it hides the least of what it is describing. A plate pinned down-right of the
# pointer sits on the neighbour edges the same plate is announcing -- "names 8 nearest" over five visible
# lines. Measured: 18 of 37 sampled hovers move off down-right and 26 neighbour dots stay visible because of
# it, so this is not a hypothetical. Both halves asserted: the four candidates, and the scoring against
# `near` rather than against, say, distance from the stage centre, which would not know what it was avoiding.
MAPTIP = body_of("mapTip")
true("the readout has four candidate corners rather than one",
     "[[1, 1], [-1, 1], [1, -1], [-1, -1]]" in MAPTIP)
true("...and picks between them by what each would cover of the eight it is describing",
     "MAP.near[i * MAP.n + k]" in MAPTIP and "hit < bestHit" in MAPTIP)

# The two pieces of context state the focus pass sets and must put back. `setLineDash` and `shadowBlur` are
# not per-path: a dash left set turns every ring below into a dotted circle, and a shadow left set gives all
# twelve label plates a coloured halo. Both look like a styling choice rather than a leak, which is why they
# are pinned here -- and both are set inside `if (focus >= 0)`, so the leak only appears on hover.
true("the dashed in-edges put the dash back", MAPPAINT.count("setLineDash(") == 2 and "setLineDash([])" in MAPPAINT)
true("the hub's glow puts the shadow back", "shadowBlur = 12" in MAPPAINT and "shadowBlur = 0" in MAPPAINT)
# Direction is carried by two channels, not one. Out-edges solid and in-edges faint *and* dashed, for the
# reason the comparison panel gives about colour-only marks: alpha is the first thing a dim screen takes away.
true("the in-edges differ from the out-edges in more than opacity",
     "setLineDash([3, 4])" in MAPPAINT and "globalAlpha = 0.22" in MAPPAINT)
# And the eight are hollow rather than merely ringed: filled with the stage's own colour, so "which dots are
# the eight" is answered by shape before colour. A ring on a dot that still reads as one of 1,294 filled dots
# is a mark the eye has to hunt for.
true("the named eight are drawn hollow, not just circled",
     re.search(r"ctx\.fillStyle = p\.plane;\s*ctx\.fill\(\);\s*ctx\.stroke\(\);", MAPPAINT) is not None)

# Off, it leaves nothing running and nothing fetched. `mapWire()` returns before it touches the dialog, which
# is what keeps the two binaries unrequested -- the markup ships either way.
true('mapWire() is gated on FLAGS["index.constellation"]', 'FLAGS["index.constellation"]' in body_of("mapWire"))
# `#mapnope` and `.mapkey` both declare a `display`, and `[hidden]` is a user-agent rule: any author `display`
# outranks it, so `hidden` would leave both boxes on screen. The shared-list strip has shipped this once.
true("the hidden map boxes override their own display",
     "#mapnope[hidden]" in CSS and ".mapkey[hidden]" in CSS)

print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
