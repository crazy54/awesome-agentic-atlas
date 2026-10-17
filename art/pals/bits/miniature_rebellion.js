// The miniature rebellion. Archie opens the Atlas Core on the page's own world, and three tiny hologram
// agents appear on its front edge. Whatever he does, they do, a beat behind: a hand up, a wave, a flex. He
// loves it. Then he tries a little dance -- and stops, mortified. They don't. He folds them away mid-wiggle
// and leaves. The agents are holo-agent props on Archie's own skeleton, playing his clips from this bit's
// pack. Clips: miniature_rebellion.py (and _corekit.py's take/back).
({
  cast: ["archie"],
  pages: ["home", "topic", "repo", "repos", "catalog", "discover", "collections", "target", "lost"],
  ppm: 140,
  ready(s) {
    return innerWidth >= 900 && innerHeight >= 600;
  },

  async play(s) {
    const A = s.archie, T = s.T;
    const floor = innerHeight - 8, x0 = Math.round(innerWidth * 0.3);
    const core = await s.core(A);
    if (!s.alive) return;
    const clip = n => A.clips[`miniature-rebellion/${n}`];
    A.at(-0.45 * A.ppm, floor).show(true);
    A.play("idle", {loop: true});
    await A.walkTo(x0);
    if (!s.alive) return;
    await A.face(0);
    const take = A.perform("miniature-rebellion/take");
    await s.after(0.62);                                  // _corekit.GRAB
    core.hold();
    await take;
    if (!s.alive) return;
    A.play("miniature-rebellion/hold", {loop: true});
    core.play("unfold");
    await s.after(0.9);
    if (!s.alive) return;
    core.play("open-idle", {loop: true});

    // The page's own world, up to his left; three little agents on its front edge.
    const SIZE = 300;
    const proj = await s.project(s.where().world);
    if (!s.alive || !proj) return;
    const follow = s.tick(() => { const p = core.page(); proj.at(p.x, p.y, SIZE, 1); });
    const agents = await s.figures("holo-agent", 3);
    if (!s.alive) return;
    agents.forEach((a, i) => {
      proj.world.add(a.root);
      a.root.position.set((i - 1) * 0.42, 0.03, 0.6);
      a.root.scale.setScalar(1e-4);
      a.play(clip("hold"));
    });
    const born = s.clock();
    const grow = s.tick(() => {
      const k = Math.min(1, (s.clock() - born) / 0.45);
      agents.forEach(a => a.root.scale.setScalar(0.18 * (1 - Math.pow(1 - k, 3)) + 1e-4));
    });
    await s.after(0.8);
    proj.idle();
    await s.after(0.7);
    if (!s.alive) return;

    // Whatever he does, they do, a beat behind (each a hair after the last).
    const copy = (name, delay = 0.35, loop = false) => agents.forEach((a, i) =>
      s.after(delay + 0.07 * i).then(() => { if (s.alive) a.play(clip(name), loop); }));
    for (const [move, line] of [["raise", null], ["wave", "Ha!"], ["flex", "Ha! Yes!"]]) {
      copy(move);
      const done = A.perform(`miniature-rebellion/${move}`);
      if (line) s.after(0.9).then(() => s.alive && A.say(line, 1.1));
      await done;
      if (!s.alive) return;
      await s.after(0.35);
      if (!s.alive) return;
    }

    // A little dance. They copy that too -- and once he stops, they keep going.
    copy("awkward");
    agents.forEach((a, i) => s.after(0.35 + 0.07 * i + 3.0).then(() => { if (s.alive) a.play(clip("awkward-loop"), true); }));
    await A.perform("miniature-rebellion/awkward");
    if (!s.alive) return;
    const caught = A.perform("miniature-rebellion/caught", {fade: 0.05});
    await s.after(1.2);
    A.say("Nobody saw that.", 1.6);
    await caught;
    if (!s.alive) return;
    A.play("miniature-rebellion/hold", {loop: true});
    await s.after(0.8);
    if (!s.alive) return;

    // Folded, mid-wiggle.
    proj.hide(0.3);
    await s.after(0.3);
    follow(); grow();
    core.play("fold");
    await s.after(0.9);
    const back = A.perform("miniature-rebellion/back");
    await s.after(0.86);                                  // _corekit.DOCK
    core.dock();
    await back;
    if (!s.alive) return;
    await A.walkTo(-0.6 * A.ppm, {speed: 1.25});
  },
})
