// The cards view is a stylesheet, so the only honest way to check it is to let a browser lay it out and
// then measure what it did. probe.mjs asserts that the switch is state and that every rule carries the
// prefix that makes it win; none of that can tell you the cards are four across, that the screenshot came
// back, or that a 290px floor does not overflow a phone. This does, at three widths, against the bytes in
// docs/ served over HTTP.
//
// WHAT THIS HARNESS CANNOT SEE: the prefixed spelling of anything the browser it runs has an unprefixed
// implementation of. The clamp is the case that bit -- this Chrome does the standard `line-clamp`, so a
// `-webkit-line-clamp` with no `display:-webkit-box` beside it clamps perfectly here and is inert in
// Firefox. That assertion lives in probe.mjs, and the two harnesses stay separate because either one alone
// would have passed a rule that was silently doing nothing.
//
//   node tests/cards-check.mjs <chrome-binary> <origin>
//
// The browser used to be started here on a hardcoded debug port 9334 and the origin used to come from
// whatever server happened to be up. Both are now the caller's: `tests/run.mjs` finds the binary and serves
// `docs/` itself, and `lib/browser.mjs` asks the OS for the debugging port. Screenshots go to
// `$AAA_ARTIFACTS`, default `build-tmp/`, which is gitignored -- this file's own directory is not, and 250 KB
// of PNG per run is not a thing to commit.
import {mkdirSync, writeFileSync} from "node:fs";
import {tmpdir} from "node:os";
import {fileURLToPath} from "node:url";
import {join} from "node:path";
import {launch} from "./lib/browser.mjs";

const ROOT = fileURLToPath(new URL("..", import.meta.url));
const BIN = process.argv[2], ORIGIN = process.argv[3];
if (!BIN || !ORIGIN) {
  console.log("usage: node tests/cards-check.mjs <chrome-binary> <origin>");
  process.exit(2);
}
const SHOTS = process.env.AAA_ARTIFACTS || join(ROOT, "build-tmp");
mkdirSync(SHOTS, {recursive: true});

const browser = await launch(BIN, process.env.AAA_TMP || tmpdir(), "cards");

const sleep = ms => new Promise(r => setTimeout(r, ms));
let ws, id = 0;
const waiters = new Map();
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
  }
});

const {targetId} = await send("Target.createTarget", {url: "about:blank"});
const {sessionId} = await send("Target.attachToTarget", {targetId, flatten: true});
const S = (m, p) => send(m, p, sessionId);
await S("Page.enable"); await S("Runtime.enable");
// `DOM` and `CSS` are enabled for one reason: `CSS.forcePseudoState`, which is how DevTools' "force element
// state" checkbox works and the only way to put a row in `:hover` without depending on a synthetic mouse and
// the hit testing behind it. See `hoverFirstRow`.
await S("DOM.enable"); await S("CSS.enable");

// WHETHER THIS BROWSER HAS A POINTING DEVICE IS NOT THIS SUITE'S TO DECIDE, and three assertions below have
// to be built around that. They measure effects that exist only inside `@media(hover:hover)`: the table row's
// 2px accent line, and the card's outline and `card-glow` pulse. The guard is deliberate -- a touch device
// reports a hover and then latches it, so tapping a row used to leave it tinted -- so those effects are real
// for a reader with a mouse and correctly absent for everyone else, including a headless browser with no
// mouse at all.
//
// `(hover: hover)` is false on CI's Chromium 152 and true on the local headless shell, which is why those
// three passed here and failed there, and it cannot be emulated away. Measured, not assumed, in three steps
// and in this order: the query was reported beside the failure (`hoverMQ: false` on CI, `true` locally, with
// `hovered: true` on both -- so the mouse was landing and the pseudo-class was matching all along); then
// `Emulation.setEmulatedMedia` was asked for `hover: hover` and changed nothing; then it was asked for
// `hover: none` on a runner reporting `true`, and changed nothing there either. It accepts the call, returns
// no error, and ignores the feature: `hover` and `pointer` are not in the set CDP can override, unlike
// `prefers-reduced-motion` and `prefers-color-scheme`, which this file emulates below and which do work.
//
// So there is no browser state to fix and nothing to force. What is left is a fact this suite can still
// assert everywhere -- that the stylesheet declares the accent under that guard -- and a stronger one it can
// only assert where the guard is met, that the browser then computes it. `hoverFirstRow` returns both and
// each assertion takes the strongest instrument the runner supports, naming which one it used. Neither arm
// can pass vacuously: the declared arm fails if the rule or its guard goes missing, the computed arm fails
// if anything overrides it in the cascade.

const evalIn = async (expr) => {
  const r = await S("Runtime.evaluate", {expression: expr, awaitPromise: true, returnByValue: true});
  if (r.exceptionDetails) throw new Error(expr.slice(0, 70) + " threw: " +
    (r.exceptionDetails.exception?.description || r.exceptionDetails.text));
  return r.result.value;
};
const resize = (width, height) => S("Emulation.setDeviceMetricsOverride",
  {width, height, deviceScaleFactor: 1, mobile: width < 500});
const settle = async () => {
  for (let i = 0; i < 100; i++) {
    if (await evalIn("document.readyState === 'complete' && !!document.querySelector('#out tr[data-project]')"))
      break;
    await sleep(150);
  }
};
const goto = async (url) => { await S("Page.navigate", {url}); await settle(); };
// A real document load whatever the current URL happens to be. `Page.navigate` to the URL you are already
// on is a same-document fragment change, and when the fragment matches too it is nothing at all -- so the
// theme checks below, which need the pre-paint script to run again after localStorage was written, were
// silently reading a page that had never reloaded. `Page.reload` fixes that and introduces the other half of
// the same trap: it reloads whatever is in the address bar, which by then was the table's URL, so the cards
// assertions measured the table. Naming the URL and forcing the load are two requirements, not one.
const hardGoto = async (url) => { await S("Page.navigate", {url: "about:blank"}); await goto(url); };
const shot = async (name) => {
  const {data} = await S("Page.captureScreenshot", {format: "png"});
  writeFileSync(join(SHOTS, `${name}.png`), Buffer.from(data, "base64"));
};

let pass = 0, fail = 0;
const ok = (n, c, extra = "") => { c ? pass++ : (fail++, console.log("FAIL " + n + (extra ? "  -- " + extra : ""))); };

