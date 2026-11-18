// The local-AI page, `docs/local/`, driven the way a reader drives it, in a real browser.
//
//   node tests/local-check.mjs <chrome-binary> <origin>
//
// WHAT IT IS FOR. `tests/local_test.py` holds the data, the maths and the generated text. What only a browser
// can see is the flow, so this walks it: a tile, the combobox by keyboard alone (focus, type, arrow, Enter,
// Escape -- with aria-expanded and aria-activedescendant checked at each step), the memory chips, the task
// filter, the numbers toggle and the context and quant controls, the how-to panel's routes and operating
// systems, and the hash that makes a result shareable surviving a reload. Then the non-negotiables from the
// UX plan: no sideways scroll on a 375px phone, no animation under reduced motion, both themes painting the
// page from the site's tokens, and a reader with no script getting the cheat sheet and not a dead picker.
//
// The pure half of the page script (`LOCALUI`) is asserted directly too -- search ranking, the WebGL guess,
// the hash round trip -- because those are the functions whose bugs read as "the page did not understand
// me", and they are cheapest to pin where they are pure.
//
// WHAT IT CANNOT SEE: whether the numbers are right (that is `local_test.py` and, behind it, ds-models'
// method and its stated error); the clipboard (headless Chrome denies it, so only the button's existence is
// checked); a real GPU's WebGL string; and offline, which needs the service worker -- `pwa-check.mjs` owns
// that, and this page needs nothing from the worker beyond being a page it caches.
import {launch} from "./lib/browser.mjs";
import {tmpdir} from "node:os";

const BIN = process.argv[2], ORIGIN = process.argv[3].replace(/\/?$/, "/");
const PAGE = ORIGIN + "local/";
const TMP = process.env.AAA_TMP || tmpdir();
const browser = await launch(BIN, TMP, "local");

const sleep = ms => new Promise(r => setTimeout(r, ms));
let id = 0, pass = 0, fail = 0;
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
  // Excused as spotlight-check.mjs excuses them: the beacon and the site kit cannot pass CORS on localhost.
  else if (m.method === "Log.entryAdded" && m.params.entry.level === "error" &&
           !/cloudflareinsights|beacon|jeremyfhall\.com\/(kit|api\/banners)|githubassets\.com|githubusercontent\.com|github\.com/.test(m.params.entry.text + " " + (m.params.entry.url || "")))
    errors.push(m.params.entry.text);
});
const {targetId} = await send("Target.createTarget", {url: "about:blank"});
const {sessionId} = await send("Target.attachToTarget", {targetId, flatten: true});
const S = (m, p) => send(m, p, sessionId);
await S("Page.enable"); await S("Runtime.enable"); await S("Log.enable");
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
const goto = async (hash = "") => {
  await S("Page.navigate", {url: PAGE + "?r=" + (++id) + hash});
  for (let i = 0; i < 80 && !(await ev("document.readyState === 'complete'")); i++) await sleep(100);
  await sleep(150);
};
const key = async (k, code = k, text) => {
  const vk = {ArrowDown: 40, ArrowUp: 38, Enter: 13, Escape: 27, Tab: 9}[k] || 0;
  await S("Input.dispatchKeyEvent", {type: "keyDown", key: k, code, windowsVirtualKeyCode: vk, ...(text ? {text} : {})});
  await S("Input.dispatchKeyEvent", {type: "keyUp", key: k, code, windowsVirtualKeyCode: vk});
  await sleep(40);
};
const type = async (s) => { await S("Input.insertText", {text: s}); await sleep(60); };
const click = (sel) => ev(`(() => { const el = document.querySelector(${JSON.stringify(sel)}); if (!el) return false; el.click(); return true; })()`);
const hash = () => ev("location.hash");
const live = () => ev("document.getElementById('live').textContent");

// ---- first paint
await goto();
ok("the page loads with the picker, not an error", await ev("!!document.getElementById('s1') && getComputedStyle(document.getElementById('s1')).display !== 'none'"));
ok("six device tiles, as native radios", await ev("document.querySelectorAll('.lxtile input[type=radio][name=kind]').length") === 6);
ok("with nothing picked, the results say where to start", /Pick your computer/.test(await ev("document.getElementById('mach').textContent")));
ok("...and draw no cards", await ev("document.querySelectorAll('.lxcard').length") === 0);
ok("the search waits for a tile", await ev("document.getElementById('pick').hidden"));

