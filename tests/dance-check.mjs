// "Dance with me", driven for real: Chrome's fake microphone plays a WAV this file writes -- a kick on every
// beat at 120 BPM, a hi-hat on every off-beat, then silence -- and the page's own beat detector listens to
// it. So what is asserted is the detector against a known tempo, not the detector against itself.
//
// WHAT THIS HARNESS CANNOT SEE: the "On this computer" path past its offer. A shared tab's audio needs a
// picker a headless browser does not draw, so that choice is asserted to be offered and nothing more; the
// analysis behind it is the same function the microphone feeds. Nor what the 3D model does with the beats:
// that is `archie.js`. Whether it goes live depends on this Chrome's WebGL -- it did in the suite and not
// alone -- so WebGL2 is stubbed out here, the slot is always the poster, and its hop is what is checked;
// the model's arm is `data-live` set by hand, under which the poster must not hop too.
//
//   node tests/dance-check.mjs <chrome-binary> <origin>
import {writeFileSync, mkdtempSync} from "node:fs";
import {tmpdir} from "node:os";
import {join} from "node:path";
import {launch} from "./lib/browser.mjs";

const BIN = process.argv[2], ORIGIN = process.argv[3].replace(/\/?$/, "/");
const TMP = process.env.AAA_TMP || tmpdir();

// ---- The song: 16-bit mono PCM. 12 beats at 120 BPM, then 3 s of a quiet room's hiss, so a gap of about
// 3 s between two detected beats is the silence being heard as silence and not as a hundred tiny onsets.
// The hats are loud and in triplets, three to the beat: the first detector here, which weighed every
// frequency bin alike, heard them and not the kick, and counted 171. The per-band detector that replaced
// it does not need its 4:1 bass weighting to pass this song; nothing here tests that weighting, nor the
// level gate, the recent-peak floor, peak picking or the tempo's fold into 70-180. Chrome loops the file.
const RATE = 48000, BPM = 120, BEAT = 60 / BPM, BEATS = 12, QUIET = 3;
const N = Math.round((BEATS * BEAT + QUIET) * RATE);
const pcm = new Float32Array(N);
let seed = 7;
const noise = () => ((seed = (seed * 16807) % 2147483647) / 2147483647) * 2 - 1;
for (let b = 0; b < BEATS; b++) {
  const at = Math.round(b * BEAT * RATE);
  for (let i = 0; i < 0.16 * RATE; i++) {         // kick: a pitch drop from 120 to 50 Hz, 60 ms decay
    const t = i / RATE, f = 50 + 70 * Math.exp(-t / 0.03);
    pcm[at + i] += 0.8 * Math.exp(-t / 0.06) * Math.sin(2 * Math.PI * f * t);
  }
  for (const k of [1, 2]) {                        // hats: 30 ms of noise on the triplets between kicks
    const off = at + Math.round(BEAT * k / 3 * RATE);
    for (let i = 0; i < 0.03 * RATE; i++) pcm[off + i] += 0.5 * Math.exp(-i / RATE / 0.01) * noise();
  }
}
for (let i = Math.round(BEATS * BEAT * RATE); i < N; i++) pcm[i] = 0.004 * noise();
const wav = Buffer.alloc(44 + N * 2);
wav.write("RIFF", 0); wav.writeUInt32LE(36 + N * 2, 4); wav.write("WAVEfmt ", 8);
wav.writeUInt32LE(16, 16); wav.writeUInt16LE(1, 20); wav.writeUInt16LE(1, 22);
wav.writeUInt32LE(RATE, 24); wav.writeUInt32LE(RATE * 2, 28); wav.writeUInt16LE(2, 32); wav.writeUInt16LE(16, 34);
wav.write("data", 36); wav.writeUInt32LE(N * 2, 40);
for (let i = 0; i < N; i++) wav.writeInt16LE(Math.round(Math.max(-1, Math.min(1, pcm[i])) * 32767), 44 + i * 2);
const song = join(mkdtempSync(join(TMP, "aaa-dance-")), "song.wav");
writeFileSync(song, wav);

process.env.AAA_CHROME_FLAGS = [process.env.AAA_CHROME_FLAGS || "", "--use-fake-ui-for-media-stream",
  "--use-fake-device-for-media-stream", `--use-file-for-fake-audio-capture=${song}`,
  "--autoplay-policy=no-user-gesture-required"].join(" ");
