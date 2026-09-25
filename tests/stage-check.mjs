// Archie's stage, by its pixels: the video wall and the stage effects, each drawn on its own on the live
// model under swiftshader's WebGL, screenshotted and compared, in both themes.
//
// rig-check.mjs reads the levels the rig asks for; this reads what the GPU drew, because every one of these
// was reported as invisible while its level said it was up. The wall played its clip, and drew it as light
// added to the page with gains that lifted a dark clip to a flat pale panel -- or, where the video frame
// callback never came, drew black, and added black is nothing. The CO2 jets fired from behind the towers
// and left the top of the header before they built up; the flames added up to white; the haze was a veil at
// an eighth of an alpha that no beam went through. None of it could be seen, and every level was right.
//
// So each part is drawn alone, through `window.archieRig.solo()` (a camera layer: nothing else about the
// frame changes), fired through its named cue, and the header screenshotted before and after:
//   * the wall, shown by the `video-wall` cue: two frames a second apart must differ over a large area,
//     since a still or a black wall does not; and it must have contrast, since a flat panel is not a picture.
//   * CO2, flames, sparks: the cue must change a large area, CO2 in near-white (dark theme), the flames and
//     sparks in fire colours, red well over blue, never white.
//   * haze, through the beams it catches: a large area, which the veil alone never lights; and the `haze`
//     cue must light more of it than the beams' own thin haze does.
//   * the blinders, swelled by the `blinder` cue: a large, bright change.
//   * and to the reader's music, simulated as archie-dance.js reports it, some pyro within twelve seconds.
//
// WHAT THIS CANNOT SEE: whether it looks good, only that it is there and roughly the right colour; and
// swiftshader decodes the clip, which a real browser may not (autoplay refused, the frame callback never
// firing for an element outside the document). The wall's draw does not wait on either any more -- it draws
// whenever the element's currentTime moves, shows the poster until then, and retries play() once a second
// -- but a browser that will not decode the clip at all shows the poster, and that is not tested here.
//
//   node tests/stage-check.mjs <chrome-binary> <origin>
import {tmpdir} from "node:os";
import {inflateSync} from "node:zlib";
import {launch} from "./lib/browser.mjs";

const BIN = process.argv[2], ORIGIN = process.argv[3].replace(/\/?$/, "/");
const TMP = process.env.AAA_TMP || tmpdir();
const VERBOSE = !!process.env.STAGE_VERBOSE;
// STAGE_ONLY=wall,co2,... runs only those sections (wall, co2, flames, sparks, haze, blinders, music), for
// proving a check against a broken build without waiting on the rest. The suite sets neither.
const ONLY = process.env.STAGE_ONLY ? process.env.STAGE_ONLY.split(",") : null;
const run = name => !ONLY || ONLY.includes(name);
process.env.AAA_CHROME_FLAGS = [process.env.AAA_CHROME_FLAGS || "", "--enable-unsafe-swiftshader",
  "--use-angle=swiftshader", "--autoplay-policy=no-user-gesture-required"].join(" ");
const browser = await launch(BIN, TMP, "stage");

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
  // three.js reports a shader that will not compile through console.error; the draw is then skipped.
  else if (m.method === "Runtime.consoleAPICalled" && m.params.type === "error")
    errors.push(m.params.args.map(a => a.value ?? a.description ?? "").join(" ").slice(0, 300));
});
const {targetId} = await send("Target.createTarget", {url: "about:blank"});
const {sessionId} = await send("Target.attachToTarget", {targetId, flatten: true});
const S = (m, p) => send(m, p, sessionId);
await S("Page.enable"); await S("Runtime.enable");
await S("Emulation.setDeviceMetricsOverride", {width: 1440, height: 900, deviceScaleFactor: 1, mobile: false});
const ev = async expr => {
  const r = await S("Runtime.evaluate", {expression: expr, awaitPromise: true, returnByValue: true, userGesture: true});
  if (r.exceptionDetails) throw new Error(expr.slice(0, 60) + " threw: " + (r.exceptionDetails.exception?.description || r.exceptionDetails.text));
  return r.result.value;
};
const until = async (expr, ms) => {
  for (const end = Date.now() + ms; Date.now() < end; await sleep(100)) if (await ev(expr)) return true;
  return false;
};
let pass = 0, fail = 0;
const ok = (n, c, extra = "") => {
  if (c) pass++; else fail++;
  if (!c || VERBOSE) console.log((c ? "ok   " : "FAIL ") + n + (extra ? " -- " + extra : ""));
};

