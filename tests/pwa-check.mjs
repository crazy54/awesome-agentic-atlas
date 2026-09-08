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
import {execFileSync} from "node:child_process";
import {createHash} from "node:crypto";
import {tmpdir} from "node:os";
import {fileURLToPath} from "node:url";
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
// `extra` may be a function, which is called only when the assertion has already failed. Most callers pass
// a string they had anyway; one needs to run a subprocess to explain itself, and should not run it 20 times
// per green run. It cannot change the verdict either way -- `c` is evaluated by the caller, before this.
const ok = (n, c, extra = "") => {
  if (c) { pass++; return; }
  fail++;
  const d = typeof extra === "function" ? extra() : extra;
  console.log("FAIL " + n + (d ? " -- " + d : ""));
};

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
// Fetched over HTTP rather than read off disk, so this is the one assertion here that would also catch a
// *deployed* worker having gone stale rather than only a working tree.
//
// Newlines are normalised, for the same reason the generator normalises them and not as a convenience.
// `core.autocrlf` is true with no `.gitattributes`, so a Windows checkout holds CRLF while the committed
// blob -- and therefore what Pages serves -- is LF. Hashing what this server hands over would make the
// assertion pass on Linux and fail on Windows for byte-identical content, which is the same
// hash-depends-on-the-OS bug the generator was just fixed for. Normalising is what makes the local run
// compute the production answer; it is worth being clear that the bytes on this machine are genuinely not
// the bytes a reader gets, and that this line is what bridges the two.
const lf = (buf) => {
  const out = Buffer.allocUnsafe(buf.length);
  let n = 0;
  for (let i = 0; i < buf.length; i++) {
    if (buf[i] === 0x0d && buf[i + 1] === 0x0a) continue;
    out[n++] = buf[i];
  }
  return out.subarray(0, n);
};
const PRECACHED = [["index.html", ""], ["manifest.webmanifest", "manifest.webmanifest"],
                   ["pages.css", "pages.css"]];
const digest = createHash("sha256");
for (const [name, path] of [...PRECACHED].sort(([a], [b]) => a < b ? -1 : a > b ? 1 : 0)) {
  const r = await fetch(ORIGIN + path);
  if (!r.ok) throw new Error(`precached file ${name} answered ${r.status}, so VERSION cannot be checked`);
  digest.update(name, "utf8"); digest.update(Buffer.from([0]));
  digest.update(lf(Buffer.from(await r.arrayBuffer()))); digest.update(Buffer.from([0]));
}
const wantVersion = digest.digest("hex").slice(0, 12);
const swSrc = await (await fetch(ORIGIN + "sw.js")).text();
const gotVersion = (swSrc.match(/const VERSION = "([0-9a-f]+)"/) || [])[1];
ok("the served worker declares a version at all", !!gotVersion, swSrc.slice(0, 120));

