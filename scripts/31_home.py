#!/usr/bin/env python3
"""The homepage: browse and discover.

  python scripts/31_home.py                 write docs/index.html
  python scripts/31_home.py --out DIR       write DIR/index.html instead, for a preview

WHAT THIS PAGE IS FOR, AND WHAT IT REPLACES

Until this stage existed, `/` was the catalogue: a search field, a sort menu, five filter rails and a
table of 8,858 rows drawn by script out of a 569 KB `data.json`. That page is good at one job -- a reader
who knows what they are looking for -- and structurally incapable of the other one, because a first screen
ordered by stars is the same thirty projects every day and the remaining 8,828 are unreachable without a
query. The catalogue is still there, at `/catalog/`, and the masthead links to it. What is here instead is
a page made of shelves, each one with a stated reason for existing, so that arriving with no query is a
thing a reader can usefully do.

It is also lighter than what it replaces, which was not the goal but is worth stating because it is the
kind of claim that gets assumed backwards: `/` used to ship ~142 KB of HTML and then fetch 569 KB of
`data.json` before it could draw a single row. This page ships everything it draws and fetches nothing.

WHY THIS STAGE IMPORTS THE PROTOTYPE

Every shelf, every card face and every gradient here comes from `scripts/30_v2.py` by import. That file
was built as a design prototype under `docs/v2/`, and three properties are what make importing it the
right answer rather than a shortcut:

  * It reads the committed `docs/data.json`, so it computes the real 8,858-row corpus on a checkout.
  * It has no import side effects -- every write is under its `if __name__ == "__main__"` -- so loading it
    costs a parse and nothing else.
  * `shelf_defs()` already measures each shelf's pool from the data rather than asserting a number, which
    is the property that makes a shelf's prose honest.

So this file is a re-targeting layer, not a port. It changes exactly three things about the prototype's
output and everything else is called: where a card points, which bands appear and in what order, and which
palette the tokens resolve against. A port would have been ~800 lines of copied drawing code with a second
set of the same bugs.

The honest cost of that choice, recorded rather than glossed: a file written as a prototype is now
load-bearing for the site's front page. The right end state is the card system in a module of its own that
both this stage and `30_v2.py` import, and the reason to do that *after* the search views rather than now
is that the search page needs the console and the facet rail out of the same file -- the real surface area
is not known until then, and a module extracted against one caller is usually the wrong module.

THE THREE THINGS THAT CHANGE

  1. `detail_href` is rebound to `20_landing.repo_path`, so every card on this page points at the canonical
     `repo/<owner>/<name>/` the site publishes rather than the prototype's flat `repo/<owner>/<name>.html`.
     One module-level name, because `face()` calls it by that name -- see `RETARGET` below.
  2. The band order is this file's, not `shelves_html()`'s: spotlight, then the topic chips, then the day's
     Discover picks, then the shelves, then the coverage arithmetic. Discover sits in the first shelf slot
     because that is where it was asked for, and the prototype has no opinion about it -- it predates the
     feature.
  3. The palette is the site's eight token sets out of `pages.css`, not the prototype's three skins. That
     is what `BRIDGE_CSS` is for, and it is the only CSS in this file that is not either imported or a
     handful of rules for a band the prototype does not have.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import html
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUT = ROOT / "docs"

# Legal identifiers, so they need only `scripts/` on the path -- the same two lines `20_landing.py` uses,
# and for the same reason: `python scripts/31_home.py` provides it and a test that loads this module by
# file path does not.
sys.path.insert(0, str(HERE))
import mark  # noqa: E402
import pagemin  # noqa: E402


def _load(name: str, alias: str):
    """The dynamic load every stage here uses, because `19_pages` is not an identifier.

    Reuse of an already-loaded copy matters more in this file than in the others: `20_landing.py` loads
    `19_pages.py` itself, so without the `sys.modules` check the 6,400-line template would be parsed twice
    in one process under two module objects -- wasteful, and wrong for anything that caches at module
    level. All three targets do their work under `if __name__`, so none of this runs a build.
    """
    if alias in sys.modules:
        return sys.modules[alias]
    spec = importlib.util.spec_from_file_location(alias, HERE / name)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[alias] = mod
    spec.loader.exec_module(mod)
    return mod


# What each one is here for. `19_pages.py`: the Settings control, in the three pieces it was lifted into so
# that a second page could use it, and the analytics beacon. `20_landing.py`: the pre-paint theme script and
# the one rule that turns an `nwo` into a detail-page path. `30_v2.py`: the entire card and shelf system.
b19 = _load("19_pages.py", "b19")
b20 = _load("20_landing.py", "b20")
b30 = _load("30_v2.py", "b30")

SITE = b20.SITE
REPO = b20.REPO
LISTS = b20.LISTS
DATA = b30.DATA
ROWS = b30.ROWS
esc = b20.esc

# RETARGET. The prototype's detail pages are flat files under `docs/v2/repo/`; the site's are directories
# under `docs/repo/`, slugged by a rule that `22_detail.py` owns and `20_landing.repo_path` states. Rebound
# on the module rather than passed as an argument because `face()` calls `detail_href(row)` by that global
# name, which makes this one assignment the only seam needed to redirect every card the prototype can draw
# -- posters, the hero, the dossier, all of them.
#
# Asserted rather than assumed, immediately below, because a rename in either file would otherwise turn
# every link on the front page into a 404 silently: the page would build, the cards would draw, and the
# hrefs would be wrong.
b30.detail_href = lambda row: b20.repo_path(b30.g(row, "nwo"))
_probe = b30.face(ROWS[0])["href"]
assert _probe.startswith("repo/") and _probe.endswith("/"), f"detail_href did not retarget: {_probe}"
assert ".html" not in _probe, f"detail_href still points at a flat file: {_probe}"

# Where each day's Discover cards are published for the band to swap in after midnight -- see
# `day_fragments()`. Under `discover/` because they are that page's plan drawn as this page's cards, and JSON
# rather than `.html` so nothing that walks the site's pages mistakes a fragment for one.
CARDS_DIR = "discover/cards"

# The published plan, read rather than recomputed. `19d_discover.py` writes it and `docs/discover/` draws
# from it, so reading the same file is what makes the band and the page agree about what today's set is;
# calling `discover.plan()` again here would be a second scheduler run whose only job is to produce the
# same answer, and it would write a ledger this stage has no business touching.
PLAN = json.loads((OUT / "discover.json").read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------------------------------
# THE TOKEN BRIDGE
#
# The prototype names 41 palette tokens; `pages.css` names 22, and 19 of those are the same name for the
# same thing, because the site's four themes were built out of the prototype's vocabulary. This block is
# the other 22, and it is the whole of the palette work -- with it in place, 141 imported selectors draw
# in graphite, glass, terminal and prism, light and dark, without one of them knowing a theme exists.
#
# Three kinds of token, and the kind decides where the value comes from:
#
#   * An alias. `--field` is the site's `--wash`; `--panel-b` is the site's `--grid`; `--accent-slate` is
#     `--muted`. These follow all eight sets for free and are the reason this block is short.
#   * A geometry or a typeface. A 14px radius and a hairline do not change when the lights go out, so they
#     are declared once on `:root` and never per theme. `--num` is the UI font rather than a second family:
#     the site has one typeface per theme and a numeral stack that disagreed with it would show up as a
#     wobble in every star count.
#   * A shadow or a scrim. Colour-bearing but not contrast-bearing -- nothing is read *through* them -- so
#     they are declared per *mode* rather than per theme. A drop shadow in a light theme is a soft grey and
#     in a dark one is nearly black, and that is two values, not eight.
#
# Fifteen, not the twenty-two an inventory of the prototype's palette suggests, and the difference is worth
# recording because it was measured rather than guessed. Seven of that twenty-two are read only by
# `BASE_CSS`, which this page replaces with `pages.css` and therefore never loads -- `--blur`,
# `--accent-slate`, `--shadow`, `--fx-sheen` and `--fx-lift` among them. Declaring a token nothing reads is
# not free: it is a line a future reader has to check against a rule that does not exist.
#
# Ten more tokens the imported rules read are defined nowhere here on purpose, and they are the two kinds a
# stylesheet should not define. Eight -- `--ang --arc --gap --p1 --p2 --px --py` and `--ac` -- are set
# per element in an inline `style` by the card drawing code, because they *are* the card's data: the two
# colour stops and the angle of the gradient drawn for a project with no Open Graph image. Two, `--ring` and
# `--ring2`, are initialised to `transparent` on `.cx` itself so that a state rule can fill one slot without
# knowing whether the other is occupied. Both kinds resolve at the element. Adding either to `:root` would
# turn a card with a broken state class from invisibly unstyled into confidently wrong.
BRIDGE_CSS = r"""/* THE PROTOTYPE'S TOKENS, IN THE SITE'S. See BRIDGE_CSS in scripts/31_home.py for the
   three kinds of value here, why shadows are per mode rather than per theme, and which of the prototype's
   tokens are deliberately absent. */
