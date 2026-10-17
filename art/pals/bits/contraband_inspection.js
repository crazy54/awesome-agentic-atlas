// Contraband inspection. Archie takes out the Atlas Core, proudly. Brick, arms folded, unfolds them and holds
// out one enormous hand for it: inspection. Archie hands it over, reluctantly. Brick turns it upside down
// and shakes it like a salt cellar -- out falls the stolen spotlight, three decorative stars and the missing
// light-switch remote. Brick looks at the pile, then at Archie. Archie whistles, hands behind his back,
// looking anywhere else. Clips: contraband_inspection.py (and _corekit.py's take/hold).
({
  cast: ["archie", "brick"],
  pages: ["home", "topic", "repo", "repos", "catalog", "discover", "collections"],
  ppm: 110,
  ready(s) {
    return document.documentElement.clientWidth >= 900 && innerHeight >= 3.3 * 110;
  },

  // The Atlas Core: its glow drawn additively (as archie-core.js does), its clips on a mixer the stage runs,
  // kept on a pal's bone: Archie's `core` (docked), a palm (`on`).
  glow(T, root) {
    root.traverse(m => {
      if (!m.isMesh) return;
      const swap = mat => {
        if (!mat || !/^holo/i.test(mat.name) || mat.isMeshBasicMaterial) return mat;
        const c = mat.emissive && mat.emissive.getHex() ? mat.emissive.clone() : mat.color.clone();
        c.multiplyScalar(Math.min(1.6, Math.max(1, mat.emissiveIntensity || 1)));
        return new T.MeshBasicMaterial({color: c, transparent: true, opacity: mat.opacity < 1 ? mat.opacity : 0.85,
          blending: T.AdditiveBlending, depthWrite: false, side: T.DoubleSide, name: mat.name});
      };
      m.material = Array.isArray(m.material) ? m.material.map(swap) : swap(m.material);
    });
  },
  async core(s, pal) {
    const T = s.T, g = await s.glb("pals/core.glb");
    this.glow(T, g.scene);
    const root = new T.Group(), v = new T.Vector3();
    root.add(g.scene);
    const mixer = s.mixer(g.scene), clips = Object.fromEntries(g.animations.map(c => [c.name, c]));
    let off = null;
    const c = {
      root, scene: g.scene,
      play(name) {
        mixer.stopAllAction();
        const a = mixer.clipAction(clips[name]);
        a.reset().setLoop(T.LoopOnce, 1);
        a.clampWhenFinished = true;
        a.play();
      },
      on(who, bone, offset) { if (off) off(); root.scale.setScalar(1); off = s.attach(root, who, bone, {offset}); },
      world() { root.getWorldPosition(v); return v.clone(); },
    };
    s.page.undo(() => { mixer.stopAllAction(); if (off) off(); root.removeFromParent(); });
    c.play("closed");
    c.on(pal, "core", [0, 0.018, 0]);
    return c;
  },

  async play(s) {
    const A = s.archie, B = s.brick, T = s.T, ppm = 110;
    const W = document.documentElement.clientWidth, floor = innerHeight - 8;
    // contraband_inspection.py: BRICK_X 1.95, HAND_AT 1.7, TAKE_AT 1.3, BRICK_PALM 0, FLIP, SPAWN
    const ax = Math.round(W * 0.36), bx = ax + 1.95 * ppm;
    const HAND_AT = 1.7, TAKE_AT = 1.3, FLIP = [1.9, 4.9], SPAWN = [2.4, 3.2, 3.32, 3.44, 4.25];
    const core = await this.core(s, A);
    const [spot, starG, remote] = await Promise.all([s.prop("spotlight"), s.glb("pals/props/star.glb"),
                                                     s.prop("remote")]);
    if (!s.alive) return;
    spot.model.traverse(n => { if (/beam/i.test(n.name)) n.visible = false; });     // switched off

    // What falls out: each a thing on the page, dropped from the Core with a little sideways kick, bouncing
    // to rest on the floor in front of them.
    const things = [spot.root, ...[0, 1, 2].map(() => { const r = new T.Group(); r.add(starG.scene.clone()); return r; }),
                    remote.root];
    const front = 0.9 * ppm;
    const drop = (obj, i) => {
      const p = core.world();
      s.add(obj);
      obj.scale.setScalar(ppm);
      obj.position.set(p.x, p.y, front);
      let vx = [-0.9, 0.5, -0.3, 0.9, -0.6][i] * ppm, spin = [2.5, -6, 5, -4, 3][i], vy = 0, rz = 0, settled = false;
      const ground = -floor + (i === 0 ? 0.1 : 0.06) * ppm;
      const stop = s.tick(dt => {
        if (settled) return;
        vy -= 9.8 * ppm * dt;
        obj.position.x += vx * dt;
        obj.position.y += vy * dt;
        rz += spin * dt;
        if (obj.position.y <= ground) {
          obj.position.y = ground;
          if (Math.abs(vy) < 0.8 * ppm) { settled = true; rz = Math.round(rz / Math.PI) * Math.PI + (i === 0 ? Math.PI / 2 : 0); stop(); }
          vy = -vy * 0.32; vx *= 0.5; spin *= 0.4;
        }
        obj.rotation.z = rz;
      });
      s.page.undo(() => obj.removeFromParent());
    };

    A.at(ax, floor, ppm).show(true);
    B.at(bx, floor, ppm).show(true);
    B.turn.position.z = -0.3;
    A.play("idle", {loop: true});
    B.play("guard-hold", {loop: true});
    await s.after(0.6);
    if (!s.alive) return;
    const take = A.perform("contraband-inspection/take");
    await s.after(0.62);                                  // _corekit.GRAB
    core.on(A, "grip_L", [0, 0, 0.085]);
    await take;
    if (!s.alive) return;
    A.play("contraband-inspection/hold", {loop: true});
    A.say("My Atlas Core.", 1.6);
    await s.after(1.4);
    if (!s.alive) return;
    await B.perform("guard-off");
    if (!s.alive) return;
    B.say("Inspection.", 1.5);
    // Archie's hand-over and Brick's inspect, started so the Core is at OFFER as Brick's palm gets there
    A.perform("contraband-inspection/hand-over");
    await s.after(HAND_AT - TAKE_AT);
    if (!s.alive) return;
    const insp = B.perform("contraband-inspection/inspect");
    await s.until(() => B.time() >= TAKE_AT || !s.alive);
    if (!s.alive) return;
    core.on(B, "grip_R", [0, 0, 0]);
    // upside down for the shaking, and things falling out of it
    await s.until(() => B.time() >= FLIP[0] - 0.25 || !s.alive);
    const turnTo = (to, secs) => {
      const from = core.scene.rotation.x, t0 = s.clock();
      const stop = s.tick(() => {
        const u = Math.min(1, (s.clock() - t0) / secs);
        core.scene.rotation.x = from + (to - from) * u * u * (3 - 2 * u);
        if (u >= 1) stop();
      });
    };
    turnTo(Math.PI, 0.35);
    for (let i = 0; i < SPAWN.length; i++) {
      await s.until(() => B.time() >= SPAWN[i] || !s.alive);
      if (!s.alive) return;
      drop(things[i], i);
      if (i === SPAWN.length - 1) {
        A.play("contraband-inspection/whistle", {loop: true, fade: 0.4});
      }
    }
    await s.until(() => B.time() >= FLIP[1] || !s.alive);
    turnTo(0, 0.35);
    await s.after(0.6);
    A.say("♪ ~ ♪", 1.8);
    await insp;
    if (!s.alive) return;
    B.play("contraband-inspection/inspect-hold", {loop: true});
    await s.after(0.4);
    A.say("♪ ♪ ~", 1.8);
    await s.after(2.4);
  },
})
