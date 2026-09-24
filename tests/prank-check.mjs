// Archie's pranks and moods, played for real on the live model: each prank is asked for with `?archie=prank:<name>`,
// which goes through the same gates as a prank he picks himself, and what is asserted is the page after it
// -- put back exactly as it was, nothing saved, and a reader who changed something mid-prank keeping it.
// The lights are timed as well as counted, because their rate is the one thing here with a safety rule
// behind it: WCAG 2.3.1 allows three flashes a second, and they are meant to make 1.25.
//
// WHAT THIS HARNESS CANNOT SEE: whether a prank is funny, and when he picks one unasked -- the three-minute
// gap and the one-in-three roll are the director's, and waiting them out would be a four-minute test. Nor
// the tab title under a real tab switch: `document.hidden` is overridden and the event dispatched by hand.
//
// Then his mood, which is sessionStorage's `archie-mood` and is set there before each page load: that
// being ignored lowers it and a poke or a resting pointer raises it, that it carries to the next page, that
// one poke forgives anything, that he adores a reader who pokes a lot and plays his pranks as payback on one
// who does not, and that each of his attempts to get rid of a reader comes to nothing and leaves the page
// as it was. Not the eight minutes before he tires of a reader: `?archie=tired:<name>` skips them.
//
// And following the reader down the page: scrolled away from the masthead, he comes down a fireman's pole
// or in a lift (`?archie=visit:pole`, `visit:lift`), drawn behind him in the visit's fixed layer, and every
// prop is gone again whether he leaves the way he came or the reader scrolls back up mid-visit.
//
// And off the index: met there, he follows the reader to the rest of the site and docks in a corner of the
// window, live, carrying his mood and saying so; and he does not, even as far as fetching himself, for a
// reader who never met him in this tab, one in Quiet mode, or a URL in `archie-src` from another origin.
//
// To the music, fed as the beat detector feeds it (`archie:music`, `archie:beat`, `window.archieMusic`): he
// dances and the rig is lit while the beats come; two seconds after they stop, the dance is cut off where it
// was and he only idles, the rig still hung but dark and still, until the beats come back and so does it;
// and with music mode off, the rig is hauled away.
//
// The model has to go live, so WebGL is swiftshader's; a Chrome that cannot give it one fails the first
// assertion rather than passing the rest on the poster, which plays no pranks.
//
//   node tests/prank-check.mjs <chrome-binary> <origin>
import {readFileSync, readdirSync} from "node:fs";
import {tmpdir} from "node:os";
import {launch} from "./lib/browser.mjs";

const BIN = process.argv[2], ORIGIN = process.argv[3].replace(/\/?$/, "/");
const TMP = process.env.AAA_TMP || tmpdir();

// His lines, read from the script, so a bubble can be checked against the set it must come from.
const SRC = readFileSync(new URL("../docs/assets/archie.js", import.meta.url), "utf8");
const lines = key => {
  const m = SRC.match(new RegExp(`\\s"?${key}"?: (\\[\\[[\\s\\S]*?\\]\\])(?=,\\s*\\n)`));
  if (!m) throw new Error(`no LINES["${key}"] in archie.js`);
  return Function(`return ${m[1]}`)().map(l => l[0]);
};
const AWAY = Function(`return ${SRC.match(/const AWAY = (\[[^\]]*\])/)[1]}`)();
const OURS = name => [...lines(`prank-${name}`), ...lines(`prank-${name}-after`)];

process.env.AAA_CHROME_FLAGS = [process.env.AAA_CHROME_FLAGS || "", "--enable-unsafe-swiftshader",
  "--use-angle=swiftshader"].join(" ");