:root{
  /* Aliases. These follow every one of the eight token sets without being restated. */
  --field:var(--wash);
  --panel-b:var(--grid);
  /* Geometry and type. Not contrast-bearing and not mode-dependent. */
  --radius:14px; --radius-sm:10px; --hair:1px;
  --num:var(--ui);
  --mono:ui-monospace,"SF Mono","Cascadia Mono",Consolas,"Liberation Mono",monospace;
  --kick-case:uppercase; --kick-track:.1em;
}
/* The effects axis. Four themes, and the values are the argument each theme already makes about itself:
   graphite is the flat drawing with no light on it, which is what `--wash:none` and `--bdf:none` say in
   `pages.css`, so it gets zeroes and the animations never enter the compositor at all. Terminal is the
   only one that wants a scanline, because it is the only one pretending to be a tube. Prism is the
   maximal one and says so. Gated as numbers rather than as `display` switches so that a rule can multiply
   by them -- `calc(2.4s * var(--fx-pulse))` is 0s in graphite, which is an animation that does not exist
   rather than one animating between two identical frames.

   Three of the prototype's five and not five: `--fx-sheen` and `--fx-lift` are read by nothing this page
   loads, so the axis is glow, pulse and scan. The `:root` line below is the one that matters most and the
   easiest to lose -- it is the only declaration of all three, so every skin rule that does not mention a
   token is relying on inheriting a zero from it. It was lost twice while this file was being written, and
   the second time is worth a warning: DO NOT WRITE A CLOSE-COMMENT SEQUENCE INSIDE THIS COMMENT. CSS
   comments do not nest and the stripper is not confused about that -- it ends the comment at the first
   close it meets, which was one I had typed inside a sentence explaining the first bug. Everything after
   it became loose text at the top of the stylesheet, the text swallowed the `:root` rule that followed,
   and all three tokens resolved to nothing.

   Neither loss changed one byte of markup, and the symptom of both was a pulse ring animating in graphite,
   where the whole point of the axis is that nothing animates: `opacity:var(--fx-pulse)` with nothing to
   resolve is an invalid declaration, and an invalid opacity is 1. That is why this block is verified by
   reading computed values out of a browser in all eight sets rather than by looking at the page. */
:root{--fx-glow:0; --fx-pulse:0; --fx-scan:0}
html[data-skin=glass]{--fx-glow:1; --fx-pulse:1}
html[data-skin=terminal]{--fx-glow:1; --fx-pulse:1; --fx-scan:1}
html[data-skin=prism]{--fx-glow:1; --fx-pulse:1}
/* The depth shadows and the poster scrim, per mode. Dark first because dark is the default and lives at
   `:root` everywhere else in this codebase. The scrim is what a poster's title sits on top of its artwork
   in, so it is doing contrast work in a sense -- but against a photograph, which no ratio can be computed
   against, which is why it is a heavy gradient in both modes rather than a light one in light. */
