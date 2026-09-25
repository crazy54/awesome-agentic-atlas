// Archie's hidden admin panel (`docs/assets/archie-admin.js`) and the command dispatcher it drives
// (`window.archie`, "Commands" in `docs/assets/archie.js`), on the live model under swiftshader's WebGL, as in
// friends-check.mjs.
//
//   node tests/admin-check.mjs <chrome-binary> <origin>
//
// WHAT IS ASSERTED is what the two files' headers promise:
//
//   * hidden by default. On a plain page view there is no panel, the panel's module is never requested, and
//     the trigger is the footer's last thing, faint (a quarter opacity), and still a focusable <button>
//     with an aria-label;
//   * it opens from the trigger, by keyboard (Enter on the focused dot), and from `?archie=admin`;
//   * one button per command: every name `window.archie.list()` gives, and a `friend:<id>` for each id in
//     `archie-friends-data.js`'s ORDER, read here from the file rather than from the page;
//   * each enabled button dispatches its own command, and only it: `window.archie.run` is wrapped and every
//     button pressed. Then the dispatcher is shown to do the thing, not just take the call: a dance and a
//     sit become the act `status()` reports, a flag (`?archie=robot`) goes the same way, a poke answers in
//     his live region, a friend comes and `quiet` sends it home, and a rig cue reaches `window.archieRig`;
//   * a command that cannot run is a disabled button that says why: a cue the live rig lacks, every cue once
//     `window.archieRig` is taken away, and every button under reduced motion, where Archie is a poster;
//   * Escape closes it and focus goes back to the trigger, from either way of opening it.
//
// WHAT IT CANNOT SEE: whether an act looks right (that is dance-check's, prank-check's and friends-check's),
// or what a cue does to the rig: that is rig-check's. The panel's side of a cue is checked against the live
// `window.archieRig` for which cues are enabled, and against a stand-in with the same shape
// ({cues, cue(name)}), installed from here, for what reaches the rig -- then the real one is put back.
import {tmpdir} from "node:os";
import {launch} from "./lib/browser.mjs";

const BIN = process.argv[2], ORIGIN = process.argv[3].replace(/\/?$/, "/");
const TMP = process.env.AAA_TMP || tmpdir();
const {ORDER} = await import(new URL("../docs/assets/archie-friends-data.js", import.meta.url));
process.env.AAA_CHROME_FLAGS = [process.env.AAA_CHROME_FLAGS || "", "--enable-unsafe-swiftshader",
  "--use-angle=swiftshader"].join(" ");
const browser = await launch(BIN, TMP, "admin");

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
  // Excused as friends-check.mjs excuses them: the beacon cannot pass CORS against localhost, and the
  // pictures are on GitHub's hosts, which a runner may not reach.
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
const ev = async expr => {
  const r = await S("Runtime.evaluate", {expression: expr, awaitPromise: true, returnByValue: true});
  if (r.exceptionDetails) throw new Error(expr.slice(0, 60) + " threw: " + (r.exceptionDetails.exception?.description || r.exceptionDetails.text));
  return r.result.value;
};
// A poll that lands while the page is navigating can be answered with a CDP error ("Execution context was
// destroyed", or "Cannot find context"), not a value. That means "not yet", so it is polled again. Only
// those two messages are swallowed, and `ev` itself still throws, so a wrong expression still fails. Added
// after one local run in ten died on an uncaught CDP error whose message was not captured, so this is the
// likely cause, not a proven one.
const until = async (expr, ms) => {
  for (const end = Date.now() + ms; Date.now() < end; await sleep(100))
    if (await ev(expr).catch(e => (/context|navigat/i.test(e.message) ? false : Promise.reject(e)))) return true;
  return false;
};
const goto = async (q = "", live = true) => {
  requested.length = 0;
  await S("Page.navigate", {url: ORIGIN + q});
  await until("document.readyState === 'complete'", 15000);
  return live ? until(`!!document.querySelector(".mhmascot[data-live]")`, 30000) : true;
};
const key = async (k, code, vk) => {
  for (const type of ["keyDown", "keyUp"])
    // A keyDown with `text` is the one that activates a button, as a real Enter's keypress does.
    await S("Input.dispatchKeyEvent", {type, key: k, code, windowsVirtualKeyCode: vk, nativeVirtualKeyCode: vk,
                                       ...(type === "keyDown" && k === "Enter" ? {text: String.fromCharCode(13)} : {})});
};
const PANEL = `!!document.getElementById("archiepanel")`;
const focused = () => ev(`document.activeElement && document.activeElement.id`);

