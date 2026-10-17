# Writing a bit

A bit is a gag the pals play over the page: "the glass door", "the heavy README". It is made of two halves
that share a name:

| half | where | what it does |
|---|---|---|
| the clips | `art/pals/bits/<bit_name>.py` | each pal's pieces of the bit, as `kit.anim.Clip`s named `<bit>/<piece>` |
| the staging | `art/pals/bits/<bit_name>.js` | where on the page it happens, and the order the pieces play in |

`art/pals/bits_js.py` joins every staging file into `docs/assets/archie-bits.js` (generated: never edit it),
checking each with Node first and leaving out, with a warning, any that does not parse.

`art/pals/build_bits.py` bakes the clips into `docs/assets/pals/bits/<bit>@<pal>.glb` (each pal's skeleton,
a stand-in face, and that bit's clips only); the page fetches those when the bit is about to play and plays
them on the models it already has, by bone name. `docs/assets/archie-stage.js` is the stage the staging
runs on. `glass_door.py` and `glass_door.js` are the worked example: read both before writing one.

## The clips

```python
NAME = "glass-door"
CAST = ("archie",)
def clips(bodies):            # {pal: Body}; bodies[pal].lib is that pal's base clip module
    body = bodies["archie"]; L = body.lib
    ...
    return {"archie": [clip, clip, ...]}
```

* A piece is a short clip, in place: the pal's root does not travel. The page moves him between places
  (`walkTo`), turns him (`face`), and plays a piece where he stands. A piece starts and ends on the pal's
  `REST` pose unless it says otherwise, so pieces and the everyday clips chain without a jump.
* Pieces two pals play together are written in one space: a module that lists both pals in `CAST` writes
  each pal's clips with that pal's root where the page will stand him (say so in the module docstring as
  `FORMATION`, in metres from the bit's origin), so a hand-off lines up.
* Write with the base clip module's tools (`L.REST`, `L.hips`, `L.fist`, `L.point`, `L.open_hand`,
  `L.hand_world`, `L.wrist_of`) and `clips/common.py`'s `Body` (`plant`, `hand_to`, `move_world`, `where`).
  Order matters in a solver: **the body first** (hips, spine), **then the arms** (`hand_to`), **then the
  feet** (`plant`), or a hand placed before the hips move goes down with them.
* Props in a pal's hand ride a bone (`grip_L`/`grip_R`): the page attaches them. Write the hand's pose for
  holding it, and put the timings the page needs (when the prop appears, when a line should be traced) in
  the module's docstring and constants.
* **Python closures bind late.** A solver that reads a variable (`T`, a duration) reads its value when the
  clip is evaluated, not when the solver was written: give each piece's constants their own names (`TD`,
  `TT`), or bind them as default arguments.

Preview pieces as stills (Eevee, quick):

```
tools/sheet_clips.sh archie side glass-door/bonk:0,0.1,0.3,0.6,1.0,1.5      # from E:/Development Workspaces/Archie and Pals/
```

## The staging

A staging file is one object expression in parentheses; the bit's name is the file's, with dashes:

```js
// The glass door: ...
({
  cast: ["archie"],                  // its clip files are pals/bits/<bit>@<pal>.glb for each of them
  pages: ["repo"],                   // archie-stage.js where(): home, repo, topic, catalog, discover, collections, ...
  ppm: 56,                           // CSS px per metre for this bit (62.5 is a visit's size)
  ready(s) { ... },                  // its element on screen, with room: true or false, cheaply
  async play(s) { ... },
})
```

`s` is the stage: `s.archie` / `s.zip` / `s.brick` (each `.at(x, y)`, `.show(on)`, `.walkTo(x, {speed})`,
`.face(-1|0|1)`, `.play(clip, {loop})`, `.perform(clip)` (resolves at its end), `.say(text, secs)`,
`.pageAt(bone)`, `.time()`, `.clipRight(x)`), `s.after(secs)`, `s.until(pred)`, `s.tick(fn)` (returns its
remover), `s.page.rect(sel)`, `s.page.flicker(n)`, `s.page.undo(fn)`, `s.svg.path()`, `s.svg.door(box)`,
`s.prop(name)` (a prop GLB from `pals/props/`: `.at(x, y)`, `.hold(pal, bone)`, `.play(clip)`), and
`s.alive`. Positions are CSS pixels in the window, x across and y down; a pal's `y` is his floor.

* After every `await`, `if (!s.alive) return;`. A click, Escape, Tab or a hidden tab ends the bit; the stage
  then puts the page back (anything registered with `s.page.undo`) and takes the cast away.
* Never move, restyle or cover the page's own elements except through `s.page`, and never for long. Never
  touch the reader's cursor, text, numbers or buttons: a card, a star or a cursor in a bit is a picture of
  one (a prop, or an SVG). Nothing flashes more than three times a second.
* Speech is short: a bubble of a few words, or none. The bit should read with the sound off and the
  bubbles unread.

## Checking it

Bake (always `--only` your bit: others are building theirs), re-stamp, record:

```
blender -b --factory-startup --python art/pals/build_bits.py -- --only <bit>     # also runs bits_js.py
python scripts/31_home.py && python scripts/24_pwa.py
# with tests/lib/serve.mjs serving docs/ on 54006, from E:/Development Workspaces/Archie and Pals/:
node tools/capture-bit.mjs --bit <bit> --page <path/> --scroll "<selector>" --size 1400x900
blender -b --factory-startup --python tools/vse.py -- renders/bits/<bit> renders/bits/<bit>.mp4
```

`capture-bit.mjs` drives Chrome over CDP with the stage in capture mode (its clock steps 1/15 s per
screenshot), so the recording is frame-exact however slowly it is taken. Look at a contact sheet of the
frames, fix, and record again.