const browser = await launch(BIN, TMP, "prank");

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
  // The Cloudflare beacon cannot pass CORS against localhost; pwa-check.mjs excuses it the same way.
  else if (m.method === "Log.entryAdded" && m.params.entry.level === "error" &&
           !/cloudflareinsights|beacon|opengraph\.githubassets\.com/.test(m.params.entry.text + " " + (m.params.entry.url || "")))
    errors.push(m.params.entry.text);
});
const {targetId} = await send("Target.createTarget", {url: "about:blank"});
const {sessionId} = await send("Target.attachToTarget", {targetId, flatten: true});
const S = (m, p) => send(m, p, sessionId);
await S("Page.enable"); await S("Runtime.enable"); await S("Log.enable");
await S("Emulation.setDeviceMetricsOverride", {width: 1440, height: 900, deviceScaleFactor: 1, mobile: false});
// The recorder, in every document before the page's own scripts: every change to the theme and skin on
// <html>, with when it happened; every write to localStorage; every line in his bubble.
await S("Page.addScriptToEvaluateOnNewDocument", {source: `(() => {
  const rec = window.__rec = {attr: [], writes: [], said: []};
  const set = Storage.prototype.setItem;
  Storage.prototype.setItem = function (k, v) { if (this === localStorage) rec.writes.push(k); return set.call(this, k, v); };
  new MutationObserver(ms => { for (const m of ms) {
    if (m.type === "attributes" && m.target === document.documentElement)
      rec.attr.push({t: performance.now(), name: m.attributeName, v: m.target.getAttribute(m.attributeName)});
    const b = (m.target.closest ? m.target : m.target.parentElement)?.closest?.(".archie-say");
    if (b && m.type === "childList" && b.textContent && rec.said.at(-1)?.text !== b.textContent)
      rec.said.push({t: performance.now(), text: b.textContent});
  } }).observe(document, {subtree: true, childList: true, attributes: true, attributeFilter: ["data-theme", "data-skin"]});
})()`});
const ev = async expr => {
  const r = await S("Runtime.evaluate", {expression: expr, awaitPromise: true, returnByValue: true, userGesture: true});
  if (r.exceptionDetails) throw new Error(expr.slice(0, 60) + " threw: " + (r.exceptionDetails.exception?.description || r.exceptionDetails.text));
  return r.result.value;
};
// `mood` is his mood on arrival, as though the tab had met him just now; null keeps whatever it was. It is
// set from robots.txt, on the same origin, because a page with him on it saves his own mood every two
// seconds and would write over it before the navigation.
const goto = async (q = "", mood = 0) => {
  if (mood !== null) {
    await S("Page.navigate", {url: ORIGIN + "robots.txt"});
    for (let i = 0; i < 40 && !(await ev(`location.pathname === "/robots.txt" && document.readyState === "complete"`)); i++)
      await sleep(100);
    await ev(`sessionStorage.setItem("archie-mood", JSON.stringify({v: ${mood}, since: Date.now()}))`);
  }
  await S("Page.navigate", {url: ORIGIN + q});
  for (let i = 0; i < 80 && !(await ev("document.readyState === 'complete'")); i++) await sleep(150);
  for (let i = 0; i < 200 && !(await ev(`!!document.querySelector(".mhmascot[data-live]")`)); i++) await sleep(150);
  return ev(`!!document.querySelector(".mhmascot[data-live]")`);
};
// Until a condition on the page holds, or `ms` passes; returns whether it did.
const until = async (expr, ms) => {
  for (const end = Date.now() + ms; Date.now() < end; await sleep(100)) if (await ev(expr)) return true;
  return false;
};
const rec = () => ev(`window.__rec`);
// Whether the bubble's latest line is one of LINES[key], within `ms`.
const saying = (key, ms = 20000) => until(`${JSON.stringify(lines(key))}.includes(__rec.said.at(-1)?.text)`, ms);
// The prank is over when its excuse is in the bubble; a second more for the shrug's restore to land.
const over = async key => { const ok = await saying(key, 25000); await sleep(1000); return ok; };
const done = name => over(`prank-${name}-after`);
let pass = 0, fail = 0;
const ok = (n, c, extra = "") => { if (c) pass++; else { fail++; console.log("FAIL " + n + (extra ? " -- " + extra : "")); } };
// The changes to an attribute of <html> from `from` on, as values: the page sets both itself as it loads,
// and setting one to the value it already has is recorded too, so neither counts as a change.
const changes = (r, name, from) => {
  const all = r.attr.filter(a => a.name === name), out = [];
  let was = all.filter(a => a.t < from).at(-1)?.v ?? null;
  for (const a of all) if (a.t >= from && a.v !== was) { out.push(a); was = a.v; }
  return out;
};
const setup = (r, name) => r.said.find(s => lines(`prank-${name}`).includes(s.text))?.t ?? 1e12;
const document_has = (r, key) => r.said.some(s => lines(key).includes(s.text));
const saidOnly = (r, name, from) => r.said.filter(s => s.t >= from).every(s => OURS(name).includes(s.text));

