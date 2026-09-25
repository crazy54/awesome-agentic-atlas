// Archie's friends: five small characters who drop by the homepage now and then, do one harmless thing to
// it, get told off by Archie, and leave. Imported by `archie.js`, and only once his live model has drawn its
// first frame: so never before the page's `load`, never on a screen narrower than 900 px, never for a reader
// who asked for reduced motion and never without WebGL, because on any of those he stays a poster and this
// file is never asked for. It degrades to nothing, by not being loaded.
//
// WHO THEY ARE is `archie-friends-data.js` (the designer's file: names, personalities and every line). WHAT
// THEY LOOK LIKE AND DO is this file: each is an inline SVG drawn here in the masthead's palette -- the flat
// colours of the brief, a glossy dark outline where one reads better, and the same round, chunky proportions
// as Archie -- animated with the Web Animations API. There is no canvas and no three.js here: a friend is a
// few hundred bytes of SVG, and the model's renderer is busy enough.
//
//  - Nib, the arrow cursor from Archie's cursor prank, escaped and grown legs. Walks along the top of a
//    section heading, lifts one of its letters "for a font", and puts it back.
//  - Posy, a sticky note. Flutters down, sticks a note of her own on the corner of a project card, and
//    peels away; the note curls and drops off a few seconds later.
//  - Lumen, a moth. Drifts over to the Spotlight, lands on its corner and strikes a pose.
//  - Oh-Four, a shy 404 ghost. Peeks over the top edge of the masthead's search button, and ducks if the
//    pointer comes near.
//  - Quack, the rubber-duck debugger. Bobs up beside Archie and asks him one question, which is all it takes
//    for him to find his own bug.
//
// NOTHING ON THE PAGE IS CHANGED. Every friend, prop, bubble, lifted letter and the chip that masks the
// letter's gap is an element of one layer of our own, `.archie-pals`: fixed over the window, clipped to it
// so nobody walking off an edge can give the page a scrollbar, `pointer-events:none`, `aria-hidden`. No
// text node, attribute, style or class of the page's own is written, nothing takes focus, nothing is typed
// into anything, and putting the page back is removing the layer. The one thing a reader can touch is the
// friend itself, a target of 30-odd pixels that is a poke (a line, and it leaves). Any click anywhere else,
// Escape or Tab sends the friend away at once -- a reader who clicks or moves focus is busy, and that is
// the whole rule. A friend on its way out takes no clicks at all.
//
// WHEN. At most one visit per page view, and on only a quarter of page views at all: the dice are rolled
// once, when this loads. A winner waits 20 to 60 seconds (never inside the first 20, which are the page's)
// and then goes the next time Archie is free: at home in the masthead, the masthead on screen, idle, not
// dancing to music, not mid-prank, not in Quiet mode (`atlas-byte-quiet`, which `archie.js` reads and
// passes on). A visit runs about 15 to 20 seconds, because each line is on screen as long as Archie keeps
// his own; that is longer than the five seconds after which moving content must be stoppable (WCAG 2.2.2),
// and it is: any click, Escape or Tab ends it at once. A hard stop at 25 s tears the layer down whatever
// state the choreography is in, so a throttled background tab cannot strand a friend on screen.
// While a friend is visiting, Archie plays no prank.
//
// WHICH. The friend of the day: `ORDER[n % ORDER.length]`, where n is the reader's LOCAL date as days since
// 1970, the same integer the page's daily line rotates on (`window.ATLASDAY.n`, falling back to computing it
// the same way), so the friend changes at the reader's midnight along with the line and not at 7 pm in
// Chicago. On a day the page's daily line is a friend's (`[data-daily][data-friend]`), that friend comes,
// so the text and the sprite agree. If today's friend has nothing to do on screen -- no heading, no card, no
// Spotlight in view -- the next one in ORDER that has goes instead; Quack needs nothing but Archie, so
// somebody always can.
//
// SAFETY. Nothing flashes: no opacity, colour or brightness changes faster than once in 333 ms (WCAG 2.3.1
// allows three flashes a second; the fastest thing here is Lumen's wings at 1.6 beats a second, and that is
// shape, not light). Reduced motion never gets here, and a reader who turns it on mid-visit takes Archie
// down (`archie.js` listens) and this layer with him, through `stop()`. A friend never parks over a link or
// a button for long: they walk past controls rather than stopping on them, Posy's note and the lifted
// letter take no pointer events, and `tests/friends-check.mjs` samples every control on screen through each
// visit to hold them to it. The target of a trick is skipped while the reader is on it -- hovered, focused,
// or holding a text selection inside it.
//
// `?archie=friend:<id>` sends that friend two seconds after the model is up, skipping the dice and the wait
// but through every other gate, so Quiet mode can be checked to stop it.

const V = new URL(import.meta.url).search;
const TRICKS = {nib: "borrow", posy: "note", lumen: "photobomb", "oh-four": "peek", quack: "debug"};
const CHANCE = 0.25;                 // of page views that get a visit at all
const EARLIEST = 20000, LATEST = 60000;
const HARD_STOP = 25000;             // ms from arrival to the layer being gone, whatever else happens

