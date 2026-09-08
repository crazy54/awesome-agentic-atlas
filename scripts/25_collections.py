"""Render the curated collections: the one part of this site that is an opinion.

Everything else here is a merge. `17_markdown.py`, `19_pages.py`, `20_landing.py` and `22_detail.py` all
answer "what did eleven awesome-lists agree on", and the ranking is stars because stars are a number
somebody else maintains. That is the right posture for an index and it is useless to a reader whose
question is "which one should I install". 1,294 projects sorted by popularity is not an answer to that.

So these pages answer it. Five sets, seven picks each, one project per slot -- an agent, the thing it
loads, the place it runs, the tool that tells you afterwards what it did. The opinions live in
`config/collections.json` so they are reviewable in a diff, and every one of them is checked against the
committed dataset before a page is written.

  docs/collections/index.html            the hub
  docs/collections/<slug>/index.html      one per collection
  mega-list/collections/<slug>.md         the Markdown twin, same picks, same prose
  mega-list/collections/README.md         its index

  python scripts/25_collections.py
  python scripts/24_pwa.py                 re-version the worker, or returning readers miss it

Four decisions worth stating.

The build fails rather than publishes a stale recommendation. A pick names a repository by `nwo`, and a
repository can be renamed, removed from every source list, or -- the interesting case -- keep existing
while the claim about it stops being true. "Runs on Windows, and says so" is a page whose entire value is
that the verdict is `Y` and not `L`; if one of its seven drops to inferred, the honest outcome is a red
build and a curator's decision, not a page that quietly means something weaker. `requires` in the JSON is
how a collection declares the claim its prose is making, and `check()` below enforces it.

Every pick carries its evidence beside the prose. The `why` line is a judgement and is presented as one;
under it the page prints the star count, how many of the source lists agreed, the licence, the language,
the last push and the five platform verdicts, all from `data.json`. A reader who disagrees with the
judgement can see exactly what it was made from, which is the only form of "trust us" worth offering. The
verdicts are drawn as the marks `scripts/osicons.py` owns, each carrying its platform's name in a `title`
and in a visually-hidden span, while the Markdown twins below keep the words -- GitHub strips `<svg>` from
rendered Markdown, so a mark there is not a smaller label, it is nothing at all.

The set is exportable as a set. Each page links to the atlas with `#list=` carrying its seven `nwo`s,
which is the share format `19_pages.py` reads: one click puts the collection in the interactive view,
where the Export dialog turns it into Markdown, a standalone HTML page, a PDF, or the reader's own saved
projects. The collection is a starting point for somebody's list rather than a destination.

It reads `docs/data.json` and nothing else -- no build cache, no network -- so a clone with nothing
fetched can rebuild every page here, the same property `19b_refresh.py` and `20_landing.py` have.
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUT = ROOT / "docs"
MD = ROOT / "mega-list" / "collections"
CURATION = ROOT / "config" / "collections.json"

# The same dynamic load the other stages use, and for the same reason: `19_pages` and `20_landing` are not
# identifiers. Both do their work under `if __name__`, so importing them runs no build.
#
# What is taken from each is the part that must not be spelled twice. From `19_pages.py`: the site URL, the
# repository, the count of merged lists that goes in the footer, and the analytics beacon. From
# `20_landing.py`: `esc`, `clip`, `repo_path` -- the rule that turns an `nwo` into a detail-page path -- and
# the two theme scripts, so a reader following a link from a facet page to a collection page sees the same
# palette resolved by the same code before first paint. Nothing here has its own copy of any of that.
def _load(name: str, alias: str):
    # Reuse an already-loaded copy. Both stages here load `19_pages.py`, and `20_landing.py` loads this
    # module in turn to ask it for its URLs -- so without this the same file gets executed twice in one
    # process under two module objects, which is wasteful and, for anything that ever caches at module
    # level, wrong.
    if alias in sys.modules:
        return sys.modules[alias]
    spec = importlib.util.spec_from_file_location(alias, HERE / name)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[alias] = mod
    spec.loader.exec_module(mod)
    return mod


b19 = _load("19_pages.py", "b19")
b20 = _load("20_landing.py", "b20")
# And `22_detail.py`, for the one thing it owns: the prose behind each verdict character. The five platform
# verdicts on a pick are marks rather than words now, so the sentence that was implicit in the word has to
# be somewhere a reader can reach -- and the only honest place to take it from is the surface whose job is
# to write it out in full. Free: `20_landing.py` has already loaded this module for `segment()`, so `_load`
# hands back the cached one. Imported rather than retyped so a hover here and the platform table there
# cannot end up describing the same evidence differently.
b22 = _load("22_detail.py", "b22")

# `19_pages.py` above has already put `scripts/` on the path for its own plain-named siblings, and the
# comment over that line says exactly why it is not something to lean on: relying on it as a side effect of
# somebody else's import is how this breaks the day the import order changes. Stated here for that reason.
# `osicons` is an identifier, so it needs none of the machinery above.
sys.path.insert(0, str(HERE))
import osicons  # noqa: E402

SITE = b19.b17.SITE
REPO = b19.REPO
esc, clip, repo_path = b20.esc, b20.clip, b20.repo_path
ICON, HEAD_THEME, THEME_JS = b20.ICON, b20.HEAD_THEME, b20.THEME_JS
# `{"Y": ("Yes", "good", "Stated in the project's own README, ...")}`, keyed by verdict character.
VERDICT = b22.VERDICT

# How many picks a collection may have. The floor is what makes it a set rather than a recommendation, and
# the ceiling is what keeps it from becoming another list -- which is the thing the whole site already is.
MIN_PICKS, MAX_PICKS = 5, 8

# A download piped straight into a shell. Not a judgement about the projects that ship one -- it is the
# normal way to install a Go binary -- but a page that hands somebody seven commands to paste owes them
# the count of how many of them execute a remote script without showing it to them first. Deliberately
# narrow: a fetch on one side of a pipe and a shell on the other, so a command that merely contains the
# word `bash` does not get counted.
#
# The PowerShell aliases are here because leaving them out was a live bug rather than a hypothetical one.
# The first version listed only the Unix fetchers, and two of the five pages went out saying "none of this
# set pipes a download into a shell" over a pick whose command was `irm https://.../install.ps1 | iex` --
# the same hazard, one letter of alias away from being counted. `irm`/`iwr` are the aliases people actually
# paste; the full cmdlet names are here so a command written out in full is caught too.
PIPED = re.compile(r"\b(?:curl|wget|fetch|irm|iwr|Invoke-RestMethod|Invoke-WebRequest)\b"
                   r"[^|]*\|[^|]*\b(?:sh|bash|zsh|fish|iex|Invoke-Expression|python3?|node)\b", re.I)


class CurationError(Exception):
    """A curation that cannot be published. Raised rather than warned about: see the module docstring."""


def merged_lists(data: dict) -> int:
    """How many source lists the rows on this page actually came from.

    Deliberately not `b19.LISTS`, which is `len(SOURCES)` -- the number of lists configured today, 39.
    The committed dataset predates that expansion and its rows carry 11 distinct `listed_by` labels, so
    on this data the two numbers are different facts and only one of them belongs here: every pick prints
    "N of M lists" beside it, `N` counts agreement among the lists that contributed, and with 39 as the
    denominator that sentence is false about its own row. This is the same derivation
    `apply_flags.render_index()` uses for the same reason, and the number the index shows.
    """
    k = data["cols"].index("listed_by")
    return len({name.strip() for row in data["rows"] for name in row[k].split(",") if name.strip()})


# ------------------------------------------------------------------ the data
def load_rows(data: dict) -> dict[str, dict]:
    """Every project in the atlas, by `nwo`, as objects rather than the column arrays on disk."""
    rows = {}
    for raw in data["rows"]:
        r = dict(zip(data["cols"], raw))
        r["cat_name"] = data["cats"][r["cat"]]["name"]
        r["cat_slug"] = data["cats"][r["cat"]]["slug"]
        r["target_names"] = [data["targets"][t]["name"] for t in r["targets"]]
        r["target_slugs"] = [data["targets"][t]["slug"] for t in r["targets"]]
        rows[r["nwo"]] = r
    return rows


def check(coll: dict, picks: list[dict], data: dict) -> None:
    """Everything that would make this collection a lie, checked before it is written.

    Ordered cheapest-first only incidentally; what matters is that each of these has a distinct failure
    mode and none of them is a style rule.
    """
    slug, n = coll["slug"], len(picks)
    if not MIN_PICKS <= n <= MAX_PICKS:
        raise CurationError(f"{slug}: {n} picks, wanted {MIN_PICKS}-{MAX_PICKS}")
    # Two picks in the same slot means the set has stopped being a set -- the reader is back to choosing,
    # which is the work these pages exist to have already done. Compared case-insensitively, because "The
    # agent" and "The Agent" are the same slot and a curator editing one of them should not be able to
    # create a second by accident; reported as written, because that is the string to search the file for.
    roles = [p["role"].strip().lower() for p in picks]
    if len(set(roles)) != len(roles):
        dupe = next(r for r in roles if roles.count(r) > 1)
        wrote = next(p["role"] for p in picks if p["role"].strip().lower() == dupe)
        raise CurationError(f"{slug}: two picks fill the same slot ({wrote!r})")
    if len({p["nwo"] for p in picks}) != n:
        raise CurationError(f"{slug}: the same project is picked twice")
    for p in picks:
        if len(p["why"].split()) < 12:
            raise CurationError(f"{slug}: {p['nwo']} has no real reason written for it")

    req = coll.get("requires") or {}
    for key, want in req.items():
        if key == "os":
            if want not in data["os"]:
                raise CurationError(f"{slug}: requires os {want!r}, which is not a platform in the data")
            k = data["os"].index(want)
            # `Y` and not `L`: stated support, not support inferred from the language. That distinction is
            # the entire claim of the page that uses this, so an inferred verdict fails here.
            bad = [p["nwo"] for p in picks if (p["row"]["os"][k:k + 1] or "-") != "Y"]
            if bad:
                raise CurationError(
                    f"{slug}: claims stated {want} support, but the snapshot no longer says so for "
                    + ", ".join(bad) + " -- re-pick, or drop the requirement and rewrite the intro")
        elif key == "target":
            slugs = {t["slug"] for t in data["targets"]}
            if want not in slugs:
                raise CurationError(f"{slug}: requires target {want!r}, which is not in the data")
            bad = [p["nwo"] for p in picks if want not in p["row"]["target_slugs"]]
            if bad:
                raise CurationError(
                    f"{slug}: claims every pick targets {want}, but the snapshot disagrees for "
                    + ", ".join(bad))
        else:
            raise CurationError(f"{slug}: unknown requirement {key!r}")


def plan(data: dict, curation: dict | None = None) -> list[dict]:
    """Resolve the curation against the dataset. Every consumer calls this and gets the same list.

    Three of them do: the renderer, the Markdown twin, and `20_landing.py`, which puts these URLs in
    `sitemap.xml`. That last one is why this is a plain function of two JSON files and touches no disk
    beyond reading them -- a sitemap entry for a page that was never written is the one failure a separate
    list of "which pages exist" always eventually produces.
    """
    curation = curation or json.loads(CURATION.read_text(encoding="utf-8"))
    rows = load_rows(data)
    out, seen = [], set()
    for coll in curation["collections"]:
        slug = coll["slug"]
        if slug in seen:
            raise CurationError(f"two collections share the slug {slug!r}")
        seen.add(slug)
        picks = []
        for p in coll["picks"]:
            row = rows.get(p["nwo"])
            if row is None:
                # The common case, and the reason this is fatal: a repository that was renamed or dropped
                # from every source list is no longer in `data.json`, and a page recommending it would link
                # to a detail page that this build also did not write.
                raise CurationError(
                    f"{slug}: {p['nwo']} is not in the atlas -- renamed, or no longer on any source list")
            picks.append(dict(p, row=row))
        check(coll, picks, data)
        out.append(dict(coll, picks=picks, path=["collections", slug]))
    return out


def urls(data: dict, curation: dict | None = None) -> list[str]:
    """Every URL this stage publishes, hub first. Imported by `20_landing.py` for the sitemap."""
    return [SITE + "collections/"] + [SITE + "collections/" + c["slug"] + "/"
                                      for c in plan(data, curation)]


# ------------------------------------------------------------------ shared bits of markup
def share_hash(coll: dict) -> str:
    """The atlas link that carries the whole set: `#list=owner/name,owner/name`.

    Unescaped slashes and commas, matching `writeHash()` in `19_pages.py` -- both are legal unescaped in a
    fragment, and `%2F` six times over in a link somebody is about to click is not readable enough to
    trust. Ordering is the curation's, so the interactive view arrives in the order the page was read in.
    """
    return "#list=" + ",".join(p["nwo"] for p in coll["picks"])


def verdicts(row: dict, os_labels: list[str]) -> str:
    """The five platform verdicts, same classes as every other surface, drawn as marks instead of words.

    The word does not go away, it moves. Each mark carries the platform's name and the sentence behind its
    verdict in a `title`, so hovering still answers "does this run on my machine", and the name again in a
    visually-hidden span, so a screen reader still hears which platform each verdict belongs to -- it heard
    "Win" here before and now hears "Windows", which is the one part of this change that is strictly a gain.
    A mark is a shorthand for people who can see it and nothing at all to anyone else; see
    `scripts/osicons.py`'s docstring, which owns that rule and the geometry.

    The hover is `platform: what the verdict means`, which is the shape the index's own tooltip uses, with
    `22_detail.py`'s sentence in it rather than a sixth paraphrase of the same evidence. Indexed and not
    `.get`: the five characters come from `19_pages.VERDICT`, and a sixth would mean the wire format changed
    under this page, which is a build to stop rather than a mark to guess the meaning of.
    """
    out = []
    for k, o in enumerate(os_labels):
        v = row["os"][k:k + 1] or "-"
        _word, _tone, why = VERDICT[v]
        hover = f"{osicons.title(k)}: {why}"
        out.append(f'<span class="v{esc(v)}" title="{esc(hover)}">'
                   f'{osicons.use(k)}<span class="sr">{esc(o)}</span></span>')
    return " ".join(out)


def rel(depth: int, tail: str = "") -> str:
    """A link out of a page `depth` directories below `docs/`, relative so the tree serves from either
    a local `python -m http.server` in `docs/` or the Pages subpath unchanged."""
    return "../" * depth + tail


def head(title: str, desc: str, url: str, depth: int, ld: str = "") -> str:
    """The <head> every page here shares, including the pre-paint theme resolution.

    No collection-specific `og:image`: `23_og.py` renders cards for the 26 facets, and inventing a
    seventh kind of card is a bigger change than these five pages justify. The repository card is the
    same fallback `20_landing.py` uses for an uncarded facet, with no dimensions claimed for it because
    it is 1200x600 today and that is not ours to promise.
    """
    card = f"https://opengraph.githubassets.com/1/{esc(REPO)}"
    return f"""<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(url)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(url)}">
