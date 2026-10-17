// The pals' bits (`docs/assets/archie-bits.js`, built from art/pals/bits/*.js), every one of them played for
// real on the live model, on the stage in `archie-stage.js`, in capture mode: the stage's clock is frozen and
// stepped from here a fifth of a second at a time, so every assertion below is about stage time rather than
// about how busy the machine was. For each bit in BITS:
//
//   - a place it can play: each page family in its `pages` opened in turn, at the top and then with each
//     of the elements bits stand on scrolled to 250 px from the top, until `archie.can("bit:<name>")` is ""
//     -- with a mouse pointer brought onto the page for a bit whose `ready()` reads one, and the README's
//     request held open for one that wants the reader still loading. A bit that cannot be placed anywhere is
//     reported as skipped, with why, and is not a failure;
//   - that it ends on its own inside 120 stage seconds, and how long it took;
//   - that the page is put back exactly: every element's tag, id, class and style attribute, the text of
//     <main>, every attribute of <html>, the window's scroll and every scrollable element's;
//   - that nothing was saved -- localStorage and sessionStorage as they were, no cookie -- and nothing
//     focused, sampled on every step;
//   - that the theme flips no more than three flashes (a change and its change back) in any second of
//     stage time, which is WCAG 2.3.1's line and the one `s.page.flicker` keeps -- measured a frame at a
//     time, since the clock is stepped by 1/60 s rather than 0.2 s for two seconds after any change;
//   - that the stage's layer is inert while it is up -- aria-hidden, no pointer events on it or anything in
//     it, nothing focusable -- and that nothing is added to the document outside it;
//   - and that nothing threw: no console error, no uncaught exception, and none of the warnings the stage
//     logs when it swallows a bit's own exception or misses a clip ("pals: ...").
//
// Then stopping: the three longest bits each started, stepped four seconds, and sent a real Escape, and one
// more sent a pointerdown on an empty part of the page; each must be gone within one stage second and leave
// the page as it found it.
//
// WHAT THIS HARNESS CANNOT SEE: whether a bit is funny, or reads at all -- that is the frames
// tools/capture-bit.mjs records, and a person watching them. Nor the director choosing a bit unasked (once in
// three minutes at most, and never with an `?archie=` flag, which every page here carries so that he plays
// nothing else meanwhile), nor a bit's `cue` firing on its own: the bits are run through `archie.run`, and a
// cue's row is scrolled by this harness mid-bit, so that row's scrollLeft is the harness's and is held only to
// what the bit itself would do to it, which is nothing. Nor the 404 page: the test server answers a missing URL
// with a line of its own rather than docs/404.html, and docs/404.html has no Archie on it to play anything, so
// a bit is placed on the other families it names. Nor anything about a bit's look: only the DOM is read.
//
// Every page is opened fresh for every bit, because a page view plays a bit at most once and a fresh page
// keeps one bit's leftovers out of the next one's assertions. The window is 1400x900, light colour scheme.
// The model has to go live, so WebGL is swiftshader's, as in prank-check.mjs. A page that stops answering
// -- a bit looping on `await s.after()` without asking `s.alive` spins for ever once it is stopped -- fails
// that bit and is replaced by a fresh tab, rather than hanging the run.
//
// About thirty minutes for forty-two bits, and it is not the stepping that could be cut: each fresh page waits
// for the stage, which loads six seconds after the model in idle time, and each step is a frame swiftshader
// draws at 1400x900. More tabs at once (`AAA_BITS_TABS`, each in a browser context of its own so that one
// tab's storage is not another's "nothing saved") was slower on the machine this was written on, because
// the tabs' frames share the CPU; it defaults to one. `AAA_BITS=name,name` plays only those bits, for
// working on one, and `AAA_BITS_DEBUG=1` says where the time went. run.mjs sets none of them, and its floor
// is what notices a run that played too few.
//
//   node tests/bits-check.mjs <chrome-binary> <origin>
import {tmpdir} from "node:os";
import {launch} from "./lib/browser.mjs";

const BIN = process.argv[2], ORIGIN = (process.argv[3] || "").replace(/\/?$/, "/");
if (!BIN || !process.argv[3]) {
  console.error("usage: node tests/bits-check.mjs <chrome-binary> <origin>");
  process.exit(2);
}
const TMP = process.env.AAA_TMP || tmpdir();
const ONLY = (process.env.AAA_BITS || "").split(",").map(s => s.trim()).filter(Boolean);
const TABS = Math.max(1, Number(process.env.AAA_BITS_TABS) || 1);
const STARTED = Date.now();

// Where each page family of `where()` (archie-stage.js) is opened. `lost` is the 404 page: Pages serves
// docs/404.html for any missing URL, tests/lib/serve.mjs answers with a one-line 404 of its own instead, so
// it is asked for by name -- and tried last, since nothing plays there (see the header).
const URLS = {home: "", topic: "topic/coding-agents/", repo: "repo/ollama/ollama/", repos: "repo/",
              catalog: "catalog/", discover: "discover/", collections: "collections/", target: "target/mcp/",
              lost: "404.html"};
// Where on a page a bit is looked for: the top, then each of the elements bits stand on, 250 px down.
const SPOTS = [null, ".source-preview .reader", "article.hero", ".rowscroll", "article.cx"];
// A flag on every page: the director plays nothing on his own while one is set (no bit, no cue), and this
// one names no friend, so the friends' dice are never rolled and nobody comes over mid-bit.
const FLAG = "?archie=friend:nobody";
const STEP = 0.2, CAP = 120, STOP_AFTER = 4, STOP_WITHIN = 1;

