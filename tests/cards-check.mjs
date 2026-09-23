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
// The page this harness is about is the catalogue, and the catalogue is at `catalog/` -- the site root is
// the shelves homepage now, which has no table, no card view, no filter bar and no `#view=` state. Pointed at
// the root, nearly every assertion below would fail for one reason ("the element is not there") and none of
// the failures would say why. `ORIGIN` is kept for the few checks that really are about the root: the
// favicon, and `DORIGIN` for the Discover page.
const CATALOG = ORIGIN.replace(/\/?$/, "/") + "catalog/";
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
await goto(CATALOG);
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
// The pill holds both spellings and the stylesheet paints one, so `textContent` is now "Archie 'Atlas'
// AlgorithmArchie" at every width and asserting it would be asserting nothing about what a reader sees. What
// is checked is the painted text, and separately that the accessible name is the full one wherever it is.
const tagText = await evalIn(`(() => {
  const el = document.querySelector('.atlas-name');
  if (!el) return {missing: true};
  const shown = [...el.querySelectorAll('span')].filter(s => getComputedStyle(s).display !== 'none');
  return {painted: shown.map(s => s.textContent).join(""), spans: shown.length,
          label: el.getAttribute('aria-label')};
})()`);
ok("the mascot has a visible name tag, and one spelling of it at a time",
   tagText.painted === "Archie 'Atlas' Algorithm" && tagText.spans === 1, JSON.stringify(tagText));
ok("the name tag's accessible name is the full name whatever is painted",
   tagText.label === "Archie 'Atlas' Algorithm", JSON.stringify(tagText));

// THE NAME TAG'S LINE COUNT, WHICH IS THE RENAME'S OWN CLAIM. "Archie 'Atlas' Algorithm" is 24 characters
// where "Atlas Byte" was 10, and the stylesheet's answer is that it wraps to two lines inside the mascot's
// own column. That was asserted by comparing the pill's text, which cannot see a line, and the claim was
// consequently false at every width below 641: the mobile rule narrows the column from 128px to 82px without
// touching the 10px type, so the pill went to three lines and the masthead grew for it exactly where vertical
// space is scarcest.
//
// THE PILL'S BOX CANNOT COUNT ITS OWN LINES, so do not be tempted to simplify this into a height comparison.
// `header button` gives the pill the 44px WCAG 2.5.5 tap floor, so at the narrow widths it measures 82x44 with
// one word in it, with two lines, and with three: 82x44 is exactly what CI reported alongside three lines, and
// what this machine reports alongside two. Counting line boxes with a Range is the instrument that sees the
// difference. `overflows` is the consequence a reader would actually see, and it is not the same test: a third
// 9px line is 44.45px against a 42px content box, so the text crosses the pill's own border instead of the
// box growing to admit it.
//
// The expected count is per width because the stylesheet's answer differs by width, and the reason it differs
// is a font: the two-line arrangement of the full name had 2.41px of slack in 62px at 375, and forced
// monospace, Verdana and Tahoma each took three lines. One word cannot wrap to three in any face, so below 641
// the pill paints "Archie" and this asserts one line -- a bound that holds on a runner whose fonts nobody
// here can enumerate, rather than a number retuned until this machine agreed.
const nametag = async (label, width, lines) => {
  const m = await evalIn(`(() => {
    const el = document.querySelector('.atlas-name');
    if (!el) return {missing: true};
    const rg = document.createRange(); rg.selectNodeContents(el);
    const tops = new Set();
    for (const r of rg.getClientRects()) if (r.width > 0 && r.height > 0) tops.add(Math.round(r.top * 2) / 2);
    const r = el.getBoundingClientRect(), wrap = document.querySelector('.atlas-byte-wrap').getBoundingClientRect();
    const shown = [...el.querySelectorAll('span')].filter(s => getComputedStyle(s).display !== 'none');
    return {lines: tops.size, w: Math.round(r.width), h: Math.round(r.height),
            wrapW: Math.round(wrap.width), font: getComputedStyle(el).fontSize,
            painted: shown.map(s => s.textContent).join(""), label: el.getAttribute('aria-label'),
            overflows: el.scrollHeight > el.clientHeight || el.scrollWidth > el.clientWidth,
            escapes: Math.round(r.width) > Math.round(wrap.width) + 1, offscreen: r.left < 0};
  })()`);
  ok(label, !m.missing && m.lines === lines && !m.overflows && !m.escapes && !m.offscreen
     && m.label === "Archie 'Atlas' Algorithm",
     JSON.stringify({width, want: lines, ...m}));
};
await nametag("Archie's name tag is two lines at 1440px", 1440, 2);
const accents = await evalIn(`new Set([...document.querySelectorAll('#out tr[data-project]')]
  .slice(0,20).map(r => getComputedStyle(r).getPropertyValue('--card-accent'))).size`);
ok("cards have varied curated accents", accents > 1, accents);

// Archie only repeats facts already in the row. The browser check exercises the delayed hover path,
// the reader-controlled quiet switch, and the hidden click sequence rather than merely looking for the
// markup those behaviours need.
//
// The point is measured each time it is used, and scrolled to when it is below the fold. The Discover strip
// sits between the bar and the first card, and at 1440x900 it pushes the card's top past the viewport's
// bottom edge -- a mouse event dispatched there hits nothing, so every Archie check read as a silent bubble.
// Checks further down scroll back to the top for their own measurements, so a point fixed once would be
// stale by the time it was reused.
const firstProjectPoint = () => evalIn(`(() => {
  const row = document.querySelector('#out tr[data-project]');
  const at = () => { const r = row.getBoundingClientRect();
    return {x: Math.round(r.left + 18), y: Math.round(r.top + Math.min(240, r.height - 18))}; };
  let p = at();
  if (p.y > innerHeight - 8 || p.y < 0) { window.scrollBy(0, p.y - innerHeight / 2); p = at(); }
  return p;
})()`);
await S("Input.dispatchMouseEvent", {type: "mouseMoved", ...await firstProjectPoint()});
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
// generator's budgets were picked by rendering all 3,837 strings its templates can produce into this box; the
// worst of them is checked below, so this one asserts the row the reader is actually on.
//
// Blurb exclusion is separate because the cap alone would pass on a row whose blurb happens to be short.
// `maxBlurb` is reported so a future reader can see what the cap is holding back rather than trusting that
// it is holding anything.
//
// THE CAPS ARE READ OUT OF THE PAGE RATHER THAN COPIED INTO THIS FILE, and that is not tidiness. They were
// written here nine times -- the name cap in four places, the sentence cap in two, the rest in prose -- and
// the generator owns them. Cut a cap in `19_pages.py` and miss one of the nine and this harness goes wrong in
// both directions at once: it asserts the old, larger bound, so a bubble that is now too big still passes,
// AND it rebuilds the exhaustive string set under the old caps, so it measures sentences the page can no
// longer say while never measuring the ones it now can. Both failures are silent and they hide each other.
//
// Parsed rather than exported because there is nothing to export from: the page's script is an IIFE and these
// are `const`s inside it, invisible to `evalIn`. Matching the source text is the memory-hole risk this file
// has hit before -- a substring check that matched the comment quoting a rule and stayed green after the rule
// was deleted -- so this requires EXACTLY ONE match of a declaration-shaped pattern. `pagemin.py` strips the
// page's comments before it ships, so a comment cannot supply the match, and the count assertion catches it
// if that ever stops being true.
const capsSource = await (await fetch(CATALOG)).text();
const capsFound = [...capsSource.matchAll(/const NAME_MAX = (\d+), SAY_MAX = (\d+)/g)];
ok("the page declares Archie's two caps, exactly once, where this harness can read them",
   capsFound.length === 1, JSON.stringify({matches: capsFound.length}));
