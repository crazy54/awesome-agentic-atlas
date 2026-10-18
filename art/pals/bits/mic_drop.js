// The mic drop. On top of the spotlight, Archie presents its project into a tiny microphone (a FRAGILE
// sticker on it), holds the mic out at arm's length, lets go and turns away. Brick, beside him, lunges with
// surprising speed and catches it a hand's breadth off the card, looks it over and hands it back -- then taps
// the sticker with one enormous finger, twice. Archie looks at it, and at the reader. Clips: mic_drop.py.
({
  cast: ["archie", "brick"],
  pages: ["home"],
  ppm: 80,
  ready(s) {
    const h = s.page.rect("article.hero");
    return !!h && h.top > 3.0 * 80 && h.top < innerHeight - 60 && h.width > 6 * 80;
  },
  async play(s) {
    const A = s.archie, B = s.brick, T = s.T, ppm = 80;
    const h = s.page.rect("article.hero");
    const floor = h.top, ax = h.left + h.width * 0.55, bx = ax - 2.6 * ppm;     // mic_drop.py BRICK_X
    // mic_drop.py: DROP_AT, CATCH_AT (also the fall's length), HAND_AT, TAKE_LEAD, TAPS
    const DROP_AT = 0.95, FALL = 0.6, HAND_AT = 3.6, TAKE_AT = HAND_AT - 1.2, TAPS = [4.65, 5.2];
    const title = ((document.querySelector("article.hero h2") || {}).textContent || "").trim().slice(0, 24);
    const [mic, tag] = await Promise.all([s.prop("microphone"), s.prop("fragile-label")]);
    if (!s.alive) return;
    // the mic and its sticker, one upright thing held by a grip bone
    const held = new T.Group();
    held.add(mic.root, tag.root);
    tag.root.scale.setScalar(2.1);
    tag.root.position.set(0.0, -0.01, 0.03);
    tag.root.rotation.z = -0.14;
    let off = s.attach(held, A, "grip_R", {upright: true});
    const take = (pal, bone) => { off(); held.scale.setScalar(1); off = s.attach(held, pal, bone, {upright: true}); };
    A.at(ax, floor, ppm).show(true);
    B.at(bx, floor, ppm).show(true);
    B.turn.position.z = -0.6;
    A.play("idle", {loop: true});
    B.play("idle", {loop: true});
    await s.after(0.5);
    if (!s.alive) return;
    const pres = A.perform("mic-drop/present");
    await s.after(0.6);
    A.say(title ? `${title}!` : "Ta-da!", 1.8);
    await pres;
    if (!s.alive) return;
    const drop = A.perform("mic-drop/drop");
    await s.until(() => A.time() >= DROP_AT || !s.alive);
    if (!s.alive) return;
    // let go: the mic falls (gravity's ease) into Brick's left hand, wherever it has got to
    off();
    const w = new T.Vector3();
    held.getWorldPosition(w);
    s.add(held);
    held.position.copy(w);
    held.scale.setScalar(ppm);
    held.quaternion.identity();
    const save = B.perform("mic-drop/save", {fade: 0.06});
    const t0 = s.clock(), from = {x: w.x, y: -w.y};
    await new Promise(res => {
      const stop = s.tick(() => {
        // straight down under gravity, sliding into his palm only at the very end
        const u = Math.min(1, (s.clock() - t0) / FALL), g = B.pageAt("grip_L");
        const k = u < 0.75 ? 0 : (u - 0.75) / 0.25;
        held.position.set(from.x + (g.x - from.x) * k * k, -(from.y + (g.y - from.y) * u * u), w.z);
        if (u >= 1 || !s.alive) { stop(); res(); }
      });
    });
    if (!s.alive) return;
    take(B, "grip_L");
    A.say("Boom.", 1.0);
    await s.until(() => B.time() >= TAKE_AT || !s.alive);
    if (!s.alive) return;
    const back = A.perform("mic-drop/take", {fade: 0.15});
    await s.until(() => B.time() >= HAND_AT || !s.alive);
    if (!s.alive) return;
    take(A, "grip_R");
    // each tap of the finger makes the sticker jump
    for (const at of TAPS) {
      await s.until(() => B.time() >= at || !s.alive);
      if (!s.alive) return;
      if (at === TAPS[0]) B.say("Fragile.", 1.6);
      const t1 = s.clock();
      const stop = s.tick(() => {
        const u = Math.min(1, (s.clock() - t1) / 0.25);
        tag.root.scale.setScalar(2.1 * (1 + 0.25 * Math.sin(Math.PI * u)));
        if (u >= 1) stop();
      });
    }
    await back;
    if (!s.alive) return;
    const sheep = A.perform("mic-drop/sheepish");
    A.say("...oh.", 1.4);
    await save;
    if (!s.alive) return;
    B.play("idle", {loop: true});
    await sheep;
    await s.after(0.4);
  },
})