process.env.AAA_CHROME_FLAGS = [process.env.AAA_CHROME_FLAGS || "", "--enable-unsafe-swiftshader",
  "--use-angle=swiftshader"].join(" ");
const browser = await launch(BIN, TMP, "bits");

const sleep = ms => new Promise(r => setTimeout(r, ms));
let id = 0;
const waiters = new Map(), tabs = new Map();
const ws = new WebSocket(browser.wsUrl);
await new Promise(r => ws.addEventListener("open", r, {once: true}));
const send = (method, params = {}, sid) => new Promise((res, rej) => {
  const n = ++id; waiters.set(n, {res, rej});
  ws.send(JSON.stringify({id: n, method, params, ...(sid ? {sessionId: sid} : {})}));
});
// The network noise prank-check.mjs excuses, for its reasons: the Cloudflare beacon cannot pass CORS
// against localhost, and GitHub turns down the page's anonymous API calls with a 403 or a 429 once an
// address has spent its sixty an hour.
const excused = e => /cloudflareinsights|beacon|opengraph\.githubassets\.com/.test(e.text + " " + (e.url || "")) ||
  (/^https:\/\/api\.github\.com\//.test(e.url || "") && /status of (403|429)\b/.test(e.text));
const words = args => (args || []).map(a => a.value !== undefined ? String(a.value) : a.description || "").join(" ");
ws.addEventListener("message", ev => {
  const m = JSON.parse(ev.data);
  if (m.id && waiters.has(m.id)) {
    const w = waiters.get(m.id); waiters.delete(m.id);
    m.error ? w.rej(new Error(m.error.message)) : w.res(m.result);
    return;
  }
  const tab = tabs.get(m.sessionId);
  if (!tab) return;
  if (m.method === "Runtime.exceptionThrown")
    tab.errors.push("uncaught: " + (m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text));
  else if (m.method === "Log.entryAdded" && m.params.entry.level === "error" && !excused(m.params.entry))
    tab.errors.push(m.params.entry.text + (m.params.entry.url ? ` (${m.params.entry.url})` : ""));
  else if (m.method === "Runtime.consoleAPICalled") {
    // console.error is an error. So is a "pals: ..." warning: it is how the stage reports a bit's exception
    // it caught (`<bit> stopped:`), a ticker or a wait that threw, a clip the bit asked for that its pal does
    // not have, and a pack that would not load -- each one a bit that played less than it was written to.
    const said = words(m.params.args);
    if (m.params.type === "error") tab.errors.push("console.error: " + said);
    else if (m.params.type === "warning" && /^pals:/.test(said)) tab.errors.push("console.warn: " + said);
  } else if (m.method === "Fetch.requestPaused") void github(tab, m.params);
});

// ---- the README reader's GitHub calls, answered here --------------------------------------------------
// The repo page's reader fetches the README from api.github.com. Answered from here, so that a placement on
// that page is the same on every machine and offline, and so that it can be held open for a bit that plays
// while the reader is still loading (`tab.hold`). Anything else under the repository goes to the network.
const README = `<div class="markdown-heading"><h1>Ollama</h1></div>
<p>Get up and running with large language models.</p>
${Array.from({length: 14}, (_, i) => `<h2>Section ${i + 1}</h2>
<p>Run, customise and share models locally. This paragraph is here to give the reader its height, the way a real
README does, so that a bit that stands on the reader finds as much wall as it would on the published page.</p>
<ul><li>One</li><li>Two</li><li>Three</li></ul>`).join("\n")}`;
const RAW = "# Ollama\n\nGet up and running with large language models.\n";
async function github(tab, p) {
  const url = new URL(p.request.url), h = p.request.headers || {}, accept = h.Accept || h.accept || "";
  let code = 200, type = "text/html; charset=utf-8", body = "";
  if (p.request.method === "OPTIONS") code = 204;
  else if (/\/(readme|contents\/)/.test(url.pathname)) {
    if (tab.hold) return;                                 // left pending: the reader stays "loading"
    body = accept.includes("raw") ? RAW : README;
    if (accept.includes("raw")) type = "text/plain; charset=utf-8";
  } else if (url.pathname.endsWith("/git/trees/HEAD")) {
    type = "application/json; charset=utf-8";
    body = JSON.stringify({truncated: false, tree: [{path: "README.md", type: "blob", size: RAW.length}]});
  } else return tab.S("Fetch.continueRequest", {requestId: p.requestId}).catch(() => {});
  await tab.S("Fetch.fulfillRequest", {requestId: p.requestId, responseCode: code, body: Buffer.from(body).toString("base64"),
    responseHeaders: [{name: "content-type", value: type}, {name: "access-control-allow-origin", value: "*"},
                      {name: "access-control-allow-headers", value: "accept"}]}).catch(() => {});
}

// ---- the recorder, in every document before the page's own scripts ------------------------------------
// Archie's own furniture runs on his own clock, so it is left out of the page's picture: his slot and dock,
// his bubble (it follows his head), the live region he speaks through, the poke target and its hearts, and
// anything else his director's scripts make -- the layer a visit or a friend draws in, say, which comes and
// goes on his clock and not the bit's. That last is told by who called createElement: archie.js or one of
// its fellows, with neither archie-stage.js nor archie-bits.js on the stack. Everything a bit or the
// stage makes, and everything of the page's own, is in the picture.
const RECORDER = `(() => {
  const OWN = ".mhmascot, .archie-dock, .archie-say, .archie-sr, .archie-poke, .archie-heart";
  const STAGE = ".pals-stage";
  const bc = window.__bc = {armed: false, flips: [], added: [], writes: [], said: [], focusOff: [], inert: [],
                            row: null, rowLeft: null, snaps: {}};
  const name = e => !e || e.nodeType !== 1 ? String(e && e.nodeName) : e.tagName.toLowerCase() +
    (e.id ? "#" + e.id : "") + (e.classList.length ? "." + [...e.classList].slice(0, 3).join(".") : "");
  const DIRECTOR = /[/]assets[/](archie|archie-core|archie-friends|archie-dance|archie-admin)[.]js/;
  const BIT = /[/]assets[/]archie-(stage|bits)[.]js/;
  const own = new WeakSet();
  for (const k of ["createElement", "createElementNS"]) {
    const f = Document.prototype[k];
    Document.prototype[k] = function (...a) {
      const e = f.apply(this, a), st = new Error().stack || "";
      if (DIRECTOR.test(st) && !BIT.test(st)) own.add(e);
      return e;
    };
  }
  const his = e => { for (; e && e.nodeType === 1; e = e.parentElement) if (own.has(e) || e.matches(OWN)) return true; return false; };
  const within = (e, q) => !!(e && e.nodeType === 1 && (q === OWN ? his(e) : e.closest(q)));
  const clock = () => { try { return window.archieStage ? window.archieStage.status().clock : null; } catch { return null; } };
  bc.name = name;
  // Every storage write while armed, and whether the stage or a bit made it.
  for (const op of ["setItem", "removeItem", "clear"]) {
    const f = Storage.prototype[op];
    Storage.prototype[op] = function (...a) {
      if (bc.armed) bc.writes.push({area: this === localStorage ? "local" : "session", op, key: a[0],
                                    bit: /archie-(stage|bits)\\.js/.test(new Error().stack || "")});
      return f.apply(this, a);
    };
  }
  let theme = null;
  new MutationObserver(ms => { for (const m of ms) {
    if (m.type === "attributes") {
      if (m.target !== document.documentElement) continue;
      const v = m.target.getAttribute("data-theme");
      if (bc.armed && v !== theme) bc.flips.push({t: clock(), v});
      theme = v;
      continue;
    }
    if (!bc.armed) continue;
    if (within(m.target, ".archie-sr") && m.target.textContent) bc.said.push(m.target.textContent);
    for (const n of m.addedNodes) {
      if (n.nodeType !== 1 || within(n, STAGE) || within(m.target, STAGE) || within(n, OWN) || within(m.target, OWN)) continue;
      bc.added.push(name(n) + " into " + name(m.target));
    }
  } }).observe(document, {subtree: true, childList: true, attributes: true, attributeFilter: ["data-theme"]});

  // The page, as far as a bit could change it, kept here under a key and compared here, so only the
  // differences cross the wire.
  bc.snap = key => {
    const L = document.querySelector(STAGE), els = [], scrolls = new Map();
    for (const e of document.getElementsByTagName("*")) {
      if (L && (e === L || L.contains(e)) || his(e)) continue;
      els.push(name(e).split(".")[0] + " class=" + JSON.stringify(e.getAttribute("class")) +
               " style=" + JSON.stringify(e.getAttribute("style")));
      if (e !== document.documentElement && e !== document.body &&
          (e.scrollWidth > e.clientWidth || e.scrollHeight > e.clientHeight) && e !== bc.row)
        scrolls.set(els.length - 1 + " " + name(e), e.scrollLeft + "," + e.scrollTop);
    }
    const root = document.querySelector("main") || document.body, words = [];
    const tw = document.createTreeWalker(root, NodeFilter.SHOW_TEXT,
      {acceptNode: t => his(t.parentElement) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT});
    for (let t; (t = tw.nextNode());) words.push(t.data);
    bc.snaps[key] = {els, scrolls, text: words.join(""),
      html: [...document.documentElement.attributes].map(a => a.name + "=" + JSON.stringify(a.value)).sort().join(" "),
      win: scrollX + "," + scrollY, active: document.activeElement,
      local: JSON.stringify(Object.entries(localStorage).sort()),
      session: Object.fromEntries(Object.entries(sessionStorage).sort()), cookie: document.cookie};
    return els.length;
  };
  bc.diff = (a, b) => {
    const A = bc.snaps[a], B = bc.snaps[b], out = {};
    if (A.els.join("\\n") !== B.els.join("\\n")) {
      const gone = new Map(), more = new Map();
      for (const s of A.els) gone.set(s, (gone.get(s) || 0) + 1);
      for (const s of B.els) if (gone.get(s)) gone.set(s, gone.get(s) - 1); else more.set(s, (more.get(s) || 0) + 1);
      const list = m => [...m].filter(([, n]) => n > 0).map(([s, n]) => (n > 1 ? n + "x " : "") + s);
      out.dom = {before: A.els.length, after: B.els.length, lost: list(gone).slice(0, 4), gained: list(more).slice(0, 4)};
      if (!out.dom.lost.length && !out.dom.gained.length) out.dom.order = "the same elements, in another order";
    }
    if (A.text !== B.text) {
      let i = 0;
      while (i < A.text.length && A.text[i] === B.text[i]) i++;
      out.text = JSON.stringify(A.text.slice(Math.max(0, i - 30), i + 50)) + " became " +
                 JSON.stringify(B.text.slice(Math.max(0, i - 30), i + 50));
    }
    if (A.html !== B.html) out.html = A.html + " became " + B.html;
    const sc = [];
    if (A.win !== B.win) sc.push("window " + A.win + " -> " + B.win);
    for (const [k, v] of A.scrolls) if (B.scrolls.has(k) && B.scrolls.get(k) !== v) sc.push(k + " " + v + " -> " + B.scrolls.get(k));
    if (sc.length) out.scroll = sc.slice(0, 4).join("; ");
    if (bc.row && bc.rowLeft !== null && bc.row.scrollLeft !== bc.rowLeft)
      out.row = "the row the harness scrolled was left at " + bc.rowLeft + " and is at " + bc.row.scrollLeft;
    if (A.local !== B.local) out.local = A.local + " became " + B.local;
    // His mood is sessionStorage's archie-mood, which the director rewrites every two seconds while the
    // masthead is on screen and drifts on his clock, not a bit's. Only when the tab met him is held to it;
    // a write to it by a bit is caught by \`writes\` like any other.
    const since = v => { try { return JSON.parse(v).since; } catch { return v; } };
    const ses = s => JSON.stringify(Object.entries(s).map(([k, v]) => k === "archie-mood" ? [k, since(v)] : [k, v]));
    if (ses(A.session) !== ses(B.session)) out.session = ses(A.session) + " became " + ses(B.session);
    if (A.cookie !== B.cookie) out.cookie = JSON.stringify(A.cookie) + " became " + JSON.stringify(B.cookie);
    if (A.active !== B.active) out.focus = name(A.active) + " became " + name(B.active);
    return out;
  };
  bc.arm = () => {
    Object.assign(bc, {armed: true, flips: [], added: [], writes: [], said: [], focusOff: [], inert: [],
                       focus0: document.activeElement});
    theme = document.documentElement.getAttribute("data-theme");
  };
  bc.disarm = () => { bc.armed = false; };
  // The overlay, as it stands: what about it is not inert.
  const FOCUSABLE = "a[href],button,input,select,textarea,summary,iframe,[tabindex]:not([tabindex='-1']),[contenteditable]";
  bc.inertNow = () => {
    const L = document.querySelector(STAGE), bad = [];
    if (!L) return bad;
    if (L.getAttribute("aria-hidden") !== "true") bad.push("the layer is not aria-hidden");
    const svg = L.querySelector("svg");
    if (svg && !svg.closest('[aria-hidden="true"]')) bad.push("its svg is not aria-hidden");
    for (const e of [L, ...L.querySelectorAll("*")]) {
      if (getComputedStyle(e).pointerEvents !== "none") bad.push(name(e) + " takes pointer events");
      if (e.matches(FOCUSABLE)) bad.push(name(e) + " is focusable");
      if (e.getAttribute("aria-hidden") === "false") bad.push(name(e) + " un-hides itself");
    }
    return bad;
  };
  // One step of the stage's clock, and what the page looks like after it.
  bc.step = async dt => {
    const late = await Promise.race([window.archieStage.step(dt).then(() => false),
                                     new Promise(r => setTimeout(() => r(true), 8000))]);
    const st = window.archieStage.status();
    if (document.activeElement !== bc.focus0 && bc.focusOff.length < 5)
      bc.focusOff.push(name(document.activeElement) + " at " + st.clock);
    if (st.bit) for (const b of bc.inertNow()) if (!bc.inert.includes(b) && bc.inert.length < 8) bc.inert.push(b);
    return {bit: st.bit, clock: st.clock, cast: Object.keys(st.cast).length, late, flips: bc.flips.length};
  };
  // Scrolling a page to a spot: the top, or an element 250 px down from the top of the window.
  bc.scrollSpot = q => {
    const e = q && document.querySelector(q);
    if (q && !e) return false;
    scrollTo({left: 0, top: e ? Math.max(0, e.getBoundingClientRect().top + scrollY - 250) : 0, behavior: "instant"});
    return true;
  };
  // Where a pointer could rest for a bit that wants one: across the spot's element (or the spotlight, or
  // <main>), some way down from its top edge.
  bc.points = q => {
    const e = (q && document.querySelector(q)) || document.querySelector("article.hero") || document.querySelector("main");
    if (!e) return [];
    const r = e.getBoundingClientRect(), y = Math.max(20, Math.min(innerHeight - 60, r.top + Math.min(160, r.height / 2)));
    return [0.85, 0.15, 0.5].map(f => ({x: Math.round(r.left + r.width * f), y: Math.round(y)}));
  };
  // Somewhere a click lands on nothing: no control, no Archie, not the stage.
  bc.empty = () => {
    for (const [x, y] of [[12, 0.55], [12, 0.75], [innerWidth - 30, 0.55], [innerWidth - 30, 0.75], [innerWidth / 2, 0.97]]) {
      const py = Math.round(innerHeight * y), hit = document.elementFromPoint(x, py);
      if (hit && !hit.closest("a,button,input,select,textarea,summary,label,[tabindex],[role=button],header," + OWN))
        return {x, y: py, hit: name(hit)};
    }
    return null;
  };
  // A cue's row, scrolled as a reader would scroll it, and where it was left.
  bc.scrollRow = dx => {
    const fits = e => { const r = e.getBoundingClientRect(); return r.width >= 400 && r.top >= 0 && r.bottom <= innerHeight && e.scrollWidth > r.width; };
    const row = bc.row || [...document.querySelectorAll(".rowscroll")].find(fits);
    if (!row) return null;
    bc.row = row;
    row.scrollBy({left: dx, behavior: "instant"});
    return (bc.rowLeft = row.scrollLeft);
  };
  bc.rowSettled = () => { if (bc.row) bc.rowLeft = bc.row.scrollLeft; };
})()`;

// A tab, in a browser context of its own, with the recorder in it and the README answered from here.
async function openTab() {
  const {browserContextId} = await send("Target.createBrowserContext", {disposeOnDetach: true});
  const {targetId} = await send("Target.createTarget", {url: "about:blank", browserContextId});
  const {sessionId} = await send("Target.attachToTarget", {targetId, flatten: true});
  const tab = {sessionId, targetId, browserContextId, errors: [], spans: [], hold: false,
               S: (m, p) => send(m, p, sessionId)};
  tabs.set(sessionId, tab);
  const S = tab.S;
  await S("Page.enable"); await S("Runtime.enable"); await S("Log.enable"); await S("Network.enable");
  await S("Fetch.enable", {patterns: [{urlPattern: "https://api.github.com/repos/ollama/ollama*"}]});
  await S("Emulation.setDeviceMetricsOverride", {width: 1400, height: 900, deviceScaleFactor: 1, mobile: false});
  await S("Emulation.setEmulatedMedia", {features: [{name: "prefers-color-scheme", value: "light"}]});
  await S("Page.addScriptToEvaluateOnNewDocument", {source: RECORDER});
  // With a deadline, because a page can stop answering altogether: a bit that loops on `await s.after()`
  // without asking `s.alive` spins forever once it is stopped, since every wait resolves at once after that.
  // The harness then fails that bit and carries on in a new tab, rather than hanging with it.
  tab.ev = async expr => {
    let timer;
    const r = await Promise.race([
      S("Runtime.evaluate", {expression: expr, awaitPromise: true, returnByValue: true, userGesture: true}),
      new Promise((_, rej) => { timer = setTimeout(() => rej(new Error("the page stopped answering: " + expr.slice(0, 60))), 45000); }),
    ]).finally(() => clearTimeout(timer));
    if (r.exceptionDetails) throw new Error(expr.slice(0, 80) + " threw: " + (r.exceptionDetails.exception?.description || r.exceptionDetails.text));
    return r.result.value;
  };
  tab.until = async (expr, ms, every = 150) => {
    for (const end = Date.now() + ms; Date.now() < end; await sleep(every)) if (await tab.ev(expr)) return true;
    return false;
  };
  tab.frames = (n = 2) => tab.ev(`new Promise(r => { let k = ${n}; const f = () => --k ? requestAnimationFrame(f) : r(); requestAnimationFrame(f); })`);
  tab.cookies = async () => JSON.stringify(((await S("Network.getCookies", {urls: [ORIGIN]})).cookies || [])
    .map(c => c.name + "=" + c.value).sort());
  // The index first, as a reader would come: it is where he meets them, and what lets him follow them to
  // the rest of the site (sessionStorage's archie-src and archie-hi).
  tab.ready = await goto(tab, "home");
  return tab;
}

let pass = 0, fail = 0;
const ok = (n, c, extra = "") => { if (c) pass++; else { fail++; console.log("FAIL " + n + (extra ? " -- " + extra : "")); } };
const problems = [];                                       // [bit, check, detail], for the summary at the end
const packless = new Set();                                // "<bit>@<pal>": a pack fetched and not there
const check = (bit, what, c, extra = "") => { ok(`${bit}: ${what}`, c, extra); if (!c) problems.push([bit, what, extra]); };

// A fresh page view of `fam`, with Archie live on it and the stage loaded. His mood is set as though the tab
// had met him just now, from robots.txt on the same origin, so that he is never tired of the reader (eight
// minutes in) or angry with one in the middle of a run. Returns "" or why not.
const atRobots = `location.pathname.endsWith("/robots.txt") && document.readyState === "complete"`;
async function goto(tab, fam, {held = false} = {}) {
  tab.hold = held;
  await tab.S("Page.navigate", {url: ORIGIN + "robots.txt"});
  await tab.until(atRobots, 8000, 100);
  await tab.ev(`sessionStorage.setItem("archie-mood", JSON.stringify({v: 0, since: Date.now()}))`);
  await tab.S("Page.navigate", {url: ORIGIN + URLS[fam] + FLAG});
  if (!(await tab.until(`document.readyState === "complete"`, 20000))) return "the page never finished loading";
  if (!(await tab.until(`!!(window.archie && window.archie.status()) && !!document.querySelector(".mhmascot canvas")`, 40000)))
    return "Archie never went live here";
  if (!(await tab.until(`window.archie.list().some(c => c.startsWith("bit:"))`, 40000, 250))) return "the stage never loaded";
  if (fam === "repo" && !held)
    await tab.until(`(document.querySelector(".source-preview .reader") || {dataset: {}}).dataset.state !== "loading"`, 15000);
  await tab.frames();
  return "";
}
const can = (tab, name) => tab.ev(`window.archie.can(${JSON.stringify("bit:" + name)})`);
const mouse = (tab, p) => tab.S("Input.dispatchMouseEvent", {type: "mouseMoved", x: p.x, y: p.y});

// Where `name` can play: the first family in its `pages` and the first spot on it where `can()` says "".
// Leaves that page open and scrolled there. Returns {fam, spot, pointer} or {why}. Given a place, opens that.
async function place(tab, name, info, again = null) {
  const fams = again ? [again.fam] : (info.pages || Object.keys(URLS)).filter(f => URLS[f] !== undefined)
    .sort((a, b) => (a === "lost") - (b === "lost"));
  const why = [];
  for (const fam of fams) {
    const err = await goto(tab, fam, {held: info.loading});
    if (err) { why.push(`${fam}: ${err}`); continue; }
    let last = "";
    for (const spot of again ? [again.spot] : SPOTS) {
      if (!(await tab.ev(`__bc.scrollSpot(${JSON.stringify(spot)})`))) continue;
      await sleep(300); await tab.frames();
      if (again && again.pointer) { await mouse(tab, again.pointer); await tab.frames(); }
      if ((last = await can(tab, name)) === "") return {fam, spot, pointer: again ? again.pointer : null};
      if (!info.pointer || again) continue;
      for (const p of await tab.ev(`__bc.points(${JSON.stringify(spot)})`)) {
        await mouse(tab, p); await tab.frames();
        if ((last = await can(tab, name)) === "") return {fam, spot, pointer: p};
      }
    }
    why.push(`${fam}: ${last || "none of its spots is on the page"}`);
  }
  return {why};
}
const where = p => p.fam + (p.spot ? " @ " + p.spot : " @ top") + (p.pointer ? " +pointer" : "");

// The page standing still: two pictures of it 400 ms apart that agree. A page still settling after its load
// would otherwise be blamed on the bit. Returns whether it settled.
async function settle(tab) {
  for (let i = 0; i < 12; i++) {
    await tab.ev(`__bc.snap("a")`); await sleep(400); await tab.ev(`__bc.snap("b")`);
    if (!Object.keys(await tab.ev(`__bc.diff("a", "b")`)).length) return true;
  }
  return false;
}

// One bit, played from start to finish (or to `interrupt`), with everything in the header asserted. `label`
// prefixes its assertions. Returns {secs, rate, ended} for the table.
async function trial(tab, name, info, {label = name, interrupt = null} = {}) {
  const {ev} = tab;
  if (!(await settle(tab))) console.log(`  (${label}: the page never stood still before the bit; compared anyway)`);
  await ev(`__bc.snap("before")`);
  const cookies0 = await tab.cookies();
  const from = tab.errors.length;
  await ev(`__bc.arm()`);
  await ev(`window.archieStage.capture(true)`);
  const took = await ev(`window.archie.run(${JSON.stringify("bit:" + name)})`);
  check(label, "taken by archie.run", took === true, String(took));
  // The cast is fetched before the bit's clock starts. A Core projection up when it was asked for is put
  // away on the stage's clock first, so the clock is stepped while there is a stage and no bit yet.
  let st = null;
  for (const end = Date.now() + 60000; Date.now() < end;) {
    st = await ev(`(() => { const s = window.archieStage.status(); return {bit: s.bit, cast: Object.keys(s.cast).length, layer: !!document.querySelector(".pals-stage")}; })()`);
    if (st.bit === name && st.cast >= info.cast.length) break;
    if (!st.bit && st.layer) await ev(`window.archieStage.step(${STEP})`);
    else await sleep(100);
  }
  const started = st && st.bit === name && st.cast >= info.cast.length;
  check(label, "started, with its whole cast on the stage", started, JSON.stringify(st));
  let secs = 0, ended = false, capped = false, stopAt = null, rowSteps = 0, flips = 0, fine = -1;
  if (started) {
    const c0 = await ev(`window.archieStage.status().clock`);
    if (process.env.AAA_BITS_DEBUG) console.log(`  [${label}: cast up]`);
    for (;;) {
      // A fifth of a second a step, except for two stage seconds after any change of theme, which are
      // stepped a frame (1/60 s) at a time. A wait resolves at most once a step, so at 0.2 s a bit flipping
      // the theme every 0.1 s would be read as flipping it every 0.2 s -- half the rate a reader sees.
      const r = await ev(`__bc.step(${secs < fine ? 1 / 60 : STEP})`);
      if (r.late) { check(label, "every step of the clock is taken", false, "a step went unanswered for 8 s"); break; }
      secs = r.clock - c0;
      if (r.flips > flips) { flips = r.flips; fine = secs + 2; }
      if (!r.bit) { ended = true; break; }
      if (secs > CAP) { capped = true; break; }
      // A cue that listens for a row being scrolled gets one: two flicks of a shelf, as a reader gives it.
      if (info.rowCue && ((secs >= 2.5 && secs < 4) || (secs >= 9 && secs < 10.5))) {
        await ev(`__bc.scrollRow(120)`); rowSteps = 2;
      } else if (rowSteps && !--rowSteps) await ev(`__bc.rowSettled()`);
      if (interrupt && stopAt === null && secs >= STOP_AFTER) { await interrupt.send(tab); stopAt = secs; }
    }
    if (capped) {
      check(label, `ends on its own inside ${CAP} stage seconds`, false, `still playing at ${secs.toFixed(1)} s`);
      await ev(`window.archieStage.stop()`);
      for (let n = 0; n < 50 && (await ev(`__bc.step(${STEP})`)).bit; n++);
    } else if (!interrupt) check(label, `ends on its own inside ${CAP} stage seconds`, ended, `stopped stepping at ${secs.toFixed(1)} s`);
    if (interrupt)
      check(label, `${interrupt.what} ${STOP_AFTER} s in ends it within ${STOP_WITHIN} stage second`,
            stopAt !== null && ended && secs - stopAt <= STOP_WITHIN + 1e-6,
            stopAt === null ? `it ended at ${secs.toFixed(1)} s, before the ${interrupt.what} was sent`
                            : `sent at ${stopAt.toFixed(1)} s, ${ended ? "ended" : "still on"} at ${secs.toFixed(1)} s`);
  }
  if (process.env.AAA_BITS_DEBUG && started) console.log(`  [${label}: ${secs.toFixed(1)} stage s stepped]`);
  await tab.frames();
  await ev(`window.archieStage.capture(false)`);
  await ev(`__bc.disarm()`);
  await ev(`__bc.snap("after")`);
  const d = await ev(`__bc.diff("before", "after")`);
  const rec = await ev(`({flips: __bc.flips, added: __bc.added, writes: __bc.writes, focusOff: __bc.focusOff,
                          inert: __bc.inert, said: __bc.said, layer: !!document.querySelector(".pals-stage")})`);
  const j = x => typeof x === "string" ? x : JSON.stringify(x);
  check(label, "the page's elements are as they were (tag, id, class, style)", !d.dom, j(d.dom));
  check(label, "the text of <main> is as it was", !d.text, d.text);
  check(label, "<html>'s attributes are as they were, data-theme included", !d.html, d.html);
  check(label, "the window and every scrollable element are scrolled where they were", !d.scroll && !d.row,
        [d.scroll, d.row].filter(Boolean).join("; "));
  check(label, "the stage's layer is gone", !rec.layer);
  // His mood is the director's to write, every two seconds while the masthead is on screen; any other key,
  // or any write at all from the stage or a bit, is a bit saving something.
  const saved = rec.writes.filter(w => w.bit || w.key !== "archie-mood");
  check(label, "nothing saved: localStorage and sessionStorage as they were, and no write to either",
        !d.local && !d.session && !saved.length,
        [d.local, d.session, saved.length && "written: " + j(saved)].filter(Boolean).join("; "));
  check(label, "no cookie set", !d.cookie && (await tab.cookies()) === cookies0, d.cookie || "");
  check(label, "focus never moved, before, during or after", !d.focus && !rec.focusOff.length,
        [d.focus, ...rec.focusOff].filter(Boolean).join("; "));
  // Flashes: a change of theme and its change back, counted in every one-second window of stage time.
  const t = rec.flips.map(f => f.t).filter(x => x !== null).sort((a, b) => a - b);
  let worst = 0;
  for (let i = 0; i < t.length; i++) worst = Math.max(worst, t.filter(x => x >= t[i] && x < t[i] + 1 - 1e-6).length);
  const rate = worst / 2;
  check(label, "the theme flashes no more than 3 times in any second (WCAG 2.3.1)", rate <= 3,
        `${worst} changes in one second: ${j(rec.flips)}`);
  check(label, "the stage's layer is inert throughout: aria-hidden, no pointer events, nothing focusable",
        !rec.inert.length, rec.inert.join("; "));
  check(label, "nothing added to the document outside the stage's layer", !rec.added.length,
        rec.added.slice(0, 5).join("; ") + (rec.added.length > 5 ? ` (+${rec.added.length - 5} more)` : ""));
  // A pal with no pieces of his own in a bit has no pack, which archie-stage.js's run() says is fine -- and
  // fetches the one he would have anyway: a 404 in the console, and a "pals: pals/bits/<bit>@<pal>.glb"
  // warning. Those two are excused and listed at the end; a clip the bit asks for that he lacks is not.
  const pack = e => {
    const m = /assets\/pals\/bits\/([\w-]+)@(\w+)\.glb\b/.exec(e);
    return m && m[1] === name && info.cast.includes(m[2]) && /\b404\b|Not Found/.test(e) ? m[2] : null;
  };
  const errs = tab.errors.slice(from).filter(e => !(pack(e) && packless.add(`${name}@${pack(e)}`)));
  tab.spans.push([from, tab.errors.length]);
  check(label, "no console error, uncaught exception or swallowed bit exception", !errs.length,
        errs.slice(0, 3).join(" | ").slice(0, 600));
  if (rec.said.length) console.log(`  (${label}: Archie's live region spoke during it: ${j(rec.said.slice(0, 3))})`);
  return {secs, rate, ended};
}

// Work shared out over the tabs: each takes the next job as it comes free. A job that throws -- a page that
// stopped answering, most likely -- fails its bit, and that tab is closed and replaced by a fresh one.
const retired = [];
async function pool(jobs, run) {
  let next = 0;
  await Promise.all(open.map(async (_, i) => {
    while (next < jobs.length) {
      const job = jobs[next++], name = typeof job === "string" ? job : job[0].name;
      try { await run(open[i], job); } catch (e) {
        check(name, "the harness got through it, the page answering throughout", false, String(e.message || e).slice(0, 300));
        if (typeof job === "string" && !rows[name]) rows[name] = {name, where: "-", secs: null, rate: null, result: "FAIL"};
        const old = open[i];
        old.spans.push([0, old.errors.length]);              // its errors belong to the bit just failed
        retired.push(old);
        tabs.delete(old.sessionId);
        await send("Target.closeTarget", {targetId: old.targetId}).catch(() => {});
        await send("Target.disposeBrowserContext", {browserContextId: old.browserContextId}).catch(() => {});
        open[i] = await openTab();
      }
    }
  }));
}

// ---- the bits, as the page has them ---------------------------------------------------------------------
const open = [];
for (let i = 0; i < TABS; i++) open.push(await openTab());
ok("the model goes live under swiftshader, with the stage loaded, in every tab", open.every(t => !t.ready),
   open.map(t => t.ready).filter(Boolean).join("; "));
if (open.some(t => t.ready)) { await browser.close(); console.log(`\n${pass} passed, ${fail} failed`); process.exit(1); }
// Read off the page's own module rather than imported here: the same instance archie.js plays (its `?v=`
// query and all), and a bit whose file reaches for `document` as it loads cannot break the harness.
const ALL = await open[0].ev(`(async () => {
  const src = sessionStorage.getItem("archie-src");
  const B = await import(new URL("archie-bits.js" + new URL(src).search, src).href);
  return Object.fromEntries(Object.entries(B.BITS).map(([n, b]) => [n, {pages: b.pages || null, cast: b.cast || [],
    ready: typeof b.ready === "function" ? b.ready.toString() : "", cue: typeof b.cue === "function" ? b.cue.toString() : ""}]));
})()`);
const listed = await open[0].ev(`window.archie.list().filter(c => c.startsWith("bit:")).map(c => c.slice(4))`);
ok("the director lists every bit in BITS", Object.keys(ALL).every(n => listed.includes(n)),
   Object.keys(ALL).filter(n => !listed.includes(n)).join(", "));
const names = Object.keys(ALL).filter(n => !ONLY.length || ONLY.includes(n));
ok("there are bits to check", names.length > 0, ONLY.length ? `none of ${ONLY.join(", ")} is in BITS` : "BITS is empty");
for (const n of names) {
  const b = ALL[n];
  b.pointer = /pointer/i.test(b.ready);                     // its ready() reads where the reader's pointer is
  b.loading = /["']loading["']/.test(b.ready);              // ...or wants the README reader still loading
  b.rowCue = /rowscroll/.test(b.cue);                       // its cue listens for a row being scrolled
}

const rows = Object.fromEntries(names.map(n => [n, null]));
await pool(names, async (tab, name) => {
  const info = ALL[name];
  const t0 = Date.now();
  const at = await place(tab, name, info);
  if (process.env.AAA_BITS_DEBUG) console.log(`  [${name}: placed in ${((Date.now() - t0) / 1000).toFixed(1)} s]`);
  if (at.why) {
    rows[name] = {name, where: "-", secs: null, rate: null, result: "skipped (" + at.why.join("; ") + ")"};
    console.log(`  ${name.padEnd(26)} skipped (${at.why.join("; ")})`);
    return;
  }
  const before = problems.filter(p => p[0] === name).length;
  const r = await trial(tab, name, info);
  const result = problems.filter(p => p[0] === name).length > before ? "FAIL" : "pass";
  rows[name] = {name, at, where: where(at), secs: r.secs, rate: r.rate, ended: r.ended, result};
  console.log(`  ${name.padEnd(26)} ${where(at).padEnd(38)} ${r.secs.toFixed(1).padStart(6)} s  ` +
              `worst ${r.rate} flashes/s  ${result}`);
});

// ---- stopping ----------------------------------------------------------------------------------------
// The longest bits, because a long bit is the one a reader most wants to be able to stop: three by Escape,
// one more by a pointerdown on an empty part of the page. Each is a fresh page view at the place it played.
const long = Object.values(rows).filter(r => r && r.at && r.ended && r.secs >= STOP_AFTER + 2).sort((a, b) => b.secs - a.secs);
const escape = {what: "Escape", send: async tab => {
  for (const type of ["keyDown", "keyUp"])
    await tab.S("Input.dispatchKeyEvent", {type, key: "Escape", code: "Escape", windowsVirtualKeyCode: 27, nativeVirtualKeyCode: 27});
}};
const poke = {what: "a pointerdown on an empty part of the page", send: async tab => {
  const p = await tab.ev(`__bc.empty()`);
  if (!p) return;
  for (const type of ["mousePressed", "mouseReleased"])
    await tab.S("Input.dispatchMouseEvent", {type, x: p.x, y: p.y, button: "left", buttons: type === "mousePressed" ? 1 : 0, clickCount: 1});
}};
const stops = [...long.slice(0, 3).map(r => [r, escape]), ...long.slice(3, 4).map(r => [r, poke])];
if (!ONLY.length) ok("four bits long enough to stop mid-way", stops.length === 4, `${long.length} played for over ${STOP_AFTER + 2} s`);
await pool(stops, async (tab, [row, how]) => {
  const at = await place(tab, row.name, ALL[row.name], row.at);
  if (at.why) { check(row.name, `placed again for the ${how.what}`, false, at.why.join("; ")); return; }
  if (how === poke) check(row.name, "there is an empty spot to click", !!(await tab.ev(`__bc.empty()`)));
  const r = await trial(tab, row.name, ALL[row.name], {label: `${row.name} (${how.what})`, interrupt: how});
  console.log(`  ${row.name.padEnd(26)} stopped by ${how.what} at ${STOP_AFTER} s: gone at ${r.secs.toFixed(1)} s`);
});

// The pages' own errors, outside any bit: not a bit's doing, but not to be lost either.
const outside = [...open, ...retired].flatMap(t => t.errors.filter((_, i) => !t.spans.some(([a, b]) => i >= a && i < b)));
ok("no console errors on the pages outside the bits", !outside.length, outside.slice(0, 3).join(" | ").slice(0, 600));
if (packless.size)
  console.log(`\npacks fetched and not there (a 404 each, excused above): ${[...packless].sort().join(", ")}`);
if (problems.length) {
  console.log("\nbit problems:");
  for (const [bit, what, extra] of problems) console.log(`  ${bit}: ${what}${extra ? " -- " + extra : ""}`);
}
const all = Object.values(rows).filter(Boolean);
console.log(`\nbits: ${all.filter(r => r.result === "pass").length} clean, ${all.filter(r => r.result === "FAIL").length} with ` +
            `problems, ${all.filter(r => r.result.startsWith("skipped")).length} skipped, in ` +
            `${((Date.now() - STARTED) / 1000).toFixed(0)} s`);
await browser.close();
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