const browser = await launch(BIN, TMP, "dance");

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
await S("Page.addScriptToEvaluateOnNewDocument", {source: `(() => { const get = HTMLCanvasElement.prototype.getContext;
  HTMLCanvasElement.prototype.getContext = function (t, ...a) { return /webgl/.test(t) ? null : get.call(this, t, ...a); }; })()`});
const ev = async expr => {
  const r = await S("Runtime.evaluate", {expression: expr, awaitPromise: true, returnByValue: true, userGesture: true});
  if (r.exceptionDetails) throw new Error(expr.slice(0, 60) + " threw: " + (r.exceptionDetails.exception?.description || r.exceptionDetails.text));
  return r.result.value;
};
const size = (w, h) => S("Emulation.setDeviceMetricsOverride", {width: w, height: h, deviceScaleFactor: 1, mobile: w < 600});
const goto = async () => {
  await S("Page.navigate", {url: ORIGIN});
  for (let i = 0; i < 80 && !(await ev("document.readyState === 'complete'")); i++) await sleep(150);
  await sleep(300);                                // module scripts run after load's microtasks
};
let pass = 0, fail = 0;
const ok = (n, c, extra = "") => { if (c) pass++; else { fail++; console.log("FAIL " + n + (extra ? " -- " + extra : "")); } };
const shown = `(() => { const b = document.getElementById("dancebtn"); return !!b && !b.hidden && b.getBoundingClientRect().width > 0; })()`;

// ---- Where it is offered.
await size(1440, 900);
await goto();
ok("the button is shown at 1440 with motion allowed", await ev(shown));
ok("...labelled for what it does", (await ev(`document.getElementById("dancebtn").textContent`)) === "Dance with me");
ok("...in the masthead's navigation, just before Settings", await ev(`(() => {
  const d = document.getElementById("dancebtn"), s = document.getElementById("setbtn");
  return !!d.closest("header nav") && !!(d.compareDocumentPosition(s) & Node.DOCUMENT_POSITION_FOLLOWING); })()`));
ok("...as tall as the Settings chip beside it", await ev(`document.getElementById("dancebtn").offsetHeight ===
  document.getElementById("setbtn").offsetHeight`));
await size(375, 740);
await sleep(200);
ok("hidden at 375, where there is no mascot to dance", !(await ev(shown)));
await size(1440, 900);
await S("Emulation.setEmulatedMedia", {features: [{name: "prefers-reduced-motion", value: "reduce"}]});
await sleep(200);
ok("hidden for a reader who asked for reduced motion", !(await ev(shown)));
await S("Emulation.setEmulatedMedia", {features: []});
await sleep(200);
ok("...and back when they stop asking", await ev(shown));

// ---- The menu.
await ev(`document.getElementById("dancebtn").click()`);
await sleep(300);
const menu = await ev(`(() => { const m = document.getElementById("dancemenu");
  return {open: !m.hidden, exp: document.getElementById("dancebtn").getAttribute("aria-expanded"),
          offered: [...m.querySelectorAll("[data-src]")].filter(c => !c.hidden).map(c => c.dataset.src),
          focus: document.activeElement?.dataset?.src || "", status: !!m.querySelector("[role=status]"),
          lifted: document.querySelector("header").classList.contains("danceopen")}; })()`);
ok("the button opens a menu and says so", menu.open && menu.exp === "true", JSON.stringify(menu));
ok("...offering both sources where both exist (Chromium, with a microphone)",
   menu.offered.includes("mic") && menu.offered.includes("system"), JSON.stringify(menu.offered));
ok("...with focus on the first of them", menu.focus === menu.offered[0], JSON.stringify(menu));
ok("...and a status line for what happens next", menu.status);
ok("...lifting the masthead over the pinned bar while it is open", menu.lifted);
ok("...inside the viewport", await ev(`(() => { const r = document.getElementById("dancemenu").getBoundingClientRect();
  return r.left >= 0 && r.right <= innerWidth; })()`));
await S("Input.dispatchKeyEvent", {type: "keyDown", key: "Escape", code: "Escape", windowsVirtualKeyCode: 27});
await sleep(100);
ok("Escape closes it and hands focus back to the button", await ev(`document.getElementById("dancemenu").hidden &&
  document.activeElement === document.getElementById("dancebtn") && !document.querySelector("header.danceopen")`));

// ---- A refusal is said in words, and nothing starts.
await ev(`(() => { window.__gum = navigator.mediaDevices.getUserMedia;
  navigator.mediaDevices.getUserMedia = () => Promise.reject(new DOMException("no", "NotAllowedError")); })()`);