// Geometry of the first row of cards: how many share a top edge, how wide each is, and whether the
// document had to grow sideways to fit them.
const geom = `(() => {
  const rows = [...document.querySelectorAll('#out tbody tr')];
  const r0 = rows[0].getBoundingClientRect();
  const across = rows.filter(t => Math.abs(t.getBoundingClientRect().top - r0.top) < 2).length;
  const img = rows[0].querySelector('.shot img');
  const ir = img ? img.getBoundingClientRect() : null;
  const cell = rows[0].querySelector('td.shot');
  return {
    across, cardW: Math.round(r0.width), cardH: Math.round(r0.height),
    imgW: ir ? Math.round(ir.width) : 0, imgH: ir ? Math.round(ir.height) : 0,
    imgShown: !!cell && getComputedStyle(cell).display !== 'none',
    lazy: img ? img.loading : '',
    theadShown: getComputedStyle(document.querySelector('#out thead')).display !== 'none',
    tagsShown: getComputedStyle(rows[0].querySelector('td.tg')).display !== 'none',
    langShown: getComputedStyle(rows[0].querySelector('td.lc')).display !== 'none',
    rankPrefix: getComputedStyle(rows[0].querySelector('td.rk'), '::before').content,
    rowBg: getComputedStyle(rows[0]).backgroundColor,
    bodyBg: getComputedStyle(document.body).backgroundColor,
    stripeA: getComputedStyle(rows[0].querySelector('td')).backgroundColor,
    stripeB: getComputedStyle(rows[1].querySelector('td')).backgroundColor,
    hscroll: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    rows: rows.length,
  };
})()`;
const hoverFirstRow = async () => {
  const point = await evalIn(`(() => {
    const r = document.querySelector('#out tbody tr').getBoundingClientRect();
    return {x: Math.round(r.left + Math.min(20, r.width / 2)), y: Math.round(r.top + Math.min(20, r.height / 2))};
  })()`);
  // Away first, then onto the row. A `mouseMoved` to where the pointer already is is not a move, and the
  // pointer is wherever the last dispatch in this file left it -- the mascot check parks it inside the first
  // card and never takes it off. Two events make the arrival a transition from somewhere else whatever ran
  // before.
  await S("Input.dispatchMouseEvent", {type: "mouseMoved", x: 0, y: 0, buttons: 0});
  await S("Input.dispatchMouseEvent", {type: "mouseMoved", x: point.x, y: point.y, buttons: 0});
  // Let the 140ms hover transition reach its final computed value before
  // checking the exact 2px outline width.
  await sleep(200);
  // Every precondition the measurement needs, beside the measurement, because a hover effect reads as absent
  // for four unrelated reasons and a computed `box-shadow:none` distinguishes none of them: the pointing
  // device may be wrong (both rules sit inside `@media(hover:hover)`), the pseudo-class may never have
  // matched, the point may have landed on something stacked over the row, or the view may not be the one the
  // selector names. All four were live suspects on a failure that reproduced only on a runner nobody could
  // attach to, so each is a key in the message rather than a thing to redeploy the suite to find out.
  const measure = `(() => {
    const row = document.querySelector('#out tbody tr'), cell = row.querySelector('td');
    const at = document.elementFromPoint(${point.x}, ${point.y});
    return {row: getComputedStyle(row).boxShadow, cell: getComputedStyle(cell).boxShadow,
            animation: getComputedStyle(row).animationName,
            hoverMQ: matchMedia('(hover: hover)').matches,
            pointerMQ: matchMedia('(pointer: fine)').matches,
            hovered: row.matches(':hover'), cellHovered: cell.matches(':hover'),
            at: at ? [at.tagName.toLowerCase(), ...at.classList].join('.') : null,
            view: document.documentElement.dataset.view};
  })()`;
  const pointed = await evalIn(measure);
  // The same properties again with `:hover` forced on the row rather than pointed at. The mouse turns out to
  // land on both runners, so this is not a workaround for one of them -- it is the deterministic way to hold
  // a row hovered while several properties are read, and it removes hit testing from the list of things a
  // `none` could have meant. Released afterwards, because the forced state outlives the measurement and the
  // next thing this file does is screenshot a layout that must not be hovered.
  const {root} = await S("DOM.getDocument", {depth: 0});
  const {nodeId} = await S("DOM.querySelector", {nodeId: root.nodeId, selector: "#out tbody tr"});
  await S("CSS.forcePseudoState", {nodeId, forcedPseudoClasses: ["hover"]});
  await sleep(200);
  const forced = await evalIn(measure);
  await S("CSS.forcePseudoState", {nodeId, forcedPseudoClasses: []});
  // The hover-guarded rules as this browser parsed them, which is the one reading of them available on a
  // runner where the guard is unmet. CSSOM rather than a regex over the served text on purpose: a rule the
  // browser failed to parse is absent here and present there, and "the stylesheet says so" is only worth
  // asserting about the stylesheet the browser actually built.
  const declared = await evalIn(`(() => {
    const out = [];
    for (const sheet of document.styleSheets) {
      let rules; try { rules = sheet.cssRules; } catch { continue; }
      for (const rule of rules) {
        const guard = rule.media ? (rule.conditionText || rule.media.mediaText) : "";
        if (!/hover/.test(guard)) continue;
        for (const inner of rule.cssRules || [])
          if (/:hover/.test(inner.selectorText || "")) out.push({guard, css: inner.cssText});
      }
    }
    return out;
  })()`);
  return {...forced, declared,
          how: forced.hoverMQ ? "computed" : "declared -- this browser reports no pointing device",
          pointed: {hovered: pointed.hovered, row: pointed.row, cell: pointed.cell,
                    animation: pointed.animation}};
};

// The strongest instrument the runner supports, for one hover effect. `computed` is a predicate over the
// forced-hover computed style; `selector` and `value` locate the declaration to fall back to. Both arms are
// real assertions -- see the note at the top of the file for why there are two and what each one catches --
// and the one that ran is named in the assertion's own label so a green log says which it was.
const drawn = (h, computed, selector, value) => h.hoverMQ
  ? computed(h)
  : h.declared.some((r) => selector.test(r.css) && value.test(r.css));

// ---- 1440px: the view exists for this width
await resize(1440, 900);
await goto(ORIGIN);
const coldView = await evalIn("document.documentElement.dataset.view");
ok("cards are what a cold visit gets", coldView === "cards", coldView);
// No synthetic input before this check: the original loader waited for a human gesture.
await sleep(500);
const initialArt = await evalIn(`(() => {
  const imgs = [...document.querySelectorAll('#out .shot img')];
  const visible = imgs.filter(i => i.getBoundingClientRect().top < innerHeight);
  return {visible: visible.length, started: visible.every(i => !!i.getAttribute('src')),
          deferred: imgs.some(i => i.hasAttribute('data-src'))};
})()`);
ok("visible screenshots start loading before any interaction", initialArt.visible > 0 && initialArt.started,
   JSON.stringify(initialArt));
ok("distant screenshots remain deferred", initialArt.deferred);
ok("the mascot has a visible name tag",
   await evalIn(`document.querySelector('.atlas-name')?.textContent === "Archie 'Atlas' Algorithm"`));

// THE NAME TAG'S LINE COUNT, WHICH IS THE RENAME'S OWN CLAIM. "Archie 'Atlas' Algorithm" is 24 characters
// where "Atlas Byte" was 10, and the stylesheet's answer is that it wraps to two lines inside the mascot's
// own column. That was asserted by comparing the pill's text, which cannot see a line, and the claim was
// consequently false at every width below 641: the mobile rule narrows the column from 128px to 82px without
// touching the 10px type, so the pill went to three lines (82x49) and the masthead grew for it exactly where
// vertical space is scarcest. Counting line boxes with a Range is the instrument, because a height comparison
// would have to assume a line height the stylesheet is free to change.
const nametag = async (label, width) => {
  const m = await evalIn(`(() => {
    const el = document.querySelector('.atlas-name');
    if (!el) return {missing: true};
    const rg = document.createRange(); rg.selectNodeContents(el);
    const tops = new Set();
    for (const r of rg.getClientRects()) if (r.width > 0 && r.height > 0) tops.add(Math.round(r.top * 2) / 2);
    const r = el.getBoundingClientRect(), wrap = document.querySelector('.atlas-byte-wrap').getBoundingClientRect();
    return {lines: tops.size, w: Math.round(r.width), h: Math.round(r.height),
            wrapW: Math.round(wrap.width), font: getComputedStyle(el).fontSize,
            escapes: Math.round(r.width) > Math.round(wrap.width) + 1, offscreen: r.left < 0};
  })()`);
  ok(label, !m.missing && m.lines === 2 && !m.escapes && !m.offscreen,
     JSON.stringify({width, ...m}));
};
await nametag("Archie's name tag is two lines at 1440px", 1440);
const accents = await evalIn(`new Set([...document.querySelectorAll('#out tr[data-project]')]
  .slice(0,20).map(r => getComputedStyle(r).getPropertyValue('--card-accent'))).size`);
ok("cards have varied curated accents", accents > 1, accents);

// Archie only repeats facts already in the row. The browser check exercises the delayed hover path,
// the reader-controlled quiet switch, and the hidden click sequence rather than merely looking for the
// markup those behaviours need.
const firstProjectPoint = await evalIn(`(() => {
  const r = document.querySelector('#out tr[data-project]').getBoundingClientRect();
  return {x: Math.round(r.left + 18), y: Math.round(r.top + Math.min(240, r.height - 18))};
})()`);
await S("Input.dispatchMouseEvent", {type: "mouseMoved", ...firstProjectPoint});
await sleep(450);
ok("Archie introduces a hovered project from its Atlas record", await evalIn(`(() => {
  const speech = document.getElementById('byte-speech');
  return speech && !speech.hidden && speech.textContent.length > 20;
})()`));

// TWO LINES, NOT A PARAGRAPH. The bubble used to end with `r.blurb` verbatim -- the upstream repository
// description -- so its length was set by an unrelated project's GitHub "about" field and the box grew until
// it covered the masthead.
//
// The character cap is asserted, but the LINE COUNT is the assertion that matters and the reason this reads
// geometry rather than string length: a cap does not buy a line count when a project name is an unbreakable
// 67-character run, and a 72-character cap was measured reaching three lines for exactly that reason. The
// generator's budgets were picked by rendering all 3,835 strings its templates can produce into this box; the
// worst of them is checked below, so this one asserts the row the reader is actually on.
//
// Blurb exclusion is separate because the cap alone would pass on a row whose blurb happens to be short.
// `maxBlurb` is reported so a future reader can see what the cap is holding back rather than trusting that
// it is holding anything.
const bubble = await evalIn(`(() => {
  const speech = document.getElementById('byte-speech');
  const row = ROWS.find(r => r.nwo === document.querySelector('#out tr[data-project]').dataset.project);
  const box = speech.getBoundingClientRect(), cs = getComputedStyle(speech);
  const lines = Math.round((box.height - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom)
                            - parseFloat(cs.borderTopWidth) - parseFloat(cs.borderBottomWidth))
                           / parseFloat(cs.lineHeight));
  return {text: speech.textContent, len: speech.textContent.length, lines,
          blurb: row ? row.blurb : "", carriesBlurb: !!(row && row.blurb && row.blurb.length > 24 &&
            speech.textContent.includes(row.blurb.slice(0, 24))),
          maxBlurb: Math.max(...ROWS.map(r => (r.blurb || "").length))};
})()`);
ok("Archie says at most two short lines", bubble.len > 0 && bubble.len <= 74,
   JSON.stringify({len: bubble.len, text: bubble.text}));