let pass = 0, fail = 0;
const ok = (n, c, extra = "") => { if (c) pass++; else { fail++; console.log("FAIL " + n + (extra ? " -- " + extra : "")); } };

// ---- Hidden by default --------------------------------------------------------------------------------
ok("the model goes live under swiftshader", await goto());
await sleep(1500);
const dot = await ev(`(() => {
  const b = document.getElementById("archieadmin"), f = document.querySelector("footer");
  if (!b) return null;
  const all = [...f.querySelectorAll("*")];
  return {tag: b.tagName, type: b.type, label: b.getAttribute("aria-label"), expanded: b.getAttribute("aria-expanded"),
          inFooter: f.contains(b), last: all.filter(e => !b.contains(e)).at(-1) !== undefined &&
            !all.some(e => e !== b && !b.contains(e) && (b.compareDocumentPosition(e) & Node.DOCUMENT_POSITION_FOLLOWING)),
          opacity: +getComputedStyle(b).opacity, tab: b.tabIndex, disabled: b.disabled,
          w: b.getBoundingClientRect().width};
})()`);
ok("the footer has the trigger", !!dot);
ok("...a <button>, type button", dot && dot.tag === "BUTTON" && dot.type === "button", JSON.stringify(dot));
ok("...with an aria-label, and collapsed", dot && /admin/i.test(dot.label || "") && dot.expanded === "false");
ok("...the footer's last thing", dot && dot.inFooter && dot.last);
ok("...faint: a quarter opacity or less", dot && dot.opacity <= 0.3, dot && String(dot.opacity));
ok("...and in the tab order", dot && dot.tab === 0 && !dot.disabled && dot.w > 0);
ok("no panel on a plain page view", !(await ev(PANEL)));
ok("...and its module was never requested", !requested.some(u => u.includes("archie-admin.js")),
   requested.filter(u => u.includes("archie-admin")).join(" "));
ok("the dispatcher is up with the model", await ev(`!!(window.archie && window.archie.status())`));

// ---- Opens from the trigger, by keyboard ----------------------------------------------------------------
await ev(`document.getElementById("archieadmin").focus()`);
ok("the trigger takes focus", (await focused()) === "archieadmin");
await key("Enter", "Enter", 13);
ok("Enter on the trigger opens the panel", await until(PANEL, 5000));
ok("...which fetched its module only now", requested.some(u => u.includes("archie-admin.js")));
ok("...the trigger says it is expanded", await ev(`document.getElementById("archieadmin").getAttribute("aria-expanded") === "true"`));
ok("...it is a labelled dialog", await ev(`(() => { const p = document.getElementById("archiepanel");
  return p.getAttribute("role") === "dialog" && !!document.getElementById(p.getAttribute("aria-labelledby")); })()`));
ok("...and focus moved into it", await ev(`document.getElementById("archiepanel").contains(document.activeElement)`));

// One button per command
const list = await ev(`window.archie.list()`);
const want = [...list, ...ORDER.map(i => "friend:" + i)];
const have = await ev(`[...document.querySelectorAll("#archiepanel button[data-cmd]")].map(b => b.dataset.cmd)`);
ok("one button for every command and every friend", want.length === have.length && want.every(c => have.includes(c)),
   `missing ${want.filter(c => !have.includes(c)).join(",")} extra ${have.filter(c => !want.includes(c)).join(",")}`);
for (const [what, re, n] of [["dance", /^dance:/, 13], ["prank", /^prank:/, 5], ["friend", /^friend:/, ORDER.length],
                             ["rig cue", /^cue:/, 11]])
  ok(`...including every ${what} (${n})`, have.filter(c => re.test(c)).length === n, String(have.filter(c => re.test(c)).length));
for (const c of ["idle", "watch", "sit", "sleep", "press", "shrug", "walk-off", "show", "chatter", "poke", "quiet"])
  ok(`...and "${c}"`, have.includes(c));

