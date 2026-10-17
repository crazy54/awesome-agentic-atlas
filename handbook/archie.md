# Archie, the mascot

Archie is the 3D robot in the homepage masthead. He idles, reacts, dances, plays pranks, has friends to
visit, and can put on a light show. He carries the Atlas Core, a ball in his belly that opens on a little
world of the page the reader is on. Now and then he and his pals, Zip and Brick, play a *bit* -- a short gag
over the page itself. He appears only on the homepage (`/`, built by `31_home.py`).

## Files

Every runtime file is under `docs/assets/`, written by hand, and served as-is. Sizes are as measured on 2026-09-25.

| File | Size | What it is |
|---|---|---|
| `archie.js` | 163 KB | The loader and the whole director: when to go live, which act next, speech, pranks, visits, bits, the `window.archie` command API, and the rig's lighting (`lights()`, which exposes `window.archieRig`) |
| `three-archie.js` | 652 KB | The subset of three.js Archie uses, bundled once (see [below](#the-threejs-bundle)). Do not edit it by hand |
| `archie.glb` | 806 KB | The model, rigged, with his everyday clips (meshopt-compressed) |
| `archie-dances.glb` | 478 KB | His dances: clips only, on the same skeleton, fetched once he is live and the page is idle |
| `archie-3d.webp` | | The poster: a still of the idle's first frame. Shown before the model loads, and instead of it when the model cannot run |
| `archie-core.js` | 6 KB | The Atlas Core: the ball on his `core` bone or in his hand, opening on the page's world |
| `archie-stage.js` | 41 KB | The pals' stage: a full-window canvas over the page where bits play, the cast, props, the Core's projection, and `where()`, which page and world the reader is on |
| `archie-bits.js` | 220 KB | Every bit's staging, generated from `art/pals/bits/*.js` by `art/pals/bits_js.py`. Do not edit it by hand |
| `pals/` | | `zip.glb`, `brick.glb`, `core.glb`; `worlds/` (a world per page family and topic, and `holo-bot.glb`); `props/` (the bits' props); `bits/` (each bit's clips, `<bit>@<pal>.glb`) |
| `archie-fx.js` | 15 KB | Stage effects: LED dance floor, fog, haze, CO2 jets, flames and sparks |
| `rig-show.js` | 8 KB | The rig's look book: `LOOKS` (colours), `GOBOS`, `LASERS` (laser graphics) and `PATTERNS` |
| `rig/rig.glb`, `rig/wall-{a,b,c,d}.{webm,mp4,webp}`, `rig-gobos/*.svg` | | Fixture models, LED-wall video loops and their posters, gobo masks |
| `archie-friends.js`, `archie-friends-data.js` | 41 KB, 17 KB | The friends' art and choreography; their roster and lines. `ORDER` is `nib`, `posy`, `lumen`, `oh-four`, `quack` |
| `archie-dance.js`, `archie-beat.js` | 13 KB, 3 KB | "Dance with me": the audio source picker and the AudioWorklet beat detector |
| `archie-admin.js` | 8 KB | The hidden admin panel |

The sources that generate the binaries are in `art/`:

| Source | Builds | Command |
|---|---|---|
| `art/pals/build.py` (`archie.py`, `zip.py`, `brick.py`; clips in `art/pals/clips/`) | `docs/assets/archie.glb`, `archie-dances.glb`, `archie-3d.webp`; `docs/assets/pals/zip.glb`, `brick.glb` | `blender -b --factory-startup --python art/pals/build.py -- archie` (or `zip`, `brick`) |
| `art/pals/core.py` | `docs/assets/pals/core.glb` | `blender -b --factory-startup --python art/pals/core.py` |
| `art/pals/worlds.py` | `docs/assets/pals/worlds/*.glb` | `blender -b --factory-startup --python art/pals/worlds.py` |
| `art/pals/props.py` | `docs/assets/pals/props/*.glb` | `blender -b --factory-startup --python art/pals/props.py [-- --only name,name]` |
| `art/pals/build_bits.py` (`art/pals/bits/*.py`, `*.js`) | `docs/assets/pals/bits/*.glb`, `docs/assets/archie-bits.js` | `blender -b --factory-startup --python art/pals/build_bits.py [-- --only bit,bit]` |
| `art/rig/rig.py` | `docs/assets/rig/rig.glb`, `art/rig/rig.blend` | `blender --background --factory-startup --python art/rig/rig.py` |
| `art/rig/wall.py` | `docs/assets/rig/wall-*.{webm,mp4,webp}` | `python art/rig/wall.py [a b c d]`, or `--check` to measure and encode nothing. Needs numpy and Pillow, and runs Blender for its FFmpeg (set `BLENDER` if it is not at the default Windows path) |
| `art/archie/three-entry.js` | `docs/assets/three-archie.js` | see below |

Each script's docstring is the full reference. `art/pals/README.md` explains the pals' kit and
conventions, `art/pals/reference.md` the model sheets' landmarks, and `art/pals/BITS.md` how to write a bit.
The pals' GLBs are compressed with meshopt by a gltf-transform step that `kit/export.py` runs (Node, with
`@gltf-transform/cli` and `meshoptimizer`, outside the repository); the bundle carries the decoder.

## When he is live

`archie.js` switches from the poster to the live model only when all three of these hold:

- the viewport is at least **900 px** wide;
- the reader has **not** asked for reduced motion;
- the browser has **WebGL2**.

Otherwise he stays a poster, and the admin panel's buttons say why. `31_home.py` wires him into the page
only when `archie.js`, `archie-fx.js`, `three-archie.js`, `archie.glb` and `archie-3d.webp` all exist. Friends,
dance and the rig are optional: without them he still loads.

## Animation

His clips are written in Python (`art/pals/clips/archie_base.py`: key poses, layers and solvers, baked
per frame) and split across two files:

- **`archie.glb`, everyday acts:** `idle`, `watch`, `sit`, `sleep`, `press`, `shrug`, `walk`, `moonwalk`,
  `core-show`.
- **`archie-dances.glb`, fifteen dances**, each listed in `BEATS` in `archie.js` with its length in beats:
  `floss`, `take-the-l`, `default-dance`, `orange-justice`, `robot`, `electro-shuffle`, `hype`, `boogie-down`,
  `get-griddy`, `billy-bounce`, `fresh`, `scenario`, `groove-jam`, `headbang`, `the-drop`. A dance asked for
  before the file lands waits for it.

The lights keep time to those beat counts. **If you change a dance's rhythm in `archie_base.py`, change its
`BEATS` entry too.** The walk's ground speed (`WALK_SPEED` in `archie.js`, and the stage's `CAST`) is
likewise derived from the clip's stride, so the feet skate if the two drift apart.