// ---- a Mac, by keyboard alone through the combobox
await click("input[name=kind][value=mac]");
ok("a tile opens the search", !(await ev("document.getElementById('pick').hidden")));
ok("...with popular Macs offered as chips", await ev("document.querySelectorAll('#pop [data-dev]').length") >= 3);
ok("...and the choice is in the hash", (await hash()).includes("k=mac"));
await ev("document.getElementById('q').focus()");
await type("air m3");
ok("typing opens the listbox", await ev("document.getElementById('q').getAttribute('aria-expanded')") === "true");
ok("...and finds the MacBook Air (M3) first", await ev("document.querySelector('#qlist li').textContent").then(t => t.startsWith("MacBook Air (M3)")));
await key("ArrowDown");
ok("ArrowDown makes an option active by aria-activedescendant, focus staying in the box",
   await ev("document.activeElement.id === 'q' && document.getElementById('q').getAttribute('aria-activedescendant') === 'qlist-0'"));
ok("...and marks it selected", await ev("document.getElementById('qlist-0').getAttribute('aria-selected')") === "true");
await key("Enter", "Enter", "\r");
ok("Enter picks it", (await hash()).includes("d=macbook-air-m3"));
ok("...closes the listbox", await ev("document.getElementById('qlist').hidden && document.getElementById('q').getAttribute('aria-expanded') === 'false'"));
ok("...and the box names the machine", await ev("document.getElementById('q').value") === "MacBook Air (M3)");
ok("a machine sold in three sizes asks which, with chips", await ev("document.querySelectorAll('#ramo input[name=ram]').length") === 3);
ok("...assuming the smallest until told", await ev("document.querySelector('#ramo input:checked').value") === "8");
await click("#ramo input[value='16']");
ok("a memory chip is in the hash", (await hash()).includes("r=16"));
ok("the machine is explained in one sentence, with its AI budget", /16 GB.*macOS lets AI use about/.test(await ev("document.getElementById('mach').textContent")));
ok("the live region announces the result", /run great/.test(await live()), await live());
ok("there is one pick", await ev("document.querySelectorAll('#best .lxcard').length") === 1);
ok("...that runs great on a 16 GB Mac", await ev("document.querySelector('#best .lxcard').dataset.verdict") === "great");
ok("...with its reason in the reader's units", /Needs [\d.]+ GB(, you have [\d.]+ GB for AI| of your [\d.]+ GB)/.test(await ev("document.querySelector('#best .lxwhy').textContent")),
   await ev("document.querySelector('#best .lxwhy').textContent"));
// The picker and the no-script cheat sheet are one method run in two places (the browser, and Node at build
// time); the 16 GB M3 Air is the cheat sheet's "Mac with 16 GB" row, so the two must name the same three.
const top3 = await ev("[...document.querySelectorAll('[data-verdict=great] h4')].map(h => h.textContent).slice(0, 3).sort().join()");
const row = await ev("[...document.querySelectorAll('.lxcheat tbody tr')].find(r => /Mac with 16 GB/.test(r.textContent)).querySelector('td').textContent.split(', ').sort().join()");
ok("the picker's best three agree with the cheat sheet's row for the same machine", top3 === row, `${top3} vs ${row}`);
ok("...and its speed in words", /Speed: .*(read|typing|instant|slow).*words a second/.test(await ev("document.querySelector('#best .lxwhy').textContent")));
ok("...and the verdict as a word and a shape, not colour alone", await ev("document.querySelector('#best .lxv').textContent") === "●Runs great");
ok("the pick's how-to is open by default", await ev("document.querySelector('#best .lxhow').getAttribute('aria-expanded')") === "true" &&
   !(await ev("document.querySelector('#best .lxhowb').hidden")));
ok("...on macOS, the Mac's own OS", await ev("document.querySelector('#best [data-os][aria-pressed=true]').dataset.os") === "macos");
ok("...with LM Studio, the no-typing route, chosen first", await ev("document.querySelector('#best [data-route][aria-pressed=true]').dataset.route") === "lmstudio");
ok("...and MLX offered, because this is Apple Silicon", await ev("!!document.querySelector('#best [data-route=mlx]')"));
await click("#best [data-route=ollama]");
const cmd = await ev("[...document.querySelectorAll('#best .lxcmd code')].map(c => c.textContent)");
ok("Ollama's steps carry the pick's own tag as a command", cmd.some(c => /^ollama run [a-z0-9.\-]+:[a-z0-9.]+$/.test(c)), JSON.stringify(cmd));
ok("...each with a copy button", await ev("document.querySelectorAll('#best .lxcmd .lxcopy').length") === cmd.length);
ok("...and focus stays on the route the reader chose", await ev("document.activeElement.dataset.route") === "ollama");
ok("the route is remembered in the hash", (await hash()).includes("w=ollama"));
ok("the download size is stated", /first download is about [\d.]+ GB/.test(await ev("document.querySelector('#best .lxdl').textContent")));
ok("bigger models are folded away, with a count", /\d+ bigger models? won.t fit/.test(await ev("document.querySelector('#nofit summary')?.textContent || ''")));
ok("...and each says what would make it fit",
   await ev("[...document.querySelectorAll('#nofit .lxwhy')].every(p => /would fit|too big|would only run/.test(p.textContent))"));

