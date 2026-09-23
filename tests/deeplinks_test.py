"""Unit tests for the links into the catalogue, after the catalogue moved from the root to `catalog/`.

The root used to be the catalogue, and a filtered view of it was the root plus a hash: `#topic=x&target=y`,
`#q=name`, `#new=1`. When `31_home.py` took the root and `19_pages.py` moved down to `catalog/`, every
one of those links started landing on the shelves homepage, which reads no hash, so the filter was
dropped without a word. The build stayed green, because no test followed a link.

Two groups:

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


print(f"deeplinks: {ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
