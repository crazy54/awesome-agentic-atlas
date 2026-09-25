// The homepage's two daily slots -- the spotlight and the line of the day -- in a real browser, on a clock
// this harness sets.
//
//   node tests/spotlight-check.mjs <chrome-binary> <origin>
//
// WHAT IT IS FOR. Both slots are picked by the reader's own calendar date, in the browser, out of a pool
// `scripts/31_home.py` inlines into the page (see the note above `SPOT_POOL_N`). The claim is four claims,
// and each is asserted here rather than read off the generator:
//
//   * a different project on two different days, and the same project all day long -- asserted at five
//     past midnight and five to midnight of one date, across a reload, and on consecutive dates;
//   * "day" is the reader's *local* date. Half past nine at night in Chicago is already tomorrow in UTC,
//     and a picker that used `Date.now() / 864e5` would roll over there. The zone is set with
//     `Emulation.setTimezoneOverride` and the clock with a `Date` replaced before the page's first script;
//   * nothing moves. The page's layout-shift entries must not name the spotlight, the line, or the topic
//     strip below them -- the three things a late swap would move. This is the assertion that found the
//     slot's older defect: the picture used to size its own row, so the day's pick could push the page
//     down 46px when it loaded (see the `.hero .ph img` rule in 31_home.py's HOME_CSS);
//   * a reader without script still gets a spotlight: the `<noscript>` card, which is the build day's.
//     And, the reason that fallback is a `<noscript>` at all, a reader *with* script never downloads that
//     card's picture on a day it is not shown.
//
// The expected pick is computed here from the date string, independently of the page's own arithmetic --
// days since 1970-01-01, modulo the pool -- so a picker that agreed with itself and not with the rule would
// be red. `tests/spotlight_test.py` holds the same rule to the generator's Python copy.
//
// WHAT IT CANNOT SEE: the reader's real clock, a real midnight passing on an open tab (the page does not
// re-pick then, by design -- a card that changed under a reader mid-read would be a layout shift), and
// whether the pool is any good. That last one is the generator's, and `spotlight_test.py` asserts its
// shape.
import {launch} from "./lib/browser.mjs";
import {tmpdir} from "node:os";

const BIN = process.argv[2], ORIGIN = process.argv[3].replace(/\/?$/, "/");
const TMP = process.env.AAA_TMP || tmpdir();
const browser = await launch(BIN, TMP, "spotlight");

const sleep = ms => new Promise(r => setTimeout(r, ms));
let id = 0;
const waiters = new Map(), errors = [], requested = [];
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
  // Excused exactly as dance-check.mjs and pwa-check.mjs excuse them: the beacon cannot pass CORS against
  // localhost, and the pictures are on GitHub's hosts, which a runner may not reach.
  else if (m.method === "Log.entryAdded" && m.params.entry.level === "error" &&
           !/cloudflareinsights|beacon|githubassets\.com|githubusercontent\.com|github\.com/.test(m.params.entry.text + " " + (m.params.entry.url || "")))
    errors.push(m.params.entry.text);
  else if (m.method === "Network.requestWillBeSent") requested.push(m.params.request.url);
});
const {targetId} = await send("Target.createTarget", {url: "about:blank"});
const {sessionId} = await send("Target.attachToTarget", {targetId, flatten: true});
const S = (m, p) => send(m, p, sessionId);
await S("Page.enable"); await S("Runtime.enable"); await S("Log.enable"); await S("Network.enable");
await S("Emulation.setDeviceMetricsOverride", {width: 1440, height: 900, deviceScaleFactor: 1, mobile: false});
await S("Emulation.setTimezoneOverride", {timezoneId: "America/Chicago"});
// Layout shifts from the very first one, including those before any script of ours could observe.
await S("Page.addScriptToEvaluateOnNewDocument", {source: `(() => {
  window.__shifts = [];
  try { new PerformanceObserver(l => { for (const e of l.getEntries()) window.__shifts.push({v: e.value, t: Math.round(e.startTime), rects: (e.sources || []).map(s => [s.previousRect.y, s.previousRect.height, s.currentRect.y, s.currentRect.height].map(Math.round)),
    who: (e.sources || []).map(s => s.node && s.node.nodeType === 1 ? (s.node.closest(".hero") ? "hero" :
      s.node.closest(".daily") ? "daily" : s.node.closest(".bystrip") ? "bystrip" : s.node.className || s.node.tagName) : "?")}); })
    .observe({type: "layout-shift", buffered: true}); } catch (e) {}
})()`});

const ev = async expr => {
  const r = await S("Runtime.evaluate", {expression: expr, awaitPromise: true, returnByValue: true});
  if (r.exceptionDetails) throw new Error(expr.slice(0, 60) + " threw: " + (r.exceptionDetails.exception?.description || r.exceptionDetails.text));
  return r.result.value;
};

