// The sneeze. Archie unfolds the Atlas Core's world; his nose twitches -- ah... ah... CHOO -- and the
// world's islands blow apart (the world's scatter clip). The main one sails over his head into Brick's hands;
// a little one floats off like a runaway balloon, Zip jumping for it and racing off after it. Brick lobs the
// main one back and the world gathers itself; Zip comes back towing the stray on a string and lets it go
// home. The flying islands are clones on the page; the islands themselves wait, hidden, in the world.
// Clips: the_sneeze.py (and _corekit.py's take/back); Zip plays his everyday jump, run, walk and cheer.
({
  cast: ["archie", "brick", "zip"],
  packs: {archie: "pals/bits/the-sneeze@archie.glb", brick: "pals/bits/the-sneeze@brick.glb"},  // Zip: everyday clips
  pages: ["home", "topic", "repo", "repos", "catalog", "discover", "collections", "target", "lost"],
  ppm: 120,
  ready(s) {
    return innerWidth >= 1100 && innerHeight >= 620;     // Brick on his right, Zip on his left
  },

  async play(s) {
    const A = s.archie, B = s.brick, Z = s.zip, T = s.T;
    const W = innerWidth, floor = innerHeight - 8, x0 = Math.round(W * 0.42);
    const core = await s.core(A);
    if (!s.alive) return;
    // the_sneeze.py: BRICK (-2.4, 0.2), ZIP (2.3, 0), CHOO_AT 0.16, CATCH_AT 0.42, TOSS_AT 0.72
    const bx = x0 - 2.4 * A.ppm, zx = x0 + 2.3 * A.ppm;
    const v = new T.Vector3();
    const pageOf = o => { o.getWorldPosition(v); return {x: v.x, y: -v.y}; };
    // A clone of one of the world's islands, out on the page where the island is (the island itself stays
    // put, hidden, so the world's own clips keep it), and back again.
    const lifted = [];
    s.page.undo(() => lifted.forEach(([o, c]) => { o.visible = true; c.removeFromParent(); }));
    const lift = node => {
      const c = node.clone(true);
      s.scene.add(c);
      node.updateWorldMatrix(true, true);
      node.matrixWorld.decompose(c.position, c.quaternion, c.scale);
      c.position.z = 300;
      node.visible = false;
      lifted.push([node, c]);
      return c;
    };
    const fly = (c, to, secs, height, spin = 0) => {
      const from = c.position.clone(), q0 = c.quaternion.clone(), t0 = s.clock();
      const axis = new T.Vector3(0.3, 0.2, 1).normalize(), dq = new T.Quaternion();
      return s.until(() => {
        const u = Math.min(1, (s.clock() - t0) / secs);
        c.position.set(from.x + (to.x - from.x) * u, from.y + (-to.y - from.y) * u + height * Math.sin(Math.PI * u), 300);
        c.quaternion.copy(q0).premultiply(dq.setFromAxisAngle(axis, spin * u));
        return u >= 1;
      });
    };
    const home = (node, c, secs) => {                     // a clone back to its island, and the island shown
      node.updateWorldMatrix(true, true);
      const p = new T.Vector3(), q = new T.Quaternion(), sc = new T.Vector3();
      node.matrixWorld.decompose(p, q, sc);
      const from = c.position.clone(), q0 = c.quaternion.clone(), s0 = c.scale.clone(), t0 = s.clock();
      return s.until(() => {
        const u = Math.min(1, (s.clock() - t0) / secs), e = 1 - Math.pow(1 - u, 3);
        c.position.lerpVectors(from, p, e);
        c.position.z = 300 * (1 - e);
        c.quaternion.slerpQuaternions(q0, q, e);
        c.scale.lerpVectors(s0, sc, e);
        return u >= 1;
      }).then(() => { node.visible = true; c.removeFromParent(); });
    };

    A.at(x0, floor).show(true);
    B.at(bx, floor).show(true);
    Z.at(zx, floor).show(true);
    B.depth(-0.2 * B.ppm);                                // a little behind Archie
    A.play("idle", {loop: true});
    B.play("idle", {loop: true});
    Z.play("idle", {loop: true});
    await s.after(0.6);
    const take = A.perform("the-sneeze/take");
    await s.after(0.62);                                  // _corekit.GRAB
    core.hold();
    await take;
    if (!s.alive) return;
    A.play("the-sneeze/hold", {loop: true});
    core.play("unfold");
    await s.after(0.9);
    if (!s.alive) return;
    core.play("open-idle", {loop: true});
    const SIZE = 280;
    const proj = await s.project(s.where().world);
    if (!s.alive || !proj) return;
    const follow = s.tick(() => { const p = core.page(); proj.at(p.x, p.y, SIZE, 1); });
    s.after(0.8).then(() => s.alive && proj.idle());
    await s.after(1.6);
    if (!s.alive) return;

    // Ah... ah... CHOO.
    A.say("Ah... ah...", 1.8);
    await A.perform("the-sneeze/ah");
    if (!s.alive) return;
    const choo = A.perform("the-sneeze/choo", {fade: 0.04});
    await s.after(0.16);                                  // CHOO_AT
    A.say("CHOO!", 0.9);
    core.play("sneeze");
    proj.play("scatter");
    await s.after(0.35);
    if (!s.alive) return;

    // The main island over his head into Brick's hands; a little one off like a balloon, Zip after it.
    const w = proj.world;
    const main = w.getObjectByName("island_main") || w.getObjectByName("island_1");
    const stray = w.getObjectByName("island_1") !== main ? w.getObjectByName("island_1") : w.getObjectByName("island_2");
    const mc = main && lift(main), sc = stray && lift(stray);
    let offHands = null, drift = null;
    const catchAt = {x: bx + 0.1 * A.ppm, y: floor - 0.85 * A.ppm};
    const caught = (async () => {
      if (!mc) return;
      const b = B.perform("the-sneeze/catch");
      await fly(mc, catchAt, 0.42, 300, 5);               // lands at CATCH_AT
      if (!s.alive) return;
      mc.scale.setScalar(SIZE / 2 / B.ppm);
      mc.position.z = 0;
      offHands = s.attach(mc, B, "grip_R", {offset: [0, 0.05, 0.16]});
      await b;
      if (s.alive) B.play("the-sneeze/holding", {loop: true});
    })();
    const chased = (async () => {
      if (!sc) return;
      const p0 = {x: sc.position.x, y: -sc.position.y}, t0 = s.clock();
      drift = s.tick(() => {                              // up and away, bobbing
        const t = s.clock() - t0;
        sc.position.set(p0.x + 70 * t + 12 * Math.sin(t * 3), -(p0.y - 55 * t - 10 * Math.sin(t * 4.2)), 300);
        sc.rotation.z = 0.25 * Math.sin(t * 2.1);
      });
      await s.after(0.25);
      await Z.face(1);
      Z.say("Mine!", 0.9);
      await Z.perform("jump");
      if (!s.alive) return;
      await Z.walkTo(W + 0.6 * Z.ppm, {clip: "run", mps: 0.6 / (0.4 * 0.4)});            // zip_base RUN_SPEED
      Z.show(false);
    })();
    await choo;
    if (!s.alive) return;
    A.play("the-sneeze/hold", {loop: true});
    await s.after(0.3);
    A.say("Bless me.", 1.2);
    await A.perform("the-sneeze/sheepish");
    if (!s.alive) return;
    await caught;
    if (!s.alive) return;
    A.play("the-sneeze/hold", {loop: true});

    // Brick lobs it back; the world pulls itself together.
    await s.after(0.3);
    const toss = B.perform("the-sneeze/toss");
    await s.after(0.72);                                  // TOSS_AT
    if (!s.alive) return;
    if (mc) {
      if (offHands) offHands();
      s.scene.attach(mc);
      mc.position.z = 300;
      await home(main, mc, 0.8);
    }
    if (!s.alive) return;
    proj.play("gather");
    await toss;
    if (!s.alive) return;
    B.play("idle", {loop: true});
    await s.after(1.0);
    if (!s.alive) return;

    // Zip back, towing the stray on a string.
    if (sc) {
      if (drift) drift();
      Z.show(true);
      Z.at(W + 0.5 * Z.ppm, floor);
      const string = s.svg.path({stroke: "#7a7f8c", width: 1.5});
      const tow = s.tick(() => {
        const h = Z.pageAt("grip_R"), t = s.clock();
        const top = {x: h.x + 8 * Math.sin(t * 2), y: h.y - 1.0 * Z.ppm + 6 * Math.sin(t * 3)};
        sc.position.set(top.x, -(top.y - 30), 300);
        sc.rotation.z = 0.15 * Math.sin(t * 2.2);
        string.el.setAttribute("d", `M${h.x.toFixed(1)} ${h.y.toFixed(1)} L${top.x.toFixed(1)} ${top.y.toFixed(1)}`);
      });
      await Z.walkTo(zx - 0.6 * A.ppm);
      if (!s.alive) return;
      await Z.face(0);
      tow();
      string.el.remove();
      Z.perform("cheer");
      await home(stray, sc, 0.9);
      if (!s.alive) return;
    }
    A.say("Thanks, both.", 1.4);
    await s.after(1.6);
    if (!s.alive) return;

    proj.hide(0.3);
    await s.after(0.3);
    follow();
    core.play("fold");
    await s.after(0.9);
    const back = A.perform("the-sneeze/back");
    await s.after(0.86);                                  // _corekit.DOCK
    core.dock();
    await back;
    if (!s.alive) return;
    A.play("idle", {loop: true});
    await s.after(1.0);
  },
})
