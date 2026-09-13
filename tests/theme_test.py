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
import struct
import sys
import zlib
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

    # The visual brief is graphite rather than absolute black and soft grey rather than absolute white.
    # Pinning the two endpoints catches the real regression this pass is for: a reader that receives the
    # old stark base while all the intermediate colours still happen to clear contrast.
    want_surface = "#090A0D" if mode == "dark" else "#F2F4F7"
    want_ink = "#F7F8FA" if mode == "dark" else "#14171C"
    check(f"{mode}: --surface is the intended graphite/soft-grey base", T["surface"], want_surface)
    check(f"{mode}: --ink is the intended softened foreground", T["ink"], want_ink)
    check(f"{mode}: --bar is the approved action colour", T["bar"],
          "#D6A034" if mode == "dark" else "#6557C8")
    check(f"{mode}: --warn stays distinct from the action colour", T["warn"],
          "#EF7D86" if mode == "dark" else "#875A19")

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
true("the OG card is drawn in the dark palette",
     DARK["surface"] in og_hex and DARK["surface"] == "#090A0D")

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

# The orbit sits outside the globe with a visible gap, so the boundary each shape actually shares is with
# the plate, not with the other colour. Requiring ring-vs-globe contrast would reject a brighter accent for
# a boundary the renderer never draws while failing to test the two boundaries it does draw.
atleast("the icon's ring is visible on its plate", ratio(tup("RING"), tup("SURFACE")), LARGE)
atleast("the icon's globe is visible on its plate", ratio(tup("BAR"), tup("SURFACE")), LARGE)


def png_pixel(path: Path, x: int, y: int) -> str:
    """Read one pixel from the generator's deliberately simple filter-0 RGBA PNG."""
    data = path.read_bytes()
    width, height = struct.unpack(">II", data[16:24])
    pos, compressed = 8, bytearray()
    while pos < len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        kind = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + length]
        if kind == b"IDAT":
            compressed.extend(body)
        pos += length + 12
    raw = zlib.decompress(compressed)
    stride = width * 4 + 1
    assert width == height == 192 and raw[y * stride] == 0
    start = y * stride + 1 + x * 4
    return "#" + bytes(raw[start:start + 3]).hex().upper()


# The old app icon was only a globe. These two pixels sit inside that globe but away from every grid line:
# together they prove that Archie's black pixel shades and white checker glint made it into the actual
# generated PNG a launcher installs, not merely into a source comment or the browser-tab SVG.
ICON_192 = PAGE.parent.parent / "docs" / "icon-192.png"
check("the installed icon wears Archie's dark pixel shades",
      png_pixel(ICON_192, 115, 84), DARK["surface"])
check("the installed icon carries the shades' white checker glint",
      png_pixel(ICON_192, 58, 77), DARK["ink"])

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
    found = re.search(r"html\[data-view=cards\] td\." + re.escape(cell) + r"\{grid-row:(\d)", CARD)
    check("the phone card puts td." + cell + " on grid row " + row, found and found.group(1), row)

DESKTOP_PJ = SRC.index("html[data-view=cards] td.pj{grid-column")
true("the phone card order is emitted after the cards block whose selectors it repeats",
     SRC.index(PHONE, DESKTOP_PJ + 1) > DESKTOP_PJ)

# Untouched on purpose. These carry two attributes and outrank the phone rules at every width, so a reader
# who turned the screenshots off keeps the order that was designed for not having them -- rank, then name.
check("the screenshots-off card order is left as it was",
      [re.search(r"html\[data-view=cards\]\[data-index-screenshots=off\] td\." + c + r"\{grid-row:(\d)",
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
# checkable without a build is the source, so that is what this reads. `cards-check.mjs` gains the layout
# assertions once a build has landed; the note on JFH-291 says so.
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
atleast("the comparison panel's rules are where this file expects them", len(CMP_RULES), 18)

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

# The display types the two view blocks take away, restated. This is the actual defect: not one of these is
# decoration, and a panel missing any one of them is a comparison a phone reader cannot read.
for selector, value in (("table", "table"), ("thead", "table-header-group"),
                        ("tbody", "table-row-group"), ("tr", "table-row")):
    true("the panel's " + selector + " is restored to display:" + value,
         re.search(r"^#cmp " + selector + r"\{[^}]*display:" + value + r"\b", CSS, re.M) is not None)
true("the panel's cells are restored to display:table-cell",
     re.search(r"^#cmp th,#cmp td\{[^}]*display:table-cell\b", CSS, re.M) is not None)
# 148px is what makes the scroller a scroller: four of them plus the 104px label rail is 696px, so a 375px
# phone has real width to swipe. The cards view sets `min-width:0` on every cell, which is right for a card
# that must not push its grid track wider and is exactly wrong for a column somebody is trying to read.
true("the panel's cells carry a width floor, which is what the cards view zeroed",
     re.search(r"^#cmp td\{[^}]*min-width:1\d\dpx", CSS, re.M) is not None)
# The row labels are what make four columns usable at 375px, and a sticky cell with a transparent background
# has the cells sliding under it show through.
true("the row labels are sticky and opaque",
     re.search(r"^#cmp tbody th\{[^}]*position:sticky[^}]*background:var\(--", CSS, re.M) is not None)
# Three rules paint a row on this page -- table view stripes alternate rows and tints the row under the
# pointer, the cards view glows the row holding focus -- and all three are about a list being scanned. A
# comparison whose cells change colour as the mouse crosses them is harder to read, not easier.
true("no view's row paint reaches the panel",
     re.search(r"^#cmp tbody td\{[^}]*background:transparent", CSS, re.M) is not None
     and re.search(r"^#cmp tr:hover,#cmp tr:focus-within\{[^}]*box-shadow:none", CSS, re.M) is not None)

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
for control in ("#cmp .ch .sp", "#cmp .unpin", ".pin"):
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

print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
