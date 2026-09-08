"""Unit tests for the curated collections -- `scripts/25_collections.py` and `config/collections.json`.

These five pages are the only editorial surface on the site. Everywhere else a wrong number is a bug in a
merge; here a wrong number is a recommendation that is not true, printed under a heading that says trust
us. So what this file mostly tests is the machinery that refuses to publish one.

Six groups:

  the curation   -- the committed `config/collections.json` resolves against the committed
                    `docs/data.json`: every `nwo` exists, every `requires` holds, no slot is filled twice,
                    every `why` is a sentence rather than a shrug. This is the group that goes red on a
                    data refresh, which is the entire point of it -- see the module docstring over there.
  the guard      -- each refusal separately, on a curation this file mutates rather than one it waits for.
                    A guard that has never been seen to fire is a guard nobody should believe, and the
                    committed curation passes, so the only way to see the branches is to break a copy.
  the numbers    -- that "N of M lists" uses the count of lists that actually contributed to the committed
                    rows and not `len(SOURCES)`. On this checkout those are 11 and 39, and the second one
                    makes a false sentence out of every pick's evidence line.
  the pages      -- the rendered HTML: one page per collection plus a hub, the share link carries every
                    pick, the shell is the shared one, and the evidence beside each pick is the row's own.
  the twins      -- `mega-list/collections/`: same picks, same prose, same order, and links that resolve.
  the wiring     -- that the URLs reach `docs/sitemap.xml`, that every page is linked from somewhere a
                    reader can get to, and that the pipe-into-a-shell warning is counted rather than
                    asserted -- it was wrong once, in the direction of reassuring.

What this cannot see: whether the picks are *good*. Nothing here can. It can only check that every claim
made beside them is one the dataset supports, which is the part a machine is better at than a reviewer.

Nothing here writes to `docs/` or `mega-list/`: the renderers are pure functions of two loaded dicts, and
the two that are not -- `main()` and `prune()` -- are not called.

Run: python tests/collections_test.py
"""
from __future__ import annotations

import copy
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

ok = bad = 0


def eq(name: str, got, want) -> None:
    global ok, bad
    if got == want:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}\n  got  {got!r}\n  want {want!r}")


def true(name: str, cond, detail: str = "") -> None:
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}" + (f"\n  {detail}" if detail else ""))


def raises(name: str, fn) -> str:
    """The refusal and the sentence it carries. For a guard, the message is half the deliverable: it is
    read by whoever has to decide between re-picking and rewriting the page."""
    global ok, bad
    try:
        fn()
    except b25.CurationError as e:
        ok += 1
        return str(e)
    bad += 1
    print(f"FAIL {name} did not raise CurationError")
    return ""


def says(name: str, text: str, needle: str) -> None:
    true(name, needle in text, f"{needle!r} not in {text[:200]!r}")


# `importlib` because the module's name starts with a digit. Loading it executes `19_pages` and
# `20_landing` too -- both do their work under `if __name__`, so this runs no build.
spec = importlib.util.spec_from_file_location("b25", SCRIPTS / "25_collections.py")
b25 = importlib.util.module_from_spec(spec)
sys.modules["b25"] = b25
spec.loader.exec_module(b25)

DATA = json.loads((ROOT / "docs" / "data.json").read_text(encoding="utf-8"))
CURATION = json.loads((ROOT / "config" / "collections.json").read_text(encoding="utf-8"))
SRC = (SCRIPTS / "25_collections.py").read_text(encoding="utf-8")
LISTS = b25.merged_lists(DATA)


def fresh() -> dict:
    return copy.deepcopy(CURATION)


def coll(c: dict, slug: str) -> dict:
    return next(x for x in c["collections"] if x["slug"] == slug)


# ---------------------------------------------------------------- the curation, as committed
print("── the committed curation against the committed data " + "─" * 44)
plan = b25.plan(DATA)
true("the curation resolves against the dataset", len(plan) >= 3, f"{len(plan)} collections")
eq("every collection in the file is planned", len(plan), len(CURATION["collections"]))
rows = b25.load_rows(DATA)
eq("every row in data.json is addressable by nwo", len(rows), len(DATA["rows"]))