// The clock. One script registered per visit and removed after it, so each visit sees exactly one `Date`.
// Only the no-argument constructor and `Date.now()` are pinned: every other use of `Date` on the page --
// parsing a snapshot date, `Date.UTC` -- must behave exactly as it does unpatched.
let clockId = null;
const setClock = async (y, mo, d, h, mi) => {
  if (clockId) await S("Page.removeScriptToEvaluateOnNewDocument", {identifier: clockId});
  ({identifier: clockId} = await S("Page.addScriptToEvaluateOnNewDocument", {source: `(() => {
    const R = Date, T = new R(${y}, ${mo - 1}, ${d}, ${h}, ${mi}).getTime();
    class D extends R { constructor(...a) { a.length ? super(...a) : super(T); } static now() { return T; } }
    window.Date = D;
  })()`}));
};
const goto = async () => {
  requested.length = 0;
  await S("Page.navigate", {url: ORIGIN});
  for (let i = 0; i < 80 && !(await ev("document.readyState === 'complete'")); i++) await sleep(150);
  await sleep(300);
};
const state = () => ev(`(() => {
  const heroes = [...document.querySelectorAll("article.hero")];
  const d = document.querySelector("[data-daily]");
  const ns = document.querySelector("#spotpool ~ noscript");
  return {
    heroes: heroes.length,
    nwo: heroes[0] ? heroes[0].querySelector(".own").textContent : null,
    img: heroes[0] && heroes[0].querySelector("img") ? heroes[0].querySelector("img").src : null,
    visible: heroes[0] ? heroes[0].getBoundingClientRect().height > 200 : false,
    pool: JSON.parse(document.getElementById("spotpool").textContent)
      .map(h => h.match(/<p class="own">([^<]+)<\\/p>/)[1]),
    lines: document.getElementById("dailylines") ? JSON.parse(document.getElementById("dailylines").textContent).lines : [],
    line: d ? d.dataset.line : null, kind: d ? d.dataset.kind : null,
    friend: d ? (d.dataset.friend || null) : null,
    text: d ? d.querySelector("[data-t]").textContent : null,
    kick: d ? d.querySelector("[data-k]").textContent : null,
    linked: d ? d.querySelector("[data-t] a") ? d.querySelector("[data-t] a").getAttribute("href") : null : null,
    fallback: ns ? (ns.textContent.match(/<p class="own">([^<]+)<\\/p>/) || [])[1] : null,
    fallbackImg: ns ? (ns.textContent.match(/<img\\b[^>]*\\bsrc="([^"]+)"/) || [])[1] : null,
    shifts: window.__shifts || [],
  };
})()`);
// The rule, restated from the date string: days since 1970-01-01, modulo the pool.
const dayN = (y, mo, d) => Math.round(Date.UTC(y, mo - 1, d) / 86400000);
const pickOf = (arr, y, mo, d) => arr[((dayN(y, mo, d) % arr.length) + arr.length) % arr.length];

let pass = 0, fail = 0;
const ok = (n, c, extra = "") => { if (c) pass++; else { fail++; console.log("FAIL " + n + (extra ? " -- " + extra : "")); } };

// Eight consecutive dates, straddling a month end, at noon. Consecutive picks must all differ (the pool is
// 31, so eight in a row cannot repeat under the rule) and each must be the rule's.
const days = [[2026, 9, 27], [2026, 9, 28], [2026, 9, 29], [2026, 9, 30], [2026, 10, 1], [2026, 10, 2],
              [2026, 10, 3], [2026, 10, 4]];
const seen = [];
let pool = null, lines = null;
for (const [y, mo, d] of days) {
  await setClock(y, mo, d, 12, 0);
  await goto();
  const s = await state();
  pool = pool || s.pool; lines = lines || s.lines;
  const tag = `${y}-${mo}-${d}`;
  ok(`${tag}: exactly one spotlight card in the document`, s.heroes === 1, String(s.heroes));
  ok(`${tag}: ...drawn at its full size`, s.visible);
  ok(`${tag}: ...and it is the rule's pick for that date`, s.nwo === pickOf(s.pool, y, mo, d), `${s.nwo} vs ${pickOf(s.pool, y, mo, d)}`);
  ok(`${tag}: the line of the day is the rule's pick too`, !s.lines.length || s.line === pickOf(s.lines, y, mo, d).id,
     `${s.line} vs ${s.lines.length && pickOf(s.lines, y, mo, d).id}`);
  if (s.lines.length) {
    const want = pickOf(s.lines, y, mo, d);
    ok(`${tag}: ...its text is that line's, as text`, s.text === want.text, s.text);
    ok(`${tag}: ...its kicker names its kind`, s.kick.length > 0 && s.kind === want.kind, `${s.kick}/${s.kind}`);
    ok(`${tag}: ...it links where the line says, or nowhere`, s.linked === (want.href || null), String(s.linked));
    ok(`${tag}: ...and names a friend exactly when it is a friend line`, s.friend === (want.kind === "friend" ? want.friend : null),
       String(s.friend));
  }
  const bad = s.shifts.filter(e => e.who.some(w => ["hero", "daily", "bystrip"].includes(w)));
  ok(`${tag}: no layout shift moves the spotlight, the line or the strip below them`, bad.length === 0, JSON.stringify(bad));
  // The fallback card's own picture must not have been fetched on a day it is not the one shown -- that is
  // the whole reason it is in a <noscript>. Only askable when the two pictures differ.
  if (s.fallbackImg && s.fallbackImg !== s.img)
    ok(`${tag}: the <noscript> card's picture was not downloaded`, !requested.includes(s.fallbackImg.replace(/&amp;/g, "&")),
       s.fallbackImg);
  seen.push([s.nwo, s.line]);
}
ok("the pool is the 31 the generator promises", pool && pool.length === 31, String(pool && pool.length));
ok("...with no project in it twice", pool && new Set(pool).size === pool.length);
for (let i = 1; i < seen.length; i++) {
  ok(`day ${i} and day ${i + 1}: a different spotlight`, seen[i][0] !== seen[i - 1][0], seen[i][0]);
  if (lines.length > 1) ok(`day ${i} and day ${i + 1}: a different line`, seen[i][1] !== seen[i - 1][1], seen[i][1]);
}
ok("eight consecutive days, eight different projects", new Set(seen.map(x => x[0])).size === seen.length);