:root{
  --lift:0 2px 8px rgba(2,5,16,.45),0 20px 46px -14px rgba(2,5,16,.66);
  --lift-hi:0 4px 14px rgba(2,5,16,.5),0 40px 80px -20px rgba(2,5,16,.85);
  --scrim:linear-gradient(to top,rgba(3,5,16,.92),rgba(3,5,16,.56) 38%,rgba(3,5,16,.08) 74%,transparent);
}
html[data-theme=light]{
  --lift:0 1px 3px rgba(16,24,40,.10),0 14px 34px -12px rgba(16,24,40,.22);
  --lift-hi:0 2px 8px rgba(16,24,40,.14),0 30px 60px -18px rgba(16,24,40,.30);
  --scrim:linear-gradient(to top,rgba(10,14,24,.88),rgba(10,14,24,.50) 38%,rgba(10,14,24,.06) 74%,transparent);
}
"""

# ---------------------------------------------------------------------------------------------------
# THE POSTER STAGE DOES NOT HAVE A LIGHT MODE.
#
# Everything inside a card's `.ph` sits on top of a project's own Open Graph image, and for the 65 posters on
# this page that have none, on a gradient drawn from the project's facts. Either way it is artwork, not page,
# and the tokens the prototype's rules read there have to stop following the reader's choice of mode at that
# boundary. This is the same argument `--scrim` makes above and the reason `.stz` and `.ph .plat` keep a fixed
# dark plate; it is stated separately because it is the one place the argument was not already applied and
# the consequence was a defect rather than an inconsistency.
#
# What light mode actually did, measured in a browser rather than guessed at: `.ttl .own` reads `--ink2` and
# `.ttl .nm` inherits `--ink`, so the project's name and owner rendered at `rgb(20,23,28)` -- on top of a
# `--scrim` that is `rgba(10,14,24,.88)` at the bottom in light mode *by design*. Near-black on near-black,
# about 1.1:1, on every card on the front page. Separately, `.pt`'s base gradient mixes into `--surface`, so
# the drawn artwork turned pale while `.pt-h`, `.pt-w` and `.pt-r` -- a hatch, a watermark and an arc, all
# three white by fixed value -- disappeared into it. Neither shows in the prototype, because all three of its
# skins are dark and `--ink` was never anything but light.
#
# Four tokens re-declared on `.ph` rather than a rewrite of the rules that read them, which is the whole
# point: one selector re-points `.pt`'s gradient, `.ttl`'s inherited colour, `.own`'s explicit colour and
# anything the prototype adds inside the stage later, with no duplicated selectors and no `!important`. Per
# theme, because each theme's stage should keep its own hue -- terminal's is green-black and prism's is
# purple-black, and flattening all four to one grey would be a worse answer than the bug.
#
# The values are not typed in. They are read out of `docs/pages.css`, which is the file that owns them, and
# `stage_css()` fails the build if the shape it parses stops matching. Sixteen hex values copied into a
# second file would be correct on the day they were copied and silently wrong after the first palette edit.
STAGE_TOKENS = ("--surface", "--band", "--ink", "--ink2")

# `:root` is graphite; the other three are `html[data-skin=X]`. Both forms are the *dark* declaration in
# `pages.css` -- the light halves live behind `[data-theme=light]`, which is exactly what this block is
# cancelling, so matching on a selector without it is what picks the right side.
STAGE_SKINS = (("graphite", r":root\{"), ("glass", r"html\[data-skin=glass\]\{"),
               ("terminal", r"html\[data-skin=terminal\]\{"), ("prism", r"html\[data-skin=prism\]\{"))


def stage_css() -> str:
    """`html[data-theme=light] .ph{...}` per theme, with each theme's own dark stage values.

    Parsed rather than transcribed, and asserted rather than trusted. Three things can go wrong with a value
    lifted out of another file -- it moves, it is renamed, or it changes -- and only the third is silent. The
    assertions below turn the first two into a build failure naming the token and the selector, and the third
    needs no assertion because there is no second copy to disagree with.
    """
    css = (OUT / "pages.css").read_text(encoding="utf-8")
    out = ["/* THE POSTER STAGE HAS NO LIGHT MODE. Generated by stage_css() in scripts/31_home.py from the",
           "   dark declarations in pages.css, which owns these values -- see the long note beside it. */"]
    for skin, pattern in STAGE_SKINS:
        m = re.search(pattern + r"(.*?)\}", css, re.S)
        assert m, f"pages.css no longer has a dark block matching {pattern!r} for {skin}"
        block = m.group(1)
        vals = {}
        for token in STAGE_TOKENS:
            hit = re.search(re.escape(token) + r"\s*:\s*(#[0-9A-Fa-f]{3,8})", block)
            assert hit, f"pages.css's dark {skin} block no longer declares {token}"
            vals[token] = hit.group(1)
        # One attribute stronger for the three opt-in skins than for graphite, which is the same cascade
        # ordering `pages.css` relies on for the skins themselves -- so the pair resolves skin-then-mode.
        sel = ("html[data-theme=light] .ph" if skin == "graphite"
               else f"html[data-skin={skin}][data-theme=light] .ph")
        # `color` as well as the four tokens, and it is not redundant. Re-declaring a token only reaches
        # rules that *read* it inside the stage; an element with no colour of its own inherits a colour that
        # was already resolved outside, where `--ink` is still the light mode's near-black. `.ttl` is exactly
        # that element today and gets away with it because both its children set their own colour -- so this
        # line fixes nothing visible and is here for the next element added inside `.ph`, which will not
        # necessarily be so lucky. Anchoring inheritance at the boundary is what makes "the stage has no
        # light mode" true of the stage rather than of the four rules that happen to be in it now.
        out.append(sel + "{" + ";".join(f"{t}:{v}" for t, v in vals.items())
                   + ";color:" + vals["--ink"] + "}")
    return "\n".join(out) + "\n"

# The six rules the imported stylesheet needs and does not carry, because they live in the prototype's
# `BASE_CSS` -- which is 17 KB of page chrome this page gets from `pages.css` instead. Taken as text rather
# than by importing the whole block: `.dot` and its four states plus one keyframe is the entire overlap,
# measured by generating the markup and diffing its class list against what `SHELF_CSS` styles.
DOT_CSS = r"""/* The freshness dot. From BASE_CSS in scripts/30_v2.py -- the only six rules the imported
   card stylesheet needs out of a block this page otherwise replaces with pages.css. */
.dot{position:relative;flex:none;width:7px;height:7px;border-radius:50%;background:var(--off)}
.dot.hot{background:var(--good)}
.dot.warm{background:var(--bar)}
.dot.ok{background:var(--muted)}
.dot.cold,.dot.stale,.dot.unk{background:var(--grid)}
.dot.hot::after{content:"";position:absolute;inset:-3px;border-radius:50%;
  border:1px solid var(--good);opacity:var(--fx-pulse);
  animation:ping calc(2.4s * var(--fx-pulse)) ease-out infinite}
@keyframes ping{0%{transform:scale(.6);opacity:calc(var(--fx-pulse) * .9)}
  70%{transform:scale(1.9);opacity:0}100%{transform:scale(1.9);opacity:0}}
"""

# This page's own rules, for the two bands the prototype does not have and the one thing `pages.css` does
# not know: that a `<main>` on this page is shelves rather than a table.
HOME_CSS = r"""/* WHAT THE PROTOTYPE DOES NOT HAVE. Everything else on this page is imported. */
/* THE MASTHEAD HAS NO BAR. Everywhere else the header is a panel with a rule under it; here it is drawn on
   a picture of this repository's own code -- its git log and lines from scripts/, made by
   scripts/masthead_art.py -- whose alpha is opaque at the top, reaches 0 at both sides, and fades from
   half-way down to 0 at the bottom. So there is no edge against the page anywhere but the top.
   `.mhart` is its own element, absolutely placed at the top of the body, rather than the header's
   background, because it runs on past the header's bottom and under the spotlight: that overlap is what
   makes the fade seamless. Header and main are lifted over it, header above main, so the Settings menu
   still drops over the page. `center bottom` with `cover`, so a screen too wide for the height crops the
   opaque top, never the faded bottom. One file per mode, so each reader downloads one of the two.
   The first layer is a scrim over the left, where the title and blurb sit: the code there is dimmed into
   the page's own surface, so the words are read against a near-flat field and the lit code is on the
   right, where the navigation is short. It is the page's colour, so it has no edge of its own either. */
.mhart{position:absolute;left:0;right:0;top:0;height:clamp(340px,31.67vw,560px);z-index:0;
  pointer-events:none;--scrim:linear-gradient(90deg,color-mix(in srgb,var(--surface) 88%,transparent) 0%,
  color-mix(in srgb,var(--surface) 70%,transparent) 38%,transparent 62%);
  background:var(--scrim),url(assets/masthead-dark.webp) center bottom/cover no-repeat}
html[data-theme=light] .mhart{background:var(--scrim),url(assets/masthead-light.webp) center bottom/cover no-repeat}
@media (max-width:899px){.mhart{--scrim:linear-gradient(color-mix(in srgb,var(--surface) 72%,transparent),
  color-mix(in srgb,var(--surface) 72%,transparent))}}
header{position:relative;z-index:2;background:transparent;border-bottom:0;
  backdrop-filter:none;-webkit-backdrop-filter:none}