// A command that cannot run says so. The live model's rig is up (this file was written before it landed,
// and asserted every cue disabled; it has been in the suite's page since), so first: the cues it has are
// enabled and a name it lacks is not. Then the rig is taken away, and every cue greys out with a reason.
await sleep(700);
const cueState = () => ev(`[...document.querySelectorAll("#archiepanel button[data-cmd^='cue:']")]
  .map(b => [b.dataset.cmd.slice(4), b.disabled, b.title])`);
const rigHas = await ev(`window.archieRig && Array.isArray(window.archieRig.cues) ? window.archieRig.cues.slice() : null`);
ok("the live model's rig is up, with its cues", Array.isArray(rigHas) && rigHas.length > 0, JSON.stringify(rigHas));
const upCues = await cueState();
ok("...and every cue it has is enabled", upCues.length && upCues.filter(([c]) => (rigHas || []).includes(c)).every(([, d]) => !d),
   JSON.stringify(upCues.filter(([, d]) => d)));
ok("...while a cue it lacks is disabled, saying so", upCues.filter(([c]) => !(rigHas || []).includes(c))
   .every(([, d, t]) => d && /rig/.test(t)), JSON.stringify(upCues.filter(([c]) => !(rigHas || []).includes(c))));
await ev(`window.__rig = window.archieRig; delete window.archieRig`);
await sleep(700);
const cues = (await cueState()).map(([, d, t]) => [d, t]);
ok("with no rig up, every cue button is disabled", cues.length && cues.every(([d]) => d));
ok("...and says why", cues.every(([, t]) => /rig/.test(t)), JSON.stringify(cues[0]));
ok("...and the status line says it too", await ev(`/rig/.test(document.querySelector("#archiepanel .why").textContent)`));
await ev(`window.archieRig = window.__rig`);

// Each button dispatches its own command. The real `run` is swapped for a recorder for this pass, so that
// thirty-odd acts, pranks and friends do not pile into one another, and every button is enabled for it.
await ev(`(() => {
  window.__real = window.archie.run; window.__calls = [];
  window.archie.run = c => { window.__calls.push(c); return true; };
  window.__can = window.archie.can; window.archie.can = () => "";
})()`);
await sleep(700);
const pressed = [];
for (const c of have) {
  await ev(`document.querySelector('#archiepanel button[data-cmd="${c}"]').click()`);
  await sleep(20);
  const calls = await ev(`window.__calls.splice(0)`);
  if (calls.length !== 1 || calls[0] !== c) pressed.push(`${c} -> ${JSON.stringify(calls)}`);
}
ok(`each of the ${have.length} buttons dispatches its own command, once`, pressed.length === 0, pressed.slice(0, 4).join("; "));
await ev(`(() => { window.archie.run = window.__real; window.archie.can = window.__can; })()`);

// ...and the dispatcher does the thing. From the top of the page: focusing the trigger scrolled to the
// footer, and a friend or a prank needs the masthead on screen -- which the panel says, below.
ok("with the masthead off screen, a friend says it cannot come", await until(`(() => {
  const b = document.querySelector('#archiepanel button[data-cmd="friend:quack"]'); return b.disabled && /off screen/.test(b.title); })()`, 2000));
await ev(`scrollTo(0, 0)`);
const press = c => ev(`(async () => { const b = document.querySelector('#archiepanel button[data-cmd="${c}"]');
  await new Promise(r => setTimeout(r, 600)); if (b.disabled) return "disabled: " + b.title; b.click(); return "ok"; })()`);
const actIs = (a, ms = 8000) => until(`(window.archie.status() || {}).act === ${JSON.stringify(a)}`, ms);
ok("the dance button is enabled", (await press("dance:robot")) === "ok");
ok("...and the next act is that dance, cutting the idle short", await actIs("robot"), JSON.stringify(await ev(`window.archie.status()`)));
ok("a queued act waits its turn, then plays", (await press("sit")) === "ok" && await actIs("sit", 25000),
   JSON.stringify(await ev(`window.archie.status()`)));
ok("quiet empties the queue", (await press("quiet")) === "ok" && (await ev(`window.archie.status().queued.length`)) === 0);
const said = await ev(`(document.querySelector(".archie-sr") || {}).textContent || ""`);
ok("a poke is answered, in his live region", (await press("poke")) === "ok" &&
   await until(`((document.querySelector(".archie-sr") || {}).textContent || "") !== ${JSON.stringify(said)}`, 3000));
