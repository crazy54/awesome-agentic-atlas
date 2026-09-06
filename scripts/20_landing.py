"""Prerender the topic and target views as real pages, because the hash is invisible to crawlers.

`19_pages.py` puts every filter in the URL hash, which is what makes "the best Claude Code
observability tool" a link a human can send. A crawler is not a human: the fragment is never sent to
the server and never survives into the index, so Google sees one page called "browse every agentic
tool" and 1,294 rows it never receives -- the site's whole reason for existing is unindexable. The
Markdown edition under `mega-list/` is indexable and picks one axis at a time, which is the other half
of the same gap: it cannot cross them.

This stage writes the crossing out as static HTML. Same data, same ordering, same verdicts as the
other three surfaces, and no data fetch on load -- the rows are in the initial response, which is the
only form a crawler counts.

  docs/topic/<topic>/index.html                    14, one per topic
  docs/target/<target>/index.html                  12, one per target
  docs/topic/<topic>/target/<target>/index.html    130, one per crossing that has rows
  docs/pages.css                                   the shared shell
  docs/sitemap.xml                                 every page above, plus the root
  docs/robots.txt                                  allow everything, point at the sitemap
  docs/<indexnow-key>.txt                          the IndexNow credential `26_indexnow.py` posts against

  python scripts/20_landing.py

Five decisions worth stating.

It reads `docs/data.json`, and a listing of `docs/og/` to see which Open Graph cards exist.
`19_pages.py` needs the 64 MB build cache and this does not, for the same reason `19b_refresh.py`
does not: the crossing is a pure function of the committed dataset, so a clone with nothing fetched
can rebuild all 156 pages. It follows that this stage can never invent a star count or a verdict that
the site disagrees with, because it has none of its own. The card listing does not weaken that -- the
cards are committed too, and their absence only ever costs a page the better of two `og:image`s.

Only the topic-first nesting exists. `target/<t>/topic/<c>/` would be the same 130 pages at 130 second
URLs, which is duplicate content that splits its own ranking signal; every page carries a
`rel=canonical` to say which URL it is, and one nesting means that claim is never a lie.

Empty crossings are not written. 14 x 12 is 168 and only 130 of them have a row, so 38 would be pages
whose whole content is "nothing matches" -- thin pages that earn nothing and dilute the 130 that do.

The stylesheet is a file rather than 156 inlined copies. The shell is ~4 KB; inlining it would add
~620 KB to the repo to save one cached request.

The sitemap is written here rather than in a stage of its own, on the same argument as `substitute()`
being shared between `19_pages.py` and `19b_refresh.py`: a sitemap is a list of the files somebody
else wrote, and when the writer and the lister were two passes over two derivations of "which pages
exist" they drifted. Here the list is the loop's own output, so it cannot claim a page that is not
there or miss one that is.
"""
from __future__ import annotations

import html
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUT = ROOT / "docs"

# The same dynamic load `19b_refresh.py` uses, and for the same reason: the module is named `19_pages`,
# which is not an identifier, so `import` cannot reach it. Two things are wanted from it -- `beacon()`,
# so the analytics token lives in exactly one file, and `b17.SITE`, so the absolute URL that goes in
# every canonical and every sitemap entry is the one string the Markdown edition already links to.
spec = importlib.util.spec_from_file_location("b19", HERE / "19_pages.py")
b19 = importlib.util.module_from_spec(spec)
sys.modules["b19"] = b19
spec.loader.exec_module(b19)

SITE = b19.b17.SITE
REPO = b19.REPO

# And `22_detail.py`, for one function: `segment()`, the rule that turns an `nwo` into a path. These
# pages link to the detail pages that stage writes, so the two files have to agree on the URL of every
# one of them, and a slug rule spelled twice is a slug rule that will differ once. Imported rather than
# copied even though it is two lines, because the two lines encode a decision -- a leading dot becomes
# `dot-`, so `zircote/.claude` does not land in a directory the whole toolchain treats as hidden -- and
# a copy would not carry the reason. Safe to import: the module does its work under `if __name__`, so
# loading it here runs no build.
dspec = importlib.util.spec_from_file_location("b22", HERE / "22_detail.py")
b22 = importlib.util.module_from_spec(dspec)
sys.modules["b22"] = b22
dspec.loader.exec_module(b22)

# Where `23_og.py` puts the cards, relative to `docs/`. Named here rather than spelled twice, because
# the two stages have to agree on it and there is no import between them that could carry it.
OG = "og"

# The cap. A crawler stops reading a document long before the 479th row, and the rows past the first
# hundred on the two big target pages are the ones with no stars to rank by -- so the page that gets
# indexed is the page that is worth indexing, and the rest are one click away in the view that can
# actually page through them.
CAP = 100


# ------------------------------------------------------------------ escaping
def esc(text) -> str:
    """Every interpolated value goes through this.

    These strings are other people's hand-written list entries -- 1,294 names, blurbs and install
    commands typed into eleven different READMEs. One stray `<` becomes a tag and one stray `"` closes
    the attribute it is sitting in and lets the rest of the row be read as markup. The template in
    `19_pages.py` does this in JavaScript with its own `esc()`; this is the same guarantee on the
    server side, with `quote=True` because roughly half of these land in attributes.
    """
    return html.escape("" if text is None else str(text), quote=True)