main{position:relative;z-index:1}
/* The type sits on lit code, so it gets a shadow in the page's own surface colour: a halo that is
   invisible against the page and lifts the words off the glyphs behind them. */
header h1,header .sub,header .blurb,header .top nav{text-shadow:0 0 14px var(--surface),0 0 4px var(--surface)}
/* The mascot: an animated model standing between the title and the navigation, feet just past the header's
   bottom edge, on the fading half of the picture. Hidden where the navigation wraps under the title and
   there is no room between them.
   Three layers inside the header, bottom to top: the mascot, the words, the Settings menu. The loader grows
   its canvas from this slot to the whole header's width, and a dance adds light over it, so at the words'
   level it would wash out the title and the navigation -- worst in light mode, where adding light to dark
   ink on a pale field is what lowers contrast. The words are lifted over it rather than the mascot sunk under
   the art: the art is `.mhart`, outside the header, and the header is z 2 above it, so a mascot at 0 here is
   still drawn on the picture. The menu is given its own place above the words, rather than winning a tie
   with the mascot on source order, which it did until now and would stop doing if either moved. */
header .wrap{position:relative}
.mhmascot{position:absolute;left:52%;bottom:-28px;width:240px;height:240px;pointer-events:none;z-index:0}
header .brandbar,header .top{position:relative;z-index:1}
header .setwrap{z-index:2}
@media (max-width:899px){.mhmascot{display:none}}
/* The lit field the frosted panels frost, for the themes that declare one. Fixed rather than scrolled so
   it does not slide out from under them, and behind everything. `none` in graphite, which costs nothing.
   On `body::before` rather than `body` because the shelves need a background of their own to sit on. */
body::before{content:"";position:fixed;inset:0;background:var(--field);pointer-events:none;z-index:0}
/* The scanline, for the one theme that wants to be a tube. At --fx-scan:0 this is a zero-opacity element
   with a zero-duration animation, which is nothing, so it ships to all eight sets rather than being
   conditional markup. */
.scan{position:fixed;inset:0;z-index:2;pointer-events:none;opacity:calc(var(--fx-scan) * .40);
  background:repeating-linear-gradient(180deg,rgba(0,0,0,.34) 0 1px,transparent 1px 3px)}
/* The topic strip. Fourteen chips, one per topic, and a count on each: this is the answer for a reader who
   already knows what they want and should not have to scroll past a shelf to say so. `--ac` per chip is
   the topic's accent, the same five in the same order the cards use. */
.bystrip{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 30px}
.bychip{display:inline-flex;align-items:center;gap:8px;padding:8px 13px;border-radius:999px;
  border:var(--hair) solid var(--grid);background:var(--panel);backdrop-filter:var(--bdf);
  -webkit-backdrop-filter:var(--bdf);color:var(--ink2);font-size:12.5px;font-weight:550;
  text-decoration:none;transition:border-color .16s,color .16s,transform .16s}
.bychip i{width:7px;height:7px;border-radius:50%;background:var(--ac);flex:none}
.bychip .ct{font-family:var(--num);font-variant-numeric:tabular-nums;font-size:11.5px;color:var(--muted)}
.bychip:hover{border-color:var(--ac);color:var(--ink);text-decoration:none;transform:translateY(-1px)}
.bychip:hover .ct{color:var(--ink2)}
/* The Discover band's own header line: the heading, its count, and the link to the page that shows the
   day properly, kept together on the left. */
.dsmore{font-size:12.5px;font-weight:600;color:var(--link);white-space:nowrap;margin-left:6px}
/* The rolled-over state. Shown only by script, and only when the reader's clock has passed midnight in
   the plan's own zone since this page was built *and* the current day's cards could not be fetched -- see
   `DAYCHECK_JS`. It replaces the cards rather than sitting above them, because leaving yesterday's on
   screen under a notice is the one thing worse than not checking at all. `.swap` is the fetch in flight:
   the stale cards are hidden, and nothing is announced yet. */
.dsold{display:none;padding:18px 20px;border-radius:var(--radius);border:var(--hair) solid var(--grid);
  background:var(--panel);backdrop-filter:var(--bdf);-webkit-backdrop-filter:var(--bdf);
  color:var(--ink2);font-size:13.5px;line-height:1.6;max-width:70ch}
/* The arrows go with the rail they scroll. Leaving them up gives the reader two buttons that move a hidden
   element -- they look live, they focus, and pressing either does nothing observable. The "See all 50" link
   stays, because it is the one control that still leads somewhere on this state. */
.sh.rolled .rowscroll,.sh.rolled .shwhy,.sh.rolled .nav{display:none}
.sh.swap .rowscroll{visibility:hidden}
.sh.rolled .dsold{display:block}
/* `.tight`, which the prototype asks for and does not define. `plat_pills(f, compact_pills=True)` emits
   `class="plat tight"` and no rule in 30_v2.py matches `.tight`, so the compact pills the hero asks for
   have always rendered at full size -- invisible in a preview, because the full size is not wrong, just
   bigger than intended. Defined here rather than left dead because this page is the first place that call
   ships, and the alternative is knowingly publishing a class nothing styles. The rule belongs in the
   prototype beside `.ph .plat`; moving it there is part of splitting the card system out, and it is noted
   in that file's follow-up rather than done from downstream. */
