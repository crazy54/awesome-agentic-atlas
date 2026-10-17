// Wrong category. Archie walks in, takes the Atlas Core out of his belly and announces the coding workshop.
// It unfolds onto the creative-media world instead -- a tiny stage, its disco ball turning, its spotlights
// swinging, two little hologram dancers flossing -- whatever page this is. A double take; he holds the Core
// up to his face and taps it; still dancing. He shrugs and joins in, then folds it away. Clips:
// wrong_category.py (and _corekit.py's take/back).
({
  cast: ["archie"],
  pages: ["home", "topic", "repo", "repos", "catalog", "discover", "collections", "target", "lost"],
  ppm: 140,
  ready(s) {
    if (innerWidth < 900 || innerHeight < 600) return false;
    // on the creative-media pages it would be the right category
    const canon = document.querySelector('link[rel="canonical"]');
    return !/creative-voice-media/.test((canon && canon.href) || location.pathname);
  },

  async play(s) {
    const A = s.archie, T = s.T;
    const floor = innerHeight - 8, x0 = Math.round(innerWidth * 0.3);
    const core = await s.core(A);
    if (!s.alive) return;
    A.at(-0.45 * A.ppm, floor).show(true);
    A.play("idle", {loop: true});
    await A.walkTo(x0);
    if (!s.alive) return;
    await A.face(0);
    const take = A.perform("wrong-category/take");
    await s.after(0.62);                                  // _corekit.GRAB
    core.hold();
    await take;
    if (!s.alive) return;
    A.play("wrong-category/hold", {loop: true});
    A.say("Behold: the coding workshop!", 2.4);
    await s.after(0.5);
    core.play("unfold");
    const present = A.perform("wrong-category/present");
    await s.after(0.9);
    if (!s.alive) return;
    core.play("open-idle", {loop: true});

    // The projection: the creative-media world, whatever page this is, up to his left over the Core.
    const SIZE = 270;
    const proj = await s.project("creative-voice-media");
    if (!s.alive || !proj) return;
    const follow = s.tick(() => { const p = core.page(); proj.at(p.x, p.y, SIZE, 1); });
    const w = proj.world, node = n => w.getObjectByName(n);
    const disco = node("disco"), spots = [node("spot_1"), node("spot_2")], stage = node("anchor_stage");
    // the world is shared with every other showing of it: put back what this bit turns and adds
    const turned = [disco, ...spots].filter(Boolean).map(n => [n, n.rotation.clone()]);
    s.page.undo(() => turned.forEach(([n, r]) => n.rotation.copy(r)));
    // Its dance number: the ball turning, the spots swinging, two little hologram dancers flossing.
    const t0 = s.clock();
    const show = s.tick(() => {
      const t = s.clock() - t0;
      if (disco) disco.rotation.y = t * 2.2;
      spots.forEach((sp, i) => { if (sp) sp.rotation.z = 0.45 * Math.sin(t * 2.4 + i * Math.PI); });
    });
    const dances = await s.glb("archie-dances.glb");
    const floss = dances.animations.find(c => c.name === "floss");
    const dancers = await s.figures("holo-agent", 2);
    if (!s.alive) return;
    dancers.forEach((d, i) => {
      (stage || w).add(d.root);
      d.root.position.set(i ? 0.16 : -0.16, 0, 0.02);
      d.root.scale.setScalar(1e-4);
      if (floss) d.play(floss);
    });
    proj.idle();
    const born = s.clock();
    const grow = s.tick(() => {
      const k = Math.min(1, (s.clock() - born) / 0.4);
      for (const d of dancers) d.root.scale.setScalar(0.1 * (1 - Math.pow(1 - k, 3)) + 1e-4);
    });
    await present;
    if (!s.alive) return;
    A.play("wrong-category/hold", {loop: true});
    await s.after(0.6);
    if (!s.alive) return;

    // A double take; the Core up to his face, tapped; still dancing.
    const huh = A.perform("wrong-category/huh");
    await s.after(1.0);
    A.say("...huh?", 1.2);
    await huh;
    if (!s.alive) return;
    A.say("Okay then.", 1.2);
    await A.perform("wrong-category/disco");
    if (!s.alive) return;

    // Folded away.
    proj.hide(0.35);
    await s.after(0.35);
    follow(); show(); grow();
    core.play("fold");
    await s.after(0.9);
    const back = A.perform("wrong-category/back");
    await s.after(0.86);                                  // _corekit.DOCK
    core.dock();
    await back;
    if (!s.alive) return;
    A.play("idle", {loop: true});
    await s.after(0.8);
  },
})
