// The handoff. Brick -- the responsible one, who guards the switches and confiscates the remotes -- stands on
// the window's floor with his arms folded. Zip sneaks up beside him and holds out a hand. Brick doesn't look.
// His eyes go left, right; his hand comes out from under his folded arms with the remote in it, and Zip takes
// it. Then Brick's eyes come round to the reader, and stay there. A finger to his lips. Zip sneaks off with
// the remote; Brick folds his arms as if nothing happened -- and as Zip goes, the lights flicker.
// Clips: the_handoff.py (ZIP_AT, SHOW, TAKE are its constants).
({
  cast: ["brick", "zip"],
  pages: ["home", "topic", "repo", "repos", "catalog", "discover", "collections", "target", "lost"],
  ready(s) {
    return document.documentElement.clientWidth >= 900 && innerHeight >= 560;
  },
  async play(s) {
    const {brick: B, zip: Z} = s;
    const ZIP_AT = 1.44, SHOW = 0.55, TAKE = 1.75, TAKE_ZIP = 1.0;
    const SNEAK = 0.32 / (0.62 * 1.2);                          // zip_base SNEAK_SPEED
    const W = s.W(), floor = innerHeight - 8, ppm = Math.min(110, (innerHeight - 140) / 2.9);
    const bx = Math.round(Math.max(W * 0.32, 2.4 * ppm)), zx = bx - ZIP_AT * ppm;
    B.at(bx, floor, ppm).show(true);
    B.play("guard-hold", {loop: true, fade: 0});
    Z.at(-0.8 * ppm, floor, ppm).show(true);
    const remote = await s.prop("remote");
    if (!s.alive) return;
    await s.after(0.6);
    if (!s.alive) return;

    // Zip, on tiptoe, to Brick's side; a hand out
    await Z.walkTo(zx, {clip: "sneak", mps: SNEAK, speed: 1.6});
    if (!s.alive) return;
    await Z.face(0);
    Z.play("the-handoff/ask", {loop: true, fade: 0.2});
    await s.after(1.6);
    if (!s.alive) return;

    // the slip: out from under the folded arms, down at his side, and into Zip's hand
    const slip = B.perform("the-handoff/slip", {fade: 0.25});
    await s.until(() => B.time() >= SHOW || !s.alive);
    remote.hold(B, "grip_R", [0, 0, 0], [Math.PI / 2, 0, 0]);
    await s.until(() => B.time() >= TAKE - TAKE_ZIP || !s.alive);
    const take = Z.perform("the-handoff/take", {fade: 0.15});
    await s.until(() => Z.time() >= TAKE_ZIP || !s.alive);
    remote.hold(Z, "grip_L", [0, 0, 0], [Math.PI / 2, 0, 0]);
    await Promise.all([slip, take]);
    if (!s.alive) return;
    B.play("guard-hold", {loop: true, fade: 0.25});

    // caught: his eyes come round to the reader
    await s.after(0.5);
    if (!s.alive) return;
    await B.perform("the-handoff/caught", {fade: 0.1});
    if (!s.alive) return;
    B.play("guard-hold", {loop: true, fade: 0.3});

    // Zip slips away with it, and, from the edge of the window, uses it
    const off = Z.walkTo(-0.5 * ppm, {clip: "sneak", mps: SNEAK, speed: 1.6});
    await s.until(() => Z.x < 0.6 * ppm || !s.alive);
    if (!s.alive) return;
    remote.play("click");
    await s.page.flicker(2, 380);                                // one dark beat and back: 1.3 flashes a second
    await off;
    if (!s.alive) return;
    await s.after(0.8);
    if (!s.alive) return;
    await B.perform("raise-brow");
  },
})
