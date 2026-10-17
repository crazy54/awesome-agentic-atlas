// The victory dance theft. Along the bottom of the window: Archie, "Watch this!", starts his big dance. Brick,
// standing by and unimpressed, casually does his own move -- smooth as anything, ending in a lean no one
// should be able to do, and a point at the reader. Archie has stopped dead and is staring. He slides quietly
// out of the window. Brick raises an eyebrow. Clips: victory_dance_theft.py, and Brick's `much-better`.
({
  cast: ["archie", "brick"],
  pages: ["home", "topic", "catalog", "discover", "collections", "repo"],
  ppm: 62,
  ready(s) {
    return document.documentElement.clientWidth > 7 * 62 && innerHeight > 3.4 * 62;
  },
  async play(s) {
    const A = s.archie, B = s.brick, ppm = 62;
    const W = document.documentElement.clientWidth, floor = innerHeight - 6;
    // victory_dance_theft.py: BRICK_X -3.0, SLINK_SPEED (0.5 / (0.6 * 0.9) m/s, to his left)
    const ax = W - 2.6 * ppm, bx = ax - 3.0 * ppm, SLINK = 0.5 / (0.6 * 0.9);
    A.at(ax, floor, ppm).show(true);
    B.at(bx, floor, ppm).show(true);
    B.turn.position.z = -0.5;
    A.play("idle", {loop: true});
    B.play("victory-dance-theft/watch", {loop: true});
    await s.after(0.7);
    if (!s.alive) return;
    A.say("Watch this!", 1.4);
    await s.after(0.9);
    if (!s.alive) return;
    A.play(A.has("default-dance") ? "default-dance" : "idle", {fade: 0.3});
    await s.after(4.4);
    if (!s.alive) return;
    // Brick's move; a second in, Archie stops dead
    const move = B.perform("much-better", {fade: 0.3});
    await s.after(0.9);
    if (!s.alive) return;
    A.play("victory-dance-theft/stare", {fade: 0.12});
    // side on for the lean (brick_base.py much-better: 5.0-6.7 s), leaning in at Archie, and back
    await s.until(() => B.time() >= 4.75 || !s.alive);
    B.face(1);
    await s.until(() => B.time() >= 6.75 || !s.alive);
    B.face(0);
    await move;
    if (!s.alive) return;
    B.play("idle", {loop: true});
    await s.after(0.5);
    if (!s.alive) return;
    // and away he goes, sideways, quietly
    A.play("victory-dance-theft/slink", {loop: true, fade: 0.3});
    const to = W + 0.9 * ppm, v = SLINK * ppm;
    await new Promise(res => {
      const stop = s.tick(dt => { A.x = Math.min(to, A.x + v * dt); if (A.x >= to || !s.alive) { stop(); res(); } });
    });
    if (!s.alive) return;
    await B.perform("raise-brow");
    B.play("idle", {loop: true});
    await s.after(0.4);
  },
})
