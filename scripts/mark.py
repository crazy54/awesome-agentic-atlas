"""Archie's head, for the top-left of every page's nav.

WHY THIS IS A MODULE AND NOT FIVE COPIES OF A STRING

Five generators write a `<header>` (`19_pages.py`, `20_landing.py`, `22_detail.py`, `25_collections.py`,
`flags_app.py`, and since then `31_home.py`, `32_local.py`, `33_alike.py` and `41_models_page.py`). They get
the mark and its CSS from here, so there is one drawing to change and one place to change it.

THE MARK IS THE CURRENT ARCHIE, IN A RAISED DISC

The mark is his head alone, `docs/assets/archie-head.webp`, cut transparent by `art/brand/build.py` from the
owner's render (`.github/readme/archie.png`). The site is soft UI (see THE THEMES in `sitewide.py`), and in soft
UI an icon is not a tile with a plate of its own: it is seated on a disc of the page's own colour, extruded by
the same two shadows as every other control. So `.mk` is that disc and the head sits in it. The tab and the
installed icon keep his dark tile (`archie-mark.webp`'s source), which is what a launcher's own wallpaper needs.

It stays an `<svg>` holding an `<image>` rather than becoming an `<img>`, so `width`/`height` on the `<image>`
hold its box and nothing moves when the 4 KB file lands; it is cached after the first page.
"""
from __future__ import annotations

# The file every page's mark points at, relative to the site root.
ASSET = "assets/archie-head.webp"


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
# The disc is 30px, two more than the old 28px box, and the head inside it 24px. `inline-grid` plus a baseline
# nudge rather than `display:flex` on the `h1`, because the catalogue puts the mark inside its heading, and
# `probe.mjs` and `theme_test.py` both measure that heading.
#
# The breath is the lime's light around the disc, and it is a duration gate, not an opacity gate:
# `calc(6s * var(--fx-pulse))` with `--fx-pulse:0` computes to `0s`, and a zero-duration animation never
# enters `document.getAnimations()`. Hovering the brand lifts the disc, as every other control on the site.
CSS = """
.mk{display:inline-grid;place-items:center;width:30px;height:30px;flex:none;border-radius:50%;
  vertical-align:-8px;margin-right:4px;background:var(--surface);box-shadow:var(--raise-sm);position:relative;
  transition:box-shadow .16s ease}
.mk::after{content:"";position:absolute;inset:0;border-radius:50%;pointer-events:none;
  animation:mkbreath calc(6s * var(--fx-pulse,1)) ease-in-out infinite}
.brand{display:inline-flex;align-items:center;gap:9px;text-decoration:none;color:inherit;
  font-weight:650;letter-spacing:-.01em;white-space:nowrap}
.brand:hover span{text-decoration:underline}
.brand:hover .mk{box-shadow:var(--raise-hi)}
.brand:active .mk{box-shadow:var(--press)}
/* The brand's own line, on the page families that have no breadcrumb to sit in. Named rather than
   reusing `.crumb`, which is `22_detail.py`'s class and already carries a rule there: a shared
   stylesheet that redefines a generator's own selector wins or loses on source order, which is not a
   thing to leave to chance across four files. */
.brandbar{margin:0 0 14px}
.brand .mk{vertical-align:baseline;margin-right:0}
.mk svg{width:24px;height:24px;display:block;overflow:visible}
@keyframes mkbreath{
  0%,100%{box-shadow:0 0 0 rgba(164,200,18,0)}
  50%{box-shadow:0 0 calc(10px * var(--fx-glow,1)) rgba(164,200,18,.35)}}
@media(prefers-reduced-motion:reduce){.mk::after{animation:none}}
"""
