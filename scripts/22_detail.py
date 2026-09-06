"""Give every repository a page of its own, because a table row is not a destination.

The atlas knows more about each project than the link it hands the reader: the install command, five
platform verdicts derived from the project's own README and CI, which of the eleven source lists named
it, and where it sits in a 14 x 12 taxonomy. All of that is currently squeezed into one row and then
the reader is sent to github.com, where none of it exists. This stage writes the row out as a page.

  docs/repo/<owner>/<name>/index.html   1,294, one per repository
  docs/repo/index.html                  the directory that makes the 1,294 reachable
  docs/repo/detail.css                  the shared shell
  docs/repo/detail.js                   the shared behaviour
  docs/sitemap-repos.xml                every page above

  python scripts/22_detail.py                 write into docs/
  python scripts/22_detail.py --out DIR       write somewhere else, for measuring drift

The stylesheet and the script live under `docs/repo/` next to the pages they serve rather than beside
`pages.css` at the root, because `20_landing.py` owns that filename and two stages writing one file is
how a stylesheet loses half its rules to whichever stage ran last.

  -- Why almost nothing on these pages is a number --

This is the decision the whole stage is built around, and it is a history decision rather than a design
one. Pages here is a `build_type: legacy` deployment: `docs/` is committed verbatim, so every byte this
script emits is a byte git keeps for ever, and `.git` is already ~110 MB. The 156 facet pages
`20_landing.py` writes embed a star count per row and the snapshot date in their header, which means
essentially all 156 change on every rebuild -- a rebuild is a commit of the whole set, for ever, and at
a daily cron that is hundreds of megabytes a year for data that was already committed once in
`data.json`.

1,294 pages built the same way would be that cost multiplied by eight. So they are not built that way:
nothing volatile is rendered into the HTML. No star count, no last-push date, no snapshot date, and no
ordering derived from any of them -- the related-projects list is ranked by shared targets, list count
and name, all of which are properties of the curation rather than of GitHub's counters. What is left is
a page whose bytes are a pure function of the parts of `data.json` that only change when a source list
changes, so a rebuild on a day when nothing was re-curated writes 1,294 byte-identical files and git
records nothing at all.

The two numbers a reader actually wants -- stars and last push -- are fetched after paint by `detail.js`
and injected, so neither is in the bytes this stage commits. They come from `docs/live.json`, the sidecar
`19c_live.py` derives from `data.json`: 57,418 B raw and 21,791 B gzipped, against `data.json`'s 569,096 B
and 162,473 B. Until JFH-222 that fetch was `data.json` itself -- every one of these 1,294 pages downloaded
all eighteen columns of all 1,294 rows to read three values out of one of them -- so this is 7.5x fewer
bytes on the wire for the surface that is 1,294 of the site's ~1,500 URLs and the one a search result lands
somebody on cold. Quote the gzipped pair and not the raw one: Pages serves both with
`Content-Encoding: gzip`, so the gzipped figure is the one a reader is charged.

What it costs is what an earlier version of this comment declined to pay: 57 KB of committed churn per
rebuild, for ever, against the zero additional bytes that reusing an already-committed file cost. The two
mitigations are that `live.json`'s keys are sorted by `nwo` rather than left in `data.json`'s
star-descending row order, so a day of moving stars changes values in place instead of permuting 57 KB and
git's delta stays proportional to the numbers that actually moved -- and that it is one file rather than
1,294.

It is *not* written by this stage, and that is a decision rather than an oversight. JFH-222 asked for it to
be emitted from here, out of the same in-memory rows as the pages, so that two derivations of one number
could not drift. The conclusion is right and the remedy is backwards for this pipeline: this stage runs
weekly and `data.json` is rebuilt daily. Hanging the sidecar off it would peg the star counts on 1,294
detail pages to the weekly run while the index and the 156 facet pages moved nightly, and publish a page
claiming 4,010 stars beside a facet page claiming 4,193 for the same repository for up to six days at a
time. `19c_live.py` runs in both workflows immediately after `19_pages.py` instead, which is the only stage
that writes `data.json`; see its docstring for what holds that ordering up.

The cost of this choice is that the star count is not in the first paint, which the ticket's acceptance
criteria could be read as forbidding. It is worth being precise about what is and is not in the initial
response: the name, the description, the install command, the platform table, the classification, the
eleven-list provenance and the related projects all are, which is every fact that makes this page worth
indexing and every fact a crawler could rank it on. Google has never needed a star count to understand
a page, and a reader with JavaScript off gets a page that is complete except for two figures that carry
a link to where they are authoritative anyway.

  -- Three more decisions --

No README excerpt, which the ticket asks for. The cached READMEs live in `cache/readmes/`, and `cache/`
is gitignored precisely because it is "verbatim copies of 1,293 other people's READMEs ... not ours to
redistribute". Reading it would make these pages depend on a 64 MB artefact a fresh clone does not have,
so the same clone would rebuild 1,294 *different* pages -- the exact failure `20_landing.py` avoids by
reading `data.json` and nothing else. It would also republish third-party prose the repository has
deliberately decided not to republish, and add roughly half a kilobyte of churning text per page. The
curated blurb, which is this project's own writing and is already in `data.json`, does the job.

The screenshot is the remote URL the rest of the site already uses. There are no images under `docs/`
at all: `cache/shots/` is gitignored, and the site points at each project's own asset or falls back to
`opengraph.githubassets.com`. Rendering it at full width therefore costs the repository nothing, and it
is lazy-loaded and placed below the summary so an image of unknown dimensions on somebody else's CDN is
never what the largest-contentful-paint timer is waiting for.

`sitemap-repos.xml` carries no `lastmod`. `20_landing.py` puts the snapshot date on its URLs and is
right to, because its pages really do change every run; putting the same date on 1,295 URLs whose bytes
did not change would be a false claim on a scale that teaches a crawler to stop believing the file. The
element is optional in Sitemap 0.9, and omitting it also makes this file itself byte-stable.

A second sitemap needs a second `Sitemap:` line in `docs/robots.txt`, which `20_landing.py` owns and
this stage does not write.
"""
from __future__ import annotations

import argparse
import html
import importlib.util
import json
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent

