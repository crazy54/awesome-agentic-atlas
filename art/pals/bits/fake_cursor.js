// The fake cursor. Archie and Zip walk on along the bottom of the window. Zip produces a remote and, with a
// click, a pointer: a big, obviously theatrical prop (the reader's own cursor is never touched). He flies
// it over and pokes Archie in the shoulder; Archie jumps. It pokes his head; he swats and misses. It hovers
// in front of his face, wobbling. He snatches it, looks at Zip (who has hidden the remote and is
// whistling), and twists it, squeaking, into a balloon dog, which he hands to Zip. Zip hugs it.
// Clips: fake_cursor.py.
({
  cast: ["archie", "zip"],
  pages: ["home", "topic", "repos", "catalog", "discover", "collections"],
  ppm: 70,
  ready(s) {
    return innerWidth >= 1000 && innerHeight >= 600;
  },
  async play(s) {
    const A = s.archie, Z = s.zip, ppm = A.ppm;
    const ZIP_X = 3.4, GIVE_X = 1.3, GRAB_AT = [0.55, 1.95], GRAB = 0.62, POP = 2.85, HANDOFF = 0.95;
    const REMOTE = 0.7, CLICK = 1.35;                       // fake_cursor.py
    const RUN = 0.6 / (0.4 * 0.4);                           // clips/zip_base.py
    const CS = 1.3;                                          // the pointer prop (0.55 m) a size up
    const floor = innerHeight - 8;
    const ax = Math.round(innerWidth * 0.2), zx = ax + ZIP_X * ppm, gx = ax + GIVE_X * ppm;
    const [cursor, dog, remote] = await Promise.all(["fake-cursor", "balloon-dog", "remote-zip"].map(n => s.prop(n)));
    if (!s.alive) return;
    s.page.undo(() => [cursor, dog, remote].forEach(p => p.remove()));

    // ---- on: Archie walking in from the left, Zip at a run from the right ----
    A.at(-0.6 * ppm, floor).show(true);
    A.play("idle", {loop: true});
    Z.at(innerWidth + 0.7 * ppm, floor).show(true);
    Z.play("idle", {loop: true});
    await Promise.all([A.walkTo(ax), (async () => { await s.after(0.3); await Z.walkTo(zx, {clip: "run", mps: RUN}); })()]);
    if (!s.alive) return;
    await Promise.all([A.face(0), Z.face(0)]);
    A.play("idle", {loop: true});
    Z.play("idle", {loop: true});
    await s.after(0.2);
    if (!s.alive) return;

    // ---- the remote, and the pointer ----
    const dep = Z.perform("fake-cursor/deploy");
    await s.after(REMOTE);
    remote.hold(Z, "grip_R", [0, 0, 0], [0, Math.PI, 0]);
    await s.after(CLICK - REMOTE);
    if (!s.alive) return;
    // where the pointer's tip is (it is its origin), moved by tweens; every frame onto the page
    const at = {x: zx - 0.7 * ppm, y: floor - 1.5 * ppm};
    let free = true;
    cursor.at(at.x, at.y, ppm * CS);
    cursor.root.position.z = 60;
    cursor.play("wobble", {loop: true});
    const fly = s.tick(() => { if (free) cursor.root.position.set(at.x, -at.y, 60); });
    await s.tween(0.3, u => cursor.root.scale.setScalar(Math.max(1e-3, ppm * CS * (u + 0.25 * Math.sin(Math.PI * u)))));
    await dep;
    if (!s.alive) return;
    Z.play("fake-cursor/drive", {loop: true});
    const go = (x, y, secs, ease) => { const fx = at.x, fy = at.y; return s.tween(secs, u => { at.x = fx + (x - fx) * u; at.y = fy + (y - fy) * u; }, ease); };
    const poke = async (tx, ty) => {
      const hx = at.x, hy = at.y;
      cursor.play("poke");
      await go(tx, ty, 0.12, u => u * u);
      await go(hx, hy, 0.3);
      cursor.play("wobble", {loop: true});
    };

    // ---- poke one: his shoulder ----
    let sh = A.pageAt("upper_arm_L");
    await go(sh.x + 0.6 * ppm, sh.y - 0.4 * ppm, 0.9, u => u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2);
    await s.after(0.3);
    if (!s.alive) return;
    sh = A.pageAt("upper_arm_L");
    const p1 = poke(sh.x + 0.08 * ppm, sh.y);
    await s.after(0.12);
    A.perform("fake-cursor/poked");
    A.say("Hey!", 1.0);
    await p1;
    await go(at.x + 0.4 * ppm, at.y - 0.5 * ppm, 0.5);
    await s.after(0.6);
    if (!s.alive) return;

    // ---- poke two: his head; he swats and misses ----
    const hd = () => { const h = A.pageAt("head"); return {x: h.x + 0.15 * ppm, y: h.y - 0.42 * ppm}; };
    await go(hd().x + 0.5 * ppm, hd().y - 0.45 * ppm, 0.6);
    if (!s.alive) return;
    const p2 = poke(hd().x, hd().y);
    await s.after(0.12);
    const swat = A.perform("fake-cursor/swat");
    await p2;
    await go(at.x + 0.8 * ppm, at.y - 0.4 * ppm, 0.25);                // dodged
    await swat;
    if (!s.alive) return;
    A.play("idle", {loop: true});
    await s.after(0.2);
    if (!s.alive) return;

    // ---- it hovers in front of his face, taunting; he grabs it ----
    const gp = {x: ax + GRAB_AT[0] * ppm, y: floor - GRAB_AT[1] * ppm};
    await go(gp.x + 0.1 * ppm, gp.y - 0.05 * ppm, 0.7);
    const taunt = s.tick(() => { at.x = gp.x + 0.1 * ppm + 0.12 * ppm * Math.sin(s.clock() * 7); at.y = gp.y - 0.05 * ppm + 0.06 * ppm * Math.cos(s.clock() * 5); });
    await s.after(0.9);
    if (!s.alive) return;
    const grab = A.perform("fake-cursor/grab");
    await s.after(GRAB - 0.08);
    taunt();
    await go(gp.x, gp.y, 0.08);
    free = false;
    fly();
    const offCursor = s.attach(cursor.root, A, "grip_L", {offset: [0, 0, 0.02]});
    cursor.root.scale.setScalar(CS);
    Z.perform("fake-cursor/caught").then(() => s.alive && Z.play("fake-cursor/innocent", {loop: true}));
    await grab;
    if (!s.alive) return;

    // ---- a look at Zip; twisted into a balloon dog ----
    const twist = A.perform("fake-cursor/twist");
    await s.after(1.25);
    cursor.play("bend");
    A.say("*squeak squeak*", 1.4);
    await s.after(POP - 1.25);
    if (!s.alive) return;
    offCursor();
    cursor.remove();
    const offDog = s.attach(dog.root, A, "grip_L", {offset: [0, 0, 0.04]});
    await s.tween(0.25, u => dog.root.scale.setScalar(Math.max(1e-3, 1.8 * (u + 0.3 * Math.sin(Math.PI * u)))));
    await twist;
    if (!s.alive) return;
    A.play("idle", {loop: true});

    // ---- the hand-over: Zip skips over for it ----
    await Z.walkTo(gx, {clip: "run", mps: RUN});
    if (!s.alive) return;
    await Z.face(0);
    Z.play("fake-cursor/innocent", {loop: true});
    const give = A.perform("fake-cursor/give"), take = Z.perform("fake-cursor/take");
    await s.after(HANDOFF);
    if (!s.alive) return;
    offDog();
    s.attach(dog.root, Z, "grip_R", {offset: [0, 0, 0.04]});
    await Promise.all([give, take]);
    if (!s.alive) return;
    Z.play("fake-cursor/hug", {loop: true});
    A.play("idle", {loop: true});
    Z.say("♥", 1.4);
    await s.after(1.4);
    if (!s.alive) return;
    // off: Zip skipping away with it, Archie the way he came
    await Promise.all([A.walkTo(-0.8 * ppm), Z.walkTo(innerWidth + 0.8 * ppm, {clip: "run", mps: RUN})]);
  },
})