await ev(`document.getElementById("dancebtn").click()`);
await sleep(200);
await ev(`document.querySelector("#dancemenu [data-src=mic]").click()`);
await sleep(200);
const refused = await ev(`({msg: document.querySelector(".dancemsg").textContent, label: document.getElementById("dancebtn").textContent,
  music: "archieMusic" in window})`);
ok("a refused microphone is said in the status line", /not allowed/i.test(refused.msg), JSON.stringify(refused));
ok("...and music mode does not start", refused.label === "Dance with me" && !refused.music, JSON.stringify(refused));
await ev(`navigator.mediaDevices.getUserMedia = window.__gum`);

// ---- Listening. The listener is registered before the click, as the loader's are at load. Closed audio
// contexts are counted so that stopping can be shown to release the detector, which a stopped track cannot
// show: it goes quiet either way.
await ev(`(() => { window.__closed = 0; const close = AudioContext.prototype.close;
  AudioContext.prototype.close = function () { __closed++; return close.call(this); }; })()`);
await ev(`(() => { window.__log = [];
  document.addEventListener("archie:music", e => __log.push({t: "music", ...e.detail, had: "archieMusic" in window}));
  document.addEventListener("archie:beat", e => __log.push({t: "beat", ...e.detail}));
  window.__hops = 0; document.querySelector(".mhmascot").addEventListener("animationstart", () => __hops++); })()`);
// Listened to on a throttled CPU, because that is where a detector that works on a quiet laptop fails. The
// first detector here ran on animation frames; at a quarter speed they dropped to about fifteen a second,
// each spectrum spanned more of the song, and it counted the triplet hats (171 BPM), but only when the
// suite's other harnesses had the runner busy. The worklet it became is on the audio thread, which this
// throttle does not slow.
// And with long frames made on purpose, 120 ms of every 350, which is what the model rendering on a slow
// laptop does: a beat whose message waits behind one must still say when it happened. Idle, the page
// delivered its messages on time and a detector timing beats by their arrival passed.
await S("Emulation.setCPUThrottlingRate", {rate: 4});
await ev(`window.__busy = setInterval(() => { const t = performance.now(); while (performance.now() - t < 120); }, 350)`);
await ev(`document.querySelector("#dancemenu [data-src=mic]").click()`);
await sleep(13000);
await ev(`clearInterval(__busy)`);
await S("Emulation.setCPUThrottlingRate", {rate: 1});
const got = await ev(`({log: __log, hops: __hops, label: document.getElementById("dancebtn").textContent,
  menu: document.getElementById("dancemenu").hidden, level: window.archieMusic?.level(),
  saved: localStorage.getItem("archie-dance"), live: document.querySelector(".mhmascot").hasAttribute("data-live")})`);
const on = got.log.find(e => e.t === "music");
ok("choosing the microphone starts music mode, naming the source", on && on.on === true && on.source === "mic", JSON.stringify(on));
ok("...with window.archieMusic already set when that is sent", on && on.had);
ok("...closing the menu and turning the button into its off switch", got.menu && got.label === "Stop dancing", got.label);
ok("...and remembering the choice", got.saved === "mic", got.saved);
ok("archieMusic.level() reads the music, 0..1", typeof got.level === "number" && got.level >= 0 && got.level <= 1, String(got.level));
const beats = got.log.filter(e => e.t === "beat");
const gaps = beats.slice(1).map((b, i) => b.at - beats[i].at);
const onBeat = gaps.filter(g => Math.abs(g - 500) <= 40).length;
// Over 13 s of a 9 s loop there are 12-24 kicks, depending on where in the loop the capture came in.
ok("beats are detected on the kick", beats.length >= 10 && beats.length <= 30, `${beats.length} beats`);
ok("...500 ms apart, not on the hi-hat triplets at 167 and 333", onBeat >= Math.min(8, gaps.length - 2) && !gaps.some(g => g < 280),
   JSON.stringify(gaps.map(Math.round)));
ok("...and not in the silence: one gap spans it", gaps.some(g => g > 2500), JSON.stringify(gaps.map(Math.round)));
// Timed by the audio clock, every gap is within a few ms of 500 however late its message arrived. Timed by
// arrival under this throttle, gaps ran from 359 to 643 ms, which is a model dancing off the beat. The first
// gap is left out: the capture's start can be heard as an onset (672 ms before the first kick, once).
ok("...each timed by the audio clock, not by when its message arrived",
   gaps.slice(1).filter(g => g < 2500).every(g => Math.abs(g - 500) <= 25), JSON.stringify(gaps.map(g => +g.toFixed(1))));
