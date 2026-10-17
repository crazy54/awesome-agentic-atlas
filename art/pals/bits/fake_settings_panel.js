// The fake settings panel. Brick stands guard under the theme switch (the Settings button on home and the
// catalogue, the theme chip elsewhere), arms folded. Archie climbs up from behind the page, sizes up the switch
// and Brick, and produces a remote control: aimed. Brick holds out his hand. Archie hands it over, and Brick
// folds his arms again. Archie backs off, sulking -- and Zip pops up and produces another remote. The standoff:
// Zip aims it, Brick stares, a tumbleweed rolls by, Archie begs him not to. Brick's hand comes out again; Zip
// hands it over too. The two of them point up at the switch for the reader (you do it), and Brick raises a
// brow. The switch is never pressed and the page never changes: the remotes are pictures. Clips:
// fake_settings_panel.py (the layout and timings below are its constants).
({
  cast: ["archie", "zip", "brick"],
  pages: ["home", "topic", "catalog"],
  // The switch, the floor under it (the spotlight's top edge on home, else the header's bottom) and the
  // size that puts the switch SW_Z (3.3 m) above that floor, clear over Brick's head.
  layout(s) {
    const vis = q => { const r = s.page.rect(q); return r && r.width > 0 && r.height > 0 ? r : null; };
    const sw = vis("#setbtn") || vis("#theme");
    if (!sw) return null;
    const hero = vis("article.hero"), head = vis("header");
    const below = r => r && r.top > sw.bottom + 50 ? r.top : null;
    const floor = below(hero) || (head && head.bottom > sw.bottom + 50 ? head.bottom : null);
    if (!floor) return null;
    const ppm = (floor - (sw.top + sw.height / 2)) / 3.3;
    return ppm >= 28 && ppm <= 60 ? {sw, floor, ppm, cx: sw.left + sw.width / 2} : null;
  },
  ready(s) {
    const L = this.layout(s);
    if (!L) return false;
    return L.sw.top > 0 && L.floor < innerHeight - 4 && L.cx + 1.4 * L.ppm < document.documentElement.clientWidth &&
      L.cx - 3.6 * L.ppm > 0;
  },
  async play(s) {
    const {archie: A, zip: Z, brick: B} = s;
    const L = this.layout(s);
    if (!L) return;
    const {floor, ppm: P, cx} = L;
    const AX = -2.1, ABACK = -3.0, ZX = -1.85, REMOTE_S = 4.5, PRODUCE_AT = 0.35, HANDOFF_AT = 1.55;
    const TAKE_HIDE = 1.0, HOP_RISE = 0.45;                      // ... and _moves.HOP_RISE
    for (const a of [A, Z, B]) a.ppm = P;
    const [ra, rz] = await Promise.all([s.prop("remote"), s.prop("remote-zip")]);
    if (!s.alive) return;
    const n = piece => `fake-settings-panel/${piece}`;
    // a remote into his left hand, out of sight until he produces it; and, handed over, into Brick's right,
    // kept just where it is
    const inHand = (r, who) => { r.hold(who, "grip_L"); r.root.scale.setScalar(REMOTE_S); r.root.visible = false; };
    const toBrick = r => {
      const b = B.bone("grip_R");
      B.model.updateMatrixWorld(true);
      r.root.parent.updateMatrixWorld(true);
      b.attach(r.root);
    };
    // up from behind the page's edge, and back down
    const rise = async (a, x) => {
      a.clipBelow(floor);
      a.at(x, floor + 3 * P).show(true);
      const hop = a.perform(n("hop-up"), {fade: 0});
      await s.tween(HOP_RISE, u => a.at(x, floor + 3 * P * (1 - u)), u => 1 - (1 - u) * (1 - u));
      if (!s.alive) return;
      a.clipBelow(null);
      await hop;
    };
    const sink = async a => {
      a.clipBelow(floor);
      const x = a.x;
      await s.tween(0.4, u => a.at(x, floor + 3 * P * u), u => u * u);
      if (!s.alive) return;
      a.show(false);
    };
    // the hand-over: Brick's hand out from under his folded arms, the giver's into it, and back under
    const confiscate = async (who, r) => {
      await B.perform(n("palm-out"));
      if (!s.alive) return;
      B.play(n("palm-hold"), {loop: true});
      await s.after(0.7);
      if (!s.alive) return;
      const giving = who.perform(n("hand-over"));
      await s.until(() => who.time() >= HANDOFF_AT || !s.alive);
      if (!s.alive) return;
      toBrick(r);
      await s.after(0.15);
      if (!s.alive) return;
      const take = B.perform(n("take"));
      s.after(TAKE_HIDE).then(() => { r.root.visible = false; });   // put away
      await giving;
      if (!s.alive) return;
      who.play("idle", {loop: true});
      await take;
      if (!s.alive) return;
      B.play("guard-hold", {loop: true});
    };
    // a tumbleweed across the foreground
    const tumbleweed = async () => {
      const g = s.svg.el("g", {opacity: 0}), r = 0.32 * P;
      for (const [rx, ry, a] of [[1, 0.8, 0], [0.85, 1, 40], [0.95, 0.7, 100], [0.6, 0.75, 150]]) {
        s.svg.el("ellipse", {cx: 0, cy: 0, rx: r * rx, ry: r * ry, transform: `rotate(${a})`, fill: "none",
                             stroke: "#a5773f", "stroke-width": 1.6}, g);
      }
      for (let i = 0; i < 6; i++) {
        const a = i * 1.05, b = a + 2.2;
        s.svg.el("line", {x1: r * 0.8 * Math.cos(a), y1: r * 0.8 * Math.sin(a), x2: r * 0.7 * Math.cos(b),
                          y2: r * 0.7 * Math.sin(b), stroke: "#8a6232", "stroke-width": 1.2}, g);
      }
      const x0 = cx - 4.6 * P, x1 = cx + 1.6 * P;
      await s.tween(2.4, u => {
      if (!s.alive) return;
        const x = x0 + (x1 - x0) * u, hop = Math.abs(Math.sin(u * Math.PI * 3)) * 0.35 * P;
        g.setAttribute("transform", `translate(${x},${floor - r - hop}) rotate(${(x - x0) / r * 57.3})`);
        g.setAttribute("opacity", Math.min(1, u * 6, (1 - u) * 6));
      }, u => u);
      g.remove();
    };

    // ---- Brick on guard; Archie up, sizing it up ----
    B.at(cx, floor).show(true);
    B.play("guard-hold", {loop: true});
    await s.after(0.8);
    if (!s.alive) return;
    await rise(A, cx + AX * P);
    if (!s.alive) return;
    A.play("idle", {loop: true});
    await A.perform(n("case"));
    if (!s.alive) return;

    // ---- the remote ----
    inHand(ra, A);
    const draw = A.perform(n("produce"));
    await s.after(PRODUCE_AT);
    if (!s.alive) return;
    ra.root.visible = true;
    await draw;
    if (!s.alive) return;
    A.play(n("aim"), {loop: true});
    A.say("Heh.", 1.0);
    await s.after(0.6);
    if (!s.alive) return;
    await confiscate(A, ra);
    if (!s.alive) return;

    // ---- Archie backs off; Zip comes up with another ----
    await A.perform(n("sulk"));
    if (!s.alive) return;
    await A.walkTo(cx + ABACK * P, {speed: 0.8});
    if (!s.alive) return;
    await A.face(0);
    if (!s.alive) return;
    A.play("idle", {loop: true});
    await rise(Z, cx + ZX * P);
    if (!s.alive) return;
    Z.play("idle", {loop: true});
    Z.say("Psst!", 1.0);
    await Z.perform(n("psst"));
    if (!s.alive) return;
    inHand(rz, Z);
    const draw2 = Z.perform(n("produce"));
    await s.after(PRODUCE_AT);
    if (!s.alive) return;
    rz.root.visible = true;
    await draw2;
    if (!s.alive) return;
    Z.play(n("aim"), {loop: true});

    // ---- the standoff ----
    B.play(n("stare"), {loop: true, fade: 0.4});
    const tw = tumbleweed();
    await s.after(1.6);
    if (!s.alive) return;
    A.say("Don't!", 1.0);
    await A.perform(n("dont"));
    if (!s.alive) return;
    A.play("idle", {loop: true});
    await tw;
    if (!s.alive) return;
    await confiscate(Z, rz);
    if (!s.alive) return;

    // ---- you do it; Brick, at the reader; and down they go ----
    A.perform(n("please")).then(() => s.alive && A.play("idle", {loop: true}));
    await s.after(0.2);
    Z.perform(n("please")).then(() => s.alive && Z.play("idle", {loop: true}));
    await s.after(1.2);
    if (!s.alive) return;
    await B.perform(n("brow"));
    if (!s.alive) return;
    B.play("guard-hold", {loop: true});
    await Promise.all([sink(A), s.after(0.15).then(() => s.alive && sink(Z))]);
    if (!s.alive) return;
    await s.after(0.6);
  },
})
