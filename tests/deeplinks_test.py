"""Unit tests for the site's own addresses: the host it is served at, and the links into the catalogue.

The root used to be the catalogue, and a filtered view of it was the root plus a hash: `#topic=x&target=y`,
`#q=name`, `#new=1`. When `31_home.py` took the root and `19_pages.py` moved down to `catalog/`, every
one of those links started landing on the shelves homepage, which reads no hash, so the filter was
dropped without a word. The build stayed green, because no test followed a link.

Four groups, and a fifth that is here only because this file already loads 31_home.py:

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
  the telemetry  -- the three Traceway scripts `telemetry()` writes onto every page family, resolved
                    against every committed page's own URL at all five depths, in order; the two vendored
                    builds pinned to npm's bytes; and the loader, run under node, starting on the host in
                    `docs/CNAME` and on no other, so the test server and a local copy send nothing.
  the spotlight  -- `spot_art()` gives the homepage's spotlight the project's own picture, and the social
                    card for a GIF or no picture. Fed both arms directly, since the committed page
                    shows only whichever one the day's row took.

Nothing here writes to `docs/`. It reads the committed `docs/data.json`, `docs/discover.json` and pages.

Run: python tests/deeplinks_test.py
"""
from __future__ import annotations

import hashlib
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


# =====================================================================  4. the telemetry
# The three Traceway scripts `telemetry()` in 19_pages.py puts on every page, each with a src relative to
# the page that carries it. That is the defect class this file exists for: a src with one `../` too few
# renders, runs nothing and reports nothing, and a reader sees no difference at all. So every committed
# page is resolved, not a sample of them -- the pages sit at five depths, from the homepage down to a
# topic-by-harness crossing, and each family passes its own `up`. `docs/v2/` is `30_v2.py`'s beta, built on
# demand, and carries no telemetry.
b19 = b20.b19
DOCS = ROOT / "docs"
TW = DOCS / "assets"
WANT = [SITE + "assets/" + f for f in b19.TELEMETRY]
TAG = re.compile(r'<script defer src="([^"]*)"></script>')
true("the three files the tags name are committed", all((TW / f).is_file() for f in b19.TELEMETRY),
     [f for f in b19.TELEMETRY if not (TW / f).is_file()])
true("...and the loader is last, since it reads what the other two define",
     b19.TELEMETRY[-1] == "traceway-loader.js")
for up, url in [("", SITE), ("../", CATALOG), ("../../../", SITE + "repo/o/n/"),
                ("../../../../", SITE + "topic/t/target/h/")]:
    eq(f"telemetry({up!r}) resolves from {url}", [urljoin(url, s) for s in TAG.findall(b19.telemetry(up))], WANT)
wrong, walked = [], 0
for p in sorted(DOCS.rglob("index.html")):
    parts = p.relative_to(DOCS).parts[:-1]
    if parts[:1] == ("v2",):
        continue
    walked += 1
    url = SITE + "".join(s + "/" for s in parts)
    got = [urljoin(url, s) for s in TAG.findall(p.read_text(encoding="utf-8"))]
    if got != WANT:
        wrong.append(f"{'/'.join(parts) or '(root)'}: {got}")
true(f"every one of the {walked:,} committed pages loads the three from docs/assets/, in order",
     walked and not wrong, f"{len(wrong):,} do not, e.g.\n  " + "\n  ".join(wrong[:5]))

# The two vendored builds are npm's published bytes, unmodified, and are pinned here so that an edit is a
# red rather than a quietly different SDK. Hashed raw, against this repository's rule of normalising CRLF
# first, because `.gitattributes` marks both files `-text`: every platform checks out the same bytes, and
# a normalised hash would wave through the one change autocrlf could make to them.
PINS = {
    # @tracewayapp/frontend 1.2.1, dist/traceway.iife.global.js
    "traceway-1.2.1.js": "e4855ae39209d50877a2872406d49380207714fb28ac9478f761efb9a0dec743",
    # web-vitals 6.2.3, dist/web-vitals.iife.js
    "web-vitals-6.2.3.js": "1e5e9b9af6b8d71cfef508e5a869c53b4cf2bbccad8c9b5ac664c34e93f6151a",
}
for f, pin in PINS.items():
    eq(f"docs/assets/{f} is the published npm build, byte for byte",
       hashlib.sha256((TW / f).read_bytes()).hexdigest() if (TW / f).is_file() else None, pin)
eq("...and those are the two builds the tags load", sorted(PINS), sorted(b19.TELEMETRY[:-1]))