// ---- lights
ok("the model goes live under swiftshader, which the pranks need", await goto("?archie=prank:lights"));
const start = await ev(`({theme: document.documentElement.dataset.theme, stored: localStorage.getItem("theme")})`);
ok("lights: announced with one of its own set-up lines",
   await until(`${JSON.stringify(lines("prank-lights"))}.includes(__rec.said.at(-1)?.text)`, 20000));
ok("...and finished with one of its excuses", await done("lights"));
let r = await rec();
const flips = changes(r, "data-theme", setup(r, "lights"));
const gaps = flips.slice(1).map((f, i) => f.t - flips[i].t);
ok("...the theme swapped four times", flips.length === 4, JSON.stringify(flips.map(f => f.v)));
ok("...at most 3 flashes a second: every swap at least 333 ms after the last (WCAG 2.3.1)",
   gaps.every(g => g >= 333), JSON.stringify(gaps.map(Math.round)));
// The upper bound is loose: a timer runs late on a busy main thread (618 ms once, on a cold first load),
// and late is the safe direction. It is here so that a swap on some other clock cannot pass.
ok("...and near the 400 ms it is meant to take, so this is the rate asserted",
   gaps.every(g => g <= 800), JSON.stringify(gaps.map(Math.round)));
ok("...ending on the theme it started on", await ev(`document.documentElement.dataset.theme`) === start.theme);
ok("...with nothing saved", !r.writes.includes("theme") &&
   await ev(`localStorage.getItem("theme")`) === start.stored, JSON.stringify(r.writes));
ok("...and not remarked on as if the reader had done it: no light, dark or flip line",
   flips.length && saidOnly(r, "lights", flips[0].t - 50),
   JSON.stringify(r.said.map(s => s.text)));

// ---- lights, with the reader changing the theme in the middle of it
await goto("?archie=prank:lights");
ok("mid-flicker, a reader's own choice of theme can be made",
   await until(`__rec.attr.filter(a => a.name === "data-theme").length >= 3`, 25000));
await ev(`document.getElementById("theme").click()`);
const chose = await ev(`localStorage.getItem("theme")`);
await done("lights");
ok("...and is still standing after the prank", await ev(`document.documentElement.dataset.theme`) === chose &&
   await ev(`localStorage.getItem("theme")`) === chose, `chose ${chose}`);
r = await rec();
ok("...which stopped flickering when they chose", changes(r, "data-theme", setup(r, "lights")).length <= 3,
   JSON.stringify(r.attr.map(a => a.v)));
await ev(`localStorage.removeItem("theme")`);

// ---- skin
await goto("?archie=prank:skin");
const skin0 = await ev(`document.documentElement.dataset.skin || ""`);
ok("skin: finished with one of its excuses", await done("skin"));
r = await rec();
const skins = changes(r, "data-skin", setup(r, "skin")).map(a => a.v);
ok("...Prism for a moment", skins[0] === (skin0 === "prism" ? "terminal" : "prism"), JSON.stringify(skins));
ok("...then the reader's skin back", (await ev(`document.documentElement.dataset.skin || ""`)) === skin0 &&
   (skins.at(-1) || "") === skin0, JSON.stringify(skins));