# The same dynamic load `19b_refresh.py` and `20_landing.py` use, and for the same reason: the module is
# named `19_pages`, which is not an identifier, so `import` cannot reach it. Three things are wanted --
# `beacon()`, so the analytics token lives in one file; `b17.SITE`, so the absolute URL in every
# canonical is the one string the rest of the project links to; and `b16.SHEETS`, so the eleven list
# labels in `data.json`'s `listed_by` can be turned back into links to the lists themselves.
spec = importlib.util.spec_from_file_location("b19", HERE / "19_pages.py")
b19 = importlib.util.module_from_spec(spec)
sys.modules["b19"] = b19
spec.loader.exec_module(b19)

SITE = b19.b17.SITE
REPO = b19.REPO

# How many related projects a page offers. Eight is where the section still reads as a recommendation
# rather than a second index: the two biggest topics have over 300 members each, and a page that listed
# them all would bury its own content under somebody else's names and hand a crawler 300 outbound
# internal links whose value is diluted by their own number.
KIN = 8

# The prose behind each verdict character. `19_pages.py` compresses the five verdicts to one letter for
# the wire and expands them again in the browser with a glyph and a tooltip; a detail page has room to
# print the word and the reason in full, which is the point of having a page. Kept in the same order and
# with the same wording as the template's own `VERDICT` map so the two surfaces cannot describe the same
# evidence differently.
VERDICT = {
    "Y": ("Yes", "good", "Stated in the project's own README, install route, CI config or release "
                          "assets."),
    "L": ("Likely", "warn", "Inferred from the language or runtime. Nothing in the project says so."),
    "N": ("No", "off", "No evidence of support anywhere in the project."),
    "a": ("n/a", "off", "Not applicable — this row is not something you install."),
    "-": ("—", "off", "Not established. Too little in the repository to call either way."),
}


# ------------------------------------------------------------------ escaping
def esc(text) -> str:
    """Every interpolated value goes through this.

    These strings are other people's hand-written list entries -- 1,294 names, blurbs and install
    commands typed into eleven different READMEs. One stray `<` becomes a tag and one stray `"` closes
    the attribute it is sitting in and lets the rest of the page be read as markup. `quote=True`
    because roughly half of these land in attributes, and three of the 1,294 names carry an ampersand,
    which is an unterminated character reference wherever it is not escaped.
    """
    return html.escape("" if text is None else str(text), quote=True)


def clip(text: str, limit: int) -> str:
    """Shorten on a word boundary. For `<meta name=description>`, which Google truncates at ~160."""
    if len(text) <= limit:
        return text
    return text[: limit - 1].rsplit(" ", 1)[0].rstrip(" ,;:.—-") + "…"


# ------------------------------------------------------------------ the eleven lists
def source_links() -> dict[str, str]:
    """`listed_by` label -> the repository that list lives in.

    `data.json` stores provenance as a comma-joined string of display labels, which is the right shape
    for a table cell and useless as a link. Ten of the eleven labels are `16_build_all.SHEETS`, whose
    rows are `(key, label, nwo, blurb)`; the eleventh is the original orchestrators list, which predates
    that table and is labelled from `10_parse_sources.SOURCES`. Both are static configuration rather
    than build cache, so this stays a pure function of the checkout.

    Any label that does not resolve is rendered as plain text rather than dropped, and `main()` says so
    on stdout -- a list that quietly stopped being clickable on 1,294 pages is not a failure anyone
    would notice from the output.
    """
    links = {label: nwo for _key, label, nwo, *_ in b19.b17.b16.SHEETS}
    # The orchestrators list by name, because it is the one source with no `SHEETS` row: the whole
    # collection grew out of it, so it is the original sheet rather than one of "the ten added lists".
    links.setdefault("Orchestrators", "andyrewlee/awesome-agent-orchestrators")
    return links


# ------------------------------------------------------------------ the page set
def segment(part: str) -> str:
    """One path segment of a repository's URL.

    Lowercased, which is lossless here -- 442 of the 1,294 `nwo` values carry capitals and no two of
    them collide once folded, asserted in `plan()` -- and worth doing because a URL that differs from
    another only in case is two URLs to Pages, one of which 404s, and one directory to Windows.

    A leading dot is rewritten. `zircote/.claude` is a real row, and a directory whose name starts with
    a dot is the one thing in this tree whose behaviour on Pages cannot be checked from a local server:
    Jekyll excludes dotfiles by default and `.nojekyll` is documented as being about underscores, so
    whether `/repo/zircote/.claude/` is served at all is a guess. Renaming one segment of one page costs
    less than finding out in production.
    """
    return ("dot-" + part[1:]) if part.startswith(".") else part


class Repo:
    """One output file, and everything needed to write it.

    Built for the whole set before anything is rendered, because four consumers need the same list and
    they must agree: the renderer, the related-projects lookup, the directory index, and the prune pass
    that deletes whatever this run did not produce.
    """

    def __init__(self, row: dict, out: Path):
        self.row = row
        owner, name = row["nwo"].split("/", 1)
        self.parts = ["repo", segment(owner.lower()), segment(name.lower())]
        self.path = out.joinpath(*self.parts, "index.html")
        self.url = SITE + "/".join(self.parts) + "/"

    # Every detail page sits exactly three directories below `docs/`, so this is a constant rather than
    # a computed depth. Relative rather than absolute so the tree serves identically from a
    # `python -m http.server` in `docs/` and from the `/awesome-agentic-atlas/` path prefix Pages adds.
    def rel(self, tail: str = "") -> str:
        return "../../../" + tail

    def kin_href(self, other: "Repo") -> str:
        """A link to another detail page, from this one. Both are at depth three, so the two owner and
        name segments are all that differ."""
        return "../../" + "/".join(other.parts[1:]) + "/"

    @property
    def name(self) -> str:
        return self.row["name"]

    @property
    def title(self) -> str:
        """Unique per page, front-loaded with the words someone would type.

        293 of the 1,294 names are already `owner/name`, so repeating the `nwo` after them would spend a
        third of a 60-character result snippet saying the same thing twice.
        """
        lead = self.name if self.name.lower() == self.row["nwo"].lower() else \
            f"{self.name} ({self.row['nwo']})"
        return f"{lead} — {self.row['cat_name']} — Awesome Agentic Atlas"

    @property
    def summary(self) -> str:
        """`<meta name=description>`. The curated blurb where there is one, because it is already
        written prose and is the only sentence about this project this repository wrote itself. Six rows
        have no blurb at all, and for those the classification is the description -- it is thin, but it
        is true, and it is more than the empty string a template would otherwise emit."""
        if self.row["blurb"]:
            return clip(self.row["blurb"], 158)
        targets = ", ".join(self.row["target_names"])
        lead = f"{self.name} is a {self.row['cat_name']} project"
        return clip(f"{lead} for {targets}. Install command, platform support and provenance."
                    if targets else f"{lead}. Install command, platform support and provenance.", 158)

    @property
    def shot(self) -> str:
        """The screenshot, or the social card. `data.json` stores "" for two thirds of these rows rather
        than 55 bytes x 1,294 of a string it can rebuild from the `nwo`, so rebuild it."""
        return self.row["img"] or f"https://opengraph.githubassets.com/1/{self.row['nwo']}"