# The loader, run rather than read, like the forwarder above: a stub `window` per case, and the calls it
# made on it. It must start on the host docs/CNAME names and on nothing else -- not the test server, not
# `localhost`, not a `file://` page (whose hostname is empty), not the github.io URL a fork is served at --
# and not when the SDK did not load. A HOST that drifted from the CNAME would fail no other test and
# silently record nothing.
LOADER = (TW / "traceway-loader.js").read_text(encoding="utf-8") if (TW / "traceway-loader.js").is_file() else ""
CONFIG = "fetch https://blog.jeremyfhall.com/api/telemetry-config?site=aaa"
TW_CASES = [
    ("the test server", "127.0.0.1", True, []),
    ("a local http.server", "localhost", True, []),
    ("a file:// page", "", True, []),
    ("a fork's project URL", "crazy54.github.io", True, []),
    ("the live host, with the SDK missing", cname, False, []),
    ("the live host", cname, True, ["mark the fields", CONFIG]),
]
if node and LOADER:
    harness = r"""
const vm = require("vm");
const [src, cases] = [process.argv[1], JSON.parse(process.argv[2])];
console.log(JSON.stringify(cases.map(([hostname, sdk]) => {
  const calls = [];
  const document = {documentElement: {}, addEventListener: () => calls.push("listen"),
                    querySelectorAll: () => { calls.push("mark the fields"); return []; }};
  const window = {location: {hostname, href: "https://" + hostname + "/"}, document,
                  fetch: u => { calls.push("fetch " + u); return new Promise(() => {}); }};
  if (sdk) window.Traceway = {init: () => calls.push("init")};
  vm.runInNewContext(src, {window, document});
  return calls;
})));
"""
    run = subprocess.run([node, "-e", harness, LOADER, json.dumps([[c[1], c[2]] for c in TW_CASES])],
                         capture_output=True, text=True)
    true("the loader runs under node", run.returncode == 0, run.stderr)
    if run.returncode == 0:
        for (label, *_, want), calls in zip(TW_CASES, json.loads(run.stdout)):
            eq(f"loader on {label}", calls, want)
else:
    true("the loader is committed and node is on PATH", False)


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

# Every file of Archie's that is loaded under the loader's `?v=` has to move that version when it changes,
# or a reader's browser keeps the old copy under an unchanged URL for as long as the CDN's max-age (four
# hours on the live site). The files are enumerated from what is committed in docs/assets, not from
# VERSIONED, since a loop over the list under test cannot notice a name missing from it: `wall-c`/`wall-d`
# and the admin panel were each played or imported under the version and hashed by none of it. Two groups
# are left out, each for a reason of its own: the poster, which the page names directly, and the dance
# script and its detector, which the page loads under a version of their own (tested above).
ASSETS = ROOT / "docs" / "assets"
FAMILY = sorted(p.relative_to(ASSETS).as_posix() for p in ASSETS.rglob("*") if p.is_file()
                and p.relative_to(ASSETS).as_posix().startswith(("archie", "three-archie", "rig"))
                and p.name != "archie-3d.webp" and p.name not in b31.DANCE)
true("the family enumerated off docs/assets includes the four wall clips and the panel",
     {"rig/wall-c.webm", "rig/wall-d.mp4", "archie-admin.js"} <= set(FAMILY), FAMILY)
try:
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copytree(ASSETS, Path(tmp) / "assets")
        b31.OUT = Path(tmp)
        missed = []
        for f in FAMILY:
            p = b31.OUT / "assets" / f
            saved = p.read_bytes()
            before = b31.mascot_version()
            p.write_bytes(saved + b"!")
            if b31.mascot_version() == before:
                missed.append(f)
            p.write_bytes(saved)
        eq(f"each of the {len(FAMILY)} files loaded under archie.js's ?v= moves it", missed, [])
finally:
    b31.OUT = saved_out

# ...and the committed page carries the version the committed assets hash to. The page is generated and the
# assets are hand-written, so an edit to one without a run of 31_home.py leaves a URL that no longer
# describes its file -- which is how a merge of two branches' pages left archie.js and the admin panel on
# two versions, neither of them the one the merged files hash to.
home = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
got = dict(re.findall(r'assets/(archie(?:-admin|-dance)?\.js)\?v=([0-9a-f]+)', home))
want = b31.mascot_version()
eq("the committed homepage loads archie.js under the version its files hash to", got.get("archie.js"), want)
eq("...and the admin panel under the same one", got.get("archie-admin.js"), want)
eq("...and the dance script under its own", got.get("archie-dance.js"), b31.mascot_version(b31.DANCE))


# The newer-version notice. Its button deletes and refills the worker's shell cache by name, so the prefix
# the page substitutes in is the worker's own; and the page's build id is a hash of the page, so it holds
# still across rebuilds of the same bytes and moves with any byte, or every visit would announce a
# deploy -- or none would.
b24 = load("b24", "24_pwa.py")
eq("the notice's shell prefix is the worker's", b31.SHELL_PREFIX, b24.CACHE_PREFIX)
true("...and it is the one substituted into the script",
     "__SHELLPREFIX__" in b31.UPDATE_JS and b31.SHELL_PREFIX not in b31.UPDATE_JS)
shell = f'<meta name="atlas-build" content="{b31.BUILD}"><p>a</p>'
one = b31.stamped(shell)
got = b31.BUILD_META.search(one)
true("a stamped page carries a twelve-hex build id where the placeholder was", got and b31.BUILD not in one, one)
eq("...the same one every time the same page is stamped", b31.stamped(shell), one)
true("...and a different one for a page that differs by a byte",
     b31.BUILD_META.search(b31.stamped(shell.replace("<p>a<", "<p>b<"))).group(1) != got.group(1))


print(f"deeplinks: {ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
