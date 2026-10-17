// The missing screw. In front of a card on the page, Archie finds a screw on the floor, looks at it, shrugs
// and pockets it. The card behind him swings down on its one remaining screw (its top-left corner: the
// card itself, turned for a moment through s.page and put back exactly). He freezes and slowly looks at the
// reader. Then the screw back out, a jump, a slap, and the card swings back level; he leaves whistling.
// Clips: missing_screw.py.
({
  cast: ["archie"],
  pages: ["home", "catalog", "discover", "collections", "topic"],
  ppm: 56,
  ready(s) {
    return !!this.card();
  },
  // A card on screen with room round it: tall enough to swing, clear of the window's edges.
  card() {
    return [...document.querySelectorAll("article.cx, article.card")].find(c => {
      const r = c.getBoundingClientRect();
      return r.width >= 200 && r.height >= 260 && r.left > 70 && r.right < innerWidth - 150 &&
        r.top > 70 && r.bottom < innerHeight - 10;
    });
  },
  async play(s) {
    const A = s.archie;
    const card = this.card();
    if (!card) return;
    const r = () => card.getBoundingClientRect();
    const floor = r().bottom - 4, spot = r().left + r().width * 0.3;     // clear of the card's buttons
    const GRAB = 1.2, POCKET = 0.8, SLAP = 1.3;          // missing_screw.py
    // the screw, lying on the floor at his feet (SCREW: 0.12 m to his right)
    const screw = await s.prop("screw");
    screw.at(spot - 0.12 * A.ppm, floor - 2, A.ppm);
    screw.root.rotation.z = Math.PI / 2;
    A.at(r().left - 0.5 * A.ppm, floor).show(true);
    await A.walkTo(spot);
    if (!s.alive) return;
    await A.face(0);
    // picks it up: into his right hand at GRAB
    const spotted = A.perform("missing-screw/spot");
    await s.until(() => A.time() >= GRAB || !s.alive);
    screw.hold(A, "grip_R");
    await spotted;
    if (!s.alive) return;
    await A.perform("missing-screw/inspect");
    if (!s.alive) return;
    A.say("Huh. A spare.", 1.4);
    const pocketed = A.perform("missing-screw/pocket");
    await s.until(() => A.time() >= POCKET || !s.alive);
    screw.root.visible = false;
    await pocketed;
    if (!s.alive) return;
    await s.after(0.35);
    // the card goes: a creaking swing down on its top-left corner
    const back = s.page.nudge(card, {rotate: 3.5, origin: "0% 0%", secs: 1.1, ease: "cubic-bezier(.45,0,.3,1.35)"});
    await A.perform("missing-screw/take");
    if (!s.alive) return;
    // the fix
    const fixing = A.perform("missing-screw/fix");
    await s.after(0.25);
    screw.root.visible = true;
    await s.until(() => A.time() >= SLAP || !s.alive);
    screw.root.visible = false;
    back(0.35);
    await fixing;
    if (!s.alive) return;
    A.say("♪ ♫", 1.8);
    await A.walkTo(innerWidth + 0.6 * A.ppm, {speed: 1.1});
  },
})
