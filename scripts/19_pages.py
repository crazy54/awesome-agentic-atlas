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
cached separately from the nearly 8,000 rows that change on every rebuild. And every filter is mirrored
into the URL hash, which is what makes "the best Claude Code observability tool" a link -- the thing the
Markdown pages can only approximate by existing in two directories.
"""
import importlib.util
import json
import os
import re
import sys
from datetime import date
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

# How many curated lists the atlas is built from, read off the parser's own table rather than written
# down here. The page states it four times -- the heading, both social descriptions and the footer --
# and all four said "eleven" for a while after the atlas had stopped being eleven lists. `SOURCES` is
# the same authority `16_build_all.LIST_TITLE` and `watch_sources.py` read, so the site cannot
# disagree with the workbook about how many lists were merged.
LISTS = len(b16.b10.SOURCES)

# Verdicts compress to one character each because there are only five of them and every row prints all
# five -- some forty thousand characters across the dataset. The page expands them back for display;
# the JSON is what travels over the wire.
VERDICT = {"Yes": "Y", "Likely": "L", "No": "N", "n/a": "a", DASH: "-", "": "-"}
OS_FIELDS = ["win_native", "win_wsl2", "macos", "linux", "docker"]
OS_LABELS = ["Windows", "WSL2", "macOS", "Linux", "Docker"]

# The columns of `data.json`, in order. Column-oriented rather than one object per repo: the keys would
# otherwise be repeated once per row across nearly 8,000 of them, which is megabytes of the word
# "category". The page maps them back into objects once, on load.
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
        # thirds of these rows, so spelling it out would be 55 bytes a row, across nearly 8,000 rows,
        # of a string the page can rebuild from `nwo`.
        "" if img == og(r["nwo"]) else img,
        # The raw arrival date, not a new/old flag, and for every arrival rather than only the recent
        # ones -- the page needs the date to print it and to expire the mark itself, and once it has to
        # travel anyway there is no reason to throw the older ones away.
        newness.SEEN.get(r["nwo"], ""),
    ]


def build_data(facets, shots) -> dict:
    cats = list(tax.CATEGORIES)
    tgts = [t for t, _p in tax.TARGETS]
    cat_ix = {c: i for i, c in enumerate(cats)}
    tgt_ix = {t: i for i, t in enumerate(tgts)}
    rows = sorted(facets, key=lambda r: (-(r["stars"] or 0), r["name"].lower()))
    return {
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


def substitute(page: str, data: dict, repo: str, site: str) -> str:
    """Fill the template's placeholders. Both this stage and `19b_refresh.py` render the same shell, and
    when the two chains drifted the refreshed page quietly lost whichever one had been added since."""
    return (page
            .replace("__COUNT__", f"{len(data['rows']):,}")
            .replace("__TOPICS__", str(len(data["cats"])))
            .replace("__LISTS__", str(LISTS))
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
<meta name="description" content="__COUNT__ agentic AI projects from __LISTS__ awesome-lists, merged, deduplicated and filterable by topic, harness and operating system.">
<meta property="og:title" content="Awesome Agentic Atlas">
<meta property="og:description" content="__COUNT__ projects from __LISTS__ awesome-lists, one filterable index.">
<meta property="og:image" content="https://opengraph.githubassets.com/1/__REPO__">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><text y='13' font-size='14'>&#127760;</text></svg>">
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
header{background:var(--plane);border-bottom:1px solid var(--grid);padding:22px 20px 16px}
.wrap{max-width:1500px;margin:0 auto}
h1{margin:0 0 4px;font-size:26px;letter-spacing:-.02em}
h1 span{color:var(--muted);font-weight:400;font-size:15px;letter-spacing:0}
.sub{color:var(--ink2);font-size:14px;margin:0}
.sub b{color:var(--ink)}
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
.tag{display:inline-block;background:var(--band);border:1px solid var(--grid);border-radius:5px;
  padding:2px 7px;font-size:11.5px;color:var(--ink2);margin:0 4px 4px 0;white-space:nowrap}
.tag.cat{border-color:var(--bar);color:var(--ink)}
.os{font-size:11.5px;letter-spacing:.02em;white-space:nowrap}
/* Prefixed because the verdict characters are the class names and one of them is "-", which is not a
   valid CSS identifier on its own -- ".-" invalidates the whole selector list it appears in, so the
   unprefixed version silently dropped the colour from every No, n/a and dash on the page. */
.vY{color:var(--good);font-weight:700}
.vL{color:var(--warn)}
.vN,.va,.v-{color:var(--off)}
.empty{padding:80px 0;text-align:center;color:var(--muted)}
.more{display:block;margin:26px auto 0;background:var(--band);color:var(--ink);
  border:1px solid var(--grid);border-radius:8px;padding:11px 22px;font-weight:600}
.more:hover{border-color:var(--bar)}
footer{border-top:1px solid var(--grid);background:var(--plane);padding:22px 20px;
  color:var(--muted);font-size:13px}
.blurb{color:var(--muted);font-size:13px;margin:2px 0 0}
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
  .st{font-size:15px}
  .desc{font-size:13px}
  .more{width:100%}
}
</style>
</head>
<body>
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
    <h1>Awesome Agentic Atlas <span>· __LISTS__ awesome-lists, merged</span></h1>
    <p class="sub"><b>__COUNT__</b> projects · <b>__TOPICS__</b> topics · <b>__STARS__</b> combined
      stars · snapshot __SNAPSHOT__</p>
    <p class="blurb" id="ctx"></p>
  </div>
  <nav>
    <a href="https://github.com/__REPO__">Repository</a> ·
    <a href="https://github.com/__REPO__/tree/main/mega-list">Markdown edition</a> ·
    <a href="https://github.com/__REPO__/releases/latest">Workbook</a><br>
    <button class="chip" id="theme" aria-pressed="false">Light theme</button>
  </nav>
</div></div></header>

<div class="bar"><div class="wrap">
  <div class="line">
    <label for="q">Search</label>
    <input id="q" type="search" placeholder="name, repo, description, language&hellip;"
           autocomplete="off" spellcheck="false">
    <select id="sort" aria-label="Sort by">
      <option value="stars">Most stars</option>
      <option value="lists">Named by most lists</option>
      <option value="pushed">Pushed most recently</option>
      <option value="name">Name (A&ndash;Z)</option>
    </select>
    <button class="chip newchip" id="new" aria-pressed="false"
            title="Projects the source lists added in the last __WINDOW__ days">
      <svg class="ni"><use class="a" href="#star-a"></use><use class="b" href="#star-b"></use></svg>
      <span id="newlabel">New</span></button>
    <span class="count" id="count"></span>
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
  Every entry came from someone else's curation work; all __LISTS__ source lists are credited in the
  <a href="https://github.com/__REPO__#the-source-lists">repository</a>. Stars, language, licence and
  last-push come from the GitHub API on __SNAPSHOT__ and drift daily. Platform verdicts are derived
  from each project's own README, install route, CI config and release assets &mdash;
  <span class="vY">green</span> is stated evidence, <span class="vL">amber</span> is inferred from the
  language. A dash in the star column means the row is a folder inside someone else's repo, or a dead
  link, and has no count of its own.
</div></footer>

<script>
const PAGE_SIZE = 120;
const state = {q: "", cat: "", tgt: "", os: [], strict: false, fresh: false,
               sort: "stars", shown: PAGE_SIZE};
let D = null, ROWS = [], NEW = 0;

// The window is applied here, in the browser, against the reader's own clock -- `data.json` carries the
// raw first-seen date and nothing else. That is what makes the mark expire without a rebuild: a repo
// stamped the 14th stops being new on the 29th in every open tab, on a day the cron may not have run.
// Both sides of the subtraction are ISO dates, which Date.parse reads as UTC midnight, so the result is
// a whole number of days and never 13.958 because of a timezone.
const TODAY = new Date().toISOString().slice(0, 10);
const daysAgo = iso => Math.round((Date.parse(TODAY) - Date.parse(iso)) / 86400000);
const mmddyy = iso => iso.slice(5, 7) + "/" + iso.slice(8, 10) + "/" + iso.slice(2, 4);

fetch("data.json").then(r => r.json()).then(d => {
  D = d;
  // Column-oriented on the wire, objects in here. One pass over every row, so the rest of the page can
  // read `r.stars` instead of `r[4]`.
  ROWS = d.rows.map(a => Object.fromEntries(d.cols.map((c, i) => [c, a[i]])));
  ROWS.forEach(r => {
    r.hay = (r.name + " " + r.nwo + " " + r.blurb + " " + r.lang + " " + r.listed_by).toLowerCase();
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
  document.getElementById("q").oninput = e => set({q: e.target.value}, true);
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
  document.getElementById("reset").onclick =
    () => set({q: "", cat: "", tgt: "", os: [], strict: false, fresh: false});
  document.getElementById("theme").onclick = e => {
    const light = document.documentElement.dataset.theme !== "light";
    document.documentElement.dataset.theme = light ? "light" : "dark";
    e.target.textContent = light ? "Dark theme" : "Light theme";
    e.target.setAttribute("aria-pressed", light ? "true" : "false");
  };
  window.addEventListener("hashchange", () => { readHash(); render(); });
}

function set(patch, keepFocus) {
  Object.assign(state, patch, {shown: PAGE_SIZE});
  writeHash();
  render();
  if (!keepFocus) document.getElementById("q").blur();
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
  if (state.sort !== "stars") p.set("sort", state.sort);
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
  state.sort = ["stars", "lists", "pushed", "name"].includes(p.get("sort")) ? p.get("sort") : "stars";
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

const SORTS = {
  stars: (a, b) => b.stars - a.stars || a.name.localeCompare(b.name),
  lists: (a, b) => b.lists - a.lists || b.stars - a.stars,
  pushed: (a, b) => (b.pushed || "").localeCompare(a.pushed || "") || b.stars - a.stars,
  name: (a, b) => a.name.localeCompare(b.name),
};

function render() {
  // Reflect state onto the chips. Cheaper than rebuilding them and it keeps focus where it was.
  const press = (id, on) => [...document.getElementById(id).children]
    .forEach((b, i) => b.setAttribute("aria-pressed", on(i) ? "true" : "false"));
  press("cats", i => i === 0 ? !state.cat : D.cats[i - 1].slug === state.cat);
  press("tgts", i => i === 0 ? !state.tgt : D.targets[i - 1].slug === state.tgt);
  press("oses", i => state.os.includes(i));
  document.getElementById("strict").setAttribute("aria-pressed", state.strict ? "true" : "false");
  document.getElementById("new").setAttribute("aria-pressed", state.fresh ? "true" : "false");

  const hits = ROWS.filter(match).sort(SORTS[state.sort]);
  const ranked = hits.filter(r => r.stars).length;
  document.getElementById("count").innerHTML =
    "<b>" + hits.length.toLocaleString() + "</b> of " + ROWS.length.toLocaleString() +
    " · " + ranked.toLocaleString() + " with stars";

  const cat = state.cat && D.cats.find(c => c.slug === state.cat);
  const tgt = state.tgt && D.targets.find(t => t.slug === state.tgt);
  document.getElementById("ctx").textContent =
    cat && tgt ? cat.name + ", filtered to what plugs into " + tgt.name
    : cat ? cat.blurb : tgt ? tgt.blurb : "";

  const out = document.getElementById("out");
  if (!hits.length) {
    out.innerHTML = '<p class="empty">Nothing matches. Try clearing a filter.</p>';
    return;
  }
  const page = hits.slice(0, state.shown);
  const rows = page.map((r, i) => {
    const os = D.os.map((o, k) => '<span class="v' + r.os[k] + '">' + o.slice(0, 3) + "</span>")
      .join(" ");
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
    return "<tr>" +
      '<td class="n rk">' + (i + 1) + "</td>" +
      '<td class="shot"><a href="' + url + '"><img loading="lazy" alt="" src="' + img +
        '"></a></td>' +
      '<td class="pj"><a class="nm" href="' + url + '">' + star + esc(r.name) + "</a>" + on +
        '<span class="nwo">' + esc(r.nwo) + "</span>" +
        '<div class="meta">' + os + "</div></td>" +
      '<td class="n st-c"><span class="st' + (r.stars ? "" : " none") + '">' +
        (r.stars ? r.stars.toLocaleString() : "—") + "</span>" +
        '<div class="meta">' + r.lists + (r.lists === 1 ? " list" : " lists") + "</div></td>" +
      '<td class="hide">' + tags + "</td>" +
      '<td class="ds"><div class="desc">' + esc(r.blurb) + "</div>" +
        (r.install ? '<code class="cmd">' + esc(r.install) + "</code>" : "") + "</td>" +
      '<td class="c hide"><div class="meta">' + esc(r.lang || "—") + "<br>" +
        esc(r.license || "—") + "<br>" + esc(r.pushed || "—") + "</div></td>" +
      "</tr>";
  }).join("");
  // Every th carries the same class as the td beneath it. The Shot heading used not to, and since the
  // narrow-viewport rule hides `.shot` it hid only the body cell -- leaving five headings over four
  // columns, so "Shot" sat above the project names, "Project" above the stars, "Stars" above the
  // blurbs, and auto layout invented a fifth column to hang the surplus heading on.
  out.innerHTML =
    "<table><thead><tr><th class='n'>#</th><th class='shot'>Shot</th><th class='pj'>Project</th>" +
    "<th class='n st-c'>Stars</th>" +
    "<th class='hide'>Topic &amp; targets</th><th class='ds'>What it does</th>" +
    "<th class='c hide'>Lang / licence / push</th></tr></thead><tbody>" + rows +
    "</tbody></table>";
  if (hits.length > page.length) {
    const b = document.createElement("button");
    b.className = "more";
    b.textContent = "Show " + Math.min(PAGE_SIZE * 4, hits.length - page.length).toLocaleString() +
      " more of " + hits.length.toLocaleString();
    b.onclick = () => { state.shown += PAGE_SIZE * 4; render(); };
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

    # b16.LIST_TITLE, not a second map built from SHEETS: this is the same defect the workbook and the
    # Markdown edition each carried, and the site was the last surface still holding it. SHEETS is the
    # ten lists with a sheet of their own; `listed_by` here describes rows drawn from all thirty-nine,
    # so 27 of them printed their raw internal key -- 8,158 cells across 89% of rows, reading
    # "agentsec_recon, aiagents_jenqyang" where a neighbour read "Claude Code". No visible column shows
    # it, which is why it survived, but `row_for` folds it into the client-side search haystack: a
    # reader searching "Gemini CLI Ecosystem" matched nothing while "mcp_punkpeye" matched 3,457 rows.
    # LIST_TITLE already layers SHEET_TITLE over the SOURCES titles and already carries the
    # orchestrators override, so every name this used to produce is unchanged.
    label = b16.LIST_TITLE
    tax.STARS.clear()
    tax.STARS.update(b16.star_map(records, orch, meta))
    agg = tax.by_repo(records + [dict(x, source="orchestrators") for x in orch])
    facets = b16.repo_pool(records, orch, label)
    for r in facets:
        a = agg[r["nwo"]]
        r["category"], r["targets"] = a["category"], a["targets"]
        r["stars"] = tax.STARS.get(r["nwo"], 0)

    # Before build_data, which reads the map it fills. Idempotent, so 17_markdown having already run in
    # this pipeline is fine -- it stamped the same repos with the same date and this call agrees. Passing
    # `sources` is part of agreeing: whichever stage stamps a repo first decides its date, so a call that
    # omitted it would date the same repos differently depending on which stage got there first.
    fresh = newness.resolve([r["nwo"] for r in facets],
                            sources=[s["nwo"] for s in b16.b10.SOURCES])

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
