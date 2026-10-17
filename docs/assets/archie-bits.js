// The pals' bits: the gags Archie, Zip and Brick play over the page, on the stage in archie-stage.js. Each
// bit says who is in it (`cast`), which clip files it needs (`packs`: art/pals/bits/<bit>.py, baked by
// art/pals/build_bits.py into assets/pals/bits/<bit>@<pal>.glb), where it can happen (`pages`: the page
// families of archie-stage.js's `where()`), whether it can happen now (`ready()`: its element on screen and
// room around it), and how it goes (`play(s)`).
//
// `play` gets the stage `s`: the cast (`s.archie`, `s.zip`, `s.brick`, each with at/walkTo/face/perform/
// play/say/pageAt/clip), `s.after(secs)` and `s.until(pred)` on the render clock, `s.page` (rects, and the
// page borrowed and given back), `s.svg` (a drawing layer over the cast), `s.prop(name)`, and `s.alive`,
// which goes false the moment the reader clicks, presses Escape or Tab, or the tab goes to the background:
// a bit checks it after each await and leaves, and the stage puts everything back however it left.
//
// The rules every bit keeps: nothing it draws takes a pointer event or is announced (a line it says goes to
// the polite live region instead); nothing of the page's is moved, covered for long or restyled except
// through `s.page`, which restores it; nothing flashes faster than three times a second; and the reader's
// own cursor, text and numbers are never touched -- a cursor, a card or a star in a bit is a picture of one.
const bit = (o) => o;

export const BITS = {
  // ---- The glass door --------------------------------------------------------------------------------
  // Archie walks along the bottom of the window (or of the viewer, if it ends first) into the viewer's left
  // edge. Bonk. He feels for the invisible wall, turns to the reader, draws a door on the viewer's glass
  // beside him, opens it and walks in. The door shuts behind him and the drawing fades.
  // art/pals/bits/glass_door.py has his clips.
  "glass-door": bit({
    cast: ["archie"],
    packs: {archie: "pals/bits/glass-door@archie.glb"},
    pages: ["repo"],
    ppm: 56,
    ready(s) {
      const r = s.page.rect(".source-preview .reader");
      if (!r || r.left < 180) return false;
      const floor = Math.min(innerHeight - 6, r.bottom - 2);
      return r.top > 0 && floor - r.top > 220;          // a wall taller than he is, on screen
    },
    async play(s) {
      const A = s.archie;
      const reader = () => s.page.rect(".source-preview .reader");
      const floor = Math.min(innerHeight - 6, reader().bottom - 2);
      const WALL = 0.36;                              // glass_door.py: his root to the wall at the bonk
      A.at(-0.6 * A.ppm, floor).show(true);
      A.play("idle", {loop: true});
      await A.walkTo(reader().left - WALL * A.ppm, {speed: 1.15});
      if (!s.alive) return;
      A.say("Ow.", 1.4);
      await A.perform("glass-door/bonk", {fade: 0.08});
      if (!s.alive) return;
      await A.perform("glass-door/feel");
      if (!s.alive) return;
      A.say("...glass?", 1.6);
      await A.face(0);
      // The marker's line, traced from his left hand as he draws: the drawn door is where his hand went.
      const pen = s.svg.path({stroke: "#1b1b1f", width: 4});
      let tracing = true;
      const trace = s.tick(() => {
        if (!tracing) return;
        const t = A.time();
        if (t > 0.84 && t < 3.12) pen.add(A.pageAt("grip_L"));       // glass_door.py: t0 .. the knob
      });
      await A.perform("glass-door/draw");
      tracing = false;
      trace();
      if (!s.alive) return;
      // The door: the traced outline's box, a dark doorway behind a panel hinged on its far edge.
      const b = pen.box();
      const door = s.svg.door(b, {fill: "#f2efe8", stroke: "#1b1b1f"});
      await A.face(1);
      const pull = A.perform("glass-door/through");
      await s.after(0.55);
      door.open(0.7);
      await pull;
      if (!s.alive) return;
      // In: hidden from the door's near edge on, as he walks into the dark.
      A.clipRight(b.left + 2);
      await A.walkTo(b.right + 0.4 * A.ppm, {speed: 0.9});
      door.close(0.4);
      await s.after(0.6);
      pen.fade(0.8);
      door.fade(0.8);
      await s.after(0.9);
    },
  }),
};