def plan(data: dict, out: Path) -> tuple[list[Repo], dict[int, list[Repo]]]:
    """Every repository as a page, plus the topic index the related-projects section reads.

    Column-oriented on disk, objects in here -- the same one pass the site's own JavaScript makes, so
    everything downstream reads `r["stars"]` instead of `r[4]`. The two facet columns are indexes into
    `cats` and `targets`; they are resolved to names once here rather than once per page.
    """
    cats, tgts = data["cats"], data["targets"]
    rows = [dict(zip(data["cols"], r)) for r in data["rows"]]
    for r in rows:
        r["cat_name"] = cats[r["cat"]]["name"]
        r["cat_slug"] = cats[r["cat"]]["slug"]
        r["target_names"] = [tgts[t]["name"] for t in r["targets"]]
        r["target_slugs"] = [tgts[t]["slug"] for t in r["targets"]]

    repos = [Repo(r, out) for r in rows]

    # Asserted rather than assumed, because the whole URL scheme rests on it. `nwo` is unique in
    # `data.json` today and stays unique through case-folding today, but a second row for the same
    # repository under a different capitalisation would silently overwrite the first page -- one repo
    # would vanish from the site and the sitemap would still be advertising it.
    seen: dict[str, str] = {}
    for repo in repos:
        key = "/".join(repo.parts)
        if key in seen:
            raise SystemExit(f"two rows want the same page: {seen[key]!r} and {repo.row['nwo']!r} "
                             f"both slug to {key!r}. Resolve the duplicate in the dataset first.")
        seen[key] = repo.row["nwo"]

    by_cat: dict[int, list[Repo]] = {i: [] for i in range(len(cats))}
    for repo in repos:
        by_cat[repo.row["cat"]].append(repo)
    return repos, by_cat


def kin(repo: Repo, by_cat: dict[int, list[Repo]]) -> list[Repo]:
    """The related-projects list: same topic, closest first.

    Ordered by how many harnesses it shares with this project, then by how many of the eleven lists
    named it, then by name. Deliberately not by stars, which is what the index and the facet pages rank
    by and would be the obvious choice here: a star count changes daily for most of these repositories,
    so a star-ranked list of eight would reshuffle on 1,294 pages on most days and put the whole stage
    back to rewriting the entire tree on every run. Shared targets and list count are properties of the
    curation, so they move when somebody re-curates and not otherwise.
    """
    mine = set(repo.row["targets"])
    peers = [p for p in by_cat[repo.row["cat"]] if p is not repo]
    peers.sort(key=lambda p: (-len(mine & set(p.row["targets"])), -p.row["lists"],
                             p.row["name"].lower()))
    return peers[:KIN]


# ------------------------------------------------------------------ rendering
def platforms(repo: Repo, os_labels: list[str]) -> str:
    """The five platform verdicts as a table with the reasoning printed.

    A table rather than the index's row of glyphs, because the reason behind a verdict is the part a
    reader cannot get anywhere else -- "amber" on the index narrows to "uncertain" without saying of
    what, and this is the surface with room to finish the sentence.
    """
    body = []
    for i, label in enumerate(os_labels):
        word, tone, why = VERDICT[repo.row["os"][i:i + 1] or "-"]
        body.append(f'<tr><th scope="row">{esc(label)}</th>'
                    f'<td class="v{tone}">{esc(word)}</td>'
                    f'<td class="why">{esc(why)}</td></tr>')
    return ('<table class="os"><caption>Derived from the project\'s own README, install route, CI '
            'configuration and release assets — not from running it.</caption>'
            '<thead><tr><th scope="col">Platform</th><th scope="col">Runs here</th>'
            '<th scope="col">On what evidence</th></tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table>')


def provenance(repo: Repo, lists: dict[str, str]) -> str:
    """"Named by N lists", with the lists.

    The count on its own is the one fact about a row that the index already shows and that nobody can
    check. Naming the lists and linking each to its repository turns it into something a reader can
    verify in one click, and it is also the credit those eleven curators are owed on every page that
    stands on their work.
    """
    names = [n.strip() for n in repo.row["listed_by"].split(",") if n.strip()]
    items = []
    for n in names:
        nwo = lists.get(n)
        items.append(f'<li><a href="https://github.com/{esc(nwo)}">{esc(n)}</a></li>' if nwo
                     else f"<li>{esc(n)}</li>")
    n = repo.row["lists"]
    return (f'<p class="lead">Named by <b>{n}</b> of the {b19.LISTS} lists the atlas merges'
            + ("." if n == 1 else ", independently of each other.")
            + f'</p><ul class="lists">{"".join(items)}</ul>')


def facets(repo: Repo) -> str:
    """Links out to the prerendered facet pages, which is this page's half of the link graph.

    `20_landing.py` writes 156 pages that each list up to 100 projects and are the only crawlable path
    into the dataset; without these links a detail page is a leaf hanging off a sitemap, and a sitemap
    is a hint rather than a path. The crossing page is linked in preference to the bare target page
    because it is the more specific claim and the one a reader on this page is closer to wanting.
    """
    row = repo.row
    out = [f'<a class="chip cat" href="{repo.rel("topic/" + row["cat_slug"])}/">'
           f'{esc(row["cat_name"])}</a>']
    out += [f'<a class="chip" href="{repo.rel("topic/" + row["cat_slug"])}/target/{esc(slug)}/">'
            f'{esc(name)}</a>'
            for slug, name in zip(row["target_slugs"], row["target_names"])]
    return "".join(out)


