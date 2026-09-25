// Archie's friends (`docs/assets/archie-friends.js`), each sent for with `?archie=friend:<id>` on the live
// model, which goes through every gate an unasked visit does but the dice and the wait. What is asserted is
// what the reader is promised in that file's header: a friend comes, says its own lines, gets one of
// Archie's, does its trick and leaves on its own, well inside the hard stop, and takes no clicks once it
// has faded; the page's own DOM is byte-for-byte what it was
// before; nothing took focus or was saved; the layer takes no pointer events and no control on screen is
// under a friend for more than a moment; nothing on the layer changes opacity faster than 3 times a second;
// and a click anywhere, Escape, Tab, a poke, or reduced motion switched on mid-visit each send it away at once.
// Then the gates that keep a friend from coming at all: Quiet mode, reduced motion, a narrow screen, no
// WebGL, and the first twenty seconds of an unflagged page view.
//
// WHAT THIS HARNESS CANNOT SEE: whether a friend is funny or well drawn (the screenshots in the PR are the
// evidence for that), and the dice: a quarter of page views, one visit at most, 20 to 60 seconds in. Waiting
// that out would be a minute a run and prove only that `Math.random` works. What it does check is that an
// unflagged page view brings nobody inside the first twenty seconds.
//
// The model has to go live, so WebGL is swiftshader's, as in prank-check.mjs.
//
//   node tests/friends-check.mjs <chrome-binary> <origin>
import {tmpdir} from "node:os";
import {launch} from "./lib/browser.mjs";

const BIN = process.argv[2], ORIGIN = process.argv[3].replace(/\/?$/, "/");
const TMP = process.env.AAA_TMP || tmpdir();
const {FRIENDS, ORDER} = await import(new URL("../docs/assets/archie-friends-data.js", import.meta.url));
const TRICKS = {nib: "borrow", posy: "note", lumen: "photobomb", "oh-four": "peek", quack: "debug"};
const texts = list => (list || []).map(l => l[0]);
// A friend's own lines, and Archie's lines about it
const own = id => { const L = FRIENDS[id].lines, t = TRICKS[id];
  return [...texts(L.arrive), ...texts(L.skin), ...texts(L[t]), ...texts(L[`${t}-after`]), ...texts(L.leave)]; };
const his = id => { const L = FRIENDS[id].lines, t = TRICKS[id];
  return [...texts(L[`${t}-archie`]), ...texts(L[`${t}-archie-2`]), ...texts(L.poke)]; };

process.env.AAA_CHROME_FLAGS = [process.env.AAA_CHROME_FLAGS || "", "--enable-unsafe-swiftshader",
  "--use-angle=swiftshader"].join(" ");
const browser = await launch(BIN, TMP, "friends");

