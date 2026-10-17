// The inspection scam. Archie pops up onto a project's card with a rubber stamp half his size, beams at the
// reader and brings it down on the card without a glance -- "Quality checked!" -- and leaves it standing
// there while he takes the credit. Brick picks it up and turns its face to the reader: I LICKED THIS. So,
// it turns out, does the ink. The stamp and the ink are props over the card, gone when the bit ends; the
// card itself is untouched. Clips: inspection_scam.py.
({
  cast: ["archie", "brick"],
  pages: ["home", "topic", "discover", "collections"],
  ppm: 60,
  _card() {
    for (const e of document.querySelectorAll("article.cx")) {
      const r = e.getBoundingClientRect();
      if (r.width > 200 && r.left > 60 && r.right < innerWidth - 60 && r.top > 200 && r.bottom < innerHeight + 40) return e;
    }
    return null;
  },
  ready(s) { return !!this._card(); },
  // A prop's materials faded to `to` opacity over `secs`.
  _fade(s, prop, to, secs) {
    const mats = [];
    prop.model.traverse(n => { if (n.isMesh) for (const m of [].concat(n.material)) { m.transparent = true; mats.push(m); } });
    const from = mats.map(m => m.opacity);
    return s.tween(secs, u => mats.forEach((m, i) => { m.opacity = from[i] + (to - from[i]) * u; }));
  },
  async play(s) {
    const A = s.archie, ppm = A.ppm, T = s.T;
    const card = this._card();
    if (!card) return;
    const C = () => card.getBoundingClientRect();
    const edge = C().top;
    const x0 = C().left + C().width * 0.32;
    // inspection_scam.py: STAMP_SCALE, STAMP_HOLD, INK_SCALE, STAMP_SHOW, STAMP_HIT, STAMP_LET; the stamp's
    // pad is 0.065 m below its origin (props_hand.py)
    const SC = 8.0, HOLD = 0.055, INK = 3.5, SHOW = 0.25, HIT = 1.35, LET = 2.1, PAD = 0.065;
    const [stamp, ink] = await Promise.all([s.prop("rubber-stamp"), s.prop("stamp-mark-licked")]);
    if (!s.alive) return;
    // flipped beforehand, the way its `flip` clip ends: the head half a turn about its own length (the bone's
    // Y), so the face it prints says I LICKED THIS
    const head = stamp.model.getObjectByName("head");
    if (head) head.quaternion.multiply(new T.Quaternion().setFromAxisAngle(new T.Vector3(0, 1, 0), Math.PI));

    A.clipBelow(edge);
    A.at(x0, edge + 2.6 * ppm).show(true);
    A.play("inspection-scam/hop", {fade: 0});
    await s.tween(0.45, u => A.at(x0, edge + 2.6 * ppm * (1 - u)));
    await s.until(() => A.time() > 1.1 || !s.alive);
    if (!s.alive) return;
    A.clipBelow(null);

    // The stamp, upright in his left hand, held by its shaft.
    const hold = new T.Group();
    hold.add(stamp.root);
    stamp.root.scale.setScalar(SC);
    stamp.root.position.set(0, -HOLD * SC, 0.25);
    const go = A.perform("inspection-scam/stamp");
    await s.until(() => A.time() >= SHOW || !s.alive);
    if (!s.alive) return;
    const off = s.attach(hold, A, "grip_L", {upright: true});
    A.say("Quality checked!", 1.8);
    await s.until(() => A.time() >= LET || !s.alive);
    if (!s.alive) return;
    // Stuck to the card where it came down.
    const w = new T.Vector3();
    stamp.root.getWorldPosition(w);
    off();
    hold.removeFromParent();
    stamp.at(w.x, -w.y, ppm * SC);
    stamp.root.position.z = 60;
    const pad = {x: w.x, y: -w.y + PAD * SC * ppm};
    await go;
    if (!s.alive) return;
    await A.perform("inspection-scam/present");
    if (!s.alive) return;

    // The other side of the story: the stamp's face, turned to the reader.
    // The ink, where the pad was, once the stamp comes off the card.
    const inked = () => { ink.at(pad.x, pad.y + 0.08 * INK * ppm, ppm * INK); ink.root.position.z = 30; };
    // Its pad turned to face the reader, the words the right way up, held by a pal facing `facing`: the
    // stamp's own axes (pad down its -Y, the words' up along its +Z) in that pal's model frame.
    const turnFace = async (secs, facing = 0) => {
      const m = new T.Matrix4();
      if (facing < 0) m.set(0, -1, 0, 0, 0, 0, 1, 0, -1, 0, 0, 0, 0, 0, 0, 1);
      else if (facing > 0) m.set(0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1);
      else m.set(1, 0, 0, 0, 0, 0, 1, 0, 0, -1, 0, 0, 0, 0, 0, 1);
      const q1 = new T.Quaternion().setFromRotationMatrix(m), q0 = new T.Quaternion();
      await s.tween(secs, u => { stamp.root.quaternion.slerpQuaternions(q0, q1, u); });
    };
    // inspection_scam.py: BRICK_X, TURN_TAKE, TURN_FACE; Brick's hand meets the shaft 1.05 m ahead of him
    const B = s.brick, TAKE = 0.8, FACE = 1.6;
    if (B && B.has("inspection-scam/turn")) {
      // up from behind the row of cards, right beside the stamp
      const bx = w.x + 1.05 * ppm;
      B.clipBelow(edge);
      B.at(bx, edge + 3 * ppm).show(true);
      B.play("idle", {loop: true});
      await s.tween(0.6, u => B.at(bx, edge + 3 * ppm * (1 - u)));
      if (!s.alive) return;
      B.clipBelow(null);
      await B.face(-1);
      if (!s.alive) return;
      B.play("inspection-scam/turn");
      await s.until(() => B.time() >= TAKE || !s.alive);
      if (!s.alive) return;
      const h2 = new T.Group();
      stamp.detach();
      h2.add(stamp.root);
      stamp.root.scale.setScalar(SC);
      stamp.root.position.set(0, -HOLD * SC, 0.25);
      s.attach(h2, B, "grip_L", {upright: true});
      inked();
      await s.until(() => B.time() >= FACE || !s.alive);
      if (!s.alive) return;
      await turnFace(0.4, -1);
      if (!s.alive) return;
      A.say("...", 1.0);
    } else {
      const chk = A.perform("inspection-scam/check");
      await s.until(() => A.time() >= 0.3 || !s.alive);
      if (!s.alive) return;
      const h2 = new T.Group();
      stamp.detach();
      h2.add(stamp.root);
      stamp.root.scale.setScalar(SC);
      stamp.root.position.set(0, -HOLD * SC, 0.25);
      s.attach(h2, A, "grip_L", {upright: true});
      await s.until(() => A.time() >= 0.55 || !s.alive);
      if (!s.alive) return;
      inked();
      await s.until(() => A.time() >= 0.75 || !s.alive);
      if (!s.alive) return;
      await turnFace(0.35);
      if (!s.alive) return;
      await chk;
    }
    if (!s.alive) return;
    await A.perform("inspection-scam/stare");
    if (!s.alive) return;
    await this._fade(s, ink, 0, 0.6);
  },
})
