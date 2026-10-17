// The dramatic entrance. On the hero's top edge a smoke machine fills the stage with smoke and a spotlight
// snaps on. The smoke clears on Archie in his grandest pose -- with his back to the reader. He looks over
// his shoulder. Zip walks in and turns him round, and he does it again the right way, with a wink. The
// smoke, the machine and the light are props over the page. Clips: dramatic_entrance.py.
({
  cast: ["archie", "zip"],
  pages: ["home"],
  ppm: 60,
  ready(s) {
    const r = s.page.rect("article.hero");
    return !!r && r.width > 700 && r.top > 170 && r.top < innerHeight - 220;
  },
  // Aim a spotlight-stand's beam at a page point: its `pan` bone turns about the vertical, `tilt` about the
  // bone's own length (props_hand.py).
  _aim(s, sp, target) {
    const pan = sp.model.getObjectByName("pan"), tilt = sp.model.getObjectByName("tilt");
    if (!pan || !tilt) return;
    // their rest turns, the first time (each s.prop() is a fresh copy, at rest)
    pan.__q0 = pan.__q0 || pan.quaternion.clone();
    tilt.__q0 = tilt.__q0 || tilt.quaternion.clone();
    const head = new s.T.Vector3();
    tilt.getWorldPosition(head);
    const dx = target.x - head.x, dy = -target.y - head.y;
    const Y = new s.T.Vector3(0, 1, 0);
    pan.quaternion.copy(pan.__q0).multiply(new s.T.Quaternion().setFromAxisAngle(Y, dx < 0 ? -Math.PI / 2 : Math.PI / 2));
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
    const A = s.archie, ppm = A.ppm, T = s.T;
    const H = () => s.page.rect("article.hero");
    const edge = H().top, left = H().left, width = H().width;
    const x0 = left + width * 0.42;
    const [machine, spot] = await Promise.all([s.prop("smoke-machine"), s.prop("spotlight-stand")]);
    if (!s.alive) return;
    machine.at(x0 - 3.6 * ppm, edge, ppm * 1.6);
    machine.root.position.z = 20;
    const sx = x0 + 4.2 * ppm;
    spot.at(sx, edge, ppm * 1.3);
    const beam = this._softBeam(s, spot);
    beam.forEach(b => { b.visible = false; });
    spot.model.updateMatrixWorld(true);
    this._aim(s, spot, {x: x0, y: edge - 1.2 * ppm});
    // Archie turns his back on the reader while he's still out of sight, before the smoke.
    A.at(x0, edge);
    A.face(0, Math.PI);

    // Smoke: puffs from the nozzle, rolling out across the stage and piling up in front of where he'll be.
    const puffs = [];
    const nozzle = {x: x0 - 3.6 * ppm + 0.33 * 1.6 * ppm, y: edge - 0.17 * 1.6 * ppm};
    const spots = [[-1.6, 0.2, 1.6], [-0.6, 0.4, 2.0], [0.4, 0.3, 2.2], [1.3, 0.2, 1.8], [-0.2, 1.3, 2.3],
                   [0.9, 1.4, 1.9], [-1.1, 1.2, 1.7], [0.2, 2.2, 1.8]];
    const smoke = async () => {
      for (const [i, [dx, up, k]] of spots.entries()) {
        if (!s.alive) return;
        const puff = await s.prop("smoke-puff");
        if (!s.alive) return;
        const g = puff.at(nozzle.x, nozzle.y, ppm * k * 0.25).root;
        g.traverse(n => { if (n.isMesh) { n.material.transparent = true; n.material.opacity = 0; n.material.depthWrite = false; } });
        puffs.push(puff);
        const to = {x: x0 + dx * ppm, y: edge - up * ppm};
        s.tween(1.1, u => {
          g.position.set(nozzle.x + (to.x - nozzle.x) * u, -(nozzle.y + (to.y - nozzle.y) * u), 120 + i);
          g.scale.setScalar(ppm * k * (0.25 + 0.75 * u));
          g.traverse(n => { if (n.isMesh) n.material.opacity = 0.92 * Math.min(1, u * 1.6); });
        });
        await s.after(0.22);
      }
    };
    await s.after(0.4);
    if (!s.alive) return;
    await smoke();
    if (!s.alive) return;
    await s.after(0.6);
    if (!s.alive) return;

    // Behind the smoke: Archie, facing into the page, strikes the pose; the light snaps on.
    A.show(true);
    A.play("dramatic-entrance/pose", {fade: 0});
    await s.after(0.9);
    if (!s.alive) return;
    beam.forEach(b => { b.visible = true; });
    A.play("dramatic-entrance/hold", {loop: true});
    await s.after(0.6);
    if (!s.alive) return;
    // The smoke clears, up and away.
    await Promise.all(puffs.map(({root: g}, i) => {
      const y0 = g.position.y, x = g.position.x;
      return s.tween(1.6 + i * 0.05, u => {
        g.position.set(x + (i % 2 ? 1 : -1) * 0.6 * ppm * u, y0 + 1.6 * ppm * u, g.position.z);
        g.traverse(n => { if (n.isMesh) n.material.opacity = 0.92 * (1 - u); });
      }, u => u);
    }));
    puffs.forEach(p => p.remove());
    if (!s.alive) return;
    await s.after(1.2);                                  // ...ta-da? (his back to the reader)
    await A.perform("dramatic-entrance/oops");
    if (!s.alive) return;

    // Zip turns him round (or, without Zip, he works it out himself).
    // dramatic_entrance.py: ZIP_X, ZIP_PUSH
    const Z = s.zip, ZX = 0.9, PUSH = 1.0;
    const turned = !!Z && Z.has("dramatic-entrance/turn");
    if (turned) {
      Z.at(H().left - 0.5 * ppm, edge).show(true);
      await Z.walkTo(x0 - ZX * ppm, {clip: "run", mps: 3.75});
      if (!s.alive) return;
      await Z.face(1);
      if (!s.alive) return;
      Z.play("dramatic-entrance/turn");
      await s.until(() => Z.time() >= PUSH || !s.alive);
    } else {
      A.play("idle", {loop: true});
      await s.after(0.3);
    }
    await A.face(0);
    if (!s.alive) return;
    this._aim(s, spot, {x: x0, y: edge - 1.2 * ppm});
    if (turned) { await s.until(() => Z.time() >= 2.1 || !s.alive); Z.play("laugh"); }
    await A.perform("dramatic-entrance/front");
    if (!s.alive) return;
    await s.after(0.5);
  },
})