def clip(text: str, limit: int) -> str:
    """Shorten on a word boundary. For `<meta name=description>`, which Google truncates at ~160."""
    if len(text) <= limit:
        return text
    return text[: limit - 1].rsplit(" ", 1)[0].rstrip(" ,;:.—-") + "…"


def repo_path(nwo: str) -> str:
    """Where `22_detail.py` puts one project's page, relative to `docs/`. Trailing slash.

    Constructed rather than looked up on disk, and that is deliberate: both stages derive their page set
    from the same `data.json` -- that one emits a page per row unconditionally and raises if two rows
    ever slug alike -- so a row on a landing page always has a detail page, and a disk check would only
    add a way to be wrong. It would also be wrong in one specific way: `weekly.yml` runs this stage
    *before* `22_detail.py`, so a project added this week has no page on disk at the moment this runs and
    would be handed a fallback link that then outlived the commit by a week.
    """
    owner, name = nwo.split("/", 1)
    return f"repo/{b22.segment(owner.lower())}/{b22.segment(name.lower())}/"


# ------------------------------------------------------------------ the shared shell
# Copied from `19_pages.py`'s template rather than imported out of it, because that template is one
# 25 KB string with the whole interactive page in it and there is no seam to import. What is copied is
# the part that has to match: the two custom-property blocks, verbatim, so a landing page and the site
# are the same eight neutrals and two accents. Everything after them is the subset of the layout these
# pages use -- no filter bar, no chips, no sticky header, because there is nothing here to filter.
CSS = """/* Written by scripts/20_landing.py. Shared by every page under docs/topic/ and docs/target/.

   The two blocks below are `19_pages.py`'s, character for character. Lagoon Gold: cyan primary, gold
   secondary, cool near-black surfaces. Dark is the designed mode -- its eight neutrals and two accents
   are the theme's own values. Light is stepped from the same two hues rather than flipped, because the
   accents at their dark-mode lightness fail on white (the cyan measures 2.53:1 there), and its
   neutrals are cooled to match so toggling does not change brand. --onbar exists because a filled cyan
   or gold accent carries DARK ink, not white: white on #08b0cc is 2.3:1, while the theme's own #0c1013
   on it is 7.36:1. */
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
h1{margin:0 0 6px;font-size:26px;letter-spacing:-.02em}
h2{margin:34px 0 8px;font-size:16px;letter-spacing:-.01em}
.sub{color:var(--ink2);font-size:14px;margin:0}
.sub b{color:var(--ink)}
.top{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap}
.top nav{font-size:13px;color:var(--muted);text-align:right;line-height:1.9}
.blurb{color:var(--muted);font-size:13px;margin:6px 0 0;max-width:70ch}
button{font:inherit;cursor:pointer}
.chip{display:inline-block;background:var(--band);color:var(--ink2);border:1px solid var(--grid);
  border-radius:999px;padding:5px 12px;font-size:13px;white-space:nowrap;margin:0 5px 5px 0}
.chip:hover{border-color:var(--bar);color:var(--ink);text-decoration:none}
/* The row count inside a navigation chip. Dimmed rather than smaller, so the chips stay one height. */
.ct{opacity:.65}
/* The one link on the page that has to be found, because it is the thing the page is a preview of:
   this is a snapshot of one crossing, and that is the live version of it with both axes still live.
   Filled with the accent, which is why it needs --onbar for its ink. */
.cta{display:inline-block;background:var(--bar);color:var(--onbar);font-weight:600;
  border-radius:8px;padding:9px 16px;margin:14px 0 0}
.cta:hover{text-decoration:none;filter:brightness(1.08)}
main{padding:0 20px 64px}
table{width:100%;border-collapse:collapse;margin-top:14px}
th{text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);
  padding:8px 10px;border-bottom:1px solid var(--grid);background:var(--surface)}
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
   Safari, so a repo name and a blurb naming six agents between them demand more than the content box
   has -- which the document then has to scroll sideways to satisfy. */
.nm{font-weight:600;font-size:15px;overflow-wrap:anywhere}
.nwo{display:block;color:var(--muted);font-size:12px;margin-top:2px;word-break:break-all}
/* The `nwo` is a link out to GitHub and the name above it is a link into this site, so the two need to
   be told apart without colour doing it -- muted is the right weight for the secondary line and the
   link colour would make it shout. Hover promotes it to full ink, which with the underline `a:hover`
   already adds is enough to say "this is a link" at the moment somebody asks. */
a.nwo:hover{color:var(--ink)}
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
.rest{margin:22px 0 0;color:var(--ink2);font-size:13.5px}
.rel{margin-top:34px;border-top:1px solid var(--grid);padding-top:18px}
.rel h2{margin-top:0}
.rel p{margin:0 0 12px;color:var(--muted);font-size:13px}
footer{border-top:1px solid var(--grid);background:var(--plane);padding:22px 20px;
  color:var(--muted);font-size:13px}
footer .wrap{max-width:1500px}
/* Two queries, because the page fails in two places: at 900px the screenshot and the two detail
   columns stop paying for their width, and below 640px four columns stop fitting in what is left. */
@media(max-width:900px){
  .shot,.hide{display:none}
  td,th{padding:9px 6px}
}
@media(max-width:640px){
  header{padding:16px 14px 12px}
  main{padding:0 14px 48px}
  footer{padding:18px 14px}
  h1{font-size:21px}
  .top nav{text-align:left;line-height:2.1}
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
  .cta{display:block;text-align:center}
}
"""