// A mismatch has two causes that want opposite responses, and the hash alone cannot tell them apart:
//
//   * a committed worker that describes an earlier build -- the production bug, fix and commit it
//   * a working tree mid-edit, where `index.html` has been rewritten and `24_pwa.py` not yet run --
//     expected, and cleared by finishing the build
//
// So the failure message names which one it is. This adds context to a failure and cannot suppress one:
// the assertion is the plain hash comparison above it, evaluated before `why()` is ever called. A harness
// that can decline to assert is how `pagemin_test.py` silently skipped 7 of 49 checks while exiting 0.
//
// Consulted lazily, so a passing run never shells out to git. And scoped honestly: git is asked about
// *this repository's* `docs/`, while the assertion is about whatever `ORIGIN` serves. Those are the same
// tree under `run.mjs` and deliberately not the same under a scratch fixture, which is why the wording
// below attributes the answer to git rather than stating it as fact about the served bytes.
const why = () => {
  const files = ["docs/index.html", "docs/pages.css", "docs/manifest.webmanifest", "docs/sw.js"];
  let out;
  try {
    out = execFileSync("git", ["status", "--porcelain", "--", ...files],
                       {cwd: fileURLToPath(new URL("..", import.meta.url)), encoding: "utf8"});
  } catch (e) {
    return `git could not be consulted about the tree (${e.message.split("\n")[0]})`;
  }
  const dirty = out.split("\n").filter(Boolean).map(l => l.slice(3).trim().replace(/^"|"$/g, ""));
  const shell = dirty.filter(f => f !== "docs/sw.js");
  if (!dirty.length) {
    return "git reports every precached file and docs/sw.js committed and clean, so this is a stale " +
           "worker in the repository rather than an unfinished edit -- readers with it installed are " +
           "pinned to the old shell";
  }
  if (shell.length && !dirty.includes("docs/sw.js")) {
    return `git reports ${shell.join(", ")} modified and docs/sw.js not, so the page was rewritten and ` +
           `24_pwa.py has not run since -- expected mid-edit, and a bug the moment it is committed`;
  }
  return `git reports ${dirty.join(", ")} modified, so a build may be in flight; a run taken during ` +
         `one is not evidence either way -- finish it and re-run`;
};
ok("the worker's VERSION is a hash of the bytes it precaches, not of an earlier build",
   gotVersion === wantVersion,
   () => `sw.js says ${gotVersion}, the three precached files hash to ${wantVersion} ` +
         `-- run: python scripts/24_pwa.py\n         ${why()}`);
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
//
// On both sessions, and that is the whole of it. `Network.emulateNetworkConditions` applies to the target it
// is sent to, and the target that fetches `data.json` is not the page -- it is the service worker, which is
// a target of its own with a network context of its own. Sent only to the page, as it was until this line
// was written, the page's own direct requests fail while the worker carries on fetching from the live
// server, re-caching what it gets and answering every request as if nothing had happened: the atlas renders
// offline, the rows are real, and the cache-fallback branch in `data()` has never once run. Both assertions
// below passed in that state, and so did the freshness section after them until it was made to disagree
// with itself on purpose and would not.
//
// Re-applied before each offline navigation rather than set once, because Chrome terminates an idle worker
// after about thirty seconds and the replacement starts with no emulation on it.
//
// ONE SESSION PER TARGET, and the map is the whole reason this works on a browser other than the one it was
// written against. `Target.attachToTarget` does not return an existing session for an already-attached
// target: it opens a new one, every time, with its own network state. This helper is called seven times, so
// the version of it that attached on each call left seven live sessions on the worker, six of them still
// saying `offline: true` after the seventh said false. Whether that matters is then a question about how the
// browser merges the sessions' conditions, which is a question no test should be asking: `chrome-headless-shell`
// 1223 takes the last write and passed, and Chromium 152 on `ubuntu-latest` does not and failed six
// assertions -- the first being "back online, the stamp is the network's data", with the five after it
// downstream of a worker that was never let back online.
//
// So the session is created once per target id and reused, which makes going back online the exact inverse
// of going offline instead of an eighth opinion about it. Entries for targets that have since been recycled
// are dropped rather than written to, because a dead session is a CDP error and not a no-op.
let swSession = null;
const swSessions = new Map();
const net = async (offline) => {
  const p = {offline, latency: 0, downloadThroughput: offline ? 0 : -1, uploadThroughput: offline ? 0 : -1};
  await S("Network.emulateNetworkConditions", p);
  const live = new Set();
  for (const t of (await send("Target.getTargets")).targetInfos) {
    if (t.type !== "service_worker") continue;
    live.add(t.targetId);
    let sid = swSessions.get(t.targetId);
    if (!sid) {
      ({sessionId: sid} = await send("Target.attachToTarget", {targetId: t.targetId, flatten: true}));
      swSessions.set(t.targetId, sid);
      await send("Network.enable", {}, sid);
    }
    swSession = sid;
    await send("Network.emulateNetworkConditions", p, sid);
  }
  for (const id of [...swSessions.keys()]) if (!live.has(id)) swSessions.delete(id);
};
// Whether the worker is reachable at all, asked of the page rather than of the emulation settings. Used to
// qualify the assertion below: "the stamp still says offline" and "the network is still off" are different
// failures, and the second one is this file's fault rather than the site's.
const reachesNetwork = async () => evalIn(
  `fetch(new URL('data.json?net-probe=' + Date.now(), location.href).href)
     .then(r => 'HTTP ' + r.status + (r.headers.get('x-atlas-cached') ? ' from the cache' : ' from the network'))
     .catch(e => 'unreachable: ' + e.message)`);