const CSS = String.raw`
.archie-pals{position:fixed;inset:0;overflow:hidden;pointer-events:none;z-index:30;contain:strict}
.archie-pals .inner{position:absolute;left:0;top:0;width:100%;height:100%}
.archie-pals .pal{position:absolute;left:0;top:0;pointer-events:auto;cursor:pointer;
  -webkit-tap-highlight-color:transparent;will-change:transform}
.archie-pals .pal svg,.archie-pals .prop svg{display:block;overflow:visible}
.archie-pals .prop{position:absolute;left:0;top:0;pointer-events:none}
.archie-pals .archie-say{position:absolute;z-index:2}
.archie-pals .note{position:absolute;left:0;top:0;width:68px;min-height:44px;padding:6px 7px 8px;
  box-sizing:border-box;background:#FFF1A6;color:#2B2140;border-radius:2px 2px 10px 2px;
  font:600 11px/1.2 "Segoe Print","Bradley Hand","Comic Sans MS",cursive;
  box-shadow:0 6px 12px rgba(0,0,0,.22);transform-origin:50% 0;pointer-events:none}
.archie-pals .glyph{position:absolute;left:0;top:0;white-space:pre;pointer-events:none}
.archie-pals .mask{position:absolute;left:0;top:0;pointer-events:none;border-radius:3px}
.archie-pals .clip{position:absolute;overflow:hidden;pointer-events:none}
.archie-pals .clip .pal{position:absolute}`;

// ---- The art ----------------------------------------------------------------------------------------
// Each drawing faces right, its origin top left, and is sized in CSS pixels. Parts that move on their own
// (legs, wings, a pencil) are groups with a class, so the choreography can animate them without knowing the
// drawing's insides. Colours are the brief's, as literals rather than theme tokens: a friend is a character,
// and a character does not change colour with the reader's theme. Each has a 1.5-2 px dark or light outline
// so it reads on both themes and on every skin.
const ART = {
  // The arrow is the prank cursor's own path, `M3 2v22l6-6 4 9 4-2-4-9h8z`, so the joke lands for anyone who
  // saw the prank. Legs hang from the arrow's lower edge, which is where its weight would be.
  nib: {w: 30, h: 40, svg: `<svg width="30" height="40" viewBox="0 0 30 40">
    <g class="leg" style="transform-origin:8px 24px"><path d="M8 24v11" stroke="#FF2BD6" stroke-width="2.2" stroke-linecap="round"/><circle cx="9.5" cy="36" r="2.3" fill="#FF2BD6"/></g>
    <g class="leg b" style="transform-origin:13px 20px"><path d="M13 20v15" stroke="#FF2BD6" stroke-width="2.2" stroke-linecap="round"/><circle cx="14.5" cy="36" r="2.3" fill="#FF2BD6"/></g>
    <g class="body"><path d="M3 2v22l6-6 4 9 4-2-4-9h8z" fill="#fff" stroke="#FF2BD6" stroke-width="2" stroke-linejoin="round"/>
    <circle cx="6" cy="10" r="1.3" fill="#111"/><circle cx="9.6" cy="12" r="1.3" fill="#111"/>
    <path d="M5.4 14.4q2 1.8 4 .6" fill="none" stroke="#111" stroke-width="1" stroke-linecap="round"/></g></svg>`},
  // A 44 px square with its bottom-right corner curling up, and a pencil tucked behind the top edge.
  posy: {w: 48, h: 50, svg: `<svg width="48" height="50" viewBox="0 0 48 50">
    <g class="pencil"><rect x="30" y="0" width="5" height="16" rx="1.2" fill="#FF8C42" transform="rotate(28 32 8)"/>
    <rect x="30" y="-3" width="5" height="4" rx="1.4" fill="#FF7FB0" transform="rotate(28 32 8)"/></g>
    <path d="M2 5h44v31L35 47H2z" fill="#FFD84D" stroke="#C99A1E" stroke-width="1.2" stroke-linejoin="round"/>
    <path d="M46 36L35 47l2-9.5z" fill="#E8B92E" stroke="#C99A1E" stroke-width="1.2" stroke-linejoin="round"/>
    <ellipse class="eye" cx="16" cy="22" rx="2.3" ry="3.6" fill="#2B2140"/><ellipse class="eye" cx="28" cy="22" rx="2.3" ry="3.6" fill="#2B2140"/>
    <circle cx="22" cy="32" r="2.4" fill="none" stroke="#2B2140" stroke-width="1.6"/></svg>`},
  // Seen from above, wings open. The wings are two groups that fold towards the body by scaling in x.
  lumen: {w: 40, h: 36, svg: `<svg width="40" height="36" viewBox="0 0 40 36">
    <path d="M17 7q-3-6-8-6M23 7q3-6 8-6" fill="none" stroke="#8A5BFF" stroke-width="1.4" stroke-linecap="round"/>
    <g class="wing l" style="transform-origin:20px 17px"><path d="M19 12Q6 1 2 9q-2 8 12 9 4 0 5-2z" fill="#EDE6FF" stroke="#8A5BFF" stroke-width="1.1"/>
    <path d="M19 19Q7 20 6 28q2 6 10 1 3-3 3-6z" fill="#EDE6FF" stroke="#8A5BFF" stroke-width="1.1"/><circle cx="9" cy="10" r="2.6" fill="#22E1FF"/></g>
    <g class="wing r" style="transform-origin:20px 17px"><path d="M21 12Q34 1 38 9q2 8-12 9-4 0-5-2z" fill="#EDE6FF" stroke="#8A5BFF" stroke-width="1.1"/>
    <path d="M21 19Q33 20 34 28q-2 6-10 1-3-3-3-6z" fill="#EDE6FF" stroke="#8A5BFF" stroke-width="1.1"/><circle cx="31" cy="10" r="2.6" fill="#22E1FF"/></g>
    <ellipse cx="20" cy="18" rx="4.4" ry="10" fill="#C9B8FF" stroke="#8A5BFF" stroke-width="1.1"/>
    <circle cx="17.8" cy="10.5" r="2" fill="#111"/><circle cx="22.2" cy="10.5" r="2" fill="#111"/>
    <circle cx="17.2" cy="9.8" r=".7" fill="#fff"/><circle cx="21.6" cy="9.8" r=".7" fill="#fff"/></svg>`},
  // A sheet with a three-scallop hem, and its error code faint on the forehead.
  "oh-four": {w: 34, h: 38, svg: `<svg width="34" height="38" viewBox="0 0 34 38">
    <path d="M3 17a14 14 0 0 1 28 0v19l-4.7-3.5-4.6 3.5-4.7-3.5-4.7 3.5-4.6-3.5L3 36z" fill="#F4F7FF" stroke="#9AA3B8" stroke-width="1.5" stroke-linejoin="round"/>
    <text x="17" y="10" text-anchor="middle" font-size="5.5" font-family="ui-monospace,Consolas,monospace" fill="#B8C0D0">404</text>
    <ellipse cx="12.5" cy="17" rx="2.4" ry="3.3" fill="#1A1A2E"/><ellipse cx="21.5" cy="17" rx="2.4" ry="3.3" fill="#1A1A2E"/>
    <path d="M14.5 24q2.5-1.6 5 0" fill="none" stroke="#1A1A2E" stroke-width="1.1" stroke-linecap="round"/></svg>`},
  // The classic bath duck, side on, with its badge on a lanyard.
  quack: {w: 40, h: 36, svg: `<svg width="40" height="36" viewBox="0 0 40 36">
    <path d="M6 20q0-6 8-6h6q-4-4-4-8a8 8 0 0 1 16 0q0 4-3 7 8 1 8 11 0 10-15 10H14Q6 34 6 26z" fill="#FFD23F" stroke="#B8860B" stroke-width="1.3" stroke-linejoin="round"/>
    <path d="M31 7q5-1 7 1-2 3-7 2z" fill="#FF8C42" stroke="#C0601E" stroke-width="1" stroke-linejoin="round"/>
    <circle cx="27" cy="5.5" r="1.8" fill="#111"/><circle cx="26.4" cy="4.9" r=".6" fill="#fff"/>
    <path d="M14 21q5 5 11 1" fill="none" stroke="#B8860B" stroke-width="1.2" stroke-linecap="round"/>
    <path d="M21 12.5l1 8" stroke="#22E1FF" stroke-width="1"/><rect x="18" y="20" width="9" height="5" rx="1" fill="#22E1FF"/>
    <text x="22.5" y="23.8" text-anchor="middle" font-size="3.2" font-weight="700" font-family="system-ui,sans-serif" fill="#0B2530">DEBUG</text></svg>`},
};

