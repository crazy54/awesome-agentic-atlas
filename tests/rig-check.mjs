// Archie's light show, on the live model under swiftshader's WebGL: the rig's named cues (the admin
// panel's `window.archieRig`), and the one thing in it with a safety rule behind it, the flash rate.
//
// WCAG 2.3.1 allows no more than three flashes in any one second, a flash being a pair of opposing changes
// in brightness. So every fixture's level -- each of the nine moving heads, the nine wash pars and the
// blinders -- is read on every animation frame for the length of a dance, and each series is scanned for
// swings of at least a tenth of its full scale, up then down, with the time of each. Then no one-second
// window may hold more than six of them (three flashes), and the blinders, the brightest thing on a real
// stage, must SWELL: from a tenth to nine tenths of their peak in no less than a quarter of a second.
//
// WHAT THIS HARNESS CANNOT SEE: what the show looks like, whether a gobo reads or a laser graphic is
// recognisable. Nor the lasers' 2D canvas pixel by pixel: it is checked to come in, to take no pointer
// events, and to go. Nor the wall's clip frame by frame; only that it plays, muted and inline, and is let
// go when the lights go down. The levels read are the rig's own uniforms, the brightness it asks for, not
// the pixels the GPU drew; a shader that ignored `level` would pass here and flash on screen.
//
//   node tests/rig-check.mjs <chrome-binary> <origin>
import {tmpdir} from "node:os";
import {launch} from "./lib/browser.mjs";

const BIN = process.argv[2], ORIGIN = process.argv[3].replace(/\/?$/, "/");
const TMP = process.env.AAA_TMP || tmpdir();
process.env.AAA_CHROME_FLAGS = [process.env.AAA_CHROME_FLAGS || "", "--enable-unsafe-swiftshader",
  "--use-angle=swiftshader", "--autoplay-policy=no-user-gesture-required"].join(" ");
const browser = await launch(BIN, TMP, "rig");

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
  // three.js reports a shader that will not compile through console.error, which Log does not carry: the
  // draw call is then skipped, silently, and the fixture it belonged to is simply not there.
  else if (m.method === "Runtime.consoleAPICalled" && m.params.type === "error")
    errors.push(m.params.args.map(a => a.value ?? a.description ?? "").join(" ").slice(0, 300));
  else if (m.method === "Log.entryAdded" && m.params.entry.level === "error" &&
           !/cloudflareinsights|beacon|opengraph\.githubassets\.com/.test(m.params.entry.text + " " + (m.params.entry.url || "")))
    errors.push(m.params.entry.text);
});
const {targetId} = await send("Target.createTarget", {url: "about:blank"});
const {sessionId} = await send("Target.attachToTarget", {targetId, flatten: true});
const S = (m, p) => send(m, p, sessionId);
await S("Page.enable"); await S("Runtime.enable"); await S("Log.enable");
await S("Emulation.setDeviceMetricsOverride", {width: 1440, height: 900, deviceScaleFactor: 1, mobile: false});
const ev = async expr => {
  const r = await S("Runtime.evaluate", {expression: expr, awaitPromise: true, returnByValue: true, userGesture: true});
  if (r.exceptionDetails) throw new Error(expr.slice(0, 60) + " threw: " + (r.exceptionDetails.exception?.description || r.exceptionDetails.text));
  return r.result.value;
};
const goto = async (q = "") => {
  await S("Page.navigate", {url: ORIGIN + q});
  for (let i = 0; i < 80 && !(await ev("document.readyState === 'complete'")); i++) await sleep(150);
  for (let i = 0; i < 200 && !(await ev(`!!document.querySelector(".mhmascot[data-live]")`)); i++) await sleep(150);
  return ev(`!!document.querySelector(".mhmascot[data-live]")`);
};
const until = async (expr, ms) => {
  for (const end = Date.now() + ms; Date.now() < end; await sleep(100)) if (await ev(expr)) return true;
  return false;
};
let pass = 0, fail = 0;
const ok = (n, c, extra = "") => { if (c) pass++; else { fail++; console.log("FAIL " + n + (extra ? " -- " + extra : "")); } };

// The recorder: every frame, every fixture's level, stamped. Started and stopped by hand.
const RECORD = `(() => { const rec = window.__rig = []; let on = true;
  const f = t => { if (!on) return; const s = window.archieRig && window.archieRig.status();
    if (s) rec.push({t, h: s.heads, p: s.pars, b: s.blinder}); requestAnimationFrame(f); };
  requestAnimationFrame(f); window.__rigStop = () => { on = false; return rec.length; }; })()`;
