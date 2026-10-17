// The tiny inspection. An access panel on the page's glass, low down by the bottom of the window. Zip runs
// past it, stops, comes back and knocks: hollow. He kits up -- a violet hard hat, a flashlight -- heaves the panel up and
// duck-walks in under it, and it drops shut behind him. His inspection light moves about inside: it leaks
// round the panel's dark seams, glints through its empty screw holes, fans out under it across the floor; a
// thump, a "hmm". Then the panel lifts in a puff of dust and he comes out wearing an enormous dust bunny,
// which looks at the reader. He looks up at it, sneezes, and runs off in it. Clips: tiny_inspection.py.
({
  cast: ["zip"],
  pages: ["topic", "repos", "catalog", "collections"],
  ppm: 80,
  ready(s) {
    return innerWidth >= 900 && innerHeight >= 560;
  },
  // A prop's clip run forwards (dir 1) or back to its start (dir -1), and held there.
  _run(s, prop, name, dir = 1) {
    const T = s.T, c = prop.clips[name];
    if (!c) return;
    const a = prop.mixer.clipAction(c);
    a.setLoop(T.LoopOnce, 1);
    a.clampWhenFinished = true;
    a.paused = false;
    a.timeScale = dir;
    if (!a.isRunning()) { a.reset(); a.timeScale = dir; if (dir < 0) a.time = c.duration; }
    a.play();
  },
  async play(s) {
    const Z = s.zip, ppm = Z.ppm, T = s.T;
    const GAP = 0.42, TORCH = 0.75, HAT = 1.45, LIFT = 0.45, SNEEZE = 1.05;    // tiny_inspection.py
    const DUCK = 0.24 / (0.6 * 0.6);                                             // DUCK_SPEED
    const RUN = 0.6 / (0.4 * 0.4);                                               // clips/zip_base.py
    const floor = innerHeight - 8;
    const PS = ppm * 2.3;                                  // the panel (0.9 x 0.6 m as built) at Zip's scale
    const pw = 0.9 * PS, ph = 0.6 * PS;
    const left = Math.round(innerWidth * 0.62), right = left + pw, bottom = floor - 0.1 * ppm, top = bottom - ph;
    const [panel, torch, hat, bunny, puff] = await Promise.all(
      ["wall-panel", "flashlight", "hard-hat-orange", "dust-bunny", "smoke-puff"].map(n => s.prop(n)));
    if (!s.alive) return;
    s.page.undo(() => [panel, torch, hat, bunny, puff].forEach(p => p.remove()));
    panel.at(left + pw / 2, top + ph / 2, PS);
    panel.root.position.z = -40;                           // on the wall, behind him
    // the hole in the wall behind it, dark, shown as the panel swings up
    const hole = new T.Mesh(new T.PlaneGeometry(0.86, 0.56), new T.MeshBasicMaterial({color: 0x0b0c10}));
    hole.position.z = -0.02;
    panel.root.add(hole);
    const flap = panel.model.getObjectByName("panel");
    // a thump from inside rattles it: a shake on top of wherever its clip has it this frame (the stage runs
    // the mixers before the tickers), so it never holds the flap away from the clip's pose
    let jolt = 0;
    const axis = new T.Vector3(0, 0, 1), dq = new T.Quaternion();
    const rattle = s.tick(dt => {
      if (!flap || jolt < 0.001) return;
      const k = jolt * Math.sin(s.clock() * 70);
      jolt *= Math.exp(-9 * dt);                           // dying away over a third of a second, at any fps
      flap.quaternion.multiply(dq.setFromAxisAngle(axis, 0.035 * k));
    });
    const thump = (k = 1) => { jolt = k; };
    s.holo(torch.root);
    const beam = torch.model.getObjectByName("beam");
    if (beam) beam.visible = false;

    // ---- past it at a run, back to it, and the knock ----
    Z.at(innerWidth + 0.6 * ppm, floor).show(true);
    Z.play("idle", {loop: true});
    await Z.walkTo(left - GAP * ppm, {clip: "run", mps: RUN});
    if (!s.alive) return;
    await Z.face(1);
    await Z.perform("tiny-inspection/knock");
    if (!s.alive) return;
    Z.say("hollow!", 1.2);

    // ---- kit up: the torch from behind his back, the hat on ----
    await Z.face(0);
    const kit = Z.perform("tiny-inspection/kit-up");
    await s.after(TORCH);
    torch.hold(Z, "grip_R", [0, 0, 0]);                  // its beam along grip_R's Y: where his fingers point
    await s.after(HAT - TORCH - 0.25);
    if (!s.alive) return;
    hat.hold(Z, "head", [0, 1.4, 0.02]);
    await s.tween(0.25, u => { hat.root.position.y = 1.4 - (1.4 - 0.33) * u; }, u => u * u);
    await s.after(0.35);
    if (!s.alive) return;
    if (beam) beam.visible = true;                         // click: on
    await kit;
    if (!s.alive) return;

    // ---- in under the panel ----
    await Z.face(1);
    const lift = Z.perform("tiny-inspection/lift");
    await s.after(LIFT);
    this._run(s, panel, "lift", 1);
    await lift;
    if (!s.alive) return;
    Z.clipRight(left + 2);
    await Z.walkTo(left + 0.75 * ppm, {clip: "tiny-inspection/duck", mps: DUCK});   // all of him past the edge
    if (!s.alive) return;
    Z.show(false);
    if (beam) beam.visible = false;
    this._run(s, panel, "lift", -1);
    await s.after(0.7);
    if (!s.alive) return;
    thump(1);

    // ---- the inspection: his light moving about inside, leaking out ----
    // (drawn in this order, back to front: the fan of light on the floor, the seams, the light in them, the
    // empty screw holes and the light through them)
    const g = s.svg.el("g");
    const el = (tag, attrs, parent = g) => s.svg.el(tag, attrs, parent);
    const defs = el("defs", {});
    const grad = el("linearGradient", {id: "zip-fan", x1: "0", y1: "0", x2: "0", y2: "1"}, defs);
    el("stop", {offset: "0", "stop-color": "#ffd23a", "stop-opacity": "0.9"}, grad);
    el("stop", {offset: "1", "stop-color": "#ffd23a", "stop-opacity": "0"}, grad);
    const blur = el("filter", {id: "zip-glow", x: "-50%", y: "-50%", width: "200%", height: "200%"}, defs);
    el("feGaussianBlur", {stdDeviation: "2.5"}, blur);
    const fan = el("polygon", {fill: "url(#zip-fan)", opacity: 0});
    // the panel's seams, dark (so the light in them reads on a light page as well as a dark one), and the
    // light in each
    const seam = [[left, top - 1.5, pw, 3], [left, bottom - 1.5, pw, 3], [left - 1.5, top, 3, ph], [right - 1.5, top, 3, ph]];
    seam.forEach(([x, y, w, h]) => el("rect", {x: x - 0.5, y: y - 0.5, width: w + 1, height: h + 1, fill: "#15161b", opacity: 0.8, rx: 2}));
    const edges = seam.map(([x, y, w, h]) => el("rect", {x: x - 1, y: y - 1, width: w + 2, height: h + 2, fill: "#ffd84a",
                                                     opacity: 0, rx: 2, filter: "url(#zip-glow)"}));
    const spots = [[right - 0.06 * PS, top + 0.06 * PS], [left + 0.06 * PS, bottom - 0.06 * PS], [right - 0.06 * PS, bottom - 0.06 * PS]];
    spots.forEach(([cx, cy]) => el("circle", {cx, cy, r: 3.8, fill: "#15161b", opacity: 0.85}));
    const holes = spots.map(([cx, cy]) => el("circle", {cx, cy, r: 5, fill: "#ffe66b", opacity: 0, filter: "url(#zip-glow)"}));
    const t0 = s.clock();
    let on = 1;
    const light = s.tick(() => {
      const t = s.clock() - t0;
      // where the light is inside, roaming
      const lx = left + pw * (0.5 + 0.42 * Math.sin(t * 1.3) * Math.cos(t * 0.37));
      const ly = top + ph * (0.55 + 0.35 * Math.sin(t * 2.1 + 1));
      const near = (x, y) => Math.max(0, 1 - Math.hypot(x - lx, y - ly) / (0.55 * pw));
      const flick = 0.88 + 0.12 * Math.sin(t * 2.3);       // a slow drift: no flashing
      edges[0].setAttribute("opacity", (on * flick * near(lx, top) * 0.9).toFixed(3));
      edges[1].setAttribute("opacity", (on * flick * near(lx, bottom)).toFixed(3));
      edges[2].setAttribute("opacity", (on * flick * near(left, ly) * 0.8).toFixed(3));
      edges[3].setAttribute("opacity", (on * flick * near(right, ly) * 0.8).toFixed(3));
      holes.forEach(h => h.setAttribute("opacity", (on * flick * Math.pow(near(+h.getAttribute("cx"), +h.getAttribute("cy")), 0.6)).toFixed(3)));
      const fw = 0.3 * pw, spread = 1.3 * ppm;
      fan.setAttribute("points", `${lx - fw / 2},${bottom} ${lx + fw / 2},${bottom} ${lx + fw / 2 + spread},${floor + 6} ${lx - fw / 2 - spread},${floor + 6}`);
      fan.setAttribute("opacity", (on * flick * (0.5 + 0.5 * (ly - top) / ph)).toFixed(3));
    });
    await s.after(0.6);
    if (!s.alive) return;
    Z.say("hmm...", 1.1);
    await s.after(0.8);
    if (!s.alive) return;
    thump(1);
    await s.after(0.35);
    if (!s.alive) return;
    thump(0.7);
    await s.after(0.5);
    if (!s.alive) return;
    Z.say("ooh!", 0.9);
    await s.after(0.5);
    if (!s.alive) return;
    thump(1.4);
    await s.after(0.3);
    if (!s.alive) return;

    // ---- out, in a cloud of dust, wearing what he found ----
    on = 0;
    light();
    g.remove();
    this._run(s, panel, "lift", 1);
    puff.at(left + 0.25 * ppm, floor, ppm * 1.4);
    puff.root.position.z = 30;
    puff.play("billow");
    const puffMats = [];
    puff.root.traverse(m => { if (m.isMesh) { m.material = m.material.clone(); m.material.transparent = true; puffMats.push(m.material); } });
    s.tween(1.8, u => puffMats.forEach(m => { m.opacity = 1 - u; }), u => u * u);
    bunny.hold(Z, "head", [0, 0.5, 0.0]);
    bunny.root.scale.setScalar(1.15);
    bunny.play("jiggle", {loop: true});
    Z.clipRight(left + 2);                                 // again: the hat, the torch and now the bunny too
    Z.at(left + 0.55 * ppm, floor).show(true);
    await s.after(0.2);
    if (!s.alive) return;
    await Z.walkTo(left - 0.7 * ppm, {clip: "tiny-inspection/duck", mps: DUCK});
    if (!s.alive) return;
    Z.clipRight(null);
    this._run(s, panel, "lift", -1);
    await Z.face(0);
    await Z.perform("tiny-inspection/emerge");
    if (!s.alive) return;
    Z.play("idle", {loop: true});
    await s.after(0.3);
    if (!s.alive) return;
    const sneeze = Z.perform("tiny-inspection/sneeze");
    await s.after(SNEEZE);
    if (!s.alive) return;
    // the bunny jumps on the sneeze
    s.tween(0.5, u => { bunny.root.position.y = 0.5 + 0.18 * Math.sin(Math.PI * u); }, u => u);
    Z.say("achoo!", 1.0);
    await sneeze;
    if (!s.alive) return;
    await Z.walkTo(innerWidth + 1.0 * ppm, {clip: "run", mps: RUN});
    rattle();
    if (!s.alive) return;
    // the panel, done with, fades from the glass
    const mats = [];
    panel.root.traverse(m => { if (m.isMesh) { m.material = m.material.clone(); m.material.transparent = true; mats.push(m.material); } });
    await s.tween(0.6, u => mats.forEach(m => { m.opacity = 1 - u; }), u => u);
  },
})
