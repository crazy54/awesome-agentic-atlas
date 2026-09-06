"""Write the GitHub Pages site: one static page over every repo, filterable in the browser.

The third surface, and the only one where the two axes are actually crossable live. The workbook can
cross them because Excel filters two columns at once; a Markdown page cannot, because Markdown has no
filter -- so `mega-list/topics/` and `mega-list/targets/` each pick one axis and print the other as a
column. This page does what the workbook does, without Excel.

Same data, same ordering, same verdicts as the other two: it imports `17_markdown`, which imports
`16_build_all`, so nothing here re-derives a star count or a platform call.

  docs/index.html   the page. no build step, no framework, no dependency to install.
  docs/data.json    every repo, column-oriented.
  docs/.nojekyll    stops Pages running Jekyll over a directory that has no Jekyll in it.

Two decisions worth stating. The data is a separate file rather than inlined, so the page is 30 KB and
cached separately from the 1,294 rows that change on every rebuild. And every filter is mirrored into
the URL hash, which is what makes "the best Claude Code observability tool" a link -- the thing the
Markdown pages can only approximate by existing in two directories.
"""
import importlib.util
import json
import os
import re
import sys
from datetime import date, datetime, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
OUT = ROOT / "docs"

spec = importlib.util.spec_from_file_location("b17", Path(__file__).parent / "17_markdown.py")
b17 = importlib.util.module_from_spec(spec)
sys.modules["b17"] = b17
spec.loader.exec_module(b17)

newness = b17.newness

b16 = b17.b16
tax = b17.tax
DASH = b16.DASH
REPO = b17.REPO

# Verdicts compress to one character each because they are printed 6,470 times and there are five of
# them. The page expands them back for display; the JSON is what travels over the wire.
VERDICT = {"Yes": "Y", "Likely": "L", "No": "N", "n/a": "a", DASH: "-", "": "-"}
OS_FIELDS = ["win_native", "win_wsl2", "macos", "linux", "docker"]
OS_LABELS = ["Windows", "WSL2", "macOS", "Linux", "Docker"]

# The columns of `data.json`, in order. Column-oriented rather than one object per repo: the keys would
# otherwise be repeated 1,294 times, which is 380 KB of the word "category". The page maps them back
# into objects once, on load.
COLS = ["name", "nwo", "cat", "targets", "stars", "lists", "listed_by", "os",
        "blurb", "install", "lang", "license", "pushed", "url", "img", "first_seen"]


def og(nwo: str) -> str:
    return f"https://opengraph.githubassets.com/1/{nwo}"


def row_for(r, shots, cat_ix, tgt_ix) -> list:
    img = b17.image(r, shots)
    return [
        r["name"],
        r["nwo"],
        cat_ix[r["category"]],
        sorted(tgt_ix[t] for t in r["targets"]),
        r["stars"] or 0,
        r["list_count"],
        r["listed_by"],
        "".join(VERDICT.get(r.get(f) or "", "-") for f in OS_FIELDS),
        b17.norm(r.get("blurb") or "", 400),
        b17.norm(r.get("install_cmd") or ""),
        r.get("language") or "",
        r.get("license") or "",
        r.get("pushed_at") or "",
        r["url"],
        # Empty means "derive it": the social card exists for every repo and is the fallback for two
        # thirds of these rows, so spelling it out would be 55 bytes x 1,294 of a string the page can
        # rebuild from `nwo`.
        "" if img == og(r["nwo"]) else img,
        # The raw arrival date, not a new/old flag, and for every arrival rather than only the recent
        # ones -- the page needs the date to print it and to expire the mark itself, and once it has to
        # travel anyway there is no reason to throw the older ones away.
        newness.SEEN.get(r["nwo"], ""),
    ]


SCHEMA_VERSION = 1


def build_data(facets, shots) -> dict:
    cats = list(tax.CATEGORIES)
    tgts = [t for t, _p in tax.TARGETS]
    cat_ix = {c: i for i, c in enumerate(cats)}
    tgt_ix = {t: i for i, t in enumerate(tgts)}
    rows = sorted(facets, key=lambda r: (-(r["stars"] or 0), r["name"].lower()))
    return {
        # `data.json` is published at a stable URL with `Access-Control-Allow-Origin: *`, so anyone can
        # fetch it and some people will. This is the number that tells them whether their reader still
        # works. It only moves when the *shape* changes -- the column set or order, the Y/L/N/a/-
        # encoding, the five-OS order, the slug rules, the "no nulls" rule. Adding a top-level key or
        # changing a star count does not move it, because neither breaks a reader.
        # Absent means 1: the snapshot published before this key existed is otherwise identical.
        "schema_version": SCHEMA_VERSION,
        "snapshot": date.today().isoformat(),
        "repo": REPO,
        "cols": COLS,
        # The page applies the window, so it has to be told what it is. Here rather than hardcoded in the
        # JavaScript so that changing it is one edit in `newness.py` and not two files that disagree.
        "window_days": newness.WINDOW,
        "baseline": newness.load()["baseline"],
        # Slugs travel in the URL hash, and they are the same slugs that name the Markdown pages, so a
        # link into this page and a link into `mega-list/topics/` say the same word.
        "cats": [{"name": c, "slug": b17.fileslug(c),
                  "blurb": b17.TOPIC_BLURB.get(c, "")} for c in cats],
        "targets": [{"name": t, "slug": b17.fileslug(t),
                     "blurb": b17.TARGET_BLURB.get(t, "")} for t in tgts],
        "os": OS_LABELS,
        "rows": [row_for(r, shots, cat_ix, tgt_ix) for r in rows],
    }


# Cloudflare Web Analytics: one script, no cookies, no consent banner, nothing to install, and it works
# on Pages without the domain being on Cloudflare -- the beacon reports from the reader's browser, so the
# "JS beacon" mode needs no DNS change.
#
# The token is committed rather than injected from a secret, because it is not one. Pages serves `docs/`
# verbatim and has no build step of its own, so the token has to be *in* the generated page, and that page
# is in the repo; every visitor reads it in view-source anyway. Hardcoding it also means a rebuild by
# anyone cannot quietly ship a page that measures nothing, which is the failure an env-var-only design
# invites. `CF_BEACON_TOKEN` still overrides it, and setting that to "" or "off" drops the script -- which
# is what a fork wants, and what a local `python -m http.server` run wants.
#
# `type=module` is Cloudflare's own current form and is deferred implicitly, so it cannot block the parse.
# The token lands in a JSON attribute inside HTML, so it is validated rather than trusted: one stray quote
# would close the attribute and let the rest be read as markup. Cloudflare issues 32 hex characters, and
# anything else is a typo worth stopping the build for instead of shipping a silent no-op.
CF_TOKEN = "1fe3cbfd55ef4fccab981c064489e656"
TOKEN_RE = re.compile(r"\A[0-9a-f]{32}\Z")


def beacon(token: str | None = None) -> str:
    """The analytics script tag, or "" when the token is disabled."""
    if token is None:
        token = os.environ.get("CF_BEACON_TOKEN", CF_TOKEN)
    token = token.strip()
    if not token or token.lower() in {"off", "none", "0"}:
        return ""
    if not TOKEN_RE.match(token):
        raise SystemExit(
            f"CF_BEACON_TOKEN is not a Cloudflare beacon token (expected 32 hex chars, got {token!r}).")
    return ("<!-- Cloudflare Web Analytics --><script type=\"module\" "
            'src="https://static.cloudflareinsights.com/beacon.min.js" '
            f"data-cf-beacon='{{\"token\": \"{token}\"}}'></script>"
            "<!-- End Cloudflare Web Analytics -->\n")


def facet_links(items: list[dict], prefix: str) -> str:
    """The footer's crawlable links to the prerendered facet pages `20_landing.py` writes.

    Derived from the same lists the page filters by, rather than written out, so adding a topic adds its
    link. `escape` because these names carry an ampersand -- "Harnesses & Runtime Infra" -- and a raw one
    is a parse error a validator will flag even where a browser recovers from it."""
    return " · ".join(
        f'<a href="{prefix}/{i["slug"]}/">{escape(i["name"])}</a>' for i in items)


def built() -> tuple[str, str]:
    """When this page was rendered, as (machine-readable UTC, the form the badge prints).

    The header carries a "last deployed" badge, and this is the half of its value that can be known here.
    The other half cannot: Pages serves this branch's `docs/` folder, so the commit that carries this very
    file is what triggers its own deployment, and that deployment finishes a minute or two after this
    function runs. A page therefore cannot be told its own publish time at build time -- it can only be
    told when it was built, and then look the real answer up at load. See `deployStamp` in the page, which
    reads it off the `Last-Modified` header of the `data.json` request the page already makes.

    So this value is what the badge shows before that fetch resolves, in the copy committed to the
    repository, and in a local `python -m http.server` where there is no deployment to describe at all.

    Whole minutes because that is what the badge prints, and a `datetime` attribute claiming a precision
    the visible text does not have is a small lie to a machine. It costs nothing in churn either way:
    `__SNAPSHOT__` already puts today's date in this file, so `index.html` differs on every day a build
    runs regardless of what this returns.
    """
    now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    return now.strftime("%Y-%m-%dT%H:%M:%SZ"), now.strftime("%Y-%m-%d %H:%M UTC")


def substitute(page: str, data: dict, repo: str, site: str) -> str:
    """Fill the template's placeholders. Both this stage and `19b_refresh.py` render the same shell, and
    when the two chains drifted the refreshed page quietly lost whichever one had been added since."""
    stamp_iso, stamp_utc = built()
    return (page
            .replace("__BUILT__", stamp_iso)
            .replace("__BUILT_UTC__", stamp_utc)
            .replace("__TOPICLINKS__", facet_links(data["cats"], "topic"))
            .replace("__TARGETLINKS__", facet_links(data["targets"], "target"))
            .replace("__COUNT__", f"{len(data['rows']):,}")
            .replace("__TOPICS__", str(len(data["cats"])))
            .replace("__STARS__", f"{sum(r[4] for r in data['rows']):,}")
            .replace("__SNAPSHOT__", data["snapshot"])
            .replace("__WINDOW__", str(newness.WINDOW))
            .replace("__SITE__", site)
            .replace("__REPO__", repo)
            .replace("__ANALYTICS__", beacon()))


