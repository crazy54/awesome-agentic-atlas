"""Publish Lookalikes: paste a GitHub or GitLab link, or type a project's name, and see what does the same thing.

  docs/alike/index.html        the page; the encoder and the page script are inlined, the data is fetched

  python scripts/33_alike.py                  write it
  python scripts/33_alike.py --out build-tmp  a dry run, off to one side

WHAT IT ANSWERS
---------------
"I use X. What else is there?" The owner's words: a reader should be able to paste a GitHub link or the name
of an app and search for a similar set of apps that do the same thing. So the page has one input, and three
things can be in it:

  * a project the atlas holds, by link, `owner/name` or name ("claude code" finds `anthropics/claude-code`):
    its lookalikes are ranked from the index the atlas already ships, `docs/search/`, and each one says why
    it is there -- the category, the harnesses both target, the words they share;
  * a GitHub or GitLab project the atlas does not hold: the reader's browser asks the forge for its
    description, topics and README, anonymously, and ranks the atlas against that, saying plainly that the
    project is not in the atlas -- and saying as plainly what went wrong when the forge says 404, says the
    hourly limit is used up, or cannot be reached;
  * words, when the reader describes the thing instead of naming it.

Every repository's detail page links here with `?repo=<nwo>` ("Find alternatives", `22_detail.py`), and the
nav of the homepage, the catalogue, the topic pages, Discover and the collections link here by the shared
constant. `?repo=` and `?q=` are the two states a link restores.

How "similar" is scored, and the measurements behind each weight, are at the top of `scripts/alike_page.js`,
beside the code they describe; the 32-project table that tuned them is in the pull request that added this
page. The short version: the README vector alone (what `near.bin` already holds) is poor for famous projects,
because READMEs open with badges and "works with Claude Code"; a blurb vector, the curated category, shared
rare words and an ecosystem rule ("built around it" is not "an alternative to it") together are what make
Langfuse's list start Opik, Manifest, promptfoo, Latitude and Helicone.

THE NAME IS ONE CONSTANT
------------------------
`sitewide.ALIKE_PAGE`, the way `sitewide.LOCAL_PAGE` is for the local-AI page: the title, the slug and the
pitch, read by this stage, by the nav link in every page family and by the detail pages' button. The slug is
the directory under `docs/` and the URL, so changing it moves the page.

ONE ENCODER, SHARED WITH THE CATALOGUE
--------------------------------------
The query encoder -- tokeniser, forward pass, staleness guard -- is `scripts/semantic.js`, and this page and
the catalogue (`19_pages.py`) inline the same bytes. A second transcription would be the fourth copy of an
algorithm whose drift has no symptom; see that file's header. `tests/alike_test.py` holds both generators to
one copy.

WHY THE DATA IS FETCHED RATHER THAN INLINED
-------------------------------------------
`32_local.py` inlines its data, because 440 KB of hardware catalogue is that page's alone. This page needs
`docs/data.json` and four files of `docs/search/` -- 7.2 MB on disk and 3.1 MB gzipped, measured 2026-11-19 -- which
the catalogue fetches by the same URLs. Fetched, they are one copy in the reader's HTTP cache and in the
service worker's `atlas-data` and `atlas-assets` caches, shared with the catalogue, rather than a second
3 MB embedded in a page that would then churn every day the data does. So the page itself is static: no
count, no date, nothing that changes unless this file or the encoder does, and a daily rebuild writes the
same bytes.

OFFLINE, AFTER ONE VISIT, WITH NO CHANGE TO 24_pwa.py
------------------------------------------------------
The worker already caches every page a reader navigates to (keyed without the query string, so
`?repo=anything` is answered offline by the one cached copy), `data.json` by `DATA_FILES`, and the six
index files by `PAGE_ASSETS`. So a reader who has opened this page once can look up anything in the atlas on
the train. What cannot work offline is the forge lookup for a project the atlas does not hold, and the page
says so in those words. `tests/pwa-check.mjs` owns the worker; `tests/alike-check.mjs` checks the page's
offline message.

WHERE IT GOES IN A BUILD
------------------------
Anywhere before `20_landing.py`, which imports `urls()` below into `docs/sitemap.xml` -- the same constraint
and the same reason as `32_local.py`, and it sits beside that stage in both workflows. It reads nothing but
the shared encoder and its own script, so it can run from a clone with nothing fetched.
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUT = ROOT / "docs"

sys.path.insert(0, str(HERE))
import sitewide  # noqa: E402

PAGE = sitewide.ALIKE_PAGE


def _load(name: str, alias: str):
    """The dynamic load `32_local.py` documents: the numbered stages are not identifiers, and an already-loaded
    copy is reused so `20_landing.py` importing this module for its sitemap does not execute them twice."""
    if alias in sys.modules:
        return sys.modules[alias]
    spec = importlib.util.spec_from_file_location(alias, HERE / name)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[alias] = mod
    spec.loader.exec_module(mod)
    return mod


def urls(site: str | None = None) -> list[str]:
    """Every URL this stage publishes. Imported by `20_landing.py` for the sitemap, which passes the site root
    so this module does not drag the page stack in a second time to learn it."""
    if site is None:
        site = _load("19_pages.py", "b19").b17.SITE
    return [site + PAGE["slug"] + "/"]


def detail_href(rel_to_docs: str, nwo: str) -> str:
    """The "Find alternatives" link a detail page carries: this page, with `?repo=` set to the row's `nwo`.
    `rel_to_docs` is the detail page's way back to `docs/`. The slash in `owner/name` is left readable; the
    rest is quoted, so a GitLab path or a name with an ampersand survives the query string."""
    import urllib.parse
    return f"{rel_to_docs}{PAGE['slug']}/?repo=" + urllib.parse.quote(nwo, safe="/")


# ------------------------------------------------------------------ the page
b19 = _load("19_pages.py", "b19")
b20 = _load("20_landing.py", "b20")
import mark  # noqa: E402
import pagemin  # noqa: E402

SITE = b19.b17.SITE
REPO = b19.REPO
esc = b20.esc
ICON, HEAD_THEME, THEME_JS = b20.ICON, b20.HEAD_THEME, b20.THEME_JS

# The shared encoder first, then the page: the page calls `semDecode` and `semEncode` at load.
SEMANTIC_JS = (HERE / "semantic.js").read_text(encoding="utf-8")
PAGE_JS = (HERE / "alike_page.js").read_text(encoding="utf-8")

# The starting points offered under an empty box. Each is a link, so it works with no script and is a URL a
# reader can share; the page intercepts the click to skip the reload. Chosen to show the three inputs: a name,
# a link to a project the atlas holds, and a description.
EXAMPLES = [
    ("?repo=langfuse/langfuse", "langfuse/langfuse"),
    ("?repo=upstash/context7", "Context7"),
    ("?repo=e2b-dev/E2B", "github.com/e2b-dev/E2B"),
    ("?q=" + "a%20vector%20database%20for%20agent%20memory", "a vector database for agent memory"),
]


def rel(tail: str = "") -> str:
    """A link out of `docs/<slug>/`. One level down, so everything site-wide is `../`."""
    return "../" + tail


def head(title: str, desc: str, url: str) -> str:
    """The `<head>`, the shape `32_local.py` writes. `data-up` is the page script's way back to `docs/`."""
    card = f"https://opengraph.githubassets.com/1/{esc(REPO)}"
    return f"""<!doctype html>
<html lang="en" data-theme="dark" data-up="{esc(rel())}">
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
<link rel="icon" href="{esc(rel(ICON))}" type="image/svg+xml">
{sitewide.font_preload(rel())}{HEAD_THEME}<link rel="stylesheet" href="{esc(rel('pages.css'))}">
<style>{CSS}</style>
<script>document.documentElement.classList.add("lkjs");</script>
{sitewide.SITE_KIT}
</head>
"""


