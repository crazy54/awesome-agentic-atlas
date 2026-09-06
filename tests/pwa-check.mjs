// Drives chrome-headless-shell over CDP against a real server, so what is asserted is the bytes in
// docs/ and not a re-reading of the generator. No dependencies: Node has a global WebSocket.
//
// WHAT THIS HARNESS CANNOT SEE: anything that is not observable from a page. It cannot tell you the
// `updateViaCache: "none"` in the registration is spelled correctly in the source -- only that the
// registration it got has that value; probe.mjs asserts that on the text of `docs/index.html`. It also
// cannot see anything the *browser it runs* has an opinion about: this Chrome supports navigation preload,
// so the fallback path for browsers that do not is never taken here.
//
// This block used to disclaim one more thing -- that the worker's version hash was derived from the files
// it precaches rather than hardcoded -- and that disclaimer turned out to be the hole. See the VERSION
// section below: it is now recomputed here, because nothing else was checking it and the file it guards is
// the one whose staleness has no self-healing path.
//
//   node tests/pwa-check.mjs <chrome-binary> <origin>
//
// The debug port used to be hardcoded to 9333. It is now whatever the OS gives out -- see
// `lib/browser.mjs`, which also gives every run a profile of its own. That is not housekeeping here: the
// first four assertions below are about a *cold* visit, with no worker registered and no caches, so a
// reused profile would make the second run of this file assert something different from the first.
import {createHash} from "node:crypto";
import {tmpdir} from "node:os";
import {launch} from "./lib/browser.mjs";

const BIN = process.argv[2], ORIGIN = process.argv[3];
if (!BIN || !ORIGIN) {
  console.log("usage: node tests/pwa-check.mjs <chrome-binary> <origin>");
  process.exit(2);
}
const browser = await launch(BIN, process.env.AAA_TMP || tmpdir(), "pwa");

const sleep = ms => new Promise(r => setTimeout(r, ms));
let ws, id = 0;
const waiters = new Map(), events = [];
const send = (method, params = {}, sessionId) => new Promise((res, rej) => {
  const n = ++id;
  waiters.set(n, {res, rej});
  ws.send(JSON.stringify({id: n, method, params, ...(sessionId ? {sessionId} : {})}));
});

ws = new WebSocket(browser.wsUrl);
await new Promise(r => ws.addEventListener("open", r, {once: true}));
ws.addEventListener("message", ev => {
  const m = JSON.parse(ev.data);
  if (m.id && waiters.has(m.id)) {
    const w = waiters.get(m.id); waiters.delete(m.id);
    m.error ? w.rej(new Error(m.method + ": " + m.error.message)) : w.res(m.result);
  } else events.push(m);
});

const {targetId} = await send("Target.createTarget", {url: "about:blank"});
const {sessionId} = await send("Target.attachToTarget", {targetId, flatten: true});
const S = (m, p) => send(m, p, sessionId);
await S("Page.enable"); await S("Runtime.enable"); await S("Log.enable");
await S("Network.enable");

const logs = [];
const evalIn = async (expr) => {
  const r = await S("Runtime.evaluate", {expression: expr, awaitPromise: true, returnByValue: true});
  if (r.exceptionDetails) throw new Error(expr.slice(0, 60) + " threw: " +
    (r.exceptionDetails.exception?.description || r.exceptionDetails.text));
  return r.result.value;
};
const goto = async (url) => {
  await S("Page.navigate", {url});
  for (let i = 0; i < 80; i++) {
    if (await evalIn("document.readyState === 'complete'")) break;
    await sleep(150);
  }
};

let pass = 0, fail = 0;
const ok = (n, c, extra = "") => { c ? pass++ : (fail++, console.log("FAIL " + n + (extra ? " -- " + extra : ""))); };

// -------- cold visit
await goto(ORIGIN);
ok("rows rendered on a cold visit", await evalIn("document.querySelectorAll('#out tbody tr').length") > 100,
   String(await evalIn("document.querySelectorAll('#out tbody tr').length")));