PAGE = r"""<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Awesome Agentic Atlas — browse every agentic tool</title>
<meta name="description" content="__COUNT__ agentic AI projects from eleven awesome-lists, merged, deduplicated and filterable by topic, harness and operating system.">
<meta property="og:title" content="Awesome Agentic Atlas">
<meta property="og:description" content="__COUNT__ projects from eleven awesome-lists, one filterable index.">
<meta property="og:image" content="https://opengraph.githubassets.com/1/__REPO__">
<link rel="canonical" href="__SITE__">
<!-- Autodiscovery for the arrivals feed. Relative, like the `fetch("data.json")` this page already does,
     so it resolves on Pages and from a local `python -m http.server` alike. GitHub Pages serves .xml as
     text/xml and cannot be told otherwise, so the `type` here is what actually declares the format --
     readers sniff the root element regardless, but the link tag is where a browser looks first. -->
<link rel="alternate" type="application/atom+xml" title="Awesome Agentic Atlas — new arrivals"
      href="feed.xml">
<link rel="alternate" type="application/feed+json" title="Awesome Agentic Atlas — new arrivals"
      href="feed.json">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><text y='13' font-size='14'>&#127760;</text></svg>">
<!-- Ahead of the stylesheet deliberately, and inline rather than in a file: this has to settle the theme
     before first paint. A reader who chose light, or whose OS asks for light, otherwise gets a frame of
     near-black before the toggle catches up, and an external script is one more round trip during which
     the wrong theme is on screen.

     Precedence is explicit choice, then the operating system, then dark. Dark stays the fallback because
     it is the designed mode -- the one whose accent contrast ratios were actually measured. The markup's
     data-theme="dark" is the floor if this throws, which localStorage does in some private modes. -->
<script>
try {
  var t = localStorage.getItem("theme");
  if (t !== "light" && t !== "dark")
    t = matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
  document.documentElement.dataset.theme = t;
} catch (e) {}
</script>
<style>
/* Lagoon Gold: cyan primary, gold secondary, cool near-black surfaces. Dark is the designed mode --
   its eight neutrals and two accents are the theme's own values. Light is stepped from the same two
   hues rather than flipped, because the accents at their dark-mode lightness fail on white (the cyan
   measures 2.53:1 there), and its neutrals are cooled to match so toggling does not change brand.
   --onbar exists because a filled cyan or gold accent carries DARK ink, not white: white on #08b0cc
   is 2.3:1, while the theme's own #0c1013 on it is 7.36:1. */
:root{
  --surface:#101416; --plane:#181f21; --band:#232d30; --ink:#d0d7d8; --ink2:#a8b0b2;
  --muted:#8c9496; --grid:#2c383d; --link:#08b0cc; --bar:#08b0cc;
  --good:#2eb82e; --warn:#feb932; --off:#8c9496; --onbar:#0c1013;
}
html[data-theme=light]{
  --surface:#fbfcfc; --plane:#eef1f2; --band:#f4f6f6; --ink:#101416; --ink2:#4a5254;
  --muted:#5f6769; --grid:#dbe0e1; --link:#096373; --bar:#0a6f80;
  --good:#0a7c0a; --warn:#8a5a00; --off:#5f6769; --onbar:#fff;
}
*{box-sizing:border-box}
body{margin:0;background:var(--surface);color:var(--ink);
  font:15px/1.5 "Segoe UI",system-ui,-apple-system,Helvetica,Arial,sans-serif}
a{color:var(--link);text-decoration:none}
a:hover{text-decoration:underline}
/* Only #q had a focus ring, so every chip, the sort menu and both nav buttons were invisible to anyone
   driving this page from the keyboard. :focus-visible rather than :focus so a mouse click does not leave
   a ring behind on the chip that was pressed. */
:focus-visible{outline:2px solid var(--bar);outline-offset:2px;border-radius:4px}
/* Off screen rather than display:none or visibility:hidden -- both of those take the text out of the
   accessibility tree as well as off the screen, which defeats the point. */
.sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;
  clip-path:inset(50%);white-space:nowrap;border:0}
/* Six control rows sit between the top of the document and the first result, and a screen-reader or
   keyboard reader had to walk all of them on every visit. Hidden until focused, which is the only
   state in which it is useful. */
.skip{position:absolute;left:-999px;top:0;z-index:40;background:var(--bar);color:var(--onbar);
  padding:10px 16px;border-radius:0 0 8px 0;font-weight:600}
.skip:focus{left:0}
header{background:var(--plane);border-bottom:1px solid var(--grid);padding:22px 20px 16px}
.wrap{max-width:1500px;margin:0 auto}
h1{margin:0 0 4px;font-size:26px;letter-spacing:-.02em}
h1 span{color:var(--muted);font-weight:400;font-size:15px;letter-spacing:0}
.sub{color:var(--ink2);font-size:14px;margin:0}
.sub b{color:var(--ink)}
/* The snapshot's age, not just its date. Green while the daily build is keeping up, amber once it has
   not -- at which point the star counts on the page are drifting and the reader deserves to know that
   from the header rather than from the footer's fine print. */
.fresh{color:var(--good)}
.stale{color:var(--warn);font-weight:600}
/* The "last deployed" badge, drawn to match the shields.io badges in the README rather than fetched from
   shields.io. Fetching one is not an option here: the value is a timestamp, so the URL would have to be
   regenerated on every build, the badge would still be a third-party request on the critical path of every
   page view, and it could never be corrected at load by `deployStamp` -- an <img> cannot be re-rendered
   from a response header.
   Every number below is read off the SVG shields actually serves for `?style=for-the-badge`, not guessed:
   28px tall, 10px Verdana, 12px gutters, square corners, label in normal weight on #555 and value in bold
   on the colour. The tracking is the one thing shields does not express as a property -- it forces each run
   of text to a computed width with `textLength` and lets the renderer distribute the slack -- so it is set
   here directly, at the value that lands both segments on shields' own rect widths for this badge (122.25
   and 176.0, measured, not guessed). That stays true for every date this will ever print: the value is
   always exactly 20 characters and Verdana's digits are tabular, so the string's width never moves. The
   right gutter gives the tracking back, because CSS letter-spacing applies after the final character too
   and would otherwise push the text half a pixel off-centre inside its own box.
   Fixed hexes rather than theme variables, and #1a7f37 is the README's own green: those badges are images
   and look identical in GitHub's light and dark themes, so a stamp that repainted itself with this site's
   theme would be the one thing in the family that did not match. Both fills clear 4.5:1 against white. */
.stamp{display:inline-flex;height:28px;margin:10px 0 0;text-decoration:none;
  font-family:Verdana,Geneva,DejaVu Sans,sans-serif;font-size:10px;line-height:28px;
  letter-spacing:1.28px;text-transform:uppercase;white-space:nowrap}
.stamp>span{padding:0 10.72px 0 12px;color:#fff}
.stamp .k{background:#555}
.stamp .v{background:#1a7f37;font-weight:700}
/* Amber on the same fortnight the snapshot text uses, so the header has one staleness threshold and not
   two. Recoloured rather than relabelled, and the badge's own tooltip says what the colour means. */
.stamp.late .v{background:#9a6700}
/* A ring rather than a lighter fill on hover: every lighter step of these two greens and ambers drops
   the white text below 4.5:1, and a badge that becomes unreadable when pointed at is a poor trade for an
   affordance a ring gives just as clearly. */
.stamp:hover,.stamp:focus-visible{box-shadow:0 0 0 2px var(--bar)}
.stamp:focus-visible{outline:none}
/* At its full width the badge is 298px, which needs 338px of viewport once the header's own gutters are
   paid, so on a 320px phone it was the one element on the page wide enough to give the whole document a
   horizontal scrollbar -- measured: 305px of content became 312px. What gives way is the label, never the
   value: the timestamp is the thing the badge exists to say, and "DEPLOYED 2026-09-06 18:07 UTC" loses no
   meaning at all. 360px rather than 338px so the rule lands on a phone width rather than mid-band. */
@media (max-width:360px){.stamp .lw{display:none}}
.top{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap}
.top nav{font-size:13px;color:var(--muted);text-align:right;line-height:1.9}
button{font:inherit;cursor:pointer}
.bar{position:sticky;top:0;z-index:20;background:var(--plane);
  border-bottom:1px solid var(--grid);padding:10px 20px}
.bar .wrap{display:flex;flex-direction:column;gap:8px}
.line{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.line>label{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.06em;
  min-width:74px}
#q{flex:1;min-width:220px;background:var(--surface);color:var(--ink);
  border:1px solid var(--grid);border-radius:7px;padding:9px 12px;font:inherit}
#q:focus{outline:2px solid var(--bar);outline-offset:-1px}
select{background:var(--surface);color:var(--ink);border:1px solid var(--grid);
  border-radius:7px;padding:8px 10px;font:inherit;max-width:100%}
.chip{background:var(--band);color:var(--ink2);border:1px solid var(--grid);
  border-radius:999px;padding:5px 12px;font-size:13px;white-space:nowrap}
.chip:hover{border-color:var(--bar);color:var(--ink)}
.chip[aria-pressed=true]{background:var(--bar);border-color:var(--bar);color:var(--onbar);
  font-weight:600}
/* The new-arrivals chip wears the gold accent rather than the cyan every other chip uses, because it
   is the only filter that answers a question about time rather than about the data. It is also the only
   chip that can be absent: with nothing inside the window there is nothing to filter to, and a control
   that selects zero rows is worse than no control. */
.newchip{display:none;align-items:center;gap:.4em}
.newchip.on{display:inline-flex}
.newchip[aria-pressed=true]{background:var(--warn);border-color:var(--warn);color:var(--onbar)}
.newchip:hover{border-color:var(--warn)}
.ni{width:1em;height:1em;flex:none;vertical-align:-.12em}
.ni>.a{fill:var(--warn)}
.ni>.b{fill:var(--bar)}
.newchip[aria-pressed=true] .ni>.a,.newchip[aria-pressed=true] .ni>.b{fill:var(--onbar)}
.nm .ni{margin-right:.34em}
.newon{color:var(--warn);font-size:12px;font-weight:600;white-space:nowrap}
.count{color:var(--muted);font-size:13px;margin-left:auto;white-space:nowrap}
.count b{color:var(--ink)}
main{padding:0 20px 64px}
table{width:100%;border-collapse:collapse;margin-top:14px}
th{text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);
  padding:8px 10px;border-bottom:1px solid var(--grid);position:sticky;top:0;background:var(--surface)}
th.n,td.n{text-align:right}
th.c,td.c{text-align:center}
td{padding:12px 10px;border-bottom:1px solid var(--grid);vertical-align:top}
/* Guarded, because a touch device reports a hover that then latches: tapping a row anywhere -- to
   follow its link, or just while scrolling -- left it tinted until something else was tapped. */
@media(hover:hover){tr:hover td{background:var(--band)}}
.rk{color:var(--muted);font-size:12px;font-variant-numeric:tabular-nums}
.shot{width:200px}
.shot img{width:200px;aspect-ratio:2/1;object-fit:cover;border-radius:6px;
  background:var(--band);border:1px solid var(--grid);display:block}
/* These two set the table's width. Auto table layout takes the widest unbreakable run in the column
   across every row on the page, and neither a slash nor a comma is a break opportunity in Chrome or
   Safari -- so `muratcankoylan/Agent-` and a blurb naming
   `.cursorrules/CLAUDE.md/Copilot/Windsurf/Cline/Aider` were between them demanding ~530px of a 335px
   content box, which the document then had to scroll sideways to satisfy. */
.nm{font-weight:600;font-size:15px;overflow-wrap:anywhere}
.nwo{display:block;color:var(--muted);font-size:12px;margin-top:2px;word-break:break-all}
.st{font-size:16px;font-weight:700;font-variant-numeric:tabular-nums}
.st.none{font-size:13px;font-weight:400;color:var(--muted)}
.meta{color:var(--muted);font-size:12px;margin-top:5px}
.desc{color:var(--ink2);font-size:13.5px;max-width:44em;overflow-wrap:anywhere}
.cmd{display:block;margin-top:7px;font:12px/1.5 Consolas,ui-monospace,monospace;
  color:var(--ink2);background:var(--band);border:1px solid var(--grid);border-radius:5px;
  padding:5px 8px;max-width:44em;overflow-wrap:anywhere}
/* The install line is the one thing on a row a reader wants to take with them, and taking it meant
   selecting monospace text that wraps mid-flag without catching the surrounding cell. `align-items:
   stretch` so the button matches whatever height the command wrapped to, and `min-width:0` on the code
   so a long one shrinks rather than pushing the button out of the row. */
.cmdrow{display:flex;align-items:stretch;gap:6px;max-width:44em;margin-top:7px}
.cmdrow .cmd{margin-top:0;flex:1 1 auto;min-width:0}
.copy{flex:none;background:var(--band);color:var(--ink2);border:1px solid var(--grid);
  border-radius:5px;padding:0 10px;font-size:11.5px;letter-spacing:.03em;white-space:nowrap}
.copy:hover{border-color:var(--bar);color:var(--ink)}
.copy.ok{border-color:var(--good);color:var(--good)}
.tag{display:inline-block;background:var(--band);border:1px solid var(--grid);border-radius:5px;
  padding:2px 7px;font-size:11.5px;color:var(--ink2);margin:0 4px 4px 0;white-space:nowrap}
.tag.cat{border-color:var(--bar);color:var(--ink)}
/* This rule was dead: the class was defined here but never put on an element, so the verdict row was
   rendering as plain `.meta` the whole time. The nowrap is now on each verdict rather than on the group,
   which is what it was for -- keeping "Win ✓" together, not forcing all five onto one line, which on a
   375px card is 260px of unbreakable text. */
.os{font-size:11.5px;letter-spacing:.02em}
.os>span{white-space:nowrap}
/* Prefixed because the verdict characters are the class names and one of them is "-", which is not a
   valid CSS identifier on its own -- ".-" invalidates the whole selector list it appears in, so the
   unprefixed version silently dropped the colour from every No, n/a and dash on the page. */
.vY{color:var(--good);font-weight:700}
.vL{color:var(--warn)}
.vN,.va,.v-{color:var(--off)}
/* Each verdict also carries a glyph -- see VERDICT in the script. Colour on its own was the only channel
   here, which is WCAG 1.4.1 and fails for a red/green deficiency, a greyscale print-out and a projector
   with the saturation turned down. The glyph is part of the text rather than a pseudo-element so it is
   copied with the row and announced by a screen reader ("check mark", "question mark"). */
.os .v-,.os .va{opacity:.75}
/* A repo with no push in over a year. Deliberately not a colour: amber already means "inferred" in the
   verdict column two cells away, and reusing it here would make one hue mean two things on one row. The
   dotted underline is the marker and the hint that there is a title worth hovering. */
.old{text-decoration:underline dotted;text-decoration-color:var(--muted);text-underline-offset:2px}
/* The approximate-match banner. Left-aligned and directly above the table it explains, because a centred
   notice reads as page furniture and gets skipped -- and this one has to be read, or the reader concludes
   the search ignored them. Amber like the other "this is not quite what you asked for" signals. */
.approx{margin:0 0 14px;padding:10px 14px;border-left:3px solid var(--warn);background:var(--band);
  border-radius:0 6px 6px 0;color:var(--ink2);font-size:14px}
.approx b{color:var(--ink)}
.empty{padding:64px 0 80px;text-align:center;color:var(--muted)}
/* "Nothing matches. Try clearing a filter." named neither the filter nor what clearing it would return,
   so the reader had to guess which of six controls was the tight one -- and it is usually not the one
   they touched last. Each button here is a filter to drop with the count it would restore. */
.empty .big{color:var(--ink);font-size:17px;font-weight:600;margin:0 0 6px}
.empty p{margin:0 0 12px}
.fixes{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
.fix{background:var(--band);color:var(--ink);border:1px solid var(--grid);border-radius:999px;
  padding:7px 15px;font-size:13.5px}
.fix:hover{border-color:var(--bar)}
.fix .n{color:var(--muted);font-variant-numeric:tabular-nums}
.fix:hover .n{color:var(--ink2)}
.more{display:block;margin:26px auto 0;background:var(--band);color:var(--ink);
  border:1px solid var(--grid);border-radius:8px;padding:11px 22px;font-weight:600}
.more:hover{border-color:var(--bar)}
footer{border-top:1px solid var(--grid);background:var(--plane);padding:22px 20px;
  color:var(--muted);font-size:13px}
.blurb{color:var(--muted);font-size:13px;margin:2px 0 0}
.facets{margin-top:14px;padding-top:12px;border-top:1px solid var(--grid);font-size:12.5px;
  line-height:1.9}
.facets p{margin:0 0 4px}
.facets b{color:var(--ink2);font-weight:600}
/* One query used to do all the responsive work here and all it did was hide two columns, so a 375px
   phone got the same layout as an 899px tablet. There are three now, because the page fails in three
   different ways: at 900px the screenshot and the detail columns stop paying for their width; below
   640px four columns stop fitting in what is left at all; and the filter bar fails on *height*, which
   is a separate axis and needs its own query -- see below. */
@media(max-width:900px){
  .shot,.hide{display:none}
  td,th{padding:9px 6px}
}

/* The filter bar competes for vertical space, so it is capped on vertical space -- either axis can
   trigger it. Width alone was not enough: a landscape phone is 844x390, wide enough to clear a 640px
   breakpoint entirely and short enough that the wrapped bar measured 360px of a 390px window. That is
   92% of the screen, which is the reported bug with the phone turned on its side.

   The failure being fixed: a `position:sticky` box taller than its scrollport pins its top edge and
   then covers the screen for the whole of the rest of the document, and the part of it that overflows
   the bottom can never be scrolled into view -- which is what put the Runs-on chips, Confirmed only
   and Clear all permanently out of reach. At 390x844 the bar measured 753px, 89% of the screen, and on
   a 375x667 phone it was taller than the viewport. The 27 topic and target chips are what grew it:
   they were wrapping to sixteen lines between them, so each facet becomes one scrollable rail. */
@media(max-width:640px),(max-height:560px){
  /* iOS Safari zooms the viewport whenever a focused control's text is under 16px, and because the
     viewport tag sets initial-scale=1 with no maximum-scale it never zooms back out again on blur. So
     one tap on the search box left the reader at ~350px of effective width, scrolling sideways, for
     the rest of the visit -- a second, self-inflicted cause of the horizontal scrolling. */
  #q,select{font-size:16px}
  .facet{flex-wrap:nowrap;gap:6px}
  .facet>label{flex:none;min-width:0;font-size:10px}
  .facet>.chip{flex:none}
  /* `flex:1 1 0` with `min-width:0` is what lets a rail sit beside its label and take the width that
     is left. Without the zero basis the rail asks for its full max-content width -- 2,400px of topic
     chips -- and gets bumped onto a line of its own, which is two rows per facet again. */
  #cats,#tgts,#oses{display:flex;flex-wrap:nowrap;gap:6px;overflow-x:auto;
    flex:1 1 0;min-width:0;
    scrollbar-width:none;overscroll-behavior-x:contain;-webkit-overflow-scrolling:touch}
  #cats::-webkit-scrollbar,#tgts::-webkit-scrollbar,#oses::-webkit-scrollbar{display:none}
  .bar .wrap{gap:5px}
  .chip{padding:4px 11px}
  /* And a cap on top of the rails, because rails alone still leave four to six control rows. On a tall
     screen the cap sits above the bar's natural height and nothing happens; on a short one the bar
     scrolls inside itself instead of over the page. A fraction rather than a pixel count so that it
     only ever binds where it is needed. `vh` first: a browser that does not understand `dvh` must
     still get a cap rather than none. */
  .bar{max-height:44vh;max-height:44dvh;overflow-y:auto}
}

@media(max-width:640px){
  /* 20px gutters on all four sections cost 40px, 11% of a 375px screen, and the old query left them. */
  header{padding:16px 14px 12px}
  .bar{padding:8px 14px}
  main{padding:0 14px 48px}
  footer{padding:18px 14px}
  h1{font-size:21px}
  h1 span{display:block;font-size:13px}
  .top{gap:10px}
  .top nav{text-align:left;line-height:2.1}

  #q{flex:1 1 100%;min-width:0}
  .line>label[for=q]{display:none}
  .count{margin-left:0;font-size:12px}
  /* Runs-on is the one facet that also carries Confirmed only and Clear all, and at 390px those two
     left its rail about 110px -- one OS chip at a time. That line alone wraps, so the rail keeps most
     of the row and the two buttons drop underneath it. Narrow-only: in landscape there is width enough
     for all four to share the row, and wrapping there would cost a row the bar cannot spare. */
  .facet:has(>.chip){flex-wrap:wrap}
  .facet:has(>.chip)>#oses{flex:1 1 auto;min-width:62%}

  /* A row stops being a row. Four columns cannot share 335px -- the blurb on its own wants more than
     that -- so each row becomes a card, and the headings, no longer above anything, go away. */
  thead{display:none}
  table,tbody,tr,td{display:block}
  table{margin-top:12px}
  tr{display:grid;grid-template-columns:1fr auto;gap:1px 12px;align-items:start;
    border:1px solid var(--grid);border-radius:10px;padding:11px 13px;margin:0 0 9px}
  td{border-bottom:0;padding:0}
  td.rk{grid-column:1;grid-row:1;text-align:left}
  td.st-c{grid-column:2;grid-row:1}
  td.pj{grid-column:1/-1;grid-row:2}
  td.ds{grid-column:1/-1;grid-row:3;margin-top:6px}
  /* The two `.hide` columns are dropped at 900px and, until now, never came back -- so a phone reader
     silently lost the topic and target tags and the language, licence and push date. That was a width
     decision inherited from the table, and a card is not competing for column width: it has a whole row
     to spend. `td.hide` outranks the `.hide` that hid them, so this wins without touching that rule and
     without affecting the 641-900px range, where the layout really is still a table.
     A higher specificity than `.hide`, not a later position, is what makes that true. */
  td.hide{display:block}
  td.tg{grid-column:1/-1;grid-row:4;margin-top:8px}
  td.lc{grid-column:1/-1;grid-row:5;margin-top:2px;text-align:left}
  /* Three stacked lines is right in a centred 90px column and wrong on a card, where the same three
     facts fit on one line. The <br>s are the table's formatting, so they go away here rather than
     being conditionally emitted -- the markup stays one shape and the layout decides how to read it. */
  td.lc .meta{display:flex;flex-wrap:wrap;gap:4px 12px}
  td.lc .meta br{display:none}
  .st{font-size:15px}
  .desc{font-size:13px}
  .more{width:100%}
  .cmdrow{max-width:none}
}

/* Nothing here animates on a timer, but the chip hovers transition and the chip rails scroll smoothly,
   and both are motion a reader can have asked their operating system not to show them. A blanket rule is
   safe because no state on this page is communicated *by* an animation -- removing every one of them
   changes nothing but the easing. */
@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.01ms !important;animation-iteration-count:1 !important;
    transition-duration:.01ms !important;scroll-behavior:auto !important}
}

/* Focus lands on a row after "Show more", so the row needs somewhere to put a ring and needs to clear
   the sticky filter bar if anything ever does scroll it into view. */
#out tr:focus{outline:2px solid var(--bar);outline-offset:-2px}
#out tr{scroll-margin-top:160px}
</style>
</head>
<body>
<a class="skip" href="#out">Skip to results</a>
<!-- One shared region for anything the page needs to say that is not already text on the screen: a copy
     succeeding, a clipboard being refused, how many rows "Show more" just added. The result count has its
     own role=status on #count, because that one *is* visible text and should be announced from where it
     is rather than duplicated here. -->
<span class="sr" id="live" role="status" aria-live="polite"></span>
<!-- Drawn here rather than borrowed so there is no third-party licence attached to a 300-byte glyph: a
     four-point star with concave arms, plus a smaller one trailing it. Two tones, gold and cyan, which
     is the theme's own pair -- the mark for "new" is the mark for this site, not a generic sparkle.

     Two symbols on one shared viewBox rather than one symbol with two classed paths, because a CSS rule
     cannot reach inside the shadow tree a <use> builds: `.ni .a{fill:...}` matches nothing, and the
     paths fall back to black, which on this surface is an invisible icon. `fill` *is* inherited, though,
     so colouring the two <use> elements -- which are in the ordinary document -- reaches the clones.
     Both symbols share `viewBox="0 0 16 16"`, so the two halves land in one 16x16 space and overlap
     exactly as drawn. -->
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="star-a" viewBox="0 0 16 16">
    <path d="M6.4.8Q7.63 5.17 12 6.4Q7.63 7.63 6.4 12Q5.17 7.63.8 6.4Q5.17 5.17 6.4.8Z"/></symbol>
  <symbol id="star-b" viewBox="0 0 16 16">
    <path d="M12.6 9.6Q13.26 11.94 15.6 12.6Q13.26 13.26 12.6 15.6Q11.94 13.26 9.6 12.6Q11.94 11.94 12.6 9.6Z"/></symbol>
</svg>
<header><div class="wrap"><div class="top">
  <div>
    <h1>Awesome Agentic Atlas <span>· eleven awesome-lists, merged</span></h1>
    <p class="sub"><b>__COUNT__</b> projects · <b>__TOPICS__</b> topics · <b>__STARS__</b> combined
      stars · <span id="snap" title="Rebuilt daily from the GitHub API">snapshot
      __SNAPSHOT__</span></p>
    <p class="blurb" id="ctx"></p>
    <!-- The DOM text is sentence case and the uppercase is `text-transform`, so the accessible name reads
         "Last deployed 2026-09-06 18:07 UTC" rather than being spelled out, and no aria-label is needed to
         paper over the styling. `<time>` because this is a timestamp and something will want to read it.
         The href goes to the deployment history, which is where the badge's own claim can be checked.
         The line break between the two spans is load-bearing: without a text node between them the
         accessible name comes out as "Last deployed2026-09-06 18:07 UTC", run together. A flex container
         drops whitespace-only children, so it costs nothing in layout. -->
    <a class="stamp" id="deployed" href="https://github.com/__REPO__/deployments"
       title="When this copy of the site was published."><span class="k"><span class="lw">Last </span>deployed</span>
      <span class="v"><time datetime="__BUILT__">__BUILT_UTC__</time></span></a>
  </div>
  <nav>
    <a href="https://github.com/__REPO__">Repository</a> ·
    <a href="https://github.com/__REPO__/tree/main/mega-list">Markdown edition</a> ·
    <a href="https://github.com/__REPO__/releases/latest">Workbook</a><br>
    <!-- No aria-pressed. The label names the action and changes with the state, and "Dark theme" plus
         pressed=true announces as "dark theme is on" -- which is the opposite of what it means. A toggle
         gets a static label and a pressed state, or a changing label and no pressed state; this is the
         second. It also stops the button rendering as a filled accent pill purely because the reader is
         in light mode, which made it look like an active filter. -->
    <button class="chip" id="theme">Light theme</button>
  </nav>
</div></div></header>

<div class="bar"><div class="wrap">
  <div class="line">
    <label for="q">Search</label>
    <!-- aria-label as well as the <label>, because the narrow-viewport rule sets `display:none` on
         `label[for=q]` and that removes it from the accessibility tree as well as from the screen -- so
         on a phone the search box had no accessible name at all. -->
    <input id="q" type="search" aria-label="Search projects"
           placeholder="name, repo, description, language&hellip;"
           autocomplete="off" spellcheck="false">
    <select id="sort" aria-label="Sort by">
      <!-- Best match is the default, and it is deliberately not a hidden mode. Ranking search results
           without saying so would silently override a sort the reader had chosen; as an option they can
           see selected, and move away from, the behaviour explains itself. With an empty box it has
           nothing to rank and falls through to Most stars, which is what this page has always opened on. -->
      <option value="relevance">Best match</option>
      <option value="stars">Most stars</option>
      <option value="lists">Named by most lists</option>
      <option value="pushed">Pushed most recently</option>
      <option value="name">Name (A&ndash;Z)</option>
    </select>
    <button class="chip newchip" id="new" aria-pressed="false"
            title="Projects the source lists added in the last __WINDOW__ days">
      <svg class="ni"><use class="a" href="#star-a"></use><use class="b" href="#star-b"></use></svg>
      <span id="newlabel">New</span></button>
    <!-- role=status makes this a polite live region, so pressing a chip or typing a search announces the
         new result count instead of silently rewriting a number the reader cannot see. aria-atomic so it
         is read as one sentence rather than as whichever digits changed. -->
    <span class="count" id="count" role="status" aria-atomic="true"></span>
  </div>
  <div class="line facet"><label>Topic</label><span id="cats"></span></div>
  <div class="line facet"><label>Plugs into</label><span id="tgts"></span></div>
  <div class="line facet"><label>Runs on</label><span id="oses"></span>
    <button class="chip" id="strict" aria-pressed="false"
            title="Drop rows where support is inferred from the language rather than stated">Confirmed
      only</button>
    <button class="chip" id="reset">Clear all</button>
  </div>
</div></div>

<main><div class="wrap"><div id="out"></div></div></main>

<footer><div class="wrap">
  Every entry came from someone else's curation work; all eleven source lists are credited in the
  <a href="https://github.com/__REPO__#the-eleven-lists">repository</a>. Stars, language, licence and
  last-push come from the GitHub API on __SNAPSHOT__ and drift daily. Platform verdicts are derived
  from each project's own README, install route, CI config and release assets &mdash;
  <span class="vY">green&#8201;&#10003;</span> is stated evidence,
  <span class="vL">amber&#8201;?</span> is inferred from the language, and
  <span class="vN">grey&#8201;&#10007;</span> is neither. The glyph says the same thing the colour does,
  so the column still reads in greyscale, in print, and with a colour-vision deficiency. A push date
  <span class="old">underlined like this</span> means nothing has landed in that repo for over a year.
  A dash in the star column means the row is a folder inside someone else's repo, or a dead
  link, and has no count of its own.
  <!-- Every filtered view of this page lives in the hash, which a crawler will not execute -- so the 156
       prerendered pages under topic/ and target/ were reachable only from sitemap.xml, and a sitemap is a
       hint rather than a path. These 26 links put each one click from the root and each crossing two.
       Built in `substitute()` from the same `cats`/`targets` the page itself uses, so a new topic appears
       here without anyone remembering to add it. -->
  <nav class="facets" aria-label="Browse by topic or by what a project plugs into">
    <p><b>Every topic:</b> __TOPICLINKS__</p>
    <p><b>Every integration:</b> __TARGETLINKS__</p>
  </nav>
</div></footer>

<script>
const PAGE_SIZE = 120;
const state = {q: "", cat: "", tgt: "", os: [], strict: false, fresh: false,
               sort: "relevance", shown: PAGE_SIZE};
let D = null, ROWS = [], NEW = 0;
// The pending debounced search, if any. Declared out here rather than beside the handler because `set()`
// has to cancel it, and `set()` is not inside the fetch callback where the handlers are wired.
let typing = 0;

// The window is applied here, in the browser, against the reader's own clock -- `data.json` carries the
// raw first-seen date and nothing else. That is what makes the mark expire without a rebuild: a repo
// stamped the 14th stops being new on the 29th in every open tab, on a day the cron may not have run.
// Both sides of the subtraction are ISO dates, which Date.parse reads as UTC midnight, so the result is
// a whole number of days and never 13.958 because of a timezone.
const TODAY = new Date().toISOString().slice(0, 10);
const daysAgo = iso => Math.round((Date.parse(TODAY) - Date.parse(iso)) / 86400000);
const mmddyy = iso => iso.slice(5, 7) + "/" + iso.slice(8, 10) + "/" + iso.slice(2, 4);
const SNAPSHOT = "__SNAPSHOT__";
const BUILT = "__BUILT__";

// Colour was the only thing distinguishing a stated Yes from an inferred Maybe from a No, which is a
// WCAG 1.4.1 failure and, more plainly, unreadable for anyone with a red/green deficiency. Each verdict
// now carries a glyph as well, chosen so that its screen-reader pronunciation is also the meaning:
// "check mark", "question mark", "ballot x". A tilde would have read as "tilde".
const VERDICT = {
  Y: ["✓", "stated support"],
  L: ["?", "inferred from the language"],
  N: ["✗", "no evidence of support"],
  a: ["–", "not applicable"],
  "-": ["–", "not established"],
};

// Feature-detected rather than assumed, and the button is simply not rendered when the answer is no --
// 120 buttons that fail on click are worse than none. `isSecureContext` is part of the test because the
// API exists but always rejects on plain http, which is how a contributor serving docs/ locally sees it.
const CAN_COPY = !!(navigator.clipboard && navigator.clipboard.writeText && window.isSecureContext);

// The rescue buttons drawn on an empty table, in the order render() drew them. Kept out of the markup
// because a filter patch is an object -- serialising it into a data- attribute and parsing it back would
// be two more chances to get the OS index array wrong.
let RESCUE = [];

// A live region only fires on a *change*, so setting the same string twice announces once -- which is
// exactly the case here, since copying two install lines in a row produces the same sentence. The clear
// and the tick force a second announcement.
function say(msg) {
  const el = document.getElementById("live");
  el.textContent = "";
  setTimeout(() => { el.textContent = msg; }, 30);
}

// Relative, because the question a reader is asking of this column is "is this thing alive", and nobody
// does date arithmetic in their head. Rounding is safe: the exact date stays in the title. Past a year
// it gets the dotted marker -- quietly, because a dormant repo is a fact about the repo, not a verdict.
function since(iso) {
  if (!iso) return "—";
  const d = daysAgo(iso);
  const t = d <= 0 ? "today" : d === 1 ? "yesterday" : d < 30 ? d + "d ago"
    : d < 365 ? Math.round(d / 30) + "mo ago"
    : d < 730 ? (d / 365).toFixed(1) + "y ago" : Math.floor(d / 365) + "y ago";
  return d >= 365
    ? '<span class="old" title="' + iso + ' — no push in over a year">' + t + "</span>"
    : '<span title="' + iso + '">' + t + "</span>";
}

fetch("data.json").then(r => {
  // The only place the real deployment time is available, and it arrives on a request the page was going
  // to make anyway. See `deployStamp`. Before `r.json()`, because that consumes the body and there is no
  // reason to wait for 561 KB to parse before correcting a badge that is already on screen.
  deployStamp(r.headers.get("Last-Modified"));
  return r.json();
}).then(d => {
  D = d;
  // Column-oriented on the wire, objects in here. One pass, 1,294 times, so the rest of the page can
  // read `r.stars` instead of `r[4]`.
  ROWS = d.rows.map(a => Object.fromEntries(d.cols.map((c, i) => [c, a[i]])));
  ROWS.forEach(r => {
    r.hay = (r.name + " " + r.nwo + " " + r.blurb + " " + r.lang + " " + r.listed_by).toLowerCase();
    // `hay` answers "does this row match" and cannot answer "where did it match", which is the only
    // question ranking cares about. Lowercasing the three fields separately here rather than inside the
    // scorer keeps 1,294 * 5 `toLowerCase` calls out of every keystroke.
    r.lname = r.name.toLowerCase();
    r.lnwo = r.nwo.toLowerCase();
    r.lblurb = (r.blurb || "").toLowerCase();
    r.img = r.img || ("https://opengraph.githubassets.com/1/" + r.nwo);
    const age = r.first_seen ? daysAgo(r.first_seen) : Infinity;
    r.isnew = age >= 0 && age <= (d.window_days || 14);
  });
  NEW = ROWS.filter(r => r.isnew).length;
  buildChips();
  readHash();
  render();
}).catch(err => {
  // A browser will not let a file:// page fetch a sibling file, so double-clicking index.html out of a
  // clone loads the chrome and then nothing at all, with the reason only in the console. Anyone doing
  // that is a contributor, so the message is the two commands that fix it rather than an apology.
  document.getElementById("count").innerHTML =
    "Could not load <code>data.json</code> — " + String(err);
  document.getElementById("out").innerHTML =
    '<p style="max-width:62ch;line-height:1.6">If you opened this file straight off disk, that is ' +
    'expected: browsers refuse to let a <code>file://</code> page read a sibling file. Serve the ' +
    'folder instead — <code>python -m http.server</code> from <code>docs/</code>, then open ' +
    '<code>localhost:8000</code>. The published copy is at ' +
    '<a href="__SITE__">__SITE__</a>.</p>';
});

// Before the fetch resolves, deliberately: none of this needs the data, and the theme toggle in
// particular should work on the error page as well as on the atlas.
wire();

function chip(parent, label, pressed, onclick, title) {
  const b = document.createElement("button");
  b.className = "chip";
  b.textContent = label;
  b.setAttribute("aria-pressed", pressed ? "true" : "false");
  if (title) b.title = title;
  b.onclick = onclick;
  parent.appendChild(b);
  return b;
}

function buildChips() {
  const cats = document.getElementById("cats"), tgts = document.getElementById("tgts"),
        oses = document.getElementById("oses");
  chip(cats, "All", true, () => set({cat: ""}));
  D.cats.forEach(c => chip(cats, c.name, false, () => set({cat: c.slug}), c.blurb));
  chip(tgts, "All", true, () => set({tgt: ""}));
  D.targets.forEach(t => chip(tgts, t.name, false, () => set({tgt: t.slug}), t.blurb));
  D.os.forEach((o, i) => chip(oses, o, false, () => {
    const os = state.os.includes(i) ? state.os.filter(x => x !== i) : state.os.concat(i);
    set({os});
  }));
  // Debounced, because `render()` costs ~58ms at today's 1,294 rows on a throttled mobile CPU and used to
  // run once per keystroke -- so typing "agentic" rebuilt a 120-row table seven times and the input
  // visibly trailed the keyboard. Only ~20ms of that is row-count dependent; the rest is the innerHTML
  // rebuild and layout, so this is a defect at the current size and not only a future one. 150ms is short
  // enough to still read as live and collapses those seven renders into one.
  document.getElementById("q").oninput = e => {
    const v = e.target.value;
    clearTimeout(typing);
    typing = setTimeout(() => set({q: v}, true), 150);
  };
  document.getElementById("sort").onchange = e => set({sort: e.target.value});
  document.getElementById("strict").onclick = () => set({strict: !state.strict});
  // Shown only when it would select something. The label carries the count because the whole question
  // this chip answers is "is there anything new", and a reader should be able to see the answer without
  // clicking and then having to click back.
  const nb = document.getElementById("new");
  if (NEW) {
    nb.classList.add("on");
    document.getElementById("newlabel").textContent = "New · " + NEW.toLocaleString();
    nb.onclick = () => set({fresh: !state.fresh});
  }
  document.getElementById("reset").onclick = () => set(CLEAR);
  window.addEventListener("hashchange", () => { readHash(); render(); });
}

const CLEAR = {q: "", cat: "", tgt: "", os: [], strict: false, fresh: false};

// Theme and clipboard are wired outside buildChips because buildChips only runs once `data.json` has
// arrived. When the fetch fails -- a contributor opening the file off disk, which the catch block above
// exists for -- the toggle used to be dead too, so the error page could not be read in light mode.
function wire() {
  const btn = document.getElementById("theme");
  const label = () => {
    const light = document.documentElement.dataset.theme === "light";
    btn.textContent = light ? "Dark theme" : "Light theme";
    btn.title = "Switch to the " + (light ? "dark" : "light") + " theme";
  };
  btn.onclick = () => {
    const light = document.documentElement.dataset.theme !== "light";
    document.documentElement.dataset.theme = light ? "light" : "dark";
    // The choice is the point: it used to last until the next navigation, so a reader who needs light
    // re-picked it on every page load and every shared filter link.
    try { localStorage.setItem("theme", light ? "light" : "dark"); } catch (e) {}
    label();
  };
  // The head script already resolved the theme; this only has to agree with it, since the markup's
  // hardcoded "Light theme" is wrong half the time now that the OS preference is honoured.
  label();
  // Follow the OS live, but only for a reader who has not overridden it -- flipping someone out of a
  // theme they explicitly chose because the sun went down is worse than not following at all.
  try {
    matchMedia("(prefers-color-scheme: light)").addEventListener("change", ev => {
      if (localStorage.getItem("theme")) return;
      document.documentElement.dataset.theme = ev.matches ? "light" : "dark";
      label();
    });
  } catch (e) {}

  // One delegated listener rather than one per button: `render()` replaces the whole subtree on every
  // keystroke, so per-row handlers would be 120 attachments discarded 120 times a second of typing.
  document.getElementById("out").addEventListener("click", ev => {
    const fix = ev.target.closest(".fix");
    if (fix) {
      if (fix.dataset.all) return set(CLEAR);
      const o = RESCUE[+fix.dataset.i];
      if (o) set(o.patch);
      return;
    }
    const b = ev.target.closest(".copy");
    if (b) copy(b);
  });
  stamp();
  // With no argument, so the badge shows `BUILT` and gets its relative age and tooltip immediately. The
  // fetch calls it again with the header when it lands, which is the only time the value changes. Wired
  // here rather than only there because `wire()` also runs on the error page, where the fetch never
  // resolves and a badge frozen at its rendered-in markup would have no age on it at all.
  deployStamp();
}

// writeText rejects rather than throws -- denied permission, a document that is not focused, an
// http origin -- so the failure path has to be real. Selecting the command is the fallback that leaves
// the reader one keystroke from the same result, which is better than a button that shrugs.
function copy(b) {
  const cmd = b.dataset.cmd;
  const flash = (text, ok) => {
    b.textContent = text;
    b.classList.toggle("ok", !!ok);
    setTimeout(() => { b.textContent = "Copy"; b.classList.remove("ok"); }, 1800);
  };
  navigator.clipboard.writeText(cmd).then(() => {
    flash("Copied", true);
    say("Copied " + cmd);
  }, () => {
    const code = b.parentNode.querySelector(".cmd");
    if (code) {
      const r = document.createRange();
      r.selectNodeContents(code);
      const s = getSelection();
      s.removeAllRanges();
      s.addRange(r);
    }
    flash("Ctrl+C");
    say("The clipboard was refused. The command is selected — press Control C to copy it.");
  });
}

// An ISO date answers "when" and not "is this current", which is the question. Amber past a fortnight
// because that is the point at which the star counts on the page have measurably drifted from GitHub's.
function stamp() {
  const el = document.getElementById("snap");
  if (!el) return;
  const d = daysAgo(SNAPSHOT);
  const age = d <= 0 ? "today" : d === 1 ? "yesterday" : d + " days ago";
  el.innerHTML = "snapshot " + SNAPSHOT + " · <span class=\"" + (d > 14 ? "stale" : "fresh") +
    '">' + age + "</span>";
  el.title = d > 14
    ? "The daily rebuild has not run in " + d + " days, so stars and push dates here have drifted."
    : "Rebuilt daily from the GitHub API.";
}

// The badge under the masthead. Two sources for one value, in order of authority.
//
// `Last-Modified` on the `data.json` response is the real answer. Pages stamps every file it serves with
// the moment the deployment carrying it was published -- `index.html` and `data.json` come back with the
// same second, which is what proves it is the deployment's clock and not any file's own mtime -- so this
// is the publish time of the exact bytes on screen, and it is free, because the page fetches that file
// regardless. It is also the only value that *can* be right: the commit carrying this page is what
// triggers the deployment that publishes it, so nothing known at build time could have said it.
//
// `BUILT` is the fallback, and the reason the badge is never blank or wrong-looking: it is what the copy
// in the repository shows, what a local `python -m http.server` shows, where there is no deployment to
// describe, and what is on screen for the few hundred milliseconds before the fetch resolves. It runs a
// minute or two ahead of the deployment it precedes, which is inside the minute the badge prints.
//
// Nothing in here may throw. The caller is the first link of the `data.json` promise chain, and an
// exception raised here would land in the `.catch` at the end of it and be reported to the reader as
// "could not load data.json" -- a badge failing would blank the atlas and misattribute why.
function deployStamp(lastModified) {
  try {
    const el = document.getElementById("deployed");
    if (!el) return;
    const live = Date.parse(lastModified || "");
    const ms = Number.isNaN(live) ? Date.parse(BUILT) : live;
    if (Number.isNaN(ms)) return;
    const iso = new Date(ms).toISOString();
    const shown = iso.slice(0, 10) + " " + iso.slice(11, 16) + " UTC";
    const t = el.querySelector("time");
    t.dateTime = iso;
    t.textContent = shown;
    // The same fortnight `stamp()` uses, deliberately -- one staleness threshold in the header rather than
    // two to learn. It is the right number for this clock too: the daily build is gated on a source list
    // having moved, so a quiet week is healthy and a tighter bound would cry wolf, but the weekly rebuild
    // publishes unconditionally, so past 14 days both crons have stopped and the page is on its own.
    const days = (Date.now() - ms) / 86400000;
    el.classList.toggle("late", days > 14);
    const age = days < 1 ? "Today." : days < 2 ? "Yesterday." : Math.round(days) + " days ago.";
    el.title = (Number.isNaN(live)
      ? "Built " + shown + ". This copy is not served by Pages, so its deployment time is unknown. "
      : "Published to GitHub Pages " + shown + ". ") + age
      + (days > 14 ? " Neither scheduled rebuild has run since, so the data here has drifted." : "");
  } catch (e) {}
}

function set(patch, keepFocus) {
  // Any other interaction outranks a search the reader has stopped waiting for. Without this, tapping
  // Clear all inside the 150ms window let the queued timer land afterwards and re-apply the term that was
  // just cleared: empty box, filtered table, `#q=` back in the URL. The debounce made every filter control
  // racy against the search box, so the cancel belongs here, on the shared path, not on each handler.
  clearTimeout(typing);
  Object.assign(state, patch, {shown: PAGE_SIZE});
  writeHash();
  render();
  // A rescue button or Clear all can change the search term, and the box has to say so. Skipped while
  // typing, where the box is the source of the change and rewriting its value moves the caret to the end.
  if (!keepFocus) {
    const q = document.getElementById("q");
    if (q.value !== state.q) q.value = state.q;
    q.blur();
  }
}

// Every filter lives in the hash, so any view is a link. This is the whole point of the page: a
// Markdown file can be one topic or one target, never the crossing of the two.
function writeHash() {
  const p = new URLSearchParams();
  if (state.q) p.set("q", state.q);
  if (state.cat) p.set("topic", state.cat);
  if (state.tgt) p.set("target", state.tgt);
  if (state.os.length) p.set("os", state.os.map(i => D.os[i].toLowerCase()).join(","));
  if (state.strict) p.set("confirmed", "1");
  if (state.fresh) p.set("new", "1");
  if (state.sort !== "relevance") p.set("sort", state.sort);
  const s = p.toString();
  history.replaceState(null, "", s ? "#" + s : location.pathname);
}

function readHash() {
  const p = new URLSearchParams(location.hash.slice(1));
  const slugs = l => l.map(x => x.slug);
  state.q = p.get("q") || "";
  state.cat = slugs(D.cats).includes(p.get("topic")) ? p.get("topic") : "";
  state.tgt = slugs(D.targets).includes(p.get("target")) ? p.get("target") : "";
  const names = D.os.map(o => o.toLowerCase());
  state.os = (p.get("os") || "").split(",").map(s => names.indexOf(s.trim())).filter(i => i >= 0);
  state.strict = p.get("confirmed") === "1";
  // A `#new=1` link outlives the fortnight it was written in. Honouring it once the window has emptied
  // would greet the reader with "nothing matches"; dropping it shows them the atlas instead.
  state.fresh = p.get("new") === "1" && NEW > 0;
  // Every `#sort=stars` link written before Best match existed still says exactly what it said then,
  // because the name is unchanged and only the *default* moved.
  state.sort = SORT_KEYS.includes(p.get("sort")) ? p.get("sort") : "relevance";
  document.getElementById("q").value = state.q;
  document.getElementById("sort").value = state.sort;
}

// "Does this run on my Windows machine" has two answers -- a native build, or reachable through WSL2 --
// and the workbook's Windows sheet counts both, which is where the 1,105 in the README comes from. They
// stay two columns, because a reader without WSL2 needs to see which is which, but the chip has to mean
// the same thing the same word means everywhere else in this project. WSL2 only ever counts as Yes:
// "probably works under WSL2" is not a claim anything here makes.
const OS_ANY = {0: [[0, "YL"], [1, "Y"]]};

function match(r) {
  if (state.fresh && !r.isnew) return false;
  if (state.cat && D.cats[r.cat].slug !== state.cat) return false;
  if (state.tgt) {
    const want = D.targets.findIndex(t => t.slug === state.tgt);
    if (!r.targets.includes(want)) return false;
  }
  for (const i of state.os) {
    const ways = OS_ANY[i] || [[i, "YL"]];
    const ok = ways.some(([k, allow]) =>
      (state.strict ? "Y" : allow).includes(r.os[k]));
    if (!ok) return false;
  }
  if (state.q) {
    for (const w of state.q.toLowerCase().split(/\s+/).filter(Boolean))
      if (!r.hay.includes(w)) return false;
  }
  return true;
}

// What the table would hold with one filter relaxed. Mutate-count-restore rather than threading a state
// argument through `match`, because `match` is called 1,294 times per keystroke and an extra parameter on
// the hot path to serve a case that only fires on an empty table is the wrong trade. The patches only ever
// replace `state.os` wholesale, never mutate it, so restoring the reference restores the value.
function countWith(patch) {
  const saved = Object.assign({}, state);
  Object.assign(state, patch);
  const n = ROWS.filter(match).length;
  Object.assign(state, saved);
  return n;
}

// Ranked by what each one would return, so the first button is the most productive thing to click. A
// filter whose removal still leaves nothing is dropped -- offering it would be a second dead end.
function rescue() {
  const opts = [];
  if (state.q) opts.push(["Drop the search “" + state.q + "”", {q: ""}]);
  if (state.cat) {
    const c = D.cats.find(x => x.slug === state.cat);
    if (c) opts.push(["Drop topic " + c.name, {cat: ""}]);
  }
  if (state.tgt) {
    const t = D.targets.find(x => x.slug === state.tgt);
    if (t) opts.push(["Stop requiring " + t.name, {tgt: ""}]);
  }
  state.os.forEach(i => opts.push(["Drop " + D.os[i], {os: state.os.filter(x => x !== i)}]));
  if (state.strict) opts.push(["Allow inferred support", {strict: false}]);
  if (state.fresh) opts.push(["Drop the new-arrivals filter", {fresh: false}]);
  return opts.map(o => ({label: o[0], patch: o[1], n: countWith(o[1])}))
    .filter(o => o.n > 0)
    .sort((a, b) => b.n - a.n)
    .slice(0, 4);
}

// Trigram overlap, not Levenshtein: "langraph" vs "LangGraph" is one deletion but "claude cdoe" vs
// "Claude Code" is a transposition inside a two-word name, and trigrams handle both without a matrix.
// Padding with spaces makes the first and last characters count, which is where typos cluster.
// Only ever runs on an empty table, so 1,294 set builds is a few milliseconds nobody waits for -- and it
// is memoised on the row anyway, because a reader who mistypes once usually mistypes twice.
function grams(s) {
  const p = " " + s.toLowerCase().replace(/\s+/g, " ").trim() + " ", out = new Set();
  for (let i = 0; i + 3 <= p.length; i++) out.add(p.slice(i, i + 3));
  return out;
}

// Rows matching every filter *except* the search box, ranked by how close their name is to what was
// typed. Only ever called when the exact pass returned nothing, which is what makes it safe: a query that
// does match is never diluted with approximate results, and the cost is paid on the one render where the
// reader would otherwise be staring at an empty table.
//
// It relaxes the search box and nothing else. A reader who has picked a topic and an OS has told us
// something they meant; the typo is in the word they were still typing, so the other filters stand.
function near(q) {
  const want = grams(q);
  // Under three trigrams is a five-character fragment -- a prefix someone is mid-way through typing
  // rather than a misspelling of anything, and matching it loosely would be noise.
  if (want.size < 3) return [];
  const saved = state.q;
  state.q = "";
  const pool = ROWS.filter(match);
  state.q = saved;
  const out = [];
  for (const r of pool) {
    if (!r.g) r.g = grams(r.name);
    let hit = 0;
    want.forEach(g => { if (r.g.has(g)) hit++; });
    // Divided by the larger of the two so a long name cannot win by containing a short query, which is
    // what an unnormalised count does -- every three-letter search matched the longest title on the page.
    const score = hit / Math.max(want.size, r.g.size);
    if (score >= 0.3) { r.rel = score; out.push(r); }
  }
  // Capped, because past the first handful these stop being plausible corrections and start being a
  // second way to say "nothing matched".
  return out.sort(SORTS.relevance).slice(0, 12);
}

// Where a query word landed, in descending order of what that tells us. A word in the project's own name
// is the strongest signal available; a word in the list of source lists that named it is the weakest,
// because every row from that list shares it. A prefix outranks a mid-word hit because that is how people
// type -- "lang" is someone reaching for LangGraph, not for the word "multi-language" in a blurb.
//
// The numbers are ordinal, not measured. What matters is the gaps: a name hit must be unreachable by any
// number of blurb hits, or a project merely *described* as an orchestrator outranks the one called it.
function hitScore(r, w) {
  if (r.lname === w) return 120;
  if (r.lname.startsWith(w)) return 90;
  const n = r.lname.indexOf(w);
  // A word boundary is anything that is not alphanumeric, so "code" scores as a word in "Claude Code"
  // and "Claude-Code" alike, but not inside "Decoder".
  if (n > 0) return /[a-z0-9]/.test(r.lname[n - 1]) ? 45 : 70;
  if (r.lnwo.includes(w)) return 30;
  if ((r.lang || "").toLowerCase() === w) return 20;
  const b = r.lblurb.indexOf(w);
  if (b === 0) return 12;
  if (b > 0) return /[a-z0-9]/.test(r.lblurb[b - 1]) ? 6 : 12;
  if ((r.listed_by || "").toLowerCase().includes(w)) return 2;
  return 0;
}

// Summed over the query's words, so two name hits beat one. The star bonus is logarithmic and deliberately
// small: it settles ties between rows that matched the same way, and log10 tops out near 5.5 even for a
// 300,000-star project, so it can never lift a blurb hit above a name hit. Linear stars would have made
// this a star sort wearing a relevance label.
function relevance(r, words) {
  let total = 0;
  for (const w of words) total += hitScore(r, w);
  return total + Math.log10((r.stars || 0) + 1);
}

const SORTS = {
  // `rel` is written onto the row once per render rather than computed inside the comparator, which would
  // score each row the O(log n) times the sort happens to compare it.
  relevance: (a, b) => b.rel - a.rel || b.stars - a.stars || a.name.localeCompare(b.name),
  stars: (a, b) => b.stars - a.stars || a.name.localeCompare(b.name),
  lists: (a, b) => b.lists - a.lists || b.stars - a.stars,
  pushed: (a, b) => (b.pushed || "").localeCompare(a.pushed || "") || b.stars - a.stars,
  name: (a, b) => a.name.localeCompare(b.name),
};

const SORT_KEYS = Object.keys(SORTS);

// Best match with an empty search box has nothing to rank, so it means Most stars until there is a query.
// Resolved here rather than by rewriting `state.sort`, so that clearing the box and typing again returns
// the reader to ranking instead of silently stranding them on a star sort they never chose.
function effSort() {
  return state.sort === "relevance" && !state.q ? "stars" : state.sort;
}

function render() {
  // Reflect state onto the chips. Cheaper than rebuilding them and it keeps focus where it was.
  const press = (id, on) => [...document.getElementById(id).children]
    .forEach((b, i) => b.setAttribute("aria-pressed", on(i) ? "true" : "false"));
  press("cats", i => i === 0 ? !state.cat : D.cats[i - 1].slug === state.cat);
  press("tgts", i => i === 0 ? !state.tgt : D.targets[i - 1].slug === state.tgt);
  press("oses", i => state.os.includes(i));
  document.getElementById("strict").setAttribute("aria-pressed", state.strict ? "true" : "false");
  document.getElementById("new").setAttribute("aria-pressed", state.fresh ? "true" : "false");

  const words = state.q.toLowerCase().split(/\s+/).filter(Boolean);
  let hits = ROWS.filter(match);

  // A single mistyped letter used to produce an empty page even when the answer was one letter away. The
  // fallback runs only after the exact pass has failed, so a search that works is never diluted by it.
  // Near matches keep their similarity order rather than the reader's chosen sort: this is a list of
  // corrections, and "closest first" is the only ordering that makes it one.
  let approx = false;
  if (!hits.length && words.length) {
    const alt = near(state.q);
    if (alt.length) { hits = alt; approx = true; }
  }
  if (!approx) {
    const sort = effSort();
    if (sort === "relevance") for (const r of hits) r.rel = relevance(r, words);
    hits.sort(SORTS[sort]);
  }

  const ranked = hits.filter(r => r.stars).length;
  document.getElementById("count").innerHTML = approx
    ? "<b>" + hits.length.toLocaleString() + "</b> near " +
      (hits.length === 1 ? "match" : "matches") + " · nothing matches “" + esc(state.q) + "” exactly"
    : "<b>" + hits.length.toLocaleString() + "</b> of " + ROWS.length.toLocaleString() +
      " · " + ranked.toLocaleString() + " with stars";

  const cat = state.cat && D.cats.find(c => c.slug === state.cat);
  const tgt = state.tgt && D.targets.find(t => t.slug === state.tgt);
  document.getElementById("ctx").textContent =
    cat && tgt ? cat.name + ", filtered to what plugs into " + tgt.name
    : cat ? cat.blurb : tgt ? tgt.blurb : "";

  const out = document.getElementById("out");
  if (!hits.length) {
    RESCUE = rescue();
    // No spelling suggestion here any more. `near()` above already offered every plausible correction as
    // real, clickable rows before this branch could be reached, so reaching it means the trigram pass also
    // came up empty -- and a "did you mean" that has nothing to name is worse than none. What is left is
    // genuinely a filter problem, which is what the rescue buttons address.
    out.innerHTML = '<div class="empty">' +
      '<p class="big">Nothing matches all of that.</p>' +
      (RESCUE.length
        ? "<p>" + (RESCUE.length === 1 ? "Loosening this would help:" : "Loosen one of these:") +
          '</p><div class="fixes">' + RESCUE.map((o, i) =>
            '<button class="fix" data-i="' + i + '">' + esc(o.label) +
            ' <span class="n">' + o.n.toLocaleString() + "</span></button>").join("") + "</div>"
        : "") +
      '<p style="margin-top:16px"><button class="fix" data-all="1">Clear all filters</button></p>' +
      "</div>";
    return;
  }
  const page = hits.slice(0, state.shown);
  const rows = page.map((r, i) => {
    // A U+2009 thin space, not a full one, between an OS label and its verdict glyph, so that the label
    // ignore-this-line "Win✓" break across lines
    // and its glyph read as one unit beside its four neighbours rather than as ten separate words. The
    // title carries the sentence, because a glyph narrows "amber" to "uncertain" without saying of what.
    const os = D.os.map((o, k) => {
      const v = VERDICT[r.os[k]] || ["", "not established"];
      return '<span class="v' + r.os[k] + '" title="' + esc(o + ": " + v[1]) + '">' +
        o.slice(0, 3) + " " + v[0] + "</span>";
    }).join(" ");
    const tags = '<span class="tag cat">' + esc(D.cats[r.cat].name) + "</span>" +
      r.targets.map(t => '<span class="tag">' + esc(D.targets[t].name) + "</span>").join("");
    // esc on the URLs too: these are other people's hand-typed table cells, and one stray quote in a
    // source list would otherwise close the attribute and let the rest of it be read as markup.
    const url = esc(r.url), img = esc(r.img);
    // A new row's title is the star, the name, and the day it arrived. The date is outside the anchor so
    // hovering the title does not underline it, and it is the fact that makes the mark self-explaining:
    // "New" alone leaves the reader wondering new to what, and how long ago.
    const star = r.isnew
      ? '<svg class="ni"><use class="a" href="#star-a"></use><use class="b" href="#star-b"></use></svg>'
      : "";
    const on = r.isnew ? ' <span class="newon">- New on ' + mmddyy(r.first_seen) + "</span>" : "";
    // The install line, with a button when the clipboard is reachable. The command is the one thing on a
    // row a reader wants to take away, and taking it meant selecting wrapped monospace text without
    // catching the blurb above it. The name is in the label because a screen-reader user arrives at
    // "Copy" 120 times a page and needs to know which project this one belongs to.
    const cmd = r.install
      ? '<div class="cmdrow"><code class="cmd">' + esc(r.install) + "</code>" +
        (CAN_COPY ? '<button class="copy" data-cmd="' + esc(r.install) +
          '" aria-label="Copy install command for ' + esc(r.name) + '">Copy</button>' : "") + "</div>"
      : "";
    return "<tr>" +
      '<td class="n rk">' + (i + 1) + "</td>" +
      // The screenshot is a second link to the same URL as the title next to it, so it was a duplicate
      // tab stop with no accessible name at all -- 120 unlabelled links per page, which is both a 2.4.4
      // failure and a keyboard reader pressing Tab twice for every row. aria-hidden plus tabindex="-1"
      // is the pattern for a redundant adjacent link: it stays clickable by mouse and disappears from the
      // accessibility tree, where the title already says everything it could have said.
      '<td class="shot"><a href="' + url + '" tabindex="-1" aria-hidden="true">' +
        '<img loading="lazy" alt="" src="' + img + '"></a></td>' +
      '<td class="pj"><a class="nm" href="' + url + '">' + star + esc(r.name) + "</a>" + on +
        '<span class="nwo">' + esc(r.nwo) + "</span>" +
        '<div class="meta os">' + os + "</div></td>" +
      '<td class="n st-c"><span class="st' + (r.stars ? "" : " none") + '">' +
        (r.stars ? r.stars.toLocaleString() : "—") + "</span>" +
        '<div class="meta">' + r.lists + (r.lists === 1 ? " list" : " lists") + "</div></td>" +
      '<td class="hide tg">' + tags + "</td>" +
      '<td class="ds"><div class="desc">' + esc(r.blurb) + "</div>" + cmd + "</td>" +
      // Each fact in its own span, not bare text between <br>s. The card layout lays this out as a flex
      // row, and flex builds an anonymous item per *contiguous run of text* -- so with the <br>s hidden
      // the three text nodes became one item and rendered as "ShellMIT 6d ago". Real elements are real
      // flex items, and they cost nothing in the table view.
      '<td class="c hide lc"><div class="meta"><span>' + esc(r.lang || "—") + "</span><br>" +
        "<span>" + esc(r.license || "—") + "</span><br><span>" + since(r.pushed) +
        "</span></div></td>" +
      "</tr>";
  }).join("");
  // Every th carries the same class as the td beneath it. The Shot heading used not to, and since the
  // narrow-viewport rule hides `.shot` it hid only the body cell -- leaving five headings over four
  // columns, so "Shot" sat above the project names, "Project" above the stars, "Stars" above the
  // blurbs, and auto layout invented a fifth column to hang the surplus heading on.
  // Said above the table as well as in the live region, because a sighted reader who mistyped needs to
  // know *why* they are looking at LangGraph when they asked for "langraph" -- otherwise the correction
  // looks like the search quietly ignoring them.
  const note = approx
    ? '<p class="approx">Nothing matches <b>' + esc(state.q) + "</b> exactly. Closest by name" +
      (state.cat || state.tgt || state.os.length || state.strict || state.fresh
        ? ", within your other filters" : "") + ":</p>"
    : "";
  out.innerHTML = note +
    "<table><thead><tr><th class='n'>#</th><th class='shot'>Shot</th><th class='pj'>Project</th>" +
    "<th class='n st-c'>Stars</th>" +
    "<th class='hide tg'>Topic &amp; targets</th><th class='ds'>What it does</th>" +
    "<th class='c hide lc'>Lang / licence / push</th></tr></thead><tbody>" + rows +
    "</tbody></table>";
  if (hits.length > page.length) {
    const b = document.createElement("button");
    b.className = "more";
    b.textContent = "Show " + Math.min(PAGE_SIZE * 4, hits.length - page.length).toLocaleString() +
      " more of " + hits.length.toLocaleString();
    b.onclick = () => {
      const first = state.shown;
      state.shown += PAGE_SIZE * 4;
      render();
      // render() replaced the whole subtree, so the button that was just clicked no longer exists and
      // focus fell to <body> -- which returns a keyboard reader to the top of the document, above six
      // rows of filters, every time they ask for more. Put it on the first newly revealed row instead,
      // which is where a mouse reader is already looking. preventScroll so the viewport does not jump
      // for anyone: the new rows appear below the fold, exactly where the button was.
      const rows = document.querySelectorAll("#out tbody tr");
      const t = rows[first] || document.querySelector("#out .more");
      if (t) { t.tabIndex = -1; t.focus({preventScroll: true}); }
      say(Math.min(state.shown, hits.length).toLocaleString() + " of " +
          hits.length.toLocaleString() + " shown.");
    };
    out.appendChild(b);
  }
}

function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"]/g,
    c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
}
</script>
__ANALYTICS__</body>
</html>
"""