// ---- PNG, decoded: 8-bit RGB or RGBA, not interlaced, which is what Chrome's screenshots are.
const decode = buf => {
  let p = 8, w = 0, h = 0, type = 0;
  const idat = [];
  while (p < buf.length) {
    const len = buf.readUInt32BE(p), kind = buf.toString("latin1", p + 4, p + 8), body = buf.subarray(p + 8, p + 8 + len);
    if (kind === "IHDR") {
      w = body.readUInt32BE(0); h = body.readUInt32BE(4); type = body[9];
      if (body[8] !== 8 || (type !== 2 && type !== 6) || body[12] !== 0) throw new Error("unexpected PNG format");
    } else if (kind === "IDAT") idat.push(body);
    else if (kind === "IEND") break;
    p += 12 + len;
  }
  const bpp = type === 6 ? 4 : 3, stride = w * bpp, raw = inflateSync(Buffer.concat(idat));
  const px = new Uint8Array(w * h * 3), row = new Uint8Array(stride), prev = new Uint8Array(stride);
  for (let y = 0; y < h; y++) {
    const f = raw[y * (stride + 1)], src = raw.subarray(y * (stride + 1) + 1, (y + 1) * (stride + 1));
    for (let i = 0; i < stride; i++) {
      const a = i >= bpp ? row[i - bpp] : 0, b = prev[i], c = i >= bpp ? prev[i - bpp] : 0;
      let v = src[i];
      if (f === 1) v += a; else if (f === 2) v += b; else if (f === 3) v += (a + b) >> 1;
      else if (f === 4) { const q = a + b - c, pa = Math.abs(q - a), pb = Math.abs(q - b), pc = Math.abs(q - c);
        v += pa <= pb && pa <= pc ? a : pb <= pc ? b : c; }
      row[i] = v & 255;
    }
    for (let x = 0; x < w; x++) for (let k = 0; k < 3; k++) px[(y * w + x) * 3 + k] = row[x * bpp + k];
    prev.set(row);
  }
  return {w, h, px};
};
let clip = null;
const shot = async () => decode(Buffer.from((await S("Page.captureScreenshot", {format: "png", clip})).data, "base64"));
// What changed from `a` to `b`: the pixels that moved by at least `thr` summed over the channels, their mean
// signed change per channel, how far the most-changed twentieth moved, and b's own spread of brightness
// over the changed pixels (p95 - p5 of luma).
const diff = (a, b, thr = 45) => {
  let n = 0;
  const sum = [0, 0, 0], big = [], luma = [];
  for (let i = 0; i < a.px.length; i += 3) {
    const d = [b.px[i] - a.px[i], b.px[i + 1] - a.px[i + 1], b.px[i + 2] - a.px[i + 2]];
    const m = Math.abs(d[0]) + Math.abs(d[1]) + Math.abs(d[2]);
    if (m < thr) continue;
    n++; sum[0] += d[0]; sum[1] += d[1]; sum[2] += d[2];
    big.push(m);
    luma.push(0.3 * b.px[i] + 0.59 * b.px[i + 1] + 0.11 * b.px[i + 2]);
  }
  const pct = (xs, q) => { if (!xs.length) return 0; xs.sort((x, y) => x - y); return xs[Math.floor((xs.length - 1) * q)]; };
  const mean = sum.map(s => (n ? s / n : 0));
  return {n, mean, p95: pct(big, 0.95), spread: pct(luma.slice(), 0.95) - pct(luma, 0.05)};
};
// The most `before` changes over the next `ms`, frame by frame: a screenshot under swiftshader takes a few
// hundred milliseconds, so one frame at a fixed delay lands anywhere in a flame's second of life.
const best = async (before, ms, thr) => {
  let most = {n: 0, mean: [0, 0, 0], p95: 0, spread: 0};
  for (const end = Date.now() + ms; Date.now() < end;) { const d = diff(before, await shot(), thr); if (d.n > most.n) most = d; }
  return most;
};
const act = async () => JSON.stringify(await ev(`[window.archie && window.archie.status(),
  !!document.querySelector("header canvas"), window.archieRig && window.archieRig.status().level]`));
