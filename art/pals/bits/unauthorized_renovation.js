// The unauthorized renovation. Archie (and, when they're here, Zip and Brick) climbs onto the README viewer
// in a hard hat and hammers away at its corner, and a tiny balcony grows out of the viewer's right edge. A
// deck chair appears on it; Archie strolls out and settles in. Brick hands him an eviction notice. The
// balcony, chair, hats and notice are props beside the viewer; the viewer itself is untouched.
// Clips: unauthorized_renovation.py.
({
  cast: ["archie", "zip", "brick"],
  pages: ["repo"],
  ppm: 56,
  ready(s) {
    const r = s.page.rect(".source-preview .reader");
    // room for a balcony beside it
    return !!r && r.top > 180 && r.top < innerHeight - 200 && innerWidth - r.right > 160;
  },
  async play(s) {
    const A = s.archie, ppm = A.ppm, T = s.T;
    const R = () => s.page.rect(".source-preview .reader");
    const edge = R().top, right = R().right;
    const x0 = right - 1.2 * ppm;
    // unauthorized_renovation.py: BALCONY_DEPTH, READ_TAKE; Archie's hard hat sits 0.33 m up his head bone
    const DEPTH = 2.4, TAKE = 0.7;
    const [hat, hammer, balcony, chair, notice, zhat, bhat, zhammer] = await Promise.all(["hard-hat-lime",
      "hammer", "balcony", "deck-chair", "eviction-notice", "hard-hat-violet", "hard-hat-orange", "hammer"]
      .map(n => s.prop(n)));
    if (!s.alive) return;
    const Z = s.zip, B = s.brick;
    // hats on: each sits this far up its pal's head bone (the bone starts at the neck's top)
    hat.hold(A, "head", [0, 0.33, 0.03]);
    if (Z) zhat.hold(Z, "head", [0, 0.33, 0.02]);
    if (B) bhat.hold(B, "head", [0, 0.26, -0.03]);
    // the hammer upright in his right fist, its head forward
    hammer.hold(A, "grip_R", [0, 0, 0], [0, 0, 0]);

    A.clipBelow(edge);
    A.at(x0, edge + 2.6 * ppm).show(true);
    A.play("idle", {loop: true});
    await s.tween(0.5, u => A.at(x0, edge + 2.6 * ppm * (1 - u)));
    if (!s.alive) return;
    A.clipBelow(null);
    await A.face(1);
    if (!s.alive) return;

    if (Z) {
      zhammer.hold(Z, "grip_R");
      Z.clipBelow(edge);
      Z.at(x0 - 1.4 * ppm, edge + 2.4 * ppm).show(true);
      await s.tween(0.5, u => Z.at(x0 - 1.4 * ppm, edge + 2.4 * ppm * (1 - u)));
      if (!s.alive) return;
      Z.clipBelow(null);
      await Z.face(1);
      if (!s.alive) return;
      Z.play("unauthorized-renovation/hammer", {loop: true});
    }
    // Hammering at the corner while the balcony grows out of the viewer's side: platform level with the
    // viewer's top edge, side on (turned to stick out to the right) and stretched out DEPTH deep.
    A.play("unauthorized-renovation/hammer", {loop: true});
    balcony.at(right, edge, ppm);
    balcony.root.rotation.y = Math.PI / 2;
    balcony.root.scale.set(ppm, ppm, ppm * DEPTH);
    balcony.root.position.z = -10;
    balcony.play("build");
    await s.after(2.2);
    if (!s.alive) return;
    const cx = right + 0.6 * 0.5 * DEPTH * ppm;
    chair.at(cx, edge, ppm);
    chair.root.position.z = -25;                          // behind him: he sits in it
    await s.tween(0.3, u => chair.root.scale.setScalar(ppm * Math.max(0.01, u)));
    if (!s.alive) return;

    // Out onto it, and into the chair.
    hammer.detach();
    A.play("idle", {loop: true});
    await A.walkTo(cx, {speed: 0.8});
    if (!s.alive) return;
    await A.face(0);
    if (!s.alive) return;
    await A.perform("unauthorized-renovation/sit");
    if (!s.alive) return;
    A.say("Ahh.", 1.2);
    A.play("unauthorized-renovation/lounge", {loop: true});
    await s.after(1.8);
    if (!s.alive) return;

    // The eviction notice: handed over by Brick, or, without him, floating down from above into his hand.
    if (Z) { Z.play("idle", {loop: true}); }
    if (B && B.has("unauthorized-renovation/present")) {
      notice.hold(B, "grip_R");
      notice.root.scale.setScalar(1.4);
      B.clipBelow(edge);
      B.at(right - 2.2 * ppm, edge + 3 * ppm).show(true);
      await s.tween(0.6, u => B.at(right - 2.2 * ppm, edge + 3 * ppm * (1 - u)));
      if (!s.alive) return;
      B.clipBelow(null);
      await B.walkTo(right - 0.6 * ppm);
      if (!s.alive) return;
      await B.face(1);
      if (!s.alive) return;
      await B.perform("unauthorized-renovation/present");
    } else {
      notice.at(cx - 0.2 * ppm, edge - 4 * ppm, ppm * 1.4);
      notice.root.position.z = 40;
      notice.play("flutter", {loop: true});
      await s.tween(1.6, u => notice.root.position.set(cx - 0.3 * ppm + Math.sin(u * 7) * 0.2 * ppm,
                                                                 -(edge - (4 - 2.6 * u) * ppm), 40), u => u);
    }
    if (!s.alive) return;
    const read = A.perform("unauthorized-renovation/read");
    await s.until(() => A.time() >= TAKE || !s.alive);
    if (!s.alive) return;
    notice.hold(A, "grip_R", [0, -0.1, 0.05]);
    notice.root.scale.setScalar(1.4);
    if (B) B.play("idle", {loop: true});
    if (Z) Z.play("laugh");
    await read;
    if (!s.alive) return;
    await s.after(0.8);
  },
})
