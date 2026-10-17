// The scroll treadmill. On the index's shelves of cards (the `.rowscroll` rows the reader scrolls sideways,
// with the arrows or a swipe), Archie drops onto the top edge of a row. When the reader scrolls it, the cards
// run under his feet and he jogs to keep up -- flat out, the faster they go, and carried along when they
// outrun him. When they stop he puffs, and eggs the reader on. Carried near the row's end, he grabs the card
// passing under him, sits on it, and rides it out of sight, waving. It waits for its moment: the reader
// scrolling a row (`cue`), or, picked like any other bit, a row on screen, and then he asks for it.
// Clips: scroll_treadmill.py. The row is only ever read (its position and scrollLeft), never scrolled.
({
  cast: ["archie"],
  pages: ["home"],
  ppm: 48,
  // The moment: a row scrolled by the reader, a good way (a card's width or more within a second and a half).
  cue(page, go) {
    let row = null, from = 0, at = 0;
    document.addEventListener("scroll", e => {
      const el = e.target;
      if (!(el instanceof Element) || !el.matches(".rowscroll")) return;
      if (el !== row || e.timeStamp - at > 1500) { row = el; from = el.scrollLeft; at = e.timeStamp; }
      if (Math.abs(el.scrollLeft - from) > 280) {
        this.row = el;
        this.dir = Math.sign(el.scrollLeft - from);        // +1: the cards running left
        row = null;
        go();
      }
    }, {capture: true, passive: true});
  },
  ready(s) {
    return !!this.pick();
  },
  // The row he stands on: the one the reader scrolled, if it's still in view with room above it for him; else
  // any that is.
  pick() {
    const fits = el => {
      const r = el.getBoundingClientRect();
      return r.width >= 700 && r.top >= 2.6 * this.ppm + 70 && r.top <= innerHeight - 120 && el.scrollWidth > r.width;
    };
    if (this.row && this.row.isConnected && fits(this.row)) return this.row;
    return [...document.querySelectorAll(".rowscroll")].find(fits) || null;
  },
  async play(s) {
    const A = s.archie, ppm = A.ppm;
    const row = this.pick();
    if (!row) return;
    const JOG = 0.55 / (0.42 * 0.48), FAST = 4, LAND = 0.35;   // scroll_treadmill.py
    const R = () => row.getBoundingClientRect();
    const sec = row.closest("[data-sh]");
    const nav = sec && sec.querySelector(".nav");
    // the cards' top edge, and how far along he may stand: clear of the row's ends, and of its arrows
    const floor = () => R().top + 4;
    const lo = () => R().left + 0.6 * ppm;
    const hi = () => Math.min(R().right - 0.6 * ppm, nav ? nav.getBoundingClientRect().left - 0.7 * ppm : 1e9);
    let dir = this.dir || 1;
    let x = dir > 0 ? lo() + (hi() - lo()) * 0.8 : lo() + (hi() - lo()) * 0.2;

    // ---- the belt: how fast the cards are running under him, px a second (+: to the right) ----
    let last = row.scrollLeft, v = 0, belt = 0, quiet = 0;
    s.tick(dt => {
      const sl = row.scrollLeft;
      if (dt > 0) v = -(sl - last) / dt;
      last = sl;
      belt += (v - belt) * Math.min(1, dt * 14);             // smoothed a little: a scroll comes in uneven steps
      quiet = Math.abs(belt) < 25 ? quiet + dt : 0;
    });

    // ---- down onto the row ----
    A.at(x, floor() - 3 * ppm).show(true);
    await A.face(0);
    const landing = A.perform("scroll-treadmill/land");
    const y0 = floor() - 3 * ppm;
    await s.tween(LAND, e => A.at(x, y0 + (floor() - y0) * e), u => u * u);
    s.tick(() => A.at(x, floor()));                          // and on it, wherever the page puts the row
    await landing;
    if (!s.alive) return;

    // ---- the treadmill ----
    let runs = 0, riding = false, egged = false;
    // egging the reader on: not waited for, so the cards moving cut it short
    const egg = text => {
      A.face(0);
      A.say(text, 1.6);
      A.perform("scroll-treadmill/egg");
    };
    if (Math.abs(belt) < 25) egg("Go on — scroll it.");
    for (let waited = 0; s.alive && !riding;) {
      if (Math.abs(belt) < 25) {
        // standing: wait for the cards to move; ask once more; then give up
        if (waited > 8) break;
        await s.after(0.25);
        waited += 0.25;
        if (runs && waited > 2.6 && !egged) { egged = true; egg("Again!"); }
        continue;
      }
      A.hush();
      waited = 0;
      runs++;
      // jog against the cards, as fast as they run; when they outrun him, they carry him
      dir = -Math.sign(belt);
      A.face(dir);                                           // (not waited for: he turns as he goes)
      const jog = A.play("scroll-treadmill/jog", {loop: true, fade: 0.1});
      const off = s.tick(dt => {
        const want = Math.abs(belt) / (JOG * ppm);
        if (jog) jog.timeScale = Math.max(0.6, Math.min(FAST, want));
        const keep = Math.min(Math.abs(belt), FAST * JOG * ppm);
        x += (belt + dir * keep) * dt;
        x = Math.max(lo() - 0.3 * ppm, Math.min(hi() + 0.3 * ppm, x));
        if (x <= lo() || x >= hi()) riding = true;           // at the row's end: the next card that passes
      });
      await s.until(() => quiet > 0.35 || riding || !s.alive);
      off();
      if (jog) jog.timeScale = 1;
      if (!s.alive) return;
      if (riding) break;
      if (runs >= 2) { riding = true; break; }               // twice is enough: next time, he hitches a ride
      await A.face(0);
      A.play("scroll-treadmill/pant", {loop: true, fade: 0.25});
      await s.after(1.8);
      if (!s.alive) return;
      A.play("idle", {loop: true, fade: 0.3});
    }
    if (!s.alive) return;

    if (!riding) {
      // nobody scrolled: a shrug, and he walks off the nearer end of the row, out of sight behind it
      await A.face(0);
      await A.perform("shrug");
      if (!s.alive) return;
      const toLeft = x - R().left < R().right - x;
      toLeft ? A.clipLeft(R().left) : A.clipRight(R().right);
      await A.walkTo(toLeft ? R().left - 0.8 * ppm : R().right + 0.8 * ppm);
      return;
    }

    // ---- the ride: onto the card under him, and off the end of the row with it ----
    const card = [...row.children].find(c => { const r = c.getBoundingClientRect(); return r.left <= x && r.right >= x; });
    if (!card) return;
    const dx = x - card.getBoundingClientRect().left;
    await A.face(0);
    s.tick(() => { x = card.getBoundingClientRect().left + dx; });
    await A.perform("scroll-treadmill/hop-on");
    if (!s.alive) return;
    A.play("scroll-treadmill/ride", {loop: true, fade: 0.1});
    A.clipLeft(R().left);
    A.clipRight(R().right);
    A.say("Wheee!", 1.4);
    // until the card has carried him out of the row; if the reader stops, a wave, and he rides on with the
    // next scroll -- or, left long enough, he waves goodbye where he sits and the bit ends there
    await s.until(() => x < R().left - 0.5 * ppm || x > R().right + 0.5 * ppm || quiet > 6 || !s.alive);
    if (!s.alive) return;
    if (x >= R().left - 0.5 * ppm && x <= R().right + 0.5 * ppm) {
      await A.perform("scroll-treadmill/bye");
    }
  },
})
