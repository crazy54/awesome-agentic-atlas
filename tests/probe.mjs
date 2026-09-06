// Runs the real page script from docs/index.html under a stub DOM against the real docs/data.json, then
// asserts on the HTML it actually renders. Verifying the ranking by reading the source would only confirm
// that I wrote what I meant to write.
//
// WHAT THIS HARNESS CANNOT SEE, which is why there are three of them and not one:
//
// There is no computed layout in Node. Nothing here can tell you the cards are four across, that a 290px
// floor does not overflow a phone, that the screenshot came back, or that a blurb actually clamps -- so the
// cards section below asserts the *stylesheet*, and `cards-check.mjs` measures the result in a browser.
// The split is not redundancy in either direction: a browser cannot see the prefixed `-webkit-line-clamp`
// spelling, because this Chrome implements the standard `line-clamp` and ignores the prefixed one, so a
// clamp rule missing `display:-webkit-box` would pass in the browser and be silently inert in Firefox.
// That assertion can only live here. Neither harness alone would have caught it.
//
// Paths are resolved from this file's own location rather than from the working directory, so `node
// tests/probe.mjs` works from anywhere. It used to be `readFileSync("docs/index.html")`, which was only
// ever correct when run from the repository root.
import {readFileSync} from "node:fs";
import {fileURLToPath} from "node:url";
import {join} from "node:path";

const ROOT = fileURLToPath(new URL("..", import.meta.url));
// `AAA_PAGE` is a development escape hatch, not part of the contract: it lets the text scans at the end of
// this file be pointed at an unsubstituted template while `scripts/pagemin.py` is being worked on. The
// script cannot boot from one -- `__COUNT__` is not a number -- so nothing above the scans will run.
const PAGE = process.env.AAA_PAGE || join(ROOT, "docs/index.html");
const html = readFileSync(PAGE, "utf8");
const data = JSON.parse(readFileSync(join(ROOT, "docs/data.json"), "utf8"));

// The page has several <script> blocks. Picked by content rather than by position: "the last one" was
// true until the service-worker registration was appended after it, and a harness that silently runs the
// wrong 800 lines is worse than one that cannot find them.
const blocks = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
const found = blocks.filter(b => /function relevance/.test(b));
if (found.length !== 1)
  throw new Error(`expected exactly one script block defining relevance(), found ${found.length}`);
const src = found[0];

let OUT = "";
let COUNT = "";
const el = (id) => {
  const cls = new Set();
  const attrs = {};
  const o = {
    id, _text: "", innerHTML: "", value: "", title: "", tabIndex: 0,
    children: [], dataset: {},
    setAttribute(k, v) { attrs[k] = String(v); }, getAttribute(k) { return k in attrs ? attrs[k] : null; },
    removeAttribute(k) { delete attrs[k]; },
    addEventListener(t, fn) { (this._on ??= {})[t] = fn; }, removeEventListener() {},
    appendChild(c) { this.children.push(c); }, append() {},
    querySelector() { return null; }, querySelectorAll() { return []; },
    closest() { return null; }, focus() {}, blur() {}, click() { this.onclick?.(); },
    classList: {
      add: (...c) => c.forEach(x => cls.add(x)), remove: (...c) => c.forEach(x => cls.delete(x)),
      toggle: (c, on) => (on === undefined ? (cls.has(c) ? cls.delete(c) : cls.add(c))
        : on ? cls.add(c) : cls.delete(c)),
      contains: (c) => cls.has(c),
    },
    style: {},
    // <dialog>. `open` is a real property because the Ctrl+K handler branches on it, and `close()` has to
    // clear it or a second press would never reopen the palette.
    open: false,
    showModal() { this.open = true; }, close() { this.open = false; this._on?.close?.(); },
    scrollIntoView() {},
  };
  // The palette reads its Sort group straight off this <select>, so the stub has to carry the real
  // options or the group would silently be empty and the assertion below would pass for the wrong reason.
  //
  // "Rising" is in this list and carries a real `remove()`, and both of those are load-bearing. `buildChips`
  // deletes that <option> on any build whose ledger cannot answer the sort -- which is the state this site
  // ships in until the ledger holds a sample a week old -- so a stub without the entry never reaches the
  // deletion at all, and a stub whose entries have no `remove()` throws a TypeError inside boot the moment
  // it does. The list was missing it and every option was a bare literal, so the one branch that runs on
  // the build we actually publish was the one branch with no coverage.
  if (id === "sort") {
    const opts = [
      {value: "relevance", text: "Best match"}, {value: "stars", text: "Most stars"},
      {value: "rising", text: "Rising"},
      {value: "lists", text: "Named by most lists"}, {value: "pushed", text: "Pushed most recently"},
      {value: "name", text: "Name (A–Z)"},
    ];
    for (const opt of opts) opt.remove = () => {
      const at = opts.indexOf(opt);
      if (at >= 0) opts.splice(at, 1);
    };
    o.options = opts;
  }
  Object.defineProperty(o, "textContent", {
    get() { return o._text; }, set(v) { o._text = String(v); },
  });
  if (id === "out") Object.defineProperty(o, "innerHTML", {
    get() { return OUT; }, set(v) { OUT = v; },
  });
  if (id === "count") Object.defineProperty(o, "innerHTML", {
    get() { return COUNT; }, set(v) { COUNT = v; },
  });
  return o;
};
const CACHE = new Map();
globalThis.document = {
  documentElement: {dataset: {}},
  getElementById(id) { if (!CACHE.has(id)) CACHE.set(id, el(id)); return CACHE.get(id); },
  createElement(t) { return el("<" + t + ">"); },
  createRange() { return {selectNodeContents() {}}; },
  querySelector() { return null; },
  querySelectorAll() { return []; },
  addEventListener() {},
};
// The theme's own --plane in each mode, parsed out of the page's own stylesheet rather than restated
// here: `wire()` writes this value into <meta name=theme-color> so the browser chrome matches the header,
// and a harness carrying its own copy of the hex would happily pass a colour the CSS no longer sets.
const planeOf = (theme) => {
  const rule = theme === "light" ? /html\[data-theme=light\]\{([\s\S]*?)\}/ : /:root\{([\s\S]*?)\}/;
  return html.match(rule)[1].match(/--plane:\s*([^;]+);/)[1].trim();
};
globalThis.getComputedStyle = (elt) => ({
  getPropertyValue: (prop) =>
    prop === "--plane" ? planeOf(elt && elt.dataset && elt.dataset.theme) : "",
});
globalThis.matchMedia = () => ({matches: false, addEventListener() {}});
globalThis.window = {isSecureContext: true, addEventListener() {}, matchMedia: globalThis.matchMedia};
// A real store, not the three no-ops this used to be. The theme bootstrap only ever reads this, so a stub
// that returned null and swallowed writes was enough for it -- but the saved set is *round-tripped* through
// here, and against a no-op store every persistence assertion would pass for the wrong reason: nothing was
// written, nothing came back, and "the set is empty after a reload" is also what a working implementation
// looks like when the reader saved nothing. `STORE` is exposed so the tests can read what the page believes
// it wrote, and seed a session as if a previous one had saved something.
const STORE = new Map();
globalThis.localStorage = {
  getItem: k => (STORE.has(k) ? STORE.get(k) : null),
  setItem(k, v) { STORE.set(k, String(v)); },
  removeItem(k) { STORE.delete(k); },
};
globalThis.location = {hash: "", pathname: "/awesome-agentic-atlas/", href: ""};
globalThis.history = {replaceState() {}, pushState() {}};
globalThis.getSelection = () => ({removeAllRanges() {}, addRange() {}});
Object.defineProperty(globalThis.navigator, "clipboard", {
  value: {writeText: () => Promise.resolve()}, configurable: true,
});
// `headers` matters: the page reads `Last-Modified` off this response to correct the deploy badge, and a
// response object without it throws inside the promise chain, where the page's catch reports it as a
// data.json load failure. Returning null models a local server that sends no such header.
globalThis.fetch = () => Promise.resolve({
  headers: {get: () => null},
  json: () => Promise.resolve(data),
});

// ESM exports are read-only, so module-scoped `let D` cannot be reached from outside. Append a shim that
// hands the internals back rather than trying to poke at them.
const shim = [
  "export const api = {",
  "  get state(){return state}, get ROWS(){return ROWS}, get D(){return D},",
  "  render, match, relevance, hitScore, near, effSort, grams, SORTS, SORT_KEYS,",
  "  readHash, writeHash, applyView,",
  // `RISE` is settable, not just readable, because the published `data.json` can only ever exercise one
  // side of the velocity feature at a time -- and the side it cannot reach is the side that renders.
  "  gained, get RISE(){return RISE}, set RISE(v){RISE=v},",
  "  sheetFilters, paintSheet,",
  // `SAVED` is readable but not settable, on purpose: the tests drive it the way a reader does, through
  // `toggleSave` and `clearsave`, so what they exercise is the persistence and the repaint rather than a
  // Set they assigned themselves. `loadSaved` is exposed because reading the store back is how a *new
  // session* is modelled -- there is no way to re-import the module against the same globals.
  "  get SAVED(){return SAVED}, loadSaved, storeSaved, toggleSave, paintSaved, saveBtn, saveLabel, rescue,",
  "  palItems, palRender, palMove, palPick, palOpen, palWire, PALMOD,",
  "  get PAL(){return PAL}, get PALI(){return PALI}, set PALI(v){PALI=v},",
  '  get OUT(){return document.getElementById("out").innerHTML},',
  '  get COUNT(){return document.getElementById("count").innerHTML},',
  "};",
].join("\n");
const mod = await import("data:text/javascript;base64," +
  Buffer.from(src + "\n" + shim, "utf8").toString("base64"));
const A = mod.api;
await new Promise(r => setTimeout(r, 60));
// Boot has to be a hard stop, not a logged note. The page reports *any* exception thrown anywhere in the
// data.json promise chain as "could not load data.json", so a ReferenceError from a half-generated page
// looks exactly like a file:// permissions problem and blanks the whole atlas. Fail here or every
// assertion below reports on an empty table instead.
if (A.D === null) {
  console.log("BOOT FAILED — the page's own catch handler reported:");
  console.log("  " + A.COUNT.replace(/<[^>]+>/g, ""));
  process.exit(1);
}