## The pals, the Atlas Core and bits

- **Zip and Brick** (`pals/zip.glb`, `pals/brick.glb`) are built like Archie, with the same bone names, and
  appear only in bits. They are fetched the first time a bit needs them.
- **The Atlas Core** sits on Archie's `core` bone. The `core` act takes it out and opens it on the world of
  the page the reader is on (`archie-stage.js` `where()`: a topic's world on that topic's page or a project
  in it, `discover`, `collections`, `lost` on the 404, `home` otherwise), drawn large on the stage beside
  him with a beam down to the ball. Holograms are added as light on a dark page and laid over a light one
  (`tone()`), so they read on both themes.
- **Bits** are the gags in `Bit What happens.md`, made real. Each is a staging file and its clips in
  `art/pals/bits/`. The director plays one on its own at most every three minutes, the first no sooner than
  45 seconds in, each at most once a page view, and only where it can play: its page family, and its element
  on screen with room (`ready()`). Never in Quiet mode, to music, during a prank or a friend's visit, or with
  an `?archie=` flag on the page. A bit with a `cue` waits for something the reader does instead (scrolling a
  row of cards, say), a minute after the last. While a bit plays the banner's Archie hides, and the stage's
  takes his place.
- **The stage's rules**, which every bit keeps: its layer is `aria-hidden` and takes no pointer events; the
  page's own elements are changed only through `s.page`, which puts them back exactly; nothing flashes more
  than three times a second; a click, Escape, Tab or a hidden tab ends a bit at once; nothing is saved; and
  it never takes focus. Whatever a bit hangs on a pal comes off when it ends.