.ph .plat.tight{padding:2px;border-radius:5px;gap:2px}
.ph .plat.tight i{padding:2px 3px;font-size:9px}
"""

# THE IMPORTED STYLESHEET IS NOT REWRITTEN, and the reason is worth a note because the obvious thing to do
# is rewrite it. `SHELF_CSS` contains exactly two frosted rules -- `.stz`, the star count, and `.ph .plat`,
# the platform pills -- and both carry a literal `backdrop-filter:blur(6px)` over a fixed
# `rgba(8,10,18,.62)` plate. The reflex is to point them at `--bdf` so they follow the theme, and that would
# be wrong for the same reason `--scrim` above is per mode rather than per theme: both of those elements sit
# on top of a project's own Open Graph image, which is an arbitrary photograph. `--bdf` is `none` in
# graphite, deliberately, and a pill that separated itself from artwork only in three themes out of four
# would be unreadable in the fourth against whatever happened to be behind it. The plate is fixed dark
# because what it is separating from is not the page.
#
# An earlier draft of this file did rewrite them, under a floor that asserted at least eight such
# declarations existed. There were none of the shape it looked for, the assertion fired on the first render,
# and the count was what made the reflex visible instead of shipping it.


# ---------------------------------------------------------------------------------------------------
# The bands, in the order they appear. Each one is a function returning markup so that `render()` reads as
# the page's outline and the order is a list rather than a 200-line f-string.

# The spotlight is the one card allowed the project's own picture. Every other card shows GitHub's social
# card instead (see `art()` in 30_v2.py): nothing bounds what a README banner weighs, and 13 of them made this
# page 21.49 MB. One picture is a different sum. A median banner is 447 KB, and this is the slot the page
# exists to give a project that popularity would never surface, so it gets to look like itself.
#
# Except for GIFs. They are where the weight was -- 11,955, 2,176 and 1,971 KB were the three largest
# pictures on the page, and all three were animated -- and one of them in this slot would put the page back
# over its budget by itself. A GIF, and a row with no picture, get the social card, which GitHub draws for
# every repository: its name, description, owner avatar and counts, at a fixed ~100 KB.
#
# Not lazy, and fetched at high priority: it is the largest thing on the first screen, so it is the page's
# LCP element, and `loading=lazy` on an LCP image only delays the paint.
HEAVY = re.compile(r"\.gif(?:$|[?#])", re.I)


def spot_art(f: dict) -> str:
    src = f["img"] if f["img"] and not HEAVY.search(f["img"]) else b19.og(f["nwo"])
    return (f'<img src="{esc(src)}" alt="" decoding="async" fetchpriority="high"'
            ' style="aspect-ratio:16/9">')


# The mascot in `.mhmascot`: a poster, then a live model once `assets/archie.js` has decided the reader can
# have one (wide screen, motion allowed, WebGL2) and has drawn its first frame. The loader, the model and the
# poster are committed separately from this page, so they are wired only when all three are there: a page
# that names a script it does not have 404s it on every visit, and pwa-check counts that as a console error.
# Whichever lands second, the next run of this stage turns it on.
MASCOT = ("archie.js", "three-archie.js", "archie.glb", "archie-3d.webp")
# The loader's query is its version: archie.js hands its own `?v=` on to the renderer and the model, and none
# of the three is in the service worker's precache, so without it a replaced file can meet a stale sibling
# from the HTTP cache and the mascot stays a poster. The scripts are hashed with LF endings, because the
# checkout is CRLF on Windows and LF on CI; the model is binary and hashed as it is.
VERSIONED = ("archie.js", "three-archie.js", "archie.glb")


def mascot_version() -> str:
    h = hashlib.sha256()
    for f in VERSIONED:
        b = (OUT / "assets" / f).read_bytes()
        h.update(b.replace(b"\r\n", b"\n") if f.endswith(".js") else b)
    return h.hexdigest()[:10]


def mascot() -> tuple[str, str]:
    """The poster rule and the loader tag, or two empty strings while any of MASCOT is missing."""
    if not all((OUT / "assets" / f).is_file() for f in MASCOT):
        return "", ""
    return (".mhmascot{background:url(assets/archie-3d.webp) center/contain no-repeat}",
            f'<script type="module" src="assets/archie.js?v={mascot_version()}"></script>')


def spotlight() -> str:
    """One project, chosen from outside the top 200, with its own reason for being there.

    The prototype's hero, called rather than redrawn, because the argument it makes is exactly the one this
    page exists to make: the slot with the most prominence is the one slot a project cannot reach by being
    popular. The pool is projects outside the top 200 that carry an install command, and the choice is a
    crc32 of the snapshot date -- so it is the same for every reader today and a different project when the
    data next moves.
    """
    tail = [r for r in ROWS if b30.g(r, "nwo") not in b30.TOP200 and b30.g(r, "install")]
    hero = b30.rotate(tail, 1, "spotlight")[0]
    f = b30.face(hero)
    return (
        f'<article class="hero" style="--ac:{f["ac"]}">'
        f'<span class="ph">{spot_art(f)}<span class="veil"></span>'
        f'{b30.kind_chip(f)}{b30.stars_over(f)}{b30.plat_pills(f, True)}</span>'
        f'<div class="bd"><p class="kick"><i></i>Spotlight</p>'
        f'<h2><a href="{f["href"]}">{esc(f["name"])}</a></h2>'
        f'<p class="own">{esc(f["nwo"])}</p>'
        f'<p class="dsc">{esc(f["blurb"])}</p>'
        f'<div class="ln">{b30.lang_chip(f)}'
        f'<span class="age"><i class="dot {f["fresh"]}"></i>{esc(f["age"])}</span>'
        f'{b30.lic_chip(f)}{b30.flags(f)}</div>'
        f'<p class="rot">Why you are seeing this: it is <b>#{f["rank"]} of'
        f' {b30.thousands(len(ROWS))}</b> by stars, so it cannot reach a first screen ordered by'
        f' popularity. The slot rotates on a hash of the snapshot date over the'
        f' {b30.thousands(len(tail))} projects outside the top 200, so it is the same for every reader'
        ' today and a different project tomorrow.</p>'
        f'{b30.cmdline(f)}</div></article>')


def chip_row() -> str:
    """One chip per topic, linking at the facet page that already exists for it.

    The prototype's chips are `href="#"` -- it is a single-file preview with nowhere to go. Here each one
    points at `topic/<slug>/`, which `20_landing.py` publishes and the sitemap carries, so the strip is
    navigation rather than a drawing of navigation. The slug comes from `data.json`'s own `cats`, which is
    the same list both stages index into, so a chip cannot point at a facet page that was never written.
    """
    chips = []
    for name, n in b30.topic_n.most_common():
        i = b30.TOPICS.index(name)
        slug = DATA["cats"][i]["slug"]
        accent = b30.ACCENTS[i % len(b30.ACCENTS)]
        chips.append(
            f'<a class="bychip" href="topic/{esc(slug)}/" style="--ac:var(--accent-{accent})">'
            f'<i></i>{esc(b30.KIND[name])}<span class="ct">{b30.thousands(n)}</span></a>')
    return '<nav class="bystrip" aria-label="Browse by topic">' + "".join(chips) + "</nav>"


def day_cards(day: str) -> tuple[str, int]:
    """One day's poster cards and how many there are. Only picks `data.json` carries -- the stage drops the
    rest too -- so the count is the one that survived, not `PLAN["per_day"]`."""
    picks = [n for n in b30.discover.for_day(PLAN, day)[1] if n in b30.BY_NWO]
    return "".join(b30.c_poster(b30.face(b30.BY_NWO[n])) for n in picks), len(picks)


def day_fragments() -> dict[str, dict]:
    """Every cohort in the plan, drawn, keyed by its date. `main()` writes one file per entry.

    WHY THE BAND NEEDS THEM. The page is built by whichever job last ran, and the daily only rebuilds when a
    source list moved, so the page routinely outlives the Discover day it was built for -- by hours every
    night, by days in a quiet week. The band used to answer that with a notice in place of the cards, so
    most of the time anyone looked, the homepage's Discover band was a paragraph of apology. The plan
    already names every day of the week, so the fix is to draw them all now and let the browser fetch the
    one its clock asks for. One file per day rather than all seven inline: the week is about 800 KB of
    markup, and a reader only ever needs the day it is.
    """
    out = {}
    for c in PLAN["days"]:
        html, n = day_cards(c["date"])
        out[c["date"]] = {"date": c["date"], "long": _long_day(c["date"]), "n": n, "html": html}
    return out


def discover_band() -> str:
    """The day's Discover picks, all of them, in the first shelf slot.

    All fifty rather than a shelf's twelve: the owner asked for the day's whole set here, and the rail
    scrolls, so fifty costs nothing on the first screen.

    Server-rendered, unlike the teaser on the catalogue page, and that is the whole reason this is not that
    strip moved over. The catalogue's strip is painted by script from `discover.json` because it has to
    wait for the reader's filter state before it knows whether it belongs on screen; nothing on this page
    filters, so there is nothing to wait for, and a crawler gets the cards instead of an empty box.

    The build day is `PLAN`'s own current cohort rather than `date.today()`: the plan names the zone it
    rolls over in, and a stage that asked the runner's clock would publish a different day than the page it
    links to for every build that lands in the hours between the two midnights.
    """
    # `discover.today()` and not `date.today()`: the plan rolls over in the zone it names, and a stage that
    # asked the runner's clock would publish a different cohort than `/discover/` for every build landing in
    # the hours between the runner's midnight and Chicago's.
    dated = b30.discover.for_day(PLAN, b30.discover.today())[0]
    # The count that survived `day_cards()`, and not the literal fifty: a heading promising fifty above
    # forty-nine cards is a defect this repository has already shipped once. Every place it is printed is a
    # `data-n`, because the day the browser swaps in can have a different count.
    cards, total = day_cards(b30.discover.today())
    why = (f'<span data-n>{b30.thousands(total)}</span> projects for <span data-long>{_long_day(dated)}'
           '</span>, one from every topic in the atlas, and the star count is not consulted at any point'
           ' in choosing them. Every project in the corpus gets a turn: the scheduler deals from all'
           f' {b30.thousands(len(ROWS))} oldest-featured first, so the tail arrives here as often as the'
           ' head.')
    # Now only the fallback for a day the browser could not fetch -- offline, or a day with no file.
    rolled = (
        '<div class="dsold">Today&rsquo;s set has changed since this page was built, and could not be'
        ' loaded here. <a href="discover/">Open Discover</a> for the current day &mdash; that page reads'
        ' the clock itself and is always on the right one.</div>')
    days = ",".join(c["date"] for c in PLAN["days"])
    return (
        # `data-day` is the day this page was *built for*, not `dated`. The two differ when the plan has run
        # out and `for_day` has cycled: the cohort's own date is then last week's, but it is still the right
        # cohort for today, and a browser comparing against last week's date would declare the band stale the
        # moment it loaded. The prose above says `dated`, which is the other half of the same distinction --
        # which day's picks these really are. The check downstream asks a narrower question: has midnight
        # passed since the build.
        # `data-cohort` is `dated`, the cohort these cards are; `data-days` is every cohort a file was
        # written for, which is all the browser needs to resolve its own day the way `/discover/` does.
        f'<section class="sh" data-sh data-day="{esc(b30.discover.today())}"'
        f' data-tz="{esc(PLAN["tz"])}" data-cohort="{esc(dated)}" data-days="{esc(days)}"'
        f' data-cards="{CARDS_DIR}/">'
        # The link sits beside the heading rather than across the row from it, where it read as belonging
        # to the arrows and was the last thing on the line anyone found.
        f'<div class="shh"><h2>Discover</h2><span class="ct" data-n>{b30.thousands(total)}</span>'
        f'<a class="dsmore" href="discover/">See all <span data-n>{b30.thousands(total)}</span> &rarr;</a>'
        '<span class="spring"></span>'
        '<span class="nav"><button data-dir="-1" aria-label="Scroll left">&#8592;</button>'
        '<button data-dir="1" aria-label="Scroll right">&#8594;</button></span></div>'
        f'<p class="shwhy">{why}</p>{rolled}'
        f'<div class="rowscroll">{cards}</div></section>')


def _long_day(day: str) -> str:
    """`2026-09-21` as `Sunday 21 September`. No year: this is always within a week of today, and a year on
    it would read as an archive date. The browser has the same function for the rolled-over check."""
    d = datetime.date.fromisoformat(day)
    return f"{d.strftime('%A')} {d.day} {d.strftime('%B')}"


def shelf(sh: dict) -> str:
    """One shelf: its heading, its pool size, the prose that says why these projects, and the cards.

    Straight out of `shelves_html()` except for the empty branch, which is not reachable here -- that
    branch exists in the prototype for a snapshot with no arrivals, and this page's band list is built
    from shelves that have rows, so an empty one is a build error rather than a state to draw.
    """
    assert sh["rows"], f"shelf {sh['key']} has no rows; see the note in shelf()"
    return (
        f'<section class="sh" data-sh>'
        f'<div class="shh"><h2>{esc(sh["title"])}</h2>'
        f'<span class="ct">{b30.thousands(len(sh["pool"]))}</span><span class="spring"></span>'
        '<span class="nav"><button data-dir="-1" aria-label="Scroll left">&#8592;</button>'
        '<button data-dir="1" aria-label="Scroll right">&#8594;</button></span></div>'
        f'<p class="shwhy">{sh["why"]}</p>'
        f'<div class="rowscroll">{"".join(b30.c_poster(b30.face(r)) for r in sh["rows"])}</div>'
        '</section>')


def coverage(shelves: list[dict], hero_nwo: str, discover_n: int) -> str:
    """The arithmetic, written out.

    "Give the tail screentime" is a claim that can be checked, and a page that makes it without checking is
    decoration. The prototype's version of this paragraph is the model; this one counts the Discover band
    too, and states the one thing that paragraph is careful to state -- that a hash guarantees a different
    twelve tomorrow, not a turn for every project.
    """
    union = {b30.g(r, "nwo") for sh in shelves for r in sh["rows"]} | {hero_nwo}
    outside = sum(1 for n in union if n not in b30.TOP200)
    med = sorted(b30.RANK[n] for n in union)[len(union) // 2]
    tail = [r for r in ROWS if b30.g(r, "nwo") not in b30.TOP200 and b30.g(r, "install")]
    reach = ({b30.g(r, "nwo") for sh in shelves for r in sh["pool"]}
             | {b30.g(r, "nwo") for r in tail})
    return (
        '<div class="cover">'
        f'What this page reaches. The bands above put <b>{len(union)}</b> distinct projects on screen'
        f' against the <b>30</b> a star-ranked first screen shows, and <b>{outside}</b> of them are outside'
        f' the top 200 by stars &mdash; their median position in the ranking is <b>#{med}</b> of'
        f' {b30.thousands(len(ROWS))}. Counting the pools rather than the cards on screen, these shelves'
        f' can reach <b>{b30.thousands(len(reach))}</b> of {b30.thousands(len(ROWS))} projects'
        f' ({len(reach) * 100 // len(ROWS)}%) with no query typed, and the set changes every time the'
        f' snapshot does. The Discover band adds a further {discover_n} on a rotation that is not a hash at'
        ' all but a queue, oldest-featured first, which is the one band here that can promise every'
        ' project a turn rather than only a different twelve. Stated precisely because the difference'
        ' matters: the shelves&rsquo; rotation is <b>memoryless</b>. The remaining'
        f' {b30.thousands(len(ROWS) - len(reach))} projects are reachable by topic, by the catalogue&rsquo;s'
        ' filters, or by search.</div>')


# ---------------------------------------------------------------------------------------------------
# The client half. Four pieces, none of them a framework.

# The forwarder. Until the catalogue moved to `catalog/`, this URL *was* the catalogue, and every filtered
# view of it was this URL plus a hash: `#topic=x&target=y`, `#q=name`, `#new=1`. Those links are in the
# README, in the Markdown edition, in feed entries, in readers' bookmarks and in other people's posts, and
# none of them can be regenerated. This page reads no hash of its own, so a fragment with a `=` in it can
# only be one of them, and it goes where it was always meant to go. `replace` rather than `assign`, so the
# back button skips the homepage the reader never asked for.
#
# Keyed on `=` rather than on the catalogue's list of parameters. The list grows (`cmp=`, `list=` and
# `saved=` all arrived after the README's links were written), and a copy of it here would be a list that
# forwards yesterday's links and drops tomorrow's. An in-page anchor is an id, and no id has a `=` in it.
#
# First in `<head>`, before the stylesheet, so a forwarded reader is not shown a frame of the wrong page.
# Also on `hashchange`, for the reader who pastes a filter onto this URL without reloading.
FORWARD_JS = r"""<script>
(() => {
  const go = () => {
    if (location.hash.includes("=")) location.replace("catalog/" + location.search + location.hash);
  };
  go();
  addEventListener("hashchange", go);
})();
</script>"""

# The four clock functions, verbatim from the `DISCOVER CORE` block in `scripts/19d_discover.py`. This is
# the third copy in the repository and the reason is the one the second copy gives: the alternative is this
# page loading a second script to answer one question -- what is the date in the zone the plan names.
#
# A copy is only safe if something notices when it stops being one. `tests/discover_test.py` compares all
# three character for character, by name, off the files as text; the two-space indent is not cosmetic, it
# is how that test's `jsfn()` finds the function.
#
# Only `dayIn` and `forDay` are called here. `asUTC` and `daysBetween` come along because `forDay` needs
# them and because a partial copy is the kind that drifts -- taking two of four would mean the test could
# only hold half of it.
DAYCHECK_JS = r"""<script>
const DSTRIP = (() => {
  const dayIn = (tz, at) => {
    const p = {};
    for (const {type, value} of new Intl.DateTimeFormat("en-US", {
      timeZone: tz, year: "numeric", month: "2-digit", day: "2-digit",
    }).formatToParts(at)) p[type] = value;
    return p.year + "-" + p.month + "-" + p.day;
  };
  const asUTC = (iso) => {
    const [y, m, d] = iso.split("-").map(Number);
    return Date.UTC(y, m - 1, d);
  };
  const daysBetween = (a, b) => Math.round((asUTC(b) - asUTC(a)) / 86400000);
  const forDay = (plan, day) => {
    const days = (plan && plan.days) || [];
    if (!days.length) return null;
    const hit = days.find((c) => c.date === day);
    if (hit) return hit;
    const n = days.length;
    return days[((daysBetween(days[0].date, day) % n) + n) % n];
  };
  return {dayIn, forDay};
})();

