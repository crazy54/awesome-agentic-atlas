// Bootleg Archie. Archie stands, dignified. Zip sneaks up beside him and clicks a remote at the Atlas Core in
// Archie's belly: it opens by itself and projects a tiny, big-headed hologram Archie, lecturing the reader in
// pompous bubbles. Real Archie folds his arms. Tiny Archie folds his arms. A wagged finger ("Stop that."),
// copied; Zip cracks up, and the remote goes behind his back as Archie presses the Core shut and goes -- and Zip, alone, clicks once more at where he went. Clips: bootleg_archie.py; Tiny Archie is
// the holo-archie prop, on Archie's skeleton, so it plays Archie's own pieces.
({
  cast: ["archie", "zip"],
  pages: ["home", "topic", "repo", "repos", "catalog", "discover", "collections", "target", "lost"],
  ppm: 140,
  ready(s) {
    return innerWidth >= 1000 && innerHeight >= 620;
  },
  async play(s) {
    const A = s.archie, Z = s.zip, T = s.T, ppm = A.ppm;
    const ZIP_X = 3.4, PRESS = 0.95, REMOTE = 0.7, CLICK = 1.35, AGAIN = 1.0;   // bootleg_archie.py
    const SNEAK = 0.32 / (0.62 * 1.2), RUN = 0.6 / (0.4 * 0.4);                // clips/zip_base.py
    const SIZE = 340, TINY = 0.2;                     // the projection's width (px); Tiny Archie in its units
    const floor = innerHeight - 8, ax = Math.round(innerWidth * 0.25), zx = ax + ZIP_X * ppm;
    const clip = n => A.clips[`bootleg-archie/${n}`];
    const [core, remote, figs] = await Promise.all([s.core(A), s.prop("remote-zip"), s.figures("holo-archie", 1)]);
    if (!s.alive) return;
    s.page.undo(() => remote.remove());
    const tiny = figs[0];

    // ---- Tiny Archie's bubbles: the pals' own, tinted as a hologram's, inside the stage's layer (its tint's
    // rules with it); no stage, no bubble ----
    const stage = document.querySelector(".pals-stage");
    let bub = null;
    if (stage) {
      const css = document.createElement("style");
      css.textContent = ".pals-say.holo{background:#dcfbfe;color:#06535d;box-shadow:0 0 0 2px #2fe3f1,0 4px 14px rgba(0,0,0,.2)}" +
        ".pals-say.holo::after{border-top-color:#dcfbfe}";
      bub = document.createElement("p");
      bub.className = "pals-say holo";
      stage.append(css, bub);
      s.page.undo(() => { bub.remove(); css.remove(); });
    }
    const hush = () => { if (bub) bub.classList.remove("on"); };
    let bubAt = null;                                  // () => {x, y}: where its tail points, or null: hidden
    const v = new T.Vector3();
    const tinyHead = () => {
      const h = tiny.model.getObjectByName("head");
      if (!h) return {x: 0, y: 0};
      h.getWorldPosition(v);
      return {x: v.x, y: -v.y - 1.0 * TINY * SIZE / 2};
    };
    s.tick(() => {
      if (!bubAt || !bub) return;
      const p = bubAt();
      bub.style.left = p.x + "px";
      bub.style.top = (p.y - 6) + "px";
    });
    const holoSay = async (text, secs, at = tinyHead) => {
      if (!bub) return s.after(secs);
      bub.textContent = text;
      bubAt = at;
      bub.classList.add("on");
      await s.after(secs);
      if (bub.textContent === text) bub.classList.remove("on");
    };

    // ---- on: Archie, and Zip creeping up beside him ----
    A.at(-0.45 * ppm, floor).show(true);
    A.play("idle", {loop: true});
    await A.walkTo(ax);
    if (!s.alive) return;
    await A.face(0);
    A.play("idle", {loop: true});
    A.say("Today: a calm, dignified page.", 2.4);
    // Zip, in at a run while he talks, and the last steps on tiptoe
    Z.at(innerWidth + 0.5 * ppm, floor).show(true);
    Z.play("idle", {loop: true});
    await Z.walkTo(zx + 0.5 * ppm, {clip: "run", mps: RUN});
    if (!s.alive) return;
    await Z.walkTo(zx, {clip: "sneak", mps: SNEAK});
    if (!s.alive) return;
    await Z.face(0);

    // ---- the remote; the Core opens by itself ----
    const rm = Z.perform("bootleg-archie/remote");
    await s.after(REMOTE);
    remote.hold(Z, "grip_R", [0, 0, 0], [0, Math.PI, 0]);
    remote.root.scale.setScalar(1.6);
    await s.after(CLICK - REMOTE);
    if (!s.alive) return;
    remote.play("click");
    core.play("unfold");
    const st = A.perform("bootleg-archie/startle");
    await s.after(0.4);
    A.say("!", 0.7);
    await rm;
    if (!s.alive) return;
    Z.play("bootleg-archie/aim", {loop: true});
    core.play("open-idle", {loop: true});
    const proj = await s.project(s.where().world);
    if (!s.alive || !proj) return;
    const follow = s.tick(() => { const p = core.page(); proj.at(p.x, p.y, SIZE, 1); });
    // Tiny Archie, at the front of the world's middle (clear of its own sights), popping up as it finishes
    // rising (appear is 0.8 s)
    const w = proj.world, anchor = w.getObjectByName("anchor_centre") || w;
    anchor.add(tiny.root);
    const ap = w.worldToLocal(anchor.getWorldPosition(new T.Vector3()));
    tiny.root.position.set(0, 0, Math.max(0, 0.3 - ap.z));
    tiny.root.scale.setScalar(1e-4);
    tiny.play("pompous", true);
    await st;
    if (!s.alive) return;
    A.play("bootleg-archie/watch", {loop: true});
    // the world's own holograms switched off for Zip's broadcast (the world is shared: they go back on)
    const off = [], his = new Set();
    tiny.root.traverse(m => his.add(m));
    w.traverse(m => {
      if (his.has(m)) return;
      const mats = m.isMesh ? (Array.isArray(m.material) ? m.material : [m.material]) : [];
      if (m.visible && mats.some(x => x && /^holo/i.test(x.name))) off.push(m);
    });
    const lights = on => off.forEach(m => { m.visible = on; });
    s.page.undo(() => lights(true));
    lights(false);
    s.tween(0.3, u => tiny.root.scale.setScalar(Math.max(1e-4, TINY * u)), u => 1 + 2.7 * Math.pow(u - 1, 3) + 1.7 * Math.pow(u - 1, 2));
    proj.idle();
    await s.after(0.4);

    // ---- the lecture ----
    for (const [line, secs] of [["Ahem. I am ARCHIE.", 1.6], ["Scroll slowly. I am being admired.", 2.1]]) {
      await holoSay(line, secs);
      if (!s.alive) return;
      await s.after(0.15);
    }

    // ---- real Archie folds his arms; Tiny Archie folds his arms ----
    const fold = A.perform("bootleg-archie/fold");
    await s.after(0.7);
    tiny.play(clip("fold"), false);
    await fold;
    if (!s.alive) return;
    A.play("bootleg-archie/folded", {loop: true});
    await s.after(0.4);
    tiny.play(clip("folded"), true);
    await s.after(0.4);
    if (!s.alive) return;

    // ---- "Stop that." -- copied ----
    const wag = A.perform("bootleg-archie/wag");
    await s.after(0.4);
    A.say("Stop that.", 1.3);
    await s.after(0.5);
    tiny.play(clip("wag"), false);
    await s.after(0.3);
    holoSay("Stop that.", 1.3);
    await wag;
    if (!s.alive) return;
    A.play("bootleg-archie/folded", {loop: true});
    await s.after(0.3);
    tiny.play(clip("folded"), true);

    // ---- Zip cracks up -- and, as Archie reaches for the Core, whips the remote out of sight ----
    Z.perform("laugh");
    Z.say("Hee hee hee!", 1.4);
    await s.after(0.6);
    if (!s.alive) return;
    s.after(0.9).then(() => s.alive && Z.perform("bootleg-archie/hide")
      .then(() => s.alive && Z.play("bootleg-archie/innocent", {loop: true})));

    // ---- shut ----
    const shut = A.perform("bootleg-archie/shut");
    await s.after(PRESS);
    if (!s.alive) return;
    const cut = tinyHead();
    holoSay("Ahem, I am--", 0.5, () => cut);                 // cut off as the world goes
    proj.hide(0.3);
    await s.after(0.3);
    bubAt = null;
    hush();
    follow();
    tiny.root.removeFromParent();
    lights(true);
    core.play("fold");
    await shut;
    if (!s.alive) return;
    A.play("idle", {loop: true});
    A.say("Hmph.", 1.0);
    await s.after(0.3);
    if (!s.alive) return;
    const gone = A.walkTo(-0.7 * ppm);
    await s.until(() => A.x < 0.12 * innerWidth);
    if (!s.alive) return;

    // ---- alone (nearly): once more ----
    const ag = Z.perform("bootleg-archie/again");
    await s.after(AGAIN);
    if (!s.alive) return;
    remote.play("click");
    // from off the window's edge, where he went: the Core again, and him (his bubble brought in to the edge)
    holoSay("Ahem! I am ARCH--", 1.0, () => ({x: 110, y: floor - 1.9 * ppm}));
    await s.after(0.8);
    hush();
    await gone;
    A.headAt = () => ({x: 60, y: floor - 2.3 * ppm});
    s.page.undo(() => { delete A.headAt; });
    A.say("ZIP!", 1.2);
    await s.after(0.3);
    if (!s.alive) return;
    await Z.walkTo(innerWidth + 0.7 * ppm, {clip: "run", mps: RUN});
  },
})