const NAME_MAX = Number(capsFound[0][1]), SAY_MAX = Number(capsFound[0][2]);
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
ok("Archie says at most two short lines", bubble.len > 0 && bubble.len <= SAY_MAX,
   JSON.stringify({len: bubble.len, cap: SAY_MAX, text: bubble.text}));
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
    const name = clip(r.name, ${NAME_MAX}), owner = r.nwo.split("/")[0];
    const facts = [name + " is listed under " + cat + ".",
                   name + " is on " + r.lists + (r.lists === 1 ? " source list." : " source lists.")];
    if (owner.toLowerCase() !== r.name.toLowerCase()) facts.push(name + " comes from " + owner + ".");
    const tail = tg.length ? " Tagged for " + tg[0] + "." : "";
    // One cap for both, and code points for the fit test, mirroring the generator. Two separate numbers here
    // is what let the page's own pair drift into looking like a bound it was not; see the note in 19_pages.py.
    for (const f of facts) said.add(clip(f + (Array.from(f + tail).length <= ${SAY_MAX} ? tail : ""), ${SAY_MAX}));
  }
  // TWO INSTRUMENTS, AND THE CLAMP DECIDES WHEN THEY MAY DISAGREE. Dividing the box height by lineHeight infers
  // a line count from arithmetic, and it is only as good as the assumption that every line occupies exactly one
  // lineHeight -- an inline image, a taller fallback font for one glyph, or a lineHeight the stylesheet later
  // expresses as a unitless number would all break it silently. A Range over the contents returns one client
  // rect per line box, which counts what the layout engine actually produced.
  //
  // These used to be required to agree on every string, and that was right until the box was clamped. A
  // line-clamped element still reports every line box the text WANTED -- measured 3 rects with the box two
  // lines tall -- because the third one is laid out and then clipped. So the honest invariant is no longer
  // equality: it is that the box never exceeds two lines, and that the Range may exceed the box only where the
  // clamp is visibly hiding text. Whether text is really cut is the third instrument that makes that check
  // mean something, because without it "they disagree, so something must be clipped" would be an assumption
  // rather than a reading. On this machine's stack: 0 of 3,837 clipped, both instruments maxing at 2. On a
  // wider face the clipped count rises and the box height does not, which is the entire point of the clamp.
  // (No backticks in any comment in this block. It is a template literal, and one would end it.)
  const boxes = () => {
    const rg = document.createRange(); rg.selectNodeContents(speech);
    const tops = new Set();
    for (const rect of rg.getClientRects())
      if (rect.width > 0 && rect.height > 0) tops.add(Math.round(rect.top * 2) / 2);
    return tops.size;
  };
  let worst = 0, worstText = "", tall = 0, worstBox = 0, disagreed = [];
  let clippedCount = 0, clippedSample = "";
  for (const t of said) {
    speech.textContent = t;
    const n = Math.round((speech.getBoundingClientRect().height - chrome) / lh), b = boxes();
    const cut = speech.scrollHeight > speech.clientHeight + 1;
    if (cut) { clippedCount++; if (!clippedSample) clippedSample = t; }
    // A disagreement is licensed only in the direction the clamp can cause, and only when text is really cut.
    if (n !== b && !(b > n && cut) && disagreed.length < 5)
      disagreed.push({text: t, byHeight: n, byBox: b, clipped: cut});
    if (n > 2) tall++;
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
          clippedCount, clippedSample, live: before, matchesLive: said.has(before)};
})()`);
// The box, which is what could cover something, and the only one of the three numbers below that is a promise
// to a reader. `worstBox` is deliberately NOT bounded here: it is what the text wanted, the clamp is free to
// exceed two, and asserting it was what made this fail on CI while the box it was standing in for was correct.
ok("no project in the atlas can push Archie's bubble past two lines",
   widest.said > 1000 && widest.worstLines <= 2 && widest.worstLines >= 1 && widest.tall === 0,
   JSON.stringify(widest));
ok("the bubble's two line counts differ only where the clamp is cutting text",
   widest.disagreed.length === 0, JSON.stringify(widest.disagreed));
// And what the clamp costs, on this runner, in the copy rather than the layout. Not bounded by a number tuned
// until CI agreed: on the face `SAY_MAX` was derived against this is 0, and on a wider one it is the count of
// sentences that lose a tail. Reported rather than asserted at a threshold, because the threshold would be a
// property of whatever fonts a runner happens to have installed, which no assertion here can enumerate --
// forcing three uninstalled Linux families gave identical metrics, and `document.fonts.check()` said true for
// a misspelt name. What IS asserted is that clipping never reaches the majority of what Archie can say, which
// would mean the cap and the box had drifted apart rather than the runner having odd fonts.
ok("clipping is the exception rather than how the bubble normally renders",
   widest.clippedCount * 2 < widest.said,
   JSON.stringify({clipped: widest.clippedCount, of: widest.said, sample: widest.clippedSample}));

// THE PRICE THE CLAMP CHARGES FOR ITS `display`, which every other assertion in this file is blind to.
// (The clamp's own spelling is asserted in probe.mjs, beside the card blurb's, for the reason written there:
// this Chromium implements the standard `line-clamp` and ignores the prefixed one, so a rule missing the half
// Firefox needs would pass every browser check in this file.)
// `hidden` works through the UA stylesheet's `[hidden]{display:none}`, and any author `display` outranks it --
// so adding the clamp made `hidden` stop hiding: measured `display:flow-root` and a 20px box on a bubble whose
// attribute was set. Seven assertions in this file check that Archie has stopped speaking and all seven read
// the ATTRIBUTE, which is still perfectly true, so all seven stay green with the bubble parked on the masthead
// for the rest of the visit. This one reads the box.
const hiddenBox = await evalIn(`(() => {
  const speech = document.getElementById('byte-speech');
  const wasHidden = speech.hidden, wasText = speech.textContent;
  speech.textContent = "A sentence long enough to give the box a height if anything renders it at all.";
  speech.hidden = true;
  const cs = getComputedStyle(speech), r = speech.getBoundingClientRect();
  const got = {display: cs.display, h: Math.round(r.height), w: Math.round(r.width),
               visible: !!(r.width || r.height)};
  speech.hidden = wasHidden; speech.textContent = wasText;
  return got;
})()`);
ok("setting the hidden attribute still removes the bubble's box, clamp or no clamp",
   hiddenBox.display === "none" && !hiddenBox.visible, JSON.stringify(hiddenBox));
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
// Take the pointer off the row before the walk scrolls back to the top. It is still resting where the hover
// checks above left it, and scrolling the row out from under it fires a real `mouseout` a frame later -- which
// lands after the walk has focused the first row and cancels the sentence that focus scheduled.
await S("Input.dispatchMouseEvent", {type: "mouseMoved", x: 2, y: 2, buttons: 0});
await evalIn("new Promise(r => { window.scrollTo(0, 0); requestAnimationFrame(() => requestAnimationFrame(r)); })");
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
  // The clipped arm does not just look for an ellipsis, and that mattered: there are two clippers -- NAME_MAX on the
  // name and SAY_MAX on the finished sentence -- and an ellipsis on its own cannot say which one fired.
  // Setting NAME_MAX to 999 while leaving SAY_MAX alone left this arm reporting itself seen, because long
  // unclipped names pushed whole sentences past SAY_MAX and the total clipper supplied the ellipsis. The drift was
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
      const full = nameOf.get(nwo) || "", short = clip(full, ${NAME_MAX});
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
  // sixth depends on a name being longer than NAME_MAX, and only a handful of the 120 rendered rows qualify --
  // 6 at the old cap of 26, more at 22, but "more" is not "guaranteed" and the count is read back rather than
  // assumed, because popular repositories have short names. Corpus-wide it is 18.5% at 22 and was 10.8% at 26.
  // Cutting the cap makes this arm likelier to appear and no less fragile. PAGE_SIZE redraws that
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
               cut: speech.scrollHeight > speech.clientHeight + 1,
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
  //
  // THE ROW IS FOUND BY IDENTITY, AND NOTHING HERE MAY COUNT ROWS OR TAKE THE FIRST ONE. This is the first
  // harness to type into the reader's own search box, and what comes back is not this file's to predict.
  // On a tree with plain substring search an exact project name returns its one hit. On a tree carrying the
  // semantic search (JFH-293), a query returning fewer than SEM_THIN substring hits has up to SEM_MAX
  // semantically related rows APPENDED to it, and one exact project name is the thinnest query there is, so
  // the same probe was measured returning 13. This file is merged across both and must be right on both,
  // which is the whole argument: a count written here is a count that goes stale on somebody else's feature
  // landing, with nothing in this file changed and no conflict to warn anyone.
  // Worse, the augmentation is conditional on the semantic index having loaded, so once it exists the count
  // differs between a runner where that fetch succeeds and one where it does not: any assertion on how many
  // rows came back would be green on one machine and red on another for reasons that have nothing to do with
  // Archie. Selecting on the data-project attribute is immune to all of it, and was measured so -- re-run with
  // a four-character query that fills the page to 120 rows, the probe still finds its row, still clips its
  // name and still restores the filter.
  //
  // The filtered count is recorded for that reason rather than checked. When this number changes, the change is
  // somebody else's feature working as intended, and the next person should be able to see it here instead of
  // rediscovering it.
  const longest = ROWS.reduce((a, r) => Array.from(r.name).length > Array.from(a.name).length ? r : a, ROWS[0]);
  const clippable = Array.from(longest.name).length > ${NAME_MAX};
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
      probe = {filtered: rowsNow(), nwo: longest.nwo, full: longest.name, points: Array.from(longest.name).length,
               short: clip(longest.name, ${NAME_MAX}), text, spoke: !speech.hidden && !!text,
               clipped: !!text && arms["a name clipped to fit"](text, longest.nwo),
               inSet: window.__saidByHarness.has(text),
               lines: Math.round((speech.getBoundingClientRect().height - chrome) / lh), box: boxes(),
               cut: speech.scrollHeight > speech.clientHeight + 1};
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
            .filter(r => Array.from(nameOf.get(r.dataset.project) || "").length > ${NAME_MAX}).length,
          // The box is the promise; the Range is allowed to run past it exactly where the clamp is cutting.
          // See the note on the two instruments above the corpus sweep -- a clamped element still reports every
          // line box the text wanted, so bounding the Range here would report the runner's fonts, not a defect.
          tall: said.filter(s => s.lines > 2 || s.lines < 1 || s.box < 1),
          disagreed: said.filter(s => s.lines !== s.box && !(s.box > s.lines && s.cut)),
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
// one. `clippable` false would mean no name in the atlas exceeds NAME_MAX, which is a real answer and not
// a pass -- 239 of 1,294 do at 22, and 140 did at 26 -- so it is reported rather than skipped over.
ok("the longest name in the atlas is clipped in what Archie says about it, and still fits two lines",
   !walk.broke && walk.clippable && walk.probe && !walk.probe.broke && walk.probe.spoke
   && walk.probe.clipped && walk.probe.inSet && walk.probe.lines <= 2
   && (walk.probe.box <= 2 || walk.probe.cut)
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
//
// The pointer is put on the row first, and the bubble confirmed showing, rather than assumed to be there from
// whatever ran before. The walk above parks it in the corner, so without this the leave would be a move from
// the corner to the corner -- no event at all -- and the check would read a bubble nothing had dismissed.
await S("Input.dispatchMouseEvent", {type: "mouseMoved", ...await firstProjectPoint()});
await sleep(450);
const beforeLeave = await evalIn("document.getElementById('byte-speech').hidden === false");
await S("Input.dispatchMouseEvent", {type: "mouseMoved", x: 2, y: 2, buttons: 0});
await sleep(120);
ok("Archie stops speaking when the pointer leaves the row",
   beforeLeave && await evalIn("document.getElementById('byte-speech').hidden === true"),
   JSON.stringify({showingBeforeLeave: beforeLeave}));

// A FACT THAT WAS NEVER OWED. Brushing across a row on the way to the filter bar used to arm the 320ms timer
// and let it land afterwards, about a row the pointer was no longer near. Leaving inside the delay has to
// cancel it, so this waits well past 320ms and expects silence.
await S("Input.dispatchMouseEvent", {type: "mouseMoved", ...await firstProjectPoint()});
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
await S("Input.dispatchMouseEvent", {type: "mouseMoved", ...await firstProjectPoint()});
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

// Three values, deliberately: the attribute is `../favicon.svg` because this page sits in `catalog/`, the
// file is at the site root, and the third fetch resolves the attribute the way a browser on this page would.
// The attribute alone would pass on a link pointing one level too far up; the root fetch alone would pass on
// a page with no favicon link at all.
const faviconHref = await evalIn("document.querySelector('link[rel=icon]')?.getAttribute('href') || ''");
const faviconResponse = await fetch(new URL("favicon.svg", ORIGIN));
const faviconResolved = await fetch(new URL(faviconHref || "does-not-exist", CATALOG));
ok("the globe emoji favicon is replaced by a local Archie SVG",
   faviconHref === "../favicon.svg" && faviconResponse.ok && faviconResolved.ok,
   `${faviconHref} / root HTTP ${faviconResponse.status} / resolved HTTP ${faviconResolved.status}`);

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
const source = await (await fetch(CATALOG)).text();
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
await goto(CATALOG + "#view=table");
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
await hardGoto(CATALOG + "#view=table");
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
await goto(CATALOG + "#view=cards");
ok("a #view=cards link opens in cards", await evalIn("document.documentElement.dataset.view") === "cards");
const reloaded = await evalIn(geom);
ok("...with the cards laid out, not just the attribute set", reloaded.across >= 3,
   JSON.stringify(reloaded));

// Both directions of the hash write, from a known start and with no timing loop in the way. The table is
// what the page now has to record, because it is the departure from the default -- and a reader who switches
// back has to be left with a URL that carries no opinion at all, or every link they send would pin a view
// they only ever passed through.
await goto(CATALOG + "#view=table");
await evalIn("document.getElementById('view').click()");
ok("switching to the default clears view= from the hash",
   !(await evalIn("location.hash")).includes("view="), await evalIn("location.hash"));
await evalIn("document.getElementById('view').click()");
ok("and switching to the table writes it back, so that view is shareable",
   (await evalIn("location.hash")).includes("view=table"), await evalIn("location.hash"));

// ---- 900px, where the table drops the screenshot and the two detail columns
await resize(900, 900);
await goto(CATALOG + "#view=cards");
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
await goto(CATALOG);
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
// the rule that shrinks his column to 82px is the one that pushed the pill to three lines. One word now, so
// this is the width where the count being asserted is the one no font can change.
await nametag("Archie's name tag is one unwrappable word on a phone", 375, 1);
await shot("view-cards-375");

// The table's own narrow layout, which this must not have disturbed -- it is a click away on a phone rather
// than the arrival state now. The two are one column either way and are still not the same thing: this one
// drops the screenshot, and the screenshot is the entire reason the cards view exists.
await goto(CATALOG + "#view=table");
const t375 = await evalIn(geom);
ok("the table's own narrow layout is still one column",
   await evalIn("document.documentElement.dataset.view") === "table" && t375.across === 1,
   JSON.stringify(t375));
ok("and still hides the screenshot, as it always has", !t375.imgShown, JSON.stringify(t375));
await shot("view-table-375");

// ---- 640px exactly: the boundary the name tag broke on, and it is `max-width`, so the rule applies AT 640
// and not merely below it. 375 and 1440 alone would pass a rule that started one pixel off.
await resize(640, 900);
await goto(CATALOG);
await nametag("Archie's name tag is one word at the 640px boundary itself", 640, 1);
await resize(641, 900);
await goto(CATALOG);
// And the full name comes back one pixel later, in two lines, in a 128px column with 25% of slack rather than
// 4% -- 108px of content against the 81px the widest face measured needs for "Archie 'Atlas'". This is the
// assertion that would catch the swap being written as `max-width:641px` or applied at every width.
await nametag("and the full name, two lines, on the desktop side of that boundary", 641, 2);

// ---- both themes, because the card's background and border are both theme variables
//
// Set through localStorage and a reload rather than by clicking the toggle. Headless Chrome reports a light
// OS preference, so the page's own pre-paint script resolves to light and the first click of a toggle whose
// label is the *action* goes to dark -- which is how a shot labelled "light" came out identical to every
// other shot in this file. Naming the theme is the only way to be sure which one was photographed.
await resize(1440, 900);
const surfaceIn = async (theme) => {
  await evalIn(`localStorage.setItem('theme','${theme}')`);
  await hardGoto(CATALOG + "#view=cards");
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

// ---- THE SCROLLED PAGE, WHICH THIS FILE HAD NEVER LOOKED AT (JFH-354) ----------------------------------
//
// Every measurement above opens with `scrollTo(0, 0)`, and for a good reason: a plain `focus()` scrolls the
// bar under the ruler and invents overlaps that are not real, which is why `clearance` takes focus with
// `preventScroll` and says so. The cost of that convention was a blind spot exactly the shape of the defect
// it was protecting against. `header` and `.bar` were siblings both at `position:sticky;top:0`, the header
// at `z-index:30`; from the first scroll gesture the masthead covered the search box completely -- 100% at
// 1440x900, 1024x800, 768x900 and 390x844 -- and a reader who wanted to search had to scroll back to the top
// to find out. Every assertion in this file passed throughout, because none of them had scrolled.
//
// So this block scrolls on purpose, and it is the only one that does. It puts the scroll back afterwards for
// the convention's sake, even though nothing follows it today.
//
// Two instruments, and the second is the one that speaks the reader's language. `elementFromPoint` at the
// field's centre says what is painted on top. A real `Input.dispatchMouseEvent` at the same point says what
// happens when somebody puts a finger there -- and a covered field answers that by leaving focus wherever it
// was. CDP cannot emulate hover or pointer (see the note at the top of this file), but a dispatched click
// hit-tests for real, which is why this half can be asserted on every runner.
const BUDGET = 4;   // the pinned band may take at most a quarter of the viewport
for (const [w, h] of [[1440, 900], [1024, 800], [768, 900], [390, 844]]) {
  const at = `${w}x${h}`;
  await resize(w, h);
  await hardGoto(CATALOG);
  // At rest first, which is the half that says the fix moved nothing: the rails still render directly under
  // the search line, in the same place, at the same width.
  //
  // A missing `.subbar` is reported rather than thrown: this measurement is the one that goes away if the
  // rails are put back inside the bar, and a harness that dies on a null rect reports zero assertions, which
  // is a louder failure than the one that actually happened and names none of it.
  const rest = await evalIn(`(() => {
    const subEl = document.querySelector('.subbar');
    if (!subEl) return {missing: true};
    const bar = document.querySelector('.bar').getBoundingClientRect();
    const sub = subEl.getBoundingClientRect();
    const q = document.querySelector('#q').getBoundingClientRect();
    return {seam: Math.round(sub.top - bar.bottom), qTop: Math.round(q.top),
            widths: Math.round(sub.width - bar.width),
            hasRails: !!document.querySelector('.subbar #cats')};
  })()`);
  ok(`the rails sit directly under the search line at rest at ${at}`,
     !rest.missing && Math.abs(rest.seam) <= 1 && Math.abs(rest.widths) <= 1 && rest.hasRails,
     JSON.stringify(rest));

  await evalIn("window.scrollTo(0, 900)");
  await sleep(350);
  const m = await evalIn(`(() => {
    const q = document.querySelector('#q'), qb = q.getBoundingClientRect();
    const head = document.querySelector('header').getBoundingClientRect();
    const ox = Math.max(0, Math.min(qb.right, head.right) - Math.max(qb.left, head.left));
    const oy = Math.max(0, Math.min(qb.bottom, head.bottom) - Math.max(qb.top, head.top));
    const el = document.elementFromPoint(Math.round(qb.left + qb.width / 2),
                                         Math.round(qb.top + qb.height / 2));
    // Everything still pinned at the top edge once the page has moved. Before JFH-354 this was two boxes.
    const stuck = [...document.querySelectorAll('header,.bar,.subbar')]
      .filter(e => getComputedStyle(e).position === 'sticky' &&
                   Math.round(e.getBoundingClientRect().top) <= 0.5);
    document.activeElement && document.activeElement.blur();
    return {vh: window.innerHeight, scrolled: Math.round(window.scrollY),
            x: Math.round(qb.left + qb.width / 2), y: Math.round(qb.top + qb.height / 2),
            coveredPct: Math.round((ox * oy) / (qb.width * qb.height) * 100),
            hits: el ? (el.id ? '#' + el.id : el.tagName.toLowerCase()) : null,
            pinnedPx: Math.round(stuck.reduce((n, e) => n + e.getBoundingClientRect().height, 0)),
            pinned: stuck.map(e => e.id || e.className || e.tagName.toLowerCase()).join(","),
            headerGone: Math.round(head.bottom) <= 0};
  })()`);
  ok(`the page actually scrolled and the masthead left with it at ${at}`,
     m.scrolled > 0 && m.headerGone, JSON.stringify(m));
  ok(`nothing covers the search box once the page has scrolled at ${at}`,
     m.coveredPct === 0 && m.hits === "#q", JSON.stringify(m));
  // 64 / 91 / 106 / 165px measured at the four sizes above, against viewports of 900 / 800 / 900 / 844: 7,
  // 11, 12 and 20%. The budget is a quarter, which the widest case clears by a factor of three and the phone
  // by a fifth -- generous on purpose, because the number to catch is the 51-to-86% this replaced and a floor
  // tightened to today's measurement reddens on the next chip somebody adds to the bar.
  ok(`the pinned band leaves the results most of the screen at ${at}`,
     m.pinnedPx > 0 && m.pinnedPx <= m.vh / BUDGET,
     `${m.pinnedPx}px of ${m.vh} (${Math.round(m.pinnedPx / m.vh * 100)}%), pinned: ${m.pinned}`);
  await S("Input.dispatchMouseEvent", {type: "mousePressed", x: m.x, y: m.y, button: "left", clickCount: 1});
  await S("Input.dispatchMouseEvent", {type: "mouseReleased", x: m.x, y: m.y, button: "left", clickCount: 1});
  await sleep(120);
  const landed = await evalIn("document.activeElement && document.activeElement.id");
  ok(`clicking where the search box is drawn puts the cursor in it at ${at}`, landed === "q", String(landed));
  if (w === 1440 || w === 390) await shot(`scrolled-bar-${at}`);
  await evalIn("window.scrollTo(0, 0)");
}

// ---- WHERE FOCUS LANDS WHEN THE PAGE SCROLLS ITSELF (JFH-356) -------------------------------------------
//
// The block above proves nothing covers the search box. This one asks the same question about every OTHER
// control, and the reason it is a separate question is that the browser, not the reader, chooses the scroll
// position. Moving focus scrolls the focused element into view, and it only leaves room for a pinned bar if
// the element carries `scroll-margin-top`. Before JFH-356 exactly one selector did -- `#out tr` -- and a `tr`
// has no `tabindex` (see the note at the clearance helper above), so the rule protected the one element a
// reader cannot tab to and nothing they can. The one handler that focuses a row passes `preventScroll`, so it
// did not bind there either.
//
// WHY THE FORWARD DIRECTION CANNOT FIND THIS. Tabbing forward down a document aligns the new element to the
// BOTTOM edge of the viewport, where nothing is pinned; a 60-stop forward walk at four widths found nothing
// at all. Shift+Tab scrolls upward and aligns to the TOP edge, which is exactly where the bar is. So this
// walks backwards, and it dispatches real key events -- `Input.dispatchKeyEvent` -- because sequential focus
// navigation is the thing being measured and `el.focus()` does not reproduce its alignment.
//
// The instrument is the one JFH-354 settled on: the fraction of the focused box under the pinned bar, plus
// `document.elementFromPoint` at the box's own centre, because a rect test cannot see a painted-over element.
const focusAt = `(() => {
  const el = document.activeElement;
  if (!el || el === document.body || el === document.documentElement) return {none: true};
  const bar = document.querySelector('.bar');
  const b = el.getBoundingClientRect();
  // The bar cannot obscure its own contents -- an element inside it overlaps its container by construction,
  // which read as "100% covered" for every control in the search line and invented six failures.
  const inBar = bar.contains(el);
  const r = bar.getBoundingClientRect();
  const ox = Math.max(0, Math.min(b.right, r.right) - Math.max(b.left, r.left));
  const oy = Math.max(0, Math.min(b.bottom, r.bottom) - Math.max(b.top, r.top));
  const area = b.width * b.height;
  const cx = Math.round(b.left + b.width / 2), cy = Math.round(b.top + b.height / 2);
  const at = (cy >= 0 && cy <= innerHeight && cx >= 0 && cx <= innerWidth)
    ? document.elementFromPoint(cx, cy) : null;
  return {name: el.id ? '#' + el.id : el.tagName.toLowerCase() +
            (typeof el.className === 'string' && el.className.trim()
              ? '.' + el.className.trim().split(/\\s+/)[0] : ''),
          inBar, inResults: !!el.closest('#out'),
          hiddenPct: inBar || !area ? 0 : Math.round(ox * oy / area * 100),
          reachable: inBar || (!!at && (at === el || el.contains(at) || at.contains(el))),
          aboveViewport: b.bottom <= 0,
          smt: getComputedStyle(el).scrollMarginTop,
          topmost: at ? (at.id ? '#' + at.id : at.tagName.toLowerCase()) : null};
})()`;
const tabKey = async (shift) => {
  for (const type of ["rawKeyDown", "keyUp"])
    await S("Input.dispatchKeyEvent", {type, key: "Tab", code: "Tab", windowsVirtualKeyCode: 9,
                                       nativeVirtualKeyCode: 9, modifiers: shift ? 8 : 0});
};
// Measured: the view is NOT persisted -- a reload comes back in cards, and `#view` is a toggle. So this is
// one click in practice. It is still written as "click until the page agrees" rather than "click once if the
// view is table", because a toggle plus an assumption about the starting state is how a sweep silently
// measures one view twice, and the alternative costs one property read.
const setView = async (want) => {
  for (let i = 0; i < 3; i++) {
    if (await evalIn("document.documentElement.dataset.view") === want) return true;
    await evalIn("document.getElementById('view').click()");
    await sleep(300);
  }
  return await evalIn("document.documentElement.dataset.view") === want;
};