// Transitions of at least `thr` of full scale in a series, with hysteresis: a swing counts once it has
// moved that far from the last turning point, in the other direction from the last swing.
const swings = (ts, vs, thr) => {
  const out = [];
  let ext = vs[0], dir = 0;
  for (let i = 1; i < vs.length; i++) {
    const v = vs[i];
    if (dir >= 0 && v > ext) ext = v; else if (dir <= 0 && v < ext) ext = v;
    if (dir >= 0 && ext - v >= thr) { out.push(ts[i]); dir = -1; ext = v; }
    else if (dir <= 0 && v - ext >= thr) { out.push(ts[i]); dir = 1; ext = v; }
  }
  return out;
};
const worst = times => {                            // the most swings in any one-second window
  let m = 0;
  for (let i = 0, j = 0; i < times.length; i++) { while (times[i] - times[j] > 1000) j++; m = Math.max(m, i - j + 1); }
  return m;
};
const rate = (rec, pick) => {
  const ts = rec.map(r => r.t), series = pick(rec[0]).map((_, k) => rec.map(r => pick(r)[k]));
  let most = 0, where = -1;
  series.forEach((vs, k) => { const w = worst(swings(ts, vs, 0.1)); if (w > most) { most = w; where = k; } });
  return {most, where};
};

// ---- A dance, all of it.
ok("the model goes live under swiftshader, which the rig needs", await goto("?archie=floss"));
ok("window.archieRig is there once the model is, with the cues the admin panel lists: the rig's, then the stage effects'",
   await ev(`JSON.stringify(window.archieRig && window.archieRig.cues) === JSON.stringify(["beams-chase","beams-fan",
     "beams-cross","ballyhoo","gobo","laser-symbol","blinder","wash","pods","video-wall","all-off",
     "co2","flames","sparks","haze"])`));
ok("the lights come up for the dance", await until(`window.archieRig.status().level > 0.9`, 15000));
await ev(RECORD);
// The whole of floss is 48 beats in 15-16 s; the pods drop at its half-way beat and the blinders swell
// on beats 16 and 32. Read for 14 s from the lights being up, and on until the dance is over: a frame's
// time step is capped at a tenth of a second, so where swiftshader draws four frames a second (the CI
// runner) the dance plays at under half speed, and fourteen seconds never reached its half-way beat.
const seen = {look: new Set(), program: new Set(), gobo: 0, pods: 0, lasers: false};
for (let i = 0; i < 28 || (i < 120 && (await ev(`window.archieRig.status().dancing`))); i++) {
  await sleep(500);
  const s = await ev(`window.archieRig.status()`);
  seen.look.add(s.look); seen.program.add(s.program);
  seen.gobo = Math.max(seen.gobo, s.gobo); seen.pods = Math.max(seen.pods, s.pods); seen.lasers ||= s.lasers;
}
const frames = await ev(`__rigStop()`);
const rec = await ev(`window.__rig`);
ok("the recorder ran on the frame loop", frames > 60, `${frames} frames`);
const heads = rate(rec, r => r.h), pars = rate(rec, r => r.p), bl = rate(rec, r => [r.b]);
ok("moving heads: no more than 3 flashes in any second (WCAG 2.3.1)", heads.most <= 6,
   `${heads.most} swings in a second, head ${heads.where}`);
ok("wash pars: no more than 3 flashes in any second", pars.most <= 6, `${pars.most} swings, par ${pars.where}`);
ok("blinders: no more than 3 flashes in any second", bl.most <= 6, `${bl.most} swings`);
// The swell: every rise of the blinders from under a tenth to over nine tenths of their peak.
const peak = Math.max(...rec.map(r => r.b));
const rises = [];
for (let i = 0, lo = -1; i < rec.length; i++) {
  if (rec[i].b <= peak * 0.1) lo = rec[i].t;
  else if (rec[i].b >= peak * 0.9 && lo >= 0) { rises.push(rec[i].t - lo); lo = -1; }
}
ok("the blinders swell on the dance's big downbeats", peak > 0.5 && rises.length >= 1, `peak ${peak}, ${rises.length} rises`);
ok("...and swell, not hit: a quarter of a second or more from a tenth to nine tenths",
   rises.every(d => d >= 250), JSON.stringify(rises.map(Math.round)));
