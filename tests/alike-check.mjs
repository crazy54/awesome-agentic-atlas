// Lookalikes, `docs/alike/`, driven the way a reader drives it, in a real browser.
//
//   node tests/alike-check.mjs <chrome-binary> <origin>
//
// WHAT IT IS FOR. `tests/alike-probe.mjs` holds the ranking and the resolver, under node, against the
// committed data; `tests/alike_test.py` holds the stage and the wiring. What only a browser can see is the
// flow, so this walks it: a shared `?repo=` link, a name typed and submitted by keyboard, the "which one did
// you mean" list, the three filters, a description, the back button, and -- with the forges answered by this
// harness through CDP's Fetch domain, never by the real GitHub -- a project the atlas does not hold, a 404, a
// spent rate limit, a network that will not connect and a reader who is offline. Then the non-negotiables:
// every theme paints the page from the site's tokens, a 375px phone does not scroll sideways, focus is
// visible, results are announced, and nothing throws.
//
// WHAT IT CANNOT SEE: the real GitHub and GitLab APIs (deliberately: a test that spent the runner's sixty
// anonymous lookups an hour would redden itself), whether the lookalikes are *good* (that is the probe's,
// and the hand-check table in the pull request), and the service worker's offline copy, which is
// `pwa-check.mjs`'s -- this page needs nothing from the worker beyond being a page it caches.
import {launch} from "./lib/browser.mjs";
import {tmpdir} from "node:os";
import {readFileSync} from "node:fs";

const BIN = process.argv[2], ORIGIN = process.argv[3].replace(/\/?$/, "/");
const PAGE = ORIGIN + "alike/";
const TMP = process.env.AAA_TMP || tmpdir();
const browser = await launch(BIN, TMP, "alike");

const sleep = ms => new Promise(r => setTimeout(r, ms));
let id = 0, pass = 0, fail = 0;
const waiters = new Map(), errors = [];
const ws = new WebSocket(browser.wsUrl);
await new Promise(r => ws.addEventListener("open", r, {once: true}));
const send = (method, params = {}, sid) => new Promise((res, rej) => {
  const n = ++id; waiters.set(n, {res, rej});
  ws.send(JSON.stringify({id: n, method, params, ...(sid ? {sessionId: sid} : {})}));
});

// The forges, as this harness answers them. `MOCK` maps a URL prefix to a response; anything a test has not
// set is a 503, so a test that forgot to mock cannot quietly reach the real API.
let MOCK = {};
const CORS = [{name: "Access-Control-Allow-Origin", value: "*"},
              {name: "Access-Control-Expose-Headers", value: "x-ratelimit-remaining, x-ratelimit-reset, ratelimit-remaining, ratelimit-reset"}];
let SID = null;
ws.addEventListener("message", ev => {
  const m = JSON.parse(ev.data);
  if (m.id && waiters.has(m.id)) {
    const w = waiters.get(m.id); waiters.delete(m.id);
    m.error ? w.rej(new Error(m.error.message)) : w.res(m.result);
  } else if (m.method === "Fetch.requestPaused") {
    const {requestId, request} = m.params;
    const hit = Object.keys(MOCK).find(k => request.url.startsWith(k));
    const r = hit ? MOCK[hit] : {status: 503, body: "unmocked " + request.url};
    if (r.fail) { send("Fetch.failRequest", {requestId, errorReason: "ConnectionRefused"}, SID).catch(() => {}); return; }
    send("Fetch.fulfillRequest", {requestId, responseCode: r.status,
      responseHeaders: [...CORS, {name: "Content-Type", value: r.type || "application/json"}, ...(r.headers || [])],
      body: Buffer.from(typeof r.body === "string" ? r.body : JSON.stringify(r.body)).toString("base64")}, SID).catch(() => {});
  } else if (m.method === "Runtime.exceptionThrown") errors.push(m.params.exceptionDetails.exception?.description || "exception");
  // Excused as local-check.mjs excuses them: the beacon and the site kit cannot pass CORS on localhost. And the
  // forges' own failures, which several tests below cause on purpose and the page reports in words.
  else if (m.method === "Log.entryAdded" && m.params.entry.level === "error" &&
           !/cloudflareinsights|beacon|jeremyfhall\.com\/(kit|api\/banners)|githubassets\.com|githubusercontent\.com|github\.com|gitlab\.com|ERR_CONNECTION_REFUSED|ERR_INTERNET_DISCONNECTED|status of (403|404|429)/.test(m.params.entry.text + " " + (m.params.entry.url || "")))
    errors.push(m.params.entry.text);
});
const {targetId} = await send("Target.createTarget", {url: "about:blank"});
const {sessionId} = await send("Target.attachToTarget", {targetId, flatten: true});
SID = sessionId;
const S = (m, p) => send(m, p, sessionId);
await S("Page.enable"); await S("Runtime.enable"); await S("Log.enable"); await S("Network.enable");
await S("Fetch.enable", {patterns: [{urlPattern: "https://api.github.com/*"}, {urlPattern: "https://raw.githubusercontent.com/*"},
                                    {urlPattern: "https://gitlab.com/*"}]});