for c in plan:
    slug = c["slug"]
    true(f"{slug}: has a title", bool(c["title"].strip()))
    true(f"{slug}: has a kicker", bool(c["kicker"].strip()))
    true(f"{slug}: the intro is a paragraph, not a label", len(c["intro"].split()) >= 25,
         c["intro"])
    true(f"{slug}: slug is url-safe", re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug) is not None, slug)
    true(f"{slug}: {b25.MIN_PICKS}-{b25.MAX_PICKS} picks",
         b25.MIN_PICKS <= len(c["picks"]) <= b25.MAX_PICKS, str(len(c["picks"])))
    eq(f"{slug}: every slot is filled once",
       len({p["role"].strip().lower() for p in c["picks"]}), len(c["picks"]))
    eq(f"{slug}: no project appears twice", len({p["nwo"] for p in c["picks"]}), len(c["picks"]))
    for p in c["picks"]:
        true(f"{slug}/{p['nwo']}: is in the atlas", p["nwo"] in rows)
        true(f"{slug}/{p['nwo']}: the row it carries is that project's",
             p["row"]["nwo"] == p["nwo"])
        true(f"{slug}/{p['nwo']}: has a reason written for it", len(p["why"].split()) >= 12, p["why"])
        true(f"{slug}/{p['nwo']}: the reason is prose, not a fragment", p["why"].strip()[-1] in ".!?",
             p["why"])

# The three requirements, checked here against the data as well as through the guard: a `requires` that
# `check()` reads but nothing enforces would pass every test in the next group and still publish a lie.
os_labels = DATA["os"]
target_slugs = {t["slug"] for t in DATA["targets"]}
for c in plan:
    for key, want in (c.get("requires") or {}).items():
        if key == "os":
            k = os_labels.index(want)
            verdicts = {p["row"]["os"][k:k + 1] for p in c["picks"]}
            eq(f"{c['slug']}: every pick states {want} support, none infers it", verdicts, {"Y"})
        if key == "target":
            true(f"{c['slug']}: {want} is a target in the data", want in target_slugs)
            eq(f"{c['slug']}: every pick targets {want}",
               [p["nwo"] for p in c["picks"] if want not in p["row"]["target_slugs"]], [])

# Not a rule, an observation worth guarding: five sets of seven that all picked the same project would be
# one recommendation wearing five hats.
picked = [p["nwo"] for c in plan for p in c["picks"]]
true("the sets are mostly distinct projects", len(set(picked)) >= len(picked) * 0.7,
     f"{len(set(picked))} distinct of {len(picked)} picks")
true("...and between them cover several topics",
     len({p["row"]["cat_slug"] for c in plan for p in c["picks"]}) >= 5)

# ---------------------------------------------------------------- the guard
print("\n── the refusals, on a mutated copy " + "─" * 62)
c = fresh()
coll(c, "first-setup")["picks"][0]["nwo"] = "nobody/not-a-real-repo"
msg = raises("a pick that has left the atlas is refused", lambda: b25.plan(DATA, c))
says("...and the message names the project", msg, "nobody/not-a-real-repo")
says("...and says what to suspect", msg, "no longer on any source list")

first_os = next((x for x in CURATION["collections"] if (x.get("requires") or {}).get("os")), None)
true("some collection makes a platform claim, so the branch below is reachable", first_os is not None)
if first_os:
    want = first_os["requires"]["os"]
    k = DATA["os"].index(want)
    weaker = next(n for n, r in b25.load_rows(DATA).items() if r["os"][k:k + 1] == "L")
    c = fresh()
    coll(c, first_os["slug"])["picks"][1]["nwo"] = weaker
    msg = raises(f"a {want} pick whose verdict is only inferred is refused",
                 lambda: b25.plan(DATA, c))
    says("...and the message names it", msg, weaker)
    says("...and says the snapshot is what changed its mind", msg, "snapshot")
    says("...and offers both ways out", msg, "re-pick")
    says("...including rewriting the claim", msg, "rewrite the intro")

first_tgt = next((x for x in CURATION["collections"] if (x.get("requires") or {}).get("target")), None)
true("some collection makes a target claim too", first_tgt is not None)
if first_tgt:
    want = first_tgt["requires"]["target"]
    off = next(n for n, r in b25.load_rows(DATA).items() if want not in r["target_slugs"])
    c = fresh()
    coll(c, first_tgt["slug"])["picks"][0]["nwo"] = off
    msg = raises(f"a pick that does not target {want} is refused", lambda: b25.plan(DATA, c))
    says("...and the message names the requirement", msg, want)

