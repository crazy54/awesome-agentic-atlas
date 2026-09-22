"""Archie's globe, as inline SVG, for the top-left of every page's nav.

WHY THIS IS A MODULE AND NOT FIVE COPIES OF A STRING

The mark already existed twice in this repository before this file: `docs/favicon.svg` is the vector the tab
shows, and `scripts/24_pwa.py:icon()` rasterises the same object for the installed app icon. Neither was
reachable from a page's markup, so the site's own header showed no mark at all -- the index led with a bare
`<h1>Awesome Agentic Atlas</h1>` and a project page led with the project's name behind a text-only "Atlas"
crumb. A site whose tab and whose installed icon show a logo its pages do not is a site with a favicon, not
a logo.

Five generators write a `<header>` (`19_pages.py`, `20_landing.py`, `22_detail.py`, `25_collections.py`,
`flags_app.py`). They get the drawing and its CSS from here, so there is one geometry to change and one
place to change it. `tests/theme_test.py` already enforces this shape for the palette by asserting three
generators' `:root{...}` blocks are byte-identical; the same argument applies to the logo, and a function
is a stronger guarantee than an assertion about copies.

THE COLOURS ARE LITERAL, AND THAT IS DELIBERATE

Every other drawing on these pages is tokenised. This one is not, and the reason is measurable: `--bar` is
`#D6A034` in dark and `#6557C8` in light. A `var(--bar)` globe is gold in the tab and purple in the header
of the same page, which is two logos. `favicon.svg`'s literal values keep one. They also need no theme
support to stay legible, because every dark feature is drawn *on* the globe rather than on the page: the
gold disc is the background for the grid, the shades and the smile, so the surrounding surface can be
`#090A0D` or `#F2F4F7` without touching any contrast inside the mark.

The one thing that does vary is the glow, which is a skin's business rather than a palette's, so it reads
`--fx-glow` and defaults to 1 where no skin has set it.

THE SIZE LADDER IS WHY THERE ARE TWO VARIANTS

Shot at 16/20/26/32/48/96, the faithful drawing -- rounded plate, six grid lines, antenna -- is superb from
48 up and unusable below 32: the grid collapses onto the shades and the whole thing reads as a carved
pumpkin, which is not a subtle failure. A nav mark is 28-32px, so `compact=True` is what a nav gets. It
removes what the context already provides and enlarges what carries the identity: the plate goes, because
the header *is* the plate; the globe grows 1.34x about its own centre, the largest scale at which it still
clears the antenna's ball; the grid drops from six lines to the equator and one meridian. The antenna is
re-placed by hand rather than scaled, because scaling it about the globe's centre throws the ball to
y=-4.4, outside the viewBox entirely.
"""
from __future__ import annotations

# Straight from `docs/favicon.svg`. Named rather than inlined so a diff against that file is a diff of five
# values, not of nine path elements.
PLATE = "#090A0D"     # the rounded plate, and the shades' frame
EDGE = "#3A414D"      # the plate's hairline
GLOBE = "#D6A034"     # the disc, and the antenna's stalk
GRID = "#20242D"      # meridians and parallels, drawn on the disc
LIGHT = "#F7F8FA"     # the lenses and the antenna's ball

_FULL_GRID = "M12 31h40M32 11v40M17 21h30M17 41h30M23 13c-6 11-6 25 0 36M41 13c6 11 6 25 0 36"
_LEAN_GRID = "M12 31h40M32 11v40"


