// Wrong way up. Along the bottom of the window, Archie leads the way in and Brick follows, carrying a big app
// card (a picture of the spotlight's, drawn here; edge on while he walks). They turn to the reader: the card is
// upside down. Archie presents it, grandly. Brick, without a word, turns it the right way up. Archie carries on
// presenting as if nothing had happened. Clips: wrong_way_up.py.
({
  cast: ["archie", "brick"],
  pages: ["home", "topic", "catalog", "discover", "collections"],
  ppm: 60,
  ready(s) {
    const W = document.documentElement.clientWidth;
    return W > 7.5 * 60 && innerHeight > 3.6 * 60;
  },
  // The card's face: the spotlight's project (or the page's title), as an atlas card.
  face(T) {
    const pick = q => ((document.querySelector(q) || {}).textContent || "").trim();
    const title = (pick("article.hero h2") || pick("h1") || "Atlas").slice(0, 22);
    const own = (pick("article.hero .own") || "awesome-agentic-atlas").slice(0, 32);
    const stars = (pick("article.hero .stz") || "★ 10k").replace(/\s+/g, "").replace(/^(?!★)/, "★ ");
    const c = document.createElement("canvas");
    c.width = 1024; c.height = 683;
    const g = c.getContext("2d");
    const rr = (x, y, w, h, r) => { g.beginPath(); g.roundRect(x, y, w, h, r); };
    g.fillStyle = "#ffffff"; g.fillRect(0, 0, 1024, 683);
    g.fillStyle = "#26262b"; rr(0, 0, 1024, 150, 0); g.fill();
    g.fillStyle = "#a4c812"; rr(52, 40, 170, 70, 35); g.fill();
    g.fillStyle = "#16160f"; g.font = "800 42px system-ui, sans-serif"; g.fillText("SPOTLIGHT", 66, 88);
    g.fillStyle = "#ffd34d"; g.font = "800 58px system-ui, sans-serif";
    g.textAlign = "right"; g.fillText(stars, 970, 96); g.textAlign = "left";
    g.fillStyle = "#121216"; g.font = "800 120px system-ui, sans-serif"; g.fillText(title, 56, 300);
    g.fillStyle = "#6b6b76"; g.font = "500 50px ui-monospace, monospace"; g.fillText(own, 60, 375);
    g.fillStyle = "#d9d9df";
    for (const [y, w] of [[440, 880], [495, 760], [550, 520]]) { rr(60, y, w, 26, 13); g.fill(); }
    g.fillStyle = "#a4c812"; rr(0, 650, 1024, 33, 0); g.fill();
    const tex = new T.CanvasTexture(c);
    tex.colorSpace = T.SRGBColorSpace;
    tex.flipY = false;                               // glTF UVs: v runs down the image
    tex.anisotropy = 4;
    return tex;
  },
  async play(s) {
    const A = s.archie, B = s.brick, T = s.T, ppm = 60;
    const W = document.documentElement.clientWidth, floor = innerHeight - 6;
    // wrong_way_up.py: ARCHIE_X -1.95, CARD_SCALE 1.8, TURN (0.35, 2.05)
    const bx = W - 2.9 * ppm, ax = bx - 1.95 * ppm, start = W + 1.9 * ppm;
    const card = await s.prop("app-card");
    if (!s.alive) return;
    const tex = this.face(T);
    card.model.traverse(n => {
      if (!n.isMesh) return;
      for (const m of Array.isArray(n.material) ? n.material : [n.material]) {
        if (m && /card-face/.test(m.name)) { m.map = tex; m.color.set(0xffffff); m.needsUpdate = true; }
      }
    });
    // the card between Brick's hands every frame: facing as he faces, turned in its own plane by `spin`
    const wrap = new T.Group(), facing = new T.Group(), spinner = new T.Group();
    wrap.add(facing); facing.add(spinner); spinner.add(card.root);
    card.root.scale.setScalar(1);
    wrap.scale.setScalar(ppm * 1.8);
    s.add(wrap);
    let spin = Math.PI;                              // upside down
    const gl = new T.Vector3(), gr = new T.Vector3();
    const sm = (a, b, x) => { const u = Math.min(1, Math.max(0, (x - a) / (b - a))); return u * u * (3 - 2 * u); };
    s.tick(() => {
      B.bone("grip_L").getWorldPosition(gl);
      B.bone("grip_R").getWorldPosition(gr);
      wrap.position.copy(gl).add(gr).multiplyScalar(0.5);
      // its depth is his, 0.62 m in front (wrong_way_up.py CARD), not his hands' (they go behind it to regrip)
      wrap.position.z = (B.turn.position.z + 0.62 * Math.cos(B.turn.rotation.y)) * ppm;
      facing.rotation.y = B.turn.rotation.y;
      spinner.rotation.z = spin;
    });
    A.at(start - 1.95 * ppm, floor, ppm).show(true);
    B.at(start, floor, ppm).show(true);
    B.turn.position.z = -0.4;
    B.play("wrong-way-up/carry", {loop: true});
    A.play("walk", {loop: true});
    await Promise.all([A.walkTo(ax, {speed: B.spec.speed / A.spec.speed}),
                       B.walkTo(bx, {clip: "wrong-way-up/carry"})]);
    if (!s.alive) return;
    A.play("idle", {loop: true});
    B.play("wrong-way-up/hold", {loop: true});
    await Promise.all([A.face(0), B.face(0)]);
    if (!s.alive) return;
    await s.after(0.4);
    const pres = A.perform("wrong-way-up/present");
    await s.after(0.5);
    A.say("Behold!", 1.6);
    await s.until(() => A.time() >= 2.85 || !s.alive);
    if (!s.alive) return;
    A.say("Our finest work.", 2.2);
    const turn = B.perform("wrong-way-up/turn", {fade: 0.1});
    const t0 = s.clock();
    const stop = s.tick(() => {
      const t = s.clock() - t0, k = sm(0, 1, sm(0.35, 2.05, t));
      spin = Math.PI * (1 + k);
      if (t > 2.1) stop();
    });
    await turn;
    if (!s.alive) return;
    spin = 2 * Math.PI;
    B.play("wrong-way-up/hold", {loop: true});
    await s.until(() => A.time() >= 6.1 || !s.alive);
    A.say("Stunning.", 1.6);
    await pres;
    if (!s.alive) return;
    A.play("idle", {loop: true});
    await s.after(1.2);
  },
})