<meta property="og:image" content="{card}">
<meta property="og:image:alt" content="The Awesome Agentic Atlas repository on GitHub.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{card}">
<link rel="icon" href="{rel(depth, ICON)}" type="image/svg+xml">
{HEAD_THEME}<link rel="stylesheet" href="{rel(depth, 'pages.css')}">
{ld}</head>
"""


def nav(depth: int) -> str:
    """The header navigation, matching `20_landing.py`'s so the two page families feel like one site."""
    return f"""  <nav>
    <a href="{rel(depth, 'collections/')}">Collections</a> ·
    <a href="https://github.com/{esc(REPO)}/blob/main/mega-list/leaderboard.md">Leaderboard</a> ·
    <a href="{rel(depth, 'repo/')}">All projects</a> ·
    <a href="{rel(depth)}#browse">Topics &amp; harnesses</a><br>
    <a href="https://github.com/{esc(REPO)}">Repository</a> ·
    <a href="https://github.com/{esc(REPO)}/tree/main/mega-list">Markdown</a><br>
    <button class="chip" id="theme" aria-pressed="false">Light theme</button>
  </nav>"""


def foot(depth: int, snapshot: str, lists: int) -> str:
    """The site footer, plus the one sentence these pages owe a reader that the others do not: who chose.

    Worth being explicit about. Every other page here can say "eleven lists agreed"; this one cannot, and
    a reader who thinks the picks are a merge of somebody else's judgement has been misled by the shell.
    """
    return f"""<footer><div class="wrap">
  These are editorial picks, and the only editorial pages on the
  <a href="{rel(depth)}">Awesome Agentic Atlas</a> &mdash; every other page is what {lists}
  awesome-lists agreed on, ranked by a number GitHub maintains. Here somebody chose, the reasoning is
  printed beside each pick, and the curation is a
  <a href="https://github.com/{esc(REPO)}/blob/main/config/collections.json">reviewable file</a> you can
  open an issue against. Stars, language, licence and last-push come from the GitHub API on
  {esc(snapshot)} and drift daily. Platform verdicts are derived from each project's own README, install
  route, CI config and release assets &mdash; <span class="vY">green</span> is stated evidence,
  <span class="vL">amber</span> is inferred from the language. A build here fails rather than publish a
  pick whose evidence has stopped supporting the claim above it.
</div></footer>
{THEME_JS}{b19.beacon()}</body>
</html>
"""