ok("Archie's bubble is at most two lines tall as rendered", bubble.lines >= 1 && bubble.lines <= 2,
   JSON.stringify({lines: bubble.lines, text: bubble.text}));
ok("Archie no longer reads the repository blurb aloud", !bubble.carriesBlurb,
   JSON.stringify({maxBlurb: bubble.maxBlurb, text: bubble.text}));

// THE WORST ROW IN THE ATLAS, NOT THE FIRST ONE. Everything above measures whichever project happens to sort
// first, and the defect was never about that project -- it was about the longest name in the corpus meeting
// the longest category name. This rebuilds every string the generator can say for all committed rows, renders
// each into the real bubble, and reports the tallest. It is the only assertion here that would have failed
// the 140-character cap this ticket started with, which reached four lines.
const widest = await evalIn(`(() => {
  const speech = document.getElementById('byte-speech'), cs = getComputedStyle(speech);
  const chrome = parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom)
                 + parseFloat(cs.borderTopWidth) + parseFloat(cs.borderBottomWidth);
  const lh = parseFloat(cs.lineHeight), before = speech.textContent;
  const clip = (t, n) => {
    const p = Array.from(t);
    if (p.length <= n) return t;
    const hard = p.slice(0, n - 1).join(""), word = hard.replace(/\\s+\\S*$/, "");
    return (Array.from(word).length >= n / 2 ? word : hard) + "\\u2026";
  };
  const said = new Set();
  for (const r of ROWS) {
    const cat = (D.cats[r.cat] || {}).name || "the atlas";
    const tg = r.targets.map(t => D.targets[t] && D.targets[t].name).filter(Boolean);
    const name = clip(r.name, 26), owner = r.nwo.split("/")[0];
    const facts = [name + " is listed under " + cat + ".",
                   name + " is on " + r.lists + (r.lists === 1 ? " source list." : " source lists.")];
    if (owner.toLowerCase() !== r.name.toLowerCase()) facts.push(name + " comes from " + owner + ".");
    const tail = tg.length ? " Tagged for " + tg[0] + "." : "";
    for (const f of facts) said.add(clip(f + ((f + tail).length <= 62 ? tail : ""), 74));
  }
  // TWO INSTRUMENTS, AND THEY HAVE TO AGREE. Dividing the box height by lineHeight infers a line count from
  // arithmetic, and it is only as good as the assumption that every line occupies exactly one lineHeight --
  // an inline image, a taller fallback font for one glyph, or a lineHeight the stylesheet later expresses as
  // a unitless number would all break it silently. A Range over the contents returns one client rect per line
  // box, which counts what the layout engine actually produced. Both are computed for every string and any
  // disagreement is a failure, so neither can be quietly wrong: measured 0 disagreements across all 3,835,
  // both maxing at 2, for 2.0s vs 2.2s.
  const boxes = () => {
    const rg = document.createRange(); rg.selectNodeContents(speech);
    const tops = new Set();
    for (const rect of rg.getClientRects())
      if (rect.width > 0 && rect.height > 0) tops.add(Math.round(rect.top * 2) / 2);
    return tops.size;
  };
  let worst = 0, worstText = "", tall = 0, worstBox = 0, disagreed = [];
  for (const t of said) {
    speech.textContent = t;
    const n = Math.round((speech.getBoundingClientRect().height - chrome) / lh), b = boxes();
    if (n !== b && disagreed.length < 5) disagreed.push({text: t, byHeight: n, byBox: b});
    if (n > 2 || b > 2) tall++;
    if (b > worstBox) worstBox = b;
    if (n > worst) { worst = n; worstText = t; }
  }
  speech.textContent = before;
  // Left on the page for the walk below, which checks real bubble text against this set rather than
  // rebuilding it a second time, and needs the same clipper to tell a clipped NAME from a clipped SENTENCE.
  // A handoff between two Runtime.evaluate calls in one document, not something the site sets or reads.
  window.__saidByHarness = said;
  window.__clipByHarness = clip;
  return {said: said.size, worstLines: worst, worstText, tall, worstBox, disagreed,
          live: before, matchesLive: said.has(before)};
})()`);
ok("no project in the atlas can push Archie past two lines",
   widest.said > 1000 && widest.worstLines <= 2 && widest.worstBox <= 2 && widest.worstBox >= 1
   && widest.tall === 0, JSON.stringify(widest));
ok("the two ways of counting the bubble's lines agree on every string it can say",
   widest.disagreed.length === 0, JSON.stringify(widest.disagreed));
// The block above restates the generator's sentence templates, so on its own it would keep passing against
// rules the generator no longer has. This is the tie: the string the page really produced for the hovered row
// has to be one of the strings those restated templates can produce. Edit the generator's wording or its
// budgets without editing this file and this fails, which is the only reason the measurement above can be
// trusted to be measuring the shipped text.
ok("the restated templates still match what the page says", widest.matchesLive,
   JSON.stringify({live: widest.live, said: widest.said}));

