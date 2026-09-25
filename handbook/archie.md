# Archie, the mascot

Archie is the 3D robot in the homepage masthead. He idles, reacts, dances, plays pranks, has friends to
visit, and can put on a light show. He appears only on the homepage (`/`, built by `31_home.py`).

## Files

Every runtime file is under `docs/assets/`, written by hand, and served as-is. Sizes are as measured on 2026-09-25.

| File | Size | What it is |
|---|---|---|
| `archie.js` | 121 KB | The loader and the whole director: when to go live, which act next, speech, pranks, visits, the `window.archie` command API, and the rig's lighting (`lights()`, which exposes `window.archieRig`) |
| `three-archie.js` | 640 KB | The subset of three.js Archie uses, bundled once (see [below](#the-threejs-bundle)). Do not edit it by hand |
| `archie.glb` | | The animated model, with twenty named clips |
| `archie-3d.webp` | | The poster: a still of the idle's first frame. Shown before the model loads, and instead of it when the model cannot run |
| `archie-fx.js` | 15 KB | Stage effects: LED dance floor, fog, haze, CO2 jets, flames and sparks |
| `rig-show.js` | 8 KB | The rig's look book: `LOOKS` (colours), `GOBOS`, `LASERS` (laser graphics) and `PATTERNS` |
| `rig/rig.glb`, `rig/wall-{a,b,c,d}.{webm,mp4,webp}`, `rig-gobos/*.svg` | | Fixture models, LED-wall video loops and their posters, gobo masks |
| `archie-friends.js`, `archie-friends-data.js` | 39 KB, 17 KB | The friends' art and choreography; their roster and lines. `ORDER` is `nib`, `posy`, `lumen`, `oh-four`, `quack` |
| `archie-dance.js`, `archie-beat.js` | 13 KB, 3 KB | "Dance with me": the audio source picker and the AudioWorklet beat detector |
| `archie-admin.js` | 8 KB | The hidden admin panel |

The sources that generate the binaries are in `art/`:

| Source | Builds | Command |
|---|---|---|
| `art/archie/archie.py` | `docs/assets/archie.glb`, `art/archie/archie.blend`, `docs/assets/archie-3d.webp` | `blender --background --factory-startup --python art/archie/archie.py` |
| `art/rig/rig.py` | `docs/assets/rig/rig.glb`, `art/rig/rig.blend` | `blender --background --factory-startup --python art/rig/rig.py` |
| `art/rig/wall.py` | `docs/assets/rig/wall-*.{webm,mp4,webp}` | `python art/rig/wall.py [a b c d]`, or `--check` to measure and encode nothing. Needs numpy and Pillow, and runs Blender for its FFmpeg (set `BLENDER` if it is not at the default Windows path) |
| `art/archie/three-entry.js` | `docs/assets/three-archie.js` | see below |

Each script's docstring is the full reference.

## When he is live

`archie.js` switches from the poster to the live model only when all three of these hold:

- the viewport is at least **900 px** wide;
- the reader has **not** asked for reduced motion;
- the browser has **WebGL2**.

Otherwise he stays a poster, and the admin panel's buttons say why. `31_home.py` wires him into the page
only when `archie.js`, `archie-fx.js`, `three-archie.js`, `archie.glb` and `archie-3d.webp` all exist. Friends,
dance and the rig are optional: without them he still loads.

## Animation

`archie.glb` has 20 clips:

- **Everyday acts:** `idle`, `watch`, `sit`, `sleep`, `walk`, `press`, `shrug`.
- **Thirteen dances**, each listed in `BEATS` in `archie.js` with its length in beats: `floss`, `take-the-l`,
  `default-dance`, `orange-justice`, `robot`, `electro-shuffle`, `hype`, `boogie-down`, `get-griddy`,
  `billy-bounce`, `fresh`, `scenario`, `groove-jam`.

The lights keep time to those beat counts. **If you change a dance's rhythm in `archie.py`, change its
`BEATS` entry too.** The walk's ground speed (`WALK_SPEED`) is likewise derived from the clip's stride, so the feet
skate if the two drift apart.

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

`prank-check.mjs` checks that no prank leaves anything behind in storage.

## After editing Archie

Nothing under `docs/assets/` is cached by the service worker. Instead, **the page loads Archie's scripts
with a `?v=<hash>` query string**, and `archie.js` passes its own `?v=` on to the effects, the three.js
bundle, the model, the friends and the rig files. That hash is computed by `mascot_version()` in
`31_home.py`, over:

- the files in `VERSIONED`;
- the friend files and the `RIG` files, when present.

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