# ------------------------------------------------------------------ the collection page
def itemlist(coll: dict, url: str) -> str:
    """`ItemList` for the picks, in the curated order.

    `itemListOrder` is `ItemListUnordered` and that is not laziness: everywhere else on this site the
    order is stars descending, which is a ranking, and here it is the order the slots are read in. Saying
    "descending" would claim pick one is better than pick seven, when what it actually is is the agent
    rather than the thing you read while it runs. `<` escaped for the same reason as everywhere else.
    """
    doc = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": coll["title"],
        "description": clip(coll["intro"], 300),
        "url": url,
        "numberOfItems": len(coll["picks"]),
        "itemListOrder": "https://schema.org/ItemListUnordered",
        "itemListElement": [{"@type": "ListItem", "position": i, "name": p["row"]["name"],
                             "description": p["role"], "url": SITE + repo_path(p["nwo"])}
                            for i, p in enumerate(coll["picks"], 1)],
    }
    body = json.dumps(doc, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    return f'<script type="application/ld+json">{body}</script>\n'


def pick_html(p: dict, i: int, depth: int, os_labels: list[str], lists: int) -> str:
    """One slot: what it is for, what fills it, why, and what that judgement was made from."""
    r = p["row"]
    page_url = esc(rel(depth, repo_path(p["nwo"])))
    stars = f"{r['stars']:,}" if r["stars"] else "&mdash;"
    agreed = f'{r["lists"]} of {lists} lists' if r["lists"] > 1 else "1 list"
    facts = " · ".join(filter(None, [
        f'<b>{stars}</b> stars',
        agreed,
        esc(r["lang"]) if r["lang"] else "",
        esc(r["license"]) if r["license"] else "no licence stated",
        f'pushed {esc(r["pushed"])}' if r["pushed"] else "",
    ]))
    cmd = (f'<code class="cmd">{esc(r["install"])}</code>' if r["install"] else
           '<p class="meta">No one-line install: read the project\'s own instructions.</p>')
    topic = esc(rel(depth, "topic/" + r["cat_slug"]) + "/")
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in r["target_names"])
    return f"""<li class="pick">
  <p class="role"><span class="slot">{i}</span> {esc(p["role"])}</p>
  <h2><a href="{page_url}">{esc(r["name"])}</a></h2>
  <a class="nwo" href="{esc(r["url"])}">{esc(p["nwo"])}</a>
  <p class="why">{esc(p["why"])}</p>
  <p class="desc">{esc(r["blurb"])}</p>
  {cmd}
  <p class="meta ev">{facts}</p>
  <p class="meta os">{verdicts(r, os_labels)}</p>
  <p class="meta tp"><a href="{topic}">{esc(r["cat_name"])}</a> {tags}</p>
</li>"""