const fq = await press("friend:quack");
ok("a friend button sends that friend", fq === "ok" && await until(`!!document.querySelector(".archie-pals")`, 8000),
   fq + " " + await ev(`document.querySelector("#archiepanel output").textContent`));
ok("...then the other friends say one is over", await until(`(() => { const b = document.querySelector('#archiepanel button[data-cmd="friend:nib"]');
  return b.disabled && /friend/.test(b.title); })()`, 2000));
await ev(`document.querySelector('#archiepanel button[data-cmd="quiet"]').click()`);
ok("...and quiet sends it home", await until(`!document.querySelector(".archie-pals")`, 4000));
// The rig, through the agreed shape
await ev(`window.__cued = []; window.archieRig = {cues: ["gobo", "all-off"], cue: n => (window.__cued.push(n), true), status: () => ({})}`);
ok("with a rig up, its cues are enabled", (await press("cue:gobo")) === "ok");
ok("...and a cue reaches the rig", await until(`window.__cued.includes("gobo")`, 2000), JSON.stringify(await ev(`window.__cued`)));
ok("...while a cue this rig lacks stays disabled", await ev(`document.querySelector('#archiepanel button[data-cmd="cue:blinder"]').disabled`));
await ev(`document.querySelector('#archiepanel button[data-cmd="quiet"]').click()`);
ok("...and quiet cues it off", await until(`window.__cued.includes("all-off")`, 2000));
await ev(`window.archieRig = window.__rig`);

// Escape closes it, and focus goes back to the trigger
await ev(`document.querySelector('#archiepanel button[data-cmd="dance:floss"]').focus()`);
await key("Escape", "Escape", 27);
ok("Escape closes the panel", await until(`!${PANEL}`, 2000));
ok("...focus is back on the trigger", (await focused()) === "archieadmin", String(await focused()));
ok("...which says it is collapsed", await ev(`document.getElementById("archieadmin").getAttribute("aria-expanded") === "false"`));
await ev(`document.getElementById("archieadmin").click()`);
ok("a click opens it again", await until(PANEL, 3000));
await ev(`document.getElementById("archieadmin").click()`);
ok("...and a second click closes it", await until(`!${PANEL}`, 3000));

// ---- The flags: the same path ---------------------------------------------------------------------------
ok("?archie=admin: the model goes live", await goto("?archie=admin"));
ok("...and the panel opens by itself", await until(PANEL, 5000));
await key("Escape", "Escape", 27);
ok("...Escape closes it, and focus lands on the trigger", await until(`!${PANEL}`, 2000) && (await focused()) === "archieadmin",
   String(await focused()));
ok("?archie=robot goes through the dispatcher", await goto("?archie=robot") && await actIs("robot", 5000),
   JSON.stringify(await ev(`window.archie.status()`)));

// ---- Reduced motion: a poster, and every button says so ----------------------------------------------
await S("Emulation.setEmulatedMedia", {features: [{name: "prefers-reduced-motion", value: "reduce"}]});
await goto("?archie=admin", false);
ok("reduced motion: the model stays a poster", !(await ev(`!!document.querySelector(".mhmascot[data-live]")`)));
ok("...the flag still opens the panel", await until(PANEL, 5000));
await sleep(700);
const rm = await ev(`[...document.querySelectorAll("#archiepanel button[data-cmd]")].map(b => [b.dataset.cmd, b.disabled, b.title])`);
ok("...with every button disabled", rm.length === want.length && rm.every(([, d]) => d), `${rm.length} of ${want.length}; enabled: ` + rm.filter(([, d]) => !d).map(x => x[0]).join(","));
ok("...each saying reduced motion is why", rm.every(([, , t]) => /reduced motion/.test(t)), JSON.stringify(rm[0]));
ok("...and the close button still works", await ev(`document.querySelector("#archiepanel [data-close]").click(), !document.getElementById("archiepanel")`));
ok("...giving focus back to the trigger", (await focused()) === "archieadmin");
await S("Emulation.setEmulatedMedia", {features: []});

ok("no uncaught exception or console error on any visit", errors.length === 0, errors.slice(0, 3).join(" | "));

await browser.close();
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