const fmt = d => `${d.n} px changed, mean change ${d.mean.map(v => v.toFixed(0)).join("/")}, p95 ${d.p95}, spread ${d.spread.toFixed(0)}`;

const open = async (theme, q = "") => {
  await S("Page.navigate", {url: ORIGIN + "?stage-blank"});
  await until("document.readyState === 'complete'", 12000);
  await ev(`localStorage.setItem("theme", ${JSON.stringify(theme)})`);
  await S("Page.navigate", {url: ORIGIN + q});
  await until("document.readyState === 'complete'", 12000);
  const live = await until(`!!document.querySelector(".mhmascot[data-live]") && !!window.archieRig`, 30000);
  // Only the WebGL canvas is measured: the rest of the header -- its typed-out code, his speech bubble, the
  // buttons -- is hidden, since a bubble coming up would otherwise count as an effect firing; and so are
  // the lasers' 2D canvas over it, which solo() does not reach.
  await ev(`(() => { const s = document.createElement("style"); s.textContent =
    "header *{visibility:hidden!important;transition:none!important} header canvas{visibility:visible!important}" +
    " body>canvas{visibility:hidden!important}"; document.head.appendChild(s); return 1; })()`);
  clip = await ev(`(() => { const h = document.querySelector("header").getBoundingClientRect();
    return {x: 0, y: Math.max(0, h.top), width: 1440, height: Math.min(900, h.height), scale: 1}; })()`);
  return live && (await ev("document.documentElement.dataset.theme")) === theme;
};
// Keep him idling: the director's own acts -- a dance with its own lights and pyro, a sleep, a walk-off
// that takes the canvas out of the header -- land in the middle of a measurement otherwise. A queued command
// goes before anything he would choose, and each one cuts short whatever he is doing.
const idle = () => ev(`(() => { const q = window.archie.status().queued.length;
  for (let i = q; i < 12; i++) window.archie.run("idle"); return true; })()`);
// Solo `parts`, let whatever was up go down, and hold him still for the frame it is fired over.
const quiet = async (...parts) => {
  await idle();
  await ev(`window.archieRig.cue("all-off")`);
  const solo = await ev(`window.archieRig.solo(...${JSON.stringify(parts)})`);
  await until(`window.archieRig.status().level === 0`, 8000);
  await sleep(2500);                                  // the effects' own tails, and the fog's linger
  return solo;
};
// A section, tried up to three times while any of its checks fail, and reported from its last try. What a
// queue of idles cannot hold off -- a friend dropping in over him -- goes away on a second try; a broken
// build fails all three.
const section = async fn => {
  let out = [];
  for (let k = 0; k < 3; k++) {
    out = [];
    await fn((n, c, extra = "") => out.push([n, !!c, extra]));
    if (out.every(([, c]) => c)) break;
    if (VERBOSE) console.log(`     (retrying: ${out.filter(([, c]) => !c).map(([n]) => n).join("; ")})`);
  }
  for (const [n, c, extra] of out) ok(n, c, extra);
};