def svg(compact: bool = True, cls: str = "mk") -> str:
    """The mark as an inline `<svg>` inside a `<span>`.

    Inline rather than an `<img src="favicon.svg">` because an `<img>` cannot take the drop-shadow that
    follows the silhouette -- see `CSS` -- and because a nav mark that arrives on a second request is a nav
    mark that pops in after first paint. It costs about 700 bytes a page.
    """
    grid = _LEAN_GRID if compact else _FULL_GRID
    face = (
        f'<circle cx="32" cy="31" r="20" fill="{GLOBE}"/>'
        f'<path d="{grid}" fill="none" stroke="{GRID}" stroke-width="2" '
        f'opacity="{".55" if compact else ".9"}"/>'
        f'<path d="M11 22h17v4h4v-4h21v14h-4v4H34v-4h-4v4H15v-4h-4z" fill="{PLATE}"/>'
        f'<path d="M16 25h4v4h4v4h-4v-4h-4zm22 0h4v4h4v4h-4v-4h-4z" fill="{LIGHT}"/>'
        f'<path d="M25 47c4 3 10 3 14 0" fill="none" stroke="{PLATE}" stroke-width="2.5" '
        f'stroke-linecap="round"/>')
    if compact:
        body = (f'<path d="M48 13.5l5.5-6.5" fill="none" stroke="{GLOBE}" stroke-width="3.4" '
                f'stroke-linecap="round"/>'
                f'<circle cx="55" cy="5" r="3.4" fill="{LIGHT}" stroke="{GLOBE}" stroke-width="2.2"/>'
                f'<g transform="translate(32 31) scale(1.34) translate(-32 -31)">{face}</g>')
    else:
        body = (f'<rect x="4" y="5" width="56" height="55" rx="16" fill="{PLATE}" '
                f'stroke="{EDGE}" stroke-width="2"/>'
                f'<path d="M42 10l5-6" fill="none" stroke="{GLOBE}" stroke-width="3" '
                f'stroke-linecap="round"/>'
                f'<circle cx="49" cy="3.8" r="3" fill="{LIGHT}" stroke="{GLOBE}" stroke-width="2"/>'
                + face)
    # `aria-hidden`, because every call site puts the word "Atlas" next to it. A logo that also announces
    # itself makes a screen reader say the name twice.
    return (f'<span class="{cls}" aria-hidden="true">'
            '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" focusable="false">'
            f'{body}</svg></span>')


def brand(href: str, label: str = "Atlas", compact: bool = True) -> str:
    """The mark and the site's name as one link home. This is the thing that goes top-left."""
    return f'<a class="brand" href="{href}">{svg(compact)}<span>{label}</span></a>'


# One rule set, emitted by every generator that calls `brand()`.
#
# `overflow:visible` on the `<svg>` and `drop-shadow` rather than `box-shadow` are the same decision twice.
# The compact mark has no plate, so its silhouette is a disc with an antenna sticking out past the top-right
# of the viewBox; `box-shadow` traces the element's border box and drew a square halo around a tile that is
# not there, while `drop-shadow` follows rendered alpha and lights the actual shape. `overflow:visible` is
# what stops the antenna's ball being clipped by the 30px box.
#
# The breath is a duration gate, not an opacity gate: `calc(6s * var(--fx-pulse))` with `--fx-pulse:0`
# computes to `0s`, and a zero-duration animation never enters `document.getAnimations()`. An opacity gate
# leaves the animation running and invisible, which is a thing a battery notices.
# `.mk` is styled on its own rather than as `.brand .mk`, because the index's own `<h1>` *is* the brand --
# "Awesome Agentic Atlas" is already the top-left text -- so there the mark goes inside the heading and
# there is no `.brand` to descend from. `inline-grid` plus a baseline nudge rather than `display:flex` on
# the `h1`, because `probe.mjs` and `theme_test.py` both measure that heading and changing its formatting
# context to flex moves the trailing `<span>` it asserts about.
CSS = """
.mk{display:inline-grid;place-items:center;width:28px;height:28px;flex:none;
  vertical-align:-7px;margin-right:2px}
.brand{display:inline-flex;align-items:center;gap:7px;text-decoration:none;color:inherit;
  font-weight:600;letter-spacing:-.01em;white-space:nowrap}
.brand:hover span{text-decoration:underline}
/* The brand's own line, on the page families that have no breadcrumb to sit in. Named rather than
   reusing `.crumb`, which is `22_detail.py`'s class and already carries a rule there: a shared
   stylesheet that redefines a generator's own selector wins or loses on source order, which is not a
   thing to leave to chance across four files. */
.brandbar{margin:0 0 14px}
.brand .mk{vertical-align:baseline;margin-right:0}
.mk svg{width:30px;height:30px;display:block;overflow:visible;
  filter:drop-shadow(0 0 calc(5px * var(--fx-glow,1)) rgba(214,160,52,.45));
  animation:mkbreath calc(6s * var(--fx-pulse,1)) ease-in-out infinite}
@keyframes mkbreath{
  0%,100%{filter:drop-shadow(0 0 calc(3px * var(--fx-glow,1)) rgba(214,160,52,.32))}
  50%{filter:drop-shadow(0 0 calc(9px * var(--fx-glow,1)) rgba(214,160,52,.60))}}
@media(prefers-reduced-motion:reduce){.mk svg{animation:none}}
"""
