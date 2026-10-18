// The emergency backup. Archie steps up to show the reader the atlas and reaches for the Atlas Core -- and it
// isn't there. While he pats himself down, Zip runs up with a backup: a potato with continents drawn on it.
// Archie stares at it, and takes it. Brick, who has been waiting behind Zip with his arms folded, plugs a cable
// into it. It lights up: the continents glow and it projects the page's world, a little crooked. It works.
// Archie is furious. The potato and the cable are props, passed from hand to hand at the points
// emergency_backup.py's pieces put the hands on; the continents' light comes on in three steps, a third of a
// second apart. Clips: emergency_backup.py, and Brick's everyday guard (arms folded, while he waits).
({
  cast: ["archie", "zip", "brick"],
  pages: ["home", "topic", "repo", "repos", "catalog", "discover", "collections", "target", "lost"],
  ppm: 140,
  ready(s) {
    return innerWidth >= 1100 && innerHeight >= 640;       // the world up to his right, Zip and Brick to his left
  },

  async play(s) {
    const INOUT = u => u * u * (3 - 2 * u);                // s.tween's easings (its own is an ease-out)
    const A = s.archie, Z = s.zip, B = s.brick, T = s.T, ppm = A.ppm;
    const P = n => `emergency-backup/${n}`;
    // emergency_backup.py: where Zip and Brick stand (metres to Archie's left, and nearer the reader), the
    // hand-offs' moments, the props' sizes, the potato over a palm-up grip and along from Archie's, the plug
    // ahead of Brick's grip, and the plug in the socket, from the potato's middle
    const ZIP_X = 1.0, ZIP_Y = -0.5, BRICK_X = 1.75, BRICK_Y = -0.35, TAKE_AT = 0.75, PLUG_IN = 1.05, GLOW = 0.25;
    const POTATO = 2.4, CABLE = 1.8, LIFT = 0.07, ARCHIE_DX = 0.08, PLUG_OUT = 0.05;
    const PLUGGED = 0.08 * POTATO + 0.035 * CABLE;
    const SIZE = 440, floor = innerHeight - 8;
    const x0 = Math.round(Math.max(innerWidth * 0.42, 1.25 * SIZE + 30));   // room on his right for the world
    const [potato, cable] = await Promise.all([s.prop("potato"), s.prop("cable")]);
    if (!s.alive) return;
    s.page.undo(() => { potato.remove(); cable.remove(); });
    potato.model.scale.setScalar(POTATO);
    cable.model.scale.setScalar(CABLE);

    // The continents: drawn on in green marker, until the cable goes in; then lit, as the Core's holograms are.
    const lands = [];
    potato.model.traverse(m => { if (m.isMesh && /^holo/i.test([].concat(m.material)[0].name)) lands.push(m); });
    const dim = lands.map(m => m.material);
    s.glow(potato.model);
    s.tone(potato.model);
    const lit = lands.map(m => m.material);
    for (const mat of dim.flat()) {                       // (glow() has read their colours: now the marker's)
      if (mat.emissiveIntensity !== undefined) mat.emissiveIntensity = 0;
      mat.color.multiplyScalar(0.6);
    }
    const light = on => lands.forEach((m, i) => { m.material = on ? lit[i] : dim[i]; });
    light(false);
    // The cable's chain, for hanging it from the socket once it's in.
    const chain = [1, 2, 3, 4].map(i => cable.model.getObjectByName(`cable_${i}`)).filter(Boolean);
    const rest = chain.map(b => b.quaternion.clone());
    const droop = () => {
      cable.mixer.stopAllAction();
      const pq = new T.Quaternion(), ax = new T.Vector3(), q = new T.Quaternion();
      chain.forEach((b, i) => {
        b.quaternion.copy(rest[i]);
        b.parent.updateWorldMatrix(true, false);
        b.parent.getWorldQuaternion(pq);
        ax.set(0, 0, 1).applyQuaternion(pq.invert());              // the reader's line of sight, in its parent
        b.quaternion.premultiply(q.setFromAxisAngle(ax, -[0.95, 0.4, 0.2, 0.1][i]));
      });
    };

    // In he walks, to show the reader the atlas, and reaches for the Core. It isn't there.
    A.at(-0.45 * ppm, floor).show(true);
    Z.at(innerWidth + 0.6 * ppm, floor).depth(-ZIP_Y * ppm);     // Zip in front, Brick behind him, Archie behind
    B.at(innerWidth + 1.4 * ppm, floor).depth(-BRICK_Y * ppm);   // them both
    let offPotato = s.attach(potato.root, Z, "grip_R");
    const holder = new T.Group();                          // the plug, in Brick's hand: prongs up, the cable hanging
    holder.add(cable.root);
    let offCable = s.attach(holder, B, "grip_R");
    cable.play("dangle", {loop: true});
    A.play("idle", {loop: true});
    await A.walkTo(x0);
    if (!s.alive) return;
    await A.face(0);
    if (!s.alive) return;
    const search = A.perform(P("search"));
    A.say("Behold: the—", 1.0);
    // Brick on his way in behind, with a cable
    B.show(true);
    // (and waiting with his arms folded, out of the way of the potato)
    const fold = () => B.perform("guard").then(() => { if (s.alive) B.play("guard-hold", {loop: true}); });
    const brickIn = B.walkTo(x0 + BRICK_X * ppm).then(() => s.alive && B.face(0)).then(() => s.alive && fold());
    await s.after(2.0);
    if (!s.alive) return;
    A.say("The Core! It's GONE!", 1.8);

    // Zip, at a run, with the backup.
    Z.show(true);
    await Z.walkTo(x0 + ZIP_X * ppm, {clip: "run", mps: 3.75});
    if (!s.alive) return;
    await Z.face(0);
    if (!s.alive) return;
    Z.say("Backup!", 1.3);
    const offer = Z.perform(P("offer"));
    s.tween(0.8, k => potato.model.position.set(0, LIFT * k, 0), INOUT);   // from his fist to his palm
    await offer;
    if (!s.alive) return;
    Z.play(P("offer-hold"), {loop: true});
    await search;
    if (!s.alive) return;

    // Archie looks at what he's being handed.
    const stare = A.perform(P("stare"));
    await s.after(0.8);
    if (!s.alive) return;
    A.say("...That's a potato.", 1.6);
    await stare;
    if (!s.alive) return;
    Z.say("It has CONTINENTS.", 1.6);
    await s.after(1.1);
    if (!s.alive) return;

    // He takes it, as he would the Core. (Zip's hand and his meet at the potato.)
    const take = A.perform(P("take"));
    await s.after(TAKE_AT);
    if (!s.alive) return;
    offPotato();
    offPotato = s.attach(potato.root, A, "grip_L");
    potato.model.position.set(ARCHIE_DX, LIFT, 0);         // he holds it by its right half
    // and Zip out of Brick's way: in front of him, where he can see
    const aside = Z.perform(P("let-go"))
      .then(() => s.alive && Z.walkTo(x0 + 2.0 * ppm))
      .then(() => s.alive && Z.face(0))
      .then(() => { if (s.alive) Z.play("idle", {loop: true}); });
    await take;
    if (!s.alive) return;
    A.play(P("hold"), {loop: true});
    await brickIn;
    if (!s.alive) return;
    const unfold = B.perform("guard-off");
    await aside;
    if (!s.alive) return;
    await unfold;
    if (!s.alive) return;

    // Brick plugs it in: the plug turned to the socket as his hand comes up, and left in it.
    const plug = B.perform(P("plug"));
    s.after(0.1).then(() => s.tween(0.7, k => {
      cable.root.rotation.z = k * Math.PI / 2;             // prongs to screen left, the cable trailing back
      cable.root.position.x = -PLUG_OUT * k;
    }, INOUT));
    await s.after(PLUG_IN);
    if (!s.alive) return;
    offCable();
    potato.root.add(cable.root);
    cable.root.position.set(ARCHIE_DX + PLUGGED, LIFT, 0);
    cable.root.rotation.set(0, 0, Math.PI / 2);
    droop();
    holder.removeFromParent();

    // It lights up.
    await s.after(GLOW);
    if (!s.alive) return;
    light(true);
    await s.after(0.34);
    if (!s.alive) return;
    light(false);
    await s.after(0.34);
    if (!s.alive) return;
    light(true);
    s.tween(0.5, k => potato.model.scale.setScalar(POTATO * (1 + 0.12 * Math.sin(Math.PI * k))));   // a little jolt
    await plug;
    if (!s.alive) return;
    fold();
    const proj = await s.project(s.where().world);
    if (!s.alive) return;
    if (proj) {
      const v = new T.Vector3();
      s.tick(() => { potato.root.getWorldPosition(v); proj.at(v.x, -v.y - 0.06 * ppm, SIZE, -1); });
      proj.idle();
    }
    Z.say("Ta-da!", 1.3);
    const cheer = Z.perform("cheer");
    await s.after(0.9);
    if (!s.alive) return;
    // a little crooked: a lurch, and it stays tipped
    if (proj) s.tween(0.6, k => { proj.root.rotation.z = 0.11 * k; }, u => 1 - Math.pow(1 - u, 3) * Math.cos(9 * u));
    await cheer;
    if (!s.alive) return;
    Z.play("idle", {loop: true});

    // It works. On a potato.
    const fury = A.perform(P("furious"));
    await s.after(0.3);
    if (!s.alive) return;
    A.say("It runs on a POTATO?!", 2.2);
    await fury;
    if (!s.alive) return;
    A.play(P("hold"), {loop: true});
    B.say("It's a backup.", 1.6);
    await s.after(2.2);
  },
})
