// The unnecessary crew. Up on the home page's spotlight, Archie tries to shift one tiny button with a
// fingertip and can't. He whistles for help. Brick and Zip turn up with a row of traffic cones, and a lifting
// harness built for a car comes down out of the sky; they rig the button into it and up it goes, Archie
// waving it away like a banksman. The button, cones and harness are props: none of the page's own buttons is
// touched. Clips: unnecessary_crew.py.
({
  cast: ["archie", "zip", "brick"],
  pages: ["home"],
  ppm: 58,
  ready(s) {
    const r = s.page.rect("article.hero");
    return !!r && r.width > 800 && r.top > 170 && r.top < innerHeight - 220;
  },
  // Up from behind the element whose top edge is `edge`, to stand at x (clipped at the edge on the way).
  async _rise(s, a, x, edge, clip = "idle") {
    a.clipBelow(edge);
    a.at(x, edge + 3 * a.ppm).show(true);
    a.play(clip, {fade: 0, loop: true});
    await s.tween(0.55, u => a.at(x, edge + 3 * a.ppm * (1 - u)));
    if (!s.alive) return;
    a.clipBelow(null);
  },
  async play(s) {
    const A = s.archie, ppm = A.ppm, T = s.T;
    const H = () => s.page.rect("article.hero");
    const edge = H().top;
    const x0 = H().left + H().width * 0.32;
    // unnecessary_crew.py: BUTTON_SCALE, BUTTON_X, CONES, BRICK_X, ZIP_X; the harness's cradle hangs 1.95 m
    // below its origin (props_set.py), here drawn HS times over
    const BS = 1.6, BXp = 0.5, CONES = [-0.2, 1.2, 1.9], BRX = 2.8, ZPX = -1.4, HS = 1.3;
    const [btn, harness, ...cones] = await Promise.all([s.prop("tiny-button"), s.prop("lifting-harness"),
                                                       ...CONES.map(() => s.prop("traffic-cone"))]);
    if (!s.alive) return;
    const bx = x0 + BXp * ppm;
    btn.at(bx, edge, ppm * BS);
    btn.root.position.z = 30;

    A.at(x0 - 3.5 * ppm, edge).show(true);
    await A.walkTo(x0);
    if (!s.alive) return;
    await A.face(0);
    if (!s.alive) return;
    await A.perform("unnecessary-crew/push");
    if (!s.alive) return;
    A.say("Fweeet!", 1.2);
    await A.perform("unnecessary-crew/whistle");
    if (!s.alive) return;
    A.play("idle", {loop: true});

    // The crew: Brick and Zip (when they're here) and their cones, set out round the button.
    // Brick carries the cones in, a stack between his hands; Zip runs in after him.
    const Z = s.zip, B = s.brick;
    cones.forEach(c => c.at(0, 0, ppm));
    let carried = !!B;
    const stack = s.tick(() => {
      if (!carried) return;
      const h = B.handsAt();
      cones.forEach((c, i) => c.root.position.set(h.x, -(h.y - 0.1 * ppm * i + 0.25 * ppm), 60 + i));
    });
    if (B) {
      await this._rise(s, B, x0 + BRX * ppm, edge, "lift-hold");
      if (!s.alive) return;
      await B.perform("set-down");
    }
    carried = false;
    stack();
    for (const [i, cxm] of CONES.entries()) {
      const g = cones[i].root;
      const x = x0 + cxm * ppm;
      if (!B) g.position.set(x, -(edge - 1.2 * ppm), 10 + i);
      const f0 = {x: g.position.x, y: g.position.y};
      s.tween(0.4, u => g.position.set(f0.x + (x - f0.x) * u, f0.y + (-edge - f0.y) * u, 10 + i), u => u * u);
      await s.after(0.25);
    }
    if (!s.alive) return;
    if (Z) {
      Z.at(H().left - 1 * ppm, edge).show(true);
      await Z.walkTo(x0 + ZPX * ppm, {clip: "run", mps: 3.75});
      if (!s.alive) return;
      await Z.face(0);
      if (!s.alive) return;
      Z.play("point");
    }

    // The harness, down out of the sky until its cradle is on the edge round the button.
    const drop = 1.95 * HS * ppm;
    const hx = bx;
    harness.at(hx, -40 - drop, ppm * HS);
    harness.root.position.z = -20;
    harness.play("sway", {loop: true});
    A.play("unnecessary-crew/direct", {loop: true});
    const yDown = edge - drop;
    await s.tween(2.4, u => harness.root.position.set(hx, -(-40 - drop + (yDown + drop + 40) * u), -20), u => u * (2 - u));
    if (!s.alive) return;
    // In it goes -- Brick lifts it in with both hands, as if it weighed a ton -- and up.
    if (B) {
      await B.walkTo(hx + 1.3 * ppm);
      if (!s.alive) return;
      await B.face(-1);
      if (!s.alive) return;
      const lift = B.perform("lift");
      await s.after(0.9);
      if (!s.alive) return;
      const carry = s.tick(() => { const h = B.handsAt(); btn.root.position.set(h.x, -(h.y + 0.05 * ppm), 70); });
      await lift;
      if (!s.alive) return;
      carry();
      B.play("set-down");
      await s.after(1.0);
    } else {
      await s.after(0.6);
    }
    const off = s.tick(() => { btn.root.position.set(hx, harness.root.position.y - drop + 0.06 * ppm, 30); });
    await s.after(0.4);
    if (!s.alive) return;
    await s.tween(2.2, u => harness.root.position.y = -(yDown - (yDown + drop + 60) * u), u => u * u);
    if (!s.alive) return;
    off();
    btn.detach();
    if (Z) Z.play("cheer");
    if (B) B.play("nod");
    await A.perform("unnecessary-crew/thumbs");
    if (!s.alive) return;
    await s.after(0.4);
  },
})