// A phone, where the layout is different in the way that matters: one column, the picture on top and sized
// by its own 16/9, and the line of the day's kicker on a line of its own. Three days, the same questions.
await S("Emulation.setDeviceMetricsOverride", {width: 375, height: 800, deviceScaleFactor: 2, mobile: true});
for (const [y, mo, d] of days.slice(0, 3)) {
  await setClock(y, mo, d, 12, 0);
  await goto();
  const s = await state();
  const tag = `375px ${y}-${mo}-${d}`;
  ok(`${tag}: exactly one spotlight card, at its full size`, s.heroes === 1 && s.visible, String(s.heroes));
  ok(`${tag}: the rule's pick`, s.nwo === pickOf(s.pool, y, mo, d));
  const bad = s.shifts.filter(e => e.who.some(w => ["hero", "daily", "bystrip"].includes(w)));
  ok(`${tag}: no layout shift moves the spotlight, the line or the strip`, bad.length === 0, JSON.stringify(bad));
}
await S("Emulation.setDeviceMetricsOverride", {width: 1440, height: 900, deviceScaleFactor: 1, mobile: false});

// Stable within a day: five past midnight, five to midnight, and a reload of the latter.
const within = [];
for (const [h, mi] of [[0, 5], [23, 55], [23, 55]]) {
  await setClock(2026, 10, 2, h, mi);
  await goto();
  within.push(await state());
}
ok("the same project at 00:05 and at 23:55", within[0].nwo === within[1].nwo, `${within[0].nwo} vs ${within[1].nwo}`);
ok("...and across a reload", within[1].nwo === within[2].nwo);
ok("the same line at 00:05 and at 23:55", within[0].line === within[1].line);

// Local, not UTC. 21:30 in Chicago on 2 October is 02:30 on 3 October in UTC; the pick must be the 2nd's.
await setClock(2026, 10, 2, 21, 30);
await goto();
const late = await state();
ok("half past nine at night is still the reader's today, not UTC's tomorrow", late.nwo === pickOf(pool, 2026, 10, 2),
   `${late.nwo} vs the 2nd's ${pickOf(pool, 2026, 10, 2)} and the 3rd's ${pickOf(pool, 2026, 10, 3)}`);
ok("...for the line as well", !lines.length || late.line === pickOf(lines, 2026, 10, 2).id);

// A reader without script: the <noscript> card, which is the build day's, and the slot as drawn.
await S("Emulation.setScriptExecutionDisabled", {value: true});
await goto();
const bare = await ev(`(() => {
  const h = document.querySelectorAll("article.hero"), d = document.querySelector("[data-daily]");
  return {n: h.length, nwo: h[0] ? h[0].querySelector(".own").textContent : null,
          tall: h[0] ? h[0].getBoundingClientRect().height > 200 : false,
          text: d ? d.querySelector("[data-t]").textContent.trim() : null};
})()`);
await S("Emulation.setScriptExecutionDisabled", {value: false});
ok("without script there is still exactly one spotlight card", bare.n === 1, String(bare.n));
ok("...drawn at its full size", bare.tall);
ok("...and it is the build day's, the one in the <noscript>", bare.nwo === late.fallback, `${bare.nwo} vs ${late.fallback}`);
ok("...which is one of the pool", pool.includes(bare.nwo));
ok("without script the line of the day still says something", !lines.length || (bare.text && bare.text.length > 0));

ok("no uncaught exception or console error on any visit", errors.length === 0, errors.slice(0, 3).join(" | "));

await browser.close();
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