const size = (width, height, mobile = false) =>
  S("Emulation.setDeviceMetricsOverride", {width, height, deviceScaleFactor: 1, mobile});
await size(1280, 900);

const ok = (name, cond, detail = "") => {
  if (cond) pass++; else { fail++; console.log(`FAIL ${name}${detail ? `\n  ${detail}` : ""}`); }
};
const ev = async expr => {
  const r = await S("Runtime.evaluate", {expression: expr, awaitPromise: true, returnByValue: true});
  if (r.exceptionDetails) throw new Error(expr.slice(0, 80) + " threw: " + (r.exceptionDetails.exception?.description || r.exceptionDetails.text));
  return r.result.value;
};
const until = async (expr, ms = 20000) => {
  for (let t = 0; t < ms; t += 100) { if (await ev(expr)) return true; await sleep(100); }
  return false;
};
const goto = async (qs = "") => {
  await S("Page.navigate", {url: PAGE + qs});
  await until("document.readyState === 'complete' && !!window.LOOKALIKES");
  await ev("window.LOOKALIKES.ready.then(() => true, () => false)");
  await sleep(150);
};
const key = async (k, code = k, text) => {
  const vk = {ArrowDown: 40, ArrowUp: 38, Enter: 13, Escape: 27, Tab: 9}[k] || 0;
  await S("Input.dispatchKeyEvent", {type: "keyDown", key: k, code, windowsVirtualKeyCode: vk, ...(text ? {text} : {})});
  await S("Input.dispatchKeyEvent", {type: "keyUp", key: k, code, windowsVirtualKeyCode: vk});
  await sleep(60);
};
const type = async (s) => { await S("Input.insertText", {text: s}); await sleep(60); };
const live = () => ev("document.getElementById('lklive').textContent");
const status = () => ev("document.getElementById('lkstatus').hidden ? '' : document.getElementById('lkstatus').textContent");
const cards = () => ev("document.querySelectorAll('#lkout .lkcard').length");
const qs = () => ev("location.search");
const enter = async (sel, text) => {
  await ev(`(() => { const b = document.querySelector(${JSON.stringify(sel)}); b.value = ""; b.focus(); })()`);
  await type(text);
  await key("Enter", "Enter", "\r");
};

// ---- a shared link to a project the atlas holds
await goto("?repo=langfuse/langfuse");
ok("the atlas loads, with the similarity index live", await until("window.LOOKALIKES.ix && !!window.LOOKALIKES.ix.sem"));
ok("?repo= restores the search: the box holds it", await ev("document.getElementById('lkq').value") === "langfuse/langfuse");
ok("...the source is named", /Langfuse/.test(await ev("document.getElementById('lksrch').textContent")));
ok("...and 24 lookalikes are listed", await cards() === 24, String(await cards()));
ok("...in an ordered list under a heading", await ev("!!document.querySelector('#lkout h2 + ol.lklist')"));
ok("each card links to that project's detail page", await ev("[...document.querySelectorAll('.lkcard h3 a')].every(a => /\\/repo\\/[^/]+\\/[^/]+\\/$/.test(a.href))"));
ok("...and every one says why it is here", await ev("[...document.querySelectorAll('.lkcard')].every(c => c.querySelector('.lkwhy span:not(.sr)'))"));
ok("Langfuse's own MCP servers are listed as built around it, not as lookalikes",
   await ev("!document.querySelector('#lkout').textContent.includes('langfuse-mcp') && /langfuse-mcp/.test(document.getElementById('lkaround').textContent)"));
ok("the result is announced in the live region", /24 lookalikes of Langfuse\. First: /.test(await live()), await live());
ok("loading a link does not steal focus", await ev("document.activeElement === document.body || document.activeElement.id === 'lkq' || document.activeElement === null"));

// ---- a name, typed and submitted from the keyboard
await enter("#lkq", "claude code");
ok("Enter resolves a name: 'claude code' is anthropics/claude-code", await until("location.search === '?repo=anthropics/claude-code'"), await qs());
ok("...the source is that project", /claude-code/.test(await ev("document.getElementById('lksrch').textContent")));
ok("...focus moves to the results heading", await ev("document.activeElement && document.activeElement.id === 'lkresh'"));
ok("...which shows a visible focus ring", await ev("getComputedStyle(document.activeElement).outlineStyle") !== "none");