let pass = 0, fail = 0;
const ok = (name, cond, extra = "") => {
  if (cond) pass++;
  else { fail++; console.log("FAIL " + name + (extra ? "  -- " + extra : "")); }
};
// Keyed on `nwo`, not on the displayed name. Seven names in the real dataset are duplicated -- OpenCode,
// Orca, Comet and four others -- so a name lookup silently returns the wrong row, and three contain an
// ampersand that the template escapes to `&amp;`, so a name lookup fails outright. `nwo` is the unique key.
// `<a class="nwo" href=...>`, not `<span>`: owner/name became the outward link to GitHub when the project
// title started pointing at the local detail page instead.
const order = () => [...A.OUT.matchAll(/<a class="nwo" href="[^"]*">([^<]*)</g)]
  .map(m => m[1].replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">")
    .replace(/&#39;/g, "'").replace(/&quot;/g, '"'));
const byNwo = n => A.ROWS.find(x => x.nwo === n);
const named = () => order().map(n => (byNwo(n) || {name: "?" + n}).name);
const q = (s, sort = "relevance") => {
  A.state.q = s; A.state.sort = sort; A.state.shown = 600; A.render();
};

ok("rows loaded", A.ROWS.length === data.rows.length, A.ROWS.length + " vs " + data.rows.length);
// Was `length === 5`, which went red the moment "Rising" was added and told you a number rather than a
// property. What actually matters is that the keys and the menu agree: a key with no <option> is a sort
// nobody can reach, and an <option> whose value is not a key silently falls back to relevance, which looks
// like the menu being ignored. So the set is compared against the markup, and only `relevance` being first
// is asserted positionally, because `effSort` depends on that one.
//
// Read off the static markup deliberately. `buildChips` *removes* the "rising" option at runtime on a build
// whose ledger has no history, so the page as served is the only place the full set is visible -- and the
// full set is what SORTS has to cover.
const menu = [...html.matchAll(/<option value="([^"]*)"/g)].map(m => m[1]);
ok("every sort key has a menu entry and every menu entry is a sort key",
   menu.length > 0 && JSON.stringify([...menu].sort()) === JSON.stringify([...A.SORT_KEYS].sort()),
   "menu " + JSON.stringify(menu) + " vs keys " + JSON.stringify(A.SORT_KEYS));
ok("relevance is first, which is what effSort's fallback reads",
   A.SORT_KEYS[0] === "relevance", JSON.stringify(A.SORT_KEYS));

// The graceful-degradation contract for the velocity feature, asserted against the state this site is
// actually published in. `docs/data.json` carries a `velocity` block whose `rise.col` is "" until the ledger
// holds a sample a week old, and on that build there is no such thing as a rising row -- so the chip must
// stay hidden and the sort option must be gone from the menu, or the page offers a filter selecting 0 of
// 1,294 rows and a ranking over a column that is empty everywhere.
//
// Written as an either-or on the data rather than pinned to "off", because this assertion has to keep
// meaning something on the day the ledger fills up and the answer flips. Both branches are checked; which
// one applies is read from the same field the page reads.
const rise = (A.D.velocity || {}).rise || {};
const sortOpts = document.getElementById("sort").options.map(o => o.value);
const riseChip = document.getElementById("rise");
if (rise.col) {
  ok("with history, the Rising sort stays in the menu", sortOpts.includes("rising"),
     JSON.stringify(sortOpts));
  ok("...and the chip is switched on", riseChip.classList.contains("on"));
} else {
  ok("with no history, the Rising sort is removed from the menu", !sortOpts.includes("rising"),
     JSON.stringify(sortOpts));
  ok("...and the chip is left hidden rather than offered", !riseChip.classList.contains("on"));
  ok("...and no row claims a gain", A.ROWS.every(r => r.gain === null),
     String(A.ROWS.filter(r => r.gain !== null).length) + " rows with a gain");
  // The distinction the whole ledger encoding exists to preserve, checked at the page's edge: "we were not
  // watching" must not be drawn as "+0". `gained()` returning "" is what keeps a fabricated zero off 1,294
  // rows, and it is one `=== ""` away from being wrong in a way no layout test would notice.
  ok("...so the star cell draws no gain figure at all", !/class="rise/.test(A.OUT));
}

// `gained()` on fabricated rows, so all three cases are covered on every build regardless of which branch
// above applied. This exists because the branch that actually *renders* a figure has no coverage from the
// published dataset at all -- today `rise.col` is "" and every row's gain is null -- and that is precisely
// where a bug lived: a measured zero used to be drawn as "+0" in `--good` at weight 600, which is the page
// claiming growth on a row that gained none. On a seven-day window most of the long tail of small projects
// genuinely gains nothing, so that was the common case and not an edge one. Fabricated rather than waiting
// for the ledger to fill up, because "covered once the data changes" is not covered.
{
  // Both saved and put back whole, because the assertions after this block read the real ones. A copy is
  // restored rather than the original only if there was nothing to copy.
  const savedRISE = A.RISE, savedVel = A.D.velocity;
  A.RISE = {col: "d30", min_abs: 25, min_pct: 1, days: 30, from: "2026-08-04", span: 30, n: 1239};
  A.D.velocity = Object.assign({}, A.D.velocity, {to: "2026-09-03"});
  const drew = (g) => A.gained({gain: g});
  ok("a positive gain is signed and dressed as a rise",
     /class="rise"/.test(drew(1234)) && />\+1,234</.test(drew(1234)), drew(1234));
  ok("a fall keeps a minus sign and is dressed as a fall",
     /class="rise down"/.test(drew(-45)) && />−45</.test(drew(-45)), drew(-45));
  ok("a zero gain carries no sign, because +0 asserts a direction the number denies",
     !/[+−]0/.test(drew(0)), drew(0));
  ok("...and a zero is dressed as a fall, so the success colour is never spent on no growth",
     /class="rise down"/.test(drew(0)), drew(0));
  ok("an unknown gain draws nothing whatsoever", drew(null) === "", drew(null));
  ok("...so a measured zero and an unknown are still distinguishable at the page's edge",
     drew(0) !== drew(null), `both render ${drew(0)}`);
  ok("the title says which window the figure covers, since the number alone does not",
     /title="[^"]*30 days from 2026-08-04 to 2026-09-03/.test(drew(7)), drew(7));
  A.RISE = savedRISE;
  A.D.velocity = savedVel;
}
ok("default sort is relevance", A.state.sort === "relevance", A.state.sort);
ok("effSort falls back to stars with no query", (A.state.q = "", A.effSort()) === "stars");
ok("effSort keeps relevance with a query", (A.state.q = "x", A.effSort()) === "relevance");

// --- scoring, on synthetic rows so the assertion is about the function and not the dataset ---
const row = (name, blurb = "", stars = 0, lang = "") => ({
  lname: name.toLowerCase(), lnwo: ("o/" + name).toLowerCase(),
  lblurb: blurb.toLowerCase(), name, blurb, stars, lang, listed_by: "",
});
ok("exact name beats prefix", A.hitScore(row("code"), "code") > A.hitScore(row("codex"), "code"));
ok("prefix beats mid-name word boundary",
   A.hitScore(row("Codex CLI"), "code") > A.hitScore(row("Claude Code"), "code"),
   A.hitScore(row("Codex CLI"), "code") + " vs " + A.hitScore(row("Claude Code"), "code"));
ok("word boundary beats inside-a-word",
   A.hitScore(row("Claude Code"), "code") > A.hitScore(row("Decoder"), "code"),
   A.hitScore(row("Claude Code"), "code") + " vs " + A.hitScore(row("Decoder"), "code"));
ok("hyphen counts as a word boundary",
   A.hitScore(row("Claude-Code"), "code") === A.hitScore(row("Claude Code"), "code"));
ok("name hit beats blurb hit",
   A.hitScore(row("Zzz Code"), "code") > A.hitScore(row("Zzz", "a code tool"), "code"));
ok("blurb word-boundary beats blurb mid-word",
   A.hitScore(row("X", "a code tool"), "code") > A.hitScore(row("X", "the decoder"), "code"));
ok("no hit scores zero", A.hitScore(row("Alpha", "beta"), "gamma") === 0);
ok("two words score more than one",
   A.relevance(row("Claude Code"), ["claude", "code"]) > A.relevance(row("Claude Code"), ["claude"]));

// The property that matters most: stars must never lift a blurb match above a name match.
const nameHit = A.relevance(row("Tiny Code", "", 1), ["code"]);
const blurbHit = A.relevance(row("Giant", "a code runner", 400000), ["code"]);
ok("400k stars cannot beat a name match", nameHit > blurbHit,
   nameHit.toFixed(2) + " vs " + blurbHit.toFixed(2));

// --- real data, real render ---
q("crew");
const crew = named();
ok("'crew' ranks a crew-named project first", /crew/i.test(crew[0] || ""),
   "got: " + crew.slice(0, 3).join(" | "));

q("langgraph");
const lg = named();
ok("'langgraph' puts LangGraph first", /langgraph/i.test(lg[0] || ""),
   "got: " + lg.slice(0, 3).join(" | "));
q("langgraph", "stars");
const byStars = named();
ok("relevance genuinely reorders vs stars", lg[0] !== byStars[0],
   "relevance: " + lg[0] + " / stars: " + byStars[0]);

// --- typo fallback ---
q("langraph");
const typo = named();
ok("typo returns near matches instead of nothing", typo.length > 0, "got " + typo.length);
ok("typo shows the banner", /class="approx"/.test(A.OUT));
ok("typo count line says nothing matches exactly", /nothing matches/.test(A.COUNT), A.COUNT);
ok("typo surfaces LangGraph", typo.some(n => /langgraph/i.test(n)),
   "got: " + typo.slice(0, 5).join(" | "));
ok("near matches are capped at 12", typo.length <= 12, "got " + typo.length);

q("langgraph");
ok("exact match shows no banner", !/class="approx"/.test(A.OUT));
ok("exact match count line is the normal one", /with stars/.test(A.COUNT), A.COUNT);

q("zzzqqqxxvvwwyy");
ok("gibberish reaches the empty state", /class="empty"/.test(A.OUT), A.OUT.slice(0, 140));
ok("empty state has no dead did-you-mean button", !/data-q=/.test(A.OUT));
ok("empty state offers clearing everything", /data-all="1"/.test(A.OUT));

// --- the zero-result search link ---
// Cloudflare's beacon blanks the hash before it reports a URL, so `#q=<term>` never leaves the browser and
// no plan upgrade recovers it -- a search that found nothing is the one thing about this page that cannot be
// measured, so the empty branch asks instead. What is worth asserting is the *encoding* of the href it
// composes, and that is precisely what this harness can see and a screenshot cannot.
const missAttr = () => (A.OUT.match(/<a class="miss" href="([^"]*)"/) || [])[1] ?? null;
// `esc()` emits four entities and only one of them can reach this attribute: the term's own `<`, `>` and `"`
// are percent-encoded by `encodeURIComponent` long before `esc()` sees them, so the only thing left needing
// an entity is the pair of bare `&` query separators. That is asserted below rather than assumed, which is
// why reversing just `&amp;` here is safe.
const missHref = () => { const a = missAttr(); return a === null ? null : a.replace(/&amp;/g, "&"); };
const missURL = () => { try { return new URL(missHref()); } catch { return null; } };

q("zzzqqqxxvvwwyy");
ok("a zero-result search offers to report the gap", missAttr() !== null, A.OUT.slice(0, 240));
ok("the link has a style of its own, quieter than the rescue buttons above it",
   html.includes(".empty .miss{"), "no .empty .miss rule in the stylesheet");
q("langgraph");
ok("a search that found something is not asked to report a gap", missAttr() === null, missAttr());

// An empty table with an empty search box has no term to report, so it must not be invited to file
// anything. 38 of the 168 topic x harness pairs select nothing, so one is found rather than named: a
// hardcoded pair would go red the day the data moved and would tell you nothing about the link.
let barren = null;
for (const c of A.D.cats) {
  for (const t of A.D.targets) {
    A.state.q = ""; A.state.cat = c.slug; A.state.tgt = t.slug; A.state.os = [];
    A.state.strict = false; A.state.fresh = false; A.state.rising = false;
    if (A.ROWS.filter(A.match).length === 0) { barren = c.slug + " x " + t.slug; break; }
  }
  if (barren) break;
}
A.state.shown = 600; A.render();
ok("an over-filtered reader with an empty search box is not asked to file anything",
   barren !== null && /class="empty"/.test(A.OUT) && missAttr() === null,
   barren === null ? "no filter pair selects zero rows, so the no-term case went untested"
                   : barren + " -> " + missAttr());
A.state.cat = ""; A.state.tgt = "";

// Spaces, an ampersand, a fragment marker, a quote, an angle bracket, a plus and two non-Latin scripts, in
// one term, because the href is built by concatenation and each of those breaks a different layer: the query
// string, the HTML attribute, or the form decoder that reads it back. `zzqqxx` is only there to guarantee the
// empty branch; the rest of the term is the test.
const tricky = 'kubernetes & rancher #k3s "café" <b> a+b 日本語 zzqqxx';
globalThis.location.hash = "#topic=agents&confirmed=1";
q(tricky);
const u = missURL();
ok("a term full of URL metacharacters still yields a well-formed absolute URL", u !== null,
   String(missAttr()).slice(0, 200));
ok("it opens a prefilled issue on this repository, labelled for triage",
   u !== null && u.origin === "https://github.com" && u.pathname.endsWith("/issues/new") &&
   u.pathname.split("/").length === 5 && u.searchParams.get("labels") === "coverage",
   u && u.origin + u.pathname + " labels=" + (u && u.searchParams.get("labels")));
ok("the term round-trips through the encoding character for character",
   u !== null && (u.searchParams.get("title") || "").includes(tricky),
   u && JSON.stringify(u.searchParams.get("title")));
// The filters and the snapshot are what turn "someone searched for X" into a report somebody can act on:
// "kubernetes, confirmed-only, Windows" and "kubernetes" are different findings and only one is a gap.
ok("the body carries the term, the active filters and the snapshot",
   u !== null && (u.searchParams.get("body") || "").includes("Searched for: " + tricky) &&
   (u.searchParams.get("body") || "").includes("Filters: topic=agents&confirmed=1") &&
   (u.searchParams.get("body") || "").includes("Snapshot: " + data.snapshot),
   u && JSON.stringify(u.searchParams.get("body")));
ok("the two query separators are escaped for the attribute, and nothing else had to be",
   missAttr() !== null && missAttr().includes("&amp;title=") && missAttr().includes("&amp;body=") &&
   !/&(?!amp;)/.test(missAttr()), missAttr());
ok("every space, fragment marker and non-ASCII character is percent-encoded, not passed through",
   missAttr() !== null && /^[!-~]+$/.test(missAttr()) && !missHref().includes("#"), missAttr());

// A term long enough to be cut, with an astral character sitting exactly on the cut. `.slice(0, 80)` counts
// UTF-16 units, so it would split the surrogate pair and leave a lone surrogate -- and `encodeURIComponent`
// throws URIError on one, which would come out of the `innerHTML` expression in render() and blank the empty
// state rather than show it. The cut has to fall between code points; these three assertions say so.
const octopus = String.fromCodePoint(0x1f419);
const boundary = "zzqqxx " + "qxzvbnm ".repeat(9) + octopus + " wqxz";
let threw = null;
try { q(boundary); } catch (e) { threw = e; }
ok("a term truncated across a surrogate pair does not throw out of render()", threw === null,
   threw && String(threw));
const ub = threw ? null : missURL();
ok("the astral character sitting on the 80-code-point boundary survives whole",
   ub !== null && (ub.searchParams.get("title") || "").includes(octopus),
   ub && JSON.stringify(ub.searchParams.get("title")));
ok("and the cut really happened -- nothing past the boundary reaches the issue title",
   ub !== null && !(ub.searchParams.get("title") || "").includes("wqxz"),
   ub && JSON.stringify(ub.searchParams.get("title")));
globalThis.location.hash = "";

// --- the fallback must relax only the search box ---
const catSlug = A.D.cats[0].slug;
A.state.q = "langraph"; A.state.cat = catSlug; A.state.sort = "relevance"; A.state.shown = 600;
A.render();
const scoped = named();
// `length > 0` is not padding, and the same conjunct appears on the three other `every()` assertions below.
// `[].every(...)` is `true`, so each of these would have passed on a query that matched nothing at all --
// which is the one outcome that would mean the fallback is broken. An assertion that cannot fail is worse
// than a missing one, because it reports that it checked.
const fellBack = order();
const inCat = fellBack.length > 0 && fellBack.every(n => {
  const r = byNwo(n);
  return r && A.D.cats[r.cat].slug === catSlug;
});
ok("near matches stay inside the active topic filter", inCat,
   fellBack.length === 0
     ? "the fallback returned no rows at all, so there was nothing to be inside the filter"
     : "topic " + catSlug + " got: " + scoped.join(" | "));
ok("banner names the other filters when there are some",
   !/class="approx"/.test(A.OUT) || /within your other filters/.test(A.OUT));
A.state.cat = "";

// --- state hygiene: near() borrows state.q and must give it back ---
A.state.q = "langraph";
A.near("langraph");
ok("near() restores state.q", A.state.q === "langraph", A.state.q);

// --- hash round-trip for the new default ---
globalThis.location.hash = "#sort=stars";
A.readHash();
ok("readHash honours an existing #sort=stars link", A.state.sort === "stars", A.state.sort);
globalThis.location.hash = "#sort=bogus";
A.readHash();
ok("readHash rejects an unknown sort", A.state.sort === "relevance", A.state.sort);
globalThis.location.hash = "";
A.readHash();
ok("readHash defaults to relevance", A.state.sort === "relevance", A.state.sort);

// --- every sort mode still renders ---
for (const k of A.SORT_KEYS) {
  q("agent", k);
  ok("sort mode " + k + " renders rows", order().length > 0);
}

// --- rel must be defined for every row the relevance comparator sees, and the order must respect it ---
q("agent", "relevance");
const hits = A.ROWS.filter(A.match);
ok("every matching row has a numeric rel",
   hits.length > 0 && hits.every(r => typeof r.rel === "number" && !Number.isNaN(r.rel)),
   hits.length + " rows matched");
const rels = order().map(n => byNwo(n).rel);
let mono = true;
for (let i = 1; i < rels.length; i++) if (rels[i] > rels[i - 1] + 1e-9) mono = false;
ok("rendered order is non-increasing in rel", rels.length > 1 && mono, rels.length + " rows to order");

// --- the AND semantics of multi-word search are unchanged ---
q("claude code");
const both = order();
ok("multi-word search still requires every word",
   both.length > 0 && both.every(n => {
     const r = byNwo(n);
     return r && r.hay.includes("claude") && r.hay.includes("code");
   }), "n=" + both.length);

// ---- rows link inward to the detail page, outward via owner/name -----------------------------------
q("agent", "stars");
A.state.shown = 60; A.render();
const titles = [...A.OUT.matchAll(/<a class="nm" href="([^"]*)"/g)].map(m => m[1]);
const outs = [...A.OUT.matchAll(/<a class="nwo" href="([^"]*)"/g)].map(m => m[1]);
const shots = [...A.OUT.matchAll(/<td class="shot"><a href="([^"]*)"/g)].map(m => m[1]);
ok("every row title links to a local detail page",
   titles.length > 0 && titles.every(h => /^repo\/[^"]+\/$/.test(h)), titles[0]);
ok("every row still has a way out to the repository",
   outs.length === titles.length && outs.every(h => /^https?:\/\//.test(h)), outs[0]);
ok("the shot link goes where the title goes, which is what lets it stay aria-hidden",
   shots.length === titles.length && shots.every((h, i) => h === titles[i]));
ok("detail slugs are lowercased and dot-prefixes rewritten",
   titles.every(h => h === h.toLowerCase() && !/\/\./.test(h)),
   titles.find(h => h !== h.toLowerCase() || /\/\./.test(h)));
ok("the footer offers the project directory as a crawlable path",
   /<a href="repo\/">/.test(html), "not in the page shell");

// ---- command palette -------------------------------------------------------------------------------
const dlg = document.getElementById("pal");
const palq = document.getElementById("palq");
const palList = () => document.getElementById("palist").innerHTML;
// Unescaped, for the same reason `order()` is: "Sandbox & security" renders as `Sandbox &amp; security`,
// so a raw comparison against D.cats[].name fails on every topic containing an ampersand.
const unesc = s => s.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">")
  .replace(/&#39;/g, "'").replace(/&quot;/g, '"');
const palLabels = () => [...palList().matchAll(/<span class="t">([^<]*)</g)].map(m => unesc(m[1]));
const palGroups = () => [...palList().matchAll(/class="grp"[^>]*>([^<]*)</g)].map(m => m[1]);
const openPal = (text = "") => { A.palOpen(); palq.value = text; A.PALI = 0; A.palRender(); };

A.state.q = ""; A.state.cat = ""; A.state.tgt = ""; A.state.os = [];
A.state.strict = false; A.state.fresh = false; A.state.sort = "relevance";

ok("palette hint says Ctrl off a non-Mac platform string", A.PALMOD === "Ctrl", A.PALMOD);
openPal();
ok("palette opens", dlg.open === true);
// With an empty box the palette is a menu of the page's own controls; 1,294 repos there would bury them.
ok("empty palette offers controls, not projects", !palGroups().includes("Projects"),
   palGroups().join(","));
ok("empty palette covers every control group",
   ["Topic", "Plugs into", "Runs on", "Sort", "Filter", "Page"].every(g => palGroups().includes(g)),
   palGroups().join(","));
ok("empty palette lists every topic",
   A.D.cats.every(c => palLabels().includes(c.name)), palLabels().length + " labels");
ok("Sort group comes off the real <select>",
   palLabels().includes("Best match") && palLabels().includes("Pushed most recently"));
ok("first item starts selected", /id="pal-0" aria-selected="true"/.test(palList()));
ok("input points at the highlighted option",
   palq.getAttribute("aria-activedescendant") === "pal-0", palq.getAttribute("aria-activedescendant"));

A.palMove(1);
ok("arrow down moves the highlight", /id="pal-1" aria-selected="true"/.test(palList()) &&
   palq.getAttribute("aria-activedescendant") === "pal-1");
A.palMove(-1); A.palMove(-1);
ok("arrow up from the top wraps to the last item", A.PALI === A.PAL.length - 1, String(A.PALI));

// Substring, so typing part of a long facet label reaches it.
openPal("sand");
ok("'sand' finds a Sandbox topic", palLabels().some(l => /sandbox/i.test(l)), palLabels().join(" | "));
openPal("dock");
ok("'dock' finds the Docker platform", palLabels().includes("Docker"), palLabels().join(" | "));
openPal("push");
ok("'push' finds the pushed sort", palLabels().includes("Pushed most recently"), palLabels().join(" | "));
openPal("clear");
ok("'clear' finds Clear all filters", palLabels().includes("Clear all filters"), palLabels().join(" | "));

// A query surfaces projects as a second section, ranked by the same scorer the table uses.
openPal("langgraph");
ok("a query adds a Projects group", palGroups().includes("Projects"), palGroups().join(","));
const palProj = palLabels().slice(palLabels().indexOf(
  palLabels().find(l => /langgraph/i.test(l))));
ok("palette projects lead with LangGraph", /langgraph/i.test(palProj[0] || ""), palProj.slice(0, 3).join(" | "));
ok("palette caps projects at 8", palProj.length <= 8, String(palProj.length));
openPal("zzzqqqxxvvwwyy");
ok("a hopeless query says so instead of rendering an empty list",
   /class="palnone"/.test(palList()) && A.PAL.length === 0);
ok("hopeless query drops aria-activedescendant",
   palq.getAttribute("aria-activedescendant") === null);

// Picking has to close the dialog *before* it re-renders the table, or the modal sits over a table that
// already changed and the keystroke reads as if it did nothing.
openPal("sand");
const sandIx = A.PAL.findIndex(a => a.group === "Topic" && /sandbox/i.test(a.label));
ok("a Sandbox topic action exists", sandIx >= 0);
A.PALI = sandIx; A.palPick();
ok("picking a topic closes the palette", dlg.open === false);
ok("picking a topic applies the filter", A.state.cat && /sandbox/i.test(A.state.cat), A.state.cat);
ok("the applied topic reaches the hash", /topic=/.test(globalThis.location.hash) ||
   A.D.cats.some(c => c.slug === A.state.cat), A.state.cat);

// The active marker reflects live state, so reopening shows what is already on.
openPal();
const catItem = A.PAL.find(a => a.group === "Topic" && a.label ===
  A.D.cats.find(c => c.slug === A.state.cat).name);
ok("the current topic is marked active", catItem && catItem.active === true);
ok("an active item renders 'on' rather than a tick glyph", /<span class="k">on<\/span>/.test(palList()));

// A platform toggle has to toggle, not just add.
A.state.os = []; A.state.cat = "";
openPal("linux");
const osIx = A.PAL.findIndex(a => a.group === "Runs on");
A.PALI = osIx; A.palPick();
const afterAdd = A.state.os.slice();
ok("picking a platform adds it", afterAdd.length === 1, JSON.stringify(afterAdd));
openPal("linux");
A.PALI = A.PAL.findIndex(a => a.group === "Runs on"); A.palPick();
ok("picking the same platform again removes it", A.state.os.length === 0, JSON.stringify(A.state.os));

// Sort picked from the palette must also move the <select>, or the menu and the table disagree.
openPal("name");
// Exact label, not a prefix: "Named by most lists" also begins with "Name", so a /^Name/ match picks the
// wrong sort and the assertion below passes or fails for a reason that has nothing to do with the page.
const nameIx = A.PAL.findIndex(a => a.group === "Sort" && a.label === "Name (A–Z)");
ok("both 'name' sorts are offered and they are distinguishable", nameIx >= 0,
   A.PAL.filter(a => a.group === "Sort").map(a => a.label).join(" | "));
A.PALI = nameIx; A.palPick();
ok("picking a sort sets state.sort", A.state.sort === "name", A.state.sort);
ok("picking a sort also moves the <select>",
   document.getElementById("sort").value === "name", document.getElementById("sort").value);

// Clear all from the palette has to clear everything, including the search box.
A.state.q = "agent"; A.state.cat = A.D.cats[0].slug; A.state.strict = true;
openPal("clear");
A.PALI = A.PAL.findIndex(a => a.label === "Clear all filters"); A.palPick();
ok("Clear all from the palette clears every filter",
   !A.state.q && !A.state.cat && !A.state.strict && !A.state.os.length && !A.state.fresh,
   JSON.stringify({q: A.state.q, cat: A.state.cat, strict: A.state.strict}));

// The escape hatch: the palette must never be the only way to reach something, and it must not open at
// all where <dialog> is unsupported.
ok("the hint is only shown once showModal is confirmed",
   document.getElementById("palhint").classList.contains("on"));
ok("the hint names the modifier", /Ctrl/.test(document.getElementById("palhint").innerHTML),
   document.getElementById("palhint").innerHTML);

// Each heading must appear at most once. A flat score sort interleaved groups and printed "Topic" twice,
// which reads as a rendering fault; the check is on the rendered HTML because that is where it showed.
for (const term of ["a", "e", "agent", "s", "o", "cl", "code", "linux", "new", "the"]) {
  openPal(term);
  const gs = palGroups();
  ok("no repeated group heading for " + JSON.stringify(term), gs.length === new Set(gs).size,
     gs.join(" > "));
}
// ...and the globally best-scoring item must still be first, which is the property the grouping could
// plausibly have broken.
openPal("dock");
ok("grouping keeps the best match first", palLabels()[0] === "Docker", palLabels().slice(0, 3).join(" | "));
openPal("confirmed");
ok("a unique action ranks first over any group order",
   palLabels()[0] === "Confirmed platform support only", palLabels().slice(0, 3).join(" | "));
// Projects stay last regardless of how the action groups reorder, so the accelerator never buries a
// control behind eight repositories.
openPal("agent");
const gsA = palGroups();
ok("Projects is always the final group", gsA[gsA.length - 1] === "Projects", gsA.join(" > "));

A.state.sort = "relevance"; A.state.q = "";

// ---------------------------------------------------------------- installability and browser chrome
// The head tags, asserted on the built page rather than on the template, and in document order: the
// pre-paint script sets the meta's content, so a meta that moved below it would silently do nothing.
const iTc = html.indexOf('<meta name="theme-color" id="tc"');
const iPre = html.indexOf('var t = localStorage.getItem("theme")');
ok("the manifest is linked", /<link rel="manifest" href="manifest\.webmanifest">/.test(html));
ok("the manifest link is relative, so the Pages path prefix applies",
   !/<link rel="manifest" href="\//.test(html));
ok("an apple-touch-icon is linked", /<link rel="apple-touch-icon" href="apple-touch-icon\.png">/.test(html));
ok("there is exactly one theme-color meta",
   (html.match(/name="theme-color"/g) || []).length === 1);
ok("the theme-color meta precedes the script that writes it", iTc > 0 && iPre > 0 && iTc < iPre,
   iTc + " vs " + iPre);
ok("its no-JS value is the dark theme's --plane, matching the data-theme=dark floor",
   html.slice(iTc, iTc + 120).includes('content="' + planeOf("dark") + '"'),
   planeOf("dark") + " -- " + html.slice(iTc, iTc + 90));

// And the live behaviour: `wire()` has already run, so the chrome must agree with the theme now, and it
// must keep agreeing across a toggle. This is the half two `media` metas could not have done.
const tc = document.getElementById("tc");
ok("wire() set the chrome from the stylesheet", tc.content === planeOf(undefined),
   tc.content + " vs " + planeOf(undefined));
document.getElementById("theme").click();
ok("toggling to light repaints the chrome", document.documentElement.dataset.theme === "light" &&
   tc.content === planeOf("light"), tc.content + " vs " + planeOf("light"));
ok("the two themes do not share a --plane", planeOf("light") !== planeOf("dark"));
document.getElementById("theme").click();
ok("toggling back repaints it again", document.documentElement.dataset.theme === "dark" &&
   tc.content === planeOf("dark"), tc.content);

// The registration, which the harness cannot execute -- there is no service worker in Node -- so this
// asserts the two guards that decide whether it ever runs, and that it is the last script on the page.
const reg = html.match(/<script>\s*if \("serviceWorker" in navigator[\s\S]*?<\/script>/);
ok("the service worker is registered", !!reg);
ok("registration is guarded against file://", !!reg && /location\.protocol !== "file:"/.test(reg[0]));
ok("registration waits for load", !!reg && /addEventListener\("load"/.test(reg[0]));
ok("the worker is never read from the HTTP cache", !!reg && /updateViaCache: "none"/.test(reg[0]));
ok("a failed registration cannot reach the reader", !!reg && /\.catch\(\(\) => \{\}\)/.test(reg[0]));
ok("registration comes after the application script",
   !!reg && html.indexOf(reg[0]) > html.indexOf("function relevance"));

// ------------------------------------------------------------------------------- the cards view
// The layout itself is a stylesheet, so it is asserted against the stylesheet -- there is no computed
// layout in Node to measure. What this section can prove is the half that would break silently: that the
// switch is state and not a second render path, that the state round-trips through the hash, and that every
// rule which has to outrank the two responsive blocks actually carries the prefix that makes it.
A.state.q = ""; A.state.cat = ""; A.state.tgt = ""; A.state.os = []; A.state.strict = false;
A.state.view = "table"; A.render();

const vb = document.getElementById("view");
ok("the view toggle is revealed once the data has arrived", vb.hidden === false, String(vb.hidden));
ok("the table is the default view", A.state.view === "table" && A.OUT.includes("<table>"), A.state.view);
ok("the toggle's label is the action, not the state", vb.textContent === "Card view", vb.textContent);
ok("the default needs no attribute story of its own",
   document.documentElement.dataset.view === "table", document.documentElement.dataset.view);

// The property the whole design rests on: switching must not touch a row. Snapshot the rendered HTML,
// click, and require it to be byte-identical -- that is what proves no refetch, no re-sort and no rebuild,
// and it is the only assertion here that a second render path could not fake.
const beforeHTML = A.OUT, beforeLen = A.ROWS.length;
vb.click();
ok("switching to cards changes no markup at all", A.OUT === beforeHTML,
   A.OUT.length + " vs " + beforeHTML.length);
ok("...and no row was refetched or reparsed", A.ROWS.length === beforeLen);
ok("switching sets the attribute the stylesheet reads",
   document.documentElement.dataset.view === "cards", document.documentElement.dataset.view);
ok("the label flips to the way back", vb.textContent === "Table view", vb.textContent);
// `say()` clears the region and sets it on a 30ms timer -- a live region only fires on a change, so the
// clear is what makes two identical announcements announce twice. Waiting is the harness matching the
// page's own timing, not papering over a race in it.
await new Promise(r => setTimeout(r, 60));
ok("the switch is announced, since nothing in the DOM changed to announce it",
   /card view/i.test(document.getElementById("live").textContent),
   JSON.stringify(document.getElementById("live").textContent));

// `shown` is why this does not go through `set()`. A reader four pages in must not be sent back to row 120
// for asking to see the screenshots.
A.state.shown = 600;
vb.click(); vb.click();
ok("toggling the view does not reset the page size", A.state.shown === 600, String(A.state.shown));
A.state.shown = 120;

// The hash: shareable, survives a reload, and defaults hard on anything it does not recognise.
//
// Cards are the default now, so the table is the view that has to appear in the hash and cards is the one
// that has to stay out of it. Both words are still read explicitly, which is what keeps a `#view=cards`
// link written while cards were opt-in meaning what it said -- so both are asserted, not just the opt-in
// one. Each readHash case sets `state.view` to the *other* value first: without that the state already
// holds the expected answer when the check runs, and the assertion passes whether readHash ran or not.
A.state.view = "table";
let written = "";
globalThis.history.replaceState = (a, b, url) => { written = url; };
A.writeHash();
ok("the opt-in view is written into the hash", /(^|[#&])view=table/.test(written), written);
A.state.view = "cards"; A.writeHash();
ok("the default is left out of the hash", !/view=/.test(written), written);

globalThis.location.hash = "#view=cards";
A.state.view = "table";
A.readHash();
ok("a #view=cards link is honoured", A.state.view === "cards", A.state.view);
globalThis.location.hash = "#view=table";
A.state.view = "cards";
A.readHash();
ok("a #view=table link is honoured", A.state.view === "table", A.state.view);
globalThis.location.hash = "#view=grid";
A.state.view = "table";
A.readHash();
ok("an unknown view falls back to the default", A.state.view === "cards", A.state.view);
globalThis.location.hash = "#topic=" + A.D.cats[0].slug + "&view=cards";
A.readHash();
ok("the view survives alongside the other filters",
   A.state.view === "cards" && A.state.cat === A.D.cats[0].slug,
   A.state.view + " / " + A.state.cat);
// And render() is what makes a hashchange or a back button arrive at the right layout, which is why the
// attribute write lives there and not only on the click.
document.documentElement.dataset.view = "table";
A.render();
ok("render() re-applies the view, so a hashchange lands on the right layout",
   document.documentElement.dataset.view === "cards", document.documentElement.dataset.view);
globalThis.location.hash = "";
A.readHash(); A.render();

// The palette offers it, and offers the action rather than the state -- the same rule the theme entry
// follows, so it can never propose the view the reader is already in.
A.state.view = "cards";
openPal("view");
ok("the palette offers the way back out of cards",
   A.PAL.some(a => a.group === "Page" && a.label === "Table view"),
   A.PAL.filter(a => a.group === "Page").map(a => a.label).join(" | "));
A.state.view = "table";
openPal("card");
const cardEntry = A.PAL.findIndex(a => a.label === "Card view");
ok("the palette offers the cards view", cardEntry >= 0,
   A.PAL.filter(a => a.group === "Page").map(a => a.label).join(" | "));
A.PALI = cardEntry; A.palPick();
ok("picking it from the palette goes through the button", A.state.view === "cards" &&
   document.documentElement.dataset.view === "cards", A.state.view);
A.state.view = "table"; A.applyView();

// Every cards rule has to beat `.shot,.hide{display:none}` at 900px and the whole card block at 640px, and
// it does that on specificity -- one attribute selector on <html> -- rather than on source order or on
// !important. So the thing to assert is that no rule in the block lost its prefix, because a rule that did
// would apply in *both* views and break the table for everyone.
//
// Found by selector rather than by slicing the stylesheet between two prose markers. It used to be
// `html.indexOf("---- Cards view")` up to `html.indexOf("prefers-reduced-motion")`, which was a comment
// and a rule name -- and `scripts/pagemin.py` (JFH-204) now strips every comment out of the page on the way
// out, so that anchor is gone. Collecting by prefix is the better test anyway: it asserts the property
// itself rather than the property within a region a comment happened to delimit, and it cannot drift when
// somebody adds a rule below the marker they were slicing to.
//
// The comment-stripping step that used to sit here -- `.replace(/\/\*[\s\S]*?\*\//g, "")` -- is gone with
// it. There are no comments left in the served page to strip; the scan at the end of this file is what
// asserts that. It mattered when there were, because this block's own prose quoted
// `.shot,.hide{display:none}` as the rule it has to beat and used the word !important to say it does not
// need one, so a scan that could see comments found both and reported the explanation as the defect.
const CARD = "html[data-view=cards]";
// Brace-matched rather than regex-matched, so `@media(hover:hover){...}` yields the two rules nested
// inside it with the at-rule recorded rather than being stepped over -- those two are the ones that undo
// the table's row tint, and the ones an unprefixed selector would do the most damage in, flattening it in
// both views. A regex for `{...}` with no brace inside walks straight into them and reports the at-rule
// itself as a selector.
//
// Assumes no `{` or `}` inside a CSS string. The one string in this stylesheet is `content:"#"`, and a
// brace in a `content` value would be the only way to break this; it would break it loudly, by producing
// nonsense selectors, rather than by passing quietly.
const cssRules = (text) => {
  const out = [];
  const walk = (src, at) => {
    let i = 0;
    while (i < src.length) {
      const open = src.indexOf("{", i);
      if (open < 0) break;
      let depth = 1, j = open + 1;
      while (j < src.length && depth > 0) {
        if (src[j] === "{") depth++;
        else if (src[j] === "}") depth--;
        j++;
      }
      const head = src.slice(i, open).trim().replace(/\s+/g, " ");
      const body = src.slice(open + 1, j - 1);
      if (head.startsWith("@") && body.includes("{")) walk(body, head);
      else out.push({at, sel: head, body});
      i = j;
    }
  };
  walk(text, "");
  return out;
};
const styles = [...html.matchAll(/<style>([\s\S]*?)<\/style>/g)].map(m => m[1]).join("\n");
const cardRules = cssRules(styles).filter(r => r.sel.includes(CARD));
// Rebuilt with the at-rule wrapped back around each rule, so the assertions below can go on reading one
// string and one of them can still say "and only where a pointer can actually hover".
const cardsBlock = cardRules
  .map(r => (r.at ? r.at + "{" : "") + r.sel + "{" + r.body + "}" + (r.at ? "}" : ""))
  .join("\n");

ok("there is a stylesheet to read at all", styles.length > 5000, String(styles.length));
ok("the cards block was emitted at all", cardRules.length > 10, String(cardRules.length));
// Every comma-separated part, not just the first: `html[data-view=cards] td.shot, td.hide{...}` is the
// realistic regression and it is half-scoped, so a check on the rule as a whole would pass it.
//
// What this cannot catch, said plainly: a rule that lost the prefix on *every* part is no longer a cards
// rule by this definition and is not collected, so it cannot be reported as unscoped. The named
// assertions below are what cover that -- each one looks for a specific rule by its prefixed selector, so
// a rule that dropped the prefix entirely fails the assertion that expects it.
ok("every selector in it is scoped to the cards view",
   cardRules.every(r => r.sel.split(",").every(p => p.trim().startsWith(CARD))),
   cardRules.filter(r => r.sel.split(",").some(p => !p.trim().startsWith(CARD)))
     .map(r => r.sel).join(" | "));
ok("nothing in it needed !important", !/!important/.test(cardsBlock));
ok("the screenshot column comes back, which is the whole point of the view",
   /html\[data-view=cards\] td\.shot\{[^}]*display:block/.test(cardsBlock) ||
   /html\[data-view=cards\] td\{display:block/.test(cardsBlock),
   cardsBlock.match(/td\.shot\{[^}]*\}/)?.[0] || "no td.shot rule");
ok("the image fills the card rather than keeping its 200px table width",
   /html\[data-view=cards\] td\.shot img\{[^}]*width:100%/.test(cardsBlock));
ok("the headings are dropped, since a card has nothing to head",
   /html\[data-view=cards\] thead\{display:none\}/.test(cardsBlock));
ok("the grid sizes itself, so there is no second breakpoint to keep in step",
   /auto-fill,\s*minmax\(/.test(cardsBlock), cardsBlock.match(/grid-template-columns:[^;}]*/g)?.join(" | "));
ok("the two hidden columns come back on a card, as they do on a phone",
   /html\[data-view=cards\] td\.hide\{display:block\}/.test(cardsBlock));
ok("the row's 9px phone margin is zeroed against the grid gap that replaced it",
   /html\[data-view=cards\] tr\{[^}]*margin:0/.test(cardsBlock),
   cardsBlock.match(/html\[data-view=cards\] tr\{[^}]*\}/)?.[0]);
ok("the row tint is undone, or it would band the inside of every card",
   /html\[data-view=cards\] tr:hover td\{background:transparent\}/.test(cardsBlock));
ok("...and only where a pointer can actually hover",
   /@media\(hover:hover\)\{\s*html\[data-view=cards\] tr:hover td/.test(cardsBlock));
ok("the rank gets its heading back as a glyph, the column heading being gone",
   /html\[data-view=cards\] td\.rk::before\{content:"#"\}/.test(cardsBlock));
// `-webkit-line-clamp` is inert on its own: without `display:-webkit-box` and a vertical box-orient beside
// it the blurb simply does not clamp, and it fails that way silently. A browser doing the standard
// `line-clamp` never notices the omission, which is exactly why this is checked here rather than in
// cards-check.mjs -- that harness runs one such browser, and it would pass eleven ways.
const clampRule = cardsBlock.match(/html\[data-view=cards\] \.desc\{[^}]*\}/)?.[0] || "";
ok("the blurb is clamped on a card, where the row's height is the tallest of four",
   /-webkit-line-clamp:\s*4/.test(clampRule), clampRule);
ok("...with both halves the prefixed form needs to work at all",
   /display:-webkit-box/.test(clampRule) && /-webkit-box-orient:\s*vertical/.test(clampRule), clampRule);
ok("...and the unprefixed spelling for engines that have moved on",
   /[^-]line-clamp:\s*4/.test(clampRule), clampRule);
// No separate "and it is scoped to cards" assertion here: the blanket check above already requires every
// selector in this block to carry the prefix, and a second one that tried to say it for this rule alone
// matched its own scoped selector and reported it as unscoped.

// -------------------------------------------------------------------------- the filter sheet, JFH-184
// The three facet rows used to sit in the sticky bar at every width, four rows of chip rails that ate 36%
// of a 375x812 viewport and could only be worked with two thumbs. Below the table breakpoint they are now
// a bottom sheet behind a "Filters" handle, and the handle carries a count of what is active so a reader
// who never opens it can still see that a filter is on.
//
// Two properties here are worth more than the rest and neither is visible in a screenshot:
//
// 1. Every sheet rule is gated on `html[data-fb]`, an attribute only `sheetWire()` sets. If `data.json`
//    never arrives -- the offline case, the file:// case, a 500 from Pages -- `buildChips` never runs, the
//    gate is never set, and the reader gets today's bar rather than a sheet with no chips in it that
//    nothing can open. The gate is the whole fallback, so it is asserted from both sides: the default-off
//    base rules, and that nothing which reveals or positions the sheet is missing the prefix.
// 2. `html[data-fb] .bar .chip{...}` deliberately sets no `display`. It outranks `.newchip{display:none}`,
//    so a `display:inline-flex` added to it for tidiness would reveal the New and Rising chips on every
//    build whose velocity window is empty -- which is the build this site ships most days. That is a
//    one-word regression with no visible cause, so it gets its own assertion.
const NARROW = "@media(max-width:640px),(max-height:560px)";
const sheetSel = /#sheet|#fbt|#fbn|#fbb|#fbx|#scount|\.shead/;
const sheetRules = cssRules(styles).filter(r => sheetSel.test(r.sel));
const ruleFor = (sel) => sheetRules.find(r => r.sel === sel);
const gated = sheetRules.filter(r => r.at === NARROW);

ok("the sheet was emitted at all", sheetRules.length > 15, String(sheetRules.length));
ok("nothing in it needed !important", sheetRules.every(r => !/!important/.test(r.body)));
// The default-off half of the gate. Each of these three is what a reader with no data.json sees.
ok("the handle is display:none until the gate is set",
   /^display:none/.test((ruleFor("#fbt") || {body: ""}).body), (ruleFor("#fbt") || {}).body);
ok("...as is the backdrop", (ruleFor("#fbb") || {}).body === "display:none");
ok("...as is the sheet's own header, the sheet being a plain flex column until then",
   (ruleFor(".shead") || {}).body === "display:none" &&
   /display:flex/.test((ruleFor("#sheet") || {body: ""}).body));
// The reveal half. Anything that positions the sheet over the page or shows its furniture has to carry
// both the gate and the narrow media query, or it would fire on a desktop or with no data loaded.
const reveal = sheetRules.filter(r => /position:fixed|display:(?!none)/.test(r.body) && r.at);
ok("every rule that reveals or positions the sheet is behind the gate", reveal.length >= 4 &&
   reveal.every(r => r.at === NARROW && r.sel.split(",").every(p => p.trim().startsWith("html[data-fb]"))),
   reveal.filter(r => r.at !== NARROW || r.sel.split(",").some(p => !p.trim().startsWith("html[data-fb]")))
     .map(r => r.at + " / " + r.sel).join(" | ") || String(reveal.length));
ok("...and the sheet itself is fixed to the bottom of the viewport, not the scrolling bar",
   /position:fixed/.test((ruleFor("html[data-fb] #sheet") || {body: ""}).body) &&
   /bottom:0/.test((ruleFor("html[data-fb] #sheet") || {body: ""}).body));
// `.bar` caps itself at 44dvh and scrolls inside, so a sheet positioned within it would be clipped to that
// cap. `position:fixed` takes the viewport as its containing block instead, which is what makes 80dvh
// reachable from inside an ancestor 44dvh tall.
ok("...at 80dvh with a vh fallback for engines without dvh",
   /max-height:80vh;max-height:80dvh/.test((ruleFor("html[data-fb] #sheet") || {body: ""}).body));
ok("...and it scrolls inside itself without chaining to the page behind it",
   /overflow-y:auto/.test((ruleFor("html[data-fb] #sheet") || {body: ""}).body) &&
   /overscroll-behavior:contain/.test((ruleFor("html[data-fb] #sheet") || {body: ""}).body));
// Opening restates `transition` without `visibility`. With it in the list the sheet computes `hidden` at
// progress exactly 0 -- the instant `show()` runs -- and a hidden element cannot take focus, so
// `sheet.focus()` was a silent no-op and the sheet opened with focus left on the handle. Shutting keeps
// `visibility` in the list, which is what holds the sheet visible through the 180ms slide-out.
const openRule = (ruleFor("html[data-fb][data-sheet=open] #sheet") || {body: ""}).body;
ok("the open state drops visibility from the transition, or the sheet cannot take focus",
   /transition:transform \.18s ease$/.test(openRule.trim()) && !/visibility/.test(
     openRule.split("transition:")[1] || ""), openRule);
ok("...while the shut state keeps it, so the slide-out is seen at all",
   /transition:transform \.18s ease,visibility \.18s/.test(
     (ruleFor("html[data-fb] #sheet") || {body: ""}).body));
// The JFH-200 landscape fix. Keyed on either axis, so an 844x390 phone on its side compacts on height
// even though it is wider than 640px. A media query narrowed back to `max-width` alone would put four
// rows of chip rails into 390px of height, which is the bug that shipped once.
ok("compaction is keyed on either axis, so landscape phones compact too",
   gated.length > 10 && styles.includes(NARROW), NARROW + " -> " + gated.length + " sheet rules");
ok("...and the bar's own cap is inside the same query", cssRules(styles).some(
   r => r.at === NARROW && r.sel === ".bar" && /max-height:44vh;max-height:44dvh/.test(r.body)));
// WCAG 2.5.5. Measured in cards-check at real widths; asserted here as text because a floor that is only
// ever measured on the three viewports someone thought of is a floor with holes in it.
for (const sel of ["html[data-fb] #fbt", "html[data-fb] #q", "html[data-fb] #fbx",
                   "html[data-fb] .bar .chip,html[data-fb] select", "header button", ".fix"])
  ok("44px tap target: " + sel, /min-height:44px/.test((ruleFor(sel) ||
     cssRules(styles).find(r => r.sel === sel && r.at === NARROW) || {body: ""}).body),
     (cssRules(styles).find(r => r.sel === sel && r.at === NARROW) || {}).body);
// The one-word regression described at the top of this block.
ok("the chip sizing rule sets no display, which would unhide the New and Rising chips",
   !/display/.test((cssRules(styles).find(
     r => r.sel === "html[data-fb] .bar .chip" && r.at === NARROW) || {body: ""}).body),
   (cssRules(styles).find(r => r.sel === "html[data-fb] .bar .chip") || {}).body);

// --- the markup: a disclosure, and one that actually contains the filters ---
const fbtTag = (html.match(/<button[^>]*id="fbt"[^>]*>/) || [""])[0].replace(/\s+/g, " ");
ok("the handle is a disclosure, not a toggle: aria-expanded and aria-controls",
   /aria-expanded="false"/.test(fbtTag) && /aria-controls="sheet"/.test(fbtTag), fbtTag);
// WCAG 2.5.3 Label in Name: the accessible name has to start with the visible word, or voice control
// cannot address it. `paintSheet` appends the count to it and never replaces it.
ok("...and its accessible name starts with the word on it", /aria-label="Filters/.test(fbtTag), fbtTag);
// Brace-matched in the HTML sense: walked to the `</div>` that actually closes the sheet, not to the next
// landmark. A slice that stopped at `<main>` would read a stray `</div>` -- one that closed the sheet early
// and left the Runs-on rail back in the always-visible bar -- as still being inside it, which is the one
// way this markup can go wrong without looking wrong. No `<div/>` exists in HTML, so open-minus-close is
// the whole of the arithmetic.
const divEnd = (start) => {
  const tag = /<(\/?)div\b[^>]*>/g;
  tag.lastIndex = start;
  let depth = 0, m;
  while ((m = tag.exec(html))) {
    depth += m[1] ? -1 : 1;
    if (depth === 0) return m.index;
  }
  return -1;
};
const sheetAt = html.indexOf('<div id="sheet"');
const sheetShut = divEnd(sheetAt);
ok("the sheet opens and closes", sheetAt > 0 && sheetShut > sheetAt &&
   sheetShut < html.indexOf("<main"), sheetAt + " -> " + sheetShut);
const sheetMarkup = html.slice(sheetAt, sheetShut);
// The stub DOM invents an element for any id asked of it, so every behavioural assertion above passes just
// as happily against a page that lost one of these -- writing the count into a phantom. The markup is the
// only place that is caught.
for (const id of ["fbt", "fbn", "sheet", "fbb", "fbx", "shtitle", "scount"])
  ok("the markup carries #" + id, new RegExp('id="' + id + '"').test(html));
ok("...and the badge is inside the handle, so the count travels with it",
   /id="fbt"[\s\S]*?>Filters<span id="fbn"><\/span><\/button>/.test(html));
ok("the sheet is a labelled group", /role="group"/.test(sheetMarkup) &&
   /aria-label="Filters"/.test(sheetMarkup) && /tabindex="-1"/.test(sheetMarkup));
ok("...and it wraps all three facet rails and both mode chips, not a subset",
   ["cats", "tgts", "oses", "strict", "reset", "scount", "shtitle", "fbx"]
     .every(id => sheetMarkup.includes('id="' + id + '"')),
   ["cats", "tgts", "oses", "strict", "reset", "scount", "shtitle", "fbx"]
     .filter(id => !sheetMarkup.includes('id="' + id + '"')).join(", "));
// Search, sort and the two velocity chips stay in the always-visible row on purpose: the box shows its own
// text and the chips wear the accent when pressed, so every active filter is visible while the sheet is
// shut without the badge over-reporting what opening it would show.
ok("the search box stays out of the sheet, its text being its own indicator",
   !sheetMarkup.includes('id="q"') && !sheetMarkup.includes('id="new"') &&
   !sheetMarkup.includes('id="rise"'));

// --- the count, at 0, 1 and several ---
const G = (id) => document.getElementById(id);
ok("the CSS gate is set by JS, and by nothing else", document.documentElement.dataset.fb === "1");
// The shut state's `aria-expanded="false"` comes from the markup, asserted above -- `show()` is the only
// thing that ever writes the attribute, so there is nothing to read here at boot. This half is the
// `data-sheet` the CSS keys the slide on.
ok("...and the sheet boots shut", document.documentElement.dataset.sheet === "shut",
   String(document.documentElement.dataset.sheet));

const CLR = {q: "", cat: "", tgt: "", os: [], strict: false, fresh: false, rising: false};
const paint = (over) => { Object.assign(A.state, CLR, over); A.render(); };
paint({});
ok("no filters: the badge is empty and the handle is unfilled",
   G("fbn").textContent === "" && !G("fbt").classList.contains("act"),
   JSON.stringify(G("fbn").textContent));
ok("...and the handle says so out loud",
   G("fbt").getAttribute("aria-label") === "Filters — none selected",
   G("fbt").getAttribute("aria-label"));
ok("...and the sheet's title is unadorned", G("shtitle").textContent === "Filters");

const cat0 = A.D.cats[0], tgt0 = A.D.targets[0];
paint({cat: cat0.slug});
ok("one filter: the badge reads 1 and the handle fills",
   G("fbn").textContent === "1" && G("fbt").classList.contains("act"), G("fbn").textContent);
ok("...and the label names the filter rather than its slug",
   G("fbt").getAttribute("aria-label") === "Filters — 1 selected: " + cat0.name,
   G("fbt").getAttribute("aria-label"));

ok("there are at least two operating systems to select", A.D.os.length >= 2, String(A.D.os.length));
paint({cat: cat0.slug, tgt: tgt0.slug, os: [0, 1], strict: true});
const want = [cat0.name, tgt0.name, A.D.os[0], A.D.os[1], "Confirmed only"];
ok("five filters: the badge reads 5", G("fbn").textContent === "5", G("fbn").textContent);
ok("...and each is named, in the order the rails are read",
   JSON.stringify(A.sheetFilters()) === JSON.stringify(want), JSON.stringify(A.sheetFilters()));
ok("...and the label lists all five",
   G("fbt").getAttribute("aria-label") === "Filters — 5 selected: " + want.join(", "),
   G("fbt").getAttribute("aria-label"));
ok("...and the shut sheet's title carries the count",
   G("shtitle").textContent === "Filters · 5", G("shtitle").textContent);
// The result count is repeated inside the sheet, because a reader changing filters with the sheet open
// cannot see the bar's copy behind it -- and it is painted before render()'s empty-state early return, or
// it would go stale exactly when it matters most.
ok("the sheet repeats the result count", G("scount").innerHTML === A.COUNT && A.COUNT.length > 0,
   JSON.stringify(G("scount").innerHTML));
paint({q: "zzzzqqqqxxxx-no-such-thing", cat: cat0.slug, tgt: tgt0.slug, os: [0, 1], strict: true});
ok("...even on a render that finds nothing and returns early",
   G("scount").innerHTML === A.COUNT && A.COUNT.length > 0, JSON.stringify(G("scount").innerHTML));
ok("...and the badge is repainted on that path too", G("fbn").textContent === "5", G("fbn").textContent);
// Only what is behind the handle counts. `fresh` and `rising` are chips in the visible row, and counting
// them would send a reader into a sheet that shows nothing selected.
paint({fresh: true, rising: true});
ok("the badge counts what the sheet holds and not the chips beside it",
   G("fbn").textContent === "" && A.sheetFilters().length === 0, JSON.stringify(A.sheetFilters()));

// --- opening and closing ---
const shutNow = () => document.documentElement.dataset.sheet === "shut" &&
  G("fbt").getAttribute("aria-expanded") === "false";
const openNow = () => document.documentElement.dataset.sheet === "open" &&
  G("fbt").getAttribute("aria-expanded") === "true";
G("fbt").click();
ok("the handle opens the sheet, and says it is open", openNow(),
   document.documentElement.dataset.sheet + " / " + G("fbt").getAttribute("aria-expanded"));
G("fbt").click();
ok("...and the same handle closes it", shutNow());
G("fbt").click(); G("fbx").click();
ok("Done closes it", shutNow());
G("fbt").click(); G("fbb").click();
ok("a tap on the backdrop closes it", shutNow());
paint({});

// ------------------------------------------------------------------------ saved projects, JFH-187
// The reader's own set, which is the first thing on this page that is neither in the data nor in the URL.
// That makes the interesting assertions the ones about the seams: what a link means on a machine that has no
// saved set, what happens to the filter when the set it filters by is emptied, and whether a control called
// "Clear all filters" can lose somebody's collection.
//
// Driven through `toggleSave` and the chip handlers rather than by assigning to `SAVED`, because the bugs
// worth catching here are in the repaint and the persistence, not in the Set.
const btn = (nwo, name) => {
  const attrs = {};
  return {
    dataset: {nwo, name}, textContent: "",
    setAttribute(k, v) { attrs[k] = String(v); }, getAttribute(k) { return attrs[k] ?? null; },
  };
};
const first = A.ROWS[0], second = A.ROWS[1];
const G2 = id => document.getElementById(id);

// --- the markup one row carries ---
A.state.saved = false;
STORE.clear(); A.loadSaved(); A.render();
ok("an unsaved row offers Save", /class="save"[^>]*>Save</.test(A.saveBtn(first)), A.saveBtn(first));
ok("the button carries the nwo, not a row index",
   A.saveBtn(first).includes('data-nwo="' + first.nwo + '"'), A.saveBtn(first));
// WCAG 2.5.3: someone driving the page by voice says the word they can see, so the accessible name has to
// contain it. Checked in both states because the two words differ and only one of them is the default.
for (const on of [false, true])
  ok("the accessible name contains the visible word when " + (on ? "saved" : "unsaved"),
     A.saveLabel(first.name, on).startsWith(on ? "Saved" : "Save"), A.saveLabel(first.name, on));

// --- a save round-trips through storage, which is what "survives a reload" means ---
const b1 = btn(first.nwo, first.name);
A.toggleSave(b1);
ok("pressing Save adds the project", A.SAVED.has(first.nwo));
ok("the button repaints in place, without a re-render", b1.textContent === "Saved" &&
   b1.getAttribute("aria-pressed") === "true", b1.textContent + " / " + b1.getAttribute("aria-pressed"));
ok("the set reaches localStorage", JSON.parse(STORE.get("saved") || "[]").includes(first.nwo),
   STORE.get("saved"));
// A new session, modelled the only way it can be here: the store is untouched and the set is re-read from it.
A.SAVED.clear();
A.loadSaved();
ok("a later session reads the set back", A.SAVED.has(first.nwo), [...A.SAVED].join(","));

// --- the chip appears only once there is something to filter to ---
A.render();
ok("the Saved chip is shown with one saved", G2("saved").classList.contains("on"));
ok("the chip carries the count", /Saved . 1$/.test(G2("savedlabel").textContent),
   G2("savedlabel").textContent);
ok("Remove all is hidden while the filter is off", !G2("clearsave").classList.contains("on"));

// --- the filter narrows to exactly the saved set, and composes with the rest ---
A.state.q = ""; A.state.cat = ""; A.state.tgt = ""; A.state.os = []; A.state.strict = false;
A.state.fresh = false; A.state.rising = false; A.state.shown = 600;
A.state.saved = true; A.render();
ok("the saved filter shows exactly the saved rows", order().length === 1 && order()[0] === first.nwo,
   order().join(","));
ok("Remove all appears once the reader is looking at the set", G2("clearsave").classList.contains("on"));
A.toggleSave(btn(second.nwo, second.name));
A.state.shown = 600; A.render();
ok("a second save joins the filtered view", order().length === 2 && order().includes(second.nwo),
   order().join(","));

// --- saving must not throw the reader back to the top of a long list ---
A.state.saved = false; A.state.q = "agent"; A.state.shown = 600; A.render();
const deep = A.ROWS.find(r => r.nwo !== first.nwo && r.nwo !== second.nwo);
A.toggleSave(btn(deep.nwo, deep.name));
ok("saving does not reset the page size", A.state.shown === 600, String(A.state.shown));
A.toggleSave(btn(deep.nwo, deep.name));
ok("pressing it again un-saves", !A.SAVED.has(deep.nwo));

// --- a link that travels: #saved=1 on a machine with nothing saved ---
A.state.q = "";
STORE.clear(); A.SAVED.clear();
globalThis.location.hash = "#saved=1";
A.readHash();
ok("#saved=1 is ignored where the reader has saved nothing", A.state.saved === false);
A.render();
ok("and the chip stays away", !G2("saved").classList.contains("on"));
A.toggleSave(btn(first.nwo, first.name));
A.readHash();
ok("#saved=1 is honoured once there is a set to honour it against", A.state.saved === true);
A.writeHash();
globalThis.location.hash = "";

// --- emptying the set must not strand the reader behind a filter with no control ---
A.state.saved = true; A.render();
A.toggleSave(btn(first.nwo, first.name));
ok("un-saving the last row turns the filter off", A.state.saved === false);
ok("and takes the chip with it", !G2("saved").classList.contains("on"));
A.render();
ok("the table is the whole atlas again, not an empty set", order().length > 1, String(order().length));

// --- the one destructive control is the only destructive control ---
A.toggleSave(btn(first.nwo, first.name));
A.toggleSave(btn(second.nwo, second.name));
A.state.saved = true; A.render();
A.state.q = "kubernetes";
A.render();
A.state.q = "";
ok("Clear all filters drops the saved filter", (() => {
  A.state.saved = true; G2("reset").click(); return A.state.saved === false;
})());
ok("Clear all filters does NOT empty the set", A.SAVED.size === 2, String(A.SAVED.size));
ok("nor does it clear the store", JSON.parse(STORE.get("saved") || "[]").length === 2, STORE.get("saved"));
A.state.saved = true; A.render();
G2("clearsave").click();
ok("Remove all empties the set", A.SAVED.size === 0, String(A.SAVED.size));
ok("Remove all empties the store too", JSON.parse(STORE.get("saved") || "[]").length === 0,
   STORE.get("saved"));
ok("Remove all leaves the filter off", A.state.saved === false);

// --- rescue offers the filter and never the set ---
A.toggleSave(btn(first.nwo, first.name));
A.state.saved = true; A.state.cat = A.D.cats[0].slug;
A.state.shown = 600; A.render();
const rs = A.rescue();
if (order().length === 0) {
  ok("an empty saved-and-topic view offers a way out",
     rs.some(o => /saved/.test(o.label)), rs.map(o => o.label).join(" | "));
  ok("that way out patches the filter and not the set",
     rs.every(o => !("SAVED" in o.patch)) && A.SAVED.size === 1);
} else {
  // The real dataset may well have a saved row inside the first topic, in which case there is nothing to
  // rescue from. Counted rather than skipped, because a harness that quietly tallies nothing is a harness
  // that passes when the feature is gone.
  ok("the saved row survives being crossed with a topic", order().length >= 1, String(order().length));
  ok("and the set is untouched by rendering", A.SAVED.size === 1, String(A.SAVED.size));
}

// --- storage this page did not write: it survives every deploy and is editable by hand ---
for (const junk of ['{"a":1}', "[1,2,3]", "not json at all", "null", '["ok/one", 7, "", "ok/two"]']) {
  STORE.set("saved", junk);
  let threw = false;
  try { A.loadSaved(); } catch (e) { threw = true; }
  ok("a corrupt saved key does not throw: " + junk.slice(0, 18), !threw);
  ok("and yields only strings: " + junk.slice(0, 18),
     [...A.SAVED].every(s => typeof s === "string" && s), [...A.SAVED].join(","));
}
STORE.set("saved", '["ok/one", 7, "", "ok/two"]');
A.loadSaved();
ok("the salvageable entries of a part-corrupt key are kept", A.SAVED.size === 2, [...A.SAVED].join(","));

STORE.clear(); A.loadSaved();
A.state.saved = false; A.state.cat = ""; A.state.q = ""; A.state.shown = 600; A.render();

// ------------------------------------------------------- the page as shipped: no comments, no placeholders
// The JFH-204 acceptance checks. `scripts/19_pages.py` keeps every comment it has ever had and
// `scripts/pagemin.py` takes them out on the way to `docs/`, which is 55 KB of prose off every load. The
// stripper is 250 lines of state machine over three grammars, and the way it fails is not "a comment
// survived" -- that costs bytes and nothing else. It is that it ate something that only looked like a
// comment. So the weight here is on the second kind of assertion: the nine `//` in the shipped page that
// are URLs and must still be there.
//
// Asserted on the file rather than through the browser deliberately. A browser can only tell you the page
// still works, and a page with a comment left in it works perfectly; the property is textual, so the test
// is textual. It is here rather than in a fifth harness because this file is already the one that reads
// `docs/index.html` as text.
//
// Both scans run against `AAA_PAGE` when it is set, so they can be pointed at an unsubstituted template
// while the stripper is being written -- the placeholder scan will of course fail on one of those, which
// is the point of it.
const shown = (s) => JSON.stringify(s.length > 70 ? s.slice(0, 70) + "…" : s);
const around = (i, w = 55) => shown(html.slice(Math.max(0, i - w), i + w).replace(/\s+/g, " "));

// Two HTML comments do survive, and they are not the page's. `__ANALYTICS__` is substituted *after* the
// strip pass, and what it substitutes is the Cloudflare Web Analytics snippet pasted verbatim out of
// Cloudflare's dashboard, wrapped in the two marker comments Cloudflare ships it with. So the assertion is
// that those two are the only ones -- pinned to their exact text and to an exact count, because a whitelist
// that matched loosely would wave through the next comment to escape the stripper.
//
// Worth 70 bytes on every load and worth writing down: this is a real, if small, miss in what the stripper
// set out to do, and the fix is not in the stripper. Either `beacon()` in `19_pages.py` drops the two
// markers -- they are decoration, the snippet works without them -- or the substitution happens before the
// strip rather than after it. Recorded here rather than silently allowed, and it is one line either way.
const BEACON = ["<!-- Cloudflare Web Analytics -->", "<!-- End Cloudflare Web Analytics -->"];
const htmlComments = (html.match(/<!--/g) || []).length;
ok("the only HTML comments left are the two the third-party beacon brings with it",
   htmlComments === 2 && BEACON.every(c => html.includes(c)),
   htmlComments + " left, first at " + around(html.indexOf("<!--")));
// `/*` covers CSS and JS block comments in one, there being no other legal use of the pair in either
// grammar outside a string, and no string in this page contains it.
const blockComments = (html.match(/\/\*/g) || []).length;
ok("no CSS or JS block comment survives either", blockComments === 0,
   blockComments + " left, first at " + around(html.indexOf("/*")));

// The one that is worth having. Every `//` left in the page must be part of a URL scheme, because that is
// the only reason a `//` survives a comment stripper -- and a stripper that got it wrong would have eaten
// the rest of the line, taking a `<link>`, a `<meta>` or a statement with it.
const slashes = [...html.matchAll(/\/\//g)].map(m => m.index);
const scheme = /(?:https?|file|ws|wss|data|mailto):$/;
const stray = slashes.filter(i => !scheme.test(html.slice(Math.max(0, i - 8), i)));
ok("every // left in the page is a URL scheme and not a line comment", stray.length === 0,
   stray.length + " of " + slashes.length + ", first at " + around(stray[0] ?? 0));
// Nine on the unsubstituted template -- seven in HTML attributes, two inside JS string literals -- and
// twelve once `__SITE__`'s three occurrences are substituted with an absolute URL. A floor rather than an
// equality, because the count is a property of how many links the footer has and this assertion is about
// the stripper, not about the footer. Zero would mean the scan above passed by having nothing to look at.
ok("...and there are still nine or more of them, so the scan above is not vacuous",
   slashes.length >= 9, String(slashes.length));

// Named individually, because these are the exact shapes the stripper has to get right: a `//` inside a
// double-quoted HTML attribute, inside a single-quoted one, and inside a JS string literal.
// This used to name `opengraph.githubassets.com`, which is no longer what `og:image` carries: the root page
// points at the card `23_og.py` renders, and the GitHub URL is now only the build-time fallback taken when
// that PNG is absent from disk. So the assertion follows the tag rather than the host -- what it is here to
// prove is that a `//` inside a double-quoted HTML attribute survives the stripper, and either URL proves it.
ok("the og:image URL survives in a double-quoted HTML attribute",
   /<meta property="og:image" content="https:\/\/[^"]+\/[^"]+">/.test(html),
   (html.match(/<meta property="og:image"[^>]*>/) || ["absent"])[0]);
// The two shapes it can be, asserted as an either-or rather than pinned to one, because which branch
// `image_tags()` took is a fact about whether docs/og/root.png is on disk in this checkout -- not a fact
// about the page, and not something this harness should force.
ok("...and it is either the rendered card or the documented GitHub fallback",
   /content="https:\/\/[^"]*\/og\/root\.png"/.test(html) ||
   /content="https:\/\/opengraph\.githubassets\.com\//.test(html));
ok("...and in the JS string that builds the same URL per row",
   /"https:\/\/opengraph\.githubassets\.com\/1\/"/.test(html));
ok("the favicon's SVG namespace survives inside a single-quoted data URI",
   html.includes("http://www.w3.org/2000/svg"));
ok("the file:// message survives inside a JS string with markup in it",
   /<code>file:\/\/<\/code>/.test(html));
ok("the footer's four repository links survive",
   (html.match(/https:\/\/github\.com\//g) || []).length >= 4,
   String((html.match(/https:\/\/github\.com\//g) || []).length));

// And that the substitution pass ran at all. A stripper that reformatted a placeholder -- or a template
// that grew a new one nobody wired up -- ships the literal token to a reader, and `__COUNT__` in the
// header is the sort of thing that survives review because it looks like a build artefact.
const holes = [...new Set(html.match(/__[A-Z][A-Z0-9_]*__/g) || [])];
ok("every __PLACEHOLDER__ was resolved", holes.length === 0, holes.join(", "));

console.log("\n" + pass + " passed, " + fail + " failed");
process.exit(fail ? 1 : 0);
