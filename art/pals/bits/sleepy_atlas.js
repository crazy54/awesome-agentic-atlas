// The sleepy atlas. In an idle moment Archie takes out the Atlas Core, hugs it like a teddy bear, sits down on
// the floor and nods off. Its lights pulse gently, and a little hologram of him (holo-archie) floats over it,
// holding forth in his sleep. Zip tiptoes in with a marker and very carefully draws a mustache on it (the
// mustache prop, on the hologram's head), then tiptoes off, shaking with silent laughter. Archie stirs, gets
// up, docks the Core and wanders off, none the wiser. Clips: sleepy_atlas.py (and _corekit.py's take).
({
  cast: ["archie", "zip"],
  pages: ["home", "topic", "repo", "repos", "catalog", "discover", "collections", "target", "lost"],
  ppm: 140,
  ready(s) {
    return innerWidth >= 1000 && innerHeight >= 600;
  },

  async play(s) {
    const A = s.archie, Z = s.zip, T = s.T;
    const W = innerWidth, floor = innerHeight - 8, x0 = Math.round(W * 0.6);
    const core = await s.core(A);
    const [marker, mustache] = await Promise.all([s.prop("marker"), s.prop("mustache")]);
    const [holo] = await s.figures("holo-archie", 1);
    if (!s.alive) return;
    s.page.undo(() => { marker.remove(); mustache.remove(); });
    // sleepy_atlas.py: ZIP (0.85, -0.3), HUG_AT 0.7, DOCK_AT 2.0, HOLO_SCALE 0.3, HOLO_AT (0.42, 0.15),
    // DRAW (1.15, 2.05)
    const zx = x0 + 0.85 * A.ppm, v = new T.Vector3();
    const SNEAK = 0.32 / (0.62 * 1.2);                     // zip_base SNEAK_SPEED

    A.at(x0, floor).show(true);
    A.play("idle", {loop: true});
    await s.after(0.8);
    if (!s.alive) return;
    const take = A.perform("sleepy-atlas/take");
    await s.after(0.62);                                  // _corekit.GRAB
    core.hold();
    await take;
    if (!s.alive) return;

    // A hug, a yawn, down onto the floor, asleep. The Core rides his chest from HUG_AT.
    const hs = A.perform("sleepy-atlas/hug-sit");
    await s.after(0.7);                                   // HUG_AT
    if (!s.alive) return;
    const chest = A.bone("chest");
    chest.updateWorldMatrix(true, false);
    core.root.getWorldPosition(v);
    const at = chest.worldToLocal(v.clone());
    // (laid over hold(): an attachment made later wins, and it goes before the Core is docked)
    const onChest = s.attach(core.root, A, "chest", {offset: [at.x, at.y, at.z]});
    await hs;
    if (!s.alive) return;
    A.play("sleepy-atlas/doze", {loop: true});

    // Its light, pulsing gently (the Core is shared: its glow is put back after).
    const lights = [];
    core.scene.traverse(m => { if (m.isMesh && m.material && /^holo/.test(m.material.name)) lights.push([m.material, m.material.color.clone()]); });
    s.page.undo(() => lights.forEach(([m, c]) => m.color.copy(c)));
    const t0 = s.clock();
    const pulse = s.tick(() => {
      const k = 0.5 + 0.5 * Math.sin((s.clock() - t0) * Math.PI * 2 / 2.6);
      lights.forEach(([m, c]) => m.color.copy(c).multiplyScalar(0.35 + 0.75 * k));
    });
    await s.after(1.0);
    if (!s.alive) return;

    // A little hologram of him over it, holding forth in his sleep.
    s.scene.add(holo.root);
    let shown = 0, showTo = 1, showAt = s.clock();
    const float = s.tick(() => {
      const u = Math.min(1, (s.clock() - showAt) / 0.5), e = 1 - Math.pow(1 - u, 3);
      shown = showTo ? e : 1 - e;
      const p = core.page(0), t = s.clock();
      holo.root.position.set(p.x + 0.42 * A.ppm, -(p.y - 0.15 * A.ppm - 4 * Math.sin(t * 2)), 200);
      holo.root.scale.setScalar(Math.max(1e-4, 0.3 * A.ppm * shown));
    });
    if (holo.clips.pompous) holo.play(holo.clips.pompous);
    await s.after(2.0);
    if (!s.alive) return;

    // Zip, on tiptoe, with a marker.
    marker.hold(Z, "grip_R");
    Z.at(W + 0.5 * Z.ppm, floor).show(true);
    Z.depth(0.3 * Z.ppm);                                 // in front of Archie, sat on the floor
    await Z.walkTo(zx, {clip: "sneak", mps: SNEAK, speed: 1.6});   // a brisk tiptoe
    if (!s.alive) return;
    await Z.face(0);
    const head = holo.model.getObjectByName("head");
    // on the bootleg's upper lip (its head is half as big again as his: props_holo.holo_archie), drawn big
    if (head) { head.add(mustache.root); mustache.root.position.set(0, 0.333, 0.45); mustache.root.scale.setScalar(2.6); }
    mustache.root.visible = false;
    const dr = Z.perform("sleepy-atlas/draw");
    await s.after(1.15);                                  // DRAW
    if (!s.alive) return;
    mustache.root.visible = true;
    mustache.play("draw");
    await dr;
    if (!s.alive) return;
    const off = Z.walkTo(W + 0.6 * Z.ppm, {clip: "sneak", mps: SNEAK, speed: 1.6});
    await s.after(2.4);
    if (!s.alive) return;

    // He stirs; the hologram goes; up, the Core back home, and off, none the wiser.
    const wake = A.perform("sleepy-atlas/wake");
    await s.after(0.3);
    showTo = 0; showAt = s.clock();
    await s.after(1.7);                                   // DOCK_AT
    if (!s.alive) return;
    pulse();
    lights.forEach(([m, c]) => m.color.copy(c));
    onChest();
    core.dock();
    await wake;
    if (!s.alive) return;
    float();
    A.play("idle", {loop: true});
    await off;
    await s.after(0.5);
    if (!s.alive) return;
    await A.walkTo(-0.6 * A.ppm);
  },
})