await net(true);
ok("the worker is a target of its own, and was taken offline as well as the page", !!swSession,
   "no service_worker target to attach to -- an offline test that only stops the page is not one");
await goto(ORIGIN);
const offlineRows = await evalIn("document.querySelectorAll('#out tbody tr').length");
ok("the atlas still renders with the network off", offlineRows > 100, String(offlineRows));
ok("and it is the real data, not an error page",
   !/could not load/i.test(await evalIn("document.getElementById('count').textContent")),
   await evalIn("document.getElementById('count').textContent"));

// -------- the freshness stamp must describe the rows on screen, not the shell they arrived in (JFH-207)
//
// The two halves of this page live in two caches. `atlas-shell-<version>` holds the document, `atlas-data`
// holds `data.json`, and they are filled by different requests that can succeed on different days -- so
// the pair a reader gets offline is not necessarily a pair that was ever deployed together. Every
// assertion above this line is satisfied by the *wrong* pairing: the atlas renders, the rows are real, and
// the header says the data is from today because the header's date was baked into the document.
//
// Which makes this the one thing in the file that cannot be observed by looking: nothing distinguishes a
// correct stamp from a stale one unless the two caches are made to disagree on purpose. So they are. The
// cached body is rewritten with dates that are unmistakably not the document's, still offline so that
// network-first cannot overwrite it on the way back in, and the header is then read for whose date it
// chose. `generated` and `snapshot` are given *different* old dates rather than one old date, because
// otherwise an implementation that read either one would pass and only the ladder's order is in question.
//
// The document's own stamp is taken from the served HTML rather than from a page variable: Node's `fetch`
// is not subject to the browser's emulated offline, and the bytes Pages would serve are the honest source
// for "what the page claims on its own".
const docStamp = (await (await fetch(ORIGIN)).text())
  .match(/id="snap"[^>]*>snapshot\s+(\d{4}-\d{2}-\d{2})/)?.[1];
ok("the served page has a snapshot date baked into it to be wrong with", !!docStamp, String(docStamp));

// Doctors the cached `data.json` in place. Returns "ok", or a reason, so a cache that was not there to
// doctor reports itself instead of quietly making the assertions below vacuous.
const recache = (patch) => evalIn(`(async () => {
  const url = new URL('data.json', location.href).href;
  const c = await caches.open('atlas-data');
  const hit = await c.match(url);
  if (!hit) return 'nothing cached under ' + url;
  const body = await hit.json();
  ${patch}
  await c.put(url, new Response(JSON.stringify(body),
    {headers: {'content-type': 'application/json'}}));
  return 'ok';
})()`);

// `goto` waits for readyState, which does not wait for the page's own `fetch("data.json")`, and the stamp
// is rendered twice -- once from the document before the data lands and once from the data. Polling for
// the rows is polling for the second one; reading too early would read the value this is meant to catch
// and pass for the wrong reason.
const stampAfterData = async () => {
  await net(true);
  await goto(ORIGIN);
  for (let i = 0; i < 60; i++) {
    if (await evalIn("document.querySelectorAll('#out tbody tr').length") > 100) break;
    await sleep(100);
  }
  return evalIn("document.getElementById('snap').textContent.replace(/\\s+/g, ' ').trim()");
};

const doctored = await recache("body.generated = '2025-01-15T04:05:00Z'; body.snapshot = '2025-01-16';");
ok("the cached data.json could be given a known old stamp", doctored === "ok", String(doctored));
const staleStamp = await stampAfterData();
ok("offline, the stamp is the cached data's own date and not the document's",
   staleStamp.includes("2025-01-15") && !staleStamp.includes(docStamp), staleStamp);
ok("and it prefers `generated` over `snapshot` when both are there",
   !staleStamp.includes("2025-01-16"), staleStamp);
ok("and it says where the rows came from, in the wording the reader needs",
   /offline, showing data from 2025-01-15/.test(staleStamp), staleStamp);
// The fortnight marker is the display policy and is not what this ticket changed; it has to still fire,
// and now off the data's date rather than the document's. 2025 is a long way past fourteen days.
ok("and the fortnight marker still fires, now off the data's date",
   /days old/.test(staleStamp), staleStamp);

