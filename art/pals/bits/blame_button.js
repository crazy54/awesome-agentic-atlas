// The blame button. Up on the home page's spotlight, a traffic cone falls over between the three of them.
// Everyone points at everyone else. A little replay pops up beside them -- three figures in a huddle, a high
// five, a nudge, the cone going over -- and Archie walks over and closes it. The cone and the replay are
// props; the replay's picture is drawn on a canvas. Clips: blame_button.py.
({
  cast: ["archie", "zip", "brick"],
  pages: ["home"],
  ppm: 58,
  ready(s) {
    const r = s.page.rect("article.hero");
    return !!r && r.width > 900 && r.top > 170 && r.top < innerHeight - 220;
  },
  // The replay's picture: three little figures (Archie lime-crested, Zip violet, Brick orange) huddle by a
  // cone, high-five, and Brick knocks it over; `t` seconds in.
  _replay(ctx, w, h, t) {
    ctx.fillStyle = "#18202c"; ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = "rgba(255,255,255,0.035)";
    for (let y = 0; y < h; y += 4) ctx.fillRect(0, y, w, 2);
    const ground = h * 0.8;
    ctx.fillStyle = "#2c3a2a"; ctx.fillRect(0, ground, w, h - ground);
    const k = u => Math.max(0, Math.min(1, u));
    const huddle = k(t / 0.9), five = k((t - 1.0) / 0.4) * (1 - k((t - 1.7) / 0.3)), fall = k((t - 2.0) / 0.35);
    const apart = k((t - 2.5) / 0.4);
    const cx = w * 0.52;
    // the cone, toppling
    ctx.save(); ctx.translate(cx + 14, ground); ctx.rotate(fall * Math.PI / 2);
    ctx.fillStyle = "#ff6a24"; ctx.beginPath(); ctx.moveTo(-14, 0); ctx.lineTo(14, 0); ctx.lineTo(0, -46); ctx.closePath(); ctx.fill();
    ctx.fillStyle = "#f6f4ef"; ctx.fillRect(-9, -22, 18, 6); ctx.restore();
    const fig = (x, col, ht, head, armUp, crest) => {
      ctx.fillStyle = col; ctx.fillRect(x - ht * 0.16, ground - ht * 0.72, ht * 0.32, ht * 0.5);
      ctx.fillRect(x - ht * 0.14, ground - ht * 0.22, ht * 0.08, ht * 0.22);
      ctx.fillRect(x + ht * 0.06, ground - ht * 0.22, ht * 0.08, ht * 0.22);
      ctx.beginPath(); ctx.arc(x, ground - ht * 0.84, ht * head, 0, Math.PI * 2); ctx.fillStyle = crest ? "#ebe5da" : col; ctx.fill();
      if (crest) { ctx.fillStyle = "#a4c812"; ctx.beginPath(); ctx.moveTo(x - 3, ground - ht * 0.96); ctx.lineTo(x + 8, ground - ht * 1.12); ctx.lineTo(x + 4, ground - ht * 0.94); ctx.fill(); }
      ctx.strokeStyle = col; ctx.lineWidth = 4;
      ctx.beginPath(); ctx.moveTo(x, ground - ht * 0.66); ctx.lineTo(x + armUp[0], ground - ht * 0.66 + armUp[1]); ctx.stroke();
    };
    const lean = 18 * huddle * (1 - apart), spread = 40 * apart;
    fig(cx - 70 + lean - spread, "#ebe5da", 70, 0.13, [22 * five + 6, -34 * five - 4], true);
    fig(cx + 64 - lean + spread, "#7440b8", 60, 0.16, [-20 * five - 6, -30 * five - 4], false);
    const bx = cx - 6 - (t > 1.8 && t < 2.2 ? -10 : 0);
    fig(bx - 4 * apart, "#e5671d", 82, 0.11, [fall > 0 && fall < 1 ? 26 : 14 * five, -40 * five], false);
    // the burned-in caption and a slow REC dot (one blink a second)
    ctx.fillStyle = (t % 1) < 0.6 ? "#ff3b30" : "#5a2020";
    ctx.beginPath(); ctx.arc(14, 14, 5, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = "#f4f1ea"; ctx.font = "700 13px system-ui, sans-serif"; ctx.fillText("REPLAY", 24, 19);
    ctx.font = "600 11px ui-monospace, monospace"; ctx.fillText("00:0" + Math.min(9, Math.floor(t + 1)), w - 46, 19);
    if (t > 1.0 && t < 1.8) { ctx.fillStyle = "#fff36e"; ctx.font = "800 15px system-ui"; ctx.fillText("✋", cx - 10, ground - 70); }
  },
  async play(s) {
    const A = s.archie, ppm = A.ppm, T = s.T;
    const H = () => s.page.rect("article.hero");
    const edge = H().top;
    const x0 = H().left + H().width * 0.28;
    // blame_button.py: CONE_X, ZIP_X, BRICK_X, CLOSE_HIT; the replay's close button is (0.4, 0.26) m from its
    // centre before scaling (props_paper.py)
    const CONE = 1.1, ZX = 2.2, BX = -1.9, HIT = 0.8, SC = 2.2;
    const [cone, rp] = await Promise.all([s.prop("traffic-cone-large"), s.prop("replay-screen")]);
    if (!s.alive) return;
    const cx = x0 + CONE * ppm;
    cone.at(cx, edge, ppm);
    A.at(x0, edge).show(true);
    A.play("idle", {loop: true});
    const Z = s.zip, B = s.brick;
    if (Z) { Z.at(x0 + ZX * ppm, edge).show(true); Z.play("idle", {loop: true}); }
    if (B) { B.at(x0 + BX * ppm, edge).show(true); B.play("idle", {loop: true}); }
    await s.after(0.8);
    if (!s.alive) return;

    // Over it goes, toppling about the corner of its base, with a bounce.
    const base = 0.29 * 0.62 * ppm;
    await s.tween(0.55, u => {
      const a = -Math.PI / 2 * u;
      const px = cx + base, py = edge;
      cone.root.rotation.z = a;
      cone.root.position.set(px + (-base) * Math.cos(a), -py + (-base) * Math.sin(a), 0);
    }, u => u * u);
    await s.tween(0.25, u => { cone.root.rotation.z = -Math.PI / 2 + 0.12 * Math.sin(Math.PI * u); });
    if (!s.alive) return;

    // Him! No, him!
    const pointing = [A.perform("blame-button/point")];
    if (Z) { Z.face(-0.6); pointing.push(Z.perform("point")); }
    if (B && B.has("blame-button/point")) pointing.push(B.perform("blame-button/point"));
    await Promise.all(pointing);
    if (!s.alive) return;
    A.play("idle", {loop: true});

    // The replay, beside them at head height, its picture drawn on a canvas.
    const rx = x0 + 4.6 * ppm, ry = edge - 1.55 * ppm;
    rp.at(rx, ry, ppm * SC);
    rp.root.position.z = -60;
    const cv = document.createElement("canvas");
    cv.width = 320; cv.height = 180;
    const ctx = cv.getContext("2d");
    const tex = new T.CanvasTexture(cv);
    tex.flipY = false;
    tex.colorSpace = T.SRGBColorSpace;
    rp.model.traverse(n => {
      if (!n.isMesh) return;
      for (const m of [].concat(n.material)) if (m.name === "screen-face") {
        m.map = tex; m.emissiveMap = tex; m.emissive = new T.Color(0xffffff); m.emissiveIntensity = 0.9; m.needsUpdate = true;
      }
    });
    rp.play("pop_in");
    rp.play("play");
    const t0 = s.clock();
    const draw = s.tick(() => { this._replay(ctx, cv.width, cv.height, s.clock() - t0); tex.needsUpdate = true; });
    await s.after(3.4);
    if (!s.alive) return;

    // Archie closes it: under its close button, a poke.
    const btn = new T.Vector3();
    rp.model.updateMatrixWorld(true);
    const cb = rp.model.getObjectByName("close_button");
    (cb || rp.root).getWorldPosition(btn);
    await A.walkTo(btn.x - 0.55 * ppm);
    if (!s.alive) return;
    await A.face(0);
    if (!s.alive) return;
    const close = A.perform("blame-button/close");
    await s.until(() => A.time() >= HIT || !s.alive);
    if (!s.alive) return;
    rp.play("close");
    await close;
    if (!s.alive) return;
    draw();
    if (Z) { await Z.face(0); Z.play("shrug"); }
    if (B) B.play("shrug");
    await A.perform("blame-button/whistle");
    if (!s.alive) return;
    await s.after(0.3);
  },
})