c = fresh()
target = coll(c, "first-setup")
target["picks"][1]["role"] = target["picks"][0]["role"]
msg = raises("two picks in one slot is refused", lambda: b25.plan(DATA, c))
says("...and the message names the slot", msg, target["picks"][0]["role"])

c = fresh()
target = coll(c, "first-setup")
target["picks"][1]["nwo"] = target["picks"][0]["nwo"]
raises("the same project twice in one set is refused", lambda: b25.plan(DATA, c))

c = fresh()
coll(c, "first-setup")["picks"] = coll(c, "first-setup")["picks"][:b25.MIN_PICKS - 1]
msg = raises("too few picks to be a set is refused", lambda: b25.plan(DATA, c))
says("...and the message says what the range is", msg, f"{b25.MIN_PICKS}-{b25.MAX_PICKS}")

c = fresh()
picks = coll(c, "first-setup")["picks"]
spare = next(n for n in b25.load_rows(DATA) if n not in {p["nwo"] for p in picks})
while len(picks) <= b25.MAX_PICKS:
    picks.append({"nwo": spare, "role": f"slot {len(picks)}",
                  "why": "padding written only to push this set over the ceiling the build enforces"})
raises("more picks than a set can hold is refused", lambda: b25.plan(DATA, c))

c = fresh()
coll(c, "first-setup")["picks"][0]["why"] = "it is good"
msg = raises("a pick with no reason written for it is refused", lambda: b25.plan(DATA, c))
says("...and the message names the project", msg, coll(fresh(), "first-setup")["picks"][0]["nwo"])

c = fresh()
c["collections"][1]["slug"] = c["collections"][0]["slug"]
msg = raises("two collections sharing a slug is refused", lambda: b25.plan(DATA, c))
says("...and says which slug", msg, c["collections"][0]["slug"])

c = fresh()
coll(c, "first-setup")["requires"] = {"os": "Win32"}
msg = raises("a requirement naming a platform the data does not have is refused",
             lambda: b25.plan(DATA, c))
says("...and says so rather than silently passing", msg, "not a platform in the data")

c = fresh()
coll(c, "first-setup")["requires"] = {"target": "not-a-harness"}
raises("a requirement naming a target the data does not have is refused", lambda: b25.plan(DATA, c))

c = fresh()
coll(c, "first-setup")["requires"] = {"stars": 1000}
msg = raises("an unknown kind of requirement is refused rather than ignored",
             lambda: b25.plan(DATA, c))
says("...and names it", msg, "stars")

# ---------------------------------------------------------------- the numbers
print("\n── the denominator " + "─" * 78)
k = DATA["cols"].index("listed_by")
labels = {n.strip() for r in DATA["rows"] for n in r[k].split(",") if n.strip()}
eq("merged_lists counts the labels the committed rows carry", LISTS, len(labels))
true("...which is what apply_flags derives for the index",
     "listed_by" in (SCRIPTS / "apply_flags.py").read_text(encoding="utf-8"))
# The bug this exists to prevent. `b19.LISTS` is `len(SOURCES)`; on a checkout whose data predates a source
# expansion the two differ, and the larger one turns every "2 of M lists" on these pages into a falsehood.
true("...and is not blindly taken from the live source count",
     "b19.LISTS" not in SRC.split('"""', 2)[2] or "LISTS = b19.LISTS" not in SRC,
     "25_collections.py assigns b19.LISTS")
per_row_max = max(r[DATA["cols"].index("lists")] for r in DATA["rows"])
true("no row claims agreement from more lists than contributed", per_row_max <= LISTS,
     f"max lists={per_row_max}, merged={LISTS}")

# ---------------------------------------------------------------- the rendered pages
print("\n── the rendered pages " + "─" * 75)
pages = {c["slug"]: b25.render(c, plan, DATA) for c in plan}
hub = b25.render_hub(plan, DATA)
eq("one page per collection", len(pages), len(plan))