// Is the Discover band still showing the day it was built for? The band carries the date and the zone it
// was built for in its own attributes, so this needs no payload and no fetch -- one date format and one
// string compare. Once a minute plus a `visibilitychange`, because the case being handled is a lid closed
// at half eleven and opened at one in the morning, which no page-load check can catch.
//
// When it is not, the day's cards are fetched from the file `day_fragments()` wrote for that cohort and
// swapped in. `forDay` resolves the reader's day over the plan's dates exactly as `/discover/` does, cycling
// once the week has run out, so the band and that page cannot disagree about which fifty are today's. Only
// a failed fetch -- offline, or a day with no file -- falls back to the notice and its link.
(() => {
  const band = document.querySelector("[data-day]");
  if (!band) return;
  const tz = band.dataset.tz, rail = band.querySelector(".rowscroll");
  const plan = {days: (band.dataset.days || "").split(",").filter(Boolean).map(date => ({date}))};
  let shown = band.dataset.day, have = band.dataset.cohort, want = "";
  const check = () => {
    const today = DSTRIP.dayIn(tz, new Date());
    if (today === shown) return;
    const c = DSTRIP.forDay(plan, today);
    if (c && c.date === have) { shown = today; band.classList.remove("rolled"); return; }
    if (!c || !rail) { band.classList.add("rolled"); return; }
    if (want === c.date) return;
    want = c.date;
    band.classList.add("swap");
    fetch(band.dataset.cards + c.date + ".json").then(r => {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    }).then(d => {
      rail.innerHTML = d.html;
      rail.scrollLeft = 0;
      band.querySelectorAll("[data-n]").forEach(e => { e.textContent = d.n.toLocaleString("en-US"); });
      band.querySelectorAll("[data-long]").forEach(e => { e.textContent = d.long; });
      shown = today; have = d.date;
      band.classList.remove("rolled");
    }).catch(() => band.classList.add("rolled")).finally(() => {
      want = "";
      band.classList.remove("swap");
    });
  };
  check();
  setInterval(check, 60000);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) check(); });
})();
</script>
"""

# The service worker. It moves here with the page it caches: `PRECACHE` in `24_pwa.py` begins with `"./"`,
# which is a request for this file, so whichever generator writes `/` is the one that has to register the
# worker. `19_pages.py` registered it when `/` was the catalogue.
# The offline shell. This registration used to live at the foot of `19_pages.py`'s page, and moved here with
# the catalogue: `PRECACHE` in `24_pwa.py` begins with `"./"`, which is this page, and the scope a worker gets
# is the directory of its script -- so registering from the site root covers `catalog/`, `repo/`, `discover/`
# and everything else, where a registration from inside `catalog/` would not. One per site, on the root.
#
# Everything below the first line is carried over verbatim from that page, because each clause was load-bearing
# there and nothing about moving it changes why:
#   * `location.protocol !== "file:"` -- registering from `file://` throws SecurityError, and a contributor
#     who opened the page off disk should not see it.
#   * `updateViaCache: "none"` -- Pages serves with `max-age=600`, and the one file that must never come from
#     the HTTP cache is the worker that decides what the HTTP cache is for.
#   * the explicit `reg.update()` -- per spec, `register()` with an unchanged script URL resolves against the
#     existing registration *without* queueing an update job, so without it a reader who keeps the tab open
#     gets a new worker only when the browser's own soft-update timer decides to look.
# Inside a `load` listener and last on the page, because a service worker is the least urgent thing here.
# Failure is silent and has to be: a worker that will not install is a page without offline support, not a
# page that should show an error.
SW_JS = r"""<script>
if ("serviceWorker" in navigator && location.protocol !== "file:") {
  addEventListener("load", () => {
    navigator.serviceWorker.register("sw.js", {updateViaCache: "none"})
      .then(reg => { if (reg.active) reg.update().catch(() => {}); })
      .catch(() => {});
  });
}
</script>
"""


def render() -> str:
    """The page.

    Reads as the outline deliberately: the band list below is the design, in the order it was asked for,
    and everything above this function exists so that this list can be short.
    """
    shelves = b30.shelf_defs()
    # Shelves with nothing in them are dropped rather than drawn as an empty state. The prototype draws the
    # empty one because on a preview page the absence is the subject; on the front page of the site it is
    # just a hole, and the shelf will reappear by itself on the snapshot that fills it.
    shelves = [sh for sh in shelves if sh["rows"]]
    hero = spotlight()
    hero_nwo = re.search(r'<p class="own">([^<]+)</p>', hero).group(1)
    band = discover_band()
    discover_n = int(re.search(r'See all <span data-n>([\d,]+)</span>', band).group(1).replace(",", ""))

    stars = sum(b30.g(r, "stars") or 0 for r in ROWS)
    title = "Awesome Agentic Atlas — browse and discover agentic AI projects"
    desc = (f"{len(ROWS):,} agentic AI projects merged from {LISTS} awesome-lists, on shelves with a "
            f"stated reason for each one: named by three or more lists, shipped this week, hidden gems, "
            f"runs on Windows. Snapshot {DATA['snapshot']}.")

    # `b19.verification()` is Google Search Console's HTML-tag verification. It lives in `19_pages.py`,
    # which still owns the token and its alphabet assertion, and it prints *here* because verification is
    # per property: the property is the URL prefix `SITE`, Google fetches that one URL and reads the markup
    # it gets back, so the tag has to be on whichever page answers it. That was the catalogue until the
    # catalogue moved to `catalog/`, and it is this page now. Getting it wrong has no symptom on this side
    # -- the build stays green and Search Console simply never verifies.
    #
    # Flush against the `<link>` after it, exactly as `b20.HEAD_THEME` is: the function returns "" while no
    # token is set, so that line is then just the icon link, with no blank line and no byte of difference
    # from a page built before any of this was wired up.
    head = f"""<!doctype html>