for (const theme of ["dark", "light"]) {
  ok(`${theme}: the model goes live, with its rig`, await open(theme));

  // ---- The wall.
  if (run("wall")) await section(async ok => {
    ok(`${theme}: the wall can be drawn on its own`, await quiet("wall"));
    const wb = await shot();
    ok(`${theme}: cue video-wall is taken`, (await ev(`window.archieRig.cue("video-wall")`)) === true);
    await until(`window.archieRig.status().level > 0.9`, 8000);
    await sleep(2500);                                  // the clip loads and fades up
    const w0 = await shot();
    await sleep(1000);
    const w1 = await shot();
    const dw = diff(w0, w1);
    ok(`${theme}: the wall's picture moves: frames a second apart differ over a large area`, dw.n >= 6000, fmt(dw));
    const dwUp = diff(wb, w1);
    ok(`${theme}: ...and is a picture, not a flat panel: where it came up, its brightness has a wide spread`,
       dwUp.n >= 30000 && dwUp.spread >= 90, fmt(dwUp));
  });

  // ---- Pyro and CO2.
  for (const part of ["co2", "flames", "sparks"]) {
    if (!run(part)) continue;
    await section(async ok => {
      ok(`${theme}: ${part} can be drawn on its own`, await quiet(part));
      const before = await shot();
      ok(`${theme}: cue ${part} is taken`, (await ev(`window.archieRig.cue(${JSON.stringify(part)})`)) === true);
      const d = await best(before, 1600);
      const need = {co2: 5000, flames: 4000, sparks: 800}[part];
      ok(`${theme}: ${part} fired is plainly visible (${need}+ px changed)`, d.n >= need, fmt(d) + " " + (await act()));
      const [r, g, b] = d.mean;
      if (part === "co2" && theme === "dark")
        ok(`${theme}: ...in white: every channel up, and near-equally`, r > 40 && b > 40 && Math.abs(r - b) < 0.35 * Math.max(r, b), fmt(d));
      if (part === "co2" && theme === "light")
        ok(`${theme}: ...as a cloud darker than the page, since white on white is nothing`, r < -15 && g < -15, fmt(d));
      // Red's lead over blue as a share of the whole change: white added to the dark masthead's blue-black
      // is 0.10, the flames 0.19-0.32. On the light theme it is fire laid over white, so blue falls furthest.
      if (part !== "co2")
        ok(`${theme}: ...in fire colours: red well over blue, not white`,
           theme === "dark" ? r > 30 && (r - b) / (Math.abs(r) + Math.abs(g) + Math.abs(b)) > 0.15 : r - b > 25, fmt(d));
    });
  }

  // ---- Haze, through the beams it catches.
  if (run("haze")) await section(async ok => {
    ok(`${theme}: the haze can be drawn on its own`, await quiet("haze"));
    const h0 = await shot();
    // The beams up alone first: the haze is always in the room while they are, thinly.
    await ev(`window.archieRig.cue("beams-fan")`);
    await until(`window.archieRig.status().level > 0.9`, 8000);
    await sleep(1200);
    const thin = diff(h0, await shot());
    ok(`${theme}: cue haze is taken`, (await ev(`window.archieRig.cue("haze")`)) === true);
    await sleep(2200);                                  // it thickens over a second and a half
    const dh = diff(h0, await shot());
    // The veil on its own moves no pixel past the threshold (proved by drawing the haze with no beams in
    // it), so an area this size is the beams, caught.
    ok(`${theme}: the haze is plainly visible, where the beams go through it`, dh.n >= 20000, fmt(dh));
    ok(`${theme}: ...and the haze cue thickens it: a third more of the header lit than the beams' own haze`,
       dh.n >= thin.n * 1.33, `${thin.n} px before the cue, ${dh.n} after`);
  });

  // ---- The blinders.
  if (run("blinders")) await section(async ok => {
    ok(`${theme}: the blinders can be drawn on their own`, await quiet("blinders"));
    const b0 = await shot();
    ok(`${theme}: cue blinder is taken`, (await ev(`window.archieRig.cue("blinder")`)) === true);
    const db = await best(b0, 2000);                    // the swell's rise and fall
    ok(`${theme}: the blinders' hit is plainly visible and bright`, db.n >= 5000 && db.p95 >= 170, fmt(db) + " " + (await act()));
  });
  await ev(`window.archieRig.cue("all-off")`);
  await ev(`window.archieRig.solo()`);
}

// ---- To music: pyro on the reader's beats, which before fired about once in a hundred onsets. Here he is
// left to the director, which is what dances to the music; a fresh page, so no idles are queued.
if (run("music")) {
  ok("to music: the model goes live", await open("dark"));
  await ev(`window.archieRig.solo("co2", "flames", "sparks")`);
  await sleep(2500);
  const m0 = await shot();
  await ev(`window.archieMusic = {level: () => 0.7, bass: () => 0.7};
    document.dispatchEvent(new CustomEvent("archie:music", {detail: {on: true, source: "mic"}}));
    window.__beats = setInterval(() => document.dispatchEvent(new CustomEvent("archie:beat",
      {detail: {strength: 0.9, bpm: 120, at: performance.now()}})), 500); 1`);
  const most = await best(m0, 14000);
  ok("to music: pyro fires, plainly, within fourteen seconds of beats", most.n >= 3000, fmt(most));
  await ev(`clearInterval(window.__beats); 1`);
}

ok("no console errors", errors.length === 0, errors.join(" | "));
await browser.close();
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
