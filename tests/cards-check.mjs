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
// state" checkbox works and the only way to ask this browser whether a `:hover` rule applies without going
// through a synthetic mouse and the hit testing behind it. `hoverFirstRow` reports both.
await S("DOM.enable"); await S("CSS.enable");

// The pointing device, declared rather than inherited. Three assertions below measure effects that exist
// only inside `@media(hover:hover)`: the table row's 2px accent line and the card's outline and `card-glow`
// pulse. That guard is deliberate (a touch device reports a hover and then latches it, so tapping a row left
// it tinted), which means those effects are real for a reader with a mouse and absent for everyone else --
// and whether a *headless* browser calls itself hover-capable is a property of the binary and of
// `setDeviceMetricsOverride`, not of this page. A harness that measures a guarded rule should state the
// guard's precondition rather than inherit whatever the runner happens to report. Emulated once here so
// every width sees the same capability, including the 375px pass where `resize()` sets `mobile: true`:
// nothing in this file asserts that a touch device is denied the hover, so there is no case this hides.
//
// It is NOT the reason those three assertions used to fail on CI and pass locally, and it is left here
// having been measured rather than left here having been assumed. That was the first hypothesis -- CI's
// Chromium 152 returned `none` for the row shadow, the cell shadow and the animation name at once, the local
// shell passed all three -- and this emulation was added to settle it. The failure did not move: same three
// assertions, same three `none`s, on a run that had it. `hoverFirstRow` then reported the query alongside
// the measurement and `hoverMQ` was true on both runners, so the media query had never been the difference;
// the pseudo-class was, and the fix is down there. Kept anyway, because a suite that inherits its media
// state from whichever binary CI installed is the failure this file has now been bitten by twice, and one
// line that makes the inherited thing explicit is cheaper than a third round trip to rule it out again.
const POINTING = [{name: "hover", value: "hover"}, {name: "pointer", value: "fine"}];
await S("Emulation.setEmulatedMedia", {media: "screen", features: POINTING});

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
    if (await evalIn("document.readyState === 'complete' && !!document.querySelector('#out tbody tr')"))
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
  // And now the same three properties with `:hover` forced on the row rather than pointed at -- DevTools'
  // "force element state", over CDP. THESE are the ones the three assertions below read, and the pointed
  // measurement is kept only as context in their failure message. The reason is the same one that took the
  // wall clock out of the view-switch assertion further down: what these three want to know is whether the
  // stylesheet draws a 2px accent on hover, and pointing a synthetic mouse at a row makes that answer depend
  // on the browser's input plumbing as well.
  //
  // That dependency is not hypothetical. All three failed on CI and passed locally, twice, and the numbers
  // say why: `hoverMQ` is true on both runners and the forced pass produces the exact accent on both, while
  // `hovered` after an `Input.dispatchMouseEvent` is true on the local headless shell and false on CI's
  // Chromium 152. So the rule was never in doubt and the mouse was never landing -- and whether a headless
  // browser turns a dispatched `mouseMoved` into a hover state is a property of that binary, which is not
  // this project's to assert. Nothing is lost by not pointing: real synthetic input is still exercised by
  // the mascot's own hover check above, which passes on both runners, and it is the only assertion here that
  // is actually about input.
  const {root} = await S("DOM.getDocument", {depth: 0});
  const {nodeId} = await S("DOM.querySelector", {nodeId: root.nodeId, selector: "#out tbody tr"});
  await S("CSS.forcePseudoState", {nodeId, forcedPseudoClasses: ["hover"]});
  await sleep(200);
  const forced = await evalIn(measure);
  // Released, because the node keeps the forced state for the life of the document and the next thing this
  // file measures is a layout that must not be hovered.
  await S("CSS.forcePseudoState", {nodeId, forcedPseudoClasses: []});
  return {...forced, pointed: {hovered: pointed.hovered, row: pointed.row, cell: pointed.cell,
                               animation: pointed.animation}};
};

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
ok("the mascot has a visible name tag", await evalIn("document.querySelector('.atlas-name')?.textContent === 'Atlas Byte'"));
const accents = await evalIn(`new Set([...document.querySelectorAll('#out tr[data-project]')]
  .slice(0,20).map(r => getComputedStyle(r).getPropertyValue('--card-accent'))).size`);
ok("cards have varied curated accents", accents > 1, accents);

// Atlas Byte only repeats facts already in the row. The browser check exercises the delayed hover path,
// the reader-controlled quiet switch, and the hidden click sequence rather than merely looking for the
// markup those behaviours need.
const firstProjectPoint = await evalIn(`(() => {
  const r = document.querySelector('#out tr[data-project]').getBoundingClientRect();
  return {x: Math.round(r.left + 18), y: Math.round(r.top + Math.min(240, r.height - 18))};
})()`);
await S("Input.dispatchMouseEvent", {type: "mouseMoved", ...firstProjectPoint});
await sleep(450);
ok("Atlas Byte introduces a hovered project from its Atlas record", await evalIn(`(() => {
  const speech = document.getElementById('byte-speech');
  return speech && !speech.hidden && speech.textContent.length > 20;
})()`));
await evalIn("document.getElementById('byte-quiet').click()");
ok("Atlas Byte commentary has a local quiet switch", await evalIn(`(() => {
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
ok("Atlas Byte loads in the masthead", mascot && mascot.naturalWidth > 0, JSON.stringify(mascot));
ok("Atlas Byte sits at the upper right without covering navigation",
   mascot && mascot.right > 1440 * .88 && mascot.top < 150 && mascot.left >= mascot.navRight - 1 &&
   mascot.width >= 92 && mascot.width <= 170, JSON.stringify(mascot));
ok("Atlas Byte has an idle animation", mascot && mascot.animation !== "none", JSON.stringify(mascot));
// `setEmulatedMedia` replaces the whole feature list rather than merging into it, so the pointing device
// has to be restated here and on the reset below. Dropping it would turn the hover assertions after this
// point into a test of whatever the runner reports, which is the thing being fixed.
await S("Emulation.setEmulatedMedia", {
  media: "screen", features: [...POINTING, {name: "prefers-reduced-motion", value: "reduce"}],
});
const reducedMascot = await evalIn(`(() => {
  const img = document.querySelector('header img.atlas-byte');
  return img ? getComputedStyle(img).animationName : "missing";
})()`);
ok("the mascot becomes still for reduced-motion readers", reducedMascot === "none", reducedMascot);
await S("Emulation.setEmulatedMedia", {media: "screen", features: POINTING});

const faviconHref = await evalIn("document.querySelector('link[rel=icon]')?.getAttribute('href') || ''");
const faviconResponse = await fetch(new URL("favicon.svg", ORIGIN));
ok("the globe emoji favicon is replaced by a local Atlas Byte SVG",
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
ok("a table-row hover draws a thicker 2px accent line",
   /0px -2px 0px/.test(tableHover.cell), JSON.stringify(tableHover));
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
ok("a card hover draws a thicker 2px accent outline",
   /0px 0px 0px 2px/.test(cardHover.row), JSON.stringify(cardHover));
ok("a card hover gently pulses its own accent glow", cardHover.animation === "card-glow", JSON.stringify(cardHover));
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