for slug, html in pages.items():
    c = coll({"collections": plan}, slug)
    d = len(c["path"])
    up = "../" * d
    true(f"{slug}: is a document", html.startswith("<!doctype html>"))
    says(f"{slug}: declares the dark default so a no-JS reader gets a palette",
         html, '<html lang="en" data-theme="dark">')
    says(f"{slug}: uses the shared stylesheet rather than its own", html, f'href="{up}pages.css"')
    true(f"{slug}: has no stylesheet of its own", "<style" not in html)
    says(f"{slug}: canonical is absolute", html, f'<link rel="canonical" href="{b25.SITE}')
    says(f"{slug}: resolves the theme before first paint", html, "prefers-color-scheme")
    says(f"{slug}: carries the theme toggle", html, 'id="theme"')
    says(f"{slug}: links to the hub", html, f'href="{up}collections/"')
    says(f"{slug}: the favicon resolves from this depth", html, f'href="{up}favicon.svg"')
    # The share link is the feature: one click puts the whole set in the interactive view, where the
    # reader can save it or export it. A page whose link is missing a pick is a broken promise.
    frag = b25.share_hash(c)
    says(f"{slug}: links the whole set into the atlas", html, f'href="{up}{frag}"')
    for p in c["picks"]:
        eq(f"{slug}: {p['nwo']} is in the share link", p["nwo"] in frag, True)
        says(f"{slug}: {p['nwo']} links to its detail page", html, up + b25.repo_path(p["nwo"]))
        says(f"{slug}: {p['nwo']}'s slot is named", html, p["role"])
        says(f"{slug}: {p['nwo']}'s star count is the row's",
             html, f"{p['row']['stars']:,}" if p["row"]["stars"] else "&mdash;")
    eq(f"{slug}: every pick is numbered once",
       len(re.findall(r'<span class="slot">', html)), len(c["picks"]))
    eq(f"{slug}: every pick is a list item", len(re.findall(r'<li class="pick">', html)),
       len(c["picks"]))
    says(f"{slug}: names who chose, since no list did", html, "editorial picks")
    says(f"{slug}: says a stale claim fails the build", html, "fails rather than publish")
    says(f"{slug}: offers the exports", html, "Markdown")
    # Counted from the commands on the page, not asserted in prose. The first version of this sentence
    # said "two of them pipe into a shell" on all five pages; it was true of one.
    piped = sum(1 for p in c["picks"]
                if p["row"]["install"] and b25.PIPED.search(p["row"]["install"]))
    says(f"{slug}: the pipe-into-a-shell warning matches the {piped} on the page", html,
         f"{piped} of them pipe" if piped > 1 else
         ("1 of them pipes" if piped == 1 else "none of this set pipes"))
    ld = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    true(f"{slug}: carries structured data", ld is not None)
    if ld:
        doc = json.loads(ld[1].replace("\\u003c", "<"))
        eq(f"{slug}: the ItemList counts the picks", doc["numberOfItems"], len(c["picks"]))
        eq(f"{slug}: ...and lists them all", len(doc["itemListElement"]), len(c["picks"]))
        # Everywhere else on this site the order is stars descending. Here it is the order the slots are
        # read in, and claiming otherwise would tell a crawler pick one outranks pick seven.
        says(f"{slug}: ...unordered, because the order is slots and not rank",
             doc["itemListOrder"], "Unordered")
        true(f"{slug}: ...with no raw < in the JSON, which would close the script early",
             "<" not in ld[1])

says("the hub is a document", hub, "<!doctype html>")
for c in plan:
    says(f"the hub links {c['slug']}", hub, f'href="{c["slug"]}/"')
    says(f"the hub names {c['slug']}", hub, c["title"])
eq("the hub's ItemList counts the collections",
   json.loads(re.search(r'application/ld\+json">(.*?)</script>', hub, re.S)[1]
              .replace("\\u003c", "<"))["numberOfItems"], len(plan))
says("the hub says where the picks live", hub, "config/collections.json")
says("the hub explains the build-time check", hub, "fails the build")
says("the hub points back at the whole atlas", hub, f"{len(DATA['rows']):,}")