// ASSERT THE RELATIONSHIP, NOT THE NUMBER. `--pin` has to be at least as tall as the pinned bar, and the bar
// is a wrapping flex line whose height is a step function of the width and of the text in it -- `#view` and
// `#take` relabel between the views, which moves the wrap points. The original 172px came from four round
// widths in one view and was already 19px short at 320px in the default view. A test that asserts 224 learns
// nothing when somebody adds a control to the search line; this one reddens.
//
// AND IT DID, ON A RUNNER THAT IS NOT THIS ONE. The step function is a function of the *rendered* text, so it
// is a function of the fonts installed. Windows measured 217px worst case at 320px in table view; CI's
// Chromium wraps one line further and reads 269px, which a 224px token does not clear. The heights below are
// printed rather than kept only in a failure detail, because the two tiers are chosen off them and a number
// nobody can see gets re-derived from whichever machine last looked.
const bands = [];
for (const view of ["cards", "table"]) {
  for (const [w, h] of [[1440, 900], [1024, 800], [768, 900], [390, 844], [320, 844]]) {
    const at = `${w}x${h} in ${view} view`;
    await resize(w, h);
    await hardGoto(CATALOG);
    if (!await setView(view)) { ok(`the page can be put into ${view} view at ${w}x${h}`, false); continue; }
    // Measured while genuinely stuck: unscrolled the bar sits in flow under the masthead and reads short.
    await evalIn("window.scrollTo(0, 3000)");
    await sleep(300);
    const band = await evalIn(`(() => {
      const bar = document.querySelector('.bar').getBoundingClientRect();
      const pin = getComputedStyle(document.documentElement).getPropertyValue('--pin').trim();
      return {barH: Math.round(bar.height), barTop: Math.round(bar.top), pin,
              pinPx: parseFloat(pin), smtRow: getComputedStyle(
                document.querySelector('#out tbody tr')).scrollMarginTop};
    })()`);
    ok(`the scroll margin clears the pinned bar at ${at}`,
       band.pinPx > 0 && band.barH > 0 && band.pinPx >= band.barH, JSON.stringify(band));
    // ...and the token is what the rules actually use, so the number above is not measured off a dead value.
    ok(`...and a results row uses that token at ${at}`,
       parseFloat(band.smtRow) === band.pinPx, JSON.stringify(band));
    bands.push({w, view, barH: band.barH, pinPx: band.pinPx});
    await evalIn("window.scrollTo(0, 0)");
  }
}
{
  const most = (rows) => rows.length ? Math.max(...rows.map(r => r.barH)) : 0;
  const narrow = bands.filter(b => b.w <= 640), wide = bands.filter(b => b.w > 640);
  console.log(`  the pinned bar is at most ${most(narrow)}px at 640px and below (--pin ` +
              `${narrow[0] ? narrow[0].pinPx : "?"}px) and ${most(wide)}px above it (--pin ` +
              `${wide[0] ? wide[0].pinPx : "?"}px)  ·  ` +
              bands.map(b => `${b.w}${b.view[0]}:${b.barH}`).join(" "));
}

