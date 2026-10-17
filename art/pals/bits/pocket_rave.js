// The pocket rave. Archie clears his throat and opens the Atlas Core to present a serious project -- and it is
// a nightclub (the rave world): the floor flashing, lasers fanning, a disco ball, Zip on the decks, three
// little agents dancing, and Brick on the door behind the velvet rope. Archie leans in for a closer look and
// the tiny bouncer shakes his head and folds his arms. It's HIS core. Not on the list. He folds it away -- and
// the bass keeps thumping in his hand, and in his belly. The DJ and the bouncer are holo-zip and holo-brick
// playing their own pals' clips; the dancers are holo-agents doing Archie's own dances. The floor's tiles
// flash at 2 Hz in two sets that take turns, a small part of a small picture. Clips: pocket_rave.py.
({
  cast: ["archie"],
  pages: ["home", "topic", "repo", "repos", "catalog", "discover", "collections", "target", "lost"],
  ppm: 140,
  ready(s) {
    return innerWidth >= 1000 && innerHeight >= 620;       // the projection up to his left
  },

  async play(s) {
    const BACK = u => { const c = 1.9, v = u - 1; return 1 + (c + 1) * v * v * v + c * v * v; };   // an overshoot, for s.tween
    const A = s.archie;
    const P = n => `pocket-rave/${n}`;
    const floor = innerHeight - 8, x0 = Math.round(innerWidth * 0.15);
    const SIZE = 600, M = 0.07, BEAT = 0.5;     // the world's width (CSS px); figures' metres -> world; pocket_rave.py
    const core = await s.core(A);
    if (!s.alive) return;

    // In he walks, and clears his throat. This one is serious.
    A.at(-0.45 * A.ppm, floor).show(true);
    A.play("idle", {loop: true});
    await A.walkTo(x0);
    if (!s.alive) return;
    await A.face(0);
    if (!s.alive) return;
    const ahem = A.perform(P("serious"));
    await s.after(0.6);
    if (!s.alive) return;
    A.say("And now: a serious project.", 2.2);
    await ahem;
    if (!s.alive) return;
    const take = A.perform(P("take"));
    await s.after(0.62);                        // _corekit.GRAB
    core.hold();
    await take;
    if (!s.alive) return;
    A.play(P("hold"), {loop: true});
    const present = A.perform(P("present"));
    core.play("unfold");
    await s.after(0.9);
    if (!s.alive) return;
    core.play("open-idle", {loop: true});

    // The club. Zip on the decks, three agents on the floor, Brick on the door.
    const proj = await s.project("rave");
    if (!s.alive || !proj) return;
    const follow = s.tick(() => { const p = core.page(); proj.at(p.x, p.y, SIZE, 1); });
    const w = proj.world, node = n => w.getObjectByName(n) || w;
    const [dj] = await s.figures("holo-zip", 1);
    if (!s.alive) return;
    const [bouncer] = await s.figures("holo-brick", 1);
    if (!s.alive) return;
    const dancers = await s.figures("holo-agent", 3);
    if (!s.alive) return;
    const all = [dj, bouncer, ...dancers];
    node("anchor_dj").add(dj.root);
    dj.root.position.set(0, 0.075, 0.03);       // up on a riser behind the decks, where the floor can see him
    node("anchor_bouncer").add(bouncer.root);
    bouncer.root.rotation.y = -0.35;            // turned a little towards the rope
    dancers.forEach((d, i) => { node("anchor_dancefloor").add(d.root); d.root.position.set((i - 1) * 0.09, 0, 0.05 + 0.02 * (i % 2)); });
    all.forEach(f => f.root.scale.setScalar(1e-4));
    dj.play(dj.clips.dance);
    bouncer.play(bouncer.clips.bouncer);
    ["billy-bounce", "floss", "hype"].forEach((d, i) => { if (A.clips[d]) dancers[i].play(A.clips[d]); });
    await s.after(0.5);
    if (!s.alive) return;
    s.tween(0.4, k => all.forEach(f => f.root.scale.setScalar(M * k + 1e-4)), BACK);
    proj.idle();
    await present;
    if (!s.alive) return;

    // That is not the serious project.
    const look = A.perform(P("double-take"));
    await s.after(0.9);
    if (!s.alive) return;
    A.say("...That is not the project.", 1.8);
    await look;
    if (!s.alive) return;

    // A closer look at the door. Not on the list.
    const lean = A.perform(P("lean-in"));
    await s.after(0.7);
    if (!s.alive) return;
    bouncer.root.rotation.y = 0;
    bouncer.play(bouncer.clips["shake-head"], false);
    await lean;
    if (!s.alive) return;
    const protest = A.perform(P("protest"));
    A.say("It's MY core!", 1.6);
    await s.after(0.5);
    if (!s.alive) return;
    bouncer.play(bouncer.clips.guard, false);
    await s.after(0.9);
    if (!s.alive) return;
    bouncer.play(bouncer.clips["guard-hold"]);
    await protest;
    if (!s.alive) return;

    // He folds it away. The bass carries on.
    await A.perform(P("deadpan"));
    if (!s.alive) return;
    A.say("Moving on.", 1.3);
    proj.hide(0.3);
    await s.after(0.3);
    if (!s.alive) return;
    follow();
    core.play("fold");
    await s.after(0.9);
    if (!s.alive) return;
    const t0 = s.clock();
    const thump = s.tick(() => {              // a bump on every beat: motion, not light
      const u = ((s.clock() - t0) / BEAT) % 1;
      core.root.scale.setScalar(1 + 0.16 * Math.pow(Math.max(0, Math.cos(Math.PI * u)), 6));
    });
    s.page.undo(() => { thump(); core.root.scale.setScalar(1); });
    A.play(P("hold"), {loop: true});
    await s.after(1.5);
    if (!s.alive) return;
    const back = A.perform(P("back"));
    await s.after(0.86);                        // _corekit.DOCK
    core.dock();
    await back;
    if (!s.alive) return;
    A.play("idle", {loop: true});
    await s.after(1.6);
  },
})
