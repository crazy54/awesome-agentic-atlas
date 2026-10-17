// The world needs leveling. Archie opens the Atlas Core and its world comes up crooked (its tilt clip). He
// gets out a spirit level and sets it on the main island -- the world sits beside him, the island under his
// hand -- and fiddles: the stage comes level (its level clip), and every other island tips. He fiddles again;
// they tip further. Brick strolls over and gently takes the level away, and once it has gone everything
// settles level on its own. "But I..." Clips: world_needs_leveling.py (and _corekit.py's take/back).
({
  cast: ["archie", "brick"],
  pages: ["home", "topic", "repo", "repos", "catalog", "discover", "collections", "target", "lost"],
  ppm: 140,
  ready(s) {
    return innerWidth >= 1050 && innerHeight >= 620;     // the world and Brick on his right
  },

  async play(s) {
    const A = s.archie, B = s.brick, T = s.T;
    const W = innerWidth, floor = innerHeight - 8, x0 = Math.round(W * 0.56);
    const core = await s.core(A);
    const level = await s.prop("level");
    if (!s.alive) return;
    s.page.undo(() => level.remove());
    // world_needs_leveling.py: BRICK (-2.3, 0.2), LEVEL_AT (-0.84, ., 1.69), LEVEL_GRIP 0.1, LEVEL_ON 0.6,
    // LET_GO 0.55, TAKE_AT 1.1
    const bx = x0 - 2.3 * A.ppm;
    const v = new T.Vector3();
    const pageOf = o => { o.getWorldPosition(v); return {x: v.x, y: -v.y}; };
    A.at(x0, floor).show(true);
    A.play("idle", {loop: true});
    await s.after(0.5);
    if (!s.alive) return;
    const take = A.perform("world-needs-leveling/take");
    await s.after(0.62);                                  // _corekit.GRAB
    core.hold();
    await take;
    if (!s.alive) return;
    A.play("world-needs-leveling/hold", {loop: true});
    core.play("unfold");
    await s.after(0.9);
    if (!s.alive) return;
    core.play("open-idle", {loop: true});

    // The world, beside him on his right, its main island just where his level will go; a beam to it.
    const SIZE = 250, r = SIZE / 2;
    const proj = await s.project(s.where().world);
    if (!s.alive || !proj) return;
    // the island he levels: the one on the world's right, nearest him (the rest of the world clear of him)
    const w = proj.world;
    proj.free(0, 0, SIZE);
    proj.root.updateMatrixWorld(true);
    let main = null, best = -Infinity;
    w.traverse(n => { if (/^island_/.test(n.name)) { const x = pageOf(n).x; if (x > best) { best = x; main = n; } } });
    const spot = {x: x0 - 0.84 * A.ppm, y: floor - 1.69 * A.ppm};
    // where its main island sits from the world's middle, at full size (measured again once it has risen)
    const measure = () => {
      proj.free(0, 0, SIZE);
      proj.root.updateMatrixWorld(true);
      const m = main ? pageOf(main) : {x: 0, y: -r * 0.3}, c = pageOf(proj.root);
      return {x: m.x - c.x, y: m.y - c.y};
    };
    let off = measure(), offFrom = off, offTo = off, offAt = 0, grow = 0;
    const beam = s.svg.path({stroke: "none", width: 0});
    beam.el.setAttribute("fill", "url(#pals-beam)");
    beam.el.setAttribute("opacity", "0.55");
    const t0 = s.clock();
    const place = s.tick(() => {
      grow = 1 - Math.pow(1 - Math.min(1, (s.clock() - t0) / 0.5), 3);
      const u = offAt ? Math.min(1, (s.clock() - offAt) / 0.4) : 1;
      off = {x: offFrom.x + (offTo.x - offFrom.x) * u, y: offFrom.y + (offTo.y - offFrom.y) * u};
      const cx = spot.x - off.x, cy = spot.y - off.y + 4;
      proj.free(cx, cy, Math.max(1e-3, SIZE * grow));
      const p = core.page(), dx = r * 0.85 * grow, dy = r * 0.32 * grow;
      beam.el.setAttribute("d", `M${p.x - 2} ${p.y} L${p.x + 2} ${p.y} L${cx + dx} ${cy + dy} L${cx - dx} ${cy + dy} Z`);
    });
    s.after(0.85).then(() => { if (!s.alive) return; offFrom = off; offTo = measure(); offAt = s.clock(); });
    await s.after(0.8);
    if (!s.alive) return;
    proj.play("tilt");
    await s.after(1.0);
    A.say("Hm. Crooked.", 1.3);
    await s.after(0.6);
    if (!s.alive) return;

    // The level out and onto it.
    const lo = A.perform("world-needs-leveling/level-out");
    await s.after(0.6);                                   // LEVEL_ON
    const inHand = s.attach(level.root, A, "grip_R", {offset: [0, 0, 0.1]});
    await lo;
    if (!s.alive) return;
    level.play("measure");

    // Every island but the one he's levelling tips a little further each time he fiddles with it.
    const isles = [];
    w.traverse(n => { if (/^island_/.test(n.name) && n !== main) isles.push(n); });
    const tips = isles.map((n, i) => ({n, q0: null,
      axis: new T.Vector3(Math.cos(i * 2.4), 0, Math.sin(i * 2.4)).normalize(), sign: i % 2 ? 1 : -1}));
    let tipNow = 0, tipFrom = 0, tipTo = 0, tipAt = 0, tipSecs = 0.5, tipping = null;
    const dq = new T.Quaternion();
    const tipBy = (deg, secs = 0.5) => {
      tips.forEach(t => { if (!t.q0) t.q0 = t.n.quaternion.clone(); });
      tipFrom = tipNow; tipTo = deg; tipAt = s.clock(); tipSecs = secs;
      if (!tipping) tipping = s.tick(() => {
        const u = Math.min(1, (s.clock() - tipAt) / tipSecs), e = 1 - Math.pow(1 - u, 3);
        tipNow = tipFrom + (tipTo - tipFrom) * e;
        tips.forEach(t => t.n.quaternion.copy(t.q0).multiply(dq.setFromAxisAngle(t.axis, tipNow * t.sign * Math.PI / 180)));
      });
    };
    s.page.undo(() => tips.forEach(t => { if (t.q0) t.n.quaternion.copy(t.q0); }));
    const fiddle = async (deg, line) => {
      const f = A.perform("world-needs-leveling/fiddle");
      await s.after(0.8);
      if (!s.alive) return;
      if (deg === 12) proj.play("level");
      level.play(deg === 12 ? "tip_left" : "tip_right");
      await s.after(0.7);
      if (!s.alive) return;
      if (line) A.say(line, 1.1);
      await s.after(0.3);
      tipBy(deg);
      await f;
    };
    await fiddle(12, "There.");
    if (!s.alive) return;
    // Brick has seen enough, and sets off.
    B.at(-1.2 * A.ppm, floor).show(true);
    B.depth(-0.2 * B.ppm);                                // a little behind Archie
    const comes = B.walkTo(bx);
    await A.perform("world-needs-leveling/huh");
    if (!s.alive) return;
    A.say("Hold still...", 1.2);
    await fiddle(24, null);
    if (!s.alive) return;
    A.play("world-needs-leveling/huh", {loop: true});

    // Brick, gently, takes the level away. It all settles, on its own.
    await comes;
    if (!s.alive) return;
    await B.face(0);
    const tk = B.perform("world-needs-leveling/take-level");
    await s.after(1.1 - 0.55);                            // TAKE_AT - LET_GO
    const lg = A.perform("world-needs-leveling/let-go");
    await s.after(0.55);
    if (!s.alive) return;
    inHand();
    s.attach(level.root, B, "grip_L", {offset: [0, 0, 0.1]});
    await tk;
    if (!s.alive) return;
    const gone = B.walkTo(-1.4 * A.ppm);
    await s.after(0.6);
    tipBy(0, 1.0);
    await lg;
    if (!s.alive) return;
    A.say("But I...", 1.0);
    await A.perform("world-needs-leveling/protest");
    if (!s.alive) return;
    if (tipping) { tipping(); tipping = null; }           // the world's own idle has them again
    proj.idle();
    A.play("world-needs-leveling/hold", {loop: true});
    await gone;
    await s.after(0.4);
    if (!s.alive) return;

    proj.hide(0.3);
    beam.fade(0.3);
    await s.after(0.3);
    place();
    core.play("fold");
    await s.after(0.9);
    const back = A.perform("world-needs-leveling/back");
    await s.after(0.86);                                  // _corekit.DOCK
    core.dock();
    await back;
    if (!s.alive) return;
    A.play("idle", {loop: true});
    await s.after(0.8);
  },
})