# Not a data fetch and not a framework: the light half of the theme is copied in above, and without a
# switch nothing on these pages can ever reach it. Same default as the site (dark) and the same
# unpersisted, one-tab scope, so the two surfaces behave alike. Inlined rather than a second file
# because it is 250 bytes and a request costs more than that.
THEME_JS = """<script>
document.getElementById("theme").onclick = e => {
  const light = document.documentElement.dataset.theme !== "light";
  document.documentElement.dataset.theme = light ? "light" : "dark";
  e.target.textContent = light ? "Dark theme" : "Light theme";
  e.target.setAttribute("aria-pressed", light ? "true" : "false");
};
</script>
"""

# Copied from the template so a landing page in a bookmark bar looks like the site.
ICON = ("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'>"
        "<text y='13' font-size='14'>&#127760;</text></svg>")


# ------------------------------------------------------------------ the page set
class Page:
    """One output file, and everything needed to write it.

    Built before anything is rendered, because three consumers need the same list and they must agree:
    the renderer, the sitemap, and the prune pass that deletes whatever this run did not produce.
    """

    def __init__(self, parts: list[str], cat: dict | None, tgt: dict | None, rows: list[dict]):
        self.parts = parts                      # URL path segments, no filename
        self.cat, self.tgt, self.rows = cat, tgt, rows
        self.depth = len(parts)                 # how many `../` reach docs/ from here
        self.path = OUT.joinpath(*parts, "index.html")
        self.url = SITE + "/".join(parts) + "/"

    def rel(self, tail: str = "") -> str:
        """A link out of this page, relative. Relative rather than absolute so the whole tree can be
        served from a `python -m http.server` in `docs/` and from the Pages subpath unchanged."""
        return "../" * self.depth + tail

    def repo(self, nwo: str) -> str:
        """The `22_detail.py` page for one row, from here."""
        return self.rel(repo_path(nwo))

    @property
    def live(self) -> str:
        """The same view on the site, both filters already applied -- the page's reason to exist.

        Returned unescaped, and every interpolation of it goes through `esc()`: a two-filter hash is
        `#topic=x&target=y`, and a bare `&` in an `href` is an unterminated character reference that a
        validator rejects and a strict parser is entitled to mangle.
        """
        q = "&".join(f"{k}={v}" for k, v in (("topic", self.cat and self.cat["slug"]),
                                             ("target", self.tgt and self.tgt["slug"])) if v)
        return self.rel() + (f"#{q}" if q else "")

    @property
    def heading(self) -> str:
        if self.cat and self.tgt:
            return f"{self.cat['name']} tools for {self.tgt['name']}"
        return self.cat["name"] if self.cat else f"Tools for {self.tgt['name']}"

    @property
    def title(self) -> str:
        """Unique per page, front-loaded with the words someone would actually type. The suffix is the
        site name, last, because a 60-character result snippet should spend its width on the topic."""
        if self.cat and self.tgt:
            return f"{self.heading} — Awesome Agentic Atlas"
        n = f"{len(self.rows):,}"
        if self.cat:
            return f"{self.cat['name']}: {n} agentic AI tools — Awesome Agentic Atlas"
        return f"Tools for {self.tgt['name']}: {n} projects — Awesome Agentic Atlas"

    @property
    def card(self) -> str:
        """The filename of this view's Open Graph card, under `docs/og/`.

        A crossing takes its topic's card rather than one of its own: 26 images instead of 156. The
        card carries the facet's name, its project count and its three most starred projects, and it
        says "every harness" out loud so that a topic card beside a crossing page's own title and
        description cannot be read as a claim about that one cell. `23_og.py` argues the cost.
        """
        return f"topic-{self.cat['slug']}.png" if self.cat else f"target-{self.tgt['slug']}.png"

    @property
    def card_label(self) -> str:
        """What that card has printed across it, which on a crossing is not this page's heading.

        `heading` would give "Coding Agents tools for Claude Code" for a card that says "Coding
        Agents" and nothing about Claude Code -- and `og:image:alt` is read out to somebody who cannot
        see the image, so it is the one string here that must describe the picture rather than the
        page. Identical to `heading` on the 26 pages that have a card of their own.
        """
        return self.cat["name"] if self.cat else f"Tools for {self.tgt['name']}"

    @property
    def summary(self) -> str:
        """`<meta name=description>`. The count first because it is the fact that distinguishes this
        page from the other 155, then the taxonomy's own blurb, which is already written prose."""
        n = f"{len(self.rows):,}"
        if self.cat and self.tgt:
            lead = f"{n} {self.cat['name']} projects that plug into {self.tgt['name']}"
        elif self.cat:
            lead = f"{n} {self.cat['name']} projects"
        else:
            lead = f"{n} agentic AI projects that plug into {self.tgt['name']}"
        blurb = (self.cat or self.tgt)["blurb"]
        return clip(f"{lead}, ranked by GitHub stars. {blurb}".strip(), 158)