ok("...with nothing saved", !r.writes.includes("atlas-skin"), JSON.stringify(r.writes));
ok("...and not taken for the reader's Prism: no 'rave' line", saidOnly(r, "skin", setup(r, "skin") - 50),
   JSON.stringify(r.said.map(s => s.text)));

// ---- tilt
await goto("?archie=prank:tilt");
const rot0 = await ev(`document.querySelector("main").style.rotate`);
ok("tilt: the page's <main> goes crooked", await until(`!["", "0deg"].includes(document.querySelector("main").style.rotate)`, 20000));
ok("...by under a degree", Math.abs(parseFloat(await ev(`document.querySelector("main").style.rotate`))) < 1);
ok("...and the header does not move with it", await ev(`!document.querySelector("header").style.rotate &&
  !document.querySelector("main").contains(document.querySelector("header"))`));
await done("tilt");
ok("...then its inline style is exactly as it was", await ev(`document.querySelector("main").style.rotate`) === rot0 &&
   await ev(`document.querySelector("main").style.transition`) === "");

// ---- count
await goto("?archie=prank:count");
const count0 = await ev(`document.querySelector("header .sub b").textContent`);
const plus = (parseInt(count0.replace(/[^0-9]/g, ""), 10) + 1).toLocaleString("en-US");
ok("count: the masthead's count goes up by one: him", await until(`document.querySelector("header .sub b").textContent === ${JSON.stringify(plus)}`, 20000),
   `${count0} -> want ${plus}`);
await done("count");
ok("...and back to exactly what it said", await ev(`document.querySelector("header .sub b").textContent`) === count0);

// ---- cursor
await goto("?archie=prank:cursor");
const cur = `[...document.querySelectorAll("style")].find(s => s.textContent.includes("cursor:url("))`;
ok("cursor: his own cursor takes over", await until(`!!${cur}`, 20000));
ok("...with its hotspot at the arrow's tip, where a click would land anyway", await ev(`/\\) 3 2,auto!important/.test(${cur}.textContent)`));
await done("cursor");
ok("...and is gone again", await ev(`!${cur}`));

// ---- his mood
const mood = () => ev(`JSON.parse(sessionStorage.getItem("archie-mood")).v`);
const last = () => ev(`__rec.said.at(-1)?.text || ""`);
const pokeHim = () => ev(`document.querySelector(".archie-poke").click()`);
await goto("", 0);
await sleep(8000);
const m1 = await mood();
ok("mood: ignored, it falls", m1 < 0 && m1 >= -5, String(m1));
await goto("", null);
const m2 = await mood();
ok("...and follows the reader to the next page, where it goes on falling", m2 <= m1 && m2 > m1 - 8, `${m1} then ${m2}`);
await goto("", -23);
ok("...and he says so when it sinks past sulking", await saying("to-sulk", 20000), await last());
await goto("", 0);
const box = await ev(`(() => { const r = document.querySelector(".archie-poke").getBoundingClientRect();
  return {x: r.left + r.width / 2, y: r.top + r.height / 2}; })()`);
await S("Input.dispatchMouseEvent", {type: "mouseMoved", x: box.x, y: box.y});
await sleep(4000);
const hov = await mood();
await S("Input.dispatchMouseEvent", {type: "mouseMoved", x: 5, y: 890});
ok("a pointer resting on him raises it", hov >= 4, String(hov));
await goto("", -60);
await pokeHim();
await sleep(300);
ok("an angry Archie, poked, forgives at once", lines("forgive").includes(await last()), await last());
ok("...all the way: from -60 to 30", await mood() === 30, String(await mood()));
await goto("", 70);
await pokeHim();
await sleep(300);
ok("one who adores the reader says so when poked", lines("love").includes(await last()), await last());
ok("...with hearts", await ev(`document.querySelectorAll(".archie-heart[aria-hidden=true]").length`) === 5);
ok("...a poke is +20", await mood() >= 88 && await mood() <= 90, String(await mood()));
await sleep(2500);
ok("...and the hearts are gone again", await ev(`document.querySelectorAll(".archie-heart").length`) === 0);
await goto("?archie=prank:tilt", -90);
ok("furious, a prank is announced as payback", await saying("revenge"), await last());
await done("tilt");
ok("...and still put back afterwards", await ev(`document.querySelector("main").style.rotate`) === "");