ok("the heads run more than one program in a dance", seen.program.size >= 2, [...seen.program].join(","));
ok("the dance arcs through more than one look", seen.look.size >= 2, [...seen.look].join(","));
ok("gobos go in during the dance", seen.gobo > 0.9, String(seen.gobo));
ok("the pods drop in its second half", seen.pods > 0.9, String(seen.pods));
ok("the pods' heads light when they are down", rec.some(r => r.h.slice(6).every(v => v > 0.3)),
   JSON.stringify(Math.max(...rec.map(r => Math.min(...r.h.slice(6))))));
ok("the lasers come in for a bar, as an accent", seen.lasers);

// ---- The cues, fired between dances.
await until(`window.archieRig.status().level === 0`, 20000);
ok("an unknown cue is refused", (await ev(`window.archieRig.cue("strobe")`)) === false);
for (const [name, check] of [
  ["beams-chase", `s.program === "chase"`], ["beams-fan", `s.program === "fan"`], ["beams-cross", `s.program === "cross"`],
  ["ballyhoo", `s.program === "ballyhoo"`], ["gobo", `s.gobo > 0.9`], ["pods", `s.pods > 0.9`],
  ["wash", `s.look === "low-tide" && s.pars.every(v => v > 0.8)`], ["blinder", `s.blinder > 0.5`],
]) {
  ok(`cue ${name}: taken`, (await ev(`window.archieRig.cue(${JSON.stringify(name)})`)) === true);
  ok(`...and it plays`, await until(`(s => ${check})(window.archieRig.status())`, 6000),
     name + " " + JSON.stringify(await ev(`window.archieRig.status()`)));
}
// A second blinder cue as soon as the first swell is over swells them again: a dance's downbeat in the
// four seconds before once swallowed the cue, which is how it failed on CI, mid-dance.
await until(`window.archieRig.status().blinder < 0.05`, 6000);
ok("cue blinder, again straight after a swell: taken", (await ev(`window.archieRig.cue("blinder")`)) === true);
ok("...and it swells again", await until(`window.archieRig.status().blinder > 0.5`, 3000),
   JSON.stringify(await ev(`window.archieRig.status()`)));
ok("cue laser-symbol: taken", (await ev(`window.archieRig.cue("laser-symbol")`)) === true);
const laserCanvas = `[...document.querySelectorAll("body > canvas")].find(c => c.style.zIndex === "30")`;
ok("...the laser canvas comes in", await until(`${laserCanvas}?.style.display === ""`, 6000));
ok("...over the page, taking no pointer events", await ev(`getComputedStyle(${laserCanvas}).pointerEvents === "none"`));
ok("cue all-off: taken", (await ev(`window.archieRig.cue("all-off")`)) === true);
ok("...and the lights go down", await until(`window.archieRig.status().level === 0`, 6000), JSON.stringify(await ev(`window.archieRig.status()`)));
ok("...and the lasers with them", await until(`${laserCanvas}.style.display === "none"`, 4000));
ok("an archie:cue event fires a cue too", await ev(`(async () => {
  document.dispatchEvent(new CustomEvent("archie:cue", {detail: {name: "beams-fan"}}));
  await new Promise(r => setTimeout(r, 1500)); return window.archieRig.status().cue === "beams-fan"; })()`));
await ev(`window.archieRig.cue("all-off")`);

// ---- Quiet mode: the reader asked the mascot to leave them alone, so no cue plays.
await ev(`localStorage.setItem("atlas-byte-quiet", "1")`);
ok("in Quiet mode the model still goes live", await goto(""));
ok("...but a cue is refused", (await ev(`window.archieRig.cue("gobo")`)) === false);
await ev(`localStorage.removeItem("atlas-byte-quiet")`);

// ---- No model, no cues: reduced motion keeps the poster.
await S("Emulation.setEmulatedMedia", {features: [{name: "prefers-reduced-motion", value: "reduce"}]});
await S("Page.navigate", {url: ORIGIN});
await sleep(3000);
ok("for a reader who asked for reduced motion there is no rig to cue", await ev(`!("archieRig" in window) &&
   !document.querySelector(".mhmascot[data-live]")`));
await S("Emulation.setEmulatedMedia", {features: []});

ok("no console errors", errors.length === 0, errors.join(" | "));
await browser.close();
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
