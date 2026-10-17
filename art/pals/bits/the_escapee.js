// The escapee. Archie opens the Atlas Core on the page's own world, and one tiny hologram bot on its front
// edge waves at the reader -- then climbs out, jumps down to the floor by his foot, waves at him and runs off.
// He gets an app card out from behind his back and creeps after it, lays the card on the floor in front of
// it, and when the curious little thing walks on, lifts it and tips it back into the world, where it folds
// its arms and sulks. The bot is the holo-agent prop (Archie's skeleton: it runs with his walk). Clips:
// the_escapee.py (and _corekit.py's take/back).
({
  cast: ["archie"],
  pages: ["home", "topic", "repo", "repos", "catalog", "discover", "collections", "target", "lost"],
  ppm: 140,
  ready(s) {
    return innerWidth >= 1000 && innerHeight >= 600;     // room on his left to run
  },

  async play(s) {
    const A = s.archie, T = s.T;
    const floor = innerHeight - 8, x0 = Math.round(innerWidth * 0.26);
    const core = await s.core(A);
    const card = await s.prop("app-card");
    if (!s.alive) return;
    s.page.undo(() => card.remove());
    const v = new T.Vector3();
    const pageOf = o => { o.getWorldPosition(v); return {x: v.x, y: -v.y}; };
    // `fn(dt)` every frame of the stage's clock until it returns true
    const step = fn => { let last = s.clock(); return s.until(() => { const t = s.clock(), dt = t - last; last = t; return fn(dt); }); };
    A.at(-0.45 * A.ppm, floor).show(true);
    A.play("idle", {loop: true});
    await A.walkTo(x0);
    if (!s.alive) return;
    await A.face(0);
    const take = A.perform("the-escapee/take");
    await s.after(0.62);                                  // _corekit.GRAB
    core.hold();
    await take;
    if (!s.alive) return;
    A.play("the-escapee/hold", {loop: true});
    core.play("unfold");
    await s.after(0.9);
    if (!s.alive) return;
    core.play("open-idle", {loop: true});

    // The page's world, and one little bot on its front edge, waving at the reader.
    const SIZE = 300, BOT = 0.18, BOT_PPM = SIZE / 2 * BOT;    // the bot's metres in world units, in page px
    const proj = await s.project(s.where().world);
    if (!s.alive || !proj) return;
    const follow = s.tick(() => { const p = core.page(); proj.at(p.x, p.y, SIZE, 1); });
    const [bot] = await s.figures("holo-agent", 1);
    if (!s.alive) return;
    proj.world.add(bot.root);
    bot.root.position.set(0.3, 0.03, 0.6);
    bot.root.scale.setScalar(1e-4);
    const born = s.clock();
    const grow = s.tick(() => {
      if (bot.root.parent !== proj.world) return;
      const k = Math.min(1, (s.clock() - born) / 0.45);
      bot.root.scale.setScalar(BOT * (1 - Math.pow(1 - k, 3)) + 1e-4);
    });
    await s.after(0.8);
    proj.idle();
    bot.play(bot.clips.wave, false);
    await s.after(2.0);
    if (!s.alive) return;

    // Out it climbs: off the world's edge and down to the floor by his left foot.
    const jumpTo = async (to, secs, height) => {
      const from = pageOf(bot.root), t0 = s.clock();
      bot.play(bot.clips.cheer);
      await s.until(() => {
        const u = Math.min(1, (s.clock() - t0) / secs);
        const x = from.x + (to.x - from.x) * u, y = from.y + (to.y - from.y) * u - height * Math.sin(Math.PI * u);
        bot.root.position.set(x, -y, 120);              // in front of him
        return u >= 1;
      });
    };
    grow();
    s.scene.attach(bot.root);                             // into the page, where it is now, upright
    bot.root.rotation.set(0, 0, 0);
    bot.root.scale.setScalar(BOT_PPM);
    const land = {x: A.x + 1.0 * A.ppm, y: floor};
    const spot = A.perform("the-escapee/spot");
    await jumpTo(land, 0.75, 70);
    if (!s.alive) return;
    A.say("Hey!", 1.2);
    bot.play(bot.clips.wave, false);
    await spot;
    if (!s.alive) return;

    // It runs off; he gets a card out and creeps after it.
    const run = (dir, dist, speed) => {
      bot.root.rotation.y = dir * Math.PI / 2;
      const a = bot.play(A.clips.walk);
      a.timeScale = speed;
      const x1 = bot.root.position.x + dir * dist;
      return step(dt => {
        bot.root.position.x += dir * 1.21 * speed * BOT_PPM * dt;
        if (dir * (x1 - bot.root.position.x) <= 0) { bot.root.position.x = x1; return true; }
        return false;
      });
    };
    const ran = run(1, 0.95 * A.ppm, 2.2);
    const getCard = A.perform("the-escapee/card");
    await s.after(0.62);                                  // the_escapee.py CARD_ON
    card.hold(A, "grip_R", [0, 0.05, 0.015], [-Math.PI / 2, 0, 0]);
    card.root.scale.setScalar(0.5);
    await Promise.all([ran, getCard]);
    if (!s.alive) return;
    bot.root.rotation.y = 0;
    bot.play(bot.clips.wave, false);                      // cheeky
    A.play("the-escapee/creep", {loop: true});
    const CREEP = 0.24 / (0.6 * 1.0);                     // the_escapee.py CREEP_SPEED, metres a second
    const stopAt = bot.root.position.x - 0.85 * A.ppm;    // the card will lie just short of the bot
    await step(dt => { A.x = Math.min(stopAt, A.x + CREEP * A.ppm * dt); return A.x >= stopAt; });
    if (!s.alive) return;

    // The card on the floor; the bot can't resist it; up it goes, and back in.
    await A.perform("the-escapee/offer");
    if (!s.alive) return;
    await s.after(0.4);
    const pad = pageOf(card.root);
    bot.root.rotation.y = -Math.PI / 2;
    const a = bot.play(A.clips.walk);
    a.timeScale = 1.2;
    await step(dt => { bot.root.position.x -= 1.21 * 1.2 * BOT_PPM * dt; return bot.root.position.x <= pad.x + 0.45 * A.ppm; });
    if (!s.alive) return;
    bot.root.rotation.y = 0;
    await jumpTo({x: pad.x + 4, y: pad.y - 6}, 0.5, 34);  // hop, onto the card
    if (!s.alive) return;
    bot.play(A.clips.idle);
    card.root.attach(bot.root);                           // it rides the card now
    await s.after(0.35);
    const lift = A.perform("the-escapee/lift");
    await s.after(1.2);                                   // the_escapee.py TIP
    if (!s.alive) return;
    proj.world.attach(bot.root);                          // tipped back into the world
    const hop0 = bot.root.position.clone(), q0 = bot.root.quaternion.clone(), s0 = bot.root.scale.x, h0 = s.clock();
    const home = new T.Vector3(0.3, 0.03, 0.6), up = new T.Quaternion();
    s.until(() => {
      const u = Math.min(1, (s.clock() - h0) / 0.5);
      bot.root.position.lerpVectors(hop0, home, u);
      bot.root.position.y += 0.25 * Math.sin(Math.PI * u);
      bot.root.quaternion.slerpQuaternions(q0, up, u);
      bot.root.scale.setScalar(s0 + (BOT - s0) * u);
      return u >= 1;
    }).then(() => { if (s.alive) bot.play(bot.clips.fold_arms, false); });
    await s.after(0.85);                                  // CARD_OFF
    card.root.visible = false;
    await lift;
    if (!s.alive) return;
    A.play("the-escapee/hold", {loop: true});
    A.say("And stay.", 1.4);
    await s.after(1.6);
    if (!s.alive) return;

    // Folded away, sulking bot and all.
    proj.hide(0.3);
    await s.after(0.3);
    follow();
    core.play("fold");
    await s.after(0.9);
    const back = A.perform("the-escapee/back");
    await s.after(0.86);                                  // _corekit.DOCK
    core.dock();
    await back;
    if (!s.alive) return;
    A.play("idle", {loop: true});
    await s.after(0.8);
  },
})