def breadcrumb(repo: Repo) -> str:
    """`BreadcrumbList`, and nothing else.

    The obvious markup for a page about a piece of software is `SoftwareApplication`, and it is not used
    here for the reason `20_landing.py` gives for not using it either: its interesting properties would
    be the star count and the platform list, which are a dated snapshot of somebody else's repository,
    and marking them up as this site's structured claims about that software is a claim this site cannot
    stand behind. A breadcrumb is true without qualification -- it describes this site's own hierarchy.

    `<` is escaped to `\\u003c` -- valid JSON, and the one sequence that could otherwise close the
    script element early and turn the rest of the document into text.
    """
    trail = [("Awesome Agentic Atlas", SITE),
             (repo.row["cat_name"], f"{SITE}topic/{repo.row['cat_slug']}/"),
             (repo.name, repo.url)]
    doc = {"@context": "https://schema.org", "@type": "BreadcrumbList",
           "itemListElement": [{"@type": "ListItem", "position": i, "name": n, "item": u}
                               for i, (n, u) in enumerate(trail, 1)]}
    return json.dumps(doc, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")


def render(repo: Repo, by_cat: dict[int, list[Repo]], lists: dict[str, str], data: dict) -> str:
    row = repo.row
    # `#q=` is the index's own search parameter, so this lands the reader on their row with every other
    # filter still live. Quoted because 293 of these names contain a slash and three an ampersand, both
    # of which are structural inside a query string.
    live = repo.rel() + "#q=" + urllib.parse.quote(repo.name, safe="")
    peers = kin(repo, by_cat)
    install = (f'<div class="cmdrow"><code class="cmd" id="cmd">{esc(row["install"])}</code>'
               '<button class="copy" hidden data-for="cmd" '
               f'aria-label="Copy install command for {esc(repo.name)}">Copy</button></div>'
               if row["install"] else
               '<p class="none">No install command — this row is a write-up, a folder inside a larger '
               'repository, or a project that documents no one-line install.</p>')
    peer_html = "".join(
        f'<li><a href="{repo.kin_href(p)}">{esc(p.name)}</a>'
        f'<span class="nwo">{esc(p.row["nwo"])}</span>'
        + (f'<span class="desc">{esc(clip(p.row["blurb"], 150))}</span>' if p.row["blurb"] else "")
        + "</li>" for p in peers)

    return f"""<!doctype html>
<html lang="en" data-theme="dark" data-nwo="{esc(row["nwo"])}" data-root="{repo.rel()}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(repo.title)}</title>
<meta name="description" content="{esc(repo.summary)}">
<link rel="canonical" href="{esc(repo.url)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(repo.name)} — Awesome Agentic Atlas">
<meta property="og:description" content="{esc(repo.summary)}">
<meta property="og:url" content="{esc(repo.url)}">
<meta property="og:image" content="{esc(repo.shot)}">
<link rel="icon" href="{ICON}">
{HEAD_THEME}<link rel="stylesheet" href="../../detail.css">
<script type="application/ld+json">{breadcrumb(repo)}</script>
</head>
<body>
<header><div class="wrap">
  <nav class="crumb"><a href="{repo.rel()}">Atlas</a> ›
    <a href="{repo.rel("topic/" + row["cat_slug"])}/">{esc(row["cat_name"])}</a> ›
    <a href="{repo.rel("repo/")}">All projects</a></nav>
  <div class="top">
    <div>
      <h1>{esc(repo.name)}</h1>
      <p class="nwo"><a href="{esc(row["url"])}">{esc(row["nwo"])}</a></p>
      {f'<p class="lead">{esc(row["blurb"])}</p>' if row["blurb"]
       else '<p class="lead none">No description in any of the lists that named this project.</p>'}
      <p class="facts">
        <span>{esc(row["lang"] or "Language not detected")}</span>
        <span>{esc(row["license"] or "No licence declared")}</span>
        <span id="stars" class="live"></span>
        <span id="pushed" class="live"></span>
        <span id="snap" class="live"></span>
      </p>
      <p class="acts"><a class="cta" href="{esc(row["url"])}">View on GitHub &rarr;</a>
        <a class="alt" href="{esc(live)}">Find it in the atlas</a></p>
    </div>
    <nav class="util">
      <button class="chip" id="theme" aria-pressed="false">Light theme</button>
    </nav>
  </div>
</div></header>

<main><div class="wrap">
<section>
  <h2>Install</h2>
  {install}
</section>

<section>
  <h2>Screenshot</h2>
  <figure class="shot">
    <img loading="lazy" decoding="async" src="{esc(repo.shot)}"
         alt="Screenshot or social card for {esc(repo.name)}">
    <figcaption>{"The project's own screenshot" if row["img"] else
                 "GitHub's social card — no screenshot was found for this project"}, fetched from
      source rather than copied into this repository.</figcaption>
  </figure>
</section>

<section>
  <h2>Platform support</h2>
  {platforms(repo, data["os"])}
</section>

<section>
  <h2>Where it came from</h2>
  {provenance(repo, lists)}
</section>

<section>
  <h2>How it is classified</h2>
  <p class="lead">One topic, {len(row["target_names"]) or "no"}
    {"harness" if len(row["target_names"]) == 1 else "harnesses"}. Each link is a prerendered page of
    everything else in that slice.</p>
  <div class="chips">{facets(repo)}</div>
</section>

{f'''<section class="kin">
  <h2>Related in {esc(row["cat_name"])}</h2>
  <p class="lead">Closest first — projects that plug into the same harnesses, then the ones the most
    lists agreed on.</p>
  <ul class="kinlist">{peer_html}</ul>
</section>''' if peers else ""}
</div></main>

<footer><div class="wrap">
  One project from the <a href="{repo.rel()}">Awesome Agentic Atlas</a>, which merges {b19.LISTS}
  awesome-lists into a single index; all {b19.LISTS} are credited in the
  <a href="https://github.com/{esc(REPO)}#the-source-lists">repository</a>. The description, install
  command and platform verdicts are derived from this project's own README, install route, CI
  configuration and release assets. Star count and last push are read from the atlas dataset, which is
  a dated snapshot rather than a live figure — <a href="{esc(row["url"])}">GitHub</a> is authoritative
  for both. Nothing here is an endorsement, and nothing here has been run.
</div></footer>
<script src="../../detail.js"></script>
{b19.beacon()}</body>
</html>
"""


# ------------------------------------------------------------------ the directory
def directory(repos: list[Repo], data: dict) -> str:
    """`docs/repo/index.html`: all 1,294, grouped by topic.

    Without it every detail page is an orphan. The index at the site root renders its rows from
    `data.json` in the browser, which is the entire reason `20_landing.py` exists -- a crawler receives
    that page with an empty table -- and the facet pages cap at 100 rows, so between them they leave
    over a thousand of these pages reachable only from a sitemap. A sitemap is a hint. This is a path,
    it puts every page one hop from something crawlable, and because it carries names and nothing else
    it is as stable as the pages it links to.

    Alphabetical within each topic rather than by stars, for the reason `kin()` gives: an ordering that
    depends on a star count is an ordering that rewrites this file every night.
    """
    cats = data["cats"]
    by_cat: dict[int, list[Repo]] = {i: [] for i in range(len(cats))}
    for r in repos:
        by_cat[r.row["cat"]].append(r)

    blocks = []
    for i, cat in enumerate(cats):
        group = sorted(by_cat[i], key=lambda r: r.name.lower())
        if not group:
            continue
        links = "".join(f'<li><a href="{"/".join(r.parts[1:])}/">{esc(r.name)}</a></li>'
                        for r in group)
        blocks.append(f'<section><h2 id="{esc(cat["slug"])}">{esc(cat["name"])} '
                      f'<span class="ct">{len(group):,}</span></h2>'
                      f'<p class="lead">{esc(cat["blurb"])}</p>'
                      f'<ul class="dir">{links}</ul>'
                      f'<p class="more"><a href="../topic/{esc(cat["slug"])}/">'
                      f'{esc(cat["name"])} ranked by stars &rarr;</a></p></section>')

    jump = " · ".join(f'<a href="#{esc(c["slug"])}">{esc(c["name"])}</a>'
                      for i, c in enumerate(cats) if by_cat[i])
    url = SITE + "repo/"
    return f"""<!doctype html>
<html lang="en" data-theme="dark" data-root="../">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Every project in the atlas, A–Z by topic — Awesome Agentic Atlas</title>
<meta name="description" content="{len(repos):,} agentic AI projects from {b19.LISTS} awesome-lists, each with a page of its own: install command, platform support and provenance.">
<link rel="canonical" href="{esc(url)}">
<meta property="og:type" content="website">
<meta property="og:title" content="Every project in the Awesome Agentic Atlas">
<meta property="og:description" content="{len(repos):,} projects, one page each.">
<meta property="og:url" content="{esc(url)}">
<meta property="og:image" content="https://opengraph.githubassets.com/1/{esc(REPO)}">
<link rel="icon" href="{ICON}">
{HEAD_THEME}<link rel="stylesheet" href="detail.css">
</head>
<body>
<header><div class="wrap">
  <nav class="crumb"><a href="../">Atlas</a> › All projects</nav>
  <div class="top">
    <div>
      <h1>Every project, by topic</h1>
      <p class="lead">All <b>{len(repos):,}</b> projects the atlas merges, each with a page carrying its
        install command, its five platform verdicts and which of the {b19.LISTS} lists named it. Grouped by
        topic and alphabetical inside it — the star rankings are on the
        <a href="../">interactive index</a> and the {len(cats)} topic pages.</p>
      <p class="jump">{jump}</p>
    </div>
    <nav class="util">
      <button class="chip" id="theme" aria-pressed="false">Light theme</button>
    </nav>
  </div>
</div></header>
<main><div class="wrap">{"".join(blocks)}</div></main>
<footer><div class="wrap">
  A directory of the <a href="../">Awesome Agentic Atlas</a>. Every name here links to a page about one
  project; all {b19.LISTS} source lists are credited in the
  <a href="https://github.com/{esc(REPO)}#the-source-lists">repository</a>.
</div></footer>
<script src="detail.js"></script>
{b19.beacon()}</body>
</html>
"""


# ------------------------------------------------------------------ sitemap
def sitemap(repos: list[Repo]) -> str:
    """Sitemap 0.9, the directory first, and no `lastmod` -- see the module docstring.

    A second file rather than an addition to `sitemap.xml`, which `20_landing.py` writes. Two stages
    writing one file is how a sitemap loses whichever half ran first, and the split is also how the
    standard expects a set this size to be organised.

    No `changefreq` and no `priority`: Google ignores both, and a number invented for 1,295 pages is
    noise in a file whose whole value is that everything in it is checkable.
    """
    locs = [SITE + "repo/"] + [r.url for r in repos]
    body = "\n".join(f"  <url><loc>{esc(u)}</loc></url>" for u in locs)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{body}\n</urlset>\n")


# ------------------------------------------------------------------ writing
def prune(base: Path, keep: set[Path]) -> list[Path]:
    """Delete detail pages this run did not write, then the directories they emptied.

    Overwriting in place makes a rerun idempotent for pages that still exist and does nothing about the
    ones that stopped existing. A repository that was renamed upstream, or dropped from the last list
    that named it, would otherwise leave a page that is still served, still claiming a canonical URL,
    and no longer in any sitemap -- indexed, stale, and invisible to every later run. Only `index.html`
    files under `docs/repo/` and the directories that held them are touched.
    """
    gone = []
    if not base.exists():
        return gone
    for path in sorted(base.rglob("index.html")):
        if path.resolve() not in keep:
            path.unlink()
            gone.append(path)
    # Deepest first, so a repository directory is gone before its owner directory is examined.
    for d in sorted((p for p in base.rglob("*") if p.is_dir()),
                    key=lambda p: len(p.parts), reverse=True):
        if not any(d.iterdir()):
            d.rmdir()
    return gone


def kb(n: int) -> str:
    return f"{n / 1024:,.1f} KB" if n < 1024 * 1024 else f"{n / 1048576:,.2f} MB"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    # `--out` exists so the drift of this stage can be measured without touching the committed tree:
    # generate into a scratch directory from a perturbed copy of the dataset, diff the two trees, and
    # you have the number of pages a rebuild would actually rewrite. That number is the whole argument
    # for the design above, and a claim about repository growth that cannot be re-measured on demand is
    # a claim that will be wrong within a month.
    ap.add_argument("--out", default=str(ROOT / "docs"), metavar="DIR",
                    help="write into DIR instead of docs/ (for measuring, not for deploying)")
    ap.add_argument("--data", default=None, metavar="FILE",
                    help="read this data.json instead of DIR/data.json")
    args = ap.parse_args()

    out = Path(args.out).resolve()
    src = Path(args.data).resolve() if args.data else out / "data.json"
    data = json.loads(src.read_text(encoding="utf-8"))

    repos, by_cat = plan(data, out)
    lists = source_links()
    unresolved = sorted({n.strip() for r in repos for n in r.row["listed_by"].split(",")
                         if n.strip() and n.strip() not in lists})

    total = 0
    for repo in repos:
        repo.path.parent.mkdir(parents=True, exist_ok=True)
        repo.path.write_text(render(repo, by_cat, lists, data), encoding="utf-8")
        total += repo.path.stat().st_size

    base = out / "repo"
    base.mkdir(parents=True, exist_ok=True)
    (base / "index.html").write_text(directory(repos, data), encoding="utf-8")
    (base / "detail.css").write_text(CSS, encoding="utf-8")
    (base / "detail.js").write_text(JS, encoding="utf-8")
    (out / "sitemap-repos.xml").write_text(sitemap(repos), encoding="utf-8")

    gone = prune(base, {r.path.resolve() for r in repos} | {(base / "index.html").resolve()})

    shell = sum((base / f).stat().st_size for f in ("index.html", "detail.css", "detail.js"))
    shell += (out / "sitemap-repos.xml").stat().st_size
    print(f"{len(repos):,} detail pages · {kb(total)} · {kb(total / len(repos))} each")
    print(f"repo/index.html + detail.css + detail.js + sitemap-repos.xml · {kb(shell)} · "
          f"{len(repos) + 1:,} URLs, no lastmod")
    print(f"{kb(total + shell)} written under {out.name}/ · no star count, push date or snapshot "
          "date in any of it")
    if gone:
        print(f"{len(gone)} stale page(s) removed: "
              + ", ".join(str(p.relative_to(base)) for p in gone[:5]))
    if unresolved:
        print("source lists with no repository to link to, rendered as plain text: "
              + ", ".join(unresolved))
    print("docs/robots.txt needs a second line: Sitemap: " + SITE + "sitemap-repos.xml")


# ------------------------------------------------------------------ the shared shell
# One stylesheet for 1,295 pages rather than 1,295 inlined copies. The shell is ~7 KB; inlining it would
# add ~9 MB to the repository to save one cached request, and every byte of that 9 MB would be
# re-committed the next time a colour changed.
#
# `19_pages.py`'s two custom-property blocks are copied in verbatim rather than imported, because that
# template is one 25 KB string with the whole interactive page in it and there is no seam to import.
# Everything after them is this surface's own layout: a detail page is a document, not a table, so it
# shares the theme and none of the grid.
CSS = """/* Written by scripts/22_detail.py. Shared by every page under docs/repo/.

   Deliberately not docs/pages.css, which scripts/20_landing.py writes: two stages writing one file
   means the later run silently deletes the earlier one's rules.

   The two blocks below are 19_pages.py's, character for character. Lagoon Gold: cyan primary, gold
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
  font:15px/1.6 "Segoe UI",system-ui,-apple-system,Helvetica,Arial,sans-serif}
a{color:var(--link);text-decoration:none}
a:hover{text-decoration:underline}
button{font:inherit;cursor:pointer}
header{background:var(--plane);border-bottom:1px solid var(--grid);padding:18px 20px 22px}
/* Narrower than the 1500px the table surfaces use. This one is prose, and a 44-character-per-line
   measure is what a blurb and a licence sentence want; 1500px would set the lead paragraph 180
   characters wide, which is unreadable for the one thing on the page a reader has to read. */
.wrap{max-width:1000px;margin:0 auto}
main{padding:0 20px 64px}
footer{border-top:1px solid var(--grid);background:var(--plane);padding:22px 20px;
  color:var(--muted);font-size:13px}
h1{margin:0 0 4px;font-size:30px;letter-spacing:-.02em;overflow-wrap:anywhere}
h2{margin:0 0 10px;font-size:15px;text-transform:uppercase;letter-spacing:.07em;color:var(--muted)}
.crumb{font-size:13px;color:var(--muted);margin-bottom:14px}
.top{display:flex;justify-content:space-between;align-items:flex-start;gap:20px;flex-wrap:wrap}
.top>div{min-width:0}
/* word-break rather than overflow-wrap, because an owner/name pair breaks nowhere: a slash is not a
   break opportunity in Chrome or Safari, so a 52-character nwo would otherwise widen the document. */
.nwo{margin:0 0 12px;color:var(--muted);font-size:13px;word-break:break-all}
.lead{margin:0 0 14px;color:var(--ink2);font-size:16px;max-width:68ch}
.lead.none,.none{color:var(--muted);font-style:italic}
/* Each fact its own element rather than text separated by dots, so that when the row wraps on a phone
   the separator never ends up orphaned at the start of a line. */
.facts{display:flex;flex-wrap:wrap;gap:6px 18px;margin:0 0 18px;font-size:13px;color:var(--muted)}
.facts span{white-space:nowrap}
/* The live pair starts hidden and detail.js reveals it once live.json has answered. Hidden rather than
   showing a placeholder, because "Stars —" that never fills in reads as a broken page, whereas a fact
   that simply is not there reads as a fact that is not there. */
.facts .live{display:none}
.facts .live.on{display:inline;color:var(--ink2)}
.facts .live b{color:var(--ink);font-variant-numeric:tabular-nums}
.acts{display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center;margin:0}
/* The one link that has to be found. Filled with the accent, which is why it needs --onbar for ink. */
.cta{display:inline-block;background:var(--bar);color:var(--onbar);font-weight:600;
  border-radius:8px;padding:10px 18px}
.cta:hover{text-decoration:none;filter:brightness(1.08)}
.alt{font-size:14px}
.chip{display:inline-block;background:var(--band);color:var(--ink2);border:1px solid var(--grid);
  border-radius:999px;padding:5px 12px;font-size:13px;white-space:nowrap;margin:0 5px 5px 0}
.chip:hover{border-color:var(--bar);color:var(--ink);text-decoration:none}
.chip.cat{border-color:var(--bar);color:var(--ink)}
.chips{margin-top:2px}
.util{flex-shrink:0}
section{margin:34px 0 0;border-top:1px solid var(--grid);padding-top:22px}
/* The install command, and the button that takes it away. Selecting wrapped monospace text without
   catching the paragraph above it is the thing this replaces. */
.cmdrow{display:flex;gap:10px;align-items:flex-start}
.cmd{flex:1;min-width:0;font:13.5px/1.6 Consolas,ui-monospace,monospace;color:var(--ink);
  background:var(--band);border:1px solid var(--grid);border-radius:6px;padding:10px 12px;
  overflow-wrap:anywhere;display:block}
.copy{background:var(--band);color:var(--ink2);border:1px solid var(--grid);border-radius:6px;
  padding:10px 14px;font-size:13px;white-space:nowrap}
.copy:hover{border-color:var(--bar);color:var(--ink)}
figure.shot{margin:0}
/* A fixed 2:1 box with the image contained inside it. The src is somebody else's CDN and its
   dimensions are unknown at build time, so height cannot be declared on the img -- and without a box
   the whole page below would jump when it finally arrives. `contain` rather than `cover` because these
   are arbitrary images: cropping a social card to fill a frame cuts the repository name off it. */
.shot img{width:100%;aspect-ratio:2/1;object-fit:contain;border-radius:10px;background:var(--band);
  border:1px solid var(--grid);display:block}
figcaption{color:var(--muted);font-size:12.5px;margin-top:8px;max-width:70ch}
table.os{width:100%;border-collapse:collapse;font-size:14px}
table.os caption{text-align:left;color:var(--muted);font-size:12.5px;margin-bottom:10px;
  max-width:70ch}
table.os th[scope=col]{text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.07em;
  color:var(--muted);padding:8px 10px;border-bottom:1px solid var(--grid);font-weight:600}
table.os th[scope=row]{text-align:left;padding:10px;border-bottom:1px solid var(--grid);
  font-weight:600;white-space:nowrap}
table.os td{padding:10px;border-bottom:1px solid var(--grid);vertical-align:top}
table.os .why{color:var(--ink2);font-size:13px}
/* Prefixed, on the same reasoning as 20_landing.py's .vY: a class name has to be a valid CSS
   identifier, and these are tone names rather than the verdict characters for exactly that reason. */
.vgood{color:var(--good);font-weight:700;white-space:nowrap}
.vwarn{color:var(--warn);white-space:nowrap}
.voff{color:var(--off);white-space:nowrap}
ul.lists{list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:8px}
ul.lists li{background:var(--band);border:1px solid var(--grid);border-radius:6px;padding:6px 12px;
  font-size:13.5px}
/* Two columns of cards on a desktop, one on a phone, without a media query: auto-fill collapses to a
   single track as soon as 320px stops fitting twice. */
ul.kinlist{list-style:none;padding:0;margin:0;display:grid;gap:10px;
  grid-template-columns:repeat(auto-fill,minmax(320px,1fr))}
ul.kinlist li{border:1px solid var(--grid);border-radius:10px;padding:12px 14px;background:var(--plane)}
ul.kinlist a{font-weight:600;overflow-wrap:anywhere}
ul.kinlist .nwo{display:block;margin:2px 0 0;font-size:12px}
ul.kinlist .desc{display:block;color:var(--ink2);font-size:13px;margin-top:6px}
/* The directory page. Three or four columns of names, which is the only layout in which 1,294 links
   are scannable rather than a mile of scrolling. */
ul.dir{list-style:none;padding:0;margin:0;columns:4 220px;column-gap:26px;font-size:13.5px}
ul.dir li{margin:0 0 5px;break-inside:avoid;overflow-wrap:anywhere}
.ct{color:var(--muted);font-weight:400}
.jump{font-size:13px;color:var(--muted);line-height:2;margin:14px 0 0}
.more{margin:14px 0 0;font-size:13.5px}
@media(max-width:640px){
  header{padding:14px 14px 18px}
  main{padding:0 14px 48px}
  footer{padding:18px 14px}
  h1{font-size:23px}
  .lead{font-size:15px}
  section{margin-top:26px;padding-top:18px}
  /* The button under the command rather than beside it. At 335px a flex row leaves the code element
     about 210px, which wraps a 145-character npm line into nine lines. */
  .cmdrow{flex-direction:column}
  .copy{align-self:flex-start}
  .cta{flex:1;text-align:center}
  /* Four columns of names in 307px is 77px a column. One column, and let it scroll. */
  ul.dir{columns:1}
  /* The evidence sentence is the first thing to go: three columns do not fit, and the verdict word
     without its reason is still the answer to "does this run on my machine". The reason stays in the
     document for a reader who asks for the desktop site, and it is never the only place a fact is. */
  table.os .why,table.os th[scope=col]:last-child{display:none}
}
"""

# The browser chrome, and the half of the theme that has to be settled before the first pixel.
#
# This one *is* inlined into all 1,295 pages, against the argument the stylesheet and the script above
# make, and the exception is the whole reason it exists: it has to have finished before first paint, and
# `detail.js` is a separate request that by definition has not. A reader who chose light would otherwise
# get a frame of near-black on every page they open -- the flash the inline form prevents. It is ~700
# bytes x 1,295, and unlike the star count it is a constant, so it is committed once and never rewritten
# by a rebuild; the churn argument in the module docstring is about volatile *values*, not about size.
#
# Copied out of `19_pages.py`'s head rather than shared with it, on the same argument the two palette
# blocks in `CSS` above are copied: that template is one 25 KB string and there is no seam to import.
#
# One `theme-color`, written by script, rather than the two `media` variants that would be the obvious way
# to do it: the HTML spec picks the *first* such element whose media matches, so a pair keyed on
# `prefers-color-scheme` cannot be overridden by anything appended later -- and these pages now honour a
# choice made *against* the OS preference, so the pair would paint the chrome the opposite colour to the
# page for exactly the readers who made one. The value is `--plane` in dark, because `--plane` is the
# header's background and the header is what sits under the chrome. It is a literal because `detail.css`
# has not been fetched, let alone parsed, at the moment the script below runs; with JavaScript off it
# stays this value, which agrees with the `data-theme="dark"` floor on <html>.
#
# Precedence is explicit choice, then the operating system, then dark. Dark stays the fallback because it
# is the designed mode -- the one whose accent contrast ratios were actually measured. The markup's
# `data-theme="dark"` is the floor if this throws, which `localStorage` does in some private modes. The
# key is `theme`, the same string the index writes, so a choice made on the index is honoured here
# immediately and there is nothing to migrate.
HEAD_THEME = """<meta name="theme-color" id="tc" content="#181f21">
<script>
try {
  var t = localStorage.getItem("theme");
  if (t !== "light" && t !== "dark")
    t = matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
  document.documentElement.dataset.theme = t;
  // The two literals track --plane in the two blocks at the top of detail.css. Once detail.js has run it
  // re-derives this from the computed value so the stylesheet stays the single source of truth; here
  // there is no computed value to read yet, and a chrome one shade out for one frame is the cost of not
  // blocking the paint on a stylesheet.
  document.getElementById("tc").content = t === "light" ? "#eef1f2" : "#181f21";
} catch (e) {}
</script>
"""

# One script for 1,295 pages, for the same reason as the stylesheet: ~1 KB inlined 1,295 times is 1.3 MB
# of repository that gets rewritten whenever a line of it changes.
JS = """/* Written by scripts/22_detail.py. Shared by every page under docs/repo/.

   Three jobs, none of which the page needs in order to be complete: the theme toggle, the copy button,
   and the two figures that are deliberately not in the HTML. */
"use strict";

/* Not a data fetch and not a framework: the light half of the theme is in detail.css and without a
   switch nothing on these pages can ever reach it.

   Three pieces, ported from `wire()` in 19_pages.py, because the toggle used to change nothing beyond
   this tab's current document: the write on click, so the choice survives the next link; the agreement
   with the head script on load; and the listener, so a reader who has expressed no choice follows their
   OS the way the index does. The *read* is not here -- it is inline in every page's <head>, because by
   the time this file has been fetched and run the wrong theme has already been painted.

   label() is folded into every path that changes the theme, which is the index's arrangement and for its
   reasons: the button's markup says "Light theme" and aria-pressed="false", which is wrong for every
   reader the head script just resolved to light, and --plane is read off the stylesheet rather than
   restated here so the browser chrome cannot drift from the page. There is a computed value to read by
   now -- detail.css is a render-blocking link in the head, so it is parsed before this runs. The meta is
   looked up defensively: this file is one shared request, and a page that ever ships without the head
   block should lose the chrome colour, not the copy button and the two figures below. */
var toggle = document.getElementById("theme");
if (toggle) {
  var label = function () {
    var light = document.documentElement.dataset.theme === "light";
    toggle.textContent = light ? "Dark theme" : "Light theme";
    toggle.setAttribute("aria-pressed", light ? "true" : "false");
    var tc = document.getElementById("tc");
    var plane = getComputedStyle(document.documentElement).getPropertyValue("--plane").trim();
    if (tc && plane) tc.content = plane;
  };
  toggle.onclick = function () {
    var light = document.documentElement.dataset.theme !== "light";
    document.documentElement.dataset.theme = light ? "light" : "dark";
    /* The choice is the point: it used to last until the next navigation, so a reader who needs light
       re-picked it on every one of these 1,295 pages and again on every trip back to the atlas. */
    try { localStorage.setItem("theme", light ? "light" : "dark"); } catch (e) {}
    label();
  };
  label();
  /* Follow the OS live, but only for a reader who has not overridden it -- flipping someone out of a
     theme they explicitly chose because the sun went down is worse than not following at all. */
  try {
    matchMedia("(prefers-color-scheme: light)").addEventListener("change", function (ev) {
      if (localStorage.getItem("theme")) return;
      document.documentElement.dataset.theme = ev.matches ? "light" : "dark";
      label();
    });
  } catch (e) {}
}

/* Feature-detected rather than assumed, and the button stays hidden when the answer is no -- a button
   that fails on click is worse than no button. isSecureContext is part of the test because the API
   exists but always rejects on plain http, which is how anyone serving docs/ locally sees it. */
var copy = document.querySelector(".copy");
if (copy && navigator.clipboard && navigator.clipboard.writeText && window.isSecureContext) {
  copy.hidden = false;
  copy.onclick = function () {
    var cmd = document.getElementById(copy.dataset.for);
    navigator.clipboard.writeText(cmd.textContent).then(function () {
      copy.textContent = "Copied";
      setTimeout(function () { copy.textContent = "Copy"; }, 1400);
    });
  };
}

/* The star count and the last push.

   These are the only two facts on the page that change daily, and they are read from a file here
   instead of being written into the HTML by the generator. docs/ is committed verbatim on this
   deployment, so a star count in the markup means all 1,294 pages are rewritten in git every time the
   cron runs.

   The file is docs/live.json, written by scripts/19c_live.py:

     {"snapshot": "<date>", "repos": {"<owner>/<name>": [stars, "<pushed>"]}}

   which is these three values for every repository and nothing else -- 21.8 KB gzipped. Until JFH-222
   this fetched docs/data.json, all eighteen columns of all 1,294 rows at 162.5 KB gzipped, and then
   scanned it for one row. Same two numbers, 7.5x fewer bytes, and an object lookup instead of a linear
   search through 1,294 arrays.

   Failure is silent by design. The three spans are hidden until this succeeds, so a 404, an offline
   reader or a parse error leaves a page that is missing two figures rather than a page with a broken
   promise on it -- and every other fact on it was in the initial response. */
var root = document.documentElement.dataset.root || "";
var nwo = document.documentElement.dataset.nwo;
if (nwo && window.fetch) {
  fetch(root + "live.json").then(function (r) {
    return r.ok ? r.json() : Promise.reject(r.status);
  }).then(function (d) {
    /* Array.isArray rather than a truth test. Every nwo contains a slash, so none of them can name an
       inherited property of Object.prototype and a plain lookup is in fact safe -- but a check that is
       exact rather than merely sufficient costs nothing, and this one also declines a sidecar whose
       shape has changed underneath the page instead of rendering "undefined stars". */
    var row = d.repos && d.repos[nwo];
    if (!Array.isArray(row)) return;
    show("stars", row[0] ? "<b>" + row[0].toLocaleString() + "</b> stars" : "No stars recorded");
    if (row[1]) show("pushed", "last push <b>" + row[1] + "</b>");
    /* The snapshot the two figures above belong to. It is the single most volatile string in the
       dataset -- it changes on every run without exception -- so one copy of it per page would be
       1,294 rewritten files for one date, and it is also the qualifier without which the two numbers
       beside it are being presented as live when they are not. */
    if (d.snapshot) show("snap", "snapshot " + d.snapshot);
  }).catch(function () {});
}

function show(id, html) {
  var el = document.getElementById(id);
  if (!el) return;
  el.innerHTML = html;
  el.className = "live on";
}
"""

# Copied from the template so a detail page in a bookmark bar looks like the site.
ICON = ("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'>"
        "<text y='13' font-size='14'>&#127760;</text></svg>")


if __name__ == "__main__":
    main()