def render(coll: dict, others: list[dict], data: dict) -> str:
    # Before a byte is written. The marks below are paired with platforms by position and by nothing else,
    # so a reordered or renamed `os` column would print the Docker whale beside the Windows verdict -- a
    # page making a false statement about where a project runs, under a heading that says trust us. That is
    # the same class of failure as a pick whose evidence has expired, and it gets the same answer: a red
    # build and a curator's decision, not a page that quietly means something else.
    osicons.check(data["os"])
    depth = len(coll["path"])
    lists = merged_lists(data)
    url = SITE + "/".join(coll["path"]) + "/"
    picks = coll["picks"]
    stars = sum(p["row"]["stars"] or 0 for p in picks)
    topics = len({p["row"]["cat_slug"] for p in picks})
    live = esc(rel(depth) + share_hash(coll))
    desc = clip(f"{len(picks)} picked projects: {coll['intro']}", 158)
    installs = [p["row"]["install"] for p in picks if p["row"]["install"]]
    # Counted rather than asserted. An earlier draft of the warning below said "two of them pipe into a
    # shell" on all five pages, which was true of one of them: the sentence a reader is most likely to act
    # on was the one nothing checked.
    piped = sum(1 for c in installs if PIPED.search(c))
    warn = ("Read them before you run them &mdash; they are other people's one-liners"
            + (f", and {piped} of them {'pipes' if piped == 1 else 'pipe'} a download straight into a "
               "shell." if piped else ", and none of this set pipes a download into a shell."))
    chips = "".join(
        '<a class="chip" href="{}">{} <span class="ct">{}</span></a>'.format(
            esc(rel(depth, "collections/" + o["slug"]) + "/"), esc(o["title"]), len(o["picks"]))
        for o in others if o["slug"] != coll["slug"])
    # The mark-to-word key, once per page, above the picks. Each verdict below already carries the platform
    # name in a `title` and in a visually-hidden span, so a screen reader and a mouse are both answered --
    # and neither of those exists on a phone, which is where a page called "a first setup on Windows" is
    # most likely to be read. Five marks and five words in text is the only form of the pairing that
    # survives having no pointer. Shared with `20_landing.py` rather than restated: the two surfaces print
    # the same marks for the same reason and a second copy of the key is a second thing to drift.
    oskey = osicons.legend()
    # The sprite the marks in every `.meta.os` row resolve against, once per document and first thing in the
    # body. A `<use>` with no matching `<symbol>` draws nothing at all -- not a broken glyph, an empty box --
    # so a page that lost this looks like a slightly airy layout and states no verdicts.
    return head(f"{coll['title']} — Awesome Agentic Atlas", desc, url, depth,
                itemlist(coll, url)) + f"""<body>
{osicons.SPRITE}
<header><div class="wrap"><div class="top">
  <div>
    <p class="kick">Collection · {esc(coll["kicker"])}</p>
    <h1>{esc(coll["title"])}</h1>
    <p class="sub"><b>{len(picks)}</b> picks · <b>{topics}</b> of the atlas's
      {len(data["cats"])} topics · <b>{stars:,}</b> combined stars ·
      snapshot {esc(data["snapshot"])}</p>
    <p class="intro">{esc(coll["intro"])}</p>
    <a class="cta" href="{live}">Open all {len(picks)} in the atlas &rarr;</a>
    <p class="meta take">From there: save them to your own projects, or export the set as Markdown,
      a standalone HTML page, or a PDF.</p>
  </div>
{nav(depth)}
</div></div></header>

<main><div class="wrap">
{oskey}
<ol class="picks">
{chr(10).join(pick_html(p, i, depth, data["os"], lists) for i, p in enumerate(picks, 1))}
</ol>

<section class="allin">
  <h2>The whole set, in one paste</h2>
  <p>Every install command above, in the order they are listed. {warn}</p>
  <pre class="cmd">{esc(chr(10).join(installs))}</pre>
</section>

<nav class="rel">
  <h2>The other collections</h2>
  <p>Same idea, different question. Each one fills every slot once.</p>
  {chips}
  <h2>Or browse the whole atlas</h2>
  <p>{len(data["rows"]):,} projects, no opinions, every filter in the URL.</p>
  <a class="chip" href="{rel(depth)}">The interactive index</a>
  <a class="chip" href="{rel(depth, 'collections/')}">All collections</a>
</nav>
</div></main>

""" + foot(depth, data["snapshot"], lists)