const bpms = beats.map(b => b.bpm).filter(Boolean);
ok("the tempo is found: 120 BPM", bpms.length >= 4 && Math.abs(bpms.at(-1) - BPM) <= 4, JSON.stringify(bpms));
ok("...and is null until there are four gaps to take a median of", beats.length > 4 &&
   beats.slice(0, 4).every(b => b.bpm === null), JSON.stringify(beats.slice(0, 5).map(b => b.bpm)));
ok("strength is 0..1", beats.every(b => b.strength >= 0 && b.strength <= 1));
// Not one hop per beat: two beats whose messages waited behind the same long frame restart one hop, and the
// first never starts (15 hops for 19 beats, once in four runs). A loop that hopped once would not get near.
ok("the poster hops on the beat while there is no live model", !got.live && got.hops >= beats.length * 0.6,
   `${got.hops} hops, ${beats.length} beats, live ${got.live}`);
// The model's arm: once `archie.js` marks it live, the beats go to the model and the poster stays still.
// Five seconds, so at least two of them are music whatever part of the loop they fall in.
// Counted as hops ASKED FOR -- the slot's `beat` class put back on, which is what `bounce()` does -- not as
// `animationstart`s. The event comes at the next style pass, which on this runner is 20 to 150 ms after the
// beat, so a hop asked for by a beat 2 ms before the slot went live started 21 ms after, and was counted
// against the live model (hops:1, in 1 run of 3 here and 3 of 4 on another checkout). A class mutation is recorded in the task
// that made it, so one made before this block runs is delivered before it, and every one counted here
// was asked for while the model was live.
const live = await ev(`(async () => { const slot = document.querySelector(".mhmascot");
  let asked = 0;
  // One bounce() is a remove and an add in one task, so one delivery: counted once.
  const mo = new MutationObserver(ms => { if (slot.classList.contains("beat") &&
    ms.some(m => !(" " + (m.oldValue || "") + " ").includes(" beat "))) asked++; });
  slot.dataset.live = ""; const n0 = __log.length;
  mo.observe(slot, {attributes: true, attributeFilter: ["class"], attributeOldValue: true});
  await new Promise(r => setTimeout(r, 5000));
  mo.disconnect();
  const r = {hops: asked, beats: __log.slice(n0).filter(e => e.t === "beat").length};
  delete slot.dataset.live; return r; })()`);
ok("...and does not while the model is live, though the beats go on", live.beats >= 2 && live.hops === 0,
   JSON.stringify(live));

// ---- Stopping.
await ev(`document.getElementById("dancebtn").click()`);
await sleep(200);
const n = await ev(`__log.filter(e => e.t === "beat").length`);
await sleep(1500);
const off = await ev(`({log: __log.filter(e => e.t === "music"), n: __log.filter(e => e.t === "beat").length,
  music: "archieMusic" in window, label: document.getElementById("dancebtn").textContent})`);
ok("the button stops music mode", off.log.at(-1)?.on === false && off.log.at(-1)?.source === "mic", JSON.stringify(off.log));
ok("...removing window.archieMusic and restoring the label", !off.music && off.label === "Dance with me");
ok("...and no beat comes after it", off.n === n, `${n} then ${off.n}`);
ok("...because the audio context, and the detector in it, is closed", (await ev("__closed")) === 1);
await ev(`document.getElementById("dancebtn").click()`);
await sleep(300);
ok("reopened, the remembered source is offered first", await ev(`(() => {
  const c = [...document.querySelectorAll("#dancemenu [data-src]")].filter(c => !c.hidden)[0];
  return c.dataset.src === "mic" && c.classList.contains("dancelast"); })()`));

// ---- The share path, as far as a headless browser can take it: a stream with no sound is said in words.
await ev(`navigator.mediaDevices.getDisplayMedia = async () => { const c = document.createElement("canvas");
  return c.captureStream(); }`);
await ev(`document.querySelector("#dancemenu [data-src=system]").click()`);
await sleep(300);
const silent = await ev(`({msg: document.querySelector(".dancemsg").textContent, music: "archieMusic" in window})`);
ok("a share with no audio track says so and starts nothing", /no sound/i.test(silent.msg) && !silent.music, JSON.stringify(silent));

ok("no console errors", errors.length === 0, errors.join(" | "));
await browser.close();
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