// ONE ROW IS NOT A TIE, AND A ROW'S DATA DOES NOT PICK ITS SENTENCE. The assertion above holds the restated
// corpus to the one string the page produced for whichever project sorts first, which exercises a single arm
// of the generator. The obvious repair -- choose rows whose data takes the other arms, one with a single
// source list, one named after its own owner, one with no tags -- does not work, and was tried here first:
// the generator picks WHICH of a row's two or three facts to say by hashing its `nwo`, so a row with one
// source list usually says something else about itself. That version passed while the page's singular wording
// was deliberately changed underneath it, because the row it picked never said the singular sentence at all.
//
// What follows therefore selects nothing. It walks the rendered rows in order, focuses each one, waits past
// the 320ms hover delay, reads what the bubble really says, and classifies THAT -- so the arms are arms of
// the observed output, not of a rule this file believes the generator follows. It stops as soon as every arm
// has been seen, which was measured at 29 rows and about 12 seconds; a run where an arm is unreachable walks
// all 120 and fails, which is the right way round.
//
// Three things are then asserted, and the third is the one the row-picking version faked:
//   - every live string it saw rendered in at most two lines. Real measurements of real output, so they hold
//     even if the corpus sweep above ever drifts.
//   - every live string it saw is in the restated set. That is the tie, now over 29 strings covering every
//     wording the generator has rather than over one.
//   - all six wordings were actually observed. Without this the tie could stay green while five of the six
//     went unexercised, which is exactly how the first attempt passed a control it should have failed. Under
//     that control this arm names the missing wording and the tie names 24 strings the templates cannot say.
const walk = await evalIn(`(async () => {
  window.scrollTo(0, 0);
  const speech = document.getElementById('byte-speech'), cs = getComputedStyle(speech);
  const chrome = parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom)
                 + parseFloat(cs.borderTopWidth) + parseFloat(cs.borderBottomWidth);
  const lh = parseFloat(cs.lineHeight);
  if (!window.__saidByHarness || !window.__clipByHarness)
    return {broke: 'the corpus sweep above did not leave its handoff on the page, so there is nothing to '
                 + 'check the live strings against -- read that block\\'s failure first, not this one'};
  const clip = window.__clipByHarness;
  const nameOf = new Map(ROWS.map(r => [r.nwo, r.name]));
  // The wordings, named by what a reader would see. Membership is read off the live string; nothing here
  // decides what any row will say.
  //
  // The clipped arm does not just look for an ellipsis, and that mattered: there are two clippers -- NAME_MAX 26 on the
  // name and BUBBLE_MAX 74 on the finished sentence -- and an ellipsis on its own cannot say which one fired.
  // Setting NAME_MAX to 999 while leaving BUBBLE_MAX alone left this arm reporting itself seen, because long
  // unclipped names pushed whole sentences past 74 and the total clipper supplied the ellipsis. The drift was
  // still caught, but by the restated-set tie alone; this label was lying. It now asks the only question worth
  // asking -- is the name in this sentence this row's name, shortened -- so it can only be satisfied by the
  // clipper it is named after.
  const arms = {
    "filed under a category": t => t.includes(" is listed under "),
    "on one source list": t => t.includes(" source list."),
    "on several source lists": t => t.includes(" source lists."),
    "published by an owner": t => t.includes(" comes from "),
    "tagged for a runtime": t => t.includes(" Tagged for "),
    "a name clipped to fit": (t, nwo) => {
      const full = nameOf.get(nwo) || "", short = clip(full, 26);
      return short !== full && t.startsWith(short);
    }
  };
  const boxes = () => {
    const rg = document.createRange(); rg.selectNodeContents(speech);
    const tops = new Set();
    for (const rect of rg.getClientRects())
      if (rect.width > 0 && rect.height > 0) tops.add(Math.round(rect.top * 2) / 2);
    return tops.size;
  };
  // WHAT THE RENDERED PAGE OWES, AND WHAT IT CANNOT BE ASKED FOR. Five of the six wordings depend only on a
  // row's category, list count, owner and tags, and the first 120 rows carry all five many times over. The
  // sixth depends on a name being longer than 26 characters, and only 6 of the 120 rendered rows qualify --
  // 5.0%, against 10.8% corpus-wide, because popular repositories have short names. PAGE_SIZE redraws that
  // window from whatever the corpus becomes, and the next ingest takes it from 1,294 rows to roughly 8,293: a
  // new top 120 with no long name would turn this red with nobody having changed a line. So the clipped arm is
  // recorded here if it happens to appear and is REQUIRED of the probe below, which goes and finds the longest
  // name in the whole corpus instead of hoping it sorted into the first page.
  const names = Object.keys(arms), fromRows = names.filter(n => n !== "a name clipped to fit");
  const seen = {}, said = [];
  for (const row of [...document.querySelectorAll('#out tr[data-project]')]) {
    if (fromRows.every(n => seen[n])) break;
    // Focus has to leave first: refocusing the element that already holds focus fires no focusin, so the
    // handler never runs and this would read the previous row's sentence out of a stale bubble. Blanking it
    // closes the same hole the other way -- with the bubble emptied and hidden, there is no previous sentence
    // left to mistake for this row's, so a sentence read here was necessarily spoken for this row.
    if (document.activeElement && document.activeElement !== document.body) document.activeElement.blur();
    speech.hidden = true;
    speech.textContent = "";
    (row.querySelector('a') || row).focus({preventScroll: true});
    // WAIT FOR THE EVENT, DO NOT BUDGET FOR IT. This was a flat 400ms against the generator's 320ms delay,
    // which is 80ms of slack -- fine on this machine and an invitation to a flake on a loaded CI runner, where
    // losing the race would have been reported as the bubble refusing to appear. Polling is both safer and
    // faster: it returns as soon as the timer fires rather than always paying 400ms.
    for (let waited = 0; waited < 2500 && (speech.hidden || !speech.textContent); waited += 25)
      await new Promise(r => setTimeout(r, 25));
    if (speech.hidden || !speech.textContent)
      return {broke: 'no sentence within 2.5s for ' + row.dataset.project};
    const text = speech.textContent;
    const lines = Math.round((speech.getBoundingClientRect().height - chrome) / lh), box = boxes();
    said.push({nwo: row.dataset.project, text, len: text.length, lines, box,
               inSet: window.__saidByHarness.has(text)});
    for (const n of names) if (arms[n](text, row.dataset.project)) seen[n] = seen[n] || row.dataset.project;
  }

  // THE PROBE: the longest name in the atlas, fetched through the reader's own search box rather than waited
  // for. This is the same measurement as the walk -- type, focus, read what the bubble really says -- but on a
  // row chosen for the property under test, so the clipped arm no longer rests on six rows out of a hundred and
  // twenty. Every one of the generator's facts begins with the name, so whichever fact the hash picks for this
  // row, a clipped name has to be at the front of it; that is why the probe does not care which arm it gets.
  //
  // The filter is put back before returning, because everything after this file's walk measures the unfiltered
  // table and a leaked query would quietly change what those assertions are looking at.
  const longest = ROWS.reduce((a, r) => Array.from(r.name).length > Array.from(a.name).length ? r : a, ROWS[0]);
  const clippable = Array.from(longest.name).length > 26;
  const qbox = document.getElementById('q'), rowsNow = () => document.querySelectorAll('#out tr[data-project]').length;
  const wasRows = rowsNow();
  let probe = null;
  if (clippable) {
    qbox.value = longest.name;
    qbox.dispatchEvent(new Event('input'));
    let target = null;
    for (let waited = 0; waited < 3000 && !target; waited += 25) {
      await new Promise(r => setTimeout(r, 25));
      target = document.querySelector('#out tr[data-project="' + longest.nwo + '"]');
    }
    if (!target) probe = {broke: 'searching for the longest name (' + longest.nwo + ') never rendered its row'};
    else {
      if (document.activeElement && document.activeElement !== document.body) document.activeElement.blur();
      speech.hidden = true;
      speech.textContent = "";
      (target.querySelector('a') || target).focus({preventScroll: true});
      for (let waited = 0; waited < 2500 && (speech.hidden || !speech.textContent); waited += 25)
        await new Promise(r => setTimeout(r, 25));
      const text = speech.textContent;
      probe = {nwo: longest.nwo, full: longest.name, points: Array.from(longest.name).length,
               short: clip(longest.name, 26), text, spoke: !speech.hidden && !!text,
               clipped: !!text && arms["a name clipped to fit"](text, longest.nwo),
               inSet: window.__saidByHarness.has(text),
               lines: Math.round((speech.getBoundingClientRect().height - chrome) / lh), box: boxes()};
      if (probe.clipped) seen["a name clipped to fit"] = seen["a name clipped to fit"] || longest.nwo;
    }
    qbox.value = "";
    qbox.dispatchEvent(new Event('input'));
    for (let waited = 0; waited < 3000 && rowsNow() !== wasRows; waited += 25)
      await new Promise(r => setTimeout(r, 25));
  }

  return {visited: said.length, seen, missing: fromRows.filter(n => !seen[n]),
          clippable, longestPoints: Array.from(longest.name).length, probe,
          qRestored: rowsNow() === wasRows, qbox: qbox.value,
          clippableRendered: [...document.querySelectorAll('#out tr[data-project]')]
            .filter(r => Array.from(nameOf.get(r.dataset.project) || "").length > 26).length,
          tall: said.filter(s => s.lines > 2 || s.lines < 1 || s.box > 2 || s.box < 1),
          disagreed: said.filter(s => s.lines !== s.box),
          empty: said.filter(s => !s.len),
          adrift: said.filter(s => !s.inSet).map(s => s.nwo + ': ' + s.text)};
})()`);
// FOUR ROWS, NOT SIX. The floor here is a guard against the loop not running at all, and it was the number of
// arms, which is the wrong quantity: a row says exactly one fact, and the four fact wordings are mutually
// exclusive per row, so four rows is the arithmetic minimum that can cover them -- one row can satisfy the tag
// clause and the clipped name on top of its own fact. Today's ordering needs 29, but a corpus where the first
// four rows happened to cover everything would have failed all three of these with nothing wrong.
const FLOOR = 4;
ok("walking the rendered rows reaches every wording Archie has",
   !walk.broke && walk.missing.length === 0 && walk.visited >= FLOOR,
   JSON.stringify({broke: walk.broke, missing: walk.missing, visited: walk.visited, seen: walk.seen,
                   clippableRendered: walk.clippableRendered}));
ok("every sentence Archie was caught saying fits in two lines, by both counts",
   !walk.broke && walk.tall.length === 0 && walk.empty.length === 0 && walk.disagreed.length === 0
   && walk.visited >= FLOOR, JSON.stringify({tall: walk.tall, empty: walk.empty, disagreed: walk.disagreed}));
ok("every sentence Archie was caught saying is one the restated templates can produce",
   !walk.broke && walk.adrift.length === 0 && walk.visited >= FLOOR,
   JSON.stringify({adrift: walk.adrift, visited: walk.visited}));