# ------------------------------------------------------------------ the hub
def render_hub(colls: list[dict], data: dict) -> str:
    depth = 1
    lists = merged_lists(data)
    url = SITE + "collections/"
    picks = sum(len(c["picks"]) for c in colls)
    desc = clip(f"{len(colls)} curated sets of agentic AI tools, {picks} picks in total: a first setup, "
                "a Windows stack, a Claude Code kit, a fully local stack, and the tools that tell you "
                "what your agent actually did.", 158)
    ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Collections",
        "description": desc,
        "url": url,
        "numberOfItems": len(colls),
        "itemListOrder": "https://schema.org/ItemListUnordered",
        "itemListElement": [{"@type": "ListItem", "position": i, "name": c["title"],
                             "url": SITE + "collections/" + c["slug"] + "/"}
                            for i, c in enumerate(colls, 1)],
    }, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    cards = []
    for c in colls:
        roles = "".join(f'<span class="tag">{esc(p["role"])}</span>' for p in c["picks"])
        stars = sum(p["row"]["stars"] or 0 for p in c["picks"])
        # Said on the card rather than only on the page, because it is the reason to trust the page: the
        # claim in the title is not prose somebody wrote once, it is a condition this build re-checked.
        checked = ""
        if c.get("requires"):
            key = next(iter(c["requires"]))
            checked = f" · every pick's {esc(key)} claim re-checked at build time"
        cards.append(f"""<li class="coll">
  <p class="kick">{esc(c["kicker"])}</p>
  <h2><a href="{esc(c["slug"])}/">{esc(c["title"])}</a></h2>
  <p class="intro">{esc(clip(c["intro"], 240))}</p>
  <p class="meta">{roles}</p>
  <p class="meta ev"><b>{len(c["picks"])}</b> picks ·
    <b>{stars:,}</b> combined stars{checked}</p>
</li>""")
    cards = "\n".join(cards)
    return head("Collections: recommended sets of agentic tools — Awesome Agentic Atlas",
                desc, url, depth,
                f'<script type="application/ld+json">{ld}</script>\n') + f"""<body>
<header><div class="wrap"><div class="top">
  <div>
    <p class="kick">The opinionated corner</p>
    <h1>Collections</h1>
    <p class="sub"><b>{len(colls)}</b> sets · <b>{picks}</b> picks · drawn from
      <b>{len(data["rows"]):,}</b> projects · snapshot {esc(data["snapshot"])}</p>
    <p class="intro">The rest of this site tells you what {lists} awesome-lists agreed on and sorts it by
      stars, which is the honest answer to "what exists" and no answer at all to "what should I install".
      These pages answer the second question. Each one is a working set with every slot filled once, the
      reasoning printed beside each pick, and the evidence it was made from printed under that.</p>
    <a class="cta" href="{rel(depth)}">Or browse all {len(data["rows"]):,} projects &rarr;</a>
  </div>
{nav(depth)}
</div></div></header>

<main><div class="wrap">
<ul class="colls">
{cards}
</ul>
<section class="allin">
  <h2>How these are made</h2>
  <p>The picks live in
    <a href="https://github.com/{esc(REPO)}/blob/main/config/collections.json">one JSON file</a>, so a
    disagreement is a diff rather than an argument about a rendered page. Every pick is checked against
    the committed snapshot before anything is published: a project that has left the atlas, or a
    "runs on Windows" pick whose platform verdict has dropped from stated to inferred, fails the build
    instead of quietly weakening the page. Each set is also a link &mdash; the atlas reads
    <code class="cmd">#list=</code> in a URL, so a collection opens as a filtered view you can save,
    print, or export as Markdown or HTML and take somewhere else.</p>
</section>
</div></main>

""" + foot(depth, data["snapshot"], lists)