// The walk itself, at the two widths that failed hardest before the fix (20 of 30 reverse stops at 1024x800,
// and at 390x844 the row's own name link, repo link, Save and Compare) and in both views.
for (const view of ["cards", "table"]) {
  for (const [w, h] of [[1024, 800], [390, 844]]) {
    const at = `${w}x${h} in ${view} view`;
    await resize(w, h);
    await hardGoto(CATALOG);
    if (!await setView(view)) { ok(`the page can be put into ${view} view at ${w}x${h}`, false); continue; }
    await evalIn("window.scrollTo(0, 0)");
    // WALK IN BY STRUCTURE, NOT BY A KEYSTROKE COUNT. This used to Tab a fixed 58 times at 1024 and 34 at
    // 390, tuned until focus was inside `#out`. 58 put it exactly two stops in, so the walk had one result
    // element to report -- and the first ingest to reveal the New chip added one control to the bar, moved
    // the boundary by one, and left the reverse walk with zero. The assertion that fired was the vacuity
    // guard, which is the right assertion firing for a reason that is nothing to do with focus or the bar:
    // a constant tuned against one build's chrome is a constant that expires the next time a chip appears.
    // So walk until the page says focus is in the results, then six stops further, which is what makes the
    // reverse walk below cross the boundary with a dozen stops left over on the other side of it.
    const DEEP = 6;
    let inside = 0;
    for (let i = 0; i < 200 && inside < DEEP; i++) {
      await tabKey(false);
      await sleep(30);
      if (await evalIn("!!(document.activeElement && document.activeElement.closest('#out'))")) inside++;
    }
    ok(`tabbing forward reaches the results at ${at}`, inside === DEEP, `${inside} of ${DEEP} stops inside`);
    await sleep(200);
    const stops = [];
    for (let i = 0; i < 18; i++) {
      await tabKey(true);
      await sleep(55);
      const f = await evalIn(focusAt);
      if (!f.none) stops.push(f);
    }
    const buried = stops.filter(s => s.hiddenPct >= 25 || !s.reachable || s.aboveViewport);
    // The vacuity guard. A walk that focused nothing, or never left the chrome, would report zero failures
    // for the wrong reason -- and that is the one shape this cannot otherwise distinguish from a pass.
    ok(`tabbing backwards visits real controls at ${at}`,
       stops.length >= 12 && stops.some(s => s.inResults) && stops.some(s => !s.inBar),
       `${stops.length} stops, ${stops.filter(s => s.inResults).length} in the results`);
    ok(`nothing keyboard focus lands on hides under the pinned bar at ${at}`, buried.length === 0,
       buried.slice(0, 4).map(s => `${s.name} ${s.hiddenPct}% under, topmost ${s.topmost}, smt ${s.smt}`)
         .join(" | "));
    if (buried.length) await shot(`focus-under-bar-${w}x${h}-${view}`);
    await evalIn("window.scrollTo(0, 0)");
  }
}

