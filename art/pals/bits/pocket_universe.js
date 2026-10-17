// Pocket universe, wrong pocket. Archie can't find the Atlas Core. He pats himself down, then digs behind his
// back: a rubber duck (over his shoulder with it), a cable (dropped), a tiny traffic cone (set down,
// carefully). Zip wanders over and points at his tummy, where it's docked, as always. "...oh." Archie takes it
// out and shows the world anyway: as planned. Clips: pocket_universe.py (and _corekit.py's take/back).
({
  cast: ["archie", "zip"],
  pages: ["home", "topic", "repo", "repos", "catalog", "discover", "collections", "target", "lost"],
  ppm: 140,
  ready(s) {
    return innerWidth >= 1000 && innerHeight >= 620;
  },

  async play(s) {
    const A = s.archie, Z = s.zip, T = s.T;
    const W = innerWidth, floor = innerHeight - 8, x0 = Math.round(W * 0.38);
    const core = await s.core(A);
    const [duck, cable, cone] = await Promise.all(["rubber-duck", "cable", "tiny-traffic-cone"].map(n => s.prop(n)));
    if (!s.alive) return;
    s.page.undo(() => [duck, cable, cone].forEach(p => p.remove()));
    // drawn a little bigger than life, to read at this size: SIZE times the prop's metres
    const SIZE = new Map([[duck, 1.6], [cable, 1.0], [cone, 2.5]]);
    // pocket_universe.py: ZIP (0.95, -0.1), PULL_AT 0.75, TOSS_AT 0.32, DROP_AT 0.45, SET_AT 0.95
    const zx = x0 + 0.95 * A.ppm;
    // What he digs out: in his right hand, upright, from PULL_AT, and let go of onto the page.
    let held = null;
    const out = async (prop, offset) => {
      const d = A.perform("pocket-universe/dig");
      await s.after(0.75);                                // PULL_AT
      if (!s.alive) return;
      held = s.attach(prop.root, A, "grip_R", {offset});
      prop.root.scale.setScalar(SIZE.get(prop));
      await d;
    };
    const free = prop => {                                // off his hand and onto the page, where it is now
      if (held) { held(); held = null; }
      s.scene.attach(prop.root);
      prop.root.rotation.set(0, 0, 0);
      prop.root.scale.setScalar(A.ppm * SIZE.get(prop));
      return prop.root;
    };
    const fall = (o, vx, vy, spin, rest = 0) => {        // under gravity to the floor (page px a second)
      let x = o.position.x, y = -o.position.y, last = s.clock();
      return s.until(() => {
        const dt = s.clock() - last; last = s.clock();
        vy += 1500 * dt;
        x += vx * dt; y += vy * dt;
        o.rotation.z += spin * dt;
        const done = y >= floor - rest;
        if (done) { y = floor - rest; o.rotation.z = Math.round(o.rotation.z / Math.PI) * Math.PI; }
        o.position.set(x, -y, o.position.z);
        return done;
      });
    };

    A.at(-0.45 * A.ppm, floor).show(true);
    A.play("idle", {loop: true});
    await A.walkTo(x0);
    if (!s.alive) return;
    await A.face(0);
    A.say("Where's my Core?", 1.6);
    await A.perform("pocket-universe/search");
    if (!s.alive) return;

    // A rubber duck: over the shoulder.
    await out(duck, [0, 0, 0.03]);
    if (!s.alive) return;
    A.say("...a duck?", 1.1);
    await s.after(1.0);
    const toss = A.perform("pocket-universe/toss");
    await s.after(0.32);                                  // TOSS_AT
    if (!s.alive) return;
    const d = free(duck);
    d.position.z = -60;                                   // behind him
    fall(d, -260, -520, 9);
    await toss;
    if (!s.alive) return;

    // A cable: dropped.
    await out(cable, [0, 0, 0]);
    if (!s.alive) return;
    cable.play("dangle", {loop: true});
    A.say("Cable.", 0.9);
    await s.after(1.1);
    const drop = A.perform("pocket-universe/drop");
    await s.after(0.45);                                  // DROP_AT
    if (!s.alive) return;
    const cb = free(cable);
    cb.position.z = 60;
    fall(cb, 0, 0, 0, 0.9 * A.ppm).then(() => {           // it lands on its loose end and flops over
      if (!s.alive) return;
      const t0 = s.clock(), y0 = cb.position.y;
      s.until(() => {
        const u = Math.min(1, (s.clock() - t0) / 0.35);
        cb.rotation.z = -Math.PI / 2 * u * u;
        cb.position.y = y0 - 0.85 * A.ppm * u * u;
        return u >= 1;
      });
    });
    await drop;
    if (!s.alive) return;

    // A tiny traffic cone: set down, carefully. Zip has wandered over.
    Z.at(W + 0.5 * Z.ppm, floor).show(true);
    const zipIn = Z.walkTo(zx);
    await out(cone, [0, 0, 0.02]);
    if (!s.alive) return;
    A.say("...?", 0.8);
    await s.after(0.9);
    const set = A.perform("pocket-universe/set");
    await s.after(0.95);                                  // SET_AT
    if (!s.alive) return;
    const cn = free(cone);
    cn.position.set(cn.position.x, -floor, 60);
    await set;
    if (!s.alive) return;
    A.play("idle", {loop: true});

    // Zip, pointing at his tummy.
    await zipIn;
    if (!s.alive) return;
    await Z.face(0);
    const pt = Z.perform("pocket-universe/point-belly");
    await s.after(0.7);
    Z.say("Tummy.", 1.2);
    await s.after(0.4);
    const re = A.perform("pocket-universe/realize");
    await s.after(1.0);
    A.say("...oh.", 1.0);
    await Promise.all([pt, re]);
    if (!s.alive) return;
    Z.perform("laugh");

    // As planned.
    const take = A.perform("pocket-universe/take");
    await s.after(0.62);                                  // _corekit.GRAB
    core.hold();
    await take;
    if (!s.alive) return;
    A.play("pocket-universe/hold", {loop: true});
    core.play("unfold");
    await s.after(0.9);
    if (!s.alive) return;
    core.play("open-idle", {loop: true});
    const proj = await s.project(s.where().world);
    if (!s.alive || !proj) return;
    // up on his right, this time: Zip is on his left
    const follow = s.tick(() => { const p = core.page(); proj.at(p.x, p.y, 260, -1); });
    s.after(0.8).then(() => s.alive && proj.idle());
    const pr = A.perform("pocket-universe/present");
    await s.after(0.5);
    A.say("As planned.", 1.5);
    await pr;
    if (!s.alive) return;
    A.play("pocket-universe/hold", {loop: true});
    await s.after(1.2);
    if (!s.alive) return;
    proj.hide(0.3);
    await s.after(0.3);
    follow();
    core.play("fold");
    await s.after(0.9);
    const back = A.perform("pocket-universe/back");
    await s.after(0.86);                                  // _corekit.DOCK
    core.dock();
    await back;
    if (!s.alive) return;
    A.play("idle", {loop: true});
    await s.after(0.8);
  },
})