def nav() -> str:
    """The header navigation, matching `32_local.py`'s so the standalone pages feel like one family."""
    return f"""  <nav>
    <a href="{esc(rel('discover/'))}">Discover</a> &middot;
    <a href="{esc(rel(sitewide.LOCAL_PAGE['slug'] + '/'))}">{esc(sitewide.LOCAL_PAGE['title'])}</a> &middot;
    <a href="{esc(rel('collections/'))}">Collections</a> &middot;
    <a href="{esc(rel('catalog/'))}">Catalogue</a> &middot;
    <a href="{esc(rel('repo/'))}">All projects</a><br>
    <a href="https://github.com/{esc(REPO)}">Repository</a> &middot;
    <a href="https://github.com/{esc(REPO)}/tree/HEAD/mega-list">Markdown</a><br>
    <button class="chip" id="theme" aria-pressed="false">Light theme</button>
  </nav>"""


def render() -> str:
    title = f"{PAGE['title']}: find projects that do the same thing | Awesome Agentic Atlas"
    desc = (f"{PAGE['pitch']} Ranked across every project in the Awesome Agentic Atlas, with the reason each "
            "one is similar. Works for projects the atlas doesn't list, too.")
    url = SITE + PAGE["slug"] + "/"
    examples = " ".join(f'<a class="chip" data-ex href="{esc(h)}">{esc(t)}</a>' for h, t in EXAMPLES)
    stars = "".join(f'<option value="{v}">{esc(t)}</option>' for v, t in
                    ((0, "Any"), (10, "10+"), (100, "100+"), (1000, "1,000+"), (10000, "10,000+")))
    return f"""{head(title, desc, url)}<body>
<header><div class="wrap">
  <nav class="brandbar">{mark.brand(rel())}</nav><div class="top">
  <div>
    <p class="kick">{esc(PAGE['title'])}</p>
    <h1>Find projects that do the same thing</h1>
    <p class="sub">{esc(PAGE['pitch'])}</p>
  </div>
{nav()}
  </div>
</div></header>
<main class="lk" id="lk"><div class="wrap">
<noscript><p class="lknojs">Lookalikes ranks the atlas in your browser, so it needs JavaScript. Without it, every
  project&rsquo;s page lists related projects in its own category: start from <a href="{esc(rel('repo/'))}">All
  projects</a> or the <a href="{esc(rel('catalog/'))}">catalogue</a>.</p></noscript>

<section class="lks" aria-labelledby="lkformh">
  <h2 id="lkformh" class="sr">Search</h2>
  <form id="lkform" class="lkform" role="search">
    <label for="lkq">A GitHub or GitLab link, or a project&rsquo;s name</label>
    <div class="lkrow">
      <input id="lkq" name="repo" type="text" autocomplete="off" autocapitalize="off" spellcheck="false"
             placeholder="e.g. github.com/langfuse/langfuse or claude code" aria-describedby="lkhint">
      <button class="cta" type="submit">Find lookalikes</button>
    </div>
    <p class="lkquiet" id="lkhint">Paste any link to the repository, or type its name. Try {examples}</p>
  </form>
  <details class="lkdesc" id="lkdescribe">
    <summary>Or describe what it does</summary>
    <form id="lkdform" class="lkform" role="search">
      <label for="lkdq">What should it do?</label>
      <div class="lkrow">
        <input id="lkdq" name="q" type="text" autocomplete="off" placeholder="e.g. tracing and evals for LLM apps">
        <button class="cta" type="submit">Find projects</button>
      </div>
    </form>
  </details>
  <div class="lkstatus" id="lkstatus" role="status" hidden></div>
</section>

<section class="lks lkchoose" id="lkchoose" hidden></section>

<section class="lks lkres" aria-label="Results">
  <div class="lksrc" id="lksrc" hidden></div>
  <fieldset class="lkfilters" id="lkfilters" hidden><legend class="sr">Filter the lookalikes</legend>
    <label for="lklang">Language</label> <select id="lklang"><option value="">Any language</option></select>
    <label for="lkstars">Stars</label> <select id="lkstars">{stars}</select>
    <label class="lkcheck"><input type="checkbox" id="lkactive"> Active in the last 6 months</label>
  </fieldset>
  <div id="lkout"></div>
  <div class="lkaround" id="lkaround" hidden></div>
  <p class="sr" id="lklive" aria-live="polite"></p>
</section>

<section class="lks lkhow" aria-labelledby="lkhowh">
  <h2 id="lkhowh">How lookalikes are found</h2>
  <p>Every project in the atlas has two short fingerprints of meaning: one of its README, one of the sentence
    describing it. A lookalike is close on both, shares the project&rsquo;s category or the harnesses it is
    built for, and shares the less common words in its description. Projects from the same maintainer, or
    named after it, are listed separately, because an add-on for something is not an alternative to it.</p>
  <p>For a project the atlas doesn&rsquo;t list, your browser asks GitHub or GitLab for its description,
    topics and README, and compares those instead. GitHub allows 60 of those lookups an hour from one
    connection. Nothing you type is sent anywhere else.</p>
</section>
</div></main>
<footer><div class="wrap">
  {sitewide.buildtags(REPO)}
  {esc(PAGE['title'])} is part of the <a href="{esc(rel())}">Awesome Agentic Atlas</a>. Similarity is computed in
  your browser from the atlas&rsquo;s own index.
</div></footer>
<script>
{SEMANTIC_JS}
{PAGE_JS}</script>
{sitewide.site_script(rel())}{THEME_JS}{b19.follow()}{b19.beacon()}</body>
</html>
"""