// The skip link is the same defect in the place it costs most: it is the first keystroke a keyboard or
// screen-reader guest makes, and `#out` is not focusable, so the browser scrolls to it without focusing it.
// Its focus behaviour was always right -- the next Tab lands on the first row's name link -- so what is
// asserted here is the landing position: the rows the link exists to show are not under the bar.
for (const [w, h] of [[1440, 900], [390, 844]]) {
  const at = `${w}x${h}`;
  await resize(w, h);
  await hardGoto(CATALOG);
  await evalIn("window.scrollTo(0, 0)");
  await tabKey(false);
  await sleep(150);
  const first = await evalIn(focusAt);
  ok(`the first tab stop is the skip link at ${at}`, first.name === "a.skip", JSON.stringify(first));
  await S("Input.dispatchKeyEvent", {type: "rawKeyDown", key: "Enter", code: "Enter",
                                     windowsVirtualKeyCode: 13, nativeVirtualKeyCode: 13});
  await S("Input.dispatchKeyEvent", {type: "keyUp", key: "Enter", code: "Enter",
                                     windowsVirtualKeyCode: 13, nativeVirtualKeyCode: 13});
  await sleep(500);
  const land = await evalIn(`(() => {
    const r = document.querySelector('.bar').getBoundingClientRect();
    const rows = [...document.querySelectorAll('#out tbody tr')];
    const touched = rows.filter(x => { const b = x.getBoundingClientRect();
      return b.top < r.bottom && b.bottom > r.top; });
    const b0 = rows[0].getBoundingClientRect();
    const at = document.elementFromPoint(Math.round(b0.left + 60), Math.round(b0.top + b0.height / 2));
    return {hash: location.hash, scrolled: Math.round(scrollY), rows: rows.length,
            touched: touched.length, firstTop: Math.round(b0.top), barBottom: Math.round(r.bottom),
            over: at ? (at.id ? '#' + at.id : at.tagName.toLowerCase() +
              (typeof at.className === 'string' && at.className.trim()
                ? '.' + at.className.trim().split(/\\s+/)[0] : '')) : null};
  })()`);
  ok(`"Skip to results" actually moves the page at ${at}`,
     land.hash === "#out" && land.scrolled > 0, JSON.stringify(land));
  ok(`...and lands with no result row under the bar at ${at}`, land.touched === 0, JSON.stringify(land));
  ok(`...so what is drawn over the first row is the first row at ${at}`,
     land.over !== "div.bar", JSON.stringify(land));
  await evalIn("window.scrollTo(0, 0)");
}