# ------------------------------------------------------------------ the Markdown twin
def markdown(coll: dict, data: dict, lists: int) -> str:
    """The same picks and the same prose, for the readers `mega-list/` exists for.

    Not a second curation and not a summary: a reader who found this on GitHub gets the reasoning, the
    evidence and the same share link. The only thing missing is the theme toggle.
    """
    out = [f"# {coll['title']}", "",
           f"*{coll['kicker']}*", "",
           coll["intro"], "",
           f"{len(coll['picks'])} picks · "
           f"{sum(p['row']['stars'] or 0 for p in coll['picks']):,} combined stars · "
           f"snapshot {data['snapshot']}", "",
           f"[Open all {len(coll['picks'])} in the atlas]({SITE}{share_hash(coll)}) — from there you can "
           "save them to your own projects or export the set as Markdown, HTML or a PDF.", ""]
    if coll.get("requires"):
        key, want = next(iter(coll["requires"].items()))
        out += [f"> Every pick is checked at build time: `{key}` = `{want}`. If the committed snapshot "
                "stops supporting that for any one of them, this page fails to build rather than "
                "quietly meaning something weaker.", ""]
    out += ["---", ""]
    for i, p in enumerate(coll["picks"], 1):
        r = p["row"]
        stars = f"{r['stars']:,}" if r["stars"] else "—"
        agreed = f"{r['lists']} of {lists} lists" if r["lists"] > 1 else "1 list"
        os_bits = " ".join(f"{o[:3]} {r['os'][k:k + 1] or '-'}" for k, o in enumerate(data["os"]))
        out += [f"## {i}. {p['role']} — [{r['name']}]({r['url']})", "",
                f"`{p['nwo']}` · [detail page]({SITE}{repo_path(p['nwo'])})", "",
                p["why"], "",
                f"> {r['blurb']}", ""]
        if r["install"]:
            out += ["```sh", r["install"], "```", ""]
        out += [f"**{stars}** stars · {agreed} · {r['lang'] or 'language not detected'} · "
                f"{r['license'] or 'no licence stated'} · pushed {r['pushed'] or 'unknown'}", "",
                f"Platforms: {os_bits}  (Y stated · L inferred · N no evidence · a n/a · - unknown)", "",
                f"Topic: {r['cat_name']}"
                + (f" · Targets: {', '.join(r['target_names'])}" if r["target_names"] else ""), "",
                "---", ""]
    out += ["These are editorial picks — the only editorial pages on the atlas. Everything else here is "
            f"what {lists} awesome-lists agreed on. The curation is a "
            f"[reviewable file](https://github.com/{REPO}/blob/main/config/collections.json); open an "
            "issue if you would pick differently.", ""]
    return "\n".join(out)


