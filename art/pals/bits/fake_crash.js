// The fake crash. Archie walks on and waves -- and freezes mid-wave, a blue screen on his face (the
// error-face prop). Brick ambles over, peers at him, knocks on his head, and flicks his crest: he spins round to
// face away. Brick steps up and opens the door in his back. In the bay behind it tiny Zip is working two levers
// (the control-box prop), and Archie's raised arm is going with them. Zip freezes, looks round, waves a very
// small wave. Brick looks at the reader and shuts the door. Archie turns back round on his own, the screen goes
// off -- "Rebooted! Good as new." -- and he walks off a little too stiffly. Brick raises a brow at the reader.
// Clips: fake_crash.py (the layout and timings below are its constants).
({
  cast: ["archie", "brick", "zip"],
  pages: ["home", "topic", "repo", "repos", "catalog", "discover", "collections", "target", "lost"],
  ready(s) {
    return innerWidth >= 1100 && innerHeight >= 640;
  },
  async play(s) {
    const {archie: A, brick: B, zip: Z} = s;
    const D1 = 1.7, D2 = 1.6, K = 0.09, BOX = 2.6, SPAN = 0.44, ZIP_DX = 0.018;
    const CRASH = 1.5, FLICK = 1.1, SPIN = -Math.PI, SPIN_SECS = 0.9, ZIP_SHOW = 1.0, ZIP_HIDE = 0.85;
    const WALK = 0.6 / (0.62 * 0.8);                             // archie_base WALK_SPEED: the puppet's stride
    const W = s.W(), P = Math.min(230, (innerHeight - 150) / 2.75), floor = innerHeight - 8;
    const xA = Math.round(W * 0.4);
    for (const a of [A, B]) a.ppm = P;

    // ---- on, and hello ----
    A.at(-0.8 * P, floor).show(true);
    await A.walkTo(xA);
    if (!s.alive) return;
    await A.face(0);
    const screen = await s.prop("error-face");
    if (!s.alive) return;
    const hello = A.perform("fake-crash/hello");
    A.say("Hello! Welcome to th—", 3);
    await s.until(() => A.time() >= CRASH || !s.alive);
    A.hush();
    s.attach(screen.root, A, "head", {offset: [0, 0.178, 0.32], upright: false});
    screen.play("on");
    await hello;
    if (!s.alive) return;
    A.play("fake-crash/frozen", {loop: true, fade: 0});

    // ---- Brick: over, a peer, two knocks ----
    await s.after(0.8);
    B.at(W + 1.6 * P, floor).show(true);
    await B.walkTo(xA + D1 * P);
    if (!s.alive) return;
    await B.face(0);
    await B.perform("fake-crash/peer");
    if (!s.alive) return;
    A.play("fake-crash/knocked", {fade: 0.05});
    await B.perform("fake-crash/knock");
    if (!s.alive) return;
    A.play("fake-crash/frozen", {loop: true, fade: 0.05});

    // ---- the flick: he spins round to face away ----
    const flick = B.perform("fake-crash/flick");
    await s.until(() => B.time() >= FLICK || !s.alive);
    A.play("fake-crash/spun", {fade: 0.05});
    const overshoot = u => { const c = 1.6; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
    await s.tween(SPIN_SECS, e => { A.turnTo = A.turn.rotation.y = SPIN * e; }, overshoot);
    A.facing = 2;
    await flick;
    if (!s.alive) return;
    A.play("fake-crash/frozen", {loop: true, fade: 0.1});

    // ---- the door ----
    await B.walkTo(xA + D2 * P);
    if (!s.alive) return;
    await B.face(0);
    const box = await s.prop("control-box");
    if (!s.alive) return;
    // tiny Zip and his box stand on the bay's ledge, wherever Archie's chest is
    const inBay = () => {
      const b = A.pageAt("bay");
      const zx = b.x + ZIP_DX * P;
      Z.at(zx, b.y, K * P).depth(b.z + 2);
      box.at(zx - SPAN * K * P, b.y, K * BOX * P);
      box.root.position.z = b.z + 3;
      box.root.rotation.y = -Math.PI / 2;                    // its levers swing across the page
    };
    const opening = B.perform("fake-crash/open");
    const door = A.perform("fake-crash/door");
    await s.until(() => A.time() >= ZIP_SHOW || !s.alive);
    inBay();
    const following = s.tick(inBay);
    await Z.face(-1);
    Z.play("fake-crash/levers", {loop: true, fade: 0});
    box.play("operate", {loop: true});
    Z.show(true);
    await Promise.all([opening, door]);
    if (!s.alive) return;
    // the levers have him: his arm and head go with them, in step
    const driven = A.play("fake-crash/driven", {loop: true, fade: 0.1});
    if (driven) driven.time = Z.time();
    await s.after(1.9);
    if (!s.alive) return;

    // ---- caught ----
    let last = Z.time();
    await s.until(() => { const t = Z.time(), wrapped = t < last; last = t; return wrapped || !s.alive; });
    box.mixer.stopAllAction();                               // its levers at rest: where his hands are
    A.play("fake-crash/held", {loop: true, fade: 0.1});
    const caught = Z.perform("fake-crash/caught");
    const stare = B.perform("fake-crash/stare");
    await s.after(1.4);
    Z.say("...hi.", 1.6);
    await Promise.all([caught, stare]);
    if (!s.alive) return;

    // ---- shut ----
    const closing = B.perform("fake-crash/close");
    const shut = A.perform("fake-crash/shut");
    await s.until(() => A.time() >= ZIP_HIDE || !s.alive);
    Z.show(false);
    following();
    box.remove();
    await Promise.all([closing, shut]);
    if (!s.alive) return;
    A.play("fake-crash/frozen", {loop: true, fade: 0.1});
    await s.after(0.7);
    if (!s.alive) return;

    // ---- reboot: round on his own, the screen off ----
    const reboot = A.perform("fake-crash/reboot");
    await s.tween(0.9, e => { A.turnTo = A.turn.rotation.y = SPIN * (1 - e); }, u => u < 0.5 ? 2 * u * u : 1 - 2 * (1 - u) * (1 - u));
    A.facing = 0;
    screen.play("off");
    await s.after(0.35);
    screen.root.visible = false;
    await s.until(() => A.time() >= 1.95 || !s.alive);
    A.say("Rebooted! Good as new.", 1.8);
    await reboot;
    if (!s.alive) return;
    await s.after(0.4);
    const off = A.walkTo(-0.9 * P, {clip: "fake-crash/puppet", mps: WALK});
    await s.after(1.2);
    if (!s.alive) return;
    await B.face(0);
    await B.perform("raise-brow");
    await off;
    if (!s.alive) return;
    await B.walkTo(W + 1.6 * P);
  },
})
