// The stolen spotlight. Up on the home page's spotlight, Archie introduces its project in the beam of a stage
// light. Zip swings the light round onto himself and starts dancing; Archie wrestles it back. Then Brick
// switches on a third spotlight, twice the size, and dances them both off the stage. The lights are props
// over the page; the project's own card is never touched. Clips: stolen_spotlight.py.
({
  cast: ["archie", "zip", "brick"],
  pages: ["home"],
  ppm: 58,
  ready(s) {
    const r = s.page.rect("article.hero");
    return !!r && r.width > 900 && r.top > 170 && r.top < innerHeight - 220;
  },
  // A spotlight-stand's beam at a page point: `pan` turns about the vertical, `tilt` about its own length.
  _aim(s, sp, target) {
    const pan = sp.model.getObjectByName("pan"), tilt = sp.model.getObjectByName("tilt");
    if (!pan || !tilt) return;
    // their rest turns, the first time (each s.prop() is a fresh copy, at rest)
    pan.__q0 = pan.__q0 || pan.quaternion.clone();
    tilt.__q0 = tilt.__q0 || tilt.quaternion.clone();
    const head = new s.T.Vector3();
    sp.root.updateMatrixWorld(true);
    tilt.getWorldPosition(head);
    const dx = target.x - head.x, dy = -target.y - head.y;
    const Y = new s.T.Vector3(0, 1, 0);
    pan.quaternion.copy(pan.__q0).multiply(new s.T.Quaternion().setFromAxisAngle(Y, Math.sign(dx || 1) * Math.PI / 2));
    tilt.quaternion.copy(tilt.__q0).multiply(new s.T.Quaternion().setFromAxisAngle(Y, Math.atan2(-dy, Math.abs(dx))));
  },
  // A beam the page can see through on a light theme or a dark one: soft, warm, normally blended.
  _softBeam(s, sp, opacity = 0.3) {
    const b = [];
    sp.model.traverse(n => {
      if (!n.isMesh || !/beam/.test(n.name)) return;
      n.material = new s.T.MeshBasicMaterial({color: 0xffe9a8, transparent: true, opacity, depthWrite: false,
                                              side: s.T.DoubleSide, name: "holo-beam"});
      b.push(n);
    });
    return b;
  },
  async play(s) {
    const A = s.archie, ppm = A.ppm;
    const H = () => s.page.rect("article.hero");
    const edge = H().top;
    const x0 = H().left + H().width * 0.3;
    // stolen_spotlight.py: LAMP_X, ZIP_X, BRICK_X, BRICK_LAMP_X, BIG_SCALE, GRAB_TURN
    const LAMP = 3.6, ZX = 1.9, BX = -3.0, BLAMP = -4.6, BIG = 2.0, TURN = 0.9;
    // his lamp, and Brick's (the same prop, twice the size, kept back till he switches it on)
    const [lamp, big] = await Promise.all([s.prop("spotlight-stand"), s.prop("spotlight-stand")]);
    if (!s.alive) return;
    const lx = Math.min(x0 + LAMP * ppm, H().right - 0.6 * ppm);
    lamp.at(lx, edge, ppm);
    lamp.root.position.z = -30;                                   // behind the cast
    this._softBeam(s, lamp);
    let target = {x: x0, y: edge - 1.3 * ppm};
    const steer = s.tick(() => this._aim(s, lamp, target));
    const swingTo = (to, secs) => { const from = {...target}; return s.tween(secs, u => {
      target = {x: from.x + (to.x - from.x) * u, y: from.y + (to.y - from.y) * u}; }); };

    A.at(x0 - 3 * ppm, edge).show(true);
    await A.walkTo(x0);
    if (!s.alive) return;
    await A.face(0);
    if (!s.alive) return;
    A.say("Ladies and gentlemen...", 2.2);
    await A.perform("stolen-spotlight/present");
    if (!s.alive) return;

    // The light leaves him: Zip has it (or it wanders off on its own).
    // stolen_spotlight.py: SWING_TURN; Zip's hands meet the lamp's head 0.42 m ahead of him
    const Z = s.zip, zx = x0 + ZX * ppm, SWING = 0.8;
    if (Z) {
      Z.at(lx + 2.2 * ppm, edge).show(true);
      await Z.walkTo(lx + 0.42 * ppm);
      if (!s.alive) return;
      await Z.face(-1);
      if (!s.alive) return;
      const sw = Z.perform("stolen-spotlight/swing");
      await s.until(() => Z.time() >= SWING || !s.alive);
      if (!s.alive) return;
      await swingTo({x: zx, y: edge - 0.8 * ppm}, 0.5);
      if (!s.alive) return;
      await sw;
      if (!s.alive) return;
      await Z.walkTo(zx);
      if (!s.alive) return;
      await Z.face(0);
      if (!s.alive) return;
      Z.play("dance", {loop: true});
    } else {
      await swingTo({x: zx, y: edge - 0.9 * ppm}, 0.6);
    }
    A.play("idle", {loop: true});
    await A.perform("stolen-spotlight/huh");
    if (!s.alive) return;

    // He hauls it back.
    await A.walkTo(lx - 0.62 * ppm);
    if (!s.alive) return;
    await A.face(0);
    if (!s.alive) return;
    const grab = A.perform("stolen-spotlight/grab");
    await s.until(() => A.time() >= TURN || !s.alive);
    if (!s.alive) return;
    await swingTo({x: x0, y: edge - 1.3 * ppm}, 0.5);
    if (!s.alive) return;
    await grab;
    if (!s.alive) return;
    if (Z) { Z.play("hands-on-hips"); }
    await A.walkTo(x0);
    if (!s.alive) return;
    await A.face(0);
    if (!s.alive) return;
    A.play("idle", {loop: true});
    await s.after(0.6);
    if (!s.alive) return;

    // Brick's light: twice the size, and Brick dancing in it.
    const B = s.brick;
    if (B) {
      big.at(Math.max(H().left + 0.6 * ppm, x0 + BLAMP * ppm), edge, ppm * BIG);
      big.root.position.z = -40;
      const beam = this._softBeam(s, big, 0.38);
      beam.forEach(b => { b.visible = false; });
      // up from behind the hero, by his lamp
      const bxp = x0 + BX * ppm;
      B.clipBelow(edge);
      B.at(bxp, edge + 3 * ppm).show(true);
      B.play("idle", {loop: true});
      await s.tween(0.55, u => B.at(bxp, edge + 3 * ppm * (1 - u)));
      B.clipBelow(null);
      if (!s.alive) return;
      await B.face(0);
      if (!s.alive) return;
      this._aim(s, big, {x: x0 + BX * ppm, y: edge - 1.6 * ppm});
      await B.perform("finger-point");
      if (!s.alive) return;
      beam.forEach(b => { b.visible = true; });
      B.play("much-better", {loop: true});
      await s.after(0.6);
    }
    A.play("stolen-spotlight/jaw");
    if (Z && Z.has("stolen-spotlight/stare")) Z.play("stolen-spotlight/stare");
    await s.after(B ? 3.4 : 1.2);
    if (!s.alive) return;
    steer();
  },
})