// Degrading, rung by rung. A `data.json` cached before `generated` existed still carries `snapshot`, which
// is the same fact at a day's resolution, so the ladder's second rung is what makes this fix work for
// bodies that are already in readers' caches rather than only for ones built after it.
ok("a body with no `generated` falls back to its own `snapshot`",
   await recache("delete body.generated; body.snapshot = '2025-01-17';") === "ok" &&
   (await stampAfterData()).includes("2025-01-17"));
// And the last rung. With nothing in the body to read, the document's constant is all there is -- and the
// failure to avoid is not a wrong date but "undefined", "NaN days old" or an Invalid Date.
const noStamp = await recache("delete body.generated; delete body.snapshot;") === "ok" &&
  await stampAfterData();
ok("a body with neither falls back to the document, not to undefined",
   noStamp.includes(docStamp) && !/undefined|NaN|Invalid/.test(noStamp), noStamp);

await net(false);
// And back. The header the wording hangs on means "the network did not answer", not "there is a copy in the
// cache" -- the worker fills that cache on every successful fetch, so a header set on the way *in* would
// have every online reader told they were offline. The doctored body is still in the cache here and is
// replaced by the fetch that succeeds, so this also checks the network still wins when it answers.
await goto(ORIGIN);
for (let i = 0; i < 60; i++) {
  if (await evalIn("document.querySelectorAll('#out tbody tr').length") > 100) break;
  await sleep(100);
}
const backOnline = await evalIn("document.getElementById('snap').textContent.replace(/\\s+/g, ' ').trim()");
// Not compared against `docStamp` outright: past a fortnight the age is appended, and a checkout that has
// been sitting for three weeks is a stale copy of the site rather than a broken one. The shape, the absence
// of the offline wording and the absence of the doctored date are the three things being claimed.
//
// The reachability probe is in the failure message and not in an assertion of its own, because it is a fact
// about this harness rather than about the site. When this went red on `ubuntu-latest` the stamp read
// "offline, showing data from <the document's own date>" -- which is what the page renders when the body it
// got has had both dates deleted, i.e. the doctored copy out of the cache, i.e. a worker that never came
// back online. Six failures, one cause, and half an hour to work out which. Saying so in the message costs
// one CDP round trip on the failing path only.
const backOnlineOk = /^snapshot \d{4}-\d{2}-\d{2}/.test(backOnline) && !backOnline.includes("2025-01");
ok("back online, the stamp is the network's data and says nothing about the cache", backOnlineOk,
   backOnlineOk ? backOnline
                : `${backOnline} -- and the page's own fetch right now says ${await reachesNetwork()}`);

// -------- docs/live.json, on a real detail page (JFH-222)
//
// The worker used to route the data path by one exact filename, `/data.json`. The 1,294 detail pages now
// fetch `live.json` instead -- three columns of the same dataset, 21.8 KB gzipped against 162.5 KB -- and
// a filename this worker does not recognise gets no branch at all: no `atlas-data` entry, no
// `x-atlas-cached` marking, and a detail page that silently loses its star count the moment a reader is
// offline. Nothing above this line would notice, because every assertion above is about the index page and
// the index page does not fetch this file.
//
// The page is taken from `sitemap-repos.xml` rather than hardcoded, because a hardcoded `nwo` is a repo
// that will one day leave the source lists and turn this section into a 404 that passes.
const repoLocs = [...(await (await fetch(ORIGIN + "sitemap-repos.xml")).text())
  .matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => new URL(m[1]).pathname.split("/").filter(Boolean));
const detailPath = repoLocs.filter(p => p.length === 4 && p[1] === "repo")
  .map(p => p.slice(1).join("/") + "/")[0];
ok("the repo sitemap names a detail page to visit", !!detailPath, JSON.stringify(repoLocs[0]));
const detailUrl = ORIGIN + detailPath;