// The deliberate exclusion, stated as an assertion because a positive one passes either way. The bar is
// pinned, so its own controls are always visible and have nothing to clear -- and a scroll margin on `#q`
// would make focusing the search box jump a scrolled page to the top.
await resize(1440, 900);
await hardGoto(CATALOG);
const excluded = await evalIn(`(() => {
  const g = (s) => { const e = document.querySelector(s);
    return e ? parseFloat(getComputedStyle(e).scrollMarginTop) : null; };
  return {q: g('#q'), sort: g('#sort'), take: g('#take'),
          rowLink: g('#out tbody tr a'), rowSave: g('#out tbody tr .save'), sub: g('.subbar .chip')};
})()`);
ok("the controls inside the pinned bar are left without a scroll margin",
   excluded.q === 0 && excluded.sort === 0 && excluded.take === 0, JSON.stringify(excluded));
ok("...while the ones outside it have one", excluded.rowLink > 0 && excluded.rowSave > 0 && excluded.sub > 0,
   JSON.stringify(excluded));

// ---- DISCOVER'S CAROUSEL, WHICH IS A SCROLLER AND NOT A TRANSFORMED TRACK -------------------------------
//
// `docs/discover/` is the one page on this site whose primary control is horizontal, and everything worth
// asserting about it is geometry: whether a rail of fifty 320px cards scrolls inside its own box or drags
// the document sideways, whether a phone gets one card and a sliver of the next, whether the grid toggle
// reflows the same fifty into columns, and whether the arrows and the buttons move by a screenful.
//
// probe.mjs has the other half -- that the markup the stage wrote is the markup the page's own renderer
// produces -- and neither harness can do the other's job: a string comparison cannot tell you a rail
// overflows its phone, and a browser cannot tell you two renderers disagree about an apostrophe.
//
// The auto-advance is checked in both directions, and that is the expensive part of this section: the
// interval is six seconds, so proving it runs costs seven and proving it stays off under
// `prefers-reduced-motion` costs seven more. Worth it, because a carousel that advances on its own is the
// single most intrusive thing in this repository and "it is off for readers who asked for no motion" is a
// claim no static check can make.
const DORIGIN = ORIGIN.replace(/\/?$/, "/") + "discover/";
const dSettle = async () => {
  for (let i = 0; i < 100; i++) {
    if (await evalIn("document.readyState === 'complete' && !!document.querySelector('#drail .dcard')"))
      break;
    await sleep(150);
  }
};
// `about:blank` first, for the reason `hardGoto` does it: these navigations differ from each other only by
// fragment, and `Page.navigate` to a URL you are already on with a fragment change is not a load at all --
// which would mean the deep-link assertions below measured a page whose script had never re-run.
const dGoto = async (tail = "") => {
  await S("Page.navigate", {url: "about:blank"});
  await S("Page.navigate", {url: DORIGIN + tail});
  await dSettle();
};
// One read of the rail: how it is laid out, how far it can scroll, and whether the document had to grow
// sideways to contain it. `fullyVisible` is the count a reader would call "on screen" -- a card clipped by
// the rail's right edge is the sliver that says there are more, not a card you can read.
const drail = `(() => {
  const rail = document.getElementById('drail');
  const cards = [...rail.querySelectorAll('.dcard')];
  const rr = rail.getBoundingClientRect(), c0 = cards[0].getBoundingClientRect();
  const across = cards.filter(c => Math.abs(c.getBoundingClientRect().top - c0.top) < 2).length;
  const fully = cards.filter(c => { const b = c.getBoundingClientRect();
    return b.left >= rr.left - 1 && b.right <= rr.right + 1; }).length;
  return {
    cards: cards.length, across, fullyVisible: fully,
    cardW: Math.round(c0.width), railW: Math.round(rr.width),
    scrollW: rail.scrollWidth, clientW: rail.clientWidth, scrollLeft: Math.round(rail.scrollLeft),
    rows: new Set(cards.map(c => Math.round(c.getBoundingClientRect().top))).size,
    snap: getComputedStyle(rail).scrollSnapType,
    railOverflow: getComputedStyle(rail).overflowX,
    docHScroll: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    mode: document.documentElement.getAttribute('data-dmode'),
    pos: (document.getElementById('dpos') || {}).textContent,
    noteShown: !document.getElementById('dnote').hidden,
    note: document.getElementById('dnote').textContent,
    focus: document.activeElement ? (document.activeElement.dataset.project ||
      document.activeElement.id || document.activeElement.tagName.toLowerCase()) : null,
  };
})()`;

