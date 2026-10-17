// The hostile takeover. Archie opens the Atlas Core to show the reader the atlas -- and the miniature agents
// have fortified it (the no-archies world). Two of them heave a NO ARCHIES sign up out of the ground in front
// of the gate while a third marches out to stand guard. He leans in and reads it, and protests: it's HIS core.
// Stop right there, says the guard. Then Zip strolls up and waves, and the agents cheer, step aside, swing the
// gate open and wave him straight through: he hops into the projection and struts in. Archie turns to the
// reader. Clips: hostile_takeover.py (Archie's pieces and the agents'), Zip's everyday clips, holo-zip's own.
({
  cast: ["archie", "zip"],
  packs: {archie: "pals/bits/hostile-takeover@archie.glb", zip: null},     // Zip has no pieces of his own
  pages: ["home", "topic", "repo", "repos", "catalog", "discover", "collections", "target", "lost"],
  ppm: 140,
  ready(s) {
    return innerWidth >= 1100 && innerHeight >= 640;       // the projection up to his left, Zip beside it
  },

  async play(s) {
    const INOUT = u => u * u * (3 - 2 * u);                        // s.tween's easings (its own is an ease-out)
    const BACK = u => { const c = 1.9, v = u - 1; return 1 + (c + 1) * v * v * v + c * v * v; };
    const A = s.archie, Z = s.zip, T = s.T;
    const P = n => `hostile-takeover/${n}`;
    const floor = innerHeight - 8, x0 = Math.round(innerWidth * 0.15);
    const SIZE = 600, M = 0.07;                 // the world's width on the page (CSS px); figures' metres -> world
    const core = await s.core(A);
    if (!s.alive) return;
    const sign = await s.prop("no-archies-sign");
    if (!s.alive) return;
    s.page.undo(() => sign.remove());

    // He walks on and takes the Core out: behold, the atlas.
    A.at(-0.45 * A.ppm, floor).show(true);
    A.play("idle", {loop: true});
    await A.walkTo(x0);
    if (!s.alive) return;
    await A.face(0);
    if (!s.alive) return;
    const take = A.perform(P("take"));
    await s.after(0.62);                        // _corekit.GRAB
    core.hold();
    await take;
    if (!s.alive) return;
    A.play(P("hold"), {loop: true});
    const present = A.perform(P("present"));
    A.say("Behold: the atlas!", 1.8);
    core.play("unfold");
    await s.after(0.9);
    if (!s.alive) return;
    core.play("open-idle", {loop: true});

    // The no-archies fortress, where the atlas should be. Its own sign comes down: the agents put up theirs.
    const proj = await s.project("no-archies");
    if (!s.alive || !proj) return;
    const follow = s.tick(() => { const p = core.page(); proj.at(p.x, p.y, SIZE, 1); });
    const w = proj.world, node = n => w.getObjectByName(n);
    const own = node("sign"), gate = node("gate");
    const gate0 = gate ? gate.rotation.y : 0;
    if (own) own.visible = false;
    s.page.undo(() => { if (own) own.visible = true; if (gate) gate.rotation.y = gate0; });
    // world points: Blender's (x, y, z) is three's (x, z, -y); the island's grass is at z 0.3
    const at = (x, y, z = 0.302) => new T.Vector3(x, z, -y);
    const agents = await s.figures("holo-agent", 3);
    if (!s.alive) return;
    const [zipFig] = await s.figures("holo-zip", 1);
    if (!s.alive) return;
    const spots = [at(-0.3, -0.33), at(-0.1, -0.33), at(0.0, -0.07)];
    agents.forEach((a, i) => { w.add(a.root); a.root.position.copy(spots[i]); a.root.scale.setScalar(1e-4); });
    w.add(sign.root);
    sign.root.position.copy(at(-0.2, -0.22));
    sign.root.scale.set(1, 1e-3, 1);
    await present;
    if (!s.alive) return;
    proj.idle();

    // What? Two agents heave the sign up out of the ground; the third marches out of the gate to guard it.
    const look = A.perform(P("double-take"));
    const grown = s.tween(0.4, k => agents.forEach(a => a.root.scale.setScalar(M * k + 1e-4)), BACK);
    agents[0].play(A.clips[P("agent-heave")]);
    agents[1].play(A.clips[P("agent-heave")]);
    agents[2].root.rotation.y = Math.PI;        // facing in, then out of the gate
    await grown;
    if (!s.alive) return;
    await s.tween(0.9, k => sign.root.scale.set(1, Math.max(1e-3, k), 1), BACK);
    if (!s.alive) return;
    agents[0].play(agents[0].clips.cheer);
    agents[1].play(agents[1].clips.cheer);
    agents[2].root.rotation.y = 0;
    agents[2].play(A.clips.walk).timeScale = 1.6;
    await s.tween(0.9, k => agents[2].root.position.copy(at(0.0, -0.07 - 0.13 * k)), INOUT);
    if (!s.alive) return;
    agents.forEach(a => a.play(a.clips.fold_arms, false));
    await look;
    if (!s.alive) return;

    // He leans in and reads it. No ARCHIES? Stop right there. It's MY core.
    const lean = A.perform(P("lean-in"));
    await s.after(0.6);
    if (!s.alive) return;
    A.say("No ARCHIES?!", 1.5);
    await s.after(0.5);
    if (!s.alive) return;
    agents[2].play(A.clips[P("agent-stop")], false);
    await lean;
    if (!s.alive) return;
    const protest = A.perform(P("protest"));
    A.say("It's MY core!", 1.6);
    // Meanwhile, Zip.
    const zx = Math.min(innerWidth - 0.45 * A.ppm, proj.root.position.x + SIZE / 2 + 0.45 * A.ppm);
    Z.at(innerWidth + 0.5 * A.ppm, floor).show(true);
    const zipIn = Z.walkTo(zx);
    await protest;
    if (!s.alive) return;
    A.play(P("hold"), {loop: true});
    agents[2].play(agents[2].clips.fold_arms, false);
    await zipIn;
    if (!s.alive) return;

    // Zip waves; the agents light up, the guard steps aside, the gate swings open, and he's waved through.
    await Z.face(-1);
    if (!s.alive) return;
    Z.play("wave");
    await s.after(0.5);
    if (!s.alive) return;
    agents[0].play(agents[0].clips.cheer);
    agents[1].play(agents[1].clips.cheer);
    agents[2].root.rotation.y = Math.PI / 2;    // a step to the side, out of the way
    agents[2].play(A.clips.walk).timeScale = 1.6;
    await s.tween(0.6, k => agents[2].root.position.copy(at(0.16 * k, -0.2)), INOUT);
    if (!s.alive) return;
    agents[2].root.rotation.y = 0;
    agents[2].play(A.clips[P("agent-marshal")]);
    if (gate) await s.tween(0.6, k => { gate.rotation.y = gate0 + 1.75 * k; }, BACK);
    if (!s.alive) return;

    // In he goes: a hop off the floor, smaller and smaller, into the projection, and through the gate.
    Z.depth(300);
    const v = new T.Vector3();
    const land = at(0.03, -0.36);
    const pageOf = p => { v.copy(p); w.localToWorld(v); return {x: v.x, y: -v.y}; };
    Z.play("jump");
    await s.after(0.42);
    if (!s.alive) return;
    const from = {x: Z.x, y: Z.y, ppm: Z.ppm}, tiny = M * SIZE / 2;
    await s.tween(0.6, k => {
      const to = pageOf(land);
      Z.at(from.x + (to.x - from.x) * k, from.y + (to.y - from.y) * k - 110 * Math.sin(Math.PI * k),
           from.ppm + (tiny - from.ppm) * k);
    }, INOUT);
    if (!s.alive) return;
    Z.show(false);
    w.add(zipFig.root);
    zipFig.root.position.copy(land);
    zipFig.root.scale.setScalar(M);
    zipFig.play(zipFig.clips.cheer, false);
    await s.after(0.9);
    if (!s.alive) return;
    zipFig.root.rotation.y = Math.PI;           // away from us, through the gate
    zipFig.play(zipFig.clips.walk).timeScale = 2;
    await s.tween(2.0, k => zipFig.root.position.copy(at(0.03 - 0.03 * k, -0.36 + 0.43 * k)), INOUT);
    if (!s.alive) return;
    zipFig.root.visible = false;
    if (gate) s.tween(0.4, k => { gate.rotation.y = gate0 + 1.75 * (1 - k); });
    agents.forEach((a, i) => { a.root.rotation.y = 0; a.play(a.clips.fold_arms, false); });

    // He looks at the reader. Folded away.
    await A.perform(P("deadpan"));
    if (!s.alive) return;
    A.say("Unbelievable.", 1.4);
    await s.after(1.0);
    if (!s.alive) return;
    proj.hide(0.3);
    await s.after(0.3);
    if (!s.alive) return;
    follow();
    core.play("fold");
    await s.after(0.9);
    if (!s.alive) return;
    const back = A.perform(P("back"));
    await s.after(0.86);                        // _corekit.DOCK
    core.dock();
    await back;
    if (!s.alive) return;
    A.play("idle", {loop: true});
    await s.after(0.8);
  },
})
