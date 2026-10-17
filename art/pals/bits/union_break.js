// The union break. Along the bottom of the window, an app card is stuck fast in the floor at a tilt, and Archie,
// behind it, heaves at it: it shudders, and stays. He wipes his brow and whistles for help. In stroll Zip, with
// a picket sign, and Brick, lugging two folding chairs. Zip plants the sign -- YOUR POOR PLANNING IS NOT OUR
// EMERGENCY -- Brick unfolds the chairs beside it, and they sit down, arms folded. Archie stares. He gives up,
// and slumps over the card. The card, the sign and the chairs are props; the page is not touched.
// Clips: union_break.py.
({
  cast: ["archie", "zip", "brick"],
  pages: ["home", "topic", "repo", "repos", "catalog", "discover", "collections", "target", "lost"],
  ppm: 120,
  ready(s) {
    return innerWidth >= 1000 && innerHeight >= 480;       // Brick standing, and the six metres of them
  },

  async play(s) {
    const INOUT = u => u * u * (3 - 2 * u);                // s.tween's easings (its own is an ease-out)
    const A = s.archie, Z = s.zip, B = s.brick, T = s.T, ppm = A.ppm;
    const P = n => `union-break/${n}`;
    // union_break.py: the card; the sign and where Zip plants it from; the chairs, how Brick holds them and
    // sets them down; how far in front of his chair each pal sits; Zip's and Brick's depths, walking in
    const CARD_S = 1.5, CARD_Y = -0.45, CARD_Z = 0.35, TILT = 9 * Math.PI / 180;
    const PULLS = [[0.9, 1.7], [2.0, 2.9]];
    const SIGN_S = 1.3, STICK_GRIP = 0.7 * SIGN_S, PLANT_AT = 0.75, ZIP_PLANT_X = 2.2;
    const CHAIR_S = {zip: 1.0, brick: 1.4}, CHAIR_TOP = {y: 0.18, z: 0.89}, SET_AT = 1.1, BRICK_SET_X = 3.65;
    const SEAT_FROM = {zip: 0.27, brick: 0.5}, ZIP_Y = -0.3, BRICK_Y = -0.25;
    const YAW = -0.6;                                      // chairs and sitters turned towards Archie: the chairs show
    const W = innerWidth, floor = innerHeight - 8;
    const x0 = Math.round(Math.max(ppm + 20, Math.min(W - 5.6 * ppm - 20, 0.3 * W)));   // Archie, behind the card

    const [card, sign, zc, bc] = await Promise.all(["app-card", "picket-sign", "folding-chair", "folding-chair"].map(n => s.prop(n)));
    if (!s.alive) return;
    s.page.undo(() => [card, sign, zc, bc].forEach(p => p.remove()));

    // The card, stuck in the floor: tipped, and cut off at the floor's line.
    card.at(x0, floor - CARD_Z * ppm, ppm * CARD_S);
    card.root.position.z = -CARD_Y * ppm;
    card.root.rotation.z = -TILT;
    const cut = [new T.Plane(new T.Vector3(0, 1, 0), floor)];
    card.model.traverse(m => { if (m.isMesh) [].concat(m.material).forEach(mat => { mat.clippingPlanes = cut; mat.needsUpdate = true; }); });

    // The chairs, folded, each hanging from one of Brick's hands by the middle of its back, turned YAW.
    const v = new T.Vector3();
    const folded = c => { const a = c.play("fold"); if (a) a.time = c.clips.fold.duration; };
    folded(zc);
    folded(bc);
    const hang = (c, sc, bone) => {
      c.at(-1e4, 0, ppm * sc);
      c.root.rotation.y = YAW;
      const back = CHAIR_TOP.y * sc * ppm;                 // the origin, in front of the back's rail
      return s.tick(() => {
        const b = B.bone(bone);
        if (!b) return;
        b.getWorldPosition(v);
        c.root.position.set(v.x + back * Math.sin(YAW), v.y - CHAIR_TOP.z * sc * ppm, v.z + back * Math.cos(YAW));
      });
    };
    // The sign, in Zip's right hand by its stick: turned with him (edge on, as he walks).
    const holder = new T.Group();
    holder.add(sign.root);
    sign.root.position.set(0, -STICK_GRIP, 0);
    sign.root.scale.setScalar(SIGN_S);

    // In he walks, behind the card, and heaves at it. Twice.
    A.at(-0.5 * ppm, floor).show(true);
    A.play("idle", {loop: true});
    await A.walkTo(x0);
    if (!s.alive) return;
    await A.face(0);
    if (!s.alive) return;
    const t0 = s.clock();
    const shudder = s.tick(() => {                          // the card shudders, while he heaves (motion, not light)
      const t = s.clock() - t0;
      const e = PULLS.reduce((m, [a, b]) => Math.max(m, Math.min(1, (t - a) / 0.25, (b - t) / 0.2)), 0);
      card.root.rotation.z = -TILT + 0.012 * Math.max(0, e) * Math.sin(2 * Math.PI * 7 * t);
    });
    const heave = A.perform(P("heave"));
    await s.after(1.0);
    if (!s.alive) return;
    A.say("Hnnngh!", 0.9);
    await s.after(1.1);
    if (!s.alive) return;
    A.say("HNNNGH!", 0.9);
    await heave;
    if (!s.alive) return;
    shudder();
    card.root.rotation.z = -TILT;
    const wipe = A.perform(P("wipe"));
    await s.after(0.5);
    if (!s.alive) return;
    A.say("It's stuck.", 1.2);
    await wipe;
    if (!s.alive) return;

    // He whistles for help. Help arrives, at its own pace.
    const whistle = A.perform(P("whistle"));
    await s.after(0.3);
    if (!s.alive) return;
    Z.at(W + 0.5 * ppm, floor).depth(-ZIP_Y * ppm).show(true);
    B.at(W + 1.4 * ppm, floor).depth(-BRICK_Y * ppm).show(true);
    const offSign = s.attach(holder, Z, "grip_R");
    const offZc = hang(zc, CHAIR_S.zip, "grip_R"), offBc = hang(bc, CHAIR_S.brick, "grip_L");
    const zipIn = Z.walkTo(x0 + ZIP_PLANT_X * ppm, {clip: P("carry-sign")}).then(() => s.alive && Z.face(0));
    const brickIn = B.walkTo(x0 + BRICK_SET_X * ppm, {clip: P("lug"), speed: 1.3}).then(() => s.alive && B.face(0));
    await whistle;
    if (!s.alive) return;
    A.say("Over here!", 1.2);
    await zipIn;
    if (!s.alive) return;

    // Zip plants the sign, and Brick sets the chairs down, and unfolds them.
    const plant = Z.perform(P("plant-sign"));
    await s.after(PLANT_AT);
    if (!s.alive) return;
    sign.root.getWorldPosition(v);
    offSign();
    sign.at(v.x, -v.y, ppm * SIGN_S);                      // standing on its own now
    sign.root.position.z = v.z;
    holder.removeFromParent();
    await brickIn;
    if (!s.alive) return;
    A.say("Great! Grab that end and—", 1.8);
    const set = B.perform(P("set-chairs"));
    await s.after(SET_AT);
    if (!s.alive) return;
    offZc();
    offBc();
    for (const c of [zc, bc]) { c.mixer.stopAllAction(); c.play("unfold"); }
    await plant;
    if (!s.alive) return;

    // They sit down beside it.
    const sit = async (pal, c) => {
      // over to it, and (unseen, in depth) to just in front of it
      const f = SEAT_FROM[pal.name] * ppm;
      const from = pal.x, x1 = c.root.position.x + f * Math.sin(YAW), z0 = pal.z, z1 = c.root.position.z + f * Math.cos(YAW);
      const off = s.tick(() => pal.depth(z0 + (z1 - z0) * INOUT(Math.min(1, Math.abs((pal.x - from) / (x1 - from || 1))))));
      await pal.walkTo(x1, pal === B ? {speed: 1.3} : {});
      if (!s.alive) return;
      off();
      pal.depth(z1);
      await pal.face(0, YAW);
      if (!s.alive) return;
      await pal.perform(P("sit-down"));
      if (s.alive) pal.play(P("seated"), {loop: true});
    };
    const zipSat = sit(Z, zc);
    await s.after(0.5);
    if (!s.alive) return;
    await set;
    if (!s.alive) return;
    const brickSat = sit(B, bc);
    await zipSat;
    if (!s.alive) return;
    Z.say("Union break.", 1.6);
    await brickSat;
    if (!s.alive) return;

    // Archie looks at them. They look back.
    const stare = A.perform(P("stare"));
    await s.after(0.9);
    if (!s.alive) return;
    A.say("...Seriously?", 1.4);
    await stare;
    if (!s.alive) return;
    B.say("Read the sign.", 1.6);
    await s.after(1.8);
    if (!s.alive) return;

    // He gives up.
    await A.perform(P("slump"));
    if (!s.alive) return;
    A.play(P("slump-hold"), {loop: true});
    A.say("...Fine.", 1.3);
    await s.after(1.9);
  },
})