const sleep = ms => new Promise(r => setTimeout(r, ms));
let id = 0;
const waiters = new Map(), errors = [];
const ws = new WebSocket(browser.wsUrl);
await new Promise(r => ws.addEventListener("open", r, {once: true}));
const send = (method, params = {}, sid) => new Promise((res, rej) => {
  const n = ++id; waiters.set(n, {res, rej});
  ws.send(JSON.stringify({id: n, method, params, ...(sid ? {sessionId: sid} : {})}));
});
ws.addEventListener("message", ev => {
  const m = JSON.parse(ev.data);
  if (m.id && waiters.has(m.id)) {
    const w = waiters.get(m.id); waiters.delete(m.id);
    m.error ? w.rej(new Error(m.error.message)) : w.res(m.result);
  } else if (m.method === "Runtime.exceptionThrown") errors.push(m.params.exceptionDetails.exception?.description || "exception");
  else if (m.method === "Log.entryAdded" && m.params.entry.level === "error" &&
           !/cloudflareinsights|beacon|opengraph\.githubassets\.com/.test(m.params.entry.text + " " + (m.params.entry.url || "")))
    errors.push(m.params.entry.text);
});
const {targetId} = await send("Target.createTarget", {url: "about:blank"});
const {sessionId} = await send("Target.attachToTarget", {targetId, flatten: true});
const S = (m, p) => send(m, p, sessionId);
await S("Page.enable"); await S("Runtime.enable"); await S("Log.enable");
const size = w => S("Emulation.setDeviceMetricsOverride", {width: w, height: 900, deviceScaleFactor: 1, mobile: false});
await size(1440);
// The recorder, in every document before the page's own scripts. Archie's lines (his bubble in the header)
// and the friend's (its bubble on the layer) are kept apart; every localStorage write; and, every 100 ms
// while a friend is on the layer, which on-screen controls are under it, how long each has been, and the
// opacity animations running on the layer.
await S("Page.addScriptToEvaluateOnNewDocument", {source: `(() => {
  const rec = window.__rec = {archie: [], friend: [], writes: [], seen: 0, gone: 0, covered: 0, coveredBy: "",
                              fast: [], props: {}, near: 1e9, overlap: 0, ghost: 0};
  const set = Storage.prototype.setItem;
  Storage.prototype.setItem = function (k, v) { if (this === localStorage) rec.writes.push(k); return set.call(this, k, v); };
  new MutationObserver(ms => { for (const m of ms) {
    const e = m.target.nodeType === 1 ? m.target : m.target.parentElement;
    const b = e && e.closest && e.closest(".archie-say");
    if (!b || !b.textContent) continue;
    const list = b.closest(".archie-pals") ? rec.friend : rec.archie;
    if (list.at(-1) !== b.textContent) list.push(b.textContent);
  } }).observe(document, {subtree: true, childList: true, characterData: true});
  const under = new Map(), started = new WeakSet(), starts = new Map();
  setInterval(() => {
    const layer = document.querySelector(".archie-pals");
    if (!layer) { if (rec.seen && !rec.gone) rec.gone = performance.now(); under.clear(); return; }
    if (!rec.seen) rec.seen = performance.now();
    for (const c of ["mask", "glyph", "note"]) { const x = layer.querySelector("." + c); if (x) rec.props[c] = x.textContent || "yes"; }
    for (const el of document.querySelectorAll("a[href],button,input,select,textarea,summary")) {
      const r = el.getBoundingClientRect();
      if (!r.width || r.bottom < 0 || r.top > innerHeight || r.right < 0 || r.left > innerWidth) continue;
      const hit = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
      if (hit && layer.contains(hit)) {
        const t = (under.get(el) || 0) + 100;
        under.set(el, t);
        if (t > rec.covered) { rec.covered = t; rec.coveredBy = (el.textContent || el.tagName).trim().slice(0, 40); }
      } else under.delete(el);
    }
    // A flash is a change of light and back. Two ways to make three a second: one animation repeating
    // faster than 333 ms a cycle, or animations started on one element more than three times in a second.
    for (const a of document.getAnimations()) {
      const t = a.effect && a.effect.target;
      if (!t || !layer.contains(t) || started.has(a)) continue;
      started.add(a);
      const k = a.effect.getKeyframes(), tm = a.effect.getTiming();
      if (!k.some(f => "opacity" in f || "filter" in f || "backgroundColor" in f || "color" in f)) continue;
      if ((tm.iterations > 1) && tm.duration < 333) rec.fast.push("repeating every " + tm.duration + " ms");
      const list = (starts.get(t) || []).filter(s => s > performance.now() - 1000);
      list.push(performance.now());
      starts.set(t, list);
      if (list.length > 3) rec.fast.push(list.length + " light changes in a second on " + (t.className || t.tagName));
    }
    // A friend that still takes clicks but has faded out is an invisible patch of page that swallows the
    // reader's click. (One off the window is not: the layer clips it, so there is nothing there to click.)
    const me = layer.querySelector(".pal");
    if (me && getComputedStyle(me).pointerEvents !== "none" &&
        +getComputedStyle(me).opacity * +getComputedStyle(layer).opacity < 0.2) rec.ghost += 100;
    // Lumen's landing, against the Spotlight's corner; Oh-Four's visible part, against the button
    const pal = layer.querySelector(".pal"), p = pal && pal.getBoundingClientRect();
    const hero = document.querySelector("main .hero");
    if (p && hero && layer.dataset.friend === "lumen") {
      const h = hero.getBoundingClientRect();
      rec.near = Math.min(rec.near, Math.hypot(p.left + p.width / 2 - h.left, p.top + p.height / 2 - h.top));
    }
    const clip = layer.querySelector(".clip"), cta = document.querySelector("header a.cta");
    if (p && clip && cta) {
      const c = clip.getBoundingClientRect(), b = cta.getBoundingClientRect();
      const top = Math.max(p.top, c.top), bottom = Math.min(p.bottom, c.bottom);
      const left = Math.max(p.left, c.left), right = Math.min(p.right, c.right);
      if (bottom > top && right > left)
        rec.overlap = Math.max(rec.overlap, Math.min(bottom, b.bottom) - Math.max(top, b.top) > 0.5 &&
                                            Math.min(right, b.right) - Math.max(left, b.left) > 0.5 ? 1 : 0);
    }
  }, 100);
})()`});
const ev = async expr => {
  const r = await S("Runtime.evaluate", {expression: expr, awaitPromise: true, returnByValue: true});
  if (r.exceptionDetails) throw new Error(expr.slice(0, 60) + " threw: " + (r.exceptionDetails.exception?.description || r.exceptionDetails.text));
  return r.result.value;
};
const until = async (expr, ms) => {
  for (const end = Date.now() + ms; Date.now() < end; await sleep(100)) if (await ev(expr)) return true;
  return false;
};
const goto = async (q = "", live = true) => {
  await S("Page.navigate", {url: ORIGIN + q});
  await until("document.readyState === 'complete'", 15000);
  return live ? until(`!!document.querySelector(".mhmascot[data-live]")`, 30000) : true;
};
// The page's own DOM, as a reader has it: <main> whole, and the header without the three things Archie
// himself keeps in it (his canvas, his bubble and his poke target), which change with his every line. Less
// the parts the page fills in itself whenever GitHub answers -- the "This atlas on GitHub" row
// (`[data-ghrow]`) and the masthead's star count (`[data-gh]`) -- which on a cold first load land mid-visit.
const PAGE = `(() => {
  const h = document.querySelector("header").cloneNode(true), m = document.querySelector("main").cloneNode(true);
  h.querySelectorAll("canvas,.archie-say,.archie-poke,.archie-sr").forEach(e => e.remove());
  for (const x of [h, m]) x.querySelectorAll("[data-ghrow],[data-gh]").forEach(e => e.remove());
  // Archie's own state, which he reports on his slot for the harnesses: what he plays and where the rig is.
  h.querySelectorAll(".mhmascot").forEach(e => { delete e.dataset.act; delete e.dataset.rig; });
  return m.outerHTML + h.outerHTML + document.title;
})()`;
const rec = () => ev(`window.__rec`);
const PAL = `!!document.querySelector(".archie-pals .pal")`, GONE = `!document.querySelector(".archie-pals")`;