// ---- Helpers ------------------------------------------------------------------------------------------
const ABORT = Symbol("abort");
const rnd = a => a[Math.floor(Math.random() * a.length)];
const onScreen = (r, pad = 0) => r.width > 0 && r.top >= pad && r.bottom <= innerHeight - pad &&
  r.left >= 0 && r.right <= document.documentElement.clientWidth;
// Is the reader on this element: pointer over it, focus in it, or a selection in it? Then it is not ours.
const busyWith = el => {
  if (!el || el.matches(":hover")) return true;
  const a = document.activeElement;
  if (a && a !== document.body && el.contains(a)) return true;
  const s = getSelection();
  return !!(s && s.rangeCount && !s.isCollapsed && el.contains(s.getRangeAt(0).commonAncestorContainer));
};
// The colour a masking chip must be to hide a glyph: the first opaque background up the tree. Null when
// something between the heading and that colour is see-through or drawn -- a translucent panel (Glass,
// Sherbet and Aurora's are about 80% opaque), a gradient wash or a grid -- because a flat chip over any of
// those shows as a rectangle, not as a gap; Nib picks another heading, or stays home.
const backdrop = el => {
  for (let e = el; e && e.nodeType === 1; e = e.parentElement) {
    const cs = getComputedStyle(e);
    if (cs.backgroundImage && cs.backgroundImage !== "none") return null;
    const c = cs.backgroundColor, m = c && c.match(/rgba?\(([^)]*)\)/);
    const alpha = !c || c === "transparent" ? 0 : m ? (m[1].split(/[\s,\/]+/).filter(Boolean)[3] ?? 1) : 1;
    if (+alpha === 0) continue;
    return +alpha >= 1 ? c : null;
  }
  return getComputedStyle(document.body).backgroundColor || "#fff";
};
// The reader's local date as days since 1970, the page's own `ATLASDAY.n` when it has one.
const today = () => {
  const n = window.ATLASDAY && Number(window.ATLASDAY.n);
  if (Number.isFinite(n)) return n;
  const d = new Date();
  return Math.round(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()) / 864e5);
};

