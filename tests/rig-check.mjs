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
// COLOUR, which is not a safety rule but is what the rig is for: the lasers play all through a dance and
// take the palette of the reader's theme -- the accents `pages.css` declares for it, read here out of the
// page's own computed style, independently of the rig -- and change to the new theme's when the reader
// switches, in the numbers the rig reports and in the pixels on the laser canvas. The wash pars cover the
// colour wheel over a dance, not one family; and the heads throw open white at times, and colour at others.
//
// WHAT THIS HARNESS CANNOT SEE: what the show looks like, whether a gobo reads. The laser canvas is read
// for its colours, not its shapes. Nor the wall's clip frame by frame; only that it plays, muted and
// inline, and is let go when the lights go down. The levels read are the rig's own uniforms, the brightness it asks for, not
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
const rgbOf = hex => [0, 2, 4].map(i => parseInt(hex.slice(i, i + 2), 16));
// Hue in degrees, and saturation as HSV has it, of an "rrggbb".
const hsv = hex => {
  const [r, g, b] = rgbOf(hex), mx = Math.max(r, g, b), mn = Math.min(r, g, b), d = mx - mn;
  let h = 0;
  if (d) h = mx === r ? ((g - b) / d + 6) % 6 : mx === g ? (b - r) / d + 2 : (r - g) / d + 4;
  return {h: h * 60, s: mx ? d / mx : 0};
};
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
// on beats 16 and 32. Read for 14 s from the lights being up.
const seen = {look: new Set(), program: new Set(), gobo: 0, pods: 0, lasers: 0, samples: 0, wash: [], scenes: new Set(),
              white: 0, whiteOnHim: false, coloured: false};