let pass = 0, fail = 0;
const ok = (n, c, extra = "") => { if (c) pass++; else { fail++; console.log("FAIL " + n + (extra ? " -- " + extra : "")); } };

// ---- every friend, sent for, start to finish
for (const f of ORDER) {
  ok(`${f}: the model goes live under swiftshader`, await goto(`?archie=friend:${f}`));
  const page0 = await ev(PAGE);
  ok(`${f}: comes when sent for`, await until(PAL, 20000));
  ok(`${f}: ...as ${f}, and nobody else`, await ev(`document.querySelector(".archie-pals").dataset.friend`) === f);
  ok(`${f}: ...on a layer hidden from assistive technology and taking no pointer events`, await ev(`(() => {
    const l = document.querySelector(".archie-pals");
    return l.getAttribute("aria-hidden") === "true" && getComputedStyle(l).pointerEvents === "none" &&
      [...l.querySelectorAll("*")].every(e => e.classList.contains("pal") || e.closest(".pal") || getComputedStyle(e).pointerEvents === "none");
  })()`));
  // The box as laid out, not as drawn: a friend tipping mid-flutter has a wider bounding rect than target.
  ok(`${f}: ...with a poke target no bigger than 56 px`, await ev(`(() => { const p = document.querySelector(".archie-pals .pal");
    return p.offsetWidth <= 56 && p.offsetHeight <= 56; })()`));
  ok(`${f}: gone again within the 25 s hard stop`, await until(GONE, 27000));
  await sleep(300);
  const r = await rec();
  ok(`${f}: ...on screen for a visit's length, not a flicker`, r.gone - r.seen > 5000, `${Math.round(r.gone - r.seen)} ms`);
  // A visit that ends only because the hard stop fired is one whose teardown is broken.
  ok(`${f}: ...and gone on its own, well before the hard stop`, r.gone - r.seen < 23000, `${Math.round(r.gone - r.seen)} ms`);
  ok(`${f}: ...never taking clicks once faded out`, r.ghost <= 200, `${r.ghost} ms`);
  ok(`${f}: said something, all of it its own lines`, r.friend.length > 0 && r.friend.every(t => own(f).includes(t)),
     JSON.stringify(r.friend));
  const about = r.archie.filter(t => his(f).includes(t));
  ok(`${f}: Archie answered with one of his lines about ${f}`, about.length > 0, JSON.stringify(r.archie));
  const page1 = await ev(PAGE);
  let at0 = 0; while (at0 < page0.length && page0[at0] === page1[at0]) at0++;      // in code units, as slice() counts
  ok(`${f}: the page's DOM is exactly what it was`, page1 === page0,
     `first difference at ${at0}: ${JSON.stringify(page0.slice(at0 - 120, at0 + 80))} became ${JSON.stringify(page1.slice(at0 - 120, at0 + 80))}`);
  ok(`${f}: ...no style left behind`, await ev(`![...document.querySelectorAll("style")].some(s => s.textContent.includes(".archie-pals"))`));
  // The page caches its GitHub star count (`atlas-gh-*`) on a first visit; that one is not ours.
  const writes = r.writes.filter(k => !k.startsWith("atlas-gh-"));
  ok(`${f}: ...nothing saved`, writes.length === 0, JSON.stringify(writes));
  ok(`${f}: ...and focus never moved`, await ev(`document.activeElement === document.body`));
  ok(`${f}: no control on screen under a friend for more than 1.5 s`, r.covered <= 1500,
     `${r.covered} ms over "${r.coveredBy}"`);
  ok(`${f}: nothing on the layer changes opacity faster than 3 times a second (WCAG 2.3.1)`, r.fast.length === 0,
     JSON.stringify(r.fast.slice(0, 5)));
  if (f === "nib") {
    ok("nib: lifted a letter, with a chip over the gap it left", r.props.mask && /^[A-Za-z]$/.test(r.props.glyph || ""),
       JSON.stringify(r.props));
    ok("nib: ...one that is really in a heading on the page", await ev(`[...document.querySelectorAll("main h2")].some(h => h.textContent.includes(${JSON.stringify(r.props.glyph || "?")}))`));
  }
  if (f === "posy") ok("posy: left one of her notes", texts(FRIENDS.posy.notes).includes(r.props.note), JSON.stringify(r.props));
  if (f === "lumen") ok("lumen: landed on the Spotlight's corner", r.near < 30, `${Math.round(r.near)} px away at closest`);
  if (f === "oh-four") ok("oh-four: never a pixel of him over the search button", r.overlap === 0);
  if (f === "quack") {
    const A = texts(FRIENDS.quack.lines["debug-archie"]), B = texts(FRIENDS.quack.lines["debug-archie-2"]);
    const i = A.findIndex(t => r.archie.includes(t));
    ok("quack: Archie explained, then found his bug, the realisation paired with the explanation",
       i >= 0 && r.archie.indexOf(B[i]) > r.archie.indexOf(A[i]), JSON.stringify(r.archie));
  }
}