<html lang="en" data-theme="dark" data-skin="graphite">
<head>
<meta charset="utf-8">
{FORWARD_JS}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(SITE)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(SITE)}">
{b19.verification()}<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="manifest" href="manifest.webmanifest">
{b20.HEAD_THEME}<link rel="stylesheet" href="pages.css">
<style>__HOMECSS__</style>
</head>"""

    body = [
        '<body>',
        '<div class="scan" aria-hidden="true"></div>',
        '<div class="mhart" aria-hidden="true"></div>',
        '<header><div class="wrap">',
        '  <div class="mhmascot" aria-hidden="true"></div>',
        f'  <nav class="brandbar">{mark.brand("./")}</nav><div class="top">',
        '  <div>',
        '    <h1>Awesome Agentic Atlas</h1>',
        f'    <p class="sub"><b>{len(ROWS):,}</b> projects · <b>{len(DATA["cats"])}</b> topics ·'
        f' <b>{stars:,}</b> combined stars · snapshot {esc(DATA["snapshot"])}</p>',
        f'    <p class="blurb">{LISTS} awesome-lists, merged and de-duplicated, on shelves that each say'
        ' why the projects on them are there.</p>',
        '    <a class="cta" href="catalog/">Search and filter all'
        f' {len(ROWS):,} &rarr;</a>',
        '  </div>',
        '  <nav>',
        '    <a href="discover/">Discover</a> ·',
        '    <a href="collections/">Collections</a> ·',
        f'    <a href="https://github.com/{esc(REPO)}/blob/main/mega-list/leaderboard.md">Leaderboard</a> ·',
        '    <a href="catalog/">Catalogue</a> ·',
        '    <a href="repo/">All projects</a><br>',
        f'    <a href="https://github.com/{esc(REPO)}">Repository</a> ·',
        f'    <a href="https://github.com/{esc(REPO)}/tree/main/mega-list">Markdown</a><br>',
        '__SETTINGS__',
        '  </nav>',
        '</div></div></header>',
        '<main><div class="shwrap">',
        hero,
        chip_row(),
        band,
        *[shelf(sh) for sh in shelves],
        coverage(shelves, hero_nwo, discover_n),
        '</div></main>',
        '<footer><div class="wrap">',
        f'  The Awesome Agentic Atlas merges {LISTS} awesome-lists into one index; all {LISTS} are credited'
        f' in the <a href="https://github.com/{esc(REPO)}#the-source-lists">repository</a>. Stars,'
        f' language, licence and last-push come from the GitHub API on {esc(DATA["snapshot"])} and drift'
        ' daily. Card artwork is each project&rsquo;s own Open Graph image where it has one, and a gradient'
        ' drawn from its facts where it does not.',
        '</div></footer>',
        '__SETJS__',
        '<script>wireSettings();</script>',
        f'<script>{b30.SHELF_JS}</script>',
        DAYCHECK_JS,
        SW_JS,
        *filter(None, [mascot()[1]]),
        b19.beacon(),
        '</body>',
        '</html>',
        '',
    ]

    page = head + "\n".join(body)
    # The comment strip runs before substitution for the reason `substitute()` in `19_pages.py` gives at
    # length: a constant injected afterwards would smuggle its own comments into the published bytes. So
    # each injected piece goes through the stripper that matches what it is -- markup, a rule block, a bare
    # script body -- and `strip_page` is wrong for the last of those because it looks for a `<script>` tag
    # to decide that what follows is JavaScript.
    # Order is cascade order, and each piece is downstream of the ones before it: the bridge defines the
    # tokens the rest read, the dot rules are the fragment the imported sheet assumes, the imported sheet is
    # the bulk, the stage block cancels light mode inside it, the Settings control travels with its own
    # rules, and this page's own rules go last so that `.ph .plat.tight` can reach past `.ph .plat`.
    # `pages.css` is a `<link>` above all of them.
    css = BRIDGE_CSS + DOT_CSS + b30.SHELF_CSS + stage_css() + b19.SETTINGS_CSS + HOME_CSS + mascot()[0]
    return (pagemin.strip_page(page)
            .replace("__HOMECSS__", pagemin.strip_css(css))
            .replace("__SETTINGS__", pagemin.strip_page(b19.SETTINGS_MENU))
            .replace("__SETJS__", "<script>" + pagemin.strip_js(b19.SETTINGS_JS) + "</script>"))


def main() -> None:
    ap = argparse.ArgumentParser(description="Write the shelves homepage.")
    ap.add_argument("--out", default=str(OUT), help="the directory to write index.html into")
    args = ap.parse_args()
    dest = Path(args.out)
    dest.mkdir(parents=True, exist_ok=True)
    page = render()
    (dest / "index.html").write_text(page, encoding="utf-8", newline="\n")
    print(f"wrote {dest / 'index.html'}  {len(page):,} bytes")
    # The week's cards. Files for days that have left the plan are removed, so the directory is exactly the
    # plan and a stale cohort cannot be fetched by a page that still names it.
    cards = dest / CARDS_DIR
    cards.mkdir(parents=True, exist_ok=True)
    frags = day_fragments()
    for old in cards.glob("*.json"):
        if old.stem not in frags:
            old.unlink()
    for day, frag in frags.items():
        (cards / f"{day}.json").write_text(json.dumps(frag, ensure_ascii=False, separators=(",", ":")),
                                           encoding="utf-8", newline="\n")
    print(f"wrote {len(frags)} day(s) of Discover cards to {cards}")


if __name__ == "__main__":
    main()