await resize(1440, 900);
await dGoto();
const d14 = await evalIn(drail);
ok("the rail is a single horizontal line of cards at 1440px",
   d14.rows === 1 && d14.across === d14.cards, JSON.stringify(d14));
ok("...a full day of them, so this is the page and not an empty shell", d14.cards === 50,
   String(d14.cards));
ok("...scrolling inside its own box rather than dragging the document sideways",
   d14.scrollW > d14.clientW && d14.docHScroll === 0, JSON.stringify(d14));
ok("...with snap points, so a drag lands on a card and not between two",
   /mandatory/.test(d14.snap) && d14.railOverflow === "auto", d14.snap + " / " + d14.railOverflow);
ok("...three or four cards visible at once, which is what a 320px card at this width means",
   d14.fullyVisible >= 3 && d14.fullyVisible <= 5, String(d14.fullyVisible));
ok("...and the counter says where in the fifty the reader is", /^1 of 50$/.test(d14.pos || ""),
   JSON.stringify(d14.pos));

// Next moves by a rail-width, Back undoes it. Measured rather than assumed because `step()` is
// `clientWidth - 40`, and a button that moved by a fixed card count would skip two of them on a phone.
await evalIn("document.getElementById('dnext').click()");
await sleep(600);
const dNext = await evalIn(drail);
ok("Next moves the rail by about a screenful",
   dNext.scrollLeft > d14.clientW * 0.7 && dNext.scrollLeft < d14.clientW * 1.1,
   dNext.scrollLeft + " of " + d14.clientW);
ok("...and the counter moves with it", dNext.pos !== d14.pos, JSON.stringify(dNext.pos));
await evalIn("document.getElementById('dprev').click()");
await sleep(900);
// Not `=== 0`: the rail is `scroll-snap-type:mandatory`, so the final resting position is the snap point
// nearest where the smooth scroll ended, and that is the first card's leading edge give or take the 4px of
// rail padding. A failure here would be a Back button that moved nothing or moved half as far as Next.
const dBack = (await evalIn(drail)).scrollLeft;
ok("Back returns to the beginning", dBack < 8, dBack + " after " + dNext.scrollLeft);

// The arrow keys on the rail itself, and the one thing about the auto-advance that matters more than
// whether it runs: after a reader has touched it, it never starts again. The wait is longer than the
// six-second interval, so a roll that restarted would show up as movement.
await evalIn("document.getElementById('drail').focus()");
for (const key of ["ArrowRight", "ArrowRight"]) {
  await S("Input.dispatchKeyEvent", {type: "rawKeyDown", key, code: key,
                                     windowsVirtualKeyCode: key === "ArrowRight" ? 39 : 37});
  await S("Input.dispatchKeyEvent", {type: "keyUp", key, code: key,
                                     windowsVirtualKeyCode: key === "ArrowRight" ? 39 : 37});
  await sleep(500);
}
await sleep(900);
const dKeys = await evalIn(drail);
ok("ArrowRight on the focused rail scrolls it", dKeys.scrollLeft > 0, String(dKeys.scrollLeft));
await sleep(7200);
const dQuiet = await evalIn(drail);
// A tolerance measured in snap points rather than an equality. Mandatory snapping keeps nudging a rail for
// a little while after a smooth scroll ends -- 31px, on the run that first failed this -- and what the
// assertion is about is a restarted six-second roll, which moves by a screenful and not by a nudge.
ok("...and the carousel does not start rolling again after a keypress",
   Math.abs(dQuiet.scrollLeft - dKeys.scrollLeft) < d14.cardW / 2,
   dKeys.scrollLeft + " then " + dQuiet.scrollLeft + ", a card is " + d14.cardW);

