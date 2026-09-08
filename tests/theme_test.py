"""Contrast tests for the two theme blocks in `scripts/19_pages.py`.

The page's colours are thirteen CSS custom properties declared twice -- once on `:root` for dark and
once on `html[data-theme=light]`. Every ratio the comment beside them quotes was measured by hand, and
a comment is not a test: the previous palette's comments correctly recorded that its cyan measured
2.53:1 on white, and nothing in the repository would have noticed if someone had used it there anyway.

What makes this checkable rather than a matter of taste is that WCAG contrast is arithmetic on two hex
values. There is no rendering, no browser and no cache involved, so the whole of it runs from a cold
checkout in milliseconds.

The part worth explaining is the role map. A token's minimum depends on how the CSS uses it -- 4.5:1
for text, 3:1 for a focus ring or an icon -- and the roles are not guessable from the names: `--warn`
is text in four rules and a chip fill in a fifth, and `--bar` is never text on the page but IS text
inside the filter button's count badge, which inverts to `--onbar` behind it. So the roles are read out
of the stylesheet rather than hardcoded, by looking for `color:var(--x)` and `background:var(--x)`. If
a future edit stops using `--warn` as text, this file stops requiring 4.5 of it, and if a new rule
starts filling with `--good`, the `--onbar` pair appears on its own. A hardcoded map would have gone
stale exactly the way the prose did.

Run: python tests/theme_test.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

PAGE = Path(__file__).resolve().parent.parent / "scripts" / "19_pages.py"
SRC = PAGE.read_text(encoding="utf-8")

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


# Three fixed points, so a sign error in the formula above cannot pass silently. These are the values
# WCAG's own examples give, and they bracket the range: identical, maximal, and one in between that is
# easy to get wrong because both channels are mid-range.
check("black on white is 21:1", round(ratio("#000000", "#FFFFFF"), 2), 21.0)
check("a colour against itself is 1:1", round(ratio("#438BB1", "#438BB1"), 2), 1.0)
check("#777 on white is 4.48:1", round(ratio("#777777", "#FFFFFF"), 2), 4.48)
check("shorthand hex expands", ratio("#fff", "#000000"), ratio("#FFFFFF", "#000000"))

# ---------------------------------------------------------------- parse the two blocks
TOKEN = re.compile(r"--([a-z0-9]+)\s*:\s*(#[0-9a-fA-F]{3,6})\s*;")


def block(selector: str) -> dict[str, str]:
    """The declarations of one rule, by selector, from the page template."""
    i = SRC.index(selector)
    body = SRC[i + len(selector):SRC.index("}", i)]
    return {k: v.upper() for k, v in TOKEN.findall(body)}


DARK = block(":root{")
LIGHT = block("html[data-theme=light]{")

check("dark declares 13 tokens", len(DARK), 13)
check("light declares 13 tokens", len(LIGHT), 13)
check("both modes declare the same tokens", sorted(DARK), sorted(LIGHT))
# Not a style rule. `var(--x)` with no fallback resolves to nothing when the token is missing, so a
# token present in one block and absent from the other renders as an unstyled element in that one mode
# only -- the failure that is hardest to see, because the mode you are looking at is fine.
for name in sorted(set(DARK) | set(LIGHT)):
    true(f"--{name} is declared in both modes", name in DARK and name in LIGHT)

BACKDROPS = ("surface", "plane", "band")
for mode, T in (("dark", DARK), ("light", LIGHT)):
    for b in BACKDROPS:
        true(f"{mode} declares --{b}", b in T)
    true(f"{mode} declares --onbar", "onbar" in T)

# ---------------------------------------------------------------- roles, read from the CSS
# The template is one long string in this file, so the stylesheet is just text here. That is enough:
# the question is only which tokens appear after `color:` and which after `background:`.
def used_as(prop: str) -> set[str]:
    return set(re.findall(rf"{prop}\s*:\s*var\(--([a-z0-9]+)\)", SRC))


AS_TEXT = used_as("color")
AS_FILL = used_as("background") | set(re.findall(r"background\s*:\s*var\(--([a-z0-9]+)\)", SRC))
AS_STROKE = set(re.findall(r"(?:outline|border|border-color|box-shadow)[^;{}]*var\(--([a-z0-9]+)\)", SRC))
AS_STROKE |= set(re.findall(r"fill\s*:\s*var\(--([a-z0-9]+)\)", SRC))

# The map has to have found something, or every assertion below vacuously passes -- the failure mode
# this whole file exists to avoid. These four are the ones the stylesheet certainly uses each way.
true("the role map found text tokens", {"ink", "muted", "link"} <= AS_TEXT)
true("the role map found fill tokens", {"bar", "warn", "good"} <= AS_FILL)
true("the role map found stroke tokens", "bar" in AS_STROKE)
true("--onbar is only ever ink on a fill", "onbar" in AS_TEXT)

# The backdrops themselves are fills; excluded so we do not demand a surface contrast against itself.
TEXT = sorted(AS_TEXT - set(BACKDROPS) - {"onbar", "grid"})
FILL = sorted(AS_FILL - set(BACKDROPS) - {"onbar", "grid"})

# ---------------------------------------------------------------- the assertions
BODY, LARGE = 4.5, 3.0
for mode, T in (("dark", DARK), ("light", LIGHT)):
    # Every token drawn as text, on every backdrop it can land on. Which backdrop a given rule actually
    # uses is not tracked, and deliberately: rows are striped, cards sit on the plane, and the same
    # `.stale` span appears in a table row and in a card. Requiring all three is the honest reading.
    for tok in TEXT:
        if tok not in T:
            continue
        for b in BACKDROPS:
            atleast(f"{mode}: --{tok} as text on --{b}", ratio(T[tok], T[b]), BODY)

    # Every token used as a fill has to carry --onbar. This is the pair the previous theme got right
    # for the wrong reason and the pair a re-theme is most likely to break, because it is the only one
    # where making the accent *more* legible on the page makes the ink on it *less* legible.
    for tok in FILL:
        if tok not in T:
            continue
        atleast(f"{mode}: --onbar as ink on filled --{tok}", ratio(T["onbar"], T[tok]), BODY)

    # `#fbt.act #fbn` inverts: --onbar becomes the background and --bar the text on it. Asserted by
    # name rather than derived, because it is the one rule in the stylesheet that swaps the pair, and a
    # role map built from `color:`/`background:` counts both halves without noticing they are the same
    # two colours changing places.
    atleast(f"{mode}: --bar as text on --onbar (the count badge inverts)",
            ratio(T["bar"], T["onbar"]), BODY)

    # Rings, borders and the two-tone icon: not text, so 3:1 -- WCAG 1.4.11 for non-text contrast.
    #
    # --onbar is excluded, and not because it is inconvenient. It is in the stroke set legitimately --
    # `.newchip[aria-pressed=true] .ni` fills the icon with it -- but that icon is inside a pressed chip,
    # so its backdrop is the chip's fill and never the page. Measuring it against --surface asks whether
    # black ink is visible on black, which it is not, and which nothing draws.
    for tok in sorted(AS_STROKE - set(BACKDROPS) - {"grid", "ink", "onbar"}):
        if tok not in T:
            continue
        for b in BACKDROPS:
            atleast(f"{mode}: --{tok} as a stroke on --{b}", ratio(T[tok], T[b]), LARGE)

    # The backdrop --onbar actually has: each fill. 3:1 rather than 4.5 because this is the icon rather
    # than the label, though every fill here clears the text floor anyway.
    for tok in FILL:
        if tok in T:
            atleast(f"{mode}: --onbar as an icon on filled --{tok}", ratio(T["onbar"], T[tok]), LARGE)

    # Borders that separate two panels rather than carrying meaning, so no WCAG minimum applies and the
    # floor has to come from somewhere else. 1.15 is calibrated, not chosen: the palette this replaces
    # shipped for months with its worst border pair at 1.168 (dark --grid on --band), and the episode
    # recorded beside the palette -- a selected row that vanished into its own background -- measured
    # 1.05. So 1.15 sits below what has demonstrably been acceptable and above what was demonstrably
    # broken. Worth stating that this palette is the better of the two on this axis: its worst pair is
    # 1.224 against the old theme's 1.168, and an earlier draft of this file failed it at a floor of
    # 1.25 that nothing in the repository's history would have passed.
    for b in BACKDROPS:
        atleast(f"{mode}: --grid is visible on --{b}", ratio(T["grid"], T[b]), 1.15)
    atleast(f"{mode}: --plane is distinguishable from --surface", ratio(T["plane"], T["surface"]), 1.03)

    # The brief for this palette: dark is black-backed with white ink, light inverts that.
    want = "#000000" if mode == "dark" else "#F1F0F3"
    check(f"{mode}: --surface is the intended base", T["surface"], want)
    check(f"{mode}: --ink is {'white' if mode == 'dark' else 'black'}",
          T["ink"], "#FFFFFF" if mode == "dark" else "#000000")

# ---------------------------------------------------------------- the two literals that duplicate --plane
# The pre-paint script sets `theme-color` before the stylesheet is parsed, so it cannot read the
# computed value and hardcodes both. They are the one place in the page where a colour is written twice,
# and a re-theme that misses them leaves the browser chrome on the old palette for the first frame.
head = SRC[:SRC.index(":root{")]
for mode, T in (("dark", DARK), ("light", LIGHT)):
    true(f"the pre-paint script's {mode} literal matches --plane", T["plane"] in head.upper())
true("the <meta> theme-color matches dark --plane",
     re.search(r'name="theme-color"[^>]*content="([^"]+)"', SRC).group(1).upper() == DARK["plane"])

# ---------------------------------------------------------------- can this file go red
# A harness that cannot fail is decoration. Perturb one value and confirm the same assertions reject
# it: Plum at its supplied value, which is the specific thing the comment beside the palette says had
# to be lifted because black ink on it measures only 4.22:1.
supplied_plum = "#BE379C"
atleast("sanity: the shipped --bar carries black ink", ratio(DARK["onbar"], DARK["bar"]), BODY)
check("sanity: unlifted Plum would NOT carry black ink",
      ratio("#000000", supplied_plum) >= BODY, False)
check("sanity: unlifted Plum fails as text on --band too",
      ratio(supplied_plum, DARK["band"]) >= BODY, False)
# And the reverse: the value that would fail is genuinely close, so the test is measuring rather than
# rejecting anything unfamiliar.
check("sanity: unlifted Plum is close, not absurd", round(ratio("#000000", supplied_plum), 2), 4.22)

# ---------------------------------------------------------------- the four copies of the palette
# The palette is declared in one place and copied to three others, and every one of those copies is a
# separate file a reader can land on. `20_landing.py` writes the facet pages, `22_detail.py` the 1,294
# per-repo pages, and both carry a comment saying their two blocks are `19_pages.py`'s character for
# character. That comment is the promise; this is the only thing that keeps it. The alternative -- one
# shared stylesheet -- is a real option and was not taken, because these stages already write their CSS to
# separate files that different pages link, and merging them is a bigger change than the re-theme that
# surfaced the problem. Copies are acceptable only while something compares them.
SCRIPTS = PAGE.parent


def palette_text(name: str) -> str:
    """The two rules verbatim, from `:root{` to the close of the light block."""
    src = (SCRIPTS / name).read_text(encoding="utf-8")
    i = src.index(":root{")
    j = src.index("}", src.index("html[data-theme=light]{")) + 1
    return src[i:j]


CANON = palette_text("19_pages.py")
true("the canonical block is not empty", len(CANON) > 200)
for follower in ("20_landing.py", "22_detail.py"):
    check(f"{follower} declares the palette byte for byte as 19_pages.py does",
          palette_text(follower), CANON)

# `23_og.py` renders a social card as a standalone document with no stylesheet to inherit from. Its CSS
# is formatted with the module's `PALETTE`, which is also included in the card cache signature; read that
# source-of-truth object rather than looking for literals in the template that now contains placeholders.
# A value outside the page palette is still the drift this checks for.
OG = (SCRIPTS / "23_og.py").read_text(encoding="utf-8")
palette_source = OG[OG.index("PALETTE = {"):OG.index("}\n", OG.index("PALETTE = {")) + 2]


def norm(h: str) -> str:
    h = h.lstrip("#").upper()
    return "#" + ("".join(c * 2 for c in h) if len(h) == 3 else h)


og_hex = {norm(h) for h in re.findall(r'"(#[0-9a-fA-F]{3,6})"', palette_source)}
true("the OG card's palette object was found", len(og_hex) >= 5)
for h in sorted(og_hex):
    true(f"the OG card's {h} is a dark-palette value", h in set(DARK.values()))
# And that it is the *dark* palette, not the light one it would also parse against. Light `--ink` is
# black, so a card that had picked up the light block would still be "all palette values" while rendering
# black text on a black plate.
true("the OG card is drawn in the dark palette", norm("#000000") in og_hex and DARK["surface"] == "#000000")

# `24_pwa.py` draws the installed-app icon and writes the manifest, and its colours are Python tuples
# rather than CSS, so no amount of grepping for hex finds them. Asserted by name against the tokens they
# are meant to be. The manifest pair is the one that had a real defect: it declared `--surface` while the
# page's `<meta name="theme-color">` declares `--plane`, so an installed window's chrome changed colour
# between the launch frame and first paint.
PWA = (SCRIPTS / "24_pwa.py").read_text(encoding="utf-8")


def tup(name: str) -> str:
    m = re.search(rf"^{name} = \((0x[0-9A-Fa-f]{{2}}), (0x[0-9A-Fa-f]{{2}}), (0x[0-9A-Fa-f]{{2}})\)$",
                  PWA, re.M)
    return "#%02X%02X%02X" % tuple(int(g, 16) for g in m.groups()) if m else "NOT FOUND"


for const, token in (("SURFACE", "surface"), ("PLANE", "plane"), ("BAR", "bar"), ("RING", "ink")):
    check(f"24_pwa.py's {const} is dark --{token}", tup(const), DARK[token])
true("the manifest's two colours are PLANE, so they match the page's theme-color",
     PWA.count('"#%02x%02x%02x" % PLANE') == 2)

# The icon's two shapes have to be two shapes. Not a WCAG rule -- a launcher icon is not text -- but the
# reason the ring is `--ink` rather than the second accent, and the assertion is what stops a later edit
# from "restoring" the accent without knowing why it went. Every accent in this palette was fitted to
# clear 4.5:1 on black without going lighter than it had to, so they converged to within 1.01:1 of each
# other: a globe and a ring picked from them differ by hue alone, which is nothing in a monochrome icon
# slot. 3:1 is the non-text floor and the pair measures 3.81:1.
atleast("the icon's ring and globe are separable without colour", ratio(tup("RING"), tup("BAR")), LARGE)
for pair in (("bar", "warn"), ("bar", "link"), ("warn", "link")):
    a, b = pair
    check(f"sanity: --{a} and --{b} are within 1.05:1, which is why the ring is not an accent",
          ratio(DARK[a], DARK[b]) < 1.05, True)

print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
