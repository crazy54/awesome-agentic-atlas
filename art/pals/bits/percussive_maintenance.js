// Percussive maintenance. Archie takes out the Atlas Core and it won't open: it judders and clamps shut. He
// taps it. Nothing. He whacks it. Nothing. Brick, who has been watching with his arms folded, ambles over and
// gives it one delicate fingertip tap -- and it springs open perfectly, the page's world above it. Archie
// looks at Brick, then at the reader, personally offended. The Core's clips are wont-open and pop-open.
// Clips: percussive_maintenance.py (and _corekit.py's take/back).
({
  cast: ["archie", "brick"],
  pages: ["home", "topic", "repo", "repos", "catalog", "discover", "collections", "target", "lost"],
  ppm: 140,
  ready(s) {
    return innerWidth >= 1000 && innerHeight >= 620;     // room for Brick (2.75 m) beside him
  },

  async play(s) {
    const A = s.archie, B = s.brick;
    const floor = innerHeight - 8, x0 = Math.round(innerWidth * 0.34);
    const core = await s.core(A);
    if (!s.alive) return;
    // percussive_maintenance.py: BRICK (2.0 to Archie's left, 0.25 behind), TAPS, WHACK_AT, TAP_AT
    const bx = x0 + 2.0 * A.ppm, post = Math.min(innerWidth - 1.2 * A.ppm, x0 + 4.4 * A.ppm);
    A.at(-0.45 * A.ppm, floor).show(true);
    B.at(post, floor).show(true);
    B.depth(-0.25 * B.ppm);                               // a little behind Archie
    A.play("idle", {loop: true});
    B.play("guard-hold", {loop: true});
    await A.walkTo(x0);
    if (!s.alive) return;
    await A.face(0);
    const take = A.perform("percussive-maintenance/take");
    await s.after(0.62);                                  // _corekit.GRAB
    core.hold();
    await take;
    if (!s.alive) return;
    A.play("percussive-maintenance/hold", {loop: true});
    A.say("Open up.", 1.0);
    await s.after(0.3);
    await s.after(core.play("wont-open"));
    if (!s.alive) return;

    // A careful tap or two; nothing. A whack; nothing.
    const tap = A.perform("percussive-maintenance/tap");
    await s.after(0.95);
    core.play("wont-open");
    await tap;
    if (!s.alive) return;
    A.play("percussive-maintenance/hold", {loop: true});
    await s.after(0.9);
    if (!s.alive) return;
    A.say("Come on...", 1.1);
    const whack = A.perform("percussive-maintenance/whack");
    await s.after(0.62);
    core.play("wont-open");
    await whack;
    if (!s.alive) return;
    A.play("percussive-maintenance/hold", {loop: true});
    A.say("Ugh.", 1.0);
    await s.after(0.7);
    if (!s.alive) return;

    // Brick ambles over. One fingertip.
    await B.perform("guard-off");
    if (!s.alive) return;
    await B.walkTo(bx);
    if (!s.alive) return;
    await B.face(0);
    const tc = B.perform("percussive-maintenance/tap-core");
    await s.after(1.25);                                  // TAP_AT
    if (!s.alive) return;
    core.play("pop-open");
    await s.after(0.5);
    core.play("open-idle", {loop: true});
    const proj = await s.project(s.where().world);
    if (!s.alive || !proj) return;
    // on his right this time (screen left): Brick is on his left
    const follow = s.tick(() => { const p = core.page(); proj.at(p.x, p.y, 280, -1); });
    s.after(0.8).then(() => s.alive && proj.idle());
    await tc;
    if (!s.alive) return;
    B.play("idle", {loop: true});

    // Archie looks at Brick. Then at you.
    const off = A.perform("percussive-maintenance/offended");
    await s.after(2.1);
    A.say("I loosened it.", 1.6);
    await off;
    if (!s.alive) return;
    A.play("percussive-maintenance/hold", {loop: true});
    await s.after(0.6);
    if (!s.alive) return;

    proj.hide(0.3);
    await s.after(0.3);
    follow();
    core.play("fold");
    await s.after(0.9);
    const back = A.perform("percussive-maintenance/back");
    await s.after(0.86);                                  // _corekit.DOCK
    core.dock();
    const away = B.walkTo(post);
    await back;
    if (!s.alive) return;
    A.play("idle", {loop: true});
    await away;
    if (!s.alive) return;
    B.play("guard-hold", {loop: true});
    await s.after(0.8);
  },
})
