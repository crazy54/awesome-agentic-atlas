// The apology video. After a prank: Archie shuffles on, sits on a chair in front of a video camera, and the
// softbox comes on -- soft, flattering light. The camera rolls. Zip, beside it, holds up a cue card (I AM SO
// SORRY) and Archie reads it out far too cheerfully, with a thumbs-up to finish. Brick, the director, arms
// folded, unfolds them, raises a card of his own and turns it round: LOOK SADDER. Archie gives it everything --
// hands clasped, lip wobbling, the back of his hand to his brow -- and Zip has to wipe an eye. Brick lowers his
// card with a nod, the camera stops, and Archie is up at once: finger guns, "Nailed it!", and off. Brick raises a
// brow at the reader. Clips: apology_video.py (the layout and timings below are its constants).
({
  cast: ["archie", "zip", "brick"],
  pages: ["home", "topic", "repo", "repos", "catalog", "discover", "collections", "target", "lost"],
  ready(s) {
    return innerWidth >= 1100 && innerHeight >= 640;
  },
  async play(s) {
    const {archie: A, zip: Z, brick: B, T} = s;
    const AIM = 0.5, CHAIR_S = 1.2, SEAT_FROM = 0.33, SAY_AT = 1.0, SOB_AT = 2.75, GUNS_AT = 0.45, TURN_AT = 0.35;
    const SHOW = {zip: 0.22, brick: 0.4}, HIDE = {zip: 0.45, brick: 0.65};
    const W = s.W(), floor = innerHeight - 8;
    const P = Math.min(140, (W - 40) / 6.95, (innerHeight - 140) / 3.3);
    const cx = Math.round(W / 2 - 1.575 * P);                     // the chair: the set runs -1.85 m .. 5.0 m
    for (const a of [A, Z, B]) a.ppm = P;
    const names = ["folding-chair", "softbox", "video-camera", "cue-card-sorry", "cue-card"];
    const [chair, softbox, camera, sorry, sadder] = await Promise.all(names.map(n => s.prop(n)));
    if (!s.alive) return;

    // ---- the set: the chair turned to the camera, the softbox off, the cards in their hands but not yet out ----
    chair.at(cx, floor, CHAIR_S * P);
    chair.root.rotation.y = AIM;
    softbox.at(cx - 1.45 * P, floor, P);
    softbox.root.position.z = -0.3 * P;
    softbox.root.rotation.y = 0.8;                                // its diffuser at him
    camera.at(cx + 1.0 * P, floor, P);
    camera.root.position.z = 1.0 * P;                             // in front: we look over its shoulder
    camera.root.rotation.y = -2.33;                               // its lens on him
    const diffusers = [];
    softbox.root.traverse(m => { if (m.isMesh && /holo-soft/.test(m.material.name)) diffusers.push(m.material); });
    const glow = diffusers.map(m => [m, m.emissiveIntensity, m.color.clone()]);
    const dim = k => glow.forEach(([m, e, c]) => { m.emissiveIntensity = e * k; m.color.copy(c).multiplyScalar(0.72 + 0.28 * k); });
    dim(0);
    const lamp = new T.SpotLight(0xffe7c4, 0, 0, 0.42, 1, 0);    // soft, warm, and on him
    lamp.position.set(cx - 1.3 * P, -(floor - 1.5 * P), 0.1 * P);
    lamp.target.position.set(cx + 0.1 * P, -(floor - 1.2 * P), 0.3 * P);
    s.add(lamp);
    s.add(lamp.target);
    // and the light falling on him, a warm haze from the diffuser
    const sx = cx - 1.45 * P + 0.22 * P, haze = s.svg.el("polygon", {opacity: 0, fill: "url(#apology-haze)",
      points: [[sx, floor - 1.78 * P], [cx + 0.4 * P, floor - 2.1 * P], [cx + 0.4 * P, floor - 0.55 * P],
               [sx, floor - 1.12 * P]].map(q => q.join(",")).join(" ")});
    const defs = s.svg.el("defs", {});
    const grad = s.svg.el("linearGradient", {id: "apology-haze", x1: 0, y1: 0, x2: 1, y2: 0}, defs);
    s.svg.el("stop", {offset: 0, "stop-color": "#ffe6a8", "stop-opacity": 0.5}, grad);
    s.svg.el("stop", {offset: 0.7, "stop-color": "#ffe6a8", "stop-opacity": 0.14}, grad);
    s.svg.el("stop", {offset: 1, "stop-color": "#ffe6a8", "stop-opacity": 0}, grad);
    const card = (prop, scale, backwards) => {
      const g = new T.Group();
      g.add(prop.root);
      g.scale.setScalar(scale);
      if (backwards) prop.root.rotation.y = Math.PI;              // its back to the room, until he turns it
      g.visible = false;
      return g;
    };
    const zc = card(sorry, 1.5, false), bc = card(sadder, 1.9, true);
    s.attach(zc, Z, "grip_R");
    s.attach(bc, B, "grip_R");

    // the camera's REC light, as a badge over it: blinking while it rolls
    const cam = {x: cx + 1.0 * P, y: floor - 1.42 * P};
    const rec = s.svg.el("g", {opacity: 0});
    s.svg.el("circle", {cx: cam.x - 16, cy: cam.y, r: 6, fill: "#ff3b30"}, rec);
    const label = s.svg.el("text", {x: cam.x - 6, y: cam.y + 5, fill: "#ff3b30",
                                    style: "font:700 14px/1 system-ui,sans-serif;letter-spacing:.06em"}, rec);
    label.textContent = "REC";
    let rolling = false;
    s.tick(() => { rec.setAttribute("opacity", rolling && s.clock() % 1 < 0.6 ? 1 : 0); });

    // ---- on: Zip and Brick at their places, Archie shuffling in ----
    Z.at(cx + 1.85 * P, floor).depth(0.55 * P).show(true);
    Z.face(-1, -0.5);
    Z.play("idle", {loop: true});
    B.at(cx + 3.7 * P, floor).depth(-0.15 * P).show(true);
    B.face(-1, -0.35);
    B.play("guard-hold", {loop: true});
    const ax = cx + SEAT_FROM * Math.sin(AIM) * P, az = SEAT_FROM * Math.cos(AIM) * P;
    A.at(-0.7 * P, floor).depth(0.6 * P).show(true);
    await A.walkTo(ax, {speed: 0.9});
    if (!s.alive) return;
    const turning = A.face(1, AIM);
    await s.tween(0.4, e => A.depth(0.6 * P + (az - 0.6 * P) * e));
    if (!s.alive) return;
    await turning;
    if (!s.alive) return;
    const sitting = A.perform("apology-video/sit-down");
    await s.after(1.0);
    if (!s.alive) return;
    s.tween(0.25, e => { dim(e); lamp.intensity = 1.6 * e; haze.setAttribute("opacity", e); });   // ka-chunk: on
    await sitting;
    if (!s.alive) return;
    A.play("apology-video/sad", {loop: true});
    await s.after(0.4);
    if (!s.alive) return;
    rolling = true;

    // ---- take one: Zip's card, and Archie reads it out -- cheerfully ----
    await s.after(0.3);
    if (!s.alive) return;
    const zUp = Z.perform("apology-video/card-up");
    await s.after(SHOW.zip);
    if (!s.alive) return;
    zc.visible = true;
    await zUp;
    if (!s.alive) return;
    Z.play("apology-video/card-hold", {loop: true});
    await s.after(0.3);
    if (!s.alive) return;
    const lines = A.perform("apology-video/apology");
    await s.after(SAY_AT);
    if (!s.alive) return;
    A.say("I am so sorry.", 1.5);
    await s.after(1.5);
    if (!s.alive) return;
    const unfold = B.perform("guard-off");                        // Brick has seen enough
    await lines;
    if (!s.alive) return;
    A.play("apology-video/cheesy", {loop: true});
    await unfold;
    if (!s.alive) return;

    // ---- Brick's card: its back to the room, then round ----
    const bUp = B.perform("apology-video/card-up");
    await s.after(SHOW.brick);
    if (!s.alive) return;
    bc.visible = true;
    await bUp;
    if (!s.alive) return;
    B.play("apology-video/card-hold", {loop: true});
    await s.after(0.3);
    if (!s.alive) return;
    const turn = B.perform("apology-video/card-turn");
    await s.after(TURN_AT);
    if (!s.alive) return;
    sadder.play("turn");
    await turn;
    if (!s.alive) return;
    B.play("apology-video/card-hold", {loop: true});

    // ---- take two: the works; Zip is moved ----
    const works = A.perform("apology-video/sadder");
    await s.after(1.4);
    if (!s.alive) return;
    Z.perform("apology-video/moved").then(() => s.alive && Z.play("apology-video/card-hold", {loop: true}));
    await s.after(SOB_AT - 1.4);
    if (!s.alive) return;
    A.say("Sooo sorry!", 1.6);
    await works;
    if (!s.alive) return;
    A.play("apology-video/weep", {loop: true});
    await s.after(1.2);
    if (!s.alive) return;

    // ---- that'll do: Brick's card down with a nod, and the camera stops ----
    const down = B.perform("apology-video/card-down");
    await s.after(HIDE.brick);
    if (!s.alive) return;
    bc.visible = false;
    await down;
    if (!s.alive) return;
    B.play("idle", {loop: true});
    rolling = false;
    await s.after(0.3);
    if (!s.alive) return;
    const perk = A.perform("apology-video/perk-up");
    await s.after(GUNS_AT);
    if (!s.alive) return;
    A.say("Nailed it!", 1.4);
    await s.after(0.4);
    if (!s.alive) return;
    const zDown = Z.perform("apology-video/card-down");
    await s.after(HIDE.zip);
    if (!s.alive) return;
    zc.visible = false;
    await zDown;
    if (!s.alive) return;
    Z.play("idle", {loop: true});
    await perk;
    if (!s.alive) return;

    // ---- off he goes; Brick, at the reader ----
    A.depth(0.6 * P);
    const off = A.walkTo(-0.8 * P);
    await s.after(0.6);
    if (!s.alive) return;
    await B.face(0);
    if (!s.alive) return;
    await B.perform("raise-brow");
    if (!s.alive) return;
    B.play("idle", {loop: true});
    await off;
  },
})