// ---- sent away
const click = async (x, y) => {
  for (const type of ["mousePressed", "mouseReleased"])
    await S("Input.dispatchMouseEvent", {type, x, y, button: "left", clickCount: 1});
};
await goto("?archie=friend:quack");
await until(PAL, 20000);
await click(700, 880);
ok("a click anywhere else sends the friend away within a second", await until(GONE, 1000));
await goto("?archie=friend:quack");
await until(PAL, 20000);
await S("Input.dispatchKeyEvent", {type: "keyDown", key: "Escape", code: "Escape", windowsVirtualKeyCode: 27});
await S("Input.dispatchKeyEvent", {type: "keyUp", key: "Escape", code: "Escape", windowsVirtualKeyCode: 27});
ok("...and so does Escape", await until(GONE, 1000));
await goto("?archie=friend:quack");
await until(PAL, 20000);
await S("Input.dispatchKeyEvent", {type: "keyDown", key: "Tab", code: "Tab", windowsVirtualKeyCode: 9});
await S("Input.dispatchKeyEvent", {type: "keyUp", key: "Tab", code: "Tab", windowsVirtualKeyCode: 9});
ok("...and so does Tab, before focus can land under the friend", await until(GONE, 1000));
await goto("?archie=friend:quack");
await until(PAL, 20000);
await sleep(2600);                                         // bobbed in and sitting still
const at = await ev(`(() => { const r = document.querySelector(".archie-pals .pal").getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; })()`);
await click(at[0], at[1]);
ok("poked, the friend says goodbye and goes", await until(GONE, 3000));
let r = await rec();
ok("...and Archie apologises for it", r.archie.some(t => texts(FRIENDS.quack.lines.poke).includes(t)), JSON.stringify(r.archie));
await goto("?archie=friend:lumen");
await until(PAL, 20000);
await ev(`document.querySelector(".archie-poke").click()`);
await sleep(300);
r = await rec();
ok("poking Archie mid-visit gets a line about the guest", texts(FRIENDS.lumen.lines.poke).includes(r.archie.at(-1)), JSON.stringify(r.archie));
ok("...and the guest stays", await ev(PAL));
await S("Emulation.setEmulatedMedia", {features: [{name: "prefers-reduced-motion", value: "reduce"}]});
ok("reduced motion switched on mid-visit: the friend is gone at once", await until(GONE, 1000));
ok("...with Archie, back to his poster", await until(`!document.querySelector(".mhmascot[data-live]")`, 2000));

