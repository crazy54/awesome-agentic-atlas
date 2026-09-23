"""Unit tests for the site's own addresses: the host it is served at, and the links into the catalogue.

The root used to be the catalogue, and a filtered view of it was the root plus a hash: `#topic=x&target=y`,
`#q=name`, `#new=1`. When `31_home.py` took the root and `19_pages.py` moved down to `catalog/`, every
one of those links started landing on the shelves homepage, which reads no hash, so the filter was
dropped without a word. The build stayed green, because no test followed a link.

Three groups, and a fourth that is here only because this file already loads 31_home.py:

  the forwarder  -- the script in the *rendered* homepage, run under node against a stub `location`. A
                    filtered hash is forwarded to `catalog/` with its query and hash intact. An in-page
                    anchor and an empty hash are left alone. So is a hash pasted later, until it holds
                    a filter. Read out of the rendered page rather than out of the Python constant, so it
                    is the comment-stripped bytes a reader runs that are exercised.
  the generators -- each place that writes a filtered link resolves, *against the URL of the page that
                    carries it*, to `SITE + "catalog/#..."`. That covers the Markdown edition's `site()`,
                    the 156 facet pages' `live`, and the detail pages' `#q=` search link. Resolved rather
                    than string-matched, because the defect class here is a relative path that is right at
                    one depth and wrong at another.
  the address    -- `SITE` is the host in `docs/CNAME`, read here from the file rather than from `SITE`,
                    because Pages 301s the `github.io` project URL to that host and a canonical naming the
                    project URL names a redirect. A malformed CNAME is refused. The feed's `tag:` ids are
                    the ones already published in the committed `docs/feed.xml`, because an id that moved
                    with the host would show every subscriber fifty old entries as new. `robots.txt` says it
                    is read when there is a custom domain, and says it is inert when there is not.
  the spotlight  -- `spot_art()` gives the homepage's spotlight the project's own picture, and the social
                    card for a GIF or no picture. Fed both arms directly, since the committed page
                    shows only whichever one the day's row took.

Nothing here writes to `docs/`. It reads the committed `docs/data.json` and `docs/discover.json`.

Run: python tests/deeplinks_test.py
"""
from __future__ import annotations

import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

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


def load(name: str, file: str):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / file)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


b31 = load("b31", "31_home.py")
b20 = sys.modules.get("b20") or load("b20", "20_landing.py")
b17 = b20.b19.b17
b22 = load("b22", "22_detail.py")
SITE = b17.SITE
CATALOG = SITE + "catalog/"


# =====================================================================  1. the forwarder
page = b31.render()
head = page[:page.index("</head>")]
scripts = re.findall(r"<script>(.*?)</script>", head, re.S)
fwd = [s for s in scripts if "catalog/" in s]
eq("exactly one script in the homepage's <head> sends the reader to catalog/", len(fwd), 1)
fwd_at = head.find(fwd[0]) if fwd else -1
true("...and it runs before the stylesheet, so a forwarded reader is not shown a frame of the homepage",
     0 <= fwd_at < head.find('<link rel="stylesheet"'))

# Each case: the URL's query and hash at load, an optional hash assigned afterwards (fired as hashchange),
# and the one `location.replace` argument expected, or None for no call at all.
CASES = [
    ("a topic and a harness", "", "#topic=coding-agents&target=claude-code", None,
     "catalog/#topic=coding-agents&target=claude-code"),
    ("a search, with an encoded slash left encoded", "", "#q=owner%2Fname", None, "catalog/#q=owner%2Fname"),
    ("the README's #new=1", "", "#new=1", None, "catalog/#new=1"),
    ("a parameter this file has never heard of", "", "#cmp=a,b", None, "catalog/#cmp=a,b"),
    ("a query string travels with it", "?utm_source=x", "#topic=a", None, "catalog/?utm_source=x#topic=a"),
    ("an in-page anchor stays", "", "#discover", None, None),
    ("no hash stays", "", "", None, None),
    ("a filter pasted after load is forwarded on hashchange", "", "", "#q=agent", "catalog/#q=agent"),
    ("an anchor followed after load stays", "", "", "#shelves", None),
]
node = shutil.which("node")
true("node is on PATH (the forwarder is JavaScript and is run, not read)", node)
if node and fwd:
    harness = r"""
const vm = require("vm");
const [src, cases] = [process.argv[1], JSON.parse(process.argv[2])];
const out = cases.map(([search, hash, later]) => {
  const calls = [], handlers = [];
  const location = {search, hash, replace: u => calls.push(u)};
  vm.runInNewContext(src, {location, addEventListener: (t, f) => t === "hashchange" && handlers.push(f)});
  if (later !== null) { location.hash = later; handlers.forEach(f => f()); }
  return calls;
});
console.log(JSON.stringify(out));
"""
    arg = json.dumps([[c[1], c[2], c[3]] for c in CASES])
    run = subprocess.run([node, "-e", harness, fwd[0], arg], capture_output=True, text=True)
    true("the forwarder runs under node", run.returncode == 0, run.stderr)
    if run.returncode == 0:
        for (label, *_, want), calls in zip(CASES, json.loads(run.stdout)):
            eq(f"forwarder: {label}", calls, [want] if want else [])