// ---- a shared link reproduces the result
const shared = await hash();
const pickName = await ev("document.querySelector('#best h4').textContent");
await goto(shared);
ok("a reload of the shared link gives the same pick", await ev("document.querySelector('#best h4')?.textContent") === pickName);
ok("...with the same memory chip", await ev("document.querySelector('#ramo input:checked')?.value") === "16");

// ---- tasks, numbers, context, quant
await click("input[name=task][value=code]");
ok("a task is in the hash", (await hash()).includes("t=code"));
ok("with a task, every card shown is good for it",
   await ev("[...document.querySelectorAll('#results .lxcard')].every(c => /Write code/.test(c.querySelector('.lxmeta').textContent))"));
ok("...and the hidden ones are counted, with a way to show them", /\d+ others hidden/.test(await ev("document.getElementById('results').textContent")));
await click("#showall");
ok("Show all lifts the filter", await ev("[...document.querySelectorAll('#results .lxcard')].some(c => !/Write code/.test(c.querySelector('.lxmeta').textContent))"));
ok("numbers are hidden by default", await ev("document.querySelectorAll('.lxnums').length") === 0 && await ev("document.getElementById('expert').hidden"));
await click("#nums");
ok("Show the numbers reveals the breakdown on every card", await ev("document.querySelectorAll('.lxnums').length === document.querySelectorAll('.lxcard').length"));
ok("...and the context control", !(await ev("document.getElementById('expert').hidden")));
ok("...and is pressed, and in the hash", await ev("document.getElementById('nums').getAttribute('aria-pressed')") === "true" && (await hash()).includes("n=1"));
// The same model before and after, by id: a longer context can change which model is the pick.
const kvOf = await ev("document.querySelector('#best .lxcard').dataset.model");
const kv = () => ev(`parseFloat([...document.querySelectorAll('.lxcard[data-model="${kvOf}"] .lxnums dd')][2].textContent)`);
const kv8 = await kv();
await ev("(() => { const s = document.getElementById('ctx'); s.value = '131072'; s.dispatchEvent(new Event('change', {bubbles: true})); })()");
ok("a 128k context needs a bigger context cache than 8k", (await kv()) > kv8 * 8, `${kv8} -> ${await kv()}`);
ok("...and is in the hash", (await hash()).includes("c=131072"));
await ev("(() => { const s = document.getElementById('ctx'); s.value = '8192'; s.dispatchEvent(new Event('change', {bubbles: true})); })()");
const qsel = await ev("(() => { const s = document.querySelector('#best [data-quant]'); const o = [...s.options].map(o => o.value); return o; })()");
if (qsel.length > 1) {
  const pick = qsel[qsel.length - 1];
  await ev(`(() => { const s = document.querySelector('#best [data-quant]'); s.value = ${JSON.stringify(pick)}; s.dispatchEvent(new Event('change', {bubbles: true})); })()`);
  ok("a quant override is fitted", await ev("document.querySelector('[data-quant]:focus')?.value || document.querySelector('.lxcard [data-quant]').value") !== null &&
     await ev(`[...document.querySelectorAll('[data-quant]')].some(s => s.value === ${JSON.stringify(pick)})`));
} else ok("a quant override is fitted (the pick has one quant; nothing to switch)", true);

// ---- a Steam Deck: the how-to knows SteamOS
await goto("#k=handheld&d=steam-deck-oled");
ok("a handheld's how-to defaults to its own OS", await ev("document.querySelector('#best [data-os][aria-pressed=true]')?.dataset.os") === "steamos");
ok("...and starts with Desktop Mode", /Desktop/.test(await ev("document.querySelector('#best .lxhowb ol li')?.textContent || ''")));
ok("...and offers no MLX", !(await ev("!!document.querySelector('#best [data-route=mlx]')")));

// ---- enter it myself: a graphics card and RAM
await goto("#k=gaming");
ok("Gaming PC goes straight to the graphics-card picker", !(await ev("document.getElementById('customb').hidden")) && await ev("document.getElementById('devf').hidden"));
await ev("document.getElementById('gq').focus()");
await type("4070 ti super");
ok("a phrase match outranks a looser one", await ev("document.querySelector('#gqlist li').textContent").then(t => t.startsWith("GeForce RTX 4070 Ti Super")));
await key("Escape");
ok("Escape closes the listbox and keeps focus in the box", await ev("document.getElementById('gqlist').hidden && document.activeElement.id === 'gq'"));
await goto("#k=gaming&g=rtx-3060&v=12&r=32");
ok("a custom rig is explained by its card's memory", /12 GB.*of its own memory/.test(await ev("document.getElementById('mach').textContent")));
ok("...and a model too big for the card but within card + RAM says it is offloaded",
   await ev("[...document.querySelectorAll('.lxcatch')].some(u => /offload/.test(u.textContent))"));