def markdown_index(colls: list[dict], data: dict, lists: int) -> str:
    out = ["# Collections", "",
           "Curated sets, one project per slot. The rest of `mega-list/` is what "
           f"{lists} awesome-lists agreed on; these {len(colls)} pages are where somebody chose.", "",
           f"Snapshot {data['snapshot']} · {sum(len(c['picks']) for c in colls)} picks across "
           f"{len(colls)} sets.", ""]
    for c in colls:
        out += [f"## [{c['title']}]({c['slug']}.md)", "",
                f"*{c['kicker']}* — {clip(c['intro'], 200)}", "",
                "  ".join(f"`{p['role']}`" for p in c["picks"]), "",
                f"[Open the set in the atlas]({SITE}{share_hash(c)}) · "
                f"[the page]({SITE}collections/{c['slug']}/)", ""]
    return "\n".join(out)


# ------------------------------------------------------------------ writing
def prune(keep: set[Path]) -> list[Path]:
    """Delete pages and twins this run did not write, then the directories they emptied.

    A renamed or removed collection would otherwise leave a page that is still served, still claiming a
    canonical URL, and no longer in the sitemap -- indexed, stale, and invisible to every later run. Only
    files this stage's own naming produces are touched.
    """
    gone = []
    base = OUT / "collections"
    if base.exists():
        for path in sorted(base.rglob("index.html")):
            if path.resolve() not in keep:
                path.unlink()
                gone.append(path)
        for d in sorted((p for p in base.rglob("*") if p.is_dir()),
                        key=lambda p: len(p.parts), reverse=True):
            if not any(d.iterdir()):
                d.rmdir()
    if MD.exists():
        for path in sorted(MD.glob("*.md")):
            if path.resolve() not in keep:
                path.unlink()
                gone.append(path)
    return gone