// The clipped name, asked of the row that must have one rather than of whichever rows the corpus put on page
// one. `clippable` false would mean no name in the atlas exceeds 26 characters, which is a real answer and not
// a pass -- 140 of 1,294 do today -- so it is reported rather than skipped over.
ok("the longest name in the atlas is clipped in what Archie says about it, and still fits two lines",
   !walk.broke && walk.clippable && walk.probe && !walk.probe.broke && walk.probe.spoke
   && walk.probe.clipped && walk.probe.inSet && walk.probe.lines <= 2 && walk.probe.box <= 2
   && walk.qRestored, JSON.stringify({clippable: walk.clippable, longestPoints: walk.longestPoints,
                                      probe: walk.probe, qRestored: walk.qRestored, q: walk.qbox}));

// THE BUBBLE MUST NOT LAND ON ANYTHING THE READER CAME FOR, and "the navigation" turned out to be too narrow
// a way to say that. It was anchored `right:calc(100% + 12px); top:8px`, immediately left of the mascot at the
// nav's own height, so it covered the nav at every text length. Re-anchoring it under the mascot cleared the
// nav and was then measured landing on the filter bar's Ctrl/K hint at 1440 and over the search field at 375 --
// so this checks the bar as well, and it is checked at every width this file visits rather than once, because
// the masthead reflows: the band the bubble uses is only there while the nav sits beside the mascot instead of
// above it.
//
// `.bar` is `position:sticky`, so its rect depends on scroll and this has to run unscrolled to mean anything.
// Focus is taken with `preventScroll` for that reason -- a plain `focus()` scrolls the row into view, which
// moved the bar under the measurement and invented overlaps that were not real.
//
// `pin` decides what is in the bubble while it is measured, and without it this measured whatever the last
// thing to speak happened to leave there -- after the walk above, the row it stopped on. That is a real
// difference and not a tidiness point: 45 of the 120 rendered rows say something that fits on one line, and a
// one-line bubble sits 16.56px lower than a two-line one, so the gap being measured was decided by where an
// unrelated loop broke. Pinned to the tallest string the corpus can produce, the measurement is both
// deterministic and the worst case.
//
// The pin does not force the bubble open, and must not: `shown` is half of what is being asserted, so a bubble
// this file unhid itself would prove nothing about the page. A row is focused and the sentence waited for, the
// page's own handler does the showing, and only then is the text replaced. That also stopped depending on the
// walk leaving something focused -- the probe's search reset destroys the row it focused, which correctly hides
// the bubble, and this read `shown:false` the moment that landed.
const clearance = async (label, expectShown, pin) => {
  const m = await evalIn(`(async () => {
    window.scrollTo(0, 0);
    const speech = document.getElementById('byte-speech');
    const pin = ${JSON.stringify(pin ?? null)};
    if (pin !== null && speech) {
      if (document.activeElement && document.activeElement !== document.body) document.activeElement.blur();
      speech.hidden = true;
      speech.textContent = "";
      // The anchor, not the row: a comma in querySelector picks the first match in DOCUMENT ORDER rather than
      // the first selector that matches, so this asked for the row element -- which carries no tabindex, took no focus,
      // and left activeElement on BODY.
      const first = document.querySelector('#out tr[data-project]');
      (first?.querySelector('a') || first)?.focus({preventScroll: true});
      for (let waited = 0; waited < 2500 && (speech.hidden || !speech.textContent); waited += 25)
        await new Promise(r => setTimeout(r, 25));
      window.scrollTo(0, 0);
      if (!speech.hidden && speech.textContent) speech.textContent = pin;
    }
    const shown = !!speech && !speech.hidden && getComputedStyle(speech).display !== "none";
    // A silent bubble is reported with enough to tell the three reasons apart -- no mascot in the layout at
    // this width, no row to focus, or a row focused that the handler ignored -- because "shown:false" on its
    // own sent one debugging session looking at the wrong one of the three.
    if (!shown) {
      const wrap = document.querySelector('.atlas-byte-wrap');
      return {shown, display: speech ? getComputedStyle(speech).display : null,
              wrapDisplay: wrap ? getComputedStyle(wrap).display : null,
              rows: document.querySelectorAll('#out tr[data-project]').length,
              active: document.activeElement ? document.activeElement.tagName + '.' +
                      document.activeElement.className : null,
              vw: document.documentElement.clientWidth, said: speech ? speech.textContent.length : null};
    }
    const s = speech.getBoundingClientRect();
    const box = e => { const r = e.getBoundingClientRect();
      return [r.left, r.top, r.right, r.bottom].map(Math.round); };
    const hitting = [];
    for (const sel of ["header nav", ".bar"]) {
      const e = document.querySelector(sel);
      if (!e || getComputedStyle(e).display === "none") continue;
      const n = e.getBoundingClientRect();
      if (!(s.right <= n.left || s.left >= n.right || s.bottom <= n.top || s.top >= n.bottom))
        hitting.push(sel + " " + JSON.stringify(box(e)));
    }
    return {shown, hitting, speech: box(speech), vw: document.documentElement.clientWidth,
            offscreen: s.left < 0 || s.right > document.documentElement.clientWidth};
  })()`);
  if (!expectShown) {
    ok(label, m.shown === false, JSON.stringify(m));
    return;
  }
  ok(label, m.shown && m.hitting.length === 0 && !m.offscreen, JSON.stringify(m));
};
await clearance("Archie's speech bubble clears the navigation and the filter bar at 1440px", true,
                widest.worstText);

// AND WHEN THE READER MAKES THE NAV BIGGER. The clearance above is 38px at rest, which is about one and a half
// nav lines, and a reader who raises Chrome's minimum font size spends it: forcing the nav's type to 20px
// leaves 7px, and 24px -- that setting's maximum -- overlaps the bubble's rectangle by 13px. Rect overlap is
// not the complaint this ticket exists for, though, and the two are worth separating. The complaint was that
// the mascot covered navigation. The header's `z-index:30` beats the bubble's 4, so what actually happens is
// the nav paints over the bubble: the reader loses the tail of an optional fact and keeps every link. That is
// the assertion -- `elementFromPoint` at the centre of every nav link, at a font size no stylesheet here
// chooses, must return the link and never the bubble. A future change that raised the bubble above the header
// would satisfy a rectangle test and fail this one.
//
// Injected as a stylesheet because a minimum font size is a browser preference CDP does not expose, the same
// way `(hover:hover)` is not emulable; forcing the declaration is the closest honest instrument.
const navOverBubble = await evalIn(`(async () => {
  const st = document.createElement('style');
  st.textContent = ".top nav{font-size:24px}";
  document.head.appendChild(st);
  window.scrollTo(0, 0);
  const speech = document.getElementById('byte-speech'), nav = document.querySelector('header nav');
  const a = document.querySelector('#out tr[data-project] a');
  if (document.activeElement && document.activeElement !== document.body) document.activeElement.blur();
  speech.hidden = true; speech.textContent = "";
  a.focus({preventScroll: true});
  for (let waited = 0; waited < 2500 && (speech.hidden || !speech.textContent); waited += 25)
    await new Promise(r => setTimeout(r, 25));
  const spoke = !speech.hidden && !!speech.textContent;
  const s = speech.getBoundingClientRect(), n = nav.getBoundingClientRect();
  const links = [...nav.querySelectorAll('a')].map(el => {
    const r = el.getBoundingClientRect();
    const hit = document.elementFromPoint(Math.round(r.left + r.width / 2), Math.round(r.top + r.height / 2));
    return {text: el.textContent.trim().slice(0, 12),
            covered: !!(hit && (hit.id === "byte-speech" || hit.closest("#byte-speech"))),
            hit: hit ? (hit.id || hit.tagName.toLowerCase()) : null};
  });
  st.remove();
  return {spoke, links: links.length, covered: links.filter(l => l.covered),
          rectsOverlap: !(s.right <= n.left || s.left >= n.right || s.bottom <= n.top || s.top >= n.bottom),
          gap: Math.round(s.top - n.bottom)};
})()`);
ok("a reader who enlarges the navigation keeps every link, even where the bubble reaches it",
   navOverBubble.spoke && navOverBubble.links >= 5 && navOverBubble.covered.length === 0,
   JSON.stringify(navOverBubble));

// LEAVING THE ROW TAKES THE BUBBLE WITH IT. This is the defect the rename shipped alongside: `speak()` set
// `hidden = false` and nothing on the hover path ever set it back, so the first hover of a visit pinned a
// fact over the masthead until the reader found the quiet switch. Moving the pointer off the row is the
// reader's own gesture, so it is dispatched rather than simulated in JS.
await S("Input.dispatchMouseEvent", {type: "mouseMoved", x: 2, y: 2, buttons: 0});
await sleep(120);
ok("Archie stops speaking when the pointer leaves the row",
   await evalIn("document.getElementById('byte-speech').hidden === true"));