// ---- "which one did you mean"
await enter("#lkq", "memory");
ok("an ambiguous name asks which one", await until("!document.getElementById('lkchoose').hidden"));
ok("...with each choice a button", await ev("document.querySelectorAll('#lkchoose button.lkopt').length") >= 2);
ok("...the question takes focus, so a keyboard reader is there", await ev("document.activeElement.id === 'lkchooseh'"));
ok("...and is announced", /Choose one/.test(await live()), await live());
await key("Tab");
ok("Tab reaches the first choice", await ev("document.activeElement.classList.contains('lkopt')"));
const picked = await ev("document.activeElement.dataset.nwo");
await key("Enter", "Enter", "\r");
ok("Enter on it shows its lookalikes", await until(`location.search === ${JSON.stringify("?repo=" + encodeURIComponent(picked).replace(/%2F/gi, "/"))}`) && await cards() > 0, await qs());
await enter("#lkq", "memory");
await until("!document.getElementById('lkchoose').hidden");
await ev("document.getElementById('lkasq').click()");
ok("...or the words can be searched as a description instead", await until("location.search === '?q=memory'") && await cards() > 0);

// ---- the filters
await goto("?repo=langfuse/langfuse");
await ev("(() => { const s = document.getElementById('lklang'); s.value = 'Python'; s.dispatchEvent(new Event('change')); })()");
ok("the language filter keeps only that language",
   await ev("[...document.querySelectorAll('.lkcard .lkmeta')].every(m => m.textContent.includes('Python'))") && await cards() > 0);
ok("...and the heading says the list is filtered", /filtered/.test(await ev("document.getElementById('lkresh').textContent")));
await ev("(() => { const s = document.getElementById('lklang'); s.value = ''; s.dispatchEvent(new Event('change')); const t = document.getElementById('lkstars'); t.value = '10000'; t.dispatchEvent(new Event('change')); })()");
ok("the stars filter keeps only projects at or over it",
   await ev("[...document.querySelectorAll('.lkcard .lkmeta')].every(m => Number(m.textContent.split(' stars')[0].replace(/,/g, '')) >= 10000)") && await cards() > 0);
await ev("(() => { const t = document.getElementById('lkstars'); t.value = '0'; t.dispatchEvent(new Event('change')); const a = document.getElementById('lkactive'); a.checked = true; a.dispatchEvent(new Event('change')); })()");
ok("'active in the last 6 months' keeps only recent pushes",
   await ev("[...document.querySelectorAll('.lkcard')].every(c => { const r = window.LOOKALIKES.ix.rows[window.LOOKALIKES.ix.by.get(c.querySelector('.lknwo').textContent.toLowerCase())]; return Date.parse(r.pushed) >= Date.now() - 183 * 86400000; })"));
await ev("(() => { const s = document.getElementById('lklang'); s.innerHTML += '<option>Zzz-no-such</option>'; s.value = 'Zzz-no-such'; s.dispatchEvent(new Event('change')); })()");
ok("filters that leave nothing say so, with a way back", await ev("!!document.getElementById('lkreset')") && /Nothing matches/.test(await ev("document.getElementById('lkout').textContent")));
await ev("document.getElementById('lkreset').click()");
ok("...which clears them", await cards() === 24);

// ---- a description, and the back button
await goto("?q=" + encodeURIComponent("a vector database for agent memory"));
ok("?q= restores a description search", await cards() > 0 && /vector database/.test(await ev("document.getElementById('lksrch').textContent")));
await enter("#lkq", "qdrant");
await until("location.search === '?repo=qdrant/qdrant'");
await ev("history.back()");
ok("Back restores the previous search", await until("location.search.startsWith('?q=') && /vector database/.test(document.getElementById('lksrch').textContent)"), await qs());
await ev("document.getElementById('lkdescribe').open = true");
await enter("#lkdq", "tracing and evals for LLM apps");
ok("the describe box searches by what a project does", await until("location.search.startsWith('?q=tracing')") && await cards() > 0);

// ---- links that are not repositories
await enter("#lkq", "https://github.com/anthropics");
ok("a profile link is explained, not searched", await until("document.getElementById('lkstatus').dataset.kind === 'error'") && /not to one repository/.test(await status()), await status());