// ---- tired of the reader, and failing to get rid of them
for (const name of ["close", "sign", "shoo", "sulk"]) {
  await goto(`?archie=tired:${name}`, 0);
  const href = await ev(`location.href`);
  ok(`tired, ${name}: announced`, await saying(`tired-${name}`), await last());
  if (name === "close" || name === "sign")
    ok("...its prop drawn, hidden from assistive technology and taking no clicks",
       await until(`(() => { const p = document.querySelector(".archie-prop"); return !!p &&
         p.getAttribute("aria-hidden") === "true" && getComputedStyle(p).pointerEvents === "none"; })()`, 10000));
  if (name === "shoo") ok("...<main> shoved aside", await until(`!!parseFloat(document.querySelector("main").style.translate)`, 10000));
  ok("...and failing, with an excuse", await over(`tired-${name}-after`), await last());
  ok("...leaving the page as it was", await ev(`!document.querySelector(".archie-prop") &&
    document.querySelector("main").style.translate === "" && document.querySelector("main").style.transition === ""`) &&
    await ev(`location.href`) === href);
}
await goto("?archie=tired:close", 90);
await sleep(12000);
r = await rec();
ok("never tired of a reader he adores", !document_has(r, "tired-close") && await ev(`!document.querySelector(".archie-prop")`),
   JSON.stringify(r.said.map(s => s.text)));

// ---- the music going quiet
await goto("", 0);
const DANCE = Object.keys(Function(`return ${SRC.match(/const BEATS = (\{[^}]*\})/)[1]}`)());
const act = () => ev(`document.querySelector(".mhmascot").dataset.act || ""`);
const rigIs = () => ev(`document.querySelector(".mhmascot").dataset.rig || ""`);
const lasersOn = () => ev(`[...document.body.children].some(e => e.tagName === "CANVAS" && e.style.display !== "none")`);
const beats = on => ev(on
  ? `window.__beats = setInterval(() => document.dispatchEvent(new CustomEvent("archie:beat",
       {detail: {strength: 0.9, bpm: 120, at: window.__lastBeat = performance.now()}})), 500)`
  : `clearInterval(window.__beats)`);
await ev(`window.archieMusic = {level: () => 0.6, bass: () => 0.6, bpm: 120, lastBeat: 0};
  document.dispatchEvent(new CustomEvent("archie:music", {detail: {on: true, source: "mic"}}))`);
ok("music mode on, before a beat: the rig hangs, dark", await until(`document.querySelector(".mhmascot").dataset.rig === "dark"`, 4000),
   await rigIs());
await beats(true);
ok("...the beat: he dances", await until(`${JSON.stringify(DANCE)}.includes(document.querySelector(".mhmascot").dataset.act)`, 25000),
   await act());
ok("...and the rig lights up, lasers and all", await until(`document.querySelector(".mhmascot").dataset.rig === "lit"`, 4000) &&
   await lasersOn(), `${await rigIs()} lasers=${await lasersOn()}`);
await sleep(2000);
const dancing = await act();
await beats(false);
const cut = await until(`document.querySelector(".mhmascot").dataset.act === "idle"`, 5000);
const after = await ev(`performance.now() - window.__lastBeat`);
ok("quiet: two seconds on, the dance is cut off where it was", cut && after >= 1900 && after < 3000,
   `${dancing} -> ${await act()} ${Math.round(after)} ms after the last beat`);
