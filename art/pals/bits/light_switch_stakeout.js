// The light-switch stakeout. Archie, under the theme switch (the Settings button on home and the catalogue,
// the theme chip elsewhere), slaps it on the hop, and the theme flips each time. Brick has been standing a
// little way off with his arms folded, watching. He walks over and lays one enormous finger on the switch.
// Archie jumps back, then tries to get at it round the finger -- under it, in front of it, on the hop -- and
// can't. Brick looks down at him and raises an eyebrow. Archie gives up and slinks off; Brick's finger stays
// where it is, and the brow goes up at the reader. The switch itself is never touched: the finger is a picture
// on the bit's layer, and clicks go through it (and end the bit). Clips: light_switch_stakeout.py.
({
  cast: ["archie", "brick"],
  pages: ["home", "topic", "catalog"],
  ppm: 44,
  // The switch, the floor under it (the spotlight's top edge on home, else the header's bottom) and the
  // size that puts the switch SWITCH_Z (2.9 m) above that floor.
  layout(s) {
    const vis = q => { const r = s.page.rect(q); return r && r.width > 0 && r.height > 0 ? r : null; };
    const sw = vis("#setbtn") || vis("#theme");
    if (!sw) return null;
    const hero = vis("article.hero"), head = vis("header");
    const below = r => r && r.top > sw.bottom + 50 ? r.top : null;
    const floor = below(hero) || (head && head.bottom > sw.bottom + 50 ? head.bottom : null);
    if (!floor) return null;
    const ppm = (floor - (sw.top + sw.height / 2)) / 2.9;
    return ppm >= 32 && ppm <= 60 ? {sw, floor, ppm, cx: sw.left + sw.width / 2} : null;
  },
  ready(s) {
    const L = this.layout(s);
    if (!L) return false;
    const right = L.cx + (0.55 + 0.35 + 0.5) * L.ppm;      // Archie, hopped back, and half his width
    return L.sw.top > 0 && L.floor < innerHeight - 4 && right < document.documentElement.clientWidth &&
      L.cx - 4.2 * L.ppm > 0;
  },
  async play(s) {
    const A = s.archie, B = s.brick;
    const L = this.layout(s);
    if (!L) return;
    // light_switch_stakeout.py: SWITCH_Z, SLAP (x -0.55), SLAP_AT 0.5, STEP 0.35, COVER (x 1.3)
    const {floor, ppm, cx} = L;
    const ax = cx + 0.55 * ppm, bx = cx - 1.3 * ppm, post = bx - 2.2 * ppm;
    const slide = (who, to, secs) => {
      const from = who.x, at = s.clock();
      const off = s.tick(() => {
        const u = Math.min(1, (s.clock() - at) / secs), e = 1 - Math.pow(1 - u, 3);
        who.x = from + (to - from) * e;
        if (u >= 1) off();
      });
      return s.after(secs);
    };
    const slap = async () => {
      const done = A.perform("light-switch-stakeout/slap", {fade: 0.1});
      await s.after(0.5);
      if (s.alive) s.page.flicker(1, 520);
      await done;
    };
    A.at(ax, floor, ppm).show(true);
    B.at(post, floor, ppm).show(true);
    B.turn.position.z = -1;                          // Archie a little nearer the reader
    A.play("idle", {loop: true});
    B.play("guard-hold", {loop: true});
    await s.after(0.5);
    for (let i = 0; i < 2 && s.alive; i++) { await slap(); A.play("idle", {loop: true}); await s.after(0.25); }
    if (!s.alive) return;
    // the stakeout is over: he unfolds his arms and walks over, while Archie keeps at it
    await B.perform("guard-off");
    if (!s.alive) return;
    let there = false;
    const walk = B.walkTo(bx).then(() => { there = true; });
    while (!there && s.alive) { await slap(); A.play("idle", {loop: true}); await s.after(0.2); }
    await walk;
    if (!s.alive) return;
    await B.face(0);
    const cover = B.perform("light-switch-stakeout/cover");
    await s.after(1.2);
    if (!s.alive) return;
    A.play("light-switch-stakeout/startle", {fade: 0.08});
    await slide(A, ax + 0.35 * ppm, 0.6);
    await cover;
    if (!s.alive) return;
    B.play("light-switch-stakeout/cover-hold", {loop: true});
    A.play("idle", {loop: true});
    await s.after(0.4);
    A.say("Hey!", 1.2);
    await A.perform("light-switch-stakeout/reach-round");
    if (!s.alive) return;
    A.play("idle", {loop: true});
    await B.perform("light-switch-stakeout/brow");
    if (!s.alive) return;
    B.play("light-switch-stakeout/cover-hold", {loop: true});
    await A.perform("light-switch-stakeout/give-up");
    if (!s.alive) return;
    await A.walkTo(document.documentElement.clientWidth + 0.8 * ppm, {speed: 0.8});
    if (!s.alive) return;
    // and the finger stays where it is
    await B.perform("light-switch-stakeout/brow-reader");
    if (!s.alive) return;
    B.play("light-switch-stakeout/cover-hold", {loop: true});
    await s.after(0.6);
  },
})