// The roll itself, on a page nobody has touched. This is the assertion the reduced-motion one below is only
// meaningful against: without it, "nothing moved" would pass on a page where nothing ever moves.
await dGoto();
await sleep(7200);
const dRolled = await evalIn(drail);
ok("left alone, the carousel advances on its own", dRolled.scrollLeft > 0, String(dRolled.scrollLeft));

// The New pulse, as this browser computes it rather than as the stylesheet declares it. No row in the
// committed atlas carries a `first_seen` -- the arrivals ledger is written by a CI build -- so the class is
// put on a card here instead of waiting for a day that has one. The class is what the rule selects, so a
// computed `animationName` is the same reading a reader would get on a real arrival.
const pulseOn = await evalIn("(() => { const c = document.querySelector('#drail .dcard');" +
  " c.classList.add('nw'); return getComputedStyle(c).animationName; })()");
ok("a card new to the atlas breathes, on the page as well as on the index", pulseOn === "new-breathe",
   pulseOn);

// `prefers-reduced-motion` is one of the two features CDP can actually override -- see the long note at the
// top of this file about `hover`, which it cannot -- so this is a real emulation and not a proxy for one.
await S("Emulation.setEmulatedMedia",
        {features: [{name: "prefers-reduced-motion", value: "reduce"}]});
await dGoto();
const dCalm0 = await evalIn(drail);
await sleep(7200);
const dCalm = await evalIn(drail);
ok("a reader who asked for no motion gets no carousel that moves on its own",
   dCalm.scrollLeft === dCalm0.scrollLeft, dCalm0.scrollLeft + " then " + dCalm.scrollLeft);
// The same card, the same class, the same property -- and `none` this time. The ring itself is in the base
// rule and stays, which is the point: what is removed is the swell, not the thing it was drawing attention
// to. `boxShadow` is read beside it so a rule that turned the whole badge off could not pass this.
const calmPulse = await evalIn("(() => { const c = document.querySelector('#drail .dcard');" +
  " c.classList.add('nw'); const s = getComputedStyle(c);" +
  " return {animation: s.animationName, shadow: s.boxShadow}; })()");
ok("...and the New pulse is off for them too, on a card whose ring stays",
   calmPulse.animation === "none" && calmPulse.shadow !== "none", JSON.stringify(calmPulse));
ok("...while the rail still scrolls, because nothing here is communicated by the motion",
   dCalm.scrollW > dCalm.clientW && (await evalIn(
     "(() => { const r = document.getElementById('drail'); r.scrollLeft = 500;" +
     " return Math.round(r.scrollLeft); })()")) > 0);
await S("Emulation.setEmulatedMedia", {features: []});

// THE DEEP LINK, which is the whole reason the homepage strip is not a clickthrough grab: a card there links
// to `discover/#repo=<owner/name>`, and landing on it has to deliver that card rather than the top of a
// page with it somewhere inside.
await dGoto();
const pick30 = await evalIn(
  "document.querySelectorAll('#drail .dcard')[29].getAttribute('data-project')");
await dGoto("#repo=" + pick30);
await sleep(700);
const dHit = await evalIn(drail);
ok("a #repo= link scrolls that card to the rail's leading edge", dHit.scrollLeft > 0,
   pick30 + " at " + dHit.scrollLeft);
ok("...and focuses it, so a keyboard reader arrives where a mouse reader is looking",
   dHit.focus === pick30, JSON.stringify(dHit.focus));
ok("...and marks it, so it is still findable after reading two cards either side",
   await evalIn(`!!document.querySelector('.dcard.dhit[data-project="' + CSS.escape(${
     JSON.stringify(pick30)}) + '"]') || !!document.querySelector('.dcard.dhit')`));
ok("...and says nothing, because the card was in today's fifty", !dHit.noteShown, dHit.note);

// A link shared yesterday afternoon. The project is in the plan and not in today's cohort, which is not a
// broken link -- it is a dated one -- so the page says which day it was in and offers the project.
const stale = await evalIn(`(async () => {
  const d = await fetch("../discover.json").then(r => r.json());
  const today = new Set([...document.querySelectorAll('#drail .dcard')].map(c => c.dataset.project));
  for (const c of d.days) for (const n of c.picks) if (!today.has(n)) return n;
  return "";
})()`);
ok("the plan has a project that is not in today's fifty, to follow a stale link to", stale !== "", stale);
if (stale) {
  await dGoto("#repo=" + stale);
  await sleep(700);
  const dStale = await evalIn(drail);
  ok("a link to another day's card says which day it was in rather than scrolling to nothing",
     dStale.noteShown && /fifty, not today's/.test(dStale.note), JSON.stringify(dStale.note));
  ok("...and offers the project itself, which is what the reader was actually after",
     await evalIn("!!document.querySelector('#dnote a[href^=\"../repo/\"]')"));
}

// Grid view: the same fifty cards, the same markup, a different container. The rail buttons go, because
// there is nothing left for them to scroll.
await dGoto();
await evalIn("document.getElementById('dmode').click()");
await sleep(400);
const dGrid = await evalIn(drail);
ok("Grid view reflows the same fifty into rows", dGrid.mode === "grid" && dGrid.cards === 50 &&
   dGrid.rows > 1, JSON.stringify({mode: dGrid.mode, rows: dGrid.rows, cards: dGrid.cards}));
ok("...with nothing left to scroll sideways, in the rail or in the document",
   dGrid.scrollW <= dGrid.clientW + 1 && dGrid.docHScroll === 0, JSON.stringify(dGrid));
ok("...and the two rail buttons gone rather than sitting there inert",
   await evalIn("getComputedStyle(document.getElementById('dnext')).display === 'none'"));
ok("...and the choice remembered, which is what a view toggle is for",
   await evalIn("localStorage.getItem('aaa-dmode')") === "grid");
await evalIn("document.getElementById('dmode').click()");
await sleep(400);
ok("...and reversible", (await evalIn(drail)).mode === "rail");
await evalIn("localStorage.removeItem('aaa-dmode')");

// 390px, where the fixed 320px card would leave no sliver of the next one and a reader would have nothing
// on screen telling them the rail scrolls at all. `min(320px,78vw)` is the answer and this is the check.
await resize(390, 844);
await dGoto();
const dPhone = await evalIn(drail);
ok("a phone gets one card at a time", dPhone.fullyVisible === 1, JSON.stringify(dPhone));
ok("...narrower than the screen, so the next one shows as a sliver",
   dPhone.cardW < 390 - 24 && dPhone.cardW > 200, String(dPhone.cardW));
ok("...and the document still does not scroll sideways", dPhone.docHScroll === 0,
   String(dPhone.docHScroll));
if (dPhone.docHScroll !== 0 || dPhone.fullyVisible !== 1) await shot("discover-390");
await resize(1440, 900);

console.log(`\n${pass} passed, ${fail} failed`);
ws.close();
await browser.close();
process.exit(fail ? 1 : 0);