# ---------------------------------------------------------------- the Markdown twins
print("\n── the Markdown twins " + "─" * 75)
mds = {c["slug"]: b25.markdown(c, DATA, LISTS) for c in plan}
index = b25.markdown_index(plan, DATA, LISTS)
for slug, md in mds.items():
    c = coll({"collections": plan}, slug)
    true(f"{slug}.md: starts with its title", md.startswith(f"# {c['title']}"))
    eq(f"{slug}.md: one heading per pick", len(re.findall(r"^## \d+\. ", md, re.M)), len(c["picks"]))
    for i, p in enumerate(c["picks"], 1):
        says(f"{slug}.md: pick {i} keeps its slot and its order", md, f"## {i}. {p['role']}")
        says(f"{slug}.md: pick {i} keeps its reason verbatim", md, p["why"])
    says(f"{slug}.md: carries the share link", md, b25.share_hash(c))
    says(f"{slug}.md: says these are editorial", md, "editorial picks")
    true(f"{slug}.md: escapes no pipes, which render literally outside a table", "\\|" not in md)
    true(f"{slug}.md: has no in-page anchors to go stale", "](#" not in md)
    true(f"{slug}.md: is far under GitHub's 512 KB render ceiling", len(md.encode()) < 100_000,
         str(len(md.encode())))
    if c.get("requires"):
        says(f"{slug}.md: states the claim the build re-checks", md, "fails to build")
for c in plan:
    says(f"the twin index links {c['slug']}.md", index, f"({c['slug']}.md)")
    says(f"the twin index names its slots", index, f"`{c['picks'][0]['role']}`")

# ---------------------------------------------------------------- the wiring
print("\n── the wiring " + "─" * 83)
urls = b25.urls(DATA)
eq("urls() is the hub plus one per collection", len(urls), len(plan) + 1)
eq("...hub first", urls[0], b25.SITE + "collections/")
true("...all absolute", all(u.startswith("https://") for u in urls))
true("...all with a trailing slash, matching every other URL on the site",
     all(u.endswith("/") for u in urls))
sitemap = (ROOT / "docs" / "sitemap.xml").read_text(encoding="utf-8")
for u in urls:
    says(f"sitemap.xml lists {u.split('collections/')[1] or 'the hub'}", sitemap, f"<loc>{u}</loc>")
# The rule `26_indexnow.py` maps by is "any docs/**/index.html", and `indexnow_test.py` asserts the mapped
# set and the sitemap set are equal in both directions. A page family in neither sitemap is a red build.
land = (SCRIPTS / "20_landing.py").read_text(encoding="utf-8")
true("20_landing.py is the one that puts them there", "collection_urls(data)" in land)
true("...and passes them to the sitemap it owns", "sitemap(pages, data[\"snapshot\"], colls)" in land)

# Reachability. A page nothing links to is a page only a sitemap knows about.
for name, path in (("the index", ROOT / "docs" / "index.html"),
                   ("a topic page", ROOT / "docs" / "topic" / "agent-skills" / "index.html"),
                   ("the repo hub", ROOT / "docs" / "repo" / "index.html")):
    text = path.read_text(encoding="utf-8")
    true(f"{name} links to the collections", 'collections/">Collections' in text)

# The stage must not need anything a bare clone lacks. Its whole promise is that a checkout with no crawl
# cache can rebuild these pages, which is also why this test file can exist.
for mod in ("requests", "httpx", "openpyxl", "PIL", "yaml", "numpy"):
    true(f"the stage imports no {mod} of its own",
         f"\nimport {mod}" not in SRC and f"\nfrom {mod}" not in SRC)
true("the stage reads only the committed dataset", SRC.count('"data.json"') == 1)
says("the stage's docstring says the build fails rather than publishes", b25.__doc__,
     "fails rather than publishes")
says("...and that it needs no cache and no network", b25.__doc__, "no build cache, no network")
says("...and names the re-version step a reader would otherwise miss", b25.__doc__, "24_pwa.py")
says("config/README.md documents the contract", (ROOT / "config" / "README.md").read_text(
    encoding="utf-8"), "fails the build")

# The pipe detector, on the cases the committed curation does not contain. It was wrong once by omission.
for cmd in ("curl -fsSL https://get.example.com | sh",
            "wget -qO- https://x/i.sh | bash",
            "irm https://ollama.com/install.ps1 | iex",
            "Invoke-RestMethod https://x/i.ps1 | Invoke-Expression"):
    true(f"PIPED sees {cmd[:28]}...", b25.PIPED.search(cmd) is not None)
for cmd in ("pip install foo", "npm i -g bash-tools", "git clone https://x/y.git",
            "curl -O https://x/f.tgz && bash f.sh", "docker run -it x sh"):
    true(f"PIPED leaves {cmd[:28]}... alone", b25.PIPED.search(cmd) is None)

print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