## Dance with me

The `#dancebtn` chip ("Dance with me") appears only where the live model runs. It asks where the music is
playing:

- **Music on this computer:** `getDisplayMedia` with audio. This works in Chromium browsers only.
- **The microphone:** `getUserMedia`.

The choice is remembered in `localStorage["archie-dance"]`. `archie-beat.js`, an AudioWorklet, detects beats. The page
then receives two `document` events:

- `archie:music` `{on, source}` when music mode starts or stops;
- `archie:beat` `{strength, bpm, at}` on each beat.

Archie dances to the beat, and the rig follows along. `dance-check.mjs` feeds the detector a known tempo.

## The stage rig and effects

- **Lighting and cues** are in `archie.js`, in `lights()`. It exposes `window.archieRig` =
  `{cues, cue(name), status(), solo(...parts)}` while the live model's rig is up. The rig's cues
  (`RIG_CUES`) are `beams-chase`, `beams-fan`, `beams-cross`, `ballyhoo`, `gobo`, `laser-symbol`,
  `blinder`, `wash`, `pods`, `video-wall` and `all-off`. `cue()` sends `co2`, `flames`, `sparks` and
  `haze` to `archie-fx.js` instead, and `all-off` to both. `haze` fans the beams first if the rig is
  idle, because haze is only visible where a beam crosses it. `solo()` renders only the named rig or
  effect parts (`solo()` with no arguments renders everything again). `stage-check.mjs` uses it to
  measure one effect at a time. You can fire a cue in three ways:
  - `window.archieRig.cue("gobo")`;
  - dispatching an `archie:cue` event;
  - the admin panel.
- **The look book** (colours, gobos, laser graphics, patterns) is `rig-show.js`.
- **Floor, fog, haze and pyro** are `archie-fx.js`, which `archie.js` imports under its own `?v=`.
- **Fixture models and LED-wall clips** are built from `art/rig/`.
- **Photosensitivity.** The rig, effects and wall clips are all written to stay under WCAG 2.3.1:
  no more than three flashes a second, and no large bright areas. `rig-check.mjs` measures the flash rate of
  every fixture and `wall.py --check` measures the clips. Keep both green.

To test the rig:

```bash
node tests/run.mjs          # includes rig-check, stage-check, admin-check, prank-check, friends-check and dance-check
```