for (let i = 0; i < 28; i++) {
  await sleep(500);
  const s = await ev(`window.archieRig.status()`), dark = await ev(`document.documentElement.dataset.theme !== "light"`);
  seen.look.add(s.look); seen.program.add(s.program);
  seen.gobo = Math.max(seen.gobo, s.gobo); seen.pods = Math.max(seen.pods, s.pods);
  if (s.dancing && s.level > 0.9) { seen.samples++; if (s.lasers && s.laser.on) seen.lasers++; }
  seen.wash.push(...s.washColors); seen.scenes.add(s.wash);
  s.beamColors.forEach((hex, k) => {
    const [r, g, b] = rgbOf(hex), spread = Math.max(r, g, b) - Math.min(r, g, b);
    // Open white: a head all the way into white, drawing in a neutral -- near-white on the dark theme, where
    // it adds as light; on the light theme a steel grey, the one white that shows as haze over a white page.
    // Heads 1-4 are the ones whose spot lands on him.
    if (s.white[k] >= 0.95 && spread <= 40 && (!dark || Math.min(r, g, b) >= 220)) { seen.white++; if (k >= 1 && k <= 4) seen.whiteOnHim = true; }
    if (s.level > 0.9 && s.white[k] === 0 && spread >= 80) seen.coloured = true;
  });
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
ok("the lasers play all through the dance, as they did before the moving heads", seen.samples >= 10 && seen.lasers >= seen.samples * 0.9,
   `${seen.lasers} of ${seen.samples} samples with the dance's lights up`);
// The wash: every colour the nine pars showed, the saturated ones binned by hue into twelve 30-degree
// sectors. A look's two wash colours, or any one family, fills two or three.
const bins = new Set(seen.wash.map(hsv).filter(c => c.s > 0.35).map(c => Math.floor(c.h / 30) % 12));
ok("the wash covers the colour wheel over a dance: eight or more of twelve hue sectors", bins.size >= 8,
   `${bins.size} sectors: ${[...bins].sort((a, b) => a - b).join(",")}`);
ok("...in more than one colour scene", seen.scenes.size >= 3, [...seen.scenes].join(","));
ok("the heads throw open white at times", seen.white > 0, String(seen.white));
ok("...on him: a head whose spot lands on Archie goes white", seen.whiteOnHim);
ok("...and colour at others", seen.coloured);

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
// The theme's accents, as the page's computed style has them -- read here, not from the rig -- and the
// laser canvas's own pixels: of those it has drawn solidly, what share is within a small distance of one
// of the palette's colours (a beam changing colour, or two crossing, is off it for a moment).
const ACCENTS = `(() => { const cs = getComputedStyle(document.documentElement), out = [];
  for (const k of ["--accent-sky", "--accent-mint", "--accent-gold", "--accent-coral", "--accent-violet", "--bar"]) {
    const m = /^#([0-9a-f]{6})$/i.exec(cs.getPropertyValue(k).trim());
    if (m) { const n = parseInt(m[1], 16), c = [n >> 16, (n >> 8) & 255, n & 255].join(","); if (!out.includes(c)) out.push(c); }
  }
  return out; })()`;
// With `not`, only the pixels near `pal` and near none of `not`'s colours count: two themes' accents can
// be within that distance of each other.
const onPalette = (pal, not = []) => `(() => { const c = ${laserCanvas}, d = c.getContext("2d").getImageData(0, 0, c.width, c.height).data;
  const pal = ${JSON.stringify(pal)}.map(s => s.split(",").map(Number)), not = ${JSON.stringify(not)}.map(s => s.split(",").map(Number));
  const near = (ps, i) => ps.some(p => Math.hypot(p[0] - d[i], p[1] - d[i + 1], p[2] - d[i + 2]) <= 40);
  let n = 0, hit = 0;
  for (let i = 0; i < d.length; i += 4 * 7) if (d[i + 3] > 100) { n++; if (near(pal, i) && !near(not, i)) hit++; }
  return {n, share: n ? hit / n : 0}; })()`;
const theme = async (skin, mode) => {
  await ev(`window.archieRig.cue("laser-symbol")`);          // eight more seconds of lasers
  await ev(`document.documentElement.dataset.skin = ${JSON.stringify(skin)};
            document.documentElement.dataset.theme = ${JSON.stringify(mode)}; 1`);
  await sleep(300);
  const pal = await ev(ACCENTS);
  const got = await until(`JSON.stringify(window.archieRig.status().laser.palette) === ${JSON.stringify(JSON.stringify(pal))}`, 3000);
  let px = {n: 0, share: 0};
  for (const end = Date.now() + 5000; Date.now() < end && !(px.n > 200 && px.share >= 0.6); await sleep(150)) px = await ev(onPalette(pal));
  return {pal, got, px};
};
const first = await theme("graphite", "dark");
ok("the lasers take the theme's accents: graphite, dark", first.got && first.pal.length >= 4,
   JSON.stringify([first.pal, await ev(`window.archieRig.status().laser`)]));
ok("...and draw in them, on the canvas", first.px.n > 200 && first.px.share >= 0.6, JSON.stringify(first.px));
for (const [skin, mode] of [["riso", "light"], ["aurora", "dark"], ["sherbet", "light"]]) {
  const t = await theme(skin, mode);
  ok(`switching to ${skin}, ${mode}: the lasers re-read the theme's accents`, t.got && t.pal.join() !== first.pal.join(),
     JSON.stringify([t.pal, await ev(`window.archieRig.status().laser`)]));
  ok("...and draw in the new ones", t.px.n > 200 && t.px.share >= 0.6, JSON.stringify(t.px));
  const old = await ev(onPalette(first.pal, t.pal));
  ok("...not the old", old.share < 0.2, JSON.stringify(old));
}
await ev(`document.documentElement.dataset.skin = "graphite"; document.documentElement.dataset.theme = "dark"; 1`);
// That took long enough for him to have started a dance of his own, which keeps the lights up whatever the
// cues say. Wait it out, and put the lasers' cue back up, so that it is all-off that takes them down.
await until(`!window.archieRig.status().dancing`, 25000);
await ev(`window.archieRig.cue("laser-symbol")`);
await until(`${laserCanvas}.style.display === ""`, 6000);
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