def plan(data: dict) -> list[Page]:
    """Group the dataset three ways. One pass over 1,294 rows, three indexes out of it."""
    cats, tgts = data["cats"], data["targets"]
    # Column-oriented on disk, objects in here -- the same one pass the page's own JavaScript makes, so
    # everything downstream can read `r["stars"]` instead of `r[4]`. The two facet columns are indexes
    # into `cats` and `targets`; resolved to names here, once per row rather than once per row per page,
    # because a project in five targets appears on seven of these pages and the answer does not change.
    rows = [dict(zip(data["cols"], r)) for r in data["rows"]]
    for r in rows:
        r["cat_name"] = cats[r["cat"]]["name"]
        r["target_names"] = [tgts[t]["name"] for t in r["targets"]]

    by_cat: dict[int, list[dict]] = {i: [] for i in range(len(cats))}
    by_tgt: dict[int, list[dict]] = {i: [] for i in range(len(tgts))}
    by_both: dict[tuple[int, int], list[dict]] = {}
    for r in rows:
        by_cat[r["cat"]].append(r)
        for t in r["targets"]:
            by_tgt[t].append(r)
            by_both.setdefault((r["cat"], t), []).append(r)

    # Stars descending, name as the tie-break -- `SORTS.stars` in the template, and the same order the
    # Markdown facet pages and the workbook use. Sorted here rather than trusted from `data.json`,
    # which happens to arrive in this order today: a landing page that silently reordered itself
    # because an upstream stage changed its own sort would be a hard bug to see.
    def rank(group):
        return sorted(group, key=lambda r: (-(r["stars"] or 0), r["name"].lower()))

    pages = [Page(["topic", c["slug"]], c, None, rank(by_cat[i])) for i, c in enumerate(cats)]
    pages += [Page(["target", t["slug"]], None, t, rank(by_tgt[i])) for i, t in enumerate(tgts)]
    # Non-empty only, and in the dataset's own facet order rather than by size, so the sitemap reads
    # the same way the site's chips do.
    pages += [Page(["topic", cats[i]["slug"], "target", tgts[j]["slug"]], cats[i], tgts[j],
                   rank(by_both[(i, j)]))
              for i in range(len(cats)) for j in range(len(tgts)) if (i, j) in by_both]
    return pages


# ------------------------------------------------------------------ rendering
def row_html(page: Page, r: dict, i: int, os_labels: list[str]) -> str:
    """One table row. Same seven columns and the same class names as the template's `render()`, so the
    stylesheet copied out of it fits without a second set of rules to keep in step."""
    os = " ".join(f'<span class="v{esc(r["os"][k:k + 1] or "-")}">{esc(o[:3])}</span>'
                  for k, o in enumerate(os_labels))
    # The cross-axis column, on the Markdown edition's rule: a topic page prints what each project
    # plugs into, a target page prints what each project is. Printing the page's own topic 100 times
    # tells the reader nothing they did not get from the heading.
    tags = "" if page.cat else f'<span class="tag cat">{esc(r["cat_name"])}</span>'
    tags += "".join(f'<span class="tag">{esc(t)}</span>' for t in r["target_names"])
    # GitHub's social card for the repository, derived from the `nwo`, for every row. This used to prefer
    # the `img` column -- whatever URL the upstream README used for its own banner -- with the card as the
    # fallback. The column is still in `data.json`; it is simply not rendered here any more (JFH-218),
    # because nothing bounds what those 686 URLs serve: median 447,380 B, largest 10,946,713 B, one animated
    # GIF at 716,235 B. A page like this one lays out 100 rows, so preferring the column meant a static file
    # that could ask a reader for tens of megabytes from 46 hosts, and there is no client-side rescue on a
    # prerendered page. A social card is a fixed ~100 KB at 1200x600, which still oversupplies the slot.
    #
    # The same one-line change is in the index's row normaliser, for the same reason. `22_detail.py` is
    # deliberately *not* in step: one image on a page nobody's budget notices is exactly where a project's
    # own screenshot belongs, and it is the surface that keeps the column honest.
    img = esc(f"https://opengraph.githubassets.com/1/{r['nwo']}")
    url = esc(r["url"])
    # The name goes to this site's own page for the project and the `nwo` underneath it goes to GitHub,
    # which is the split the index table uses too. It matters more here than there: these 156 pages are
    # the only *crawlable* path into the atlas -- `docs/index.html` builds its table in JavaScript, so a
    # crawler that lands on the root finds no links to the 1,294 detail pages at all -- and a row whose
    # only link left the site meant every one of those pages was reachable from the sitemap and from
    # nowhere else. The picture points at the same page as the name and is hidden from the accessibility
    # tree, because a screen reader announcing an empty link before the name it duplicates is noise.
    page_url = esc(page.repo(r["nwo"]))
    stars = f"{r['stars']:,}" if r["stars"] else "&mdash;"
    return (
        "<tr>"
        f'<td class="n rk">{i}</td>'
        f'<td class="shot"><a href="{page_url}" tabindex="-1" aria-hidden="true">'
        f'<img loading="lazy" alt="" src="{img}"></a></td>'
        f'<td class="pj"><a class="nm" href="{page_url}">{esc(r["name"])}</a>'
        f'<a class="nwo" href="{url}">{esc(r["nwo"])}</a>'
        f'<div class="meta os">{os}</div></td>'
        f'<td class="n st-c"><span class="st{"" if r["stars"] else " none"}">{stars}</span>'
        f'<div class="meta">{r["lists"]} {"list" if r["lists"] == 1 else "lists"}</div></td>'
        f'<td class="hide">{tags}</td>'
        f'<td class="ds"><div class="desc">{esc(r["blurb"])}</div>'
        + (f'<code class="cmd">{esc(r["install"])}</code>' if r["install"] else "")
        + "</td>"
        f'<td class="c hide"><div class="meta">{esc(r["lang"] or "—")}<br>'
        f'{esc(r["license"] or "—")}<br>{esc(r["pushed"] or "—")}</div></td>'
        "</tr>")