// A FACT THAT WAS NEVER OWED. Brushing across a row on the way to the filter bar used to arm the 320ms timer
// and let it land afterwards, about a row the pointer was no longer near. Leaving inside the delay has to
// cancel it, so this waits well past 320ms and expects silence.
await S("Input.dispatchMouseEvent", {type: "mouseMoved", ...firstProjectPoint});
await sleep(80);
await S("Input.dispatchMouseEvent", {type: "mouseMoved", x: 2, y: 2, buttons: 0});
await sleep(500);
ok("a row brushed past within the delay never speaks",
   await evalIn("document.getElementById('byte-speech').hidden === true"));

// Escape reaches the reader who tabbed to the row and has no pointer to move away.
//
// The blur is not decoration. `focus()` on the element that already holds focus fires no `focusin`, so the
// speak handler never runs and this reads a bubble that was never asked to appear -- it passed only because
// nothing earlier in the file happened to leave focus on that link, and it failed the moment something did.
// Waiting for the sentence rather than budgeting 450ms for it is the same fix as in the walk above: the
// generator's delay is 320ms and a loaded CI runner can lose that race.
await evalIn(`(async () => {
  const speech = document.getElementById('byte-speech');
  if (document.activeElement && document.activeElement !== document.body) document.activeElement.blur();
  speech.hidden = true; speech.textContent = "";
  document.querySelector('#out tr[data-project] a')?.focus({preventScroll: true});
  for (let waited = 0; waited < 2500 && (speech.hidden || !speech.textContent); waited += 25)
    await new Promise(r => setTimeout(r, 25));
})()`);
const escaped = await evalIn(`(() => {
  const speech = document.getElementById('byte-speech');
  const spoke = !speech.hidden;
  document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', bubbles: true}));
  return {spoke, hiddenAfter: speech.hidden};
})()`);
ok("focusing a row speaks and Escape dismisses it", escaped.spoke && escaped.hiddenAfter,
   JSON.stringify(escaped));

// Back onto the row, so the quiet switch below is measured from a bubble that is actually showing rather
// than passing vacuously against one this block left hidden.
await S("Input.dispatchMouseEvent", {type: "mouseMoved", x: 0, y: 0, buttons: 0});
await S("Input.dispatchMouseEvent", {type: "mouseMoved", ...firstProjectPoint});
await sleep(450);
ok("Archie speaks again on a fresh hover",
   await evalIn("document.getElementById('byte-speech').hidden === false"));
await evalIn("document.getElementById('byte-quiet').click()");
ok("Archie commentary has a local quiet switch", await evalIn(`(() => {
  const quiet = document.getElementById('byte-quiet'), speech = document.getElementById('byte-speech');
  return quiet?.getAttribute('aria-pressed') === 'true' && speech?.hidden;
})()`));
await evalIn("document.getElementById('byte-quiet').click()");
await evalIn("for(let i=0;i<5;i++) document.getElementById('byte-name').click()");
ok("five quick name-tag clicks reveal Atlas Orbit", await evalIn("document.querySelectorAll('#atlas-orbit .orbit-star').length === 12"));

// The mascot is part of the masthead rather than a decorative background: it needs to arrive as a real
// image, occupy the top-right without covering the navigation, and stop moving when the reader asks the
// operating system for reduced motion. Measuring the served page catches a missing asset, a broken relative
// URL and a layout rule that merely mentions the mascot without putting it where anyone can see it.
const mascot = await evalIn(`(() => {
  const img = document.querySelector('header img.atlas-byte');
  const nav = document.querySelector('header nav');
  if (!img) return null;
  const r = img.getBoundingClientRect(), n = nav.getBoundingClientRect(), cs = getComputedStyle(img);
  return {naturalWidth: img.naturalWidth, left: r.left, right: r.right, top: r.top, width: r.width,
          navRight: n.right, animation: cs.animationName};
})()`);
ok("Archie loads in the masthead", mascot && mascot.naturalWidth > 0, JSON.stringify(mascot));
ok("Archie sits at the upper right without covering navigation",
   mascot && mascot.right > 1440 * .88 && mascot.top < 150 && mascot.left >= mascot.navRight - 1 &&
   mascot.width >= 92 && mascot.width <= 170, JSON.stringify(mascot));
ok("Archie has an idle animation", mascot && mascot.animation !== "none", JSON.stringify(mascot));
await S("Emulation.setEmulatedMedia", {
  media: "screen", features: [{name: "prefers-reduced-motion", value: "reduce"}],
});
const reducedMascot = await evalIn(`(() => {
  const img = document.querySelector('header img.atlas-byte');
  return img ? getComputedStyle(img).animationName : "missing";
})()`);
ok("the mascot becomes still for reduced-motion readers", reducedMascot === "none", reducedMascot);
await S("Emulation.setEmulatedMedia", {media: "screen", features: []});

const faviconHref = await evalIn("document.querySelector('link[rel=icon]')?.getAttribute('href') || ''");
const faviconResponse = await fetch(new URL("favicon.svg", ORIGIN));
ok("the globe emoji favicon is replaced by a local Archie SVG",
   faviconHref === "favicon.svg" && faviconResponse.ok,
   faviconHref + " / HTTP " + faviconResponse.status);

