// The leveling dispute. Archie pops up onto the README viewer's top edge, lays a spirit level along it and
// squints at the bubble: off. Two firm taps and it's true. Then the bubble wanders again -- Zip, hidden behind
// the viewer under the level's far end, is lifting it with his head: only the tips of his horns show -- and
// again. The third time Archie follows the level along to its end, and Zip rises into view. Who, me?
// Clips: leveling_dispute.py.
({
  cast: ["archie", "zip"],
  pages: ["repo"],
  ppm: 64,
  ready(s) {
    const r = s.page.rect(".source-preview .reader");
    return !!r && r.width > 640 && r.left > 0 && r.top > 170 && r.top < innerHeight - 160;
  },
  async play(s) {
    const A = s.archie, Z = s.zip, ppm = A.ppm;
    const R = () => s.page.rect(".source-preview .reader");
    const edge = R().top;
    const x0 = R().left + Math.min(0.22 * R().width, 240);
    // leveling_dispute.py: LEVEL_SCALE, LEVEL_NEAR, LEVEL_LEN, HOP_RISE, SET_GRAB, SET_DROP, FIX_TAPS, ZIP_Z,
    // NUDGE_RISE
    const SC = 2.0, NEAR = 0.32, LEN = 2.0, HOP = 0.45, GRAB = 0.35, DROP = 1.25, TAPS = [0.75, 1.25];
    const ZZ = 1.74, RISE = 0.07;

    const lv = await s.prop("level");
    if (!s.alive) return;
    const bub = lv.model.getObjectByName("bubble");
    const b0 = bub ? bub.position.x : 0;
    let tilt = 0;
    const xL = x0 + NEAR * ppm;
    // The level pivots on its near end, on the edge; the bubble runs to the high end.
    const lay = () => {
      lv.root.rotation.set(0, 0, tilt);
      lv.root.position.set(xL + Math.cos(tilt) * LEN / 2 * ppm, -edge + Math.sin(tilt) * LEN / 2 * ppm, 4);
      if (bub) bub.position.x = b0 + Math.max(-0.05, Math.min(0.05, tilt * 1.7));
    };
    const tiltTo = (to, secs) => { const from = tilt; return s.tween(secs, u => { tilt = from + (to - from) * u; lay(); }); };
    const UP = RISE / LEN;                                         // Zip on his toes: the far end lifted

    // Zip is already in place, under where the far end will be: nothing of him above the edge but his horns.
    const zx = x0 + (NEAR + LEN) * ppm;
    Z.clipBelow(edge);
    Z.at(zx, edge + ZZ * ppm).show(true);
    Z.play("leveling-dispute/hold", {loop: true});

    // Up from behind the viewer onto its edge.
    A.clipBelow(edge);
    A.at(x0, edge + 2.6 * ppm).show(true);
    A.play("leveling-dispute/hop", {fade: 0});
    await s.tween(HOP, u => A.at(x0, edge + 2.6 * ppm * (1 - u)));
    if (!s.alive) return;
    await s.until(() => A.time() > 1.0 || !s.alive);
    if (!s.alive) return;
    A.clipBelow(null);

    // The level from behind his back (in his left hand, upright), then down on the edge: on Zip's head.
    const hold = new s.T.Group();
    hold.add(lv.root);
    lv.root.scale.setScalar(SC);
    lv.root.position.set(0.7, -0.08, 0.15);
    const set = A.perform("leveling-dispute/set");
    await s.until(() => A.time() >= GRAB || !s.alive);
    if (!s.alive) return;
    const off = s.attach(hold, A, "grip_L", {upright: true});
    await s.until(() => A.time() >= DROP || !s.alive);
    if (!s.alive) return;
    const w = new s.T.Vector3();
    lv.root.getWorldPosition(w);
    off();
    hold.removeFromParent();
    lv.at(w.x, -w.y, ppm * SC);
    Z.play("leveling-dispute/nudge");
    tilt = UP;
    await s.tween(0.3, u => {
      lay();
      lv.root.position.x = w.x + (lv.root.position.x - w.x) * u;
      lv.root.position.y = w.y + (lv.root.position.y - w.y) * u;
    });
    lay();
    await set;
    if (!s.alive) return;

    // He squints: off. Two taps on his end, and Zip ducks back down under it: true.
    const fix = async () => {
      const f = A.perform("leveling-dispute/fix");
      await s.until(() => A.time() >= TAPS[0] || !s.alive);
      if (!s.alive) return;
      tiltTo(tilt * 0.45, 0.12);
      await s.until(() => A.time() >= TAPS[1] || !s.alive);
      if (!s.alive) return;
      Z.play("leveling-dispute/duck");
      tiltTo(0, 0.25);
      await f;
      if (!s.alive) return;
      Z.play("leveling-dispute/hold", {loop: true});
    };
    await A.perform("leveling-dispute/peer");
    if (!s.alive) return;
    await fix();
    if (!s.alive) return;
    A.say("Perfect.", 1.4);
    await A.perform("leveling-dispute/pleased");
    if (!s.alive) return;
    A.play("idle", {loop: true});

    // Rounds two and three: up on his toes again.
    const nudge = async () => {
      Z.play("leveling-dispute/nudge");
      await s.after(0.15);
      if (!s.alive) return;
      await tiltTo(UP, 0.3);
    };
    await s.after(0.9);
    if (!s.alive) return;
    await nudge();
    if (!s.alive) return;
    await A.perform("leveling-dispute/again");
    if (!s.alive) return;
    await fix();
    if (!s.alive) return;
    A.play("idle", {loop: true});
    await s.after(1.0);
    if (!s.alive) return;
    await nudge();
    if (!s.alive) return;
    await A.perform("leveling-dispute/again");
    if (!s.alive) return;

    // Along the level to its far end... and up comes Zip. The level drops back true.
    const follow = A.perform("leveling-dispute/follow");
    await s.until(() => A.time() >= 1.45 || !s.alive);
    if (!s.alive) return;
    Z.play("leveling-dispute/caught");
    tiltTo(0, 0.2);
    await s.tween(0.45, u => Z.at(zx, edge + (ZZ - 0.95 * u) * ppm));
    if (!s.alive) return;
    await follow;
    if (!s.alive) return;
    A.say("...", 1.2);
    await s.after(1.5);
  },
})
