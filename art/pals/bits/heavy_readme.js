// Heavy README. Along the bottom of the window, below the README viewer, lies the README itself: a long
// slab of it. Archie squats, takes one end and heaves -- nothing. He bellows for Brick, who comes in from the
// edge of the window, looks at it, slides one finger under its middle and lifts it over his head like a plate
// on a stick. Archie stretches, dusts his hands and puts them on his hips as if he had done the work. Brick
// looks at him. Clips: heavy_readme.py.
({
  cast: ["archie", "brick"],
  pages: ["repo"],
  ppm: 62,
  ready(s) {
    const r = s.page.rect(".source-preview .reader");
    // the README viewer on screen above them, and room over Brick's head for the slab on his finger (3.7 m)
    return !!r && r.top > 0 && r.top < innerHeight - 4.2 * 62 && innerHeight > 4.2 * 62 &&
      document.documentElement.clientWidth > 7 * 62;
  },
  async play(s) {
    const A = s.archie, B = s.brick, ppm = 62;
    const W = document.documentElement.clientWidth, floor = innerHeight - 6;
    // heavy_readme.py: SLAB_Y -0.4, ARCHIE_X -1.35, BRICK_X 1.05, GRAB_AT 1.55, TIP_OFF 0.12
    const xs = W - 3.4 * ppm, ax = xs - 1.35 * ppm, bx = xs + 1.05 * ppm;
    const slab = await s.prop("readme-slab");
    if (!s.alive) return;
    slab.at(xs, floor, ppm);
    slab.root.position.z = 0.4 * ppm;                // in front of them
    A.at(ax, floor, ppm).show(true);
    A.play("idle", {loop: true});
    await s.after(0.6);
    if (!s.alive) return;
    const strain = A.perform("heavy-readme/strain");
    await s.after(1.2);
    A.say("Hnnngh!", 1.6);
    await strain;
    if (!s.alive) return;
    A.say("BRICK!", 1.4);
    await A.perform("heavy-readme/call");
    if (!s.alive) return;
    A.play("idle", {loop: true});
    B.at(W + 1.3 * ppm, floor, ppm).show(true);
    await B.walkTo(bx, {speed: 1.3});
    if (!s.alive) return;
    await B.face(0);
    const lift = B.perform("heavy-readme/lift");
    await s.after(1.55);
    if (!s.alive) return;
    // from here the slab rides his fingertip, level
    slab.detach();
    slab.root.scale.setScalar(1);
    s.attach(slab.root, B, "index_3_R", {offset: [0, 0.12, 0], upright: true});
    await s.after(1.7);
    if (!s.alive) return;
    const stretch = A.perform("heavy-readme/stretch");
    await lift;
    if (!s.alive) return;
    B.play("finger-hold", {loop: true});
    await s.after(2.4);
    A.say("Teamwork.", 1.8);
    await stretch;
    if (!s.alive) return;
    A.play("idle", {loop: true});
    await B.perform("heavy-readme/look");
    if (!s.alive) return;
    B.play("finger-hold", {loop: true});
    await s.after(0.8);
  },
})