def main() -> None:
    records = b16.prepare(
        json.loads((CACHE / "records_all.json").read_text(encoding="utf-8")), None)
    meta = json.loads((CACHE / "meta.json").read_text(encoding="utf-8"))
    orch = json.loads((CACHE / "records.json").read_text(encoding="utf-8"))
    # Optional, unlike everything above: no shot map means every row shows its Open Graph card, which is
    # what the daily job relies on to skip the capture stage entirely. See `b17.cached`.
    shots = b16.merged_shots(b17.cached("shots_all.json"), b17.cached("shots.json"))

    for r in orch:
        r.setdefault("section", r["category"])
        r.setdefault("bucket", r["category"])
        r.setdefault("blurb", r.get("description") or "")
        r.setdefault("src_order", r.get("order", 0))
        r["shot_key"] = (r.get("nwo") or "").replace("/", "__")
        if r.get("license") in ("NOASSERTION", "NONE", DASH, "", None):
            r["license"] = ""
    b16.canonicalise_nwo(records, orch, meta)

    label = {"orchestrators": "Orchestrators", **{k: t for k, t, *_ in b16.SHEETS}}
    tax.STARS.clear()
    tax.STARS.update(b16.star_map(records, orch, meta))
    agg = tax.by_repo(records + [dict(x, source="orchestrators") for x in orch])
    facets = b16.repo_pool(records, orch, label)
    for r in facets:
        a = agg[r["nwo"]]
        r["category"], r["targets"] = a["category"], a["targets"]
        r["stars"] = tax.STARS.get(r["nwo"], 0)

    # Before build_data, which reads the map it fills. Idempotent, so 17_markdown having already run in
    # this pipeline is fine -- it stamped the same repos with the same date and this call agrees.
    fresh = newness.resolve([r["nwo"] for r in facets])

    data = build_data(facets, shots)
    OUT.mkdir(exist_ok=True)
    (OUT / "data.json").write_text(
        json.dumps(data, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
    # Pages runs Jekyll by default, which would try to interpret this directory as a site and skip
    # anything it decided looked like a draft. There is no Jekyll here.
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    page = substitute(PAGE, data, REPO, b17.SITE)
    (OUT / "index.html").write_text(page, encoding="utf-8")

    for f in ("index.html", "data.json"):
        print(f"{f:12s} {(OUT / f).stat().st_size / 1024:8.1f} KB")
    print(f"{len(data['rows']):,} repos · {len(data['cats'])} topics · "
          f"{len(data['targets'])} targets · {sum(r[4] for r in data['rows']):,} stars")
    live = sum(1 for d in fresh.values() if newness.within(d))
    print(f"{len(fresh):,} arrived since {data['baseline']} · {live:,} inside the "
          f"{newness.WINDOW}-day window")


if __name__ == "__main__":
    main()