// The three spans start hidden and `show()` sets `class="live on"`, so waiting for the class is waiting
// for the fetch rather than for the document -- which is the whole point of the file being fetched.
const liveSpans = () => evalIn(`JSON.stringify(["stars", "pushed", "snap"].map(id => {
  const el = document.getElementById(id);
  return el ? el.className + "|" + el.textContent.trim() : "missing";
}))`);
const waitLive = async () => {
  for (let i = 0; i < 60; i++) {
    const s = JSON.parse(await liveSpans());
    if (s[0].startsWith("live on")) return s;
    await sleep(100);
  }
  return JSON.parse(await liveSpans());
};
await goto(detailUrl);
const onlineSpans = await waitLive();
ok("a detail page fills in its star count from live.json after paint",
   /^live on\|(\d[\d,]*\s+stars|No stars recorded)$/.test(onlineSpans[0]), JSON.stringify(onlineSpans));
ok("and the snapshot that qualifies it, so the two figures are not presented as live",
   /^live on\|snapshot \d{4}-\d{2}-\d{2}$/.test(onlineSpans[2]), JSON.stringify(onlineSpans));
const dataKeys = async () => evalIn(`caches.has('atlas-data').then(h => h
  ? caches.open('atlas-data').then(c => c.keys()).then(ks => ks.map(r => new URL(r.url).pathname)) : [])`);
for (let i = 0; i < 40; i++) {
  if ((await dataKeys()).some(u => u.endsWith("/live.json"))) break;
  await sleep(200);
}
const keysOnline = await dataKeys();
ok("live.json is in atlas-data after the page fetched it", keysOnline.some(u => u.endsWith("/live.json")),
   JSON.stringify(keysOnline));
// Both, and in the one cache. The two files are one list in `24_pwa.py` precisely so that they cannot get
// different policies by accident, and `atlas-data` is unversioned and never swept, so this is the pair a
// reader keeps.
ok("and so is data.json, so the two are one policy and not two",
   keysOnline.some(u => u.endsWith("/data.json")), JSON.stringify(keysOnline));

// Offline, and the assertion is about the file rather than about the rendered page -- which is not a
// hedge, it is the honest boundary, and finding it was worth more than the assertion.
//
// WHAT THIS SECTION CANNOT SEE, and nor can any assertion, because it is not true: that a detail page
// works offline. It does not, and it did not before JFH-222 either. `docs/repo/detail.js` and
// `docs/repo/detail.css` are neither precached by `install` nor matched by `PRECACHED` in the fetch
// listener, so the worker declines them and the browser fetches them from the network. Measured here,
// with the network off and the document served from `atlas-pages`: `typeof show` is `"undefined"`, so the
// script never arrived, and the three spans keep their initial `class="live"`. Nothing the sidecar does
// can change that -- the reader is missing the code that reads it, not the data. On the published site
// Pages' `max-age=600` papers over the first ten minutes and no longer.
//
// So what is asserted is the routing this ticket actually changed, which is a fact about the worker and is
// checkable: the file is in the cache the reader keeps, the cache answers with the network off, and the
// response is marked. Caching `detail.css` and `detail.js` is a separate change to `24_pwa.py` -- and not
// obviously the right one, since precaching them would charge every index-page reader for two files only
// detail pages use.
await net(true);
await goto(detailUrl);
const scriptOffline = await evalIn("typeof show");
// The marking, not just the body. A cached `data.json` is told apart from a fresh one by this header, and
// the index page's freshness stamp is built on it; a sidecar served from cache with no header would be a
// cached body that nothing can tell is cached. `dataset.root` rather than a hand-counted `../../`, because
// that attribute is what `detail.js` itself resolves against and a detail page is three levels deep.
const marked = await evalIn(`fetch(new URL((document.documentElement.dataset.root || '') + 'live.json', location.href).href)
  .then(r => r.headers.get('x-atlas-cached') + '/' + r.status).catch(e => 'threw: ' + e.message)`);
ok("offline, live.json is answered from atlas-data and marked x-atlas-cached", marked === "1/200",
   `${marked} -- and for the record typeof show was ${scriptOffline}, so detail.js itself is uncached`);
const keysOffline = await dataKeys();
ok("and both data files are still in that cache, which activate never sweeps",
   ["/data.json", "/live.json"].every(n => keysOffline.some(u => u.endsWith(n))),
   JSON.stringify(keysOffline));
await net(false);

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