ok("...the rig still hung, but dark", await until(`document.querySelector(".mhmascot").dataset.rig === "dark"`, 2000),
   await rigIs());
ok("...and the lasers off", !(await lasersOn()));
const held = [];
for (let i = 0; i < 40; i++) { held.push(`${await act()}/${await rigIs()}`); await sleep(250); }
ok("...and so it stays through the quiet: no dance, no act, nothing lit", held.every(h => h === "idle/dark"),
   [...new Set(held)].join(" "));
await beats(true);
ok("the beat back: he dances again", await until(`${JSON.stringify(DANCE)}.includes(document.querySelector(".mhmascot").dataset.act)`, 25000),
   await act());
ok("...and the rig powers up again", await until(`document.querySelector(".mhmascot").dataset.rig === "lit"`, 4000), await rigIs());
await beats(false);
await ev(`delete window.archieMusic;
  document.dispatchEvent(new CustomEvent("archie:music", {detail: {on: false, source: "mic"}}))`);
ok("music mode off: the rig is hauled away", await until(`document.querySelector(".mhmascot").dataset.rig === "away"`, 6000),
   await rigIs());

// ---- following the reader down the page
// Out of the layer itself, not just gone with it: the layer is detached after every visit and used again.
const cleared = `!document.querySelector(".archie-pole,.archie-lift") && !!document.querySelector(".mhmascot canvas") &&
  !__prop.parentNode`;
for (const by of ["pole", "lift"]) {
  await goto(`?archie=visit:${by}`, 30);
  await ev(`scrollTo(0, 1600)`);
  ok(`${by}: scrolled down, it arrives`, await until(`!!(window.__prop = document.querySelector(".archie-${by}"))`, 20000));
  ok("...in the visit's fixed layer, hidden from assistive technology and taking no clicks", await ev(`(() => {
    const p = document.querySelector(".archie-${by}");
    return p.getAttribute("aria-hidden") === "true" && getComputedStyle(p).pointerEvents === "none" &&
      getComputedStyle(p.parentElement).position === "fixed" && !!p.parentElement.querySelector("canvas") &&
      !!(p.compareDocumentPosition(p.parentElement.querySelector("canvas")) & Node.DOCUMENT_POSITION_FOLLOWING); })()`),
    await ev(`(() => { const p = document.querySelector(".archie-${by}"), l = p.parentElement;
      return [p.getAttribute("aria-hidden"), getComputedStyle(p).pointerEvents, getComputedStyle(l).position,
              [...l.children].map(c => c.tagName + "." + c.className).join(",")].join(" | "); })()`));
  ok("...and he comes down by it, saying so", await saying(by, 20000), await last());
  if (by === "pole")
    ok("...a pole the height of the window, dropped in from the top", await ev(`(() => {
      const r = document.querySelector(".archie-pole").getBoundingClientRect();
      return Math.abs(r.height - innerHeight) < 2 && r.top > -2; })()`));
  else
    ok("...a lift that has counted down to the ground floor", /G$/.test(await ev(`document.querySelector(".archie-floor").textContent`)));
  if (by === "pole") {
    ok("...and, left to it, he goes back up the pole and takes it with him", await until(cleared, 40000));
  } else {
    await ev(`scrollTo(0, 0)`);
    ok("...and scrolling back up mid-visit clears it away at once", await until(cleared, 5000));
  }
  await ev(`scrollTo(0, 0)`);
}

// ---- the tab title while the reader is away
const away = on => ev(`(() => { Object.defineProperty(document, "hidden", {configurable: true, get: () => ${on}});
  document.dispatchEvent(new Event("visibilitychange")); })()`);