// ---- not in the atlas: the forge answers
MOCK = {
  "https://api.github.com/repos/someone/tiny-tracer": {status: 200, body: {full_name: "someone/tiny-tracer", name: "tiny-tracer",
    description: "Open-source LLM observability: tracing, evals and prompt management for LLM apps",
    topics: ["llm-observability", "tracing", "evals"], language: "TypeScript", stargazers_count: 12,
    pushed_at: "2026-10-01T00:00:00Z", html_url: "https://github.com/someone/tiny-tracer", default_branch: "main"}},
  "https://raw.githubusercontent.com/someone/tiny-tracer/": {status: 200, type: "text/plain",
    body: "# tiny-tracer\nTrace every LLM call, score it with evals, and compare prompt versions. Self-hosted observability."},
};
await goto("?repo=" + "someone/tiny-tracer");
ok("a project the atlas does not hold is looked up and ranked", await until("document.querySelectorAll('#lkout .lkcard').length > 0"));
ok("...and the page says plainly that it is not in the atlas", /isn.t in the atlas/.test(await ev("document.getElementById('lksrc').textContent")));
ok("...and what it read: description, topics and README", /description, topics and README/.test(await ev("document.getElementById('lksrc').textContent")));
ok("...with observability tools near the top", await ev("[...document.querySelectorAll('.lkcard .lknwo')].slice(0, 12).map(n => n.textContent.toLowerCase()).filter(t => ['langfuse/langfuse','comet-ml/opik','helicone/helicone','arize-ai/phoenix','traceloop/openllmetry','langwatch/langwatch','scale3-labs/langtrace','latitude-dev/latitude-llm'].includes(t)).length") >= 2);

MOCK = {"https://api.github.com/repos/someone/renamed-old": {status: 200, body: {full_name: "langfuse/langfuse", name: "langfuse", description: "", topics: [], html_url: "https://github.com/langfuse/langfuse"}}};
await enter("#lkq", "https://github.com/someone/renamed-old");
ok("a renamed repository the atlas holds under its new name is shown as the atlas's own", await until("location.search === '?repo=langfuse/langfuse'"));

MOCK = {"https://api.github.com/repos/someone/missing": {status: 404, body: {message: "Not Found"}}};
await enter("#lkq", "https://github.com/someone/missing");
ok("a 404 says there is no public repository there", await until("/no public repository/.test(document.getElementById('lkstatus').textContent)"), await status());
ok("...as an alert", await ev("document.getElementById('lkstatus').getAttribute('role')") === "alert");
ok("...and offers to describe it instead", await ev("!!document.getElementById('lktodesc')"));
await ev("document.getElementById('lktodesc').click()");
ok("...which opens the describe box and puts the cursor in it", await ev("document.getElementById('lkdescribe').open && document.activeElement.id === 'lkdq'"));

MOCK = {"https://api.github.com/repos/someone/limited": {status: 403, body: {message: "API rate limit exceeded"},
  headers: [{name: "x-ratelimit-remaining", value: "0"}, {name: "x-ratelimit-reset", value: String(Math.floor(Date.now() / 1000) + 1800)}]}};
await enter("#lkq", "github.com/someone/limited");
ok("a spent rate limit is explained, with when it resets", await until("/60 anonymous lookups an hour/.test(document.getElementById('lkstatus').textContent)") && /resets at/.test(await status()), await status());

MOCK = {"https://api.github.com/repos/someone/unreachable": {fail: true}};
await enter("#lkq", "github.com/someone/unreachable");
ok("a forge that cannot be reached is said so", await until("/couldn.t reach GitHub/.test(document.getElementById('lkstatus').textContent)"), await status());

MOCK = {"https://api.github.com/repos/nobody-zz/words-zz": {status: 404, body: {}}};
await enter("#lkq", "nobody-zz/words-zz");
ok("a bare owner/name GitHub has never heard of is searched as words", await until("location.search.startsWith('?q=nobody-zz')"), await qs());

MOCK = {"https://gitlab.com/api/v4/projects/grp%2Fsub%2Fproj": {status: 200, body: {path_with_namespace: "grp/sub/proj", name: "proj",
  description: "A vector database for embeddings and similarity search", topics: ["vector-database"], star_count: 4,
  last_activity_at: "2026-11-01T00:00:00Z", web_url: "https://gitlab.com/grp/sub/proj", default_branch: "main"}},
  "https://gitlab.com/api/v4/projects/grp%2Fsub%2Fproj/repository/files/": {status: 404, body: {}}};
await enter("#lkq", "https://gitlab.com/grp/sub/proj/-/tree/main");
ok("a GitLab project is looked up through GitLab's API", await until("document.querySelectorAll('#lkout .lkcard').length > 0") && /on GitLab/.test(await ev("document.getElementById('lksrc').textContent")));
ok("...and its link is shareable as a host-qualified nwo", await qs() === "?repo=gitlab.com/grp/sub/proj", await qs());