ok("the manifest resolved and is installable-shaped",
   (await S("Page.getAppManifest")).errors.length === 0,
   JSON.stringify((await S("Page.getAppManifest")).errors));
const man = await S("Page.getAppManifest");
ok("manifest scope carries the Pages path prefix", man.parsed?.scope === ORIGIN,
   man.parsed?.scope + " vs " + ORIGIN);
ok("theme-color matches the header's --plane",
   await evalIn(`document.querySelector('meta[name=theme-color]').content ===
     getComputedStyle(document.documentElement).getPropertyValue('--plane').trim()`),
   await evalIn("document.querySelector('meta[name=theme-color]').content"));

// the worker takes a moment; it registers on `load`
let reg = null;
for (let i = 0; i < 60 && !reg; i++) {
  reg = await evalIn(`navigator.serviceWorker.getRegistration().then(r =>
    r ? {scope: r.scope, active: !!r.active, via: r.updateViaCache} : null)`);
  if (!reg?.active) { reg = null; await sleep(250); }
}
ok("a service worker became active", !!reg, JSON.stringify(reg));
ok("its scope is the prefixed site, not the origin root", reg?.scope === ORIGIN, reg?.scope);
ok("it is never read from the HTTP cache", reg?.via === "none", reg?.via);

// -------- second visit: shell precached, data cached
await goto(ORIGIN);
const caches = await evalIn("caches.keys()");
ok("a version-keyed shell cache exists", caches.some(c => /^atlas-shell-/.test(c)), JSON.stringify(caches));
const shellKeys = await evalIn(`(async () => {
  const name = (await caches.keys()).find(c => c.startsWith('atlas-shell-'));
  const c = await caches.open(name);
  return (await c.keys()).map(r => r.url);
})()`);
ok("the shell holds the three precached URLs", shellKeys.length === 3, JSON.stringify(shellKeys));
ok("the root is cached as the directory, which is what a navigation asks for",
   shellKeys.includes(ORIGIN), JSON.stringify(shellKeys));

// -------- the worker's VERSION must describe the bytes actually being served
//
// Every assertion above this line passes when `sw.js` is stale, and this harness did return 17/17 in exactly
// that state. A peer session found it by inspecting a live installed worker, not by running tests.
//
// Why staleness here is worse than it sounds. `VERSION` is a hash of the three precached files, and the
// browser decides whether to install a replacement worker by byte-comparing `sw.js` and nothing else. So
// rewriting `index.html` without re-running `24_pwa.py` leaves the worker byte-identical: no update is
// detected, and every reader who already has it installed keeps being served the *old* shell from the old
// cache indefinitely, while the network serves the new page to everyone else. There is no path out of that
// on its own, because the trigger for self-healing is the one file that did not change. Every other failure
// in this file either heals on the next visit or is visible to the reader; this one is neither.
//
// Recomputed here rather than compared against a recorded number, so this check cannot go stale in the same
// way the thing it watches did. It mirrors `version()` in `24_pwa.py`: for each precached file, in sorted
// order, its *name*, a NUL, its bytes, a NUL, all into one SHA-256, truncated to twelve hex characters.
// Sorting by name rather than by path is the same order only because all three files sit in `docs/`; the
// generator sorts paths, and a precached file in a subdirectory would need this to follow suit.
//
// Fetched over HTTP rather than read off disk, so what is hashed is what a reader is served. That also
// makes this the one assertion here that would catch a *deployed* worker having gone stale, not just a
// working tree.
const PRECACHED = [["index.html", ""], ["manifest.webmanifest", "manifest.webmanifest"],
                   ["pages.css", "pages.css"]];