await goto();
const title0 = await ev(`document.title`);
await away(true); await sleep(1500); await away(false); await sleep(3500);
ok("title: a glance at another tab changes nothing", await ev(`document.title`) === title0);
await away(true); await sleep(4600);
const gone = await ev(`document.title`);
ok("...four seconds away and the tab calls them back", AWAY.includes(gone), gone);
await away(false); await sleep(200);
ok("...and has the exact title back the moment they return", await ev(`document.title`) === title0);
await goto();
await away(true); await sleep(4600);
await ev(`document.title = "Set by someone else"`);
await away(false); await sleep(200);
ok("...but does not put it back over a title something else set meanwhile", await ev(`document.title`) === "Set by someone else");

// ---- quiet mode stops all of it
await ev(`localStorage.setItem("atlas-byte-quiet", "1")`);
await goto("?archie=prank:lights");
await sleep(9000);
r = await rec();
ok("quiet mode: no prank", !changes(r, "data-theme", 1000).length && !changes(r, "data-skin", 1000).length &&
   r.said.length === 0, JSON.stringify(r));
await away(true); await sleep(4600);
ok("...and no tab title", await ev(`document.title`) === title0);
await away(false);
ok("...and a mood that stays where it was", await mood() === 0, String(await mood()));
await goto("?archie=tired:close", 0);
await sleep(9000);
ok("...and no trying to get rid of anybody", !(await ev(`!!document.querySelector(".archie-prop")`)) &&
   (await rec()).said.length === 0);
await ev(`localStorage.removeItem("atlas-byte-quiet")`);

// ---- following the reader off the index
const docked = `(() => { const d = document.querySelector(".archie-dock"), s = d && d.querySelector(".mhmascot[data-live]");
  return !!s && getComputedStyle(d).position === "fixed" && getComputedStyle(d).pointerEvents === "none" &&
    getComputedStyle(d.querySelector(".archie-poke")).pointerEvents === "auto"; })()`;
const fetched = `performance.getEntriesByType("resource").some(e => e.name.includes("/archie.js"))`;
ok("follow: the index keeps his own URL, release and all", /\/assets\/archie\.js\?v=\w/.test(
   await ev(`sessionStorage.getItem("archie-src") || ""`)), await ev(`sessionStorage.getItem("archie-src")`));
const TOPIC = readdirSync(new URL("../docs/topic/", import.meta.url))[0];
for (const page of ["catalog/", "discover/", "collections/", `topic/${TOPIC}/`, "repo/"]) {
  ok(`...to ${page}, where he is live`, await goto(page, 0));
  ok("...docked in a fixed corner that takes no clicks but his own", await ev(docked));
}
ok("...and says he followed them", await saying("follow"), await last());
await goto("catalog/", -40);
ok("...mad, if they had been ignoring him", await saying("follow-mad"), await last());
await pokeHim();
await sleep(300);
ok("...and a poke there forgives him too", lines("forgive").includes(await last()) && await mood() === 30, await last());
const stranger = async (setup, name) => {
  await S("Page.navigate", {url: ORIGIN + "robots.txt"});
  await until(`location.pathname === "/robots.txt" && document.readyState === "complete"`, 5000);
  await ev(setup);
  await S("Page.navigate", {url: ORIGIN + "catalog/"});
  await until(`document.readyState === "complete"`, 12000);
  await sleep(6000);
  ok(name, !(await ev(fetched)) && !(await ev(`!!document.querySelector(".archie-dock")`)),
     await ev(`performance.getEntriesByType("resource").map(e => e.name).filter(n => /archie/.test(n)).join(" ")`));
};
await stranger(`sessionStorage.clear()`, "not for a reader who never met him in this tab: not even fetched");
await goto("", 0);
await stranger(`localStorage.setItem("atlas-byte-quiet", "1")`, "not in Quiet mode");
await ev(`localStorage.removeItem("atlas-byte-quiet")`);
await stranger(`sessionStorage.setItem("archie-src", "https://example.com/assets/archie.js?v=x")`,
               "not from another origin, whatever sessionStorage says");

ok("no console errors", errors.length === 0, errors.join(" | "));
await browser.close();
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