# =====================================================================  2. the generators
eq("site() with a filter is the catalogue with the hash", b17.site(topic="agent-skills"),
   CATALOG + "#topic=agent-skills")
eq("site() with none is the catalogue, which is what 'filter it live' means", b17.site(), CATALOG)
eq("site() drops an empty filter", b17.site(topic="a", target=""), CATALOG + "#topic=a")

cats = [{"slug": "coding-agents", "name": "Coding agents"}]
tgts = [{"slug": "claude-code", "name": "Claude Code"}]
for parts, cat, tgt, want in [
        (["topic", "coding-agents"], cats[0], None, "#topic=coding-agents"),
        (["target", "claude-code"], None, tgts[0], "#target=claude-code"),
        (["topic", "coding-agents", "target", "claude-code"], cats[0], tgts[0],
         "#topic=coding-agents&target=claude-code")]:
    p = b20.Page(parts, cat, tgt, [])
    eq(f"facet page /{'/'.join(parts)}/: its live link resolves to the filtered catalogue",
       urljoin(p.url, p.live), CATALOG + want)

data = json.loads((ROOT / "docs" / "data.json").read_text(encoding="utf-8"))
with tempfile.TemporaryDirectory() as tmp:
    repos, by_cat = b22.plan(data, Path(tmp))
    # One name with a slash, if the data has one, because that is the case the quoting exists for.
    repo = next((r for r in repos if "/" in r.name), repos[0])
    html = b22.render(repo, by_cat, b22.source_links(), data)
    hrefs = [h for h in re.findall(r'href="([^"]*)"', html) if "#q=" in h]
    true("the detail page carries a #q= link", hrefs, repo.url)
    for h in hrefs:
        got = urljoin(repo.url, h.replace("&amp;", "&"))
        true(f"detail page {repo.url}: its search link resolves into the catalogue",
             got.startswith(CATALOG + "#q="), got)


# =====================================================================  3. the address
def refused(text: str) -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "CNAME"
        f.write_text(text, encoding="utf-8")
        try:
            b17.read_cname(f)
        except SystemExit:
            return True
        return False


cname_file = ROOT / "docs" / "CNAME"
true("docs/CNAME is committed (Pages serves a custom domain only while it is)", cname_file.exists())
cname = cname_file.read_text(encoding="utf-8").strip() if cname_file.exists() else ""
eq("SITE is the host docs/CNAME names, at its root", SITE, f"https://{cname}/")
eq("...and the project URL is what a fork without a CNAME gets", b17.site_url(""),
   "https://crazy54.github.io/awesome-agentic-atlas/")
with tempfile.TemporaryDirectory() as tmp:
    eq("a missing CNAME reads as none", b17.read_cname(Path(tmp) / "CNAME"), "")
    (Path(tmp) / "CNAME").write_bytes(b" atlas.example.org \r\n")
    eq("surrounding whitespace and a CRLF are not part of the name", b17.read_cname(Path(tmp) / "CNAME"),
       "atlas.example.org")
for wrong in ["https://atlas.example.org", "atlas.example.org/atlas", "Atlas.Example.org",
            "a.example.org\nb.example.org", "localhost", "-atlas.example.org"]:
    true(f"a CNAME of {wrong!r} is refused rather than put in every URL", refused(wrong))

b21 = load("b21", "21_feeds.py")
feed = (ROOT / "docs" / "feed.xml").read_text(encoding="utf-8")
ids = re.findall(r"<id>([^<]+)</id>", feed)
eq("the feed id is the one already published", b21.FEED_ID, ids[0])
first = re.search(r"<entry>.*?<id>([^<]+)</id>", feed, re.S).group(1)
nwo = first.split("/repos/", 1)[1]
eq("...and so is an entry's, so no subscriber is shown old entries as new", b21.entry_id(nwo), first)
true("...neither of which names the custom domain, which is an address and not a name",
     cname not in b21.FEED_ID)

text = b20.robots()
true("robots.txt points at both sitemaps under SITE",
     f"Sitemap: {SITE}sitemap.xml\n" in text and f"Sitemap: {SITE}sitemap-repos.xml\n" in text, text)
true("...says it is read, because on the custom domain it is the host root's",
     "inert" not in text and cname in text, text)
