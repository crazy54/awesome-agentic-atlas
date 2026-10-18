// The souvenir theft. Zip tiptoes along the top of the home page's spotlight to its star rating, checks
// nobody is looking, plucks a star out of it -- a copy, a prop: the rating itself is never touched -- and
// hides it behind his back. He whistles. A star drops out from behind him, then another; he stuffs them back
// and they pour out faster than he can; he shows two empty hands and runs for it, still shedding stars.
// The stars pile up on the card's edge and fade. Clips: souvenir_theft.py.
({
  cast: ["zip"],
  pages: ["home"],
  ppm: 75,
  ready(s) {
    const r = s.page.rect("article.hero"), st = s.page.rect("article.hero .stz");
    return !!r && !!st && st.width > 0 && r.width > 700 && r.top > 170 && r.top < innerHeight - 260 &&
      st.left - r.left > 160 && r.right - st.left > 300;
  },
  async play(s) {
    const Z = s.zip, ppm = Z.ppm, T = s.T;
    const H = () => s.page.rect("article.hero");
    const glyph = () => { const c = s.page.rect("article.hero .stz"); return {x: c.left + 11, y: c.top + c.height / 2}; };
    const STAND = 0.2, GRAB = 1.85;                       // souvenir_theft.py
    const SNEAK = 0.32 / (0.62 * 1.2), RUN = 0.6 / (0.4 * 0.4);   // zip_base.py SNEAK_SPEED, RUN_SPEED
    const SIZE = 2.0;                                     // the star prop (0.22 m) two sizes up, in his metres
    const g = await s.glb("pals/props/star.glb");
    if (!s.alive) return;

    // The stars: copies of the prop over the page, falling, bouncing on the card's top edge and coming to
    // rest there (or off its ends and away down the window).
    const stars = [];
    s.page.undo(() => stars.forEach(st => st.root.removeFromParent()));
    const make = () => {
      const root = new T.Group();
      root.add(g.scene.clone(true));
      root.scale.setScalar(ppm * SIZE);
      s.add(root);
      return root;
    };
    const edge = H().top, R = 0.11 * SIZE * ppm;
    let h = H();
    const fall = s.tick(dt => {
      h = H() || h;                                       // the card's last place, should it go
      for (const st of stars) {
        if (st.rest) {
          // settled: turning to face the reader, as a dropped star would land face up
          const r = st.root.rotation, face = Math.round(r.y / Math.PI) * Math.PI;
          r.y += (face - r.y) * Math.min(1, dt * 6);
          continue;
        }
        st.vy += 1500 * dt;
        st.x += st.vx * dt; st.y += st.vy * dt;
        st.root.rotation.y += st.spin * dt;
        st.root.rotation.z += st.tumble * dt;
        const over = st.x > h.left + 4 && st.x < h.right - 4;
        // the floor is the card's edge, or the heap of stars already there
        const under = stars.filter(o => o.rest && Math.abs(o.x - st.x) < R * 1.1).length;
        const top = edge - R - Math.min(3, under) * R * 0.7;
        if (over && st.y > top && st.vy > 0 && st.y < edge + R) {
          st.y = top;
          if (st.vy < 160 || under) { st.rest = true; st.vy = 0; }
          else { st.vy *= -0.38; st.vx *= 0.6; st.tumble *= 0.5; }
        }
        st.root.position.set(st.x, -st.y, st.z);
      }
    });
    // One out from behind his back, to one side or the other, up and away.
    const spill = (n = 1) => {
      for (let i = 0; i < n; i++) {
        const hip = Z.pageAt("hips"), side = Math.random() < 0.5 ? -1 : 1;
        const root = make();
        stars.push({root, x: hip.x + side * 0.12 * ppm, y: hip.y + 0.05 * ppm, z: -20,
                    vx: side * (90 + Math.random() * 190), vy: -(180 + Math.random() * 260),
                    spin: (Math.random() - 0.5) * 18, tumble: (Math.random() - 0.5) * 8, rest: false});
      }
    };

    // In along the card's top edge from its right-hand end, at a run, then the last few steps on tiptoe.
    const x0 = glyph().x + STAND * ppm, near = Math.min(H().right - 0.4 * ppm, x0 + 1.6 * ppm);
    Z.at(H().right + 0.6 * ppm, edge).show(true);
    await Z.walkTo(near, {clip: "run", mps: RUN});
    if (!s.alive) return;
    await Z.walkTo(x0, {clip: "sneak", mps: SNEAK});
    if (!s.alive) return;
    await Z.face(0);

    // The pinch: the star out of the rating and into his hand.
    const pinch = Z.perform("souvenir-theft/pinch");
    await s.after(GRAB);
    if (!s.alive) return;
    const held = make(), from = glyph();
    held.position.set(from.x, -from.y, 10);
    await s.tween(0.22, u => {
      const to = Z.pageAt("grip_R");
      held.position.set(from.x + (to.x - from.x) * u, -(from.y + (to.y - from.y) * u) + 18 * Math.sin(Math.PI * u), 10);
      held.rotation.y = u * Math.PI * 2;
    });
    held.scale.setScalar(SIZE);
    const unhold = s.attach(held, Z, "grip_R", {offset: [0, 0, 0.02]});
    await pinch;
    if (!s.alive) return;

    // Innocence. Then the first one falls out.
    Z.play("souvenir-theft/innocent", {loop: true});
    Z.say("♪", 1.6);
    await s.after(2.4);
    if (!s.alive) return;
    spill(1);
    await s.after(0.2);
    await Z.perform("souvenir-theft/oops");
    if (!s.alive) return;
    Z.play("souvenir-theft/innocent", {loop: true});
    await s.after(0.9);
    spill(1);
    await s.after(0.6);
    spill(1);
    await s.after(0.45);
    spill(2);
    if (!s.alive) return;

    // He stuffs them back; they pour out.
    Z.play("souvenir-theft/stuff", {loop: true});
    unhold();
    held.removeFromParent();
    for (let i = 0; i < 30 && s.alive; i++) {
      spill(i > 18 ? 2 : 1);
      await s.after(Math.max(0.05, 0.2 - i * 0.008));
    }
    if (!s.alive) return;
    const busted = Z.perform("souvenir-theft/busted");
    await s.after(0.4);
    Z.say("...souvenirs?", 1.6);
    await busted;
    if (!s.alive) return;

    // And away, still shedding them.
    // ... at SHED stars a second, on the stage's clock
    const SHED = 6;
    let next = s.clock();
    const trickle = s.tick(() => { while (s.clock() >= next) { spill(1); next += (0.6 + 0.8 * Math.random()) / SHED; } });
    await Z.walkTo(innerWidth + 1.2 * ppm, {clip: "run", mps: RUN});
    trickle();
    if (!s.alive) return;
    await s.until(() => stars.every(st => st.rest || st.y > innerHeight + 60) || !s.alive);
    await s.after(0.8);
    // gone: the pile fades
    const mats = new Set();
    for (const st of stars) st.root.traverse(m => { if (m.isMesh) { m.material = m.material.clone(); m.material.transparent = true; mats.add(m.material); } });
    await s.tween(0.8, u => mats.forEach(m => { m.opacity = 1 - u; }), u => u);
    fall();
  },
})
