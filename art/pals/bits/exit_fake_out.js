// The exit fake-out. On the index, Archie (taken over where he stands in the masthead, at his size there)
// moonwalks off the right edge of the window. One eye peeks back round the edge. His hand creeps out
// towards the light switch -- the Settings button there -- and freezes: the reader is watching. He takes it
// back, ducks out of sight, and a moment later the lights flicker twice anyway, and come back as they were.
// Clips: exit_fake_out.py.
({
  cast: ["archie"],
  pages: ["home"],
  ready(s) {
    const slot = s.page.slot(), at = slot && this.spot(s.page, slot);
    return !!at && slot.rect.top > -40 && slot.rect.bottom < innerHeight && at.y - 2.3 * at.ppm > 0;
  },
  // Where he stands for the peek, and at what size, so that his index fingertip at the full stretch lands on the
  // switch with the window's edge EDGE to his right; null if the switch is not near enough the edge for it.
  spot(page, slot) {
    const EDGE = 0.56, POINT = [-1.22, 1.22];               // exit_fake_out.py
    const b = [page.rect("#setbtn"), page.rect("#theme")].find(r => r && r.width > 0);
    if (!b || b.top < 0 || b.bottom > innerHeight) return null;
    const W = document.documentElement.clientWidth;
    const tx = b.left + b.width * 0.45, ty = b.top + b.height / 2;
    const ppm = (W - tx) / (-POINT[0] - EDGE);
    // nearer the glass than he was in the masthead: up to nearly twice the size, so the peek reads
    if (ppm < slot.ppm * 1.1 || ppm > slot.ppm * 1.9) return null;
    return {x: W + EDGE * ppm, y: ty + POINT[1] * ppm, ppm};
  },
  async play(s) {
    const A = s.archie;
    const slot = s.page.slot(), peek = this.spot(s.page, slot);
    if (!peek) return;
    const W = document.documentElement.clientWidth;
    A.at(slot.x, slot.y, slot.ppm).show(true);
    A.play("idle", {loop: true});
    await s.after(0.4);
    A.say("Well, I'll be off then.", 1.6);
    await s.after(0.8);
    if (!s.alive) return;
    await A.walkTo(W + 0.7 * A.ppm, {clip: "moonwalk", mps: 0.6 / 0.5, backwards: true});
    if (!s.alive) return;
    A.show(false);
    await s.after(1.6);
    if (!s.alive) return;
    // back, just past the edge, facing in, at the size and height that put his fingertip on the switch
    A.at(peek.x, peek.y, peek.ppm);
    await A.face(0);
    A.show(true);
    await A.perform("exit-fake-out/peek");
    if (!s.alive) return;
    await A.perform("exit-fake-out/reach");
    if (!s.alive) return;
    await A.perform("exit-fake-out/duck");
    A.show(false);
    await s.after(1.1);
    if (!s.alive) return;
    await s.page.flicker(4);                           // dark, light, dark, light: 1.25 flashes a second
    await s.after(0.3);
  },
})
