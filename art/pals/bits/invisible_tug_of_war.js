// The invisible tug-of-war. Up on the home page's spotlight, Archie hauls on a cable that runs off the right
// edge of the window. Zip joins in. Brick takes hold and gives it one gentle tug -- and Archie is yanked off
// his feet from behind: the cable is his own tether, from the port low on his back, along the floor under
// their feet and round. The cable and tether are drawn lines over the page. Clips: invisible_tug_of_war.py.
({
  cast: ["archie", "zip", "brick"],
  pages: ["home"],
  ppm: 58,
  ready(s) {
    const r = s.page.rect("article.hero");
    return !!r && r.width > 800 && r.top > 170 && r.top < innerHeight - 220;
  },
  // Up from behind the element whose top edge is `edge`, to stand at x (clipped at the edge on the way).
  async _rise(s, a, x, edge, clip = "idle") {
    a.clipBelow(edge);
    a.at(x, edge + 3 * a.ppm).show(true);
    a.play(clip, {fade: 0, loop: true});
    await s.tween(0.55, u => a.at(x, edge + 3 * a.ppm * (1 - u)));
    if (!s.alive) return;
    a.clipBelow(null);
  },
  async play(s) {
    const A = s.archie, ppm = A.ppm;
    const H = () => s.page.rect("article.hero");
    const edge = H().top;
    const x0 = H().left + H().width * 0.3;
    // invisible_tug_of_war.py: ZIP_AHEAD, BRICK_AHEAD, TUG_AT
    const ZA = 1.3, BA = 2.8, TUG = 0.6;
    const W = s.W();
    const cable = s.svg.path({stroke: "#2b2a29", width: 4});
    const tether = s.svg.path({stroke: "#2b2a29", width: 4});
    const stripe = s.svg.path({stroke: "#a4c812", width: 1.6});
    stripe.el.setAttribute("stroke-dasharray", "6 10");
    let sag = 0.25, taut = 0, holders = [() => A];
    // the cable: through every holder's hands, out past the window's right edge; the tether: from his port,
    // down to the floor, along it, out the same side
    const draw = s.tick(() => {
      const pts = holders.map(h => h().handsAt());
      const end = {x: W + 20, y: pts[pts.length - 1].y - 10};
      let d = `M${pts[0].x.toFixed(1)} ${pts[0].y.toFixed(1)}`, prev = pts[0];
      for (const p of [...pts.slice(1), end]) {
        d += ` Q${((prev.x + p.x) / 2).toFixed(1)} ${((prev.y + p.y) / 2 + sag * 40).toFixed(1)} ${p.x.toFixed(1)} ${p.y.toFixed(1)}`;
        prev = p;
      }
      cable.el.setAttribute("d", d);
      const port = A.pageAt("tether");
      const floor = edge - 3;
      const mid = port.x + (1 - taut) * 0.6 * ppm;
      const t = `M${port.x.toFixed(1)} ${port.y.toFixed(1)} Q${(port.x - 0.2 * ppm * (1 - taut)).toFixed(1)} ${floor} ` +
                `${mid.toFixed(1)} ${floor} L${W + 20} ${floor}`;
      tether.el.setAttribute("d", t);
      stripe.el.setAttribute("d", t);
      stripe.el.setAttribute("stroke-dashoffset", String((s.clock() * 30) % 16));
    });

    A.at(x0, edge).show(true);
    await A.face(1);
    if (!s.alive) return;
    A.play("invisible-tug-of-war/pull", {loop: true});
    A.say("Nngh!", 1.4);
    await s.after(2.4);
    if (!s.alive) return;

    const Z = s.zip, B = s.brick;
    if (Z) {
      await this._rise(s, Z, x0 + ZA * ppm, edge);
      if (!s.alive) return;
      await Z.face(1);
      if (!s.alive) return;
      Z.play("pull", {loop: true});
      holders.push(() => Z);
      await s.after(1.8);
    }
    if (!s.alive) return;
    if (B) {
      await this._rise(s, B, x0 + BA * ppm, edge);
      if (!s.alive) return;
      await B.face(1);
      if (!s.alive) return;
      holders.push(() => B);
      if (B.has("invisible-tug-of-war/tug")) {
        B.play("invisible-tug-of-war/tug");
        await s.until(() => B.time() >= TUG || !s.alive);
      }
    } else {
      await s.after(1.2);
    }
    if (!s.alive) return;

    // The slack runs out: the tether snaps taut and pulls him over from behind.
    await s.tween(0.12, u => { taut = u; sag = 0.25 * (1 - u); });
    if (!s.alive) return;
    A.play("invisible-tug-of-war/yank");
    holders = holders.filter(h => h() !== A);
    if (!holders.length) holders = [() => A];
    const ax = A.x;
    await s.tween(0.35, u => A.at(ax + 0.5 * ppm * u, edge));
    if (!s.alive) return;
    if (Z) Z.play("idle", {loop: true});
    await s.after(1.4);
    if (!s.alive) return;
    await A.perform("invisible-tug-of-war/up");
    if (!s.alive) return;
    sag = 0.6;
    await A.perform("invisible-tug-of-war/look");
    if (!s.alive) return;
    A.say("...oh.", 1.4);
    await s.after(1.4);
    if (!s.alive) return;
    draw();
  },
})