// ---- the gates: nobody comes
await goto("?archie=friend:nib", false);
await sleep(9000);
ok("reduced motion: nobody comes, and the friends' script is never fetched", await ev(GONE) &&
   await ev(`!performance.getEntriesByType("resource").some(e => /archie-friends/.test(e.name))`));
await S("Emulation.setEmulatedMedia", {features: []});

await ev(`localStorage.setItem("atlas-byte-quiet", "1")`);
ok("quiet mode: the model still goes live", await goto("?archie=friend:nib"));
await sleep(8000);
r = await rec();
ok("...but no friend comes", !r.seen, JSON.stringify(r));
await ev(`localStorage.removeItem("atlas-byte-quiet")`);

await size(800);
await goto("?archie=friend:nib", false);
await sleep(8000);
ok("a screen under 900 px: nobody comes, nothing fetched", await ev(GONE) &&
   await ev(`!performance.getEntriesByType("resource").some(e => /archie-friends/.test(e.name))`));
await size(1440);

const noGL = await S("Page.addScriptToEvaluateOnNewDocument", {source: `(() => { const g = HTMLCanvasElement.prototype.getContext;
  HTMLCanvasElement.prototype.getContext = function (k, ...a) { return /webgl/.test(k) ? null : g.call(this, k, ...a); }; })()`});
await goto("?archie=friend:nib", false);
await sleep(8000);
ok("no WebGL: nobody comes, nothing fetched", await ev(GONE) &&
   await ev(`!performance.getEntriesByType("resource").some(e => /archie-friends/.test(e.name))`));
await S("Page.removeScriptToEvaluateOnNewDocument", {identifier: noGL.identifier});

ok("unflagged: the model goes live", await goto());
const load = await ev(`performance.getEntriesByType("navigation")[0].loadEventEnd`);
// Watched until the page's own clock passes 20 s, however long the model took to go live: on CI it can be
// most of that (a run failed "now 20537" with nobody seen, which is a slow runner, not a visitor). Anyone
// seen counts only if it came before the 20 s mark.
for (let t = Date.now(); Date.now() - t < 30000 && await ev(`performance.now() < 20000`);) await sleep(250);
r = await rec();
const now = await ev("performance.now()");
ok("...and nobody comes in the first twenty seconds", now >= 20000 && (!r.seen || r.seen >= 20000),
   `seen at ${r.seen}, now ${now}`);
const fetched = await ev(`performance.getEntriesByType("resource").filter(e => /archie-friends/.test(e.name)).map(e => e.startTime)`);
ok("...and whatever it fetches for them, it fetches after the page's load", fetched.every(t => t >= load),
   `load ${load}, fetched ${JSON.stringify(fetched)}`);

ok("no console errors", errors.length === 0, errors.join(" | "));
await browser.close();
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
