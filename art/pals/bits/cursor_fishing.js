// Cursor fishing. Zip, up on the top edge of the home page's spotlight, spots the reader's pointer below him
// on the card, gets out a fishing rod and lowers a horseshoe magnet towards it. It snaps onto the pointer,
// and the pointer is stronger than he is: he is dragged along the edge, heels skidding, until he heaves;
// the magnet springs free and clangs onto his own horn, and he sits down hard. The reader's pointer is never
// touched: the bit only reads where it is (and follows it, if it moves), from the stage's `pointer()`; the
// line and the magnet are drawn over the page. Clips: cursor_fishing.py.
({
  cast: ["zip"],
  pages: ["home"],
  ppm: 72,
  _side(r, p, ppm) {
    const need = 3.9 * ppm;
    if (p.x - r.left > need) return 1;
    if (r.right - p.x > need) return -1;
    return 0;
  },
  ready(s) {
    const r = s.page.rect("article.hero"), p = s.pointer();
    if (!r || !p.seen || r.width < 800 || r.top < 140 || r.top > innerHeight - 260) return false;
    if (p.y < r.top + 60 || p.y > innerHeight - 30 || p.x < r.left || p.x > r.right) return false;
    return !!this._side(r, p, this.ppm);
  },
  async play(s) {
    // where the reader's mouse pointer is, followed as it moves: read, never moved, never drawn
    const Z = s.zip, ppm = Z.ppm, T = s.T, P = {};
    const look = () => Object.assign(P, s.pointer());
    look();
    s.tick(look);
    const ROD = 0.75, FREE = 0.42, CLANG = 0.95;            // cursor_fishing.py
    const H = () => s.page.rect("article.hero");
    const edge = H().top, dir = this._side(H(), P, ppm) || 1;
    const x0 = P.x - dir * 3.4 * ppm;
    const rod = await s.prop("fishing-rod");
    if (!s.alive) return;
    s.page.undo(() => rod.remove());
    // the rod's own line and magnet are folded away: the page draws a line that reaches
    const line1 = rod.model.getObjectByName("line_1");
    if (line1) line1.scale.setScalar(1e-4);
    const v = new T.Vector3();
    const tip = () => { if (!line1) return Z.pageAt("grip_R"); line1.getWorldPosition(v); return {x: v.x, y: -v.y}; };

    // ---- the line and the magnet, drawn over the page ----
    const line = s.svg.el("path", {fill: "none", stroke: "#2b2a29", "stroke-width": 1.6, "stroke-linecap": "round", opacity: 0});
    const m = 0.11 * ppm;                                  // the magnet's half-width
    const magnet = s.svg.el("g", {opacity: 0});
    // drawn with the top of its bend at its origin, where the line ties on, and its poles POLE below
    const POLE = m * 2.85;
    s.svg.el("path", {d: `M ${-m} ${m * 2.3} L ${-m} ${m} A ${m} ${m} 0 0 1 ${m} ${m} L ${m} ${m * 2.3}`, fill: "none",
                      stroke: "#d8322a", "stroke-width": m * 0.62, "stroke-linecap": "butt"}, magnet);
    s.svg.el("rect", {x: -m * 1.31, y: m * 2.1, width: m * 0.62, height: m * 0.75, fill: "#c9ccd2"}, magnet);
    s.svg.el("rect", {x: m * 0.69, y: m * 2.1, width: m * 0.62, height: m * 0.75, fill: "#c9ccd2"}, magnet);
    s.svg.el("path", {d: `M ${-m * 0.55} ${m * 0.38} q ${m * 0.55} ${-m * 0.3} ${m * 1.1} 0`, fill: "none", stroke: "#fff",
                      "stroke-width": 1.2, opacity: 0.6}, magnet);
    // the magnet: where its bend is (the line ties on there), the way its poles point (radians, 0 = down)
    const mag = {x: 0, y: 0, ang: 0, slack: 0.3, line: false};
    let stuck = null, onHorn = false;
    const draw = s.tick(() => {
      if (stuck) { mag.x = stuck().x; mag.y = stuck().y; }
      const t = tip();
      magnet.setAttribute("transform", `translate(${mag.x.toFixed(1)} ${mag.y.toFixed(1)}) rotate(${(-mag.ang * 180 / Math.PI).toFixed(1)})`);
      if (!mag.line) { line.setAttribute("opacity", 0); return; }
      const mx = (t.x + mag.x) / 2, my = (t.y + mag.y) / 2 + mag.slack * Math.hypot(mag.x - t.x, mag.y - t.y) * 0.25;
      line.setAttribute("d", `M ${t.x.toFixed(1)} ${t.y.toFixed(1)} Q ${mx.toFixed(1)} ${my.toFixed(1)} ${mag.x.toFixed(1)} ${mag.y.toFixed(1)}`);
      line.setAttribute("opacity", 1);
    });
    // the magnet's bend, for its poles touching the pointer's tip
    const onPointer = () => ({x: P.x - Math.sin(mag.ang) * POLE, y: P.y - Math.cos(mag.ang) * POLE});

    // ---- along the edge, and there it is ----
    Z.at(dir > 0 ? Math.max(H().left - 0.6 * ppm, x0 - 4 * ppm) : Math.min(H().right + 0.6 * ppm, x0 + 4 * ppm), edge).show(true);
    Z.play("idle", {loop: true});
    await Z.walkTo(x0);
    if (!s.alive) return;
    await Z.face(dir);
    await Z.perform("cursor-fishing/spot");
    if (!s.alive) return;

    // ---- the cast ----
    const cast = Z.perform("cursor-fishing/cast");
    await s.after(ROD);
    rod.hold(Z, "grip_R");
    await cast;
    if (!s.alive) return;
    Z.play("cursor-fishing/fish", {loop: true});
    let t0 = tip();
    mag.x = t0.x; mag.y = t0.y + 0.3 * ppm; mag.line = true;
    magnet.setAttribute("opacity", 1);
    // lowered, swinging a little, down to the pointer's height
    let depth = 0.3 * ppm;
    const target = () => P.y - 0.15 * ppm - tip().y;
    const swing = s.tick(() => {
      const t = tip(), k = s.clock();
      mag.x = t.x + 0.12 * ppm * Math.sin(k * 2.4);
      mag.y = t.y + depth;
      mag.ang = 0.12 * Math.sin(k * 2.4 + 0.6);
    });
    await s.tween(2.6, u => { depth = 0.3 * ppm + (target() - 0.3 * ppm) * u; }, u => u);
    if (!s.alive) return;
    await s.after(0.9);
    // it feels the pull: leans, creeps ... SNAP
    swing();
    const from = {x: mag.x, y: mag.y};
    const aim = Math.atan2(P.x - from.x, P.y - from.y);
    await s.tween(0.6, u => { mag.ang = aim * u * 0.6; mag.x = from.x + dir * 0.1 * ppm * u; });
    const at0 = {x: mag.x, y: mag.y, a: mag.ang};
    await s.tween(0.16, u => {
      mag.ang = at0.a + (aim - at0.a) * u;
      const q = onPointer();
      mag.x = at0.x + (q.x - at0.x) * u; mag.y = at0.y + (q.y - at0.y) * u;
      mag.slack = 0.3 * (1 - u);
    }, u => u * u);
    stuck = onPointer;
    if (!s.alive) return;

    // ---- the pull: he is dragged along the edge towards it ----
    Z.say("!!", 0.8);
    await Z.perform("cursor-fishing/bite");
    if (!s.alive) return;
    Z.play("cursor-fishing/drag", {loop: true});
    const reel = s.tick(() => { mag.ang = Math.atan2(P.x - tip().x, P.y - tip().y); });
    const stop = P.x - dir * 1.25 * ppm;
    let speed = 0;
    await new Promise(res => {
      const off = s.tick(dt => {
        speed = Math.min(1.6, speed + dt * 1.2);
        const jerk = 1 + 0.6 * Math.sin(s.clock() * 14);
        Z.x += dir * speed * jerk * ppm * dt;
        if (dir * (stop - Z.x) <= 0 || !s.alive) { Z.x = stop; off(); res(); }
      });
    });
    if (!s.alive) return;
    await s.after(0.4);

    // ---- the heave: the magnet lets go, flies back, clang ----
    const yank = Z.perform("cursor-fishing/yank");
    await s.after(FREE);
    if (!s.alive) return;
    reel();
    stuck = null;
    // the rod goes flying out of his hands, back over his shoulder and off the edge
    const rp = tip();
    rod.detach();
    rod.at(rp.x, rp.y, ppm);
    const r0 = {x: rp.x, y: rp.y};
    mag.line = false;
    s.tween(1.0, u => {
      rod.root.position.set(r0.x - dir * 2.2 * ppm * u, -(r0.y - 1.2 * ppm * Math.sin(Math.PI * u * 0.8) + 3.2 * ppm * u * u), 0);
      rod.root.rotation.z = dir * 6 * u;
    }, u => u).then(() => rod.remove());
    const f0 = {x: mag.x, y: mag.y};
    // on top of his left horn's tip (past horn_2's head by most of the way again), poles down on it
    const horn = () => {
      const a = Z.pageAt("horn_1_L"), b = Z.pageAt("horn_2_L");
      return {x: b.x + 0.8 * (b.x - a.x), y: b.y + 0.8 * (b.y - a.y) - POLE};
    };
    await s.tween(CLANG - FREE, u => {
      const h = horn();
      mag.x = f0.x + (h.x - f0.x) * u;
      mag.y = f0.y + (h.y - f0.y) * u - 0.8 * ppm * Math.sin(Math.PI * u);
      mag.ang = Math.PI * 2 * u;                           // a turn in the air, and down poles first
    }, u => u);
    stuck = horn;
    onHorn = true;
    await yank;
    if (!s.alive) return;
    Z.say("clang.", 1.0);
    await Z.perform("cursor-fishing/up");
    if (!s.alive) return;
    // off, the magnet still stuck to his horn, the way he came
    await Z.walkTo(dir > 0 ? -1.0 * ppm : innerWidth + 1.0 * ppm);
    draw();
  },
})