saved = b17.CNAME
try:
    b17.CNAME = ""
    true("...and says it is inert when there is no custom domain", "inert" in b20.robots())
finally:
    b17.CNAME = saved


# =====================================================================  the spotlight's picture
# Not a link, but this file already loads 31_home.py, and `spot_art()` needs its arms fed directly: which
# one the committed page takes depends on the day's row, so probe.mjs can only check the arm it got.
CARD = b31.b19.og("o/r")
own = "https://raw.githubusercontent.com/o/r/main/banner.png"
eq("the spotlight shows the project's own picture when it has one", re.search(
    r'src="([^"]*)"', b31.spot_art({"img": own, "nwo": "o/r"})).group(1), own)
for gif in ("https://x.io/demo.gif", "https://x.io/demo.GIF?raw=true", "https://x.io/a.gif#frag"):
    eq(f"...but the social card instead of a GIF ({gif.rsplit('/', 1)[1]})", re.search(
        r'src="([^"]*)"', b31.spot_art({"img": gif, "nwo": "o/r"})).group(1), CARD)
eq("...and a PNG whose path merely contains .gif keeps its own picture", re.search(
    r'src="([^"]*)"', b31.spot_art({"img": "https://x.io/a.gifts/b.png", "nwo": "o/r"})).group(1),
   "https://x.io/a.gifts/b.png")
eq("...and the social card when there is no picture at all", re.search(
    r'src="([^"]*)"', b31.spot_art({"img": "", "nwo": "o/r"})).group(1), CARD)
true("...which is never lazy, since it is the first screen's largest element",
     "loading=" not in b31.spot_art({"img": own, "nwo": "o/r"}))


# The mascot is wired only when its loader, model and poster are all committed, so the page never names a
# file that 404s. Both arms, on scratch directories, whatever docs/assets holds today.
saved_out = b31.OUT
try:
    with tempfile.TemporaryDirectory() as tmp:
        b31.OUT = Path(tmp)
        (b31.OUT / "assets").mkdir()
        for f in b31.MASCOT[:-1]:
            (b31.OUT / "assets" / f).write_text("x")
        eq("with any mascot file missing, nothing is wired", b31.mascot(), ("", ""))
        (b31.OUT / "assets" / b31.MASCOT[-1]).write_text("x")
        css, tag = b31.mascot()
        true("with all of them, the poster is the slot's background", "assets/archie-3d.webp" in css, css)
        v = re.fullmatch(r'<script type="module" src="assets/archie\.js\?v=([0-9a-f]{10})"></script>', tag)
        true("...and the loader is a module script, versioned", v, tag)
        a = b31.OUT / "assets"
        (a / "archie.js").write_bytes(b"x\r\ny")
        crlf = b31.mascot_version()
        (a / "archie.js").write_bytes(b"x\ny")
        eq("the version ignores line endings, which differ between a Windows checkout and CI",
           b31.mascot_version(), crlf)
        for f in ("archie.js", "three-archie.js", "archie.glb"):  # not VERSIONED: a name dropped from it must fail
            before = b31.mascot_version()
            (a / f).write_bytes((a / f).read_bytes() + b"!")
            true(f"...and changes when {f} does", b31.mascot_version() != before)
        before = b31.mascot_version()
        (a / "archie-3d.webp").write_bytes(b"changed")
        eq("...but not for the poster, which the page names directly", b31.mascot_version(), before)
        # "Dance with me" rides on the mascot: no model, no button, and no button without its script.
        eq("with the mascot but no dance script, no button", b31.dance(), ("", ""))
        (a / b31.DANCE_JS).write_bytes(b"x\r\ny")
        eq("...nor with the script but not its beat detector", b31.dance(), ("", ""))
        (a / "archie-beat.js").write_bytes(b"b")
        menu, tag = b31.dance()
        true("with it, the button, shipped hidden for the script to reveal",
             re.search(r'<button[^>]*id="dancebtn"[^>]*\bhidden\b', menu), menu[:200])
        v = re.fullmatch(r'<script type="module" src="assets/archie-dance\.js\?v=([0-9a-f]{10})"></script>', tag)
        true("...and the script, versioned", v, tag)
        (a / b31.DANCE_JS).write_bytes(b"x\ny")
        eq("...by its own bytes, line endings aside", b31.dance()[1], tag)
        (a / b31.DANCE_JS).write_bytes(b"x\nz")
        true("...which move it", b31.dance()[1] != tag)
        before = b31.dance()[1]
        (a / "archie-beat.js").write_bytes(b"c")
        true("...as the detector's do, since it is loaded under the same version", b31.dance()[1] != before)
        (a / "archie.glb").unlink()
        eq("and no button when the mascot itself is not wired", b31.dance(), ("", ""))
finally:
    b31.OUT = saved_out


print(f"deeplinks: {ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
