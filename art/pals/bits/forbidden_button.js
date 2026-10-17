// The forbidden button. Zip runs on and a pedestal rises out of the floor beside him: a big red button, DO NOT
// PRESS (a prop: nothing real is behind it). He lunges for it; Archie arrives and holds him off by the dome,
// a finger short. "It says DO NOT PRESS." Zip sulks off, back turned; Archie nods, responsibly. Then, alone
// with it: a look at it, a long look at the reader, a glance at Zip -- and he presses it. Confetti, over
// Archie only. Zip spins round: "HE PRESSED IT!" -- and clicks a remote at it from where he stands: the
// confetti goes off over Archie again. Clips: forbidden_button.py.
({
  cast: ["archie", "zip"],
  pages: ["home", "topic", "repo", "repos", "catalog", "discover", "collections", "target", "lost"],
  ppm: 140,
  ready(s) {
    return innerWidth >= 1000 && innerHeight >= 620;
  },
  async play(s) {
    const A = s.archie, Z = s.zip, ppm = A.ppm;
    const PS = 1.35, ZIP_REACH = 0.8, HOLD_GAP = 0.95, ARCHIE_PRESS = 0.65, ZIP_SULK = 0.9;  // forbidden_button.py
    const PRESS = 3.6, REMOTE = 0.35, CLICK = 0.8;
    const RUN = 0.6 / (0.4 * 0.4);                                                           // clips/zip_base.py
    const floor = innerHeight - 8, px = Math.round(innerWidth * 0.62);
    const z0 = px + ZIP_REACH * ppm, a0 = z0 + HOLD_GAP * ppm, a1 = px + ARCHIE_PRESS * ppm, z1 = a0 + ZIP_SULK * ppm;
    const [ped, remote, ...conf] = await Promise.all([s.prop("do-not-press"), s.prop("remote-zip"),
                                                      ...[0, 1, 2, 3, 4, 5].map(() => s.prop("confetti"))]);
    if (!s.alive) return;
    s.page.undo(() => [ped, remote, ...conf].forEach(p => p.remove()));

    // Confetti over Archie, only Archie: six bursts at once from just over his head, turned about, which
    // rain down round him and fade.
    const mats = conf.map(c => { const m = []; c.model.traverse(n => n.isMesh && m.push(...[].concat(n.material))); return m; });
    // (the prop's pieces fly up most of a metre before they fall: they start at his face, to rain on his head)
    const burst = () => {
      const x = A.x, y = floor - 2.0 * ppm, ys = [];
      conf.forEach((c, i) => {
        c.at(x + (i - 2.5) * 0.05 * ppm, y - (i % 2) * 0.08 * ppm, ppm * 1.3);
        c.root.rotation.y = i * Math.PI / 3 + 0.4;
        c.root.position.z = 30;
        ys.push(c.root.position.y);
        mats[i].forEach(m => { m.transparent = true; m.opacity = 1; });
        c.play("burst");
      });
      // where the clip leaves them, still falling, and gone
      s.after(1.9).then(() => s.tween(0.6, u => {
        conf.forEach((c, i) => { c.root.position.y = ys[i] - 0.7 * ppm * u; });
        mats.forEach(ms => ms.forEach(m => { m.opacity = 1 - u; }));
      }, u => u)).then(() => conf.forEach(c => c.detach()));
    };

    // ---- Zip runs on; the pedestal rises out of the floor beside him; Archie on his way ----
    Z.at(innerWidth + 0.5 * ppm, floor).show(true);
    Z.play("idle", {loop: true});
    await Z.walkTo(z0, {clip: "run", mps: RUN});
    if (!s.alive) return;
    await Z.face(0);
    const low = PS * 1.1 * ppm;
    ped.at(px, floor + low, ppm * PS);
    const delight = Z.perform("forbidden-button/delight");
    s.tween(0.5, u => { ped.root.position.y = -(floor + low * (1 - u)); }, u => 1 + 2.2 * Math.pow(u - 1, 3) + 1.2 * Math.pow(u - 1, 2));
    await s.after(0.6);
    if (!s.alive) return;
    A.at(innerWidth + 0.6 * ppm, floor).show(true);
    const walkIn = A.walkTo(a0, {speed: 1.6});
    s.after(0.3).then(() => s.alive && A.say("Whoa whoa whoa!", 1.3));
    await delight;
    if (!s.alive) return;

    // ---- the lunge; held off by the dome ----
    Z.perform("forbidden-button/reach").then(() => s.alive && Z.play("forbidden-button/strain", {loop: true}));
    await walkIn;
    if (!s.alive) return;
    await A.face(0);
    await A.perform("forbidden-button/restrain");
    if (!s.alive) return;
    A.play("forbidden-button/holding", {loop: true});
    A.say("Ah-ah-ah. It says DO NOT PRESS.", 2.0);
    await s.after(2.0);
    if (!s.alive) return;

    // ---- Zip sulks off past him, his back turned; a responsible nod ----
    A.perform("forbidden-button/release");
    await Z.perform("forbidden-button/deflate");
    if (!s.alive) return;
    Z.say("Hmph.", 0.9);
    Z.depth(-100);                                       // behind Archie, on his way past
    const off = Z.walkTo(z1);
    const nod = A.perform("forbidden-button/nod");
    s.after(0.5).then(() => s.alive && A.say("Responsible.", 1.2));
    await off;
    if (!s.alive) return;
    await Z.face(0, Math.PI);                            // his back to the lot of them
    Z.play("forbidden-button/sulk", {loop: true});
    await nod;
    if (!s.alive) return;

    // ---- alone with it ----
    await A.walkTo(a1);
    if (!s.alive) return;
    await A.face(0);
    A.perform("forbidden-button/tempt");
    await s.after(PRESS);
    if (!s.alive) return;
    ped.play("press");
    burst();
    const cf = A.perform("forbidden-button/confettied", {fade: 0.05});
    await s.after(0.5);
    if (!s.alive) return;

    // ---- sold out, and Zip's own press, by remote, from where he stands ----
    await Z.face(0);
    Z.perform("forbidden-button/snitch");
    Z.say("HE PRESSED IT!", 1.6);
    await cf;
    if (!s.alive) return;
    A.play("idle", {loop: true});
    A.say("It was very tempting.", 1.5);
    await s.after(0.4);
    if (!s.alive) return;
    const ck = Z.perform("forbidden-button/click");
    await s.after(REMOTE);
    remote.hold(Z, "grip_R", [0, 0, 0], [0, Math.PI, 0]);
    remote.root.scale.setScalar(1.6);
    await s.after(CLICK - REMOTE);
    if (!s.alive) return;
    remote.play("click");
    ped.play("press");
    burst();
    const dp = A.perform("forbidden-button/deadpan", {fade: 0.1});
    await ck;
    if (!s.alive) return;

    // ---- Zip off at a run, Archie after him, the pedestal back down ----
    const away = Z.walkTo(innerWidth + 0.7 * ppm, {clip: "run", mps: RUN});
    await s.after(1.4);                                  // the flat look, and after him
    if (!s.alive) return;
    await Promise.all([away, A.walkTo(innerWidth + 0.7 * ppm, {speed: 1.8}),
                       s.after(0.6).then(() => s.tween(0.6, u => { ped.root.position.y = -(floor + low * u); }, u => u * u))]);
  },
})