Or run `rig-check.mjs` alone; see [testing.md](testing.md#running-one-harness). To look at it yourself,
open the homepage on a wide screen, open the admin panel, and press the cue buttons.

## The admin panel

The panel is a hidden control surface for every command. It is **not a security boundary**: the site is
static, and anyone can call `window.archie.run()` from the console.

- **Open it** with the faint "·" button at the end of the footer (`#archieadmin`), or by adding
  `?archie=admin` to the URL. `archie-admin.js` loads only then.
- **Close it** with Escape, which returns focus to the trigger.
- **What it drives:** `window.archie`, which provides:
  - `list()`: every command;
  - `can(cmd)`: `""`, or a reason the command cannot run now;
  - `run(cmd)`;
  - `status()`: `{act, queued}`.
- **Commands:**
  - `dance:<name>`
  - `idle`, `watch`, `sit`, `sleep`, `press`, `shrug`, `walk-off`
  - `show` (a dance under the full rig)
  - `prank:<name>`
  - `core` (the Atlas Core), `bit:<name>` (any bit, through the same gates as one he picks)
  - `chatter`, `poke`
  - `cue:<rig cue>`
  - `friend:<id>`
  - `quiet`, which empties the queue, sends a visitor home and cues the rig off.

It is tested by `tests/admin-check.mjs`, which runs in the suite.

## `?archie=` URL flags

Add one to the homepage URL to skip the wait and see one behaviour at once:

| Flag | Effect |
|---|---|
| `?archie=<dance>` (e.g. `?archie=robot`) | starts on that dance |
| `?archie=watch`, `sit`, `sleep`, `walk-off` | starts on that act |
| `?archie=prank:lights` (or `skin`, `tilt`, `count`, `cursor`) | plays that prank first, through the usual gates, so quiet mode still stops it |
| `?archie=friend:<id>` (e.g. `friend:posy`) | that friend visits. Normally 25% of page views get a visit |
| `?archie=core` | starts on the Atlas Core |
| `?archie=bit:<name>` (e.g. `bit:glass-door`) | plays that bit as soon as it can: on its page, with its element in view |
| `?archie=visit` | Archie goes visiting after about 1.5 s instead of 20 to 45 s |
| `?archie=admin` | opens the admin panel |

## Storage

Archie keeps these keys; clear them to reset his behaviour:

| Key | Where | Meaning |
|---|---|---|
| `atlas-byte-quiet` | localStorage | `"1"` is the catalogue's Quiet mode: no chatter, pranks, friends or visits |
| `archie-dance` | localStorage | the last music source chosen |
| `archie-hi` | sessionStorage | he has already said hello this session |
| `theme`, `atlas-skin` | localStorage | the site's theme and skin, which pranks borrow and always restore |

`prank-check.mjs` checks that no prank leaves anything behind in storage, and `bits-check.mjs` that no bit
does.

## After editing Archie

Nothing under `docs/assets/` is cached by the service worker. Instead, **the page loads Archie's scripts
with a `?v=<hash>` query string**, and `archie.js` passes its own `?v=` on to the effects, the three.js
bundle, the model, the friends and the rig files. That hash is computed by `mascot_version()` in
`31_home.py`, over:

- the files in `VERSIONED`;
- the friend files and the `RIG` files, when present;
- every file under `assets/pals/`: the pals, the Core, the worlds, the props and the bits' clips.

For `.js` and `.svg` files it is hashed with LF line endings.

So after editing any Archie asset:

```bash
python scripts/31_home.py     # re-stamps ?v= in docs/index.html
python scripts/24_pwa.py      # index.html changed, so the service worker's VERSION must too
```

Commit `docs/index.html`, `docs/sw.js` and the asset together. **If you skip `31_home.py`, readers keep the
old file from their HTTP cache.** A new `archie.js` can then meet a stale sibling, and Archie stays a poster.

The hash covers every file the loader fetches under that query: all four wall clips in each format,
the gobos, the friends and `archie-admin.js`. A file added to that set has to be added to `RIG` or
`OPTIONAL` in `31_home.py`, or editing it will not bust the cache.

`archie-dance.js` has its own version, which also covers `archie-beat.js`.

## The three.js bundle

`three-archie.js` is only the three.js exports that `art/archie/three-entry.js` names, so it is about a third
the size of three's core. It is vendored rather than loaded from a CDN, so readers depend on no
third-party host. To rebuild it, outside the repository or in a scratch directory, since this repo has no
`package.json`:

```bash
npm i three@0.186.0 esbuild
npx esbuild art/archie/three-entry.js --bundle --minify --format=esm --legal-comments=eof \
  --outfile=docs/assets/three-archie.js
```

If `archie.js` starts using another three.js export, add it to `three-entry.js` and rebuild. Keep the
version pinned. Then run `31_home.py` and `24_pwa.py` as above.