const digest = createHash("sha256");
for (const [name, path] of [...PRECACHED].sort(([a], [b]) => a < b ? -1 : a > b ? 1 : 0)) {
  const r = await fetch(ORIGIN + path);
  if (!r.ok) throw new Error(`precached file ${name} answered ${r.status}, so VERSION cannot be checked`);
  digest.update(name, "utf8"); digest.update(Buffer.from([0]));
  digest.update(Buffer.from(await r.arrayBuffer())); digest.update(Buffer.from([0]));
}
const wantVersion = digest.digest("hex").slice(0, 12);
const swSrc = await (await fetch(ORIGIN + "sw.js")).text();
const gotVersion = (swSrc.match(/const VERSION = "([0-9a-f]+)"/) || [])[1];
ok("the served worker declares a version at all", !!gotVersion, swSrc.slice(0, 120));
ok("the worker's VERSION is a hash of the bytes it precaches, not of an earlier build",
   gotVersion === wantVersion,
   `sw.js says ${gotVersion}, the three precached files hash to ${wantVersion} ` +
   `-- run: python scripts/24_pwa.py`);
// Ties the recomputation to what the browser did with it. The two could disagree only if the worker built
// its cache name from something other than VERSION, which is the other half of the same coupling.
ok("and the cache the browser actually opened is keyed by that same version",
   caches.includes("atlas-shell-" + wantVersion),
   `${JSON.stringify(caches)} vs atlas-shell-${wantVersion}`);
for (let i = 0; i < 40; i++) {
  if ((await evalIn("caches.keys()")).includes("atlas-data")) break;
  await sleep(200);
}
ok("data.json is cached after the page fetched it",
   (await evalIn("caches.keys()")).includes("atlas-data"));
ok("the beacon and the Open Graph cards are not cached",
   !(await evalIn(`caches.keys().then(ks => Promise.all(ks.map(k => caches.open(k)
     .then(c => c.keys()).then(rs => rs.map(r => r.url))))).then(a => a.flat()
     .some(u => !u.startsWith(location.origin)))`)));

// Checked here rather than at the end, because everything after this line fails a request on purpose --
// the offline phase and the deliberate 404 -- so a check at the end would either be a false alarm or
// would have to whitelist the very failures it is watching for.
const consoleErrs = () => events.filter(e => e.method === "Log.entryAdded" &&
  e.params.entry.level === "error" &&
  // The Cloudflare beacon cannot pass CORS against localhost. It is the page's only third-party request
  // and it is fire-and-forget, so its failure says nothing about this page.
  !/cloudflareinsights|beacon/.test(e.params.entry.text + " " + (e.params.entry.url || "")));
const online = consoleErrs();
ok("no console errors from the page or the worker while online", online.length === 0,
   online.map(e => e.params.entry.text).join(" | "));

// -------- offline
await S("Network.emulateNetworkConditions",
  {offline: true, latency: 0, downloadThroughput: 0, uploadThroughput: 0});
await goto(ORIGIN);
const offlineRows = await evalIn("document.querySelectorAll('#out tbody tr').length");
ok("the atlas still renders with the network off", offlineRows > 100, String(offlineRows));
ok("and it is the real data, not an error page",
   !/could not load/i.test(await evalIn("document.getElementById('count').textContent")),
   await evalIn("document.getElementById('count').textContent"));
await S("Network.emulateNetworkConditions",
  {offline: false, latency: 0, downloadThroughput: -1, uploadThroughput: -1});

// -------- a 404 must never be pinned in the cache
await goto(ORIGIN + "topic/does-not-exist/");
const pageKeys = await evalIn(`caches.has('atlas-pages').then(h => h
  ? caches.open('atlas-pages').then(c => c.keys()).then(ks => ks.map(r => r.url)) : [])`);
ok("a 404 navigation was not cached", !pageKeys.some(u => u.includes("does-not-exist")),
   JSON.stringify(pageKeys));

// Everything logged after the online check is from a request this script broke on purpose. What matters
// is that none of it is an *unhandled* failure -- a rejection escaping the worker, or the page's own
// "could not load data.json" path, both of which surface as something other than a resource error.
const after = consoleErrs().slice(online.length);
ok("the only errors after going offline are the failed requests themselves",
   after.every(e => /Failed to load resource/.test(e.params.entry.text)),
   after.map(e => e.params.entry.text).join(" | "));

console.log(`\n${pass} passed, ${fail} failed`);
ws.close();
await browser.close();
process.exit(fail ? 1 : 0);
