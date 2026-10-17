// The README hostage situation. Archie pops up onto the README viewer's edge and holds a sign up over it --
// BACK IN 5 MINUTES -- so big there is nothing left of him but his shoes and the tip of his crest. Brick
// comes up behind the viewer, takes hold of the sign's edge and hauls it away like a curtain. Underneath,
// Archie is holding a smaller one: BACK IN 4 MINUTES. The signs are props, pictures over the page; the viewer
// underneath is never covered for more than a few seconds. Clips: readme_hostage.py.
({
  cast: ["archie", "brick"],
  pages: ["repo"],
  ppm: 56,
  ready(s) {
    const r = s.page.rect(".source-preview .reader");
    return !!r && r.width > 640 && r.left > 0 && r.top > 200 && r.top < innerHeight - 200;
  },
  // Keep a prop's origin at fn() (page px) every frame, `z` px towards the reader; returns its remover.
  _follow(s, prop, fn, z) {
    return s.tick(() => { const p = fn(); prop.root.position.set(p.x, -p.y, z); });
  },
  // Up from behind the viewer onto its edge, at x.
  async _rise(s, a, x, edge, clip) {
    a.clipBelow(edge);
    a.at(x, edge + 3 * a.ppm).show(true);
    a.play(clip || "idle", {fade: 0, loop: !clip});
    await s.tween(0.5, u => a.at(x, edge + 3 * a.ppm * (1 - u)));
    if (!s.alive) return;
    a.clipBelow(null);
  },
  async play(s) {
    const A = s.archie, B = s.brick, ppm = A.ppm;
    const R = () => s.page.rect(".source-preview .reader");
    const edge = R().top;
    const x0 = R().left + R().width * 0.45;
    // readme_hostage.py: BIG_SCALE, SMALL_SCALE, RAISE_SHOW, REVEAL_SNAP, BRICK_X, LIFT_GRAB; a sign's hook
    // sits 0.55 of its board's height above the board's top edge, the boards 0.72 x 0.4 and 0.44 x 0.25 m
    // before scaling (props_paper.py)
    const BIG = 5.0, SMALL = 3.6, SHOW = 0.85, SNAP = 0.18, BX = -2.5, GRAB = 0.7;
    const bigDrop = 0.55 * 0.4 * BIG * ppm, smallDrop = 0.55 * 0.25 * SMALL * ppm;
    const [big, small] = await Promise.all([s.prop("sign-back-in-5"), s.prop("sign-back-in-4")]);
    if (!s.alive) return;

    this._rise(s, A, x0, edge, "readme-hostage/hop");
    await s.after(0.5);
    await s.until(() => A.time() > 1.1 || !s.alive);
    if (!s.alive) return;

    // Up goes the big sign, its board's top edge in his hands.
    const raise = A.perform("readme-hostage/raise");
    await s.until(() => A.time() >= SHOW || !s.alive);
    if (!s.alive) return;
    big.at(0, 0, ppm * BIG);
    const followBig = this._follow(s, big, () => { const h = A.handsAt(); return {x: h.x, y: h.y - bigDrop}; }, 80);
    await raise;
    if (!s.alive) return;
    A.play("readme-hostage/hold", {loop: true});

    // Brick, up from behind the viewer beside him; a big hand on the sign's near edge.
    const bx = x0 + BX * ppm;
    await this._rise(s, B, bx, edge);
    if (!s.alive) return;
    await B.face(1);
    if (!s.alive) return;
    await s.after(0.6);
    if (!s.alive) return;
    B.play("readme-hostage/lift");
    await s.until(() => B.time() >= GRAB || !s.alive);
    if (!s.alive) return;
    followBig();
    const hook0 = {x: big.root.position.x, y: -big.root.position.y};
    const grip0 = B.pageAt("grip_R");
    // Hauled away to his left like a curtain: he backs off with it, the sign sliding with his hand.
    this._follow(s, big, () => { const g = B.pageAt("grip_R"); return {x: hook0.x + (g.x - grip0.x), y: hook0.y}; }, 80);
    B.play("pull", {loop: true});
    const back = s.tween(2.6, u => B.at(bx - 3.6 * ppm * u, edge));
    // ...and as it clears him, Archie, deadpan, with the small one.
    await s.after(0.35);
    if (!s.alive) return;
    A.play("readme-hostage/reveal");
    await s.until(() => A.time() >= SNAP * 0.7 || !s.alive);
    if (!s.alive) return;
    small.at(0, 0, ppm * SMALL);
    this._follow(s, small, () => { const h = A.handsAt(); return {x: h.x, y: h.y - smallDrop}; }, 40);
    await back;
    if (!s.alive) return;
    // ...and holds it up at his side, still in his hand, for a long look at the small one.
    B.play("readme-hostage/look", {loop: true, fade: 0.4});
    await s.until(() => A.time() >= 2.9 || !s.alive);
    if (!s.alive) return;
    A.play("readme-hostage/small", {loop: true});
    await s.after(4.4);
  },
})
