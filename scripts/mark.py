"""Archie's head, for the top-left of every page's nav.

WHY THIS IS A MODULE AND NOT FIVE COPIES OF A STRING

Five generators write a `<header>` (`19_pages.py`, `20_landing.py`, `22_detail.py`, `25_collections.py`,
`flags_app.py`, and since then `31_home.py`, `32_local.py`, `33_alike.py` and `41_models_page.py`). They get
the mark and its CSS from here, so there is one drawing to change and one place to change it.

THE MARK IS THE CURRENT ARCHIE, NOT THE FIRST ONE

This used to draw the first Archie's face as vector: a gold globe wearing blocky pixel shades, the same object
the old `docs/favicon.svg` and `24_pwa.icon()` drew. The owner retired that character for the 3D Archie
(white ceramic, graphite crest with a lime streak, lime eyes), who is the one in the homepage masthead, the
README and the catalogue. The mark is now his icon tile, `docs/assets/archie-mark.webp`, cut by
`art/brand/build.py` from the owner's own `.github/readme/icon.png`, so the tab, the installed icon, the
README and the nav are one drawing again.

It stays an `<svg>` holding an `<image>` rather than becoming an `<img>`, so every `.mk svg` rule below -- the
30px box, `overflow:visible`, the drop-shadow that follows the tile's alpha and the breath -- applies to it
unchanged. The tile is a raster because he is a render: a hand-traced vector of a lit 3D head would be a
fourth drawing of him. The cost is one 3 KB request, cached after the first page; `width`/`height` on the
`<image>` hold its box, so nothing moves when it lands.

The tile carries its own dark plate, so it reads the same on the light and the dark theme without any token.
"""
from __future__ import annotations

# The file every page's mark points at, relative to the site root.
ASSET = "assets/archie-mark.webp"


def svg(up: str = "", cls: str = "mk") -> str:
    """The mark as an inline `<svg>` inside a `<span>`.

    `up` is the page's way back to the site root (`""` or `./` on the homepage, `../` one level down), the
    same prefix the brand link's `href` already is.
    """
    # `aria-hidden`, because every call site puts the word "Atlas" next to it. A logo that also announces
    # itself makes a screen reader say the name twice.
    return (f'<span class="{cls}" aria-hidden="true">'
            '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" focusable="false">'
            f'<image href="{up}{ASSET}" width="64" height="64"/></svg></span>')


def brand(href: str, label: str = "Atlas") -> str:
    """The mark and the site's name as one link home. This is the thing that goes top-left.

    `href` is the way home, which is also the prefix to the site root, so the mark's image resolves from the
    same string.
    """
    return f'<a class="brand" href="{href}">{svg(href)}<span>{label}</span></a>'


# One rule set, emitted by every generator that calls `brand()`.
#
# `drop-shadow` rather than `box-shadow`, because it follows rendered alpha: it lights the tile's rounded
# corners rather than the element's square border box. `overflow:visible` lets that glow spill past the
# 30px box. The glow is lime, Archie's trim and the theme's `--bar`; it was the first Archie's gold.
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
  filter:drop-shadow(0 0 calc(5px * var(--fx-glow,1)) rgba(164,200,18,.45));
  animation:mkbreath calc(6s * var(--fx-pulse,1)) ease-in-out infinite}
@keyframes mkbreath{
  0%,100%{filter:drop-shadow(0 0 calc(3px * var(--fx-glow,1)) rgba(164,200,18,.32))}
  50%{filter:drop-shadow(0 0 calc(9px * var(--fx-glow,1)) rgba(164,200,18,.60))}}
@media(prefers-reduced-motion:reduce){.mk svg{animation:none}}
"""
