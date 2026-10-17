// The world-sized flex. Archie opens the Atlas Core on the page's world and presents it with enormous
// theatrical effort -- heave, heave, HEAVE -- and the projection swells to tower over the page. Zip strolls
// over, reaches up and turns the Core's size dial down: the world shrinks to a speck on the Core. Archie
// deflates. "...thanks." Clips: world_sized_flex.py (and _corekit.py's take/back).
({
  cast: ["archie", "zip"],
  pages: ["home", "topic", "repo", "repos", "catalog", "discover", "collections", "target", "lost"],
  ppm: 140,
  ready(s) {
    return innerWidth >= 1000 && innerHeight >= 620;
  },

  async play(s) {
    const A = s.archie, Z = s.zip, T = s.T;
    const W = innerWidth, H = innerHeight, floor = H - 8, x0 = Math.round(W * 0.36);
    const core = await s.core(A);
    if (!s.alive) return;
    const ease = u => 1 - Math.pow(1 - Math.min(1, Math.max(0, u)), 3);
    A.at(-0.45 * A.ppm, floor).show(true);
    A.play("idle", {loop: true});
    await A.walkTo(x0);
    if (!s.alive) return;
    await A.face(0);
    const take = A.perform("world-sized-flex/take");
    await s.after(0.62);                                  // _corekit.GRAB
    core.hold();
    await take;
    if (!s.alive) return;
    A.play("world-sized-flex/hold", {loop: true});
    core.play("unfold");
    await s.after(0.9);
    if (!s.alive) return;
    core.play("open-idle", {loop: true});

    // The world, where the Core puts it; then wherever and however big this bit says.
    // at its biggest the world stands about 70% of the window high (it draws about 0.85 of its width tall),
    // so the page still shows round it; and it is that big for little more than a second
    const SIZE = 260, BIG = Math.min(W * 0.62, H * 0.82), TINY = 54;
    const proj = await s.project(s.where().world);
    if (!s.alive || !proj) return;
    const usual = () => {                                 // archie-stage.js project()'s own placement
      const p = core.page(), r = SIZE / 2, side = p.x + r * 2.5 < W - 8 ? 1 : -1;
      return {x: p.x + side * r * 1.35, y: Math.max(r * 1.3 + 6, p.y - r * 1.1), size: SIZE};
    };
    const big = {x: W * 0.52, y: H * 0.46, size: BIG};
    let k = 0, kTo = 0, kAt = 0, kFrom = 0, mode = "at", shrink = 0;
    const follow = s.tick(() => {
      const p = core.page();
      if (mode === "at") { proj.at(p.x, p.y, SIZE, 1); return; }
      k = kFrom + (kTo - kFrom) * ease((s.clock() - kAt) / 0.4);
      const a = usual(), tiny = {x: p.x, y: p.y - 42, size: TINY};
      const at = (u, from, to) => from + (to - from) * u;
      let x = at(k, a.x, big.x), y = at(k, a.y, big.y), size = at(k, a.size, big.size);
      x = at(shrink, x, tiny.x); y = at(shrink, y, tiny.y); size = at(shrink, size, tiny.size);
      proj.free(x, y, size);
      proj.root.position.z = 400;                         // in front of the cast, however small it gets
    });
    s.after(0.8).then(() => s.alive && proj.idle());
    // Zip has seen it and is on his way over.
    Z.at(W + 0.5 * Z.ppm, floor).show(true);
    Z.depth(0.15 * Z.ppm);                                // a little in front of Archie
    const zipIn = Z.walkTo(x0 + 0.85 * A.ppm).then(() => s.alive && Z.face(0));   // world_sized_flex.py ZIP
    await s.after(1.0);
    if (!s.alive) return;

    // Behold. Heave. HEAVE.
    A.say("Behold!", 1.0);
    await s.after(0.6);
    const heave = A.perform("world-sized-flex/heave");
    for (const [i, at] of [0.7, 1.7, 2.7].entries()) {    // HEAVES
      await s.after(at - (i ? [0.7, 1.7, 2.7][i - 1] : 0));
      if (!s.alive) return;
      mode = "free"; kFrom = k; kTo = (i + 1) / 3; kAt = s.clock();
    }
    await heave;
    if (!s.alive) return;
    A.play("world-sized-flex/strain", {loop: true});
    await zipIn;
    if (!s.alive) return;

    // Zip turns it down.
    const dial = core.scene.getObjectByName("dial"), q0 = dial ? dial.quaternion.clone() : null;
    if (dial) s.page.undo(() => dial.quaternion.copy(q0));
    const yq = new T.Quaternion(), Y = new T.Vector3(0, 1, 0);
    const turn = Z.perform("world-sized-flex/dial");
    await s.after(1.05);                                  // TURN
    if (!s.alive) return;
    const t0 = s.clock();
    const twist = s.tick(() => {
      const u = Math.min(1, (s.clock() - t0) / 0.8);
      shrink = ease(u);
      if (dial) dial.quaternion.copy(q0).multiply(yq.setFromAxisAngle(Y, -2.6 * ease(u)));
      if (u >= 1) twist();
    });
    await s.after(0.8);
    if (!s.alive) return;
    A.perform("world-sized-flex/deflate");
    await turn;
    if (!s.alive) return;
    Z.play("idle", {loop: true});
    await s.after(1.0);
    A.say("...thanks.", 1.2);
    await s.after(1.4);
    if (!s.alive) return;
    const off = Z.walkTo(W + 0.6 * Z.ppm);

    proj.hide(0.3);
    await s.after(0.3);
    follow();
    core.play("fold");
    await s.after(0.9);
    const back = A.perform("world-sized-flex/back");
    await s.after(0.86);                                  // _corekit.DOCK
    core.dock();
    await back;
    if (!s.alive) return;
    A.play("idle", {loop: true});
    await off;
    await s.after(0.5);
  },
})