// ---- Targets ------------------------------------------------------------------------------------------
// What each friend's trick needs on screen, found at the moment of the visit, or null if it has nothing.
const TARGETS = {
  // A section heading, fully in view, with a letter to lift that is neither the first nor a space. The letter
  // is measured with a Range, so the lifted copy lands exactly on it. A heading that is itself a link (the
  // Spotlight's) only if there is no other: Nib should not stand on something a reader might click.
  nib() {
    const hs = [...document.querySelectorAll("main h2")];
    const plain = h => !h.closest("a") && !h.querySelector("a");
    for (const h of [...hs.filter(plain), ...hs.filter(h => !plain(h))]) {
      const r = h.getBoundingClientRect();
      if (!onScreen(r, 60) || busyWith(h)) continue;
      const walker = document.createTreeWalker(h, NodeFilter.SHOW_TEXT);
      const t = walker.nextNode();
      if (!t) continue;
      const s = t.textContent, idx = [];
      for (let i = 1; i < s.length; i++) if (/[A-Za-z]/.test(s[i])) idx.push(i);
      if (idx.length < 2) continue;
      const i = rnd(idx.slice(0, 6));
      const range = document.createRange();
      range.setStart(t, i); range.setEnd(t, i + 1);
      const lr = range.getBoundingClientRect();
      if (!lr.width) continue;
      const chip = backdrop(t.parentElement);
      if (!chip) continue;
      return {el: h, rect: r, letter: s[i], lr, parent: t.parentElement, chip};
    }
    return null;
  },
  // The top-right corner of a project card, or of the Spotlight if no card is fully on screen.
  posy() {
    for (const el of [...document.querySelectorAll("main .cx"), document.querySelector("main .hero")]) {
      if (!el) continue;
      const r = el.getBoundingClientRect();
      if (r.top >= 70 && r.top <= innerHeight - 120 && r.right <= document.documentElement.clientWidth - 20 &&
          r.right > 120 && !busyWith(el)) return {el, rect: r};
    }
    return null;
  },
  // The Spotlight's top-left corner.
  lumen() {
    const el = document.querySelector("main .hero");
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return r.top >= 60 && r.top <= innerHeight - 100 && r.left >= 20 && !busyWith(el) ? {el, rect: r} : null;
  },
  // The masthead's "Search and filter" button, the homepage's nearest thing to a search box. He peeks over
  // its top edge from behind it, and only ever above it.
  "oh-four"() {
    const el = document.querySelector("header a.cta");
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return r.top >= 50 && onScreen(r) && !busyWith(el) ? {el, rect: r} : null;
  },
  // Beside Archie, on the masthead's bottom edge.
  quack(o) {
    const s = o.slot.getBoundingClientRect(), h = o.header.getBoundingClientRect();
    return h.bottom > 120 && h.bottom < innerHeight ? {rect: s, floor: h.bottom} : null;
  },
};

