// The loading-bar tow truck. While the README viewer is fetching a file, Archie pops up onto its edge,
// hooks a rope onto a loading bar (a picture of one, on wheels) and hauls. Nothing. Zip pushes from behind.
// Brick wanders over, looks at the bar, and lets off its hand brake: it shoots forward, filling up as it
// rolls, and bowls Archie over. The bar is a prop over the page: it never reports on the real wait.
// Clips: loading_bar_tow_truck.py.
({
  cast: ["archie", "zip", "brick"],
  pages: ["repo"],
  ppm: 56,
  ready(s) {
    const e = document.querySelector(".source-preview .reader");
    if (!e || e.dataset.state !== "loading") return false;
    const r = e.getBoundingClientRect();
    return r.width > 600 && r.top > 170 && r.top < innerHeight - 200;
  },
  async _rise2(s, a, x, edge) {
    a.clipBelow(edge);
    a.at(x, edge + 3 * a.ppm).show(true);
    a.play("idle", {fade: 0, loop: true});
    await s.tween(0.55, u => a.at(x, edge + 3 * a.ppm * (1 - u)));
    if (!s.alive) return;
    a.clipBelow(null);
  },
  async play(s) {
    const A = s.archie, ppm = A.ppm, T = s.T;
    const R = () => s.page.rect(".source-preview .reader");
    const edge = R().top;
    const bx0 = R().left + R().width * 0.3;
    // loading_bar_tow_truck.py: ARCHIE_X, ZIP_X, BRAKE_AT; the bar's tow ring is 0.75 m ahead of its origin
    // and 0.27 m up, drawn BS times over (props_set.py)
    const AX = 2.1, ZX = -1.3, BRAKE = 0.7, BS = 1.25;
    const bar = await s.prop("loading-bar");
    if (!s.alive) return;
    bar.at(bx0, edge, ppm * BS);
    bar.root.position.z = 10;
    const fill = bar.play("fill");
    if (fill) fill.paused = true;                         // empty until the brake comes off
    let bx = bx0;
    const ring = () => ({x: bx + 0.75 * BS * ppm, y: edge - 0.27 * BS * ppm});

    const ax = bx0 + AX * ppm;
    A.clipBelow(edge);
    A.at(ax, edge + 2.6 * ppm).show(true);
    A.play("idle", {loop: true});
    await s.tween(0.5, u => A.at(ax, edge + 2.6 * ppm * (1 - u)));
    if (!s.alive) return;
    A.clipBelow(null);
    await A.walkTo(ring().x + 0.5 * ppm);
    if (!s.alive) return;
    await A.face(-1);
    if (!s.alive) return;
    await A.perform("loading-bar-tow-truck/hook");
    if (!s.alive) return;
    // The rope: from the ring to his hands.
    const rope = s.svg.path({stroke: "#b8925a", width: 4});
    let slack = 0.4;
    const drawRope = s.tick(() => {
      const r = ring(), h = A.handsAt();
      rope.el.setAttribute("d", `M${r.x.toFixed(1)} ${r.y.toFixed(1)} Q${((r.x + h.x) / 2).toFixed(1)} ` +
                                `${((r.y + h.y) / 2 + slack * 30).toFixed(1)} ${h.x.toFixed(1)} ${h.y.toFixed(1)}`);
    });
    await A.walkTo(ax, {speed: 0.6});
    if (!s.alive) return;
    await A.face(-1);
    if (!s.alive) return;
    slack = 0;
    A.play("loading-bar-tow-truck/pull", {loop: true});
    A.say("Hnngh!", 1.4);
    await s.after(2.2);
    if (!s.alive) return;

    const Z = s.zip, B = s.brick;
    if (Z) {
      await this._rise2(s, Z, bx0 + ZX * ppm, edge);
      if (!s.alive) return;
      await Z.face(1);
      if (!s.alive) return;
      Z.play("push", {loop: true});
      await s.after(1.8);
    }
    if (!s.alive) return;
    if (B) {
      // beyond the bar, facing back along it: his left hand reaches the lever on its back end
      await this._rise2(s, B, bx0 + 0.25 * ppm, edge);
      if (!s.alive) return;
      await B.face(-1);
      if (!s.alive) return;
      if (B.has("loading-bar-tow-truck/release")) {
        B.play("loading-bar-tow-truck/release");
        await s.until(() => B.time() >= BRAKE || !s.alive);
      }
    } else {
      await s.after(0.8);
    }
    if (!s.alive) return;

    // Off comes the brake: it shoots forward, filling as it rolls, and he goes over.
    bar.play("brake_release");
    bar.play("roll", {loop: true});
    if (fill) fill.paused = false;
    const run = s.tween(0.9, u => { bx = bx0 + 1.1 * ppm * u; bar.root.position.x = bx; });
    await s.after(0.25);
    if (!s.alive) return;
    A.play("loading-bar-tow-truck/fall");
    const ax2 = A.x;
    s.tween(0.4, u => A.at(ax2 + 0.35 * ppm * u, edge));
    if (Z) Z.play("idle", {loop: true});
    await run;
    if (!s.alive) return;
    bar.mixer.stopAllAction();
    const done = bar.play("fill");
    if (done) done.time = done.getClip().duration;
    slack = 0.6;
    await s.after(1.6);
    if (!s.alive) return;
    await A.perform("loading-bar-tow-truck/up");
    if (!s.alive) return;
    await s.after(0.6);
    if (!s.alive) return;
    drawRope();
  },
})
