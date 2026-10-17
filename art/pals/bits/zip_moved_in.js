// Zip moved in. Archie walks on, takes out the Atlas Core and shows the reader this page's world -- and in
// the middle of it, tiny, in a lounge chair, a drink with an umbrella in his hand, is Zip. He raises it to
// Archie: cheers. Archie protests; Zip sips. Archie produces the lease, reads it, and turns it to the
// reader: TENANT: ZIP. A flat look. Zip waves him off; Archie folds the Core shut on him and docks it, and
// from his belly comes a slurp. Clips: zip_moved_in.py (and _corekit.py's take/hold/back, _core_gags.py's
// reactions).
({
  cast: ["archie", "zip"],
  pages: ["home", "topic", "repo", "repos", "catalog", "discover", "collections", "target", "lost"],
  ppm: 140,
  ready(s) {
    return innerWidth >= 1000 && innerHeight >= 620;
  },
  async play(s) {
    const A = s.archie, Z = s.zip, T = s.T, ppm = A.ppm;
    const GRAB = 0.62, DOCK = 0.86;                         // _corekit.py
    const LEASE = 0.75, SHOW = 2.6, STOW = 4.6;              // zip_moved_in.py
    const SIZE = 360;                                        // the projection's width, CSS px
    const SC = 0.22;                                         // Zip and his chair in the world: its units (the
                                                             // disc's radius) to the metre
    const floor = innerHeight - 8, x0 = Math.round(innerWidth * 0.3);
    const [core, chair, drink, lease] = await Promise.all([s.core(A), s.prop("lounge-chair"), s.prop("drink"),
                                                           s.prop("lease")]);
    if (!s.alive) return;
    s.page.undo(() => [chair, drink, lease].forEach(p => p.remove()));

    // ---- on, and the Core out ----
    A.at(-0.45 * ppm, floor).show(true);
    A.play("idle", {loop: true});
    await A.walkTo(x0);
    if (!s.alive) return;
    await A.face(0);
    const take = A.perform("zip-moved-in/take");
    await s.after(GRAB);
    core.hold();
    await take;
    if (!s.alive) return;
    A.play("zip-moved-in/hold", {loop: true});
    A.say("Behold: the world of this page!", 2.2);
    await s.after(0.5);
    core.play("unfold");
    const present = A.perform("zip-moved-in/present");
    await s.after(0.9);
    if (!s.alive) return;
    core.play("open-idle", {loop: true});

    // ---- the world, and Zip in it ----
    const proj = await s.project(s.where().world);
    if (!s.alive || !proj) return;
    const follow = s.tick(() => { const p = core.page(); proj.at(p.x, p.y, SIZE, 1); });
    const w = proj.world, anchor = w.getObjectByName("anchor_centre") || w;
    // Zip -- his `turn`, and so all of him -- moved from his place on the page to a spot at the front of the
    // world's middle, with his chair, turned towards Archie; put back when the bit ends. The world is shared
    // with every other showing of it, so the spot comes out of it again too.
    const spot = new T.Group();
    spot.scale.setScalar(SC);
    spot.rotation.y = -0.8;
    anchor.add(spot);
    // to the front of it, clear of the world's own sights in its middle (the disc's radius is 1, the reader
    // at +Z): at least 0.3 out from the middle towards the reader
    const ap = w.worldToLocal(anchor.getWorldPosition(new T.Vector3()));
    spot.position.set(-0.04, 0, Math.max(0, 0.3 - ap.z));
    chair.detach();
    spot.add(chair.root);
    chair.root.position.set(0, 0, 0);
    chair.root.rotation.set(0, 0, 0);
    chair.root.scale.setScalar(1);
    spot.add(Z.turn);
    Z.show(true);
    Z.play("zip-moved-in/lounge", {loop: true});
    drink.hold(Z, "grip_L", [0, 0, 0], [0, 0, Math.PI / 2]);   // upright, along the grip's -X
    drink.root.scale.setScalar(1.6);
    // his speech bubble over his head in the world (the page's own sits a pal's head-height above his head)
    Z.headAt = () => { const p = Z.pageAt("head"); return {x: p.x, y: p.y - 0.8 * SC * SIZE / 2}; };
    s.page.undo(() => {
      spot.removeFromParent();
      Z.root.add(Z.turn);
      Z.turn.position.set(0, 0, 0);
      Z.turn.scale.setScalar(1);
      delete Z.headAt;
    });
    // he pops up with the islands, as they finish rising (the world's appear clip is 0.8 s)
    spot.scale.setScalar(1e-4);
    await s.after(0.55);
    if (!s.alive) return;
    s.tween(0.3, u => spot.scale.setScalar(Math.max(1e-4, SC * u)), u => 1 + 2.7 * Math.pow(u - 1, 3) + 1.7 * Math.pow(u - 1, 2));
    await s.after(0.25);
    proj.idle();
    await present;
    if (!s.alive) return;
    A.play("zip-moved-in/hold", {loop: true});
    await s.after(0.3);

    // ---- a double take; cheers ----
    const dbl = A.perform("zip-moved-in/double-take");
    await s.after(0.8);
    if (!s.alive) return;
    Z.perform("zip-moved-in/cheers").then(() => s.alive && Z.play("zip-moved-in/lounge", {loop: true}));
    await s.after(0.3);
    Z.say("Oh, hey! Cheers.", 1.6);
    await dbl;
    if (!s.alive) return;

    // ---- MY Core; a sip ----
    const prot = A.perform("zip-moved-in/protest");
    A.say("Hey! That's MY Core!", 1.8);
    await s.after(1.6);
    if (!s.alive) return;
    Z.perform("zip-moved-in/sip").then(() => s.alive && Z.play("zip-moved-in/lounge", {loop: true}));
    await s.after(0.4);
    Z.say("*slurrrp*", 1.2);
    await prot;
    if (!s.alive) return;
    A.play("zip-moved-in/hold", {loop: true});
    await s.after(0.6);

    // ---- the lease ----
    const ls = A.perform("zip-moved-in/lease");
    A.say("Hold on.", 0.9);
    await s.after(LEASE);
    if (!s.alive) return;
    lease.hold(A, "grip_R");
    lease.root.scale.setScalar(1.3);
    await s.after(1.1 - LEASE);
    A.say("Let's see... \"Tenant:\"", 1.3);
    await s.after(SHOW - 1.1);
    if (!s.alive) return;
    A.say("\"ZIP\"?!", 1.6);
    await s.after(STOW - SHOW);
    lease.detach();
    await ls;
    if (!s.alive) return;
    await A.perform("zip-moved-in/deadpan");
    if (!s.alive) return;
    A.play("zip-moved-in/hold", {loop: true});

    // ---- bye; folded shut on him ----
    Z.perform("zip-moved-in/bye").then(() => s.alive && Z.play("zip-moved-in/lounge", {loop: true}));
    await s.after(0.3);
    Z.say("Mind the door on your way out.", 1.8);
    await s.after(2.0);
    if (!s.alive) return;
    proj.hide(0.35);
    await s.after(0.35);
    follow();
    spot.removeFromParent();
    core.play("fold");
    await s.after(0.9);
    const back = A.perform("zip-moved-in/back");
    await s.after(DOCK);
    core.dock();
    await back;
    if (!s.alive) return;

    // ---- from his belly: a slurp ----
    Z.headAt = () => core.page(0.1);
    const belly = A.perform("zip-moved-in/belly");
    Z.say("*slurrrp*", 1.2);
    await belly;
    if (!s.alive) return;
    A.play("idle", {loop: true});
    await s.after(0.3);
    await A.walkTo(-0.6 * ppm);
  },
})