def main() -> None:
    data = json.loads((OUT / "data.json").read_text(encoding="utf-8"))
    colls = plan(data)
    lists = merged_lists(data)

    written = set()
    total = 0
    for c in colls:
        path = OUT.joinpath(*c["path"], "index.html")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render(c, colls, data), encoding="utf-8")
        written.add(path.resolve())
        total += path.stat().st_size

    hub = OUT / "collections" / "index.html"
    hub.write_text(render_hub(colls, data), encoding="utf-8")
    written.add(hub.resolve())
    total += hub.stat().st_size

    MD.mkdir(parents=True, exist_ok=True)
    md_total = 0
    for c in colls:
        path = MD / f"{c['slug']}.md"
        path.write_text(markdown(c, data, lists), encoding="utf-8")
        written.add(path.resolve())
        md_total += path.stat().st_size
    readme = MD / "README.md"
    readme.write_text(markdown_index(colls, data, lists), encoding="utf-8")
    written.add(readme.resolve())
    md_total += readme.stat().st_size

    gone = prune(written)

    picks = sum(len(c["picks"]) for c in colls)
    checked = sum(1 for c in colls if c.get("requires"))
    print(f"{len(colls)} collections · {picks} picks · {len(colls) + 1} pages · {b20.kb(total)}")
    print(f"mega-list/collections/ · {len(colls) + 1} files · {b20.kb(md_total)}")
    print(f"{checked} collection(s) carry a build-time requirement, all satisfied against the "
          f"{data['snapshot']} snapshot")
    print("sitemap.xml carries these URLs via scripts/20_landing.py -- run it after adding a collection")
    if gone:
        print(f"{len(gone)} stale file(s) removed: " + ", ".join(p.name for p in gone[:5]))


if __name__ == "__main__":
    main()