// ---- The visit ----------------------------------------------------------------------------------------
// `o` is what `archie.js` hands over: the header and his slot, `say(line)` to speak in his bubble, and
// `free()`, true when he is at home, idle and not otherwise engaged (Quiet mode included).
export function friends(o) {
  let FRIENDS = null, ORDER = [], layer = null, busy = false, visited = false, timer = 0, stopped = false;
  let finish = null;                           // tears the current visit down: see `visit()`
  let guest = null;                            // Archie's answer to a poke while a friend is over
  const asked = new URLSearchParams(location.search).get("archie") || "";
  const forced = asked.startsWith("friend:") ? asked.slice(7) : "";
  const lucky = forced || Math.random() < CHANCE;

  const style = document.createElement("style");
  style.textContent = CSS;

  const plan = ms => { clearTimeout(timer); if (!stopped && !visited) timer = setTimeout(tryVisit, ms); };
  const tryVisit = () => {
    if (stopped || visited) return;
    if (!FRIENDS || document.hidden || !o.free()) return plan(3000);
    const who = choose();
    if (!who) return plan(5000);
    visit(who.id, who.target);
  };
  const choose = () => {
    const ids = ORDER.filter(id => FRIENDS[id] && ART[id]);
    if (!ids.length) return null;
    const pick = id => { const target = TARGETS[id](o); return target ? {id, target} : null; };
    if (forced) return ids.includes(forced) ? pick(forced) : null;
    const daily = document.querySelector("[data-daily][data-friend]");
    const first = daily && ids.includes(daily.dataset.friend) ? daily.dataset.friend : ids[today() % ids.length];
    const start = ids.indexOf(first);
    for (let k = 0; k < ids.length; k++) { const w = pick(ids[(start + k) % ids.length]); if (w) return w; }
    return null;
  };

  if (lucky) import(`./archie-friends-data.js${V}`).then(m => {
    FRIENDS = m.FRIENDS; ORDER = m.ORDER || Object.keys(m.FRIENDS);
    plan(forced ? 2000 : EARLIEST + Math.random() * (LATEST - EARLIEST));
  }).catch(e => console.warn("Archie's friends stayed home:", e));

  async function visit(id, target) {
    visited = busy = true;
    const F = FRIENDS[id], lines = F.lines || {}, trick = TRICKS[id];
    // A friend on their favourite skin (`likes`) says so instead of their usual hello, half the time: Quack's
    // favourite is Graphite, the default, and the joke would wear thin.
    const fan = document.documentElement.dataset.skin === F.likes && Math.random() < 0.5;
    const line = k => {
      if (k === "arrive" && fan && lines.skin) k = "skin";
      return lines[k] && lines[k].length ? rnd(lines[k]) : null;
    };
    guest = () => line("poke");
    document.head.appendChild(style);
    layer = document.createElement("div");
    layer.className = "archie-pals";
    layer.setAttribute("aria-hidden", "true");
    layer.dataset.friend = id;
    const inner = document.createElement("div");
    inner.className = "inner";
    layer.appendChild(inner);
    document.body.appendChild(layer);

    // Everything below is placed in window coordinates as they were when the visit began; the inner layer
    // is scrolled with the page, so a friend stays on the heading or card it came for.
    const y0 = scrollY, x0 = scrollX;
    const follow = () => { inner.style.translate = `${x0 - scrollX}px ${y0 - scrollY}px`; };
    addEventListener("scroll", follow, {passive: true});

    let dead = false;
    const anims = new Set();
    const go = (el, frames, opts) => {
      const a = el.animate(frames, {fill: "forwards", easing: "ease-in-out", ...opts});
      anims.add(a);
      return a;
    };
    // Waits for an animation or a time, then checks the visit is still on: an abort anywhere unwinds the
    // whole choreography from its next step.
    const step = async p => {
      try { await (typeof p === "number" ? new Promise(r => setTimeout(r, p)) : p.finished); }
      catch { /* cancelled */ }
      if (dead) throw ABORT;
    };
    const el = (cls, html, parent = inner) => {
      const e = document.createElement("div");
      e.className = cls;
      if (html) e.innerHTML = html;
      parent.appendChild(e);
      return e;
    };
    const art = ART[id];
    const pal = el("pal", art.svg);
    pal.style.width = art.w + "px"; pal.style.height = art.h + "px";
    const at = (e, x, y, extra = "") => `translate(${Math.round(x)}px,${Math.round(y)}px)${extra}`;
    // The friend's own bubble, in Archie's style (his `.archie-say` rule is on the page while he is live).
    const bubble = document.createElement("p");
    bubble.className = "archie-say";
    inner.appendChild(bubble);
    // A line stays up as long as Archie keeps his own: 2 s plus 55 ms a character, at most 6.5 s. `hold()`
    // waits out whatever of that is left (and at least `ms`), so the next line never replaces one that is
    // still being read; `read(l)` is the same sum for a line of Archie's, whose bubble keeps its own clock.
    let hideBubble = 0, shownUntil = 0;
    const read = l => l ? Math.min(6500, 2000 + 55 * l[0].length) : 0;
    const hold = (ms = 0) => step(Math.max(ms, shownUntil - performance.now()));
    const speak = (l, x, y) => {
      if (!l) return;
      bubble.textContent = l[0];
      bubble.classList.toggle("think", !!l[1]);
      const w = Math.min(220, bubble.offsetWidth || 160), h = bubble.offsetHeight || 34;
      const left = x + 10 + w > document.documentElement.clientWidth - 8;
      bubble.classList.toggle("l", left);
      bubble.style.translate = `${Math.round(left ? x - 10 - w : x + 10)}px ${Math.round(Math.max(4, y - 14 - h))}px`;
      bubble.classList.add("on");
      clearTimeout(hideBubble);
      shownUntil = performance.now() + read(l);
      hideBubble = setTimeout(() => bubble.classList.remove("on"), read(l));
    };
    const archie = k => { const l = line(k); if (l) o.say(l); return l; };
    // On the way out a friend stops being a target at once: a fading or departing friend that still took
    // clicks would be an invisible patch of page that swallows the reader's.
    const exit = () => { pal.style.pointerEvents = "none"; };

    // Teardown, one way out for every ending: done, poked, dismissed, the hard stop, or Archie stopping.
    const hard = setTimeout(() => finish && finish(), HARD_STOP);
    // Tab counts as a click: a keyboard reader moving focus is busy, and focus must never land under a friend.
    const dismiss = e => {
      if (e.type === "keydown" && e.key !== "Escape" && e.key !== "Tab") return;
      if (!pal.contains(e.target)) leaveNow();
    };
    addEventListener("pointerdown", dismiss, {capture: true, passive: true});
    addEventListener("keydown", dismiss, {capture: true, passive: true});
    let leaving = false;
    const leaveNow = () => {
      if (leaving || dead) return;
      leaving = true;
      dead = true;
      exit();
      for (const a of anims) a.pause();
      layer.animate([{opacity: 1}, {opacity: 0}], {duration: 350, fill: "forwards"}).finished
        .then(() => finish && finish(), () => finish && finish());
    };
    // Poked, the friend says goodbye and goes, and Archie apologises for them.
    pal.addEventListener("pointerdown", () => {
      if (leaving) return;
      const r = pal.getBoundingClientRect();
      speak(line("leave"), r.left + r.width / 2, r.top);
      archie("poke");
      leaving = true; dead = true;
      exit();
      for (const a of anims) a.pause();
      setTimeout(() => layer && layer.animate([{opacity: 1}, {opacity: 0}], {duration: 350, fill: "forwards"})
        .finished.then(() => finish && finish(), () => finish && finish()), 1200);
    });
    finish = () => {
      finish = null; dead = true;
      clearTimeout(hard); clearTimeout(hideBubble);
      removeEventListener("scroll", follow);
      removeEventListener("pointerdown", dismiss, {capture: true});
      removeEventListener("keydown", dismiss, {capture: true});
      for (const a of anims) a.cancel();
      anims.clear();
      layer.remove(); style.remove();
      layer = null;
      busy = false; guest = null;
    };

    try { await SHOWS[id]({o, F, target, pal, art, go, step, hold, read, exit, el, at, speak, archie, line, trick, inner}); }
    catch (e) { if (e !== ABORT) console.warn("Archie's friend tripped:", e); }
    if (finish && !leaving) finish();
  }

  return {
    get busy() { return busy; },
    // What Archie says when he is poked mid-visit, instead of his usual reply: "Shh, Quack's thinking."
    poke() { return busy && guest ? guest() : null; },
    stop() {
      stopped = true;
      clearTimeout(timer);
      if (finish) finish();
    },
  };
}

