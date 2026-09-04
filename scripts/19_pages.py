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
cached separately from the 1,294 rows that change on every rebuild. And every filter is mirrored into
the URL hash, which is what makes "the best Claude Code observability tool" a link -- the thing the
Markdown pages can only approximate by existing in two directories.
"""
import importlib.util
import json
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

b16 = b17.b16
tax = b17.tax
DASH = b16.DASH
REPO = b17.REPO

# Verdicts compress to one character each because they are printed 6,470 times and there are five of
# them. The page expands them back for display; the JSON is what travels over the wire.
VERDICT = {"Yes": "Y", "Likely": "L", "No": "N", "n/a": "a", DASH: "-", "": "-"}
OS_FIELDS = ["win_native", "win_wsl2", "macos", "linux", "docker"]
OS_LABELS = ["Windows", "WSL2", "macOS", "Linux", "Docker"]

# The columns of `data.json`, in order. Column-oriented rather than one object per repo: the keys would
# otherwise be repeated 1,294 times, which is 380 KB of the word "category". The page maps them back
# into objects once, on load.
COLS = ["name", "nwo", "cat", "targets", "stars", "lists", "listed_by", "os",
        "blurb", "install", "lang", "license", "pushed", "url", "img"]


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
        # thirds of these rows, so spelling it out would be 55 bytes x 1,294 of a string the page can
        # rebuild from `nwo`.
        "" if img == og(r["nwo"]) else img,
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
        # Slugs travel in the URL hash, and they are the same slugs that name the Markdown pages, so a
        # link into this page and a link into `mega-list/topics/` say the same word.
        "cats": [{"name": c, "slug": b17.fileslug(c),
                  "blurb": b17.TOPIC_BLURB.get(c, "")} for c in cats],
        "targets": [{"name": t, "slug": b17.fileslug(t),
                     "blurb": b17.TARGET_BLURB.get(t, "")} for t in tgts],
        "os": OS_LABELS,
        "rows": [row_for(r, shots, cat_ix, tgt_ix) for r in rows],
    }


PAGE = r"""<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Awesome Agentic Atlas — browse every agentic tool</title>
<meta name="description" content="__COUNT__ agentic AI projects from eleven awesome-lists, merged, deduplicated and filterable by topic, harness and operating system.">
<meta property="og:title" content="Awesome Agentic Atlas">
<meta property="og:description" content="__COUNT__ projects from eleven awesome-lists, one filterable index.">
<meta property="og:image" content="https://opengraph.githubassets.com/1/__REPO__">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><text y='13' font-size='14'>&#127760;</text></svg>">
<style>
:root{
  --surface:#1a1a19; --plane:#0d0d0d; --band:#212120; --ink:#fff; --ink2:#c3c2b7;
  --muted:#898781; --grid:#2c2c2a; --link:#86b6ef; --bar:#3987e5;
  --good:#2eb82e; --warn:#fab219; --off:#6e6d68;
}
html[data-theme=light]{
  --surface:#fcfcfb; --plane:#f1f0ec; --band:#f6f5f1; --ink:#0b0b0b; --ink2:#52514e;
  --muted:#898781; --grid:#e1e0d9; --link:#1c5cab; --bar:#2a78d6;
  --good:#0a7c0a; --warn:#8a5a00; --off:#898781;
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
.chip[aria-pressed=true]{background:var(--bar);border-color:var(--bar);color:#fff;font-weight:600}
.count{color:var(--muted);font-size:13px;margin-left:auto;white-space:nowrap}
.count b{color:var(--ink)}
main{padding:0 20px 64px}
table{width:100%;border-collapse:collapse;margin-top:14px}
th{text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);
  padding:8px 10px;border-bottom:1px solid var(--grid);position:sticky;top:0;background:var(--surface)}
th.n,td.n{text-align:right}
th.c,td.c{text-align:center}
td{padding:12px 10px;border-bottom:1px solid var(--grid);vertical-align:top}
tr:hover td{background:var(--band)}
.rk{color:var(--muted);font-size:12px;font-variant-numeric:tabular-nums}
.shot{width:200px}
.shot img{width:200px;aspect-ratio:2/1;object-fit:cover;border-radius:6px;
  background:var(--band);border:1px solid var(--grid);display:block}
.nm{font-weight:600;font-size:15px}
.nwo{display:block;color:var(--muted);font-size:12px;margin-top:2px;word-break:break-all}
.st{font-size:16px;font-weight:700;font-variant-numeric:tabular-nums}
.st.none{font-size:13px;font-weight:400;color:var(--muted)}
.meta{color:var(--muted);font-size:12px;margin-top:5px}
.desc{color:var(--ink2);font-size:13.5px;max-width:44em}
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
@media(max-width:900px){
  .shot,.hide{display:none}
  td,th{padding:9px 6px}
}
</style>
</head>
<body>
<header><div class="wrap"><div class="top">
  <div>
    <h1>Awesome Agentic Atlas <span>· eleven awesome-lists, merged</span></h1>
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
    <span class="count" id="count"></span>
  </div>
  <div class="line"><label>Topic</label><span id="cats"></span></div>
  <div class="line"><label>Plugs into</label><span id="tgts"></span></div>
  <div class="line"><label>Runs on</label><span id="oses"></span>
    <button class="chip" id="strict" aria-pressed="false"
            title="Drop rows where support is inferred from the language rather than stated">Confirmed
      only</button>
    <button class="chip" id="reset">Clear all</button>
  </div>
</div></div>

<main><div class="wrap"><div id="out"></div></div></main>

<footer><div class="wrap">
  Every entry came from someone else's curation work; all eleven source lists are credited in the
  <a href="https://github.com/__REPO__#the-eleven-lists">repository</a>. Stars, language, licence and
  last-push come from the GitHub API on __SNAPSHOT__ and drift daily. Platform verdicts are derived
  from each project's own README, install route, CI config and release assets &mdash;
  <span class="vY">green</span> is stated evidence, <span class="vL">amber</span> is inferred from the
  language. A dash in the star column means the row is a folder inside someone else's repo, or a dead
  link, and has no count of its own.
</div></footer>

<script>
const PAGE_SIZE = 120;
const state = {q: "", cat: "", tgt: "", os: [], strict: false, sort: "stars", shown: PAGE_SIZE};
let D = null, ROWS = [];

fetch("data.json").then(r => r.json()).then(d => {
  D = d;
  // Column-oriented on the wire, objects in here. One pass, 1,294 times, so the rest of the page can
  // read `r.stars` instead of `r[4]`.
  ROWS = d.rows.map(a => Object.fromEntries(d.cols.map((c, i) => [c, a[i]])));
  ROWS.forEach(r => {
    r.hay = (r.name + " " + r.nwo + " " + r.blurb + " " + r.lang + " " + r.listed_by).toLowerCase();
    r.img = r.img || ("https://opengraph.githubassets.com/1/" + r.nwo);
  });
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
  document.getElementById("reset").onclick =
    () => set({q: "", cat: "", tgt: "", os: [], strict: false});
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
    return "<tr>" +
      '<td class="n rk">' + (i + 1) + "</td>" +
      '<td class="shot"><a href="' + url + '"><img loading="lazy" alt="" src="' + img +
        '"></a></td>' +
      '<td><a class="nm" href="' + url + '">' + esc(r.name) + "</a>" +
        '<span class="nwo">' + esc(r.nwo) + "</span>" +
        '<div class="meta">' + os + "</div></td>" +
      '<td class="n"><span class="st' + (r.stars ? "" : " none") + '">' +
        (r.stars ? r.stars.toLocaleString() : "—") + "</span>" +
        '<div class="meta">' + r.lists + (r.lists === 1 ? " list" : " lists") + "</div></td>" +
      '<td class="hide">' + tags + "</td>" +
      '<td><div class="desc">' + esc(r.blurb) + "</div>" +
        (r.install ? '<code class="cmd">' + esc(r.install) + "</code>" : "") + "</td>" +
      '<td class="c hide"><div class="meta">' + esc(r.lang || "—") + "<br>" +
        esc(r.license || "—") + "<br>" + esc(r.pushed || "—") + "</div></td>" +
      "</tr>";
  }).join("");
  out.innerHTML =
    "<table><thead><tr><th class='n'>#</th><th>Shot</th><th>Project</th><th class='n'>Stars</th>" +
    "<th class='hide'>Topic &amp; targets</th><th>What it does</th>" +
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
</body>
</html>
"""


def main() -> None:
    records = b16.prepare(
        json.loads((CACHE / "records_all.json").read_text(encoding="utf-8")), None)
    meta = json.loads((CACHE / "meta.json").read_text(encoding="utf-8"))
    raw_shots = json.loads((CACHE / "shots_all.json").read_text(encoding="utf-8"))
    orch = json.loads((CACHE / "records.json").read_text(encoding="utf-8"))
    orch_shots = json.loads((CACHE / "shots.json").read_text(encoding="utf-8"))
    shots = b16.merged_shots(raw_shots, orch_shots)

    for r in orch:
        r.setdefault("section", r["category"])
        r.setdefault("bucket", r["category"])
        r.setdefault("blurb", r.get("description") or "")
        r.setdefault("src_order", r.get("order", 0))
        r["shot_key"] = (r.get("nwo") or "").replace("/", "__")
        if r.get("license") in ("NOASSERTION", "NONE", DASH, "", None):
            r["license"] = ""
    b16.canonicalise_nwo(records, orch, meta)

    label = {"orchestrators": "Orchestrators", **{k: t for k, t, *_ in b16.SHEETS}}
    tax.STARS.clear()
    tax.STARS.update(b16.star_map(records, orch, meta))
    agg = tax.by_repo(records + [dict(x, source="orchestrators") for x in orch])
    facets = b16.repo_pool(records, orch, label)
    for r in facets:
        a = agg[r["nwo"]]
        r["category"], r["targets"] = a["category"], a["targets"]
        r["stars"] = tax.STARS.get(r["nwo"], 0)

    data = build_data(facets, shots)
    OUT.mkdir(exist_ok=True)
    (OUT / "data.json").write_text(
        json.dumps(data, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
    # Pages runs Jekyll by default, which would try to interpret this directory as a site and skip
    # anything it decided looked like a draft. There is no Jekyll here.
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    page = (PAGE
            .replace("__COUNT__", f"{len(data['rows']):,}")
            .replace("__TOPICS__", str(len(data["cats"])))
            .replace("__STARS__", f"{sum(r[4] for r in data['rows']):,}")
            .replace("__SNAPSHOT__", data["snapshot"])
            .replace("__SITE__", b17.SITE)
            .replace("__REPO__", REPO))
    (OUT / "index.html").write_text(page, encoding="utf-8")

    for f in ("index.html", "data.json"):
        print(f"{f:12s} {(OUT / f).stat().st_size / 1024:8.1f} KB")
    print(f"{len(data['rows']):,} repos · {len(data['cats'])} topics · "
          f"{len(data['targets'])} targets · {sum(r[4] for r in data['rows']):,} stars")


if __name__ == "__main__":
    main()