// Offline: the atlas is in hand, the forge is not.
await S("Network.emulateNetworkConditions", {offline: true, latency: 0, downloadThroughput: -1, uploadThroughput: -1});
MOCK = {"https://api.github.com/repos/someone/offline": {fail: true}};
await enter("#lkq", "github.com/someone/offline");
ok("offline, a lookup outside the atlas says the reader is offline", await until("/You.re offline/.test(document.getElementById('lkstatus').textContent)"), await status());
await enter("#lkq", "langfuse");
ok("...while a project in the atlas still works", await until("document.querySelectorAll('#lkout .lkcard').length === 24"));
await S("Network.emulateNetworkConditions", {offline: false, latency: 0, downloadThroughput: -1, uploadThroughput: -1});
MOCK = {};

// ---- themes: every one paints the page from the site's tokens
const paint = () => ev(`(() => {
  const probe = document.createElement("i"); probe.style.background = "var(--surface)"; probe.style.color = "var(--ink)";
  document.body.append(probe); const want = getComputedStyle(probe); const w = [want.backgroundColor, want.color]; probe.remove();
  const c = document.querySelector(".lkcard"), h = c.querySelector("h3 a");
  return [getComputedStyle(c).backgroundColor, w[0], getComputedStyle(document.querySelector(".lks")).backgroundColor, getComputedStyle(h).color];
})()`);
// The themes are read from `sitewide.THEMES`, the one list every generator draws from, rather than written out
// here. This file was written with three ("dark", "light", "contrast"); #121 cut the site to two and migrates a
// stored "contrast" to dark, and because a merge had left this harness unregistered nobody saw it still asking
// for three. "contrast" is no longer a theme, so it painted as dark and the distinct count came out 2 of 3.
const THEMES = [...(readFileSync(new URL("../scripts/sitewide.py", import.meta.url), "utf8")
  .match(/^THEMES = \(([^)]*)\)/m)?.[1] ?? "").matchAll(/"([a-z]+)"/g)].map(m => m[1]);
ok("the site's themes are read from sitewide.THEMES", THEMES.length >= 2, JSON.stringify(THEMES));
await goto("?repo=langfuse/langfuse");
const seen = {};
for (const theme of THEMES) {
  await ev(`document.documentElement.dataset.theme = ${JSON.stringify(theme)}`);
  await sleep(50);
  const p = await paint();
  seen[theme] = p;
  ok(`${theme}: a card is painted with the theme's --surface`, p[0] === p[1], `${p[0]} vs ${p[1]}`);
}
ok(`the ${THEMES.length} themes paint the page differently`,
   new Set(Object.values(seen).map(p => p[2])).size === THEMES.length, JSON.stringify(seen));
await ev("document.documentElement.dataset.theme = 'dark'");

// ---- a phone
await size(375, 812, true);
await goto("?repo=langfuse/langfuse");
ok("a 375px phone does not scroll sideways", await ev("document.documentElement.scrollWidth <= innerWidth + 1"), String(await ev("document.documentElement.scrollWidth")));
ok("...and the search button is a full-width, 44px target", await ev("(() => { const b = document.querySelector('#lkform .cta').getBoundingClientRect(); return b.height >= 44 && b.width > 300; })()"));
await size(1280, 900);

// ---- keyboard from the top
await goto();
ok("with nothing asked, the page shows no results and no error", await cards() === 0 && !(await status()));
await ev("document.activeElement.blur()");
let reached = false;
for (let i = 0; i < 40 && !reached; i++) { await key("Tab"); reached = await ev("document.activeElement.id === 'lkq'"); }
ok("the input is reachable by Tab", reached);
ok("...and shows a focus ring there", await ev("getComputedStyle(document.activeElement).outlineStyle") !== "none");
await ev("document.querySelector('a[data-ex][href^=\"?q=\"]').click()");
ok("an example chip runs its search without a reload", await until("document.querySelectorAll('#lkout .lkcard').length > 0") && (await qs()).startsWith("?q="));

// ---- no script
await S("Emulation.setScriptExecutionDisabled", {value: true});
await S("Page.navigate", {url: PAGE}); await sleep(800);
ok("without script the search is not shown as a dead control", await ev("getComputedStyle(document.querySelector('.lks')).display") === "none");
await S("Emulation.setScriptExecutionDisabled", {value: false});

ok("no uncaught exception or console error on any visit", errors.length === 0, errors.slice(0, 3).join(" | "));
await browser.close();
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