# The page's own rules. Colour comes only from the site's custom properties (`sitewide.THEME_CSS`), so
# Light, Dark and High contrast all reach this page with no rule here naming a colour. Everything is prefixed
# `lk` so nothing here can reach a rule in `pages.css`.
CSS = """
.lk .wrap{max-width:980px}
.lk [hidden]{display:none!important}
.kick{margin:0 0 4px;color:var(--muted);font:600 12px/1.4 var(--mono);letter-spacing:.06em;text-transform:uppercase}
.lks{margin:26px 0 0;padding:20px;border:1px solid transparent;border-radius:24px;background:var(--surface);
  box-shadow:var(--raise)}
.lks h2{margin:0;font-size:19px}
.lkform label{display:block;font-weight:600;margin:0 0 6px}
.lkrow{display:flex;gap:8px;flex-wrap:wrap;align-items:stretch}
.lkrow input{flex:1 1 280px;min-width:0;font:inherit;font-size:16px;color:var(--ink);background:var(--surface);
  border:1px solid transparent;border-radius:var(--r-ctl);padding:11px 12px;min-height:44px;
  box-shadow:var(--press)}
.lkrow .cta{border:0;font:inherit;font-weight:600;min-height:44px;padding:0 18px;cursor:pointer}
.lkrow input:focus-visible,.lkrow .cta:focus-visible,.lks a:focus-visible,.lks button:focus-visible,
.lks select:focus-visible,.lkcheck:has(input:focus-visible),.lkdesc summary:focus-visible,
.lks h2:focus-visible,.lks [tabindex="-1"]:focus{outline:2px solid var(--link);outline-offset:2px}
.lkquiet{color:var(--muted);font-size:13px;margin:8px 0 0}
.lkquiet .chip{margin:4px 4px 0 0}
.lkdesc{margin:16px 0 0;border-top:1px solid var(--grid);padding-top:12px}
.lkdesc summary{cursor:pointer;color:var(--link);font-weight:600;min-height:32px;padding:4px 0}
.lkdesc .lkform{margin:8px 0 0}
.lkstatus{margin:14px 0 0;padding:10px 14px;border:1px solid transparent;border-radius:10px;color:var(--ink2);
  font-size:14.5px;background:var(--surface);box-shadow:var(--raise-sm)}
.lkstatus[data-kind=error]{border-color:transparent;color:var(--ink);box-shadow:var(--raise-sm),inset 3px 0 0 var(--accent-gold)}
.lkstatus code{font:13px var(--mono)}
.lklink{background:none;border:0;padding:4px 0;color:var(--link);text-decoration:underline;font:inherit;cursor:pointer}
.lkpick{list-style:none;margin:12px 0 0;padding:0;display:grid;gap:8px}
.lkopt{width:100%;text-align:left;font:inherit;color:var(--ink);background:var(--surface);
  border:1px solid transparent;border-radius:var(--r-ctl);padding:10px 12px;min-height:44px;
  cursor:pointer;box-shadow:var(--raise-sm)}
.lkopt:hover{border-color:transparent;box-shadow:var(--raise-hi)}
.lkopt small{color:var(--muted)}
.lksrc h2{font-size:22px;margin:0}
.lksrc h2 a{color:var(--ink)}
.lknwo{color:var(--muted);font:12.5px/1.5 var(--mono);overflow-wrap:anywhere}
.lksrc .lknwo{margin:2px 0 0}
.lkblurb{margin:6px 0 0;color:var(--ink2);font-size:14px;max-width:75ch;overflow-wrap:anywhere}
.lkmeta{margin:8px 0 0;font-size:12.5px;color:var(--muted)}
.lknot{margin:12px 0 0;padding:10px 12px;border:1px dashed transparent;border-radius:10px;color:var(--ink2);
  font-size:14px;background:var(--surface);box-shadow:var(--raise-sm)}
.lkfilters{border:0;margin:18px 0 0;padding:12px 0 0;border-top:1px solid var(--grid);min-width:0;
  display:flex;flex-wrap:wrap;gap:8px 10px;align-items:center;font-size:14px}
.lkfilters label{font-weight:600}
.lkfilters select{font:inherit;font-size:14px;color:var(--ink);background:var(--surface);border:1px solid transparent;
  border-radius:10px;padding:6px 8px;min-height:36px;max-width:100%;box-shadow:var(--press)}
.lkcheck{font-weight:400!important;display:inline-flex;gap:6px;align-items:center;min-height:36px}
.lkh{margin:20px 0 10px!important;font-size:16px!important}
.lklist{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.lkcard{padding:14px 16px;border:1px solid transparent;border-radius:var(--r-card);background:var(--surface);
  box-shadow:var(--raise-sm)}
.lkch{display:flex;justify-content:space-between;align-items:baseline;gap:4px 12px;flex-wrap:wrap}
.lkch h3{margin:0;font-size:16px}
.lkwhy{margin:8px 0 0;display:flex;flex-wrap:wrap;gap:6px;font-size:12.5px}
.lkwhy span:not(.sr){border:1px solid transparent;border-radius:999px;padding:2px 9px;color:var(--ink2);
  background:var(--surface);box-shadow:var(--press-sm)}
.lkwhy i{font-style:normal;color:var(--ink)}
.lkwhy .lkwhy-alt{border-color:transparent;color:var(--good)}
.lkaround{margin:22px 0 0}
.lkeco{margin:8px 0 0;padding-left:20px;font-size:14px}
.lkeco li{margin:4px 0}
.lkempty{margin:16px 0 0;color:var(--ink2)}
.lkhow p{margin:10px 0 0;color:var(--ink2);max-width:75ch;font-size:14.5px}
.lknojs{margin:18px 0 0;padding:10px 14px;border:1px solid transparent;border-radius:10px;
  background:var(--surface);box-shadow:var(--raise-sm)}
html:not(.lkjs) .lks{display:none}
@media (max-width:640px){
  .lks{padding:16px 14px;border-radius:12px}
  .lkrow .cta{flex:1 1 100%}
  .lkch{display:block}
}
@media (forced-colors:active){
  .lks,.lkcard,.lkopt,.lkstatus,.lkwhy span:not(.sr){border:1px solid CanvasText}
}
@media print{.lkform,.lkdesc,.lkfilters{display:none}}
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", help="write under this directory instead of docs/ (a dry run)")
    args = ap.parse_args()
    out = Path(args.out) if args.out else OUT
    page = out / PAGE["slug"] / "index.html"
    page.parent.mkdir(parents=True, exist_ok=True)
    # Comments stripped on the way out, the way `32_local.py` ships its page: they are for whoever edits this
    # stage, `alike_page.js` and `semantic.js`, and every one stays in the source.
    page.write_text(pagemin.strip_page(render()), encoding="utf-8", newline="\n")
    print(f"{PAGE['slug']}/index.html · {b20.kb(page.stat().st_size)} · fetches data.json and docs/search/ at load")
    print("sitemap.xml carries this URL via scripts/20_landing.py")


if __name__ == "__main__":
    main()
