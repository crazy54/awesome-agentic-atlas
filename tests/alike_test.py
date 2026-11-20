"""Lookalikes: the stage `scripts/33_alike.py`, the shared encoder `scripts/semantic.js`, and the wiring.

What this file holds, and why each is here rather than in the two node/browser harnesses:

  the encoder   -- one browser copy, inlined by two generators. The catalogue (`19_pages.py`) and Lookalikes
                   must carry the same bytes of `semantic.js`, and neither may keep a private transcription of
                   `semTokens` beside it: a fourth copy of the tokeniser is the drift with no symptom. Checked
                   on the generators' output rendered here, not on the committed catalogue, because the
                   committed catalogue is rebuilt by the daily and may predate this change.
  the page      -- the generated HTML names itself from `sitewide.ALIKE_PAGE`, inlines the encoder and then
                   the page script, labels its inputs, has a live region and a no-script fallback, writes
                   colour only as custom properties, and is byte-stable across runs (it is committed, and a
                   page that churned daily would be the cost `33_alike.py`'s docstring says it avoids).
  the wiring    -- the stage is in both workflows before `20_landing.py`; its URL is in the sitemap; every
                   page family's nav links it by the constant; the detail page's "Find alternatives" button
                   points at `?repo=<nwo>` for that row and resolves to the page.

The ranking and the resolver are `tests/alike-probe.mjs`'s, which runs the page's own `ALIKE` against the
committed data; the DOM, the forge failures and the themes are `tests/alike-check.mjs`'s.

Run: python tests/alike_test.py
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
import tempfile
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
DOCS = ROOT / "docs"
sys.path.insert(0, str(SCRIPTS))
import sitewide  # noqa: E402
import pagemin  # noqa: E402


def load(name: str, alias: str):
    if alias in sys.modules:
        return sys.modules[alias]
    spec = importlib.util.spec_from_file_location(alias, SCRIPTS / name)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[alias] = mod
    spec.loader.exec_module(mod)
    return mod


b33 = load("33_alike.py", "b33")
b19 = sys.modules["b19"]

ok = bad = 0


def check(name, got, want):
    global ok, bad
    if got == want:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}\n  got  {got!r}\n  want {want!r}")


def true(name, got, detail=""):
    check(name + (f" [{detail}]" if detail and not got else ""), bool(got), True)


# ---------------------------------------------------------------- the name
PAGE = sitewide.ALIKE_PAGE
check("the constant names the page Lookalikes, at /alike/", (PAGE["title"], PAGE["slug"]), ("Lookalikes", "alike"))
true("...with a pitch", len(PAGE.get("pitch", "")) > 20)
check("the stage's PAGE is that constant, not a copy", b33.PAGE is sitewide.ALIKE_PAGE, True)
check("its URL is the slug", b33.urls("https://x/"), ["https://x/" + PAGE["slug"] + "/"])

# ---------------------------------------------------------------- the shared encoder
SEM = (SCRIPTS / "semantic.js").read_text(encoding="utf-8")
SEM_MIN = pagemin.strip_js(SEM)
for fn in ("function semTokens(", "function semEncode(", "async function semDecode(", "const SEM_WORD", "const SEM_DIMS_MAX"):
    true(f"semantic.js defines {fn.split('(')[0].split()[-1]}", fn in SEM)
true("semantic.js has no build placeholder in it, so it can be pasted into either page", "__" not in SEM_MIN)

src19 = (SCRIPTS / "19_pages.py").read_text(encoding="utf-8")
true("19_pages.py inlines semantic.js at a placeholder", "__SEMJS__" in src19 and 'replace("__SEMJS__", pagemin.strip_js(SEMANTIC_JS))' in src19)
for private in ("function semTokens(", "const SEM_WORD =", "const SEM_DIMS_MAX ="):
    check(f"...and keeps no private copy of `{private.split('(')[0]}`", src19.count(private), 0)
true("...and its guard is the shared one", "await semDecode(" in src19)

# Render both pages from the generators as they stand.
data = json.loads((DOCS / "data.json").read_text(encoding="utf-8"))
catalog = b19.substitute(b19.PAGE, data, b19.REPO, b19.b17.SITE)
alike = pagemin.strip_page(b33.render())
check("the catalogue carries the shared encoder exactly once", catalog.count(SEM_MIN.strip()), 1)
check("Lookalikes carries the same bytes exactly once", alike.count(SEM_MIN.strip()), 1)
check("...and no second tokeniser anywhere in the catalogue", catalog.count("function semTokens("), 1)
check("...or in Lookalikes", alike.count("function semTokens("), 1)
true("Lookalikes inlines the encoder before the page script that calls it",
     0 <= alike.find("async function semDecode(") < alike.find("const ALIKE = "))

# ---------------------------------------------------------------- the page
committed = DOCS / PAGE["slug"] / "index.html"
true("the committed page exists", committed.exists())
if committed.exists():
    check("...and is what the stage writes today", committed.read_text(encoding="utf-8").replace("\r\n", "\n"), alike)
with tempfile.TemporaryDirectory() as t:
    import subprocess
    for n in (1, 2):
        subprocess.run([sys.executable, str(SCRIPTS / "33_alike.py"), "--out", str(Path(t) / str(n))],
                       check=True, capture_output=True)
    a, b = ((Path(t) / str(n) / PAGE["slug"] / "index.html").read_bytes() for n in (1, 2))
    check("two runs write the same bytes (nothing dated, nothing counted)", a == b, True)
true("the page names itself from the constant", f'<p class="kick">{PAGE["title"]}</p>' in alike)
true("its title says what it does", re.search(r"<title>Lookalikes: find projects that do the same thing", alike))
true("its canonical URL is the slug", f'<link rel="canonical" href="{b33.SITE}{PAGE["slug"]}/">' in alike)
true("the input is labelled", '<label for="lkq">' in alike and 'id="lkq"' in alike)
true("...and so is the describe box", '<label for="lkdq">' in alike and 'id="lkdq"' in alike)
true("both forms are search landmarks", alike.count('role="search"') == 2)
true("the results are announced in a polite live region", 'id="lklive" aria-live="polite"' in alike)
true("the filters are labelled controls", all(f'<label for="{i}">' in alike for i in ("lklang", "lkstars"))
     and 'id="lkactive"' in alike and "Active in the last 6 months" in alike)
true("a reader with no script is told why, and given somewhere to go", "<noscript>" in alike and 'href="../repo/"' in alike)
true("it fetches data.json and the index from docs/, by the URLs the catalogue uses", 'data-up="../"' in alike
     and 'grab("data.json"' in alike and 'grab("search/docs.bin"' in alike)
css = b33.CSS
check("the page's CSS writes no colour literal (theme tokens only)",
      re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(", css), [])
true("...and paints from the site's custom properties", len(re.findall(r"var\(--", css)) > 20)
true("every focusable thing it draws has a visible focus ring", ":focus-visible" in css and "outline:2px solid var(--link)" in css)
true("it does not restyle the shared shell: every selector is prefixed lk, or is the kicker it shares with Run It Local",
     all(sel.strip().startswith((".lk", ".kick", "html:not(.lkjs)", "@media", "}")) or not sel.strip()
         for sel in re.findall(r"(?:^|})\s*([^{}@]+)\{", css)
         if not sel.strip().startswith(("from", "to"))),
     "")
true("the example starting points are links that work without script",
     all(f'href="{h}"' in alike for h, _ in b33.EXAMPLES))

# ---------------------------------------------------------------- the detail page's button
b22 = load("22_detail.py", "b22")
src22 = (SCRIPTS / "22_detail.py").read_text(encoding="utf-8")
true("22_detail.py builds the button from the constant", 'sitewide.ALIKE_PAGE["slug"]' in src22 and ">Find alternatives</a>" in src22)
true("...beside the existing actions, in the same class, so the layout is untouched",
     re.search(r'<a class="alt" href="\{esc\(live\)\}">Find it in the atlas</a>\s*<a class="alt" href="\{esc\(alike\)\}">Find alternatives</a></p>', src22))
# The link rule, for a GitHub row, a host-qualified GitLab row and a name with an ampersand: `22_detail.py`
# quotes the nwo with `safe="/"` at the depth of the page, and the query string must give the nwo back.
for nwo in ("langfuse/langfuse", "gitlab.com/group/sub/proj", "a/b&c"):
    depth = len(["repo"] + nwo.split("/"))
    href = "../" * depth + PAGE["slug"] + "/?repo=" + urllib.parse.quote(nwo, safe="/")
    q = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
    check(f"the button for {nwo} round-trips its nwo through ?repo=", q.get("repo"), [nwo])
check("the stage's own helper builds the same link", b33.detail_href("../../../", "langfuse/langfuse"),
      "../../../alike/?repo=langfuse/langfuse")

# ---------------------------------------------------------------- the wiring
STAGE = "python scripts/33_alike.py"
for wf in ("daily.yml", "weekly.yml"):
    lines = [ln.strip() for ln in (ROOT / ".github" / "workflows" / wf).read_text(encoding="utf-8").splitlines()]
    true(f"{wf} runs the stage", STAGE in lines)
    if STAGE in lines and "python scripts/20_landing.py" in lines:
        true(f"...before 20_landing in {wf}, which puts its URL in the sitemap",
             lines.index(STAGE) < lines.index("python scripts/20_landing.py"))
landing = (SCRIPTS / "20_landing.py").read_text(encoding="utf-8")
true("20_landing.py asks this stage for its URLs", "def alike_urls()" in landing and "+ alike)" in landing)
sitemap = (DOCS / "sitemap.xml").read_text(encoding="utf-8")
true("the committed sitemap names the page", f"<loc>{b33.urls(b33.SITE)[0]}</loc>" in sitemap)
for f in ("31_home.py", "20_landing.py", "19_pages.py", "19d_discover.py", "25_collections.py"):
    true(f"{f}'s nav links the page by the shared constant", "ALIKE_PAGE" in (SCRIPTS / f).read_text(encoding="utf-8"))
true("the catalogue's nav, rendered, links it once", catalog.count('href="../alike/">Lookalikes</a>') == 1)
true("the page script and the encoder are named in the stage's inputs, so a change to either reaches the page",
     "semantic.js" in (SCRIPTS / "33_alike.py").read_text(encoding="utf-8") and "alike_page.js" in (SCRIPTS / "33_alike.py").read_text(encoding="utf-8"))

print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