ok("VRAM chips appear for a card sold in two sizes", await ev("document.querySelectorAll('#vramo input').length") === 2);
await goto("#k=desktop&g=none&r=8");
ok("no graphics card and 8 GB still gets an answer", await ev("document.querySelectorAll('.lxcard').length") > 0);

// ---- the pure half
ok("guess: a desktop RTX string finds that card",
   await ev(`LOCALUI.guess("ANGLE (NVIDIA, NVIDIA GeForce RTX 4070 Ti SUPER (0x00002705) Direct3D11 vs_5_0 ps_5_0, D3D11)").map(x => x[1].id).join()`) === "rtx-4070-ti-super");
ok("guess: Apple M4 is ambiguous, and every M4 machine is offered",
   await ev(`LOCALUI.guess("ANGLE (Apple, ANGLE Metal Renderer: Apple M4, Unspecified Version)").length`) >= 2);
ok("guess: an unknown string finds nothing rather than something wrong", await ev(`LOCALUI.guess("Apple GPU").length`) === 0);
ok("the hash round-trips", await ev(`(() => { const h = "#k=mac&d=macbook-air-m3&r=16&t=code,chat&n=1&c=32768&w=ollama&o=linux";
  return LOCALUI.hashOf(LOCALUI.parseHash(h)) === h; })()`));
ok("a hash with junk numbers is ignored, not obeyed", await ev(`LOCALUI.parseHash("#r=lots").r === undefined`));
ok("search folds case, spacing and the word apple", await ev(`LOCALUI.search("APPLE mba m2", ${"window.__d = JSON.parse(document.getElementById('lxdata').textContent)"}.devices, "mac")[0].id`) === "macbook-air-m2");

// ---- the phone, the themes, motion, no script
await size(375, 812, true);
await goto("#k=mac&d=macbook-air-m3&r=16&n=1");
ok("no sideways scroll on a 375px phone, numbers and how-to open",
   await ev("document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1"),
   String(await ev("document.documentElement.scrollWidth")));
ok("tiles are at least 44px tall to tap", await ev("Math.min(...[...document.querySelectorAll('.lxtile')].map(t => t.getBoundingClientRect().height))") >= 44);
await size(1280, 900);
const paint = () => ev("[getComputedStyle(document.querySelector('.lxs')).backgroundColor, getComputedStyle(document.documentElement).getPropertyValue('--plane').trim()]");
await ev("document.documentElement.dataset.theme = 'dark'");
const dark = await paint();
await ev("document.documentElement.dataset.theme = 'light'");
const light = await paint();
ok("the panels repaint between themes", dark[0] !== light[0], `${dark[0]} vs ${light[0]}`);
ok("...from the site's --plane token", dark[1] && light[1] && dark[1] !== light[1]);
await S("Emulation.setEmulatedMedia", {features: [{name: "prefers-reduced-motion", value: "reduce"}]});
await goto("#k=mac&d=macbook-air-m3");
await click("#ramo input[value='24']");
ok("no animation under reduced motion", await ev("document.getAnimations().filter(a => a.effect && a.effect.target && a.effect.target.closest && a.effect.target.closest('main')).length") === 0);
await S("Emulation.setEmulatedMedia", {features: [{name: "forced-colors", value: "active"}]});
await goto("#k=mac&d=macbook-air-m3");
ok("in forced colours a verdict keeps a visible border", await ev("getComputedStyle(document.querySelector('.lxv')).borderTopStyle") === "solid");
await S("Emulation.setEmulatedMedia", {features: []});
await S("Emulation.setScriptExecutionDisabled", {value: true});
await goto();
ok("without script the picker is not shown as a dead control", await ev("getComputedStyle(document.getElementById('s1')).display") === "none");
ok("...the cheat sheet is", await ev("document.querySelectorAll('.lxcheat tbody tr').length") >= 8);
ok("...with an answer in every row", await ev("[...document.querySelectorAll('.lxcheat tbody td:first-of-type')].every(td => td.textContent.trim().length > 1)"));
await S("Emulation.setScriptExecutionDisabled", {value: false});

ok("no uncaught exception or console error on any visit", errors.length === 0, errors.slice(0, 3).join(" | "));

await browser.close();
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