// The default view is written twice in the generator and rendered once here, and nothing compared the three
// until now. `data-view` on the <html> tag is what the reader looks at for the length of a 561 KB fetch,
// before any script has an opinion about anything; `state.view` is what the script then reasons from. The
// commit that made cards the default had to change both, by hand, in two halves of `19_pages.py` some 660
// lines apart. If they ever drift the page paints one view and rearranges into the other the moment
// `data.json` lands -- which is the flash the attribute exists to prevent, and which nothing else in this
// file would notice, because both views render 120 rows and each passes every geometry assertion for the
// view it is actually in. So the assertion is that the three agree, not that they equal a word typed here:
// the cold-visit assertion above is where the word is pinned, and this is where the copies are kept in step.
//
// Read off the served bytes rather than off `docs/index.html`, so it is the same copy the browser was given.
// `fetch` is global in Node, so this costs no dependency.
const source = await (await fetch(ORIGIN)).text();
const attr = source.match(/<html[^>]*\bdata-view="([a-z]+)"/)?.[1];
const literal = source.match(/\bstate\s*=\s*\{[\s\S]{0,400}?\bview:\s*"([a-z]+)"/)?.[1];
// Both halves are asserted to have been *found* before they are compared, because two failed matches are
// both `undefined` and `undefined === undefined` is the kind of green that means nothing was read at all.
ok("the default view is still findable in both places the page writes it",
   !!attr && !!literal, `<html data-view=${attr}>, state.view=${literal}`);
ok("...and the tag, the state object and what actually rendered all say the same thing",
   attr === literal && attr === coldView,
   `<html data-view=${attr}>, state.view=${literal}, rendered ${coldView}`);

const cold = await evalIn(geom);
ok("...and they are laid out as cards, not merely labelled as them", cold.across >= 3,
   JSON.stringify(cold));
await shot("view-cards-cold-1440");

// The table is the opt-in view now, so it is reached by its own link rather than by arriving. Everything
// below still measures the switch *from* the table *to* cards, which is the expensive direction and the one
// worth measuring -- and the measurement's parity depends on the page being in the table when it starts.
// That is what this navigation is for as much as the three assertions on it; see the note after it.
await goto(ORIGIN + "#view=table");
const densityHeights = [];
for (const density of ["compact", "normal", "expanded"]) {
  densityHeights.push(await evalIn(`(() => {
    const s = document.getElementById('density'); if (!s) return 0;
    s.value = '${density}'; s.dispatchEvent(new Event('change', {bubbles:true}));
    return document.querySelector('#out tbody tr').getBoundingClientRect().height;
  })()`));
}
ok("table density changes actual row height", densityHeights[0] > 0 &&
   densityHeights[0] < densityHeights[1] && densityHeights[1] < densityHeights[2], densityHeights.join(','));
await hardGoto(ORIGIN + "#view=table");
ok("table density survives reload", await evalIn("document.getElementById('density')?.value === 'expanded'"));
await evalIn("document.getElementById('density') && (document.getElementById('density').value='normal',document.getElementById('density').dispatchEvent(new Event('change')))");
const tbl = await evalIn(geom);
ok("a #view=table link opens in the table",
   await evalIn("document.documentElement.dataset.view") === "table",
   await evalIn("document.documentElement.dataset.view"));
ok("one row per line in the table", tbl.across === 1, JSON.stringify(tbl));
ok("the table shows its headings", tbl.theadShown);
ok("adjacent table rows use different grey surfaces", tbl.stripeA !== tbl.stripeB,
   tbl.stripeA + " vs " + tbl.stripeB);
const tableHover = await hoverFirstRow();
// Asserted to have been found before anything is read out of it, for the same reason the default-view check
// below asserts both halves matched: on this runner the computed arm answers and an empty `declared` would
// never be looked at, while on CI it is the only arm there is. An empty list there would fail the three
// assertions with no hint that the search, rather than the stylesheet, was what came up short.
ok("the hover-guarded rules are in the stylesheet this browser parsed",
   tableHover.declared.length >= 2, JSON.stringify(tableHover.declared.map((r) => r.guard)));
ok(`a table-row hover draws a thicker 2px accent line (${tableHover.how})`,
   drawn(tableHover, (h) => /0px -2px 0px/.test(h.cell),
         /tbody tr:hover td/, /box-shadow:\s*inset 0 -2px 0/),
   JSON.stringify(tableHover));
await shot("view-table-1440");

// The toggle against the thing it exists to avoid -- counted, not timed.
//
// This used to race two wall clocks: nine medianed samples of a switch against nine of a `render()`,
// passing if the switch came out the smaller number. On an unchanged tree and an idle machine it measured
// 44.1ms against 43.0ms and went red on one run in three (JFH-223). A 2.5% margin between two timings is
// not a margin, and this was the one assertion in the suite that could not be made deterministic by
// construction while every other one compares bytes, counts, geometry or text. Widening the margin is the
// obvious repair and the wrong one: it keeps the race and only lengthens the odds, and an assertion that
// reddens at random teaches whoever is on the other end of CI to re-run until green -- which is the habit
// the assertion floors in `run.mjs` exist to prevent. A flaky guard is worse than no guard, because it
// also spends attention.
//
// The claim being made is "switching views avoids a re-render", and that is a statement about work
// performed rather than about elapsed time -- so the work is what is measured. A `MutationObserver`
// drained with `takeRecords()` reports it exactly: rows constructed, rows still on screen afterwards, and
// how many records landed under `#out`. Exact on any machine at any load, no warm-up, no median, no
// number picked out of the air, and it says the invariant out loud: JFH-182's toggle must stay a CSS
// switch and must not become "throw the list away and rebuild it".
//
// The layout the switch provokes is deliberately not measured. A table and a grid of 120 cards relayout
// either way, so that cost is common to both sides and was always the bulk of both timings -- the part
// the toggle actually skips is rebuilding 120 rows of innerHTML on top of it, and that is countable.
//
// Watched over the whole document rather than over `#out`, so a "switch" that rebuilt the list somewhere
// else and swapped it in would still be caught constructing 120 rows.
const work = await evalIn(`(() => {
  const out = document.getElementById('out');
  const rowsIn = n => (n.nodeName === 'TR' ? 1 : 0) +
    (n.querySelectorAll ? n.querySelectorAll('tbody tr').length : 0);
  const count = fn => {
    const had = [...out.querySelectorAll('tbody tr')];
    const obs = new MutationObserver(() => {});
    obs.observe(document.documentElement,
                {childList: true, subtree: true, attributes: true, characterData: true});
    fn();
    // Drained synchronously in the same turn as the call. The observer's own callback is a microtask, and
    // waiting for one would put the scheduler back inside a measurement whose entire point is that it
    // does not depend on the scheduler.
    const recs = obs.takeRecords();
    obs.disconnect();
    let rows = 0, inOut = 0;
    for (const r of recs) {
      for (const n of r.addedNodes) rows += rowsIn(n);
      if (out.contains(r.target)) inOut++;
    }
    return {rowsBuilt: rows, outRecords: inOut, had: had.length,
            survived: had.filter(t => t.isConnected).length};
  };
  // The re-render first and the switch second, so the page ends on the switch: the rows every assertion
  // below reads are then the ones the switch kept, rather than ones a \`render()\` had just rebuilt
  // underneath them.
  const rerender = count(() => render());
  const toggle = count(() => document.getElementById('view').click());
  return {rerender, toggle};
})()`);
// Printed as well as asserted, the way the other harnesses print the figures they reason from: the whole
// point of counting instead of timing is that these are exact numbers somebody can read off a CI log.
console.log(`  a switch built ${work.toggle.rowsBuilt} row(s) and kept ${work.toggle.survived} of ` +
            `${work.toggle.had} on screen; the re-render it avoids built ${work.rerender.rowsBuilt} ` +
            `and kept ${work.rerender.survived} of ${work.rerender.had}`);
// One switch out of the table is the measurement's last act, and that is what leaves the page in cards for
// every assertion below. Asserted rather than counted on, because getting the parity wrong would quietly
// measure the table's geometry and report it as the gallery's.
ok("the toggle measurement left the page in cards",
   await evalIn("document.documentElement.dataset.view") === "cards",
   await evalIn("document.documentElement.dataset.view"));
const c1440 = await evalIn(geom);
ok("the toggle switched the view", await evalIn("document.documentElement.dataset.view") === "cards");
ok("cards are more than two across at 1440px", c1440.across >= 3, JSON.stringify(c1440));
ok("the screenshot is back and fills the card width",
   c1440.imgShown && c1440.imgW >= c1440.cardW - 4, JSON.stringify(c1440));
ok("the image kept its 2:1 shape, so a lazy card reserves its height",
   Math.abs(c1440.imgW / c1440.imgH - 2) < 0.06, c1440.imgW + "x" + c1440.imgH);
ok("images still load lazily", c1440.lazy === "lazy", c1440.lazy);
ok("the headings are gone", !c1440.theadShown);
ok("the topic and target tags are on the card", c1440.tagsShown);
ok("so are the language, licence and push date", c1440.langShown);
ok("the rank carries a # now the column heading has gone", /#/.test(c1440.rankPrefix), c1440.rankPrefix);
ok("nothing overflows sideways", c1440.hscroll <= 0, String(c1440.hscroll));
ok("dark cards sit on a visible charcoal surface rather than merging into the page",
   c1440.rowBg !== c1440.bodyBg, c1440.rowBg + " vs " + c1440.bodyBg);
const cardHover = await hoverFirstRow();
// Again, and not redundantly: this is a different document from the table pass above -- `hardGoto` reloaded
// in between -- so it is a different stylesheet object and a different search of it.
ok("the hover-guarded rules survived the reload into cards",
   cardHover.declared.length >= 2, JSON.stringify(cardHover.declared.map((r) => r.guard)));
ok(`a card hover draws a thicker 2px accent outline (${cardHover.how})`,
   drawn(cardHover, (h) => /0px 0px 0px 2px/.test(h.row),
         /\[data-view="cards"\] tr:hover\s*{/, /box-shadow:\s*0 0 0 2px/),
   JSON.stringify(cardHover));
ok(`a card hover gently pulses its own accent glow (${cardHover.how})`,
   drawn(cardHover, (h) => h.animation === "card-glow",
         /\[data-view="cards"\] tr:hover\s*{/, /animation:[^;]*card-glow/),
   JSON.stringify(cardHover));
ok("no row was rebuilt, so the same count is on screen", c1440.rows === tbl.rows,
   c1440.rows + " vs " + tbl.rows);
// The three counts, each with its non-emptiness conjunct: a measurement taken over an empty list would
// report zero rows built and zero rows lost and satisfy the switch's half of every one of these.
ok("switching views constructs no rows, where the re-render it avoids constructs every one",
   work.toggle.rowsBuilt === 0 && work.rerender.had > 0 &&
   work.rerender.rowsBuilt === work.rerender.had, JSON.stringify(work));
ok("...and the rows on screen after the switch are the same elements, not rebuilt ones",
   work.toggle.had > 0 && work.toggle.survived === work.toggle.had && work.rerender.survived === 0,
   JSON.stringify(work));
ok("...having touched nothing whatever under #out, which is where a re-render does its work",
   work.toggle.outRecords === 0 && work.rerender.outRecords > 0, JSON.stringify(work));
// Cards need no hash now that they are the default, so the thing to assert here is the opposite of what it
// used to be: a reader who has arrived at the default view has a clean URL to share. The opt-in direction --
// that switching to the table does write itself into the hash -- is asserted in the reload section below,
// where there is no click parity to disturb.
ok("the default view leaves no view= in the hash",
   !(await evalIn("location.hash")).includes("view="), await evalIn("location.hash"));
await shot("view-cards-1440");

// The real reason not to re-render, and the one that is not a timing number. A reader 3,000px down the page
// who wants to see the screenshots must not be returned to the top, and a keyboard reader must not lose
// their place -- both of which a `render()` would do, because it replaces the subtree focus is inside.
const survives = await evalIn(`(() => {
  scrollTo(0, 3000);
  const row = document.querySelectorAll('#out tbody tr')[40];
  row.tabIndex = -1; row.focus({preventScroll: true});
  const before = {y: Math.round(scrollY), focused: document.activeElement === row};
  document.getElementById('view').click();
  return {before, after: {y: Math.round(scrollY), focused: document.activeElement === row,
                          stillInDoc: row.isConnected}};
})()`);
ok("the reader keeps their place in the document", survives.before.y > 2000 && survives.after.y > 2000,
   JSON.stringify(survives));
ok("and a keyboard reader keeps their focused row, the DOM never having been replaced",
   survives.before.focused && survives.after.focused && survives.after.stillInDoc,
   JSON.stringify(survives));
await evalIn("scrollTo(0, 0); document.getElementById('view').click()");

// ---- a reload has to land back in cards, off the hash alone
await goto(ORIGIN + "#view=cards");
ok("a #view=cards link opens in cards", await evalIn("document.documentElement.dataset.view") === "cards");
const reloaded = await evalIn(geom);
ok("...with the cards laid out, not just the attribute set", reloaded.across >= 3,
   JSON.stringify(reloaded));

// Both directions of the hash write, from a known start and with no timing loop in the way. The table is
// what the page now has to record, because it is the departure from the default -- and a reader who switches
// back has to be left with a URL that carries no opinion at all, or every link they send would pin a view
// they only ever passed through.
await goto(ORIGIN + "#view=table");
await evalIn("document.getElementById('view').click()");
ok("switching to the default clears view= from the hash",
   !(await evalIn("location.hash")).includes("view="), await evalIn("location.hash"));
await evalIn("document.getElementById('view').click()");
ok("and switching to the table writes it back, so that view is shareable",
   (await evalIn("location.hash")).includes("view=table"), await evalIn("location.hash"));

// ---- 900px, where the table drops the screenshot and the two detail columns
await resize(900, 900);
await goto(ORIGIN + "#view=cards");
const c900 = await evalIn(geom);
ok("cards are two or three across at 900px", c900.across >= 2, JSON.stringify(c900));
ok("the screenshot survives the width at which the table drops it", c900.imgShown);
ok("and so do the two columns the table drops with it", c900.tagsShown && c900.langShown);
ok("nothing overflows sideways at 900px", c900.hscroll <= 0, String(c900.hscroll));
// 900 is the width the masthead reflows at, and reflow is what decides whether the band the bubble sits in
// exists at all -- so the clearance is re-measured here rather than assumed from 1440. Focus rather than the
// mouse, because this only needs the bubble on screen, and `preventScroll` keeps the sticky bar where the
// reader would see it.
await evalIn("document.querySelector('#out tr[data-project] a')?.focus({preventScroll: true})");
await sleep(450);
await clearance("Archie's speech bubble clears the navigation and the filter bar at 900px", true,
                widest.worstText);
await shot("view-cards-900");

// ---- 375px: the 290px floor has to give exactly one column, not a sideways scroll
await resize(375, 812);
await goto(ORIGIN);
ok("a phone's cold visit gets the cards as well",
   await evalIn("document.documentElement.dataset.view") === "cards",
   await evalIn("document.documentElement.dataset.view"));
const c375 = await evalIn(geom);
ok("one card per line on a phone", c375.across === 1, JSON.stringify(c375));
ok("the card fits the screen", c375.cardW <= 375 - 28 + 2, String(c375.cardW));
ok("nothing overflows sideways on a phone", c375.hscroll <= 0, String(c375.hscroll));
ok("the screenshot is there, which the phone table deliberately does not show", c375.imgShown);
// AND ON A PHONE IT IS NOT THERE AT ALL, which is a decision rather than an omission. Below 640px `.headside`
// is full width, so the nav sits immediately left of the mascot and the search field immediately below it:
// there is no band left to put a 270px bubble in, and it was measured covering the search field outright.
// A reader at this width most likely has no pointer to hover with either, and the fact is already on the card
// they are touching. Asserted so that a later change to the anchoring cannot quietly put it back over the
// search field -- and so that the reason is on the record rather than looking like the rule was forgotten.
await evalIn("document.querySelector('#out tr[data-project] a')?.focus({preventScroll: true})");
await sleep(450);
await clearance("Archie says nothing on a phone, where there is nowhere to say it", false);
// The width the two-line claim was actually false at. The bubble is gone here, but the name tag is not, and
// the rule that shrinks his column to 82px is the one that pushed the pill to three lines.
await nametag("Archie's name tag is still two lines on a phone", 375);
await shot("view-cards-375");

// The table's own narrow layout, which this must not have disturbed -- it is a click away on a phone rather
// than the arrival state now. The two are one column either way and are still not the same thing: this one
// drops the screenshot, and the screenshot is the entire reason the cards view exists.
await goto(ORIGIN + "#view=table");
const t375 = await evalIn(geom);
ok("the table's own narrow layout is still one column",
   await evalIn("document.documentElement.dataset.view") === "table" && t375.across === 1,
   JSON.stringify(t375));
ok("and still hides the screenshot, as it always has", !t375.imgShown, JSON.stringify(t375));
await shot("view-table-375");

// ---- 640px exactly: the boundary the name tag broke on, and it is `max-width`, so the rule applies AT 640
// and not merely below it. 375 and 1440 alone would pass a rule that started one pixel off.
await resize(640, 900);
await goto(ORIGIN);
await nametag("Archie's name tag is two lines at the 640px boundary itself", 640);
await resize(641, 900);
await goto(ORIGIN);
await nametag("and two lines on the desktop side of that boundary", 641);

// ---- both themes, because the card's background and border are both theme variables
//
// Set through localStorage and a reload rather than by clicking the toggle. Headless Chrome reports a light
// OS preference, so the page's own pre-paint script resolves to light and the first click of a toggle whose
// label is the *action* goes to dark -- which is how a shot labelled "light" came out identical to every
// other shot in this file. Naming the theme is the only way to be sure which one was photographed.
await resize(1440, 900);
const surfaceIn = async (theme) => {
  await evalIn(`localStorage.setItem('theme','${theme}')`);
  await hardGoto(ORIGIN + "#view=cards");
  ok("the " + theme + " theme resolved", await evalIn("document.documentElement.dataset.theme") === theme,
     await evalIn("document.documentElement.dataset.theme"));
  const bg = await evalIn("getComputedStyle(document.querySelector('#out tbody tr')).backgroundColor");
  ok("a card in the " + theme + " theme has a surface of its own", bg !== "rgba(0, 0, 0, 0)", bg);
  await shot("view-cards-" + theme);
  return bg;
};
const dark = await surfaceIn("dark"), light = await surfaceIn("light");
ok("the two themes do not paint the card the same colour", dark !== light, dark + " vs " + light);

// The clamp is what keeps a row of cards from being as tall as its wordiest member. Behavioural, and
// deliberately not a check on the computed `display`: this Chrome implements the standard `line-clamp`,
// whose `continue:discard` blockifies the element, so the `-webkit-box` the rule asks for computes as
// `flow-root` and an assertion on that value fails while the clamp works perfectly. Line count and overflow
// are what the rule is for, and they mean the same thing in every engine that implements either spelling.
// probe.mjs holds the other half -- that both halves of the prefixed form are present in the stylesheet for
// the engines that only know that one.
const clampIn = () => evalIn(`(() => {
  const ds = [...document.querySelectorAll('#out tbody tr .desc')];
  const lh = parseFloat(getComputedStyle(ds[0]).lineHeight) || 18;
  return {clipped: ds.filter(d => d.scrollHeight > d.clientHeight + 1).length, total: ds.length,
          tallest: Math.round(Math.max(...ds.map(d => d.clientHeight)) / lh)};
})()`);
const clamp = await clampIn();
ok("no blurb on a card runs past four lines", clamp.tallest <= 4, JSON.stringify(clamp));
ok("and the clamp is doing real work -- some blurbs genuinely overflow", clamp.clipped > 0,
   JSON.stringify(clamp));
// The table is where the full text lives, so the clamp must not have leaked into it.
await evalIn("document.getElementById('view').click()");
const full = await clampIn();
ok("the table still shows every blurb in full", full.clipped === 0, JSON.stringify(full));
ok("...which is more than four lines for some of them", full.tallest > 4, JSON.stringify(full));

console.log(`\n${pass} passed, ${fail} failed`);
ws.close();
await browser.close();
process.exit(fail ? 1 : 0);