def itemlist(page: Page, shown: list[dict]) -> str:
    """`ItemList` for the rows that are actually on the page.

    Ranked lists are what this site is, and `ItemList` is the vocabulary for one -- it is also the only
    structured data here that is true without qualification, which is why there is no `SoftwareApplication`
    per row: the stars and the platform verdicts are a dated snapshot of somebody else's repository and
    marking them up as this site's claims about that software would be a claim we cannot stand behind.

    `<` is escaped to `\\u003c` -- valid JSON, and the one sequence that could otherwise close the
    script element early and turn the rest of the document into text.
    """
    doc = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": page.heading,
        "description": page.summary,
        "url": page.url,
        "numberOfItems": len(shown),
        "itemListOrder": "https://schema.org/ItemListOrderDescending",
        # Each item's `url` is this site's page for the project rather than its GitHub URL, which is
        # what the row's own name link now points at -- structured data that named a different
        # destination than the markup beside it would be describing a page that does not exist. It is
        # also the form the vocabulary is for: a `ListItem` in an `ItemList` on a page identifies a
        # position in *this* list, and every one of those positions is now a real URL here.
        "itemListElement": [{"@type": "ListItem", "position": i, "name": r["name"],
                             "url": SITE + repo_path(r["nwo"])}
                            for i, r in enumerate(shown, 1)],
    }
    return json.dumps(doc, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")


def related(page: Page, pages: list[Page]) -> str:
    """The link graph between the 156 pages.

    Without it every one of them is an orphan reachable only from `sitemap.xml`, and a sitemap is a
    hint rather than a path -- an unlinked page is discovered late, crawled rarely and ranked as the
    dead end it looks like. It is also the navigation a reader who arrived from a search result
    actually wants: they landed on one cell of a 14 x 12 grid and the next thing they need is the
    neighbouring cell.
    """
    out = ['<nav class="rel">']
    if page.cat and page.tgt:
        out += [f"<h2>This topic, other harnesses</h2><p>{esc(page.cat['name'])} filtered to what "
                "plugs into each of the others.</p>"]
        sibs = [p for p in pages if p.cat and p.tgt and p.cat is page.cat and p is not page]
        out += [f'<a class="chip" href="{page.rel("/".join(p.parts))}/">'
                f'{esc(p.tgt["name"])} <span class="ct">{len(p.rows):,}</span></a>'
                for p in sibs]
        out += ["<h2>Or drop a filter</h2>",
                f'<a class="chip" href="{page.rel("topic/" + page.cat["slug"])}/">'
                f'All {esc(page.cat["name"])}</a>',
                f'<a class="chip" href="{page.rel("target/" + page.tgt["slug"])}/">'
                f'Everything for {esc(page.tgt["name"])}</a>']
    elif page.cat:
        out += ["<h2>Narrow this topic to one harness</h2>"
                "<p>Only the crossings that have projects in them are listed.</p>"]
        kids = [p for p in pages if p.cat is page.cat and p.tgt]
        out += [f'<a class="chip" href="{page.rel("/".join(p.parts))}/">'
                f'{esc(p.tgt["name"])} <span class="ct">{len(p.rows):,}</span></a>'
                for p in kids]
        out += ["<h2>Every other topic</h2>"]
        out += [f'<a class="chip" href="{page.rel("topic/" + p.cat["slug"])}/">{esc(p.cat["name"])}</a>'
                for p in pages if p.cat and not p.tgt and p.cat is not page.cat]
    else:
        out += ["<h2>One topic at a time</h2>"
                f"<p>{esc(page.tgt['name'])} crossed with each topic that has projects for it.</p>"]
        kids = [p for p in pages if p.tgt is page.tgt and p.cat]
        out += [f'<a class="chip" href="{page.rel("/".join(p.parts))}/">'
                f'{esc(p.cat["name"])} <span class="ct">{len(p.rows):,}</span></a>'
                for p in kids]
        out += ["<h2>Every other harness</h2>"]
        out += [f'<a class="chip" href="{page.rel("target/" + p.tgt["slug"])}/">'
                f'{esc(p.tgt["name"])}</a>'
                for p in pages if p.tgt and not p.cat and p.tgt is not page.tgt]
    out += ["</nav>"]
    return "".join(out)


def image_tags(page: Page, cards: set[str]) -> str:
    """The Open Graph image block, and the fallback for a page whose card has not been rendered.

    Absolute, unlike every other URL these pages emit. A relative `og:image` is resolved against
    whatever the scraper decides the document's base is and several of them decide wrong, so this is
    the one place where being unambiguous is worth more than being portable between a local
    `python -m http.server` and the Pages subpath.

    Checked against a listing of `docs/og/` rather than assumed, even though `page.card` is a pure
    function of the facet: `23_og.py` needs a headless Chromium and, without one, deliberately
    degrades to leaving the committed cards alone -- so a facet added in the same run that had no
    browser has a name here and no file. Falling back to the repository card costs that page the
    specific preview; pointing at a 404 costs it the image altogether, because Slack and Discord show
    a bare link rather than substituting anything.

    `twitter:card` is not optional and is not implied by the rest. Without it X renders a small square
    thumbnail beside the text no matter what the image is, which is the one shape a 1.91:1 card cannot
    survive. `twitter:image` is a belt-and-braces duplicate -- X falls back to `og:image` -- and it is
    two lines rather than an argument.
    """
    if page.card in cards:
        return "\n".join([
            f'<meta property="og:image" content="{esc(SITE + OG + "/" + page.card)}">',
            '<meta property="og:image:type" content="image/png">',
            '<meta property="og:image:width" content="1200">',
            '<meta property="og:image:height" content="630">',
            f'<meta property="og:image:alt" content="{esc(page.card_label)} on the Awesome Agentic '
            'Atlas: the project count and the three most starred projects.">',
            '<meta name="twitter:card" content="summary_large_image">',
            f'<meta name="twitter:image" content="{esc(SITE + OG + "/" + page.card)}">',
        ])
    # No dimensions claimed for this one: it is 1200x600 today and it is not ours to promise.
    fallback = f"https://opengraph.githubassets.com/1/{esc(REPO)}"
    return "\n".join([
        f'<meta property="og:image" content="{fallback}">',
        '<meta property="og:image:alt" content="The Awesome Agentic Atlas repository on GitHub.">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:image" content="{fallback}">',
    ])


def render(page: Page, pages: list[Page], data: dict, cards: set[str]) -> str:
    shown = page.rows[:CAP]
    ranked = sum(1 for r in page.rows if r["stars"])
    stars = sum(r["stars"] or 0 for r in page.rows)
    blurbs = [b for b in ((page.cat or {}).get("blurb"), (page.tgt or {}).get("blurb")) if b]
    rest = ""
    if len(page.rows) > len(shown):
        rest = (f'<p class="rest">Showing the top {len(shown)} of {len(page.rows):,} by stars. '
                f'<a href="{esc(page.live)}">The full {len(page.rows):,} are in the interactive '
                "view</a>, "
                "which can also sort by list count or last push, search the blurbs, and filter on "
                "operating system.</p>")
    return f"""<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page.title)}</title>
<meta name="description" content="{esc(page.summary)}">
<link rel="canonical" href="{esc(page.url)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(page.heading)}">
<meta property="og:description" content="{esc(page.summary)}">
<meta property="og:url" content="{esc(page.url)}">
{image_tags(page, cards)}
<link rel="icon" href="{ICON}">
<link rel="stylesheet" href="{page.rel('pages.css')}">
<script type="application/ld+json">{itemlist(page, shown)}</script>
</head>
<body>
<header><div class="wrap"><div class="top">
  <div>
    <h1>{esc(page.heading)}</h1>
    <p class="sub"><b>{len(page.rows):,}</b> projects · <b>{ranked:,}</b> with stars to rank by ·
      <b>{stars:,}</b> combined stars · snapshot {esc(data['snapshot'])}</p>
    {"".join(f'<p class="blurb">{esc(b)}</p>' for b in blurbs)}
    <a class="cta" href="{esc(page.live)}">Filter this live on the atlas &rarr;</a>
  </div>
  <nav>
    <a href="{page.rel()}">Every project</a> ·
    <a href="https://github.com/{esc(REPO)}">Repository</a> ·
    <a href="https://github.com/{esc(REPO)}/tree/main/mega-list">Markdown edition</a><br>
    <button class="chip" id="theme" aria-pressed="false">Light theme</button>
  </nav>
</div></div></header>

<main><div class="wrap">
<table>
<thead><tr><th class="n">#</th><th class="shot">Shot</th><th class="pj">Project</th>
<th class="n st-c">Stars</th><th class="hide">{"Plugs into" if page.cat else "Topic &amp; targets"}</th>
<th class="ds">What it does</th><th class="c hide">Lang / licence / push</th></tr></thead>
<tbody>
{chr(10).join(row_html(page, r, i, data["os"]) for i, r in enumerate(shown, 1))}
</tbody></table>
{rest}
{related(page, pages)}
</div></main>

<footer><div class="wrap">
  This is a static slice of the <a href="{page.rel()}">Awesome Agentic Atlas</a>, which merges eleven
  awesome-lists into one index; all eleven are credited in the
  <a href="https://github.com/{esc(REPO)}#the-eleven-lists">repository</a>. Stars, language, licence
  and last-push come from the GitHub API on {esc(data['snapshot'])} and drift daily. Platform verdicts
  are derived from each project's own README, install route, CI config and release assets &mdash;
  <span class="vY">green</span> is stated evidence, <span class="vL">amber</span> is inferred from the
  language. A dash in the star column means the row is a folder inside someone else's repo, or a dead
  link, and has no count of its own.
</div></footer>
{THEME_JS}{b19.beacon()}</body>
</html>
"""


# ------------------------------------------------------------------ sitemap & robots
def sitemap(pages: list[Page], snapshot: str) -> str:
    """Sitemap 0.9, the root first.

    `lastmod` is `data.json`'s snapshot date rather than today: it is the day the data these pages show
    was actually true, and a build that only re-rendered the shell has not changed anything a crawler
    should come back for. Claiming otherwise on 157 URLs at once is how a sitemap teaches Google to
    stop believing its own dates.

    No `changefreq` and no `priority`. Google ignores both, and a number invented for every page is
    noise in a file whose whole value is that everything in it is checkable.
    """
    locs = [SITE] + [p.url for p in pages]
    body = "\n".join(f"  <url><loc>{esc(u)}</loc><lastmod>{esc(snapshot)}</lastmod></url>"
                     for u in locs)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{body}\n</urlset>\n")


def robots() -> str:
    """Allow everything, and say where the sitemap is.

    Nothing here is private -- it is a static index of other people's public repositories -- so a
    disallow rule could only ever hide something the site exists to publish. The absolute URL is
    required by the standard and is also the useful part: this file is the only place a crawler is
    guaranteed to look for it.

    Both sitemaps are listed, `22_detail.py`'s as well as this stage's, and the comment in the file says
    out loud that none of it currently has any effect. That is not defeatism, it is the one fact a reader
    of this file needs: robots.txt is only ever read at a *host* root, and this is a project Pages site
    served under `/awesome-agentic-atlas/`, so a crawler looks for it at `crazy54.github.io/robots.txt`
    -- which 404s, because no user-repo Pages site exists there. Checked rather than assumed. Written
    anyway because it costs nothing and becomes correct the day a custom domain appears; until then both
    sitemaps have to be submitted in Search Console to be discovered at all.
    """
    return ("# Everything here is a static index of public repositories. Nothing to hide from a\n"
            "# crawler, and the hash-filtered views are all prerendered under /topic/, /target/\n"
            "# and /repo/.\n"
            "User-agent: *\n"
            "Allow: /\n\n"
            "# Both sitemaps are listed for correctness, not for effect. This file is inert on the\n"
            "# current deployment: robots.txt is only read at a host root, and this is a *project*\n"
            "# Pages site served under /awesome-agentic-atlas/, so crawlers look for it at\n"
            "# crazy54.github.io/robots.txt -- which is a 404, because no user-repo Pages site exists.\n"
            "# Verified, not assumed. Until a custom domain appears, both sitemaps have to be submitted\n"
            "# in Search Console to be discovered at all.\n"
            f"Sitemap: {SITE}sitemap.xml\n"
            f"Sitemap: {SITE}sitemap-repos.xml\n")


# ------------------------------------------------------------------ the IndexNow key file
# IndexNow's whole credential: a file at the site root named `<key>.txt` whose entire content is that key.
# Written here rather than committed by hand, and that is not a style preference -- `docs/` is regenerated
# output and `daily.yml` fails the build for any tracked file under it that no generator wrote, so a
# hand-placed key file would either break the build or be deleted by whichever pass tidied up next. This
# stage owns it because this stage owns `robots.txt`: same kind of file, same root, same reason.
#
# The key itself and its format assertion live in `19_pages.py` beside the beacon token, so the value that
# goes in this file and the value `26_indexnow.py` puts in every payload are one string. See there.
#
# Where this file sits is load-bearing and it is the same trap `robots()` documents. IndexNow scopes a key
# to the *directory* the key file is in: a key at the host root can submit any URL on the host, and a key
# in a subdirectory can only submit URLs beneath it. This is a project Pages site under
# `/awesome-agentic-atlas/`, so the host root is not ours to write to -- `crazy54.github.io/<key>.txt`
# would be somebody else's 404. Hosting it here instead is not a workaround, it is the supported form:
# `26_indexnow.py` sends `keyLocation` pointing at this file, and every URL it submits is under this
# directory by construction. Unlike robots.txt, therefore, this one is not inert on the current
# deployment -- it works today, with no custom domain.
def key_text(key: str) -> str:
    """The key, and nothing else. No trailing newline: the spec says the file contains the key, and while
    every validator seen in the wild trims whitespace, "contains the key" is the only promise worth
    making to something that answers 403 without saying why."""
    return key


def is_key_file(path: Path) -> bool:
    """Whether `path` is an IndexNow key file, judged by what is *in* it and not by what it is called.

    A key file is the one file on this site whose name and content are the same string: `key_text` writes
    the key and nothing else into `<key>.txt`. So `content == stem` is not a heuristic, it is the file
    format, and it is the only test here that cannot be satisfied by accident.

    The name shape is checked too, but only as a cheap precondition -- on its own it is not enough, and
    that is the whole reason this function exists rather than a regex at the call site. `[A-Za-z0-9-]{8,128}`
    matches the stem of `security.txt`, which is eight in-alphabet characters and a plausible thing for
    somebody to add to a site root; deleting it on sight would be this stage silently removing a file it
    has no business knowing about. Its *content* is a security policy, not the word "security", so the
    content test spares it while still catching every real rotated key.
    """
    if not b19.INDEXNOW_RE.match(path.stem):
        return False
    try:
        return path.read_text(encoding="utf-8").strip() == path.stem
    except (OSError, UnicodeDecodeError):
        # Unreadable or not text, so not something this stage wrote. Left alone rather than guessed at.
        return False


def prune_keys(keep: set[Path]) -> list[Path]:
    """Delete key files from an earlier `INDEXNOW_KEY` that are not in `keep`.

    Rotating the key changes the *filename*, so without this a rotation leaves the old file tracked,
    served and never rewritten -- which `weekly.yml`'s "every tracked page was rewritten" assertion reads,
    correctly, as a generator having gone missing, and fails the build over a file nothing wants any more.
    Deleting it is only half of that fix: a tracked file that is *gone* from the working tree used to land
    in the same assertion's error arm, because `git ls-files` reads the index and `-nt` against a missing
    file is false. `weekly.yml` now sorts on existence first, so a file this function removes is reported
    as a deletion the commit will carry rather than as a generator that went missing.

    `keep` is resolved paths, and is the same contract as `prune` below: the delete set is derived from
    what this run actually wrote rather than from what a name looks like. That ordering matters -- the
    current key file is in `keep` because `main` wrote it, so it cannot be deleted by a mistake in the
    name test, and `robots.txt` is in `keep` for the same reason instead of being spelled out here.
    """
    gone = []
    for path in sorted(OUT.glob("*.txt")):
        if path.resolve() in keep or not is_key_file(path):
            continue
        path.unlink()
        gone.append(path)
    return gone


# ------------------------------------------------------------------ writing
def prune(keep: set[Path]) -> list[Path]:
    """Delete landing pages this run did not write, then the directories they emptied.

    Overwriting in place makes a rerun idempotent for pages that still exist; it does nothing about the
    ones that stopped existing. A renamed topic, or a crossing whose last project moved, would
    otherwise leave a page that is still served, still in nobody's sitemap, and still claiming a
    canonical URL -- indexed, stale, and invisible to every later run. Only `index.html` files and the
    directories that held them are touched, so nothing else anyone put under `docs/` is at risk.
    """
    gone = []
    for base in (OUT / "topic", OUT / "target"):
        if not base.exists():
            continue
        for path in sorted(base.rglob("index.html")):
            if path.resolve() not in keep:
                path.unlink()
                gone.append(path)
        # Deepest first, so a crossing directory is gone before its topic directory is examined.
        for d in sorted((p for p in base.rglob("*") if p.is_dir()),
                        key=lambda p: len(p.parts), reverse=True):
            if not any(d.iterdir()):
                d.rmdir()
        if not any(base.iterdir()):
            base.rmdir()
    return gone


def kb(n: int) -> str:
    return f"{n / 1024:,.1f} KB" if n < 1024 * 1024 else f"{n / 1048576:,.2f} MB"


def main() -> None:
    data = json.loads((OUT / "data.json").read_text(encoding="utf-8"))
    pages = plan(data)
    # One listing, not 156 `exists()` calls -- and taken before the loop so every page in a run is
    # judged against the same set of cards.
    cards = {p.name for p in (OUT / OG).glob("*.png")}

    written, total = 0, 0
    for p in pages:
        p.path.parent.mkdir(parents=True, exist_ok=True)
        text = render(p, pages, data, cards)
        p.path.write_text(text, encoding="utf-8")
        written += 1
        total += p.path.stat().st_size

    (OUT / "pages.css").write_text(CSS, encoding="utf-8")
    (OUT / "sitemap.xml").write_text(sitemap(pages, data["snapshot"]), encoding="utf-8")
    (OUT / "robots.txt").write_text(robots(), encoding="utf-8")
    keyfile = b19.indexnow_key_file()
    (OUT / keyfile).write_text(key_text(b19.indexnow_key()), encoding="utf-8")
    # The `keep` set is every `.txt` at the root this run wrote, taken after writing them, so it is a
    # record of what happened rather than a second list to keep in step with the writes above.
    stale_keys = prune_keys({(OUT / f).resolve() for f in ("robots.txt", keyfile)})

    gone = prune({p.path.resolve() for p in pages})

    shells = sum((OUT / f).stat().st_size
                 for f in ("pages.css", "sitemap.xml", "robots.txt", keyfile))
    tops = sum(1 for p in pages if p.cat and not p.tgt)
    tgt_n = sum(1 for p in pages if p.tgt and not p.cat)
    print(f"{tops} topic · {tgt_n} target · {written - tops - tgt_n} crossing "
          f"= {written} pages · {kb(total)}")
    print(f"pages.css + sitemap.xml + robots.txt + {keyfile} · {kb(shells)} · "
          f"{len(pages) + 1} URLs, lastmod {data['snapshot']}")
    print(f"IndexNow key hosted at {SITE}{keyfile}"
          + (f" · {len(stale_keys)} stale key file(s) removed: "
             + ", ".join(p.name for p in stale_keys) if stale_keys else ""))
    print(f"{sum(min(len(p.rows), CAP) for p in pages):,} rows rendered, "
          f"capped at {CAP} per page · {kb(total + shells)} added to docs/")
    carded = sum(1 for p in pages if p.card in cards)
    print(f"og:image · {carded}/{len(pages)} pages on one of {len(cards)} card(s) in docs/{OG}/"
          + ("" if carded == len(pages) else
             f" · {len(pages) - carded} on the repository card, run scripts/23_og.py"))
    if gone:
        print(f"{len(gone)} stale page(s) removed: "
              + ", ".join(str(p.relative_to(OUT)) for p in gone[:5]))


if __name__ == "__main__":
    main()