// ---- The shows ----------------------------------------------------------------------------------------
// Each is one visit: arrive, the trick, Archie's line, the friend's last word, leave. Every position is in
// window pixels; `at(e, x, y)` makes the transform. Every line is up for as long as Archie keeps his own
// (2 s plus 55 ms a character, at most 6.5 s): `hold()` waits a friend's line out before the next one
// replaces it, and `hold(read(l))` waits out one of Archie's, which he says in his own bubble while the
// friend's is still up. `exit()` comes before every departure, so a friend on the way out takes no clicks.
const W = () => document.documentElement.clientWidth;
const SHOWS = {
  async nib({target, pal, art, go, step, hold, read, exit, el, at, speak, archie, line, trick}) {
    const {lr, rect, letter, parent, chip} = target;
    // Feet (the drawing's bottom two pixels are the round of the feet) on the heading's cap line, which is
    // about a fifth of the way down the letter's line box.
    const floor = Math.round(lr.top + lr.height * 0.2 - art.h + 2);
    const stop = lr.left - art.w + 8;              // standing on the letters before it
    // A walk: the body bobs and leans, the legs scissor, at a little over two steps a second.
    const legs = pal.querySelectorAll(".leg");
    const walk = () => [
      go(legs[0], [{rotate: "-24deg"}, {rotate: "24deg"}], {duration: 220, iterations: Infinity, direction: "alternate"}),
      go(legs[1], [{rotate: "24deg"}, {rotate: "-24deg"}], {duration: 220, iterations: Infinity, direction: "alternate"}),
    ];
    let steps = walk();
    await step(go(pal, [{transform: at(pal, -40, floor, " rotate(10deg)")}, {transform: at(pal, stop, floor, " rotate(10deg)")}],
                  {duration: Math.max(900, (stop + 40) * 3.2), easing: "linear"}));
    steps.forEach(a => a.cancel());
    go(pal, [{transform: at(pal, stop, floor, " rotate(10deg)")}, {transform: at(pal, stop, floor)}], {duration: 160});
    speak(line("arrive"), stop + art.w / 2, floor);
    await hold();
    // The lift: a chip the colour of the heading's background hides the letter, and a copy of it, in the
    // heading's own font, rises twelve pixels into Nib's arms.
    const cs = getComputedStyle(parent);
    const mask = el("mask");
    mask.style.cssText = `width:${Math.ceil(lr.width) + 2}px;height:${Math.ceil(lr.height)}px;` +
      `transform:translate(${Math.floor(lr.left) - 1}px,${Math.floor(lr.top)}px);background:${chip}`;
    const g = el("glyph");
    g.textContent = letter;
    g.style.cssText = `font:${cs.font};color:${cs.color};letter-spacing:${cs.letterSpacing};line-height:${lr.height}px;` +
      `height:${lr.height}px;transform:translate(${lr.left}px,${lr.top}px)`;
    const up = [{transform: `translate(${lr.left}px,${lr.top}px)`}, {transform: `translate(${lr.left - 6}px,${lr.top - 14}px) rotate(-12deg)`}];
    go(g, up, {duration: 450, easing: "cubic-bezier(.34,1.56,.64,1)"});
    await step(go(pal, [{transform: at(pal, stop, floor)}, {transform: at(pal, stop - 6, floor - 4, " rotate(-6deg)")}], {duration: 450}));
    speak(line(trick), stop + art.w / 2, floor - 4);
    await step(1400);
    await hold(read(archie(`${trick}-archie`)));
    // Back it goes, and the chip with it: the page's own letter was there all along.
    await step(go(g, up.slice().reverse(), {duration: 380, easing: "cubic-bezier(.5,0,.75,0)"}));
    mask.remove(); g.remove();
    await step(go(pal, [{transform: at(pal, stop - 6, floor - 4, " rotate(-6deg)")}, {transform: at(pal, stop, floor)}], {duration: 200}));
    speak(line(`${trick}-after`), stop + art.w / 2, floor);
    await hold();
    // Off the right edge, with a hop at the end of the heading.
    exit();
    steps = walk();
    const end = W() + 40;
    await step(go(pal, [{transform: at(pal, stop, floor, " rotate(10deg)")},
                        {transform: at(pal, rect.right + 8, floor, " rotate(10deg)"), offset: 0.55},
                        {transform: at(pal, rect.right + 40, floor - 26, " rotate(20deg)"), offset: 0.7},
                        {transform: at(pal, end, floor + 30, " rotate(30deg)")}],
                  {duration: 1600, easing: "linear"}));
  },

  async posy({F, target, pal, art, go, step, hold, read, exit, el, at, speak, archie, line, trick}) {
    const r = target.rect;
    const x = r.right - art.w - 18, y = r.top - art.h + 10;    // perched on the card's top edge, near its corner
    // Down like a leaf: side to side, tipping into each swing.
    await step(go(pal, [{transform: at(pal, x + 30, -60, " rotate(14deg)")},
                        {transform: at(pal, x - 26, y * 0.33, " rotate(-12deg)")},
                        {transform: at(pal, x + 22, y * 0.66, " rotate(10deg)")},
                        {transform: at(pal, x, y, " rotate(0deg)")}], {duration: 2300, easing: "ease-out"}));
    speak(line("arrive"), x + art.w / 2, y);
    await hold();
    // The note: pressed onto the card's corner with a squash, tilted, one of her own texts.
    await step(go(pal, [{transform: at(pal, x, y)}, {transform: at(pal, x, y + 6, " scale(1.08,.9)")}, {transform: at(pal, x, y)}], {duration: 380}));
    const note = el("note");
    const text = F.notes && F.notes.length ? rnd(F.notes) : ["Hi!"];
    note.textContent = text[0];
    const nx = r.right - 78, ny = r.top + 10;
    go(note, [{transform: `translate(${nx}px,${ny}px) rotate(-3deg) scale(.6)`, opacity: 0},
              {transform: `translate(${nx}px,${ny}px) rotate(-3deg) scale(1)`, opacity: 1}],
       {duration: 380, easing: "cubic-bezier(.34,1.56,.64,1)"});
    speak(line(trick), x + art.w / 2, y);
    await step(1500);
    await hold(read(archie(`${trick}-archie`)));
    speak(line(`${trick}-after`), x + art.w / 2, y);
    await hold();
    // She peels away up and out; the note stays a moment longer, curls, and drops off the card.
    exit();
    go(pal, [{transform: at(pal, x, y), opacity: 1}, {transform: at(pal, x + 70, y - 140, " rotate(40deg) scale(.8)"), opacity: 0}],
       {duration: 1600, easing: "ease-in"});
    await step(2200);
    await step(go(note, [{transform: `translate(${nx}px,${ny}px) rotate(-3deg)`, opacity: 1},
                         {transform: `translate(${nx + 6}px,${ny + 8}px) rotate(8deg) scale(.96,.9)`, opacity: 1, offset: 0.35},
                         {transform: `translate(${nx + 14}px,${ny + 70}px) rotate(24deg) scale(.9,.8)`, opacity: 0}],
                  {duration: 900, easing: "ease-in"}));
  },

  async lumen({target, pal, art, go, step, hold, read, exit, speak, archie, line, trick, at}) {
    const r = target.rect;
    const x = r.left - art.w / 2 + 4, y = r.top - art.h / 2 - 2;       // on the Spotlight's corner
    const wings = pal.querySelectorAll(".wing");
    // 1.6 beats a second, well under the 3 Hz line, and a change of shape, not of brightness.
    const flap = () => [...wings].map(w => go(w, [{scale: "1 1"}, {scale: ".3 1"}],
      {duration: 310, iterations: Infinity, direction: "alternate", easing: "ease-in-out"}));
    let beat = flap();
    const sx = W() + 40, sy = y - 90;
    const path = [];
    for (let i = 0; i <= 8; i++) {
      const f = i / 8;
      path.push({transform: at(pal, sx + (x - sx) * f, sy + (y - sy) * f + Math.sin(f * Math.PI * 3) * 28 * (1 - f),
                               ` rotate(${Math.round(Math.cos(f * Math.PI * 3) * 14 * (1 - f))}deg)`)});
    }
    await step(go(pal, path, {duration: 2800, easing: "ease-out"}));
    beat.forEach(a => a.cancel());
    speak(line("arrive"), x + art.w / 2, y);
    await hold();
    // The pose: wings wide, a little tilt, held.
    wings.forEach(w => go(w, [{scale: "1 1"}, {scale: "1.18 1.05"}], {duration: 260}));
    await step(go(pal, [{transform: at(pal, x, y)}, {transform: at(pal, x, y, " rotate(-10deg) scale(1.1)")}], {duration: 300}));
    speak(line(trick), x + art.w / 2, y);
    await step(1500);
    await hold(read(archie(`${trick}-archie`)));
    speak(line(`${trick}-after`), x + art.w / 2, y);
    await hold();
    // A spiral up and out of the window.
    exit();
    beat = flap();
    const out = [];
    for (let i = 0; i <= 10; i++) {
      const f = i / 10, a = f * Math.PI * 3;
      out.push({transform: at(pal, x + Math.sin(a) * 40 * (1 - f * 0.4) + f * 60, y - f * (y + 80) - (1 - Math.cos(a)) * 10,
                              ` rotate(${Math.round(Math.cos(a) * 20)}deg)`)});
    }
    await step(go(pal, out, {duration: 2000, easing: "ease-in"}));
  },

  // Behind the button: the ghost sits in a clip whose bottom edge is the button's top, so however he rises,
  // not a pixel of him can land on the button or its label.
  async "oh-four"({target, pal, art, go, step, hold, read, exit, el, speak, archie, line, trick}) {
    const r = target.rect;
    const clip = el("clip");
    const cx = Math.round(r.right - art.w - 22), cy = Math.round(r.top - art.h);
    clip.style.cssText = `left:${cx}px;top:${cy}px;width:${art.w}px;height:${art.h}px`;
    clip.appendChild(pal);
    const HIDE = `translateY(${art.h + 2}px)`, PEEK = `translateY(${Math.round(art.h * 0.42)}px)`, UP = "translateY(2px)";
    let near = false, shown = PEEK;
    const move = e => {
      const dx = Math.max(r.left - e.clientX, 0, e.clientX - r.right), dy = Math.max(cy - e.clientY, 0, e.clientY - r.bottom);
      const was = near;
      near = Math.hypot(dx, dy) < 120;
      if (near && !was) exit(), go(pal, [{transform: shown}, {transform: HIDE}], {duration: 160, easing: "ease-in"});
    };
    addEventListener("pointermove", move, {passive: true});
    try {
      await step(go(pal, [{transform: HIDE}, {transform: PEEK}], {duration: 900, easing: "ease-out"}));
      if (near) return;
      speak(line("arrive"), cx + art.w / 2, cy + art.h * 0.42);
      await hold();
      if (near) return;
      // A little braver: all the way up to the rim, bobbing two pixels.
      shown = UP;
      await step(go(pal, [{transform: PEEK}, {transform: UP}], {duration: 500, easing: "ease-out"}));
      go(pal, [{transform: UP}, {transform: "translateY(0px)"}], {duration: 700, iterations: 4, direction: "alternate"});
      speak(line(trick), cx + art.w / 2, cy);
      await step(1500);
      if (near) return;
      await hold(read(archie(`${trick}-archie`)));
      if (near) return;
      speak(line(`${trick}-after`), cx + art.w / 2, cy);
      await hold();
      exit();
      await step(go(pal, [{transform: UP}, {transform: HIDE}], {duration: 800, easing: "ease-in"}));
    } finally {
      removeEventListener("pointermove", move);
      if (near) await new Promise(res => setTimeout(res, 500));
    }
  },

  async quack({o, F, target, pal, art, go, step, hold, read, exit, speak, archie, line, trick, at}) {
    const s = target.rect;
    const x = s.right - 40, y = target.floor - art.h + 6;      // at Archie's feet, on the masthead's edge
    const bob = () => go(pal.firstElementChild, [{transform: "translateY(0) rotate(-4deg)"}, {transform: "translateY(-3px) rotate(4deg)"}],
                         {duration: 600, iterations: Infinity, direction: "alternate"});
    let b = bob();
    await step(go(pal, [{transform: at(pal, W() + 30, y)}, {transform: at(pal, x, y)}], {duration: 2400, easing: "ease-out"}));
    speak(line("arrive"), x + art.w / 2, y);
    await hold();
    speak(line(trick), x + art.w / 2, y);
    await step(1200);
    // His explanation and his realisation, paired by index, so the fix answers the bug he described.
    const i = Math.floor(Math.random() * (F.lines["debug-archie"] || []).length);
    const a = [(F.lines["debug-archie"] || [])[i], (F.lines["debug-archie-2"] || [])[i]];
    if (a[0]) o.say(a[0]);
    await hold(read(a[0]));
    if (a[1]) o.say(a[1]);
    await step(read(a[1]));
    speak(line(`${trick}-after`), x + art.w / 2, y);
    await hold();
    exit();
    await step(go(pal, [{transform: at(pal, x, y)}, {transform: at(pal, W() + 30, y)}], {duration: 2000, easing: "ease-in"}));
    b.cancel();
  },
};
