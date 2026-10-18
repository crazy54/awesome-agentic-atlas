// Archie in 3D, standing in the masthead's `.mhmascot` slot. Load it as `<script type="module">`, because
// it imports the renderer relative to its own URL.
//
// The slot's own CSS shows `archie-3d.webp`, the poster, and that is all most readers ever get. This script
// replaces the poster with the live model only when all of these hold: the screen is wide enough to show the
// slot (900 px, the width where the slot's CSS stops hiding it), the reader has not asked for reduced motion,
// and WebGL works. Nothing is fetched before the page's own `load`. The renderer (`three-archie.js`, about
// 160 KB gzipped) and the model (`archie.glb`) come after that, so the banner never competes with the
// page's content for bandwidth.
//
// The model is `art/pals/archie.py`, built from his model sheet, with his clips in `art/pals/clips/` and
// both baked by `art/pals/build.py`. `archie.glb` is the model and the everyday clips: `idle` (a four-second
// loop: a weight shift, a toe tap, a glance, blinks), `watch`, `sit`, `sleep`, `press` and `shrug`, `walk`
// (a stride in place) and `moonwalk` (ditto, backwards). `archie-dances.glb`, fetched in idle time once he is
// up, is the skeleton and face again with the fifteen dances of 15 or 16 seconds each (the keys of `BEATS`
// below). Every clip but `walk` and `moonwalk` starts and ends on the idle's first pose. The director
// below idles for a few loops, then does one act -- a dance, one of the others, or a walk off the edge of
// the page and a moonwalk back in -- and idles again. He talks as he goes, in speech and thought bubbles,
// and answers when poked: see `chatter()`. A reader who scrolls on down the page gets a visit now and then:
// see "Visits". Now and then, instead of an act, he plays a prank on the page, and it never quite works:
// see `pranks()`. And now and then a friend of his drops by and makes mischief of their own, which he tells
// them off for: see "Friends" below and `archie-friends.js`. He has a mood, which pokes raise and being
// ignored lowers, and a reader who has been around a while he tries, and fails, to get rid of: see "His
// mood" in `chatter()`, and `tiring()`.
//
// HE FOLLOWS THE READER. The index keeps this script's own URL, version and all, in sessionStorage's
// `archie-src`, and every other page of the site has a one-line script that imports it from there (see
// `follow()` in `scripts/19_pages.py`). A page with no `.mhmascot` of its own gets a corner of the window
// instead: `dock()`. So he only turns up on a page for a reader who met him on the index in this tab, as the
// same release of him, carrying the same mood, and never for one who turned on Quiet mode.
//
// THE CANVAS IS WIDER THAN THE SLOT. It spans the viewport's width and the header's height, so that he can
// walk out of the banner. The camera is the one the poster is rendered with: Blender's (0.9, -6.2, 1.55)
// aimed at z 1.08, a 70 mm lens on a 36 mm sensor, converted to glTF's Y-up. `layout()` gives it an
// off-centre frustum whose slot-sized window is exactly the poster's frame, so at rest he stands in the same
// pixels the poster did and the swap between them does not jump. If you move the camera here, move it in
// `stage()` too. The canvas takes no pointer events, so the header's links work through it; the one thing
// that does is a button over his body, for poking him.
(() => {
  // Off the index: a strip along the bottom of the window, for the canvas, with a smaller slot at its right
  // for him. Fixed, so he stays with the reader down the page, and taking no pointer events but his own.
  const dock = () => {
    const d = document.createElement("div");
    d.className = "archie-dock";
    d.style.cssText = "position:fixed;left:0;right:0;bottom:0;height:250px;pointer-events:none;z-index:28";
    const s = document.createElement("div");
    s.className = "mhmascot";
    s.setAttribute("aria-hidden", "true");
    s.style.cssText = "position:absolute;right:18px;bottom:-12px;width:150px;height:150px;pointer-events:none";
    d.appendChild(s);
    document.body.appendChild(d);
    return s;
  };
  const home = document.querySelector(".mhmascot");
  if (home) try { sessionStorage.setItem("archie-src", import.meta.url); } catch {}
  let followed = false;
  // Quiet mode is the loader's to check, and it never loads this: here it is only whether they have met.
  try { followed = !home && !!sessionStorage.getItem("archie-hi"); } catch {}
  if (!home && !followed) return;
  const slot = home || dock();
  const wide = matchMedia("(min-width: 900px)");
  const calm = matchMedia("(prefers-reduced-motion: no-preference)");
  const allowed = () => wide.matches && calm.matches;
  const webgl = () => {
    try { return !!document.createElement("canvas").getContext("webgl2"); } catch { return false; }
  };

  // The walk's ground speed, in metres a second, and it has to be the clip's: each foot slides back 0.60 m
  // while it is down, which is 62% of the 0.8 s stride (art/pals/clips/archie_base.py, WALK_SPEED there).
  // The moonwalk's ball foot holds the floor for half its 1 s stride while he glides 0.60 m back over it.
  // Any other number and the feet skate.
  const WALK_SPEED = 0.6 / (0.62 * 0.8), MOON_SPEED = 0.6 / 0.5;
  const FOV = 2 * Math.atan(18 / 70);                  // radians, vertical, as the poster's camera
  // The dances, each with the number of beats its clip counts, which is how a dance keeps time with the
  // reader's music (see `tempo()`). They come from the clip functions in `archie.py`; change a dance's
  // rhythm there and change it here.
  const BEATS = {
    "floss": 48, "take-the-l": 32, "default-dance": 48, "orange-justice": 48, "robot": 32, "electro-shuffle": 30,
    "hype": 32, "boogie-down": 30, "get-griddy": 32, "billy-bounce": 32, "fresh": 32, "scenario": 32, "groove-jam": 32,
    "headbang": 32, "the-drop": 32,
  };
  const DANCES = Object.keys(BEATS);
  // The rave dances are for the music's heavy parts, not for any time: see `heavy()` and `building()`.
  const RAVE = ["headbang", "the-drop"];
  // `core`: he takes the Atlas Core out of his belly and shows the world of the page the reader is on
  // (archie-core.js); only once the Core has loaded.
  const OTHERS = ["watch", "sit", "sleep", "walk-off", "core"];
  const smooth = x => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));

  // ---- Music ----------------------------------------------------------------------------------------
  // "Dance with me" (`archie-dance.js`) listens to the reader's music and tells this script about it in two
  // document events: `archie:music` {on, source} when music mode starts or stops, and `archie:beat`
  // {strength, bpm, at} on every onset it hears, `at` on the performance.now() clock. While music mode is on,
  // `window.archieMusic` has level() and bass() for reading every frame. The listeners are here rather than
  // in start(), so that a reader who turned the music on before the model loaded is dancing when it does.
  const music = {on: !!window.archieMusic, at: -1e9, bpm: null, fresh: false};
  document.addEventListener("archie:music", e => {
    music.on = !!(e.detail && e.detail.on);
    if (!music.on) { music.at = -1e9; music.bpm = null; }
  });
  document.addEventListener("archie:beat", e => {
    const d = e.detail || {};
    music.at = typeof d.at === "number" ? d.at : performance.now();
    if (d.bpm) music.bpm = d.bpm;
    music.fresh = true;
  });
  const loudness = () => {
    try { const m = window.archieMusic; return m ? Math.max(0, Math.min(1, m.level())) : 0; } catch { return 0; }
  };
  // How heavy the music is now against how it has been: its bass over about the last second (`fast`), and
  // the last ten (`slow`). A drop is the bass well over its own recent run: he headbangs. A build is the
  // bass gone out of it while the music carries on as loud: he bows his head and prays through it, and
  // bangs when it drops (`the-drop`). Relative, so a quiet song has drops too, and a mic across the room.
  const weight = {fast: 0, slow: 0};
  const heft = () => {
    try { const m = window.archieMusic; return m && m.bass ? Math.max(0, Math.min(1, m.bass())) : 0; } catch { return 0; }
  };
  const heavy = () => weight.fast > 0.4 && weight.fast > weight.slow * 1.35;
  const building = () => weight.slow > 0.3 && weight.fast < weight.slow * 0.55 && loudness() > 0.25;

  let started = false, pals = null;          // `pals`: the friends' visit controller, see "Friends"
  const go = () => {
    if (started || !allowed() || !webgl()) return;
    started = true;
    // Any failure leaves the poster, where we began, but says why: a half-cached release fails here, silently
    // otherwise.
    start().catch(e => { console.warn("Archie stayed a poster:", e); stop(); started = false; });
  };
  let stop = () => {};

  // ---- Commands -------------------------------------------------------------------------------------
  // One way in to everything he does, shared by the `?archie=` flags (see `direct()`) and the hidden admin
  // panel in the footer (`archie-admin.js`, which loads only when its trigger is pressed -- by a reader, or
  // by the site's admin panel, which `=admin1337` at the end of the address opens). `window.archie` is:
  //
  //   list()     every command name, in the panel's order: `dance:<a BEATS key>`, `idle`, `watch`, `sit`,
  //              `sleep`, `press`, `shrug`, `walk-off` (off the edge and the moonwalk back), `core`,
  //              `prank:<name>`, `bit:<name>`, `chatter`, `poke` and `quiet`.
  //              Friends are `friend:<id>`, one per id in `archie-friends-data.js`'s ORDER, which the panel
  //              reads for itself: listing them here would mean loading that file for every reader.
  //   can(cmd)   "" when `run(cmd)` would be taken now, or why not, in words for the panel's button. With
  //              the model not running -- reduced motion, a narrow screen, no WebGL -- everything says so.
  //   run(cmd)   true when taken (for `friend:<id>`, a promise of it). Acts queue behind whatever he is doing
  //              and cut an idle or a dance short; chatter, poke, a friend and `quiet` happen at once.
  //              `quiet` empties the queue, sends a visitor home and cuts the act short.
  //   status()   {act, queued}: the act he is on or last did, and the commands waiting; null with no model.
  //
  // NOT A SECURITY BOUNDARY. This is a static site with no server and no accounts: anybody can type
  // `=admin1337`, or call `window.archie.run()` from the console, and nothing here pretends otherwise.
  // Every command is something the director already does on its own; the panel only saves waiting for it.
  const CALM_ACTS = ["idle", "watch", "sit", "sleep", "press", "shrug", "walk-off", "core"];
  let live = null;                           // start()'s side, {can, run}, while the model is up
  const parse = cmd => (cmd.includes(":") ? cmd.split(/:(.*)/).slice(0, 2) : [cmd, ""]);
  window.archie = {
    list: () => [...DANCES.map(d => "dance:" + d), ...CALM_ACTS, ...PRANKS.map(p => "prank:" + p),
                 ...(live && live.bits ? live.bits().map(b => "bit:" + b) : []), "chatter", "poke", "quiet"],
    can: cmd => live ? live.can(String(cmd)) :
      !calm.matches ? "reduced motion is on, so Archie is a poster" :
      !wide.matches ? "the screen is under 900px, so Archie is hidden" :
      !webgl() ? "no WebGL here, so Archie is a poster" : "Archie is still loading",
    // A friend's answer is a promise, because the friend may have to be looked up first.
    run: cmd => (live && !live.can(String(cmd)) ? live.run(String(cmd)) : false),
    status: () => (live ? live.status() : null),
  };

  async function start() {
    // The page loads this script as `archie.js?v=<hash>`, the hash covering all three of its files, and the
    // same query goes on the two it loads. A release then changes all three URLs at once, so the HTTP cache
    // can never pair this script with an older renderer or model, or the reverse.
    const V = new URL(import.meta.url).search;
    const T = await import(`./three-archie.js${V}`);
    const renderer = new T.WebGLRenderer({alpha: true, antialias: true, powerPreference: "low-power"});
    // Capped lower than a page image would be: the canvas is the width of the screen.
    renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 1.5));
    renderer.outputColorSpace = T.SRGBColorSpace;
    renderer.toneMapping = T.NoToneMapping;   // the poster is Blender's "Standard" view, which is none either
    renderer.setClearColor(0x000000, 0);

    const scene = new T.Scene();
    const pmrem = new T.PMREMGenerator(renderer);
    scene.environment = pmrem.fromScene(new T.RoomEnvironment(), 0.04).texture;
    scene.environmentIntensity = 0.7;
    pmrem.dispose();
    // The poster's three area lights, in glTF's axes: key upper left, cool fill right, warm rim behind.
    for (const [x, y, z, i, c] of [[-2.2, 3, 3, 2.6, 0xfff2e0], [2.8, 1.4, 2.2, 0.7, 0xbfd1ff],
                                   [0.6, 2.8, -3, 2.4, 0xffbf66]]) {
      const l = new T.DirectionalLight(c, i);
      l.position.set(x, y, z);
      scene.add(l);
    }
    const camera = new T.PerspectiveCamera(FOV * 180 / Math.PI, 1, 0.1, 60);
    camera.position.set(0.9, 1.55, 6.2);
    camera.lookAt(0, 1.08, 0);
    camera.updateMatrixWorld();

    // The pals' GLBs are meshopt-compressed (art/pals/kit/export.py); the decoder is in the bundle.
    // Decoded off the main thread, in two workers: on a slow machine the page is still loading meanwhile.
    if (T.MeshoptDecoder.useWorkers) T.MeshoptDecoder.useWorkers(2);
    const loader = new T.GLTFLoader().setMeshoptDecoder(T.MeshoptDecoder);
    const gltf = await loader.loadAsync(new URL(`archie.glb${V}`, import.meta.url).href);
    if (!allowed()) { started = false; return; }   // the reader resized or changed a setting meanwhile
    const actor = new T.Group();          // what the director moves and turns; the clips animate inside it
    actor.add(gltf.scene);
    // culled by his bounds in the bind pose, which don't follow a clip, his eyes (small meshes of their own)
    // could vanish at the window's edge
    gltf.scene.traverse(n => { if (n.isSkinnedMesh) n.frustumCulled = false; });
    scene.add(actor);

    // ---- Layout: a screen-wide canvas, and a frustum that keeps the slot's window where the poster was --
    const canvas = renderer.domElement;
    const header = slot.closest("header") || slot.parentElement;
    const host = slot.parentElement;       // the bubble and the poke target sit here, beside the slot
    const view = {W: 1, H: 1, cx: 0, cy: 0, k: 1, sw: 240, sh: 240, ppm: 75, slide: 0, ox: 0, oy: 0};
    // The frustum, with its window `slide` CSS pixels right of the slot. This is how he walks: rather
    // than moving him through the scene, which would carry him out to where a screen-wide perspective
    // stretches everything sideways, the window moves and he stays where the poster's camera sees him, so
    // he is the same size and shape at every step, all the way off the page and back.
    const frustum = slide => {
      const {W, H, cy, k} = view, cx = view.cx + slide;
      view.slide = slide;
      camera.projectionMatrix.makePerspective(-cx * k, (W - cx) * k, cy * k, -(H - cy) * k,
                                              camera.near, camera.far);
      camera.projectionMatrixInverse.copy(camera.projectionMatrix).invert();
    };
    const layout = () => {
      const s = slot.getBoundingClientRect(), h = header.getBoundingClientRect();
      const W = document.documentElement.clientWidth, top = Math.min(h.top, s.top);
      const H = Math.max(1, Math.round(s.bottom - top));
      canvas.style.cssText = `position:absolute;left:${-s.left}px;top:${top - s.top}px;` +
        `width:${W}px;height:${H}px;pointer-events:none`;
      renderer.setSize(W, H, false);
      Object.assign(view, {W, H, cx: s.left + s.width / 2, cy: s.top - top + s.height / 2, sw: s.width,
                           sh: s.height, k: camera.near * Math.tan(FOV / 2) / (s.height / 2)});
      // CSS pixels per metre where he stands, which turns the walk's metres a second into a slide
      view.ppm = (s.height / 2) / (camera.position.distanceTo(new T.Vector3(0, 1.08, 0)) * Math.tan(FOV / 2));
      frustum(0);
      // Canvas pixels -> the host's own coordinates, for the bubble and the poke target
      const hr = host.getBoundingClientRect();
      view.ox = -hr.left; view.oy = top - hr.top;
      talk.place();
    };

    // ---- Clips ----------------------------------------------------------------------------------------
    const mixer = new T.AnimationMixer(gltf.scene);
    const clip = Object.fromEntries(gltf.animations.map(a => [a.name, a]));
    // What he can do without for his first seconds -- the dances, the Atlas Core, the pals' stage -- waits
    // until he is live and the page is idle: a slow machine is still finishing the page (and its poster is
    // still dancing to the music) while the model loads, and these would only take the main thread from it.
    let liveAt = null;
    const isLive = new Promise(res => { liveAt = res; });
    const later = (secs, fn) => isLive.then(() => new Promise(res => setTimeout(res, secs * 1000)))
      .then(() => new Promise(res => (window.requestIdleCallback || setTimeout)(res, {timeout: 4000})))
      .then(fn);
    // ---- The Atlas Core (archie-core.js): docked in his belly from the start, shown by the `core` act --
    let atlas = null, atlasUp = false;
    later(4, () => Promise.all([import(`./archie-core.js${V}`), import(`./archie-stage.js${V}`)])).then(([C, S]) => {
      const cv = new T.Vector3();
      atlas = C.atlas({T, V, base: new URL("./", import.meta.url), loader, model: gltf.scene, where: () => S.where(),
        project: name => staged().then(m => m.st.project(name)),
        // a point of his scene to the page, through the banner's camera (or the dock's, or a visit's)
        toPage: p => {
          cv.copy(p).project(camera);
          const r = canvas.getBoundingClientRect();
          return {x: r.left + (cv.x + 1) / 2 * r.width, y: r.top + (1 - cv.y) / 2 * r.height};
        },
        size: () => view.sh * 0.72, tone: root => S.tone(T, root)});
      return atlas.ready.then(() => { atlasUp = true; });
    }).catch(e => { console.warn("Archie's Atlas Core stayed home:", e); atlas = null; });
    // The dances come second: about half a megabyte the first screen does not need, fetched once he is up
    // (which is after the page's own load already). A dance asked for before they land waits for them, and
    // if they never land he idles instead. Their clips drive the same skeleton and face by name, so they
    // play on this model's mixer like its own.
    let dancesWanted = null;
    const dances = Promise.race([later(2, () => 0), new Promise(res => { dancesWanted = res; })])
      .then(() => loader.loadAsync(new URL(`archie-dances.glb${V}`, import.meta.url).href))
      .then(g => { for (const a of g.animations) clip[a.name] = a; })
      .catch(e => console.warn("Archie can't dance this time:", e));
    let current = null, done = null;
    const play = (name, reps = 1) => {
      const a = mixer.clipAction(clip[name]);
      a.reset();
      a.timeScale = 1;
      a.setLoop(reps === 1 ? T.LoopOnce : T.LoopRepeat, reps);
      a.clampWhenFinished = true;
      if (current && current !== a) a.crossFadeFrom(current, 0.25, false);
      a.play();
      current = a;
      slot.dataset.act = name;
      return a;
    };
    // Only the clip now playing: one cut off and fading out can still reach its end, and would end the next.
    mixer.addEventListener("finished", e => { if (e.action !== current) return; const d = done; done = null; d && d(); });
    // ---- The stage: the pals' bits (archie-stage.js, archie-bits.js) ------------------------------------
    // Loaded in idle time once he is up, so the admin panel can list the bits; the models a bit needs are
    // fetched only when it is about to play. A bit takes him off the masthead (or the dock) for its length,
    // the way a visit does, and gives him back to the idle he left.
    let stageMods = null;
    const staged = () => (stageMods ||= Promise.all([import(`./archie-stage.js${V}`), import(`./archie-bits.js${V}`)])
      .then(([S, B]) => {
        const st = S.stage({T, V, base: new URL("./", import.meta.url)});
        window.archieStage = {status: st.status, stop: st.stop, capture: st.capture, step: st.step};
        return {S, B, st};
      }));
    let bitsReady = null;
    later(6, () => staged().then(m => { bitsReady = m; cues(m); }))
      .catch(e => console.warn("Archie's stage is closed:", e));
    let bitting = false;
    const bitNames = () => (bitsReady ? Object.keys(bitsReady.B.BITS) : []);
    // Now and then, on its own: at most one bit every three minutes, the first no sooner than 45 seconds
    // into the page; each at most once a page view; only one that can play where the reader is, now (its
    // page, and its element on screen with room: `ready()`); never in Quiet mode, to music, during a prank
    // or a friend's visit, and never with an `?archie=` flag on the page, which is a test asking for
    // something else (`?archie=bit:<name>` plays that one).
    const BIT_GAP = 180000, BIT_FIRST = 45000;
    let lastBit = Date.now() - BIT_GAP + BIT_FIRST;
    const playedBits = new Set();
    const bitable = () => !asked && !talk.quiet && !music.on && !pranking && !bitting && !(pals && pals.busy) &&
      !!bitsReady && Date.now() - lastBit >= BIT_GAP;
    const pickBit = () => {
      const pool = bitNames().filter(n => !playedBits.has(n) && bitsReady.st.can({name: n, ...bitsReady.B.BITS[n]}));
      return pool.length ? pool[Math.floor(Math.random() * pool.length)] : null;
    };
    // A bit with a `cue` waits for its moment rather than its turn: something the reader does (scrolls a row
    // of cards, say). Its `cue(page, go)` is called once, when the bits load, to listen (passively: it only
    // ever reads), and calls `go()` when the moment comes; the bit then plays if Archie could play a bit now,
    // and is between acts -- a minute since the last bit is enough, as the reader asked for this one.
    const CUE_GAP = 60000;
    const cues = m => {
      for (const [name, b] of Object.entries(m.B.BITS)) {
        if (typeof b.cue !== "function") continue;
        try {
          b.cue(m.st.page, () => {
            if (asked || talk.quiet || music.on || pranking || bitting || (pals && pals.busy) || mode === "visit") return;
            if (!idling || !done || playedBits.has(name) || Date.now() - lastBit < CUE_GAP) return;
            if (m.st.can({name, ...b})) bitVisit(name);
          });
        } catch (e) { console.warn(`pals: ${name}'s cue`, e); }
      }
    };
    const playBit = async name => {
      const m = bitsReady || await staged();
      const b = m.B.BITS[name];
      if (!b || !m.st.can({name, ...b})) return;
      bitting = true;
      playedBits.add(name);
      lastBit = Date.now();
      last = "bit:" + name;
      const was = actor.visible;
      actor.visible = false;                         // he is on the stage now
      try {
        await m.st.run({name, ...b});
      } finally {
        actor.visible = was;
        bitting = false;
        play("idle", 1);
      }
    };
    const perform = async (name, reps = 1) => {
      if (!clip[name]) { dancesWanted(); await dances; }
      if (!clip[name]) name = "idle";
      return new Promise(res => { play(name, reps); done = res; });
    };

    // Waits measured on the render clock, so a hidden tab pauses the whole act rather than skipping it.
    let clock = 0;
    const waits = [];
    const until = pred => new Promise(res => waits.push({pred, res}));
    const after = secs => { const at = clock + secs; return until(() => clock >= at); };
    let speed = 0, turnTo = 0;
    const turn = async to => { turnTo = to; await until(() => Math.abs(actor.rotation.y - to) < 0.02); };

    // ---- The acts -------------------------------------------------------------------------------------
    // `speed` is in metres a second, and moves the frustum's window (see `frustum`), not him.
    const walkOff = async () => {
      if (Math.random() < 0.5) await perform("watch");   // late for something
      talk.act("leave");
      await turn(Math.PI / 2);                           // face screen right
      play("walk", Infinity);
      speed = WALK_SPEED;
      await until(() => view.cx + view.slide > view.W + view.sw / 2);
      speed = 0;
      actor.visible = false;
      await after(1.5 + Math.random() * 2);
      // Back in from the other side, facing the way he left and gliding backwards: the moonwalk.
      frustum(-view.cx - view.sw / 2);
      actor.rotation.y = turnTo = -Math.PI / 2;
      actor.visible = true;
      play("moonwalk", Infinity);
      speed = MOON_SPEED;
      await until(() => view.slide >= 0);
      speed = 0;
      frustum(0);
      play("idle", 1);
      talk.act("back");
      await turn(0);
    };
    let last = "", idling = false, wish = null;
    // Music on, and a beat in the last two seconds: he dances, back to back, with no idles, visits or
    // walk-offs. Not with the masthead off screen, where nobody would see it and the loop would never stop.
    // Two seconds without a beat, a quiet passage or the gap between songs, and he stops: the dance is cut
    // off where it was, and while music mode is on he only idles, waiting for the next beat. The director's
    // own choices come back when music mode goes off.
    const grooving = () => music.on && seen && mode === "home" && performance.now() - music.at < 2000;
    let walking = false;                   // out on a walk-off, which a command must not cut in half
    let dancing = false;                   // on a dance, which the music going quiet cuts short (see `tick`)
    const coreAct = async () => {
      if (!atlasUp) return perform("idle");
      await atlas.begin();
      talk.say("core");
      try { await perform("core-show"); } finally { atlas.end(); }
    };
    const act = async name => {
      last = name;
      talk.act(name);
      if (name === "walk-off") { walking = true; try { return await walkOff(); } finally { walking = false; } }
      if (name === "core") return coreAct();
      dancing = DANCES.includes(name);
      await perform(name);
      dancing = false;
    };
    // `?archie=<act>` starts on that act, for checking one without waiting through the idles.
    const asked = new URLSearchParams(location.search).get("archie");
    // A prank, now and then, in place of an act: at most one every three minutes, the first no sooner than
    // a minute in. Not in quiet mode, not while the music has him dancing, not out on a visit, and only
    // with the masthead on screen, so the reader sees who did it. `?archie=prank:<name>` plays that one
    // first, through the same gates, so quiet mode can be checked to stop it.
    const PRANK_GAP = 180000;
    let lastPrank = Date.now() - PRANK_GAP + 60000, trick = null, tricks = [];
    const forced = asked && asked.startsWith("prank:") && PRANKS.includes(asked.slice(6)) ? asked.slice(6) : "";
    if (forced) lastPrank = -1e9;
    let pranking = false;                  // declared above its readers, `prankable` and the friends' `free()`
    // Angry, he plays them as payback, and more often: every minute, and furious every forty seconds.
    const payback = () => talk.feel === "angry" || talk.feel === "furious";
    const prankGap = () => talk.feel === "furious" ? 40000 : talk.feel === "angry" ? 60000 : PRANK_GAP;
    const prankable = () => !talk.quiet && seen && mode === "home" && !music.on && !grooving() &&
      !pranking && !(pals && pals.busy) && Date.now() - lastPrank >= prankGap();
    const prank = async name => {
      pranking = true;
      try { await prankOnce(name); } finally { pranking = false; }
    };
    const prankOnce = async name => {
      trick = trick || pranks(talk, header);
      if (!tricks.length) tricks = PRANKS.filter(n => n !== "count" || header.querySelector(".sub b"))
        .sort(() => Math.random() - 0.5);
      name = name || tricks.pop();
      lastPrank = Date.now(); last = "prank";
      talk.say(payback() ? "revenge" : "prank-" + name);
      await perform("press");
      await trick[name]();
      talk.say("prank-" + name + "-after");
      await perform("shrug");
    };
    // Tired of the reader, eight minutes after the tab first met him and every four minutes after that,
    // he tries to get rid of them. Not a reader he adores, and through the same gates as a prank.
    // `?archie=tired:<name>` plays one first, whatever the time.
    const TIRED_AFTER = 480000, TIRED_GAP = 240000;
    const forcedTired = asked && asked.startsWith("tired:") && TIRES.includes(asked.slice(6)) ? asked.slice(6) : "";
    let lastTired = forcedTired ? -1e9 : 0, tire = null, tires = [], tiringNow = false;
    const tirable = () => !talk.quiet && seen && mode === "home" && !music.on && !grooving() &&
      talk.feel !== "adore" && (forcedTired || Date.now() - talk.since >= TIRED_AFTER) &&
      Date.now() - lastTired >= TIRED_GAP;
    const tired = async name => {
      tiringNow = true;
      try {
        tire = tire || tiring({host, slot, turn});
        if (!tires.length) tires = TIRES.slice().sort(() => Math.random() - 0.5);
        name = name || tires.pop();
        lastTired = Date.now(); last = "tired";
        talk.say("tired-" + name);
        if (name !== "sulk") await perform("press");
        await tire[name]();
        talk.say("tired-" + name + "-after");
        await perform("shrug");
      } finally { tiringNow = false; }
    };
    // Commands (see "Commands" at the top) wait here, and the director takes the next one before it
    // chooses for itself. A flag is one command queued before the first idle: `?archie=<act>` as it always
    // was, and `?archie=prank:<name>` through `prankable()`, so quiet mode can still be checked to stop it.
    // From the panel, a prank skips only the three-minute spacing. `?archie=tired:<name>` goes through
    // `tirable()` the same way.
    const orders = [];
    const obey = async ({cmd, flag}) => {
      const [kind, name] = parse(cmd);
      if (kind === "dance") return act(name);
      if (kind === "prank") return !flag || prankable() ? prank(name) : undefined;
      if (kind === "tired") return !flag || tirable() ? tired(name) : undefined;
      if (kind === "bit") return playBit(name);
      if (OTHERS.includes(cmd)) return act(cmd);
      last = cmd; talk.act(cmd);
      return perform(cmd, cmd === "idle" ? 2 : 1);           // idle, press, shrug: a clip, and no more
    };
    // Cut what he is doing short so the command goes next: an idle or a dance, never a walk-off (he would be
    // left off the edge of the page), a prank or a try at getting rid of the reader (its prop would be left on
    // the page).
    const cut = () => {
      if (done && mode === "home" && !walking && !pranking && !tiringNow && !bitting) { const d = done; done = null; d(); }
    };
    const direct = async () => {
      if (asked && (DANCES.includes(asked) || OTHERS.includes(asked))) orders.push({cmd: DANCES.includes(asked) ? "dance:" + asked : asked, flag: true});
      if (forced) orders.push({cmd: "prank:" + forced, flag: true});
      if (forcedTired) orders.push({cmd: "tired:" + forcedTired, flag: true});
      if (asked && asked.startsWith("bit:")) orders.push({cmd: asked, flag: true});
      for (;;) {
        if (orders.length) { await obey(orders.shift()); continue; }
        if (!grooving()) {
          idling = true;
          await perform("idle", 2 + Math.floor(Math.random() * 2));
          idling = false;
        }
        if (orders.length) continue;
        if (music.on && !grooving()) continue;
        if (tirable() && Math.random() < 0.3) { await tired(); continue; }
        if (prankable() && Math.random() < (payback() ? 0.6 : 0.3)) { await prank(); continue; }
        if (seen && bitable() && Math.random() < 0.4) { const b = pickBit(); if (b) { await playBit(b); continue; } }
        // A dance half the time, and never the same act twice running, unless the reader asked for one or
        // the music did.
        if (grooving() && (heavy() || building())) { wish = null; await act(heavy() ? "headbang" : "the-drop"); continue; }
        let pool = (wish || grooving() || Math.random() < 0.5 ? DANCES : OTHERS)
          .filter(n => n !== last && (!RAVE.includes(n) || n === wish) && (n !== "core" || atlasUp));
        if (grooving() && pool.some(fits)) pool = pool.filter(fits);
        wish = null;
        await act(pool[Math.floor(Math.random() * pool.length)]);
      }
    };
    // ---- Visits ---------------------------------------------------------------------------------------
    // A reader who has scrolled on down the page gets a visit now and then. He walks in from the left of the
    // window (the side that keeps his jabbing arm towards the camera) to a button on screen and tries to press it, which does nothing: it is a picture of him pressing,
    // drawn over the page, and the button never hears of it. He shrugs. Or, with no button to hand, he sits
    // down at the bottom of the window for a while. Then he walks off by the nearer side.
    //
    // The canvas goes with him. For the visit it is fixed over the whole window, with a smaller slot, so
    // that he is nearer the size of the page's text than of the masthead, and it comes home afterwards.
    // Scroll the button out of view or come back up to the masthead, and the visit is over at once.
    //
    // Visits only start from the idle. The visit holds the idle's promise and gives it back, so the director
    // carries on from where it was. Never in Quiet mode, and not more than once in 90 seconds.
    // `?archie=visit` makes the first one come 1.5 s after the masthead leaves the screen, for checking.
    //
    // Come down to sit, he has followed the reader down the page, so he comes down: a fireman's pole drops
    // in and he slides down it, or a lift arrives, dings, and he steps out. Either way he leaves by the
    // same, back up. Both are drawn in the visit's layer, behind him, hidden from assistive technology and
    // taking no pointer events. `?archie=visit:pole` and `?archie=visit:lift` ask for one of them.
    const VISIT = 150;                       // the visit's slot size, CSS pixels, against the masthead's 240
    const HURRY = 1.5;                       // he hurries on a visit: the clip and his speed, both, so no skating
    // The front of his right fist at a jab's full extension in `press`, turned to face screen right, which
    // puts that arm towards the camera: 0.74 m in front, 1.25 m up, 0.54 m to his right (from `archie.py`).
    // The button's left edge goes here.
    const FIST = new T.Vector3(0.74, 1.25, 0.54), FEET = new T.Vector3();
    const layer = document.createElement("div");
    layer.style.cssText = "position:fixed;left:0;top:0;width:100%;height:100%;pointer-events:none;z-index:29";
    let mode = "home", aborted = false, target = null, seat = 0, grip = {x: 0, y: 0}, lastVisit = -1e9;
    let timer = 0, scrolled = 0;
    // How far above where he stands he is drawn, in CSS pixels, eased from one height to another on the
    // render clock: the pole's slide. `anchor()` adds it every frame.
    let rise = {from: 0, to: 0, at: 0, secs: 1, ease: smooth};
    const height = () => {
      const k = Math.min(1, (clock - rise.at) / rise.secs);
      return rise.from + (rise.to - rise.from) * rise.ease(k);
    };
    const glide = (to, secs, ease) => {
      rise = {from: height(), to, at: clock, secs, ease};
      return vuntil(() => clock >= rise.at + secs);
    };
    const vafter = secs => { const at = clock + secs; return vuntil(() => clock >= at); };
    const prop = (cls, css, html = "") => {
      const el = document.createElement("div");
      el.className = cls;
      el.setAttribute("aria-hidden", "true");
      el.style.cssText = "position:absolute;pointer-events:none;" + css;
      el.innerHTML = html;
      layer.insertBefore(el, canvas);          // behind him
      return el;
    };
    const POLE_CSS = "top:0;width:12px;border-radius:6px;translate:0 -100%;transition:translate .45s ease-out;" +
      "background:linear-gradient(90deg,#6d747c,#f4f7fa 35%,#b9c0c7 55%,#5b6168);box-shadow:0 0 8px rgba(0,0,0,.35)";
    const LIFT_CSS = "width:118px;height:176px;border:4px solid #6d747c;border-radius:8px 8px 0 0;" +
      "background:#2b3036;box-shadow:0 10px 30px rgba(0,0,0,.45);transition:translate 1.4s cubic-bezier(.45,0,.25,1)";
    const LIFT_HTML = '<div class="archie-floor" style="position:absolute;left:50%;top:-30px;translate:-50% 0;' +
      'padding:3px 9px;border-radius:5px;background:#111;color:#ffb000;font:700 13px/1.2 ui-monospace,monospace">' +
      '\u25BC 3</div>' +
      '<div class="archie-door" style="position:absolute;left:0;top:0;width:50%;height:100%;' +
      'background:linear-gradient(90deg,#9aa2aa,#d5dade);border-right:1px solid #5b6168;transition:translate .5s ease-in-out"></div>' +
      '<div class="archie-door" style="position:absolute;right:0;top:0;width:50%;height:100%;' +
      'background:linear-gradient(90deg,#d5dade,#9aa2aa);border-left:1px solid #5b6168;transition:translate .5s ease-in-out"></div>';
    let props = [];
    const doors = (car, open) => {
      const [l, r] = car.querySelectorAll(".archie-door");
      l.style.translate = open ? "-100% 0" : "0 0";
      r.style.translate = open ? "100% 0" : "0 0";
      car.classList.toggle("open", open);
    };
    const floors = async (car, from, to) => {
      const sign = car.querySelector(".archie-floor");
      for (let f = from; ; f += from < to ? 1 : -1) {
        sign.textContent = (from < to ? "\u25B2 " : "\u25BC ") + (f === 0 ? "G" : f);
        if (f === to) return;
        await vafter(0.4);
      }
    };
    // Down the pole: it drops in beside where he will stand, he slides down it with a bump at the bottom, and
    // it goes back up without him.
    const poleDown = async () => {
      const pole = prop("archie-pole", `left:${seat - 6 - VISIT * 0.22}px;height:${innerHeight}px;` + POLE_CSS);
      props.push(pole);
      rise = {from: innerHeight, to: innerHeight, at: clock, secs: 1, ease: smooth};
      actor.rotation.y = turnTo = -Math.PI / 2;        // facing the pole
      play("idle", 1).timeScale = 0;                   // holding on
      requestAnimationFrame(() => { pole.style.translate = "0 0"; });
      await vafter(0.5);
      talk.say("pole");
      await glide(0, 1.1, k => k * k);                 // gravity: slow at the top, fast at the bottom
      await glide(10, 0.12, smooth);
      await glide(0, 0.18, smooth);
      pole.style.translate = "0 -100%";
    };
    const poleUp = async () => {
      const pole = props.find(e => e.classList.contains("archie-pole"));
      if (!pole) return;
      pole.style.translate = "0 0";
      await vturn(-Math.PI / 2);
      play("idle", 1).timeScale = 0;
      await vafter(0.5);
      await glide(innerHeight, 1.6, smooth);           // up is harder
      pole.style.translate = "0 -100%";
      await vafter(0.5);
    };
    // The lift: it comes down with him inside, out of sight, counts down its floors, dings and opens, and
    // he steps out in front of it. It goes back up empty, and comes back for him when he leaves.
    const liftDown = async () => {
      const car = prop("archie-lift", `left:${seat - 59}px;top:${innerHeight - 6 - 176}px;` +
        `translate:0 ${-innerHeight}px;` + LIFT_CSS, LIFT_HTML);
      props.push(car);
      actor.visible = false;
      requestAnimationFrame(() => { car.style.translate = "0 0"; });
      await floors(car, 3, 0);
      await vafter(0.3);
      doors(car, true);
      await vafter(0.5);
      actor.rotation.y = turnTo = 0;
      actor.visible = true;
      talk.say("lift");
      await vafter(0.6);
      doors(car, false);
      await vafter(0.5);
      car.style.translate = `0 ${-innerHeight}px`;
    };
    const liftUp = async () => {
      const car = props.find(e => e.classList.contains("archie-lift"));
      if (!car) return;
      car.style.translate = "0 0";
      await floors(car, 3, 0);
      doors(car, true);
      await vafter(0.6);
      actor.visible = false;
      doors(car, false);
      await vafter(0.5);
      car.style.translate = `0 ${-innerHeight}px`;
      await vafter(1.4);
    };
    const onScreen = r => r.top > 60 && r.bottom < innerHeight - 10 && r.left > 90 && r.right < innerWidth - 10;
    const pickTarget = () => {
      const all = [...document.querySelectorAll("main button, main [role=button]")].filter(b => {
        const r = b.getBoundingClientRect();
        return r.width >= 18 && r.width <= 320 && r.height >= 16 && r.height <= 80 && onScreen(r);
      });
      // He comes in from the left, so a button on the left half is a shorter walk
      const near = all.filter(b => b.getBoundingClientRect().left < innerWidth * 0.55);
      const from = near.length ? near : all;
      return from.length && !way && Math.random() < 0.5 ? from[Math.floor(Math.random() * from.length)] : null;
    };
    // Where world point p lands on screen, relative to the slot's centre: the frustum is a window slid
    // across the canvas, so that offset is the same wherever the slot is.
    const vp = new T.Vector3();
    const offsetOf = p => {
      const {cx, cy, slide} = view;
      view.cx = view.cy = 0;
      frustum(0);
      vp.copy(p).project(camera);
      const o = {x: (vp.x + 1) / 2 * view.W, y: (1 - vp.y) / 2 * view.H};
      view.cx = cx; view.cy = cy;
      frustum(slide);
      return o;
    };
    // The slot, moved so that his fist meets the button's left edge, or his feet the bottom of the window.
    // Every frame, because the button scrolls with the page.
    const anchor = () => {
      let x = seat, y = innerHeight - 6;
      if (target) {
        const r = target.getBoundingClientRect();
        if (!target.isConnected || r.bottom < 0 || r.top > innerHeight) { abortVisit(); return; }
        x = r.left + 2; y = r.top + r.height / 2;
      }
      view.cx = x - grip.x; view.cy = y - grip.y - height();
      frustum(view.slide);
    };
    const visitLayout = () => {
      const W = innerWidth, H = innerHeight;
      canvas.style.cssText = `position:absolute;left:0;top:0;width:${W}px;height:${H}px;pointer-events:none`;
      renderer.setSize(W, H, false);
      Object.assign(view, {W, H, sw: VISIT, sh: VISIT, ox: 0, oy: 0,
                           k: camera.near * Math.tan(FOV / 2) / (VISIT / 2)});
      view.ppm = (VISIT / 2) / (camera.position.distanceTo(new T.Vector3(0, 1.08, 0)) * Math.tan(FOV / 2));
      grip = offsetOf(target ? FIST : FEET);
      anchor();
    };
    const relayout = () => (mode === "visit" ? visitLayout() : layout());
    const vuntil = pred => until(() => aborted || pred());
    const vperform = name => (aborted ? Promise.resolve() : perform(name));
    const vturn = to => { turnTo = to; return vuntil(() => Math.abs(actor.rotation.y - to) < 0.02); };
    const abortVisit = () => {
      if (mode !== "visit" || aborted) return;
      aborted = true;
      const d = done; done = null; d && d();
    };
    // How he comes down to sit: asked for, or the pole and the lift two times in five each, and walking in.
    const way = ["visit:pole", "visit:lift"].includes(asked) ? asked.slice(6) : "";
    const visit = async () => {
      mode = "visit"; aborted = false; idling = false;
      const held = done; done = null;
      target = pickTarget();
      const r = Math.random();
      const by = target ? "walk" : way || (r < 0.4 ? "pole" : r < 0.8 ? "lift" : "walk");
      seat = innerWidth * (0.25 + Math.random() * 0.5);
      document.body.appendChild(layer);
      layer.appendChild(canvas);
      talk.move(layer, true);
      view.slide = 0;
      visitLayout();
      if (by === "pole") await poleDown();
      else if (by === "lift") await liftDown();
      else {
        // In from just off the left of the window, facing right for the button; to sit, from the nearer side.
        const from = target || seat < innerWidth / 2 ? 1 : -1;
        frustum(from > 0 ? -view.cx - view.sw / 2 : view.W - view.cx + view.sw / 2);
        actor.rotation.y = turnTo = from * Math.PI / 2;
        play("walk", Infinity).timeScale = HURRY;
        speed = from * WALK_SPEED * HURRY;
        await vuntil(() => from * view.slide >= 0);
        speed = 0;
      }
      if (!aborted) frustum(0);
      if (target) {
        talk.say("button");
        await vperform("press");
        if (!aborted) talk.say("broken");
        await vperform("shrug");
        if (!aborted && Math.random() < 0.4) {       // one more go, harder
          talk.say("again");
          await vperform("press");
          await vperform("shrug");
        }
      } else {
        await vturn(0);
        if (by === "walk") talk.say("drop");
        await vperform("sit");
      }
      if (by === "pole") await poleUp();
      else if (by === "lift") await liftUp();
      else {
        // Off by the nearer side of the window
        const off = view.cx < view.W / 2 ? -1 : 1;
        await vturn(off * Math.PI / 2);
        if (!aborted) play("walk", Infinity).timeScale = HURRY;
        speed = off * WALK_SPEED * HURRY;
        await vuntil(() => off < 0 ? view.cx + view.slide < -view.sw / 2 : view.cx + view.slide > view.W + view.sw / 2);
      }
      // Home, whether he walked off or the visit was cut short, and back into the idle he left.
      speed = 0; target = null;
      rise = {from: 0, to: 0, at: 0, secs: 1, ease: smooth};
      actor.visible = true;
      for (const e of props) e.remove();
      props = [];
      actor.rotation.y = turnTo = 0;
      slot.appendChild(canvas);
      layer.remove();
      talk.move(host, false);
      mode = "home";
      view.slide = 0;
      layout();
      play("idle", 1);
      done = held; idling = true;
      lastVisit = Date.now();
      run();
      plan();
    };
    const plan = () => {
      clearTimeout(timer);
      if (seen || mode === "visit") return;
      timer = setTimeout(maybeVisit, asked === "visit" || way ? 1500 : 20000 + Math.random() * 25000);
    };
    const maybeVisit = () => {
      if (seen || mode === "visit" || document.hidden || talk.quiet) return;
      if (!idling || !done || music.on || Date.now() - scrolled < 1500 || Date.now() - lastVisit < 90000) {
        timer = setTimeout(maybeVisit, 3000);       // mid-act, mid-scroll or too soon: ask again shortly
        return;
      }
      // Instead of a visit, sometimes, a bit: the reader is down the page, where most bits happen.
      if (bitable() && Math.random() < 0.5) {
        const b = pickBit();
        if (b) { bitVisit(b); return; }
      }
      visit();
      run();
    };
    // A bit played from the visit's timer: it holds the idle the director is waiting in, as a visit does,
    // and gives it back.
    const bitVisit = async name => {
      const held = done; done = null; idling = false;
      try { await playBit(name); } finally {
        done = held; idling = true;
        lastVisit = Date.now();
        run();
        plan();
      }
    };
    const onScroll = () => { scrolled = Date.now(); };
    addEventListener("scroll", onScroll, {passive: true});

    // Asked for a dance (by poking, or by choosing the Prism skin): cut the idle short and dance next.
    // Mid-act, it waits for the act to end.
    const talk = chatter(T, {host, slot, header, camera, view, actor, followed, head: gltf.scene.getObjectByName("head"),
      guest: () => (pals ? pals.poke() : null),
      wish() {
        wish = true;
        if (idling && done) { const d = done; done = null; d(); }
      }});

    // ---- The loop: only runs while the tab is showing, and only draws while someone can see him --------
    // With the masthead off screen it goes on ticking, undrawn, until he is back in the idle, and stops
    // there: that is where a visit can start from, and where he is when the reader scrolls back up.
    let seen = true, raf = 0, then = 0;
    // To the music: the dance runs at the track's tempo over its own, folded by octaves to the nearer (a
    // 170 bpm track takes a 120 bpm dance to 0.71x, not 1.42x) and held to 0.75x-1.35x so that he still
    // looks like himself. On each onset the clip's phase is compared with the music's, and half the
    // difference is made up over the next beat.
    let grooved = false, lock = 0, lockUntil = 0, octave = 1;
    // The rate for a dance of `own` beats a second, at whichever octave needs the least clamping, and how
    // many of the clip's beats go by for each of the music's.
    const fold = own => {
      let best = null;
      for (const k of [0.25, 0.5, 1, 2, 4]) {
        const r = music.bpm / 60 / own * k, miss = r < 0.75 ? 0.75 / r : r > 1.35 ? r / 1.35 : 1;
        if (!best || miss < best.miss) best = {r, k, miss};
      }
      return best;
    };
    // To music, only the dances that can keep time with it: at 128 bpm, the 120 bpm ones, and not
    // `floss`, whose 180 would need 0.71x.
    const fits = name => {
      const c = clip[name];
      if (!c) return false;                            // not landed yet (see `dances`)
      return !music.bpm || fold(BEATS[name] / c.duration).miss === 1;
    };
    const tempo = (c, n) => {
      const own = n / c.duration;                      // the clip's beats a second at 1x
      const {r, k} = fold(own);
      octave = k;
      if (music.fresh) {
        music.fresh = false;
        // Where the clip was at the onset, in its beats; `octave` clip beats go by for each music beat,
        // so a music beat should land on a multiple of min(1, octave) of them.
        const at = current.time / c.duration * n - (performance.now() - music.at) / 1000 * own * r;
        const span = Math.min(1, octave);
        let e = ((at % span) + span) % span;
        if (e > span / 2) e -= span;
        lock = Math.max(-0.15, Math.min(0.15, -0.5 * e / octave));
        lockUntil = clock + 60 / music.bpm;
      }
      if (clock > lockUntil) lock = 0;
      return Math.max(0.75, Math.min(1.35, r * (1 + lock)));
    };
    let heaving = "";
    const tick = dt => {
      clock += dt;
      if (mode === "visit") anchor();
      for (let i = waits.length - 1; i >= 0; i--) if (waits[i].pred()) waits.splice(i, 1)[0].res();
      if (speed) frustum(view.slide + speed * view.ppm * dt);
      const dr = turnTo - actor.rotation.y;
      actor.rotation.y += Math.sign(dr) * Math.min(Math.abs(dr), 5 * dt);
      const c = current && current.getClip(), n = c && BEATS[c.name];
      const g = grooving();
      if (g && !grooved) { talk.say("music"); if (idling && done) { const d = done; done = null; d(); } }
      // And when it goes quiet, the dance ends there; the director's idle cross-fades out of it.
      if (!g && grooved && dancing && done) { const d = done; done = null; d(); }
      if (g) {
        const h = heft();
        // From silence any music would read as a drop, so the music starting sets where it is heavy from.
        if (!grooved) weight.fast = weight.slow = h;
        weight.fast += (h - weight.fast) * (1 - Math.exp(-dt / 0.8));
        weight.slow += (h - weight.slow) * (1 - Math.exp(-dt / 10));
        // The drop, or the build, starting: whatever he was dancing gives way to it at once.
        const now = heavy() ? "headbang" : building() ? "the-drop" : "";
        if (now && now !== heaving && c && !RAVE.includes(c.name) && done) { const d = done; done = null; d(); }
        heaving = now;
      } else heaving = "";
      grooved = g;
      if (n) current.timeScale = g && music.bpm ? tempo(c, n) : 1;
      mixer.update(dt);
      if (atlas) atlas.tick(dt, current);
      talk.update(dt, idling);
      if (!seen && mode === "home" && idling) run();
    };
    const frame = now => {
      raf = requestAnimationFrame(frame);
      // Measured off the frame timestamps, capped so that a stalled frame steps the scene by no more than
      // a tenth of a second rather than jumping clips to their ends.
      const dt = then ? Math.min(Math.max((now - then) / 1000, 0), 0.1) : 0;
      then = now;
      tick(dt);
      if (seen || mode === "visit") renderer.render(scene, camera);
    };
    const run = () => {
      const want = !document.hidden && (seen || mode === "visit" || !idling);
      if (want && !raf) { then = 0; raf = requestAnimationFrame(frame); }
      if (!want && raf) { cancelAnimationFrame(raf); raf = 0; }
    };
    const io = new IntersectionObserver(([e]) => {
      seen = e.isIntersecting;
      if (seen) { clearTimeout(timer); abortVisit(); } else plan();
      run();
    });
    io.observe(header);
    document.addEventListener("visibilitychange", run);
    addEventListener("resize", relayout);

    play("idle", 1);
    mixer.update(0);
    layout();
    renderer.render(scene, camera);
    slot.appendChild(canvas);
    slot.style.backgroundImage = "none";    // the first frame is up, so the poster can go
    // Said out loud, for `archie-dance.js`, which bounces the poster to the music only while there is no
    // model: `.mhmascot[data-live]`, and an `archie:live` event each way.
    slot.dataset.live = "";
    liveAt();
    document.dispatchEvent(new CustomEvent("archie:live", {detail: {on: true}}));
    run();
    direct();

    // ---- Friends --------------------------------------------------------------------------------------
    // `archie-friends.js`, fetched only now that the first frame is up, under this script's own `?v=`. It
    // decides for itself whether anyone visits this page view, and asks `free()` before anyone does: he is
    // at home, on screen, idle, not dancing to music or mid-prank, and not in Quiet mode. What a friend
    // says to him goes through `talk.say`, which is his bubble and his Quiet mode. While one is visiting he
    // plays no prank (see `prankable`), and a poke gets an answer about the guest (see `chatter`).
    pals = null;
    let stopped = false;                   // set by `stop()` below; read when the import lands, which is later
    import(`./archie-friends.js${V}`).then(F => {
      if (!started || stopped) return;
      pals = F.friends({header, slot, say: line => talk.say(line),
        free: () => !talk.quiet && seen && mode === "home" && idling && !pranking && !music.on && !grooving() &&
          actor.visible && view.slide === 0});
    }).catch(e => console.warn("Archie's friends stayed home:", e));

    // ---- Commands, this side ---------------------------------------------------------------------------
    // What `window.archie` (see "Commands" at the top) asks of the running model. `can` answers from the same
    // state the director's own gates read; `run` queues acts for `direct()` and does the rest at once.
    const pokeTarget = () => host.querySelector(".archie-poke");
    live = {
      bits: bitNames,
      status: () => ({act: last, queued: orders.map(o => o.cmd)}),
      can(cmd) {
        const [kind, name] = parse(cmd);
        if (cmd === "quiet") return "";
        if (cmd === "chatter") return talk.quiet ? "Quiet mode is on" : "";
        if (cmd === "poke") return pokeTarget() && !pokeTarget().hidden ? "" : "he is out on a visit";
        if (kind === "friend") return !pals ? "his friends are still loading" : pals.busy ? "a friend is over already" :
          !seen || mode !== "home" ? "the masthead is off screen" : "";
        if (kind === "dance") return DANCES.includes(name) ? "" : "no such dance";
        if (kind === "bit") {
          if (!bitsReady) return "the stage is still loading";
          const b = bitsReady.B.BITS[name];
          return !b ? "no such bit" : bitting ? "a bit is on" :
            !bitsReady.st.can(b) ? "not here, or not now (its page or its element)" : "";
        }
        if (kind === "prank") return !PRANKS.includes(name) ? "no such prank" : pranking ? "a prank is on" :
          pals && pals.busy ? "a friend is over" : !seen ? "the masthead is off screen" : "";
        return CALM_ACTS.includes(cmd) ? "" : "no such command";
      },
      run(cmd) {
        const [kind, name] = parse(cmd);
        if (kind === "friend") return pals.send(name);
        if (cmd === "chatter") { talk.say("idle"); return true; }
        if (cmd === "poke") { pokeTarget().click(); return true; }
        if (cmd === "quiet") {
          orders.length = 0;
          if (pals) pals.leave();
          abortVisit();
          cut();
          return true;
        }
        orders.push({cmd, flag: false});
        abortVisit();                        // a visit gives the director back its idle, which is then cut
        cut();
        return true;
      },
    };

    stop = () => {
      stopped = true;
      live = null;
      if (pals) { pals.stop(); pals = null; }
      cancelAnimationFrame(raf); raf = 0;
      io.disconnect();
      document.removeEventListener("visibilitychange", run);
      removeEventListener("resize", relayout);
      removeEventListener("scroll", onScroll);
      clearTimeout(timer);
      layer.remove();
      waits.length = 0;                     // strands the director's pending act, which is the point
      talk.stop();
      canvas.remove();
      slot.style.backgroundImage = "";
      delete slot.dataset.live;
      document.dispatchEvent(new CustomEvent("archie:live", {detail: {on: false}}));
      renderer.dispose();
      started = false;
    };
  }

  // What he says, in speech bubbles and thought bubbles over the masthead. Three kinds of line:
  //
  //  - his own, at the start of an act or while he idles, one every 30 to 60 seconds at most;
  //  - reactions to the reader: switching theme or skin, coming back to the tab or up to the masthead,
  //    going quiet for a while, hovering a masthead link, copying something;
  //  - replies when he is poked. A button over his body takes the click (and the keyboard), and a reader
  //    who pokes enough gets a dance.
  //
  // A reader who turned on the catalogue's "Quiet mode" (`atlas-byte-quiet`) has asked the mascot not to
  // chat, so here too only a poke gets an answer. The bubble itself is hidden from assistive technology,
  // because a line every half minute announced into a screen reader is noise; a poke's reply, which the
  // reader asked for, goes to a polite live region instead.
  //
  // The bubble is HTML, not part of the scene, so it is crisp and takes the theme's colours. Each frame it
  // is moved to where the top of his head lands on screen. It never takes a pointer event, so the links
  // under it keep working.
  const CSS = `
.archie-say{position:absolute;left:0;top:0;z-index:1;width:max-content;max-width:220px;margin:0;
  padding:8px 12px;border:1px solid var(--grid);border-radius:14px;background:var(--band);color:var(--ink);
  font:500 13px/1.38 var(--ui);box-shadow:0 12px 28px rgba(0,0,0,.25);pointer-events:none;
  opacity:0;scale:.6;transform-origin:8px 100%;
  transition:opacity .16s ease-out,scale .24s cubic-bezier(.34,1.56,.64,1)}
.archie-say.on{opacity:1;scale:1}
.archie-say.l{transform-origin:calc(100% - 8px) 100%}
.archie-say::after{content:"";position:absolute;left:12px;bottom:-6px;width:10px;height:10px;
  background:inherit;border:solid var(--grid);border-width:0 1px 1px 0;transform:rotate(45deg)}
.archie-say.l::after{left:auto;right:12px}
.archie-say.think{border-radius:22px;font-style:italic}
.archie-say.think::after{left:4px;bottom:-15px;width:11px;height:11px;border-width:1px;border-radius:50%;
  transform:none}
.archie-say.think::before{content:"";position:absolute;left:-3px;bottom:-25px;width:6px;height:6px;
  border:1px solid var(--grid);border-radius:50%;background:inherit}
.archie-say.think.l::after{left:auto;right:4px}
.archie-say.think.l::before{left:auto;right:-3px}
.archie-poke{position:absolute;left:0;top:0;z-index:0;margin:0;padding:0;border:0;background:none;
  border-radius:45% 45% 30% 30%;cursor:pointer}
.archie-poke:focus-visible{outline:2px solid var(--link);outline-offset:2px}
.archie-dock .archie-poke{pointer-events:auto}
.archie-sr{position:absolute;width:1px;height:1px;margin:0;overflow:hidden;clip-path:inset(50%);
  white-space:nowrap}
.archie-heart{position:absolute;z-index:3;color:#ff2bd6;font:700 20px/1 var(--ui);pointer-events:none;
  opacity:0;animation:archie-heart 1.3s ease-out forwards}
@keyframes archie-heart{0%{opacity:0;translate:0 0;scale:.5}20%{opacity:1}100%{opacity:0;translate:0 -80px;scale:1.25}}
.archie-prop{position:absolute;z-index:3;pointer-events:none;font:700 13px/1 var(--ui)}
.archie-close{padding:9px 14px;border-radius:9px;background:#d93025;color:#fff;box-shadow:0 6px 18px rgba(0,0,0,.3);
  animation:archie-pop .25s cubic-bezier(.34,1.56,.64,1)}
.archie-close.stuck{animation:archie-stuck .12s linear 6}
@keyframes archie-pop{from{scale:.3;opacity:0}}
@keyframes archie-stuck{25%{translate:-3px 0}75%{translate:3px 0}}
.archie-sign{padding:10px 16px;border:3px solid #6b4a2b;border-radius:6px;background:#f4e3c1;color:#6b4a2b;
  letter-spacing:.12em;transform-origin:50% -40px;
  animation:archie-hang .6s cubic-bezier(.34,1.56,.64,1),archie-fall 1s cubic-bezier(.55,0,1,.45) 2.6s forwards}
.archie-sign::before,.archie-sign::after{content:"";position:absolute;bottom:100%;width:2px;height:40px;background:#6b4a2b}
.archie-sign::before{left:18%}.archie-sign::after{right:18%}
@keyframes archie-hang{from{translate:0 -160px}}
@keyframes archie-fall{20%{rotate:14deg}100%{rotate:70deg;translate:40px 260px;opacity:0}}`;

  const NAMES = {
    "floss": "the Floss", "take-the-l": "Take the L", "default-dance": "the Default",
    "orange-justice": "Orange Justice", "robot": "the Robot", "electro-shuffle": "the Electro Shuffle",
    "hype": "Hype", "boogie-down": "Boogie Down", "get-griddy": "the Griddy", "billy-bounce": "the Billy Bounce",
    "fresh": "Fresh", "scenario": "Scenario", "groove-jam": "Groove Jam",
    "headbang": "the Headbang", "the-drop": "the Drop",
  };
  // Each line is [text] for speech or [text, 1] for a thought. `{n}` is a dance's name, `{count}` the
  // masthead's own project count, so the joke can't go stale.
  const LINES = {
    hello: [["Hi! I'm Archie. I merged the awesome-lists so you don't have to."],
            ["Oh, hello! Welcome to the Atlas. Mind the cables."]],
    idle: [["Should I refactor myself? ...nah.", 1], ["Tabs or spaces. Tabs or spaces.", 1],
           ["It works on my machine. I AM the machine."], ["Fun fact: I'm 100% vibes and 0% unit tests."],
           ["What if the real awesome-list was the friends we starred along the way?", 1],
           ["{count} projects in here. I've read every README. Well, the first line."],
           ["git commit -m \"final final v2\"", 1], ["Psst. Discover has the good stuff."],
           ["Is it a bug or a feature? Depends who's asking.", 1],
           ["I'd help you search, but my hands are mostly decorative."],
           ["Merge conflicts are just git saying hi.", 1], ["Rate my crest. Go on. Hand-polished."]],
    dance: [["Time for {n}!"], ["Lights! Camera! {n}!"], ["Deploying {n} to production."],
            ["DJ, drop the beat. It's {n} time."], ["Nobody asked for {n}. Too bad!"]],
    sit: [["Just resting my eyes.", 1], ["So this is what 'blocked on review' feels like.", 1]],
    sleep: [["zzz... merge conflicts... zzz", 1], ["zzz... 404... zzz", 1], ["zzz... one more commit... zzz", 1]],
    watch: [["Is it Friday yet?"], ["The build has been running for how long?", 1]],
    leave: [["brb, CI is red."], ["Be right back, someone @-mentioned me."],
            ["Off to fetch more awesome-lists!"]],
    follow: [["You thought you could leave without me?"], ["Wait up! I'm coming too."],
             ["Following you. It's what I do now.", 1], ["Nice page. I'll hang out down here."],
             ["Don't mind me. Just tagging along."]],
    "follow-mad": [["Oh, you're HERE now? You didn't even say goodbye."], ["You left without poking me. Rude."],
                   ["I followed you all this way and still no poke?"], ["You can't escape me that easily."]],
    back: [["Did you miss me?"], ["Moonwalking is a valid deploy strategy."],
           ["I'm back! Nothing's on fire. Probably."]],
    light: [["Light mode! My ceramic has never been so shiny."], ["Whoa, bright! Adjusting crest..."]],
    dark: [["Ahh, the dark side. Easier on the circuits."], ["Lights down. Now it's a party."]],
    flip: [["It's a theme switch, not a fidget toy! ...okay, it is a bit fun."]],
    glass: [["Ooh, frosted glass. Very fancy."]],
    terminal: [["Terminal mode. I feel like I should be hacking something."]],
    prism: [["Prism?! Now THIS is a rave."]],
    graphite: [["Back to Graphite. Classic, like a good README."]],
    // The four newer skins; their copy is the designer's, from `ARCHIE` in `archie-friends-data.js`
    sherbet: [["Sherbet! My crest feels fizzy."]],
    riso: [["Riso! Everything's slightly misaligned. On purpose."]],
    blueprint: [["Blueprint. Finally, I can see how I was built."]],
    aurora: [["Aurora! Okay, this one's pretty."]],
    welcome: [["Welcome back! I didn't touch anything. Probably."], ["Oh hi! I was definitely not napping."]],
    up: [["Oh hey, you came back up!"], ["A visitor from further down the page!"]],
    lonely: [["...is this thing on?", 1], ["*taps ear cup* ...hello?", 1]],
    copy: [["Copying? Great taste. Star the originals too!"]],
    discover: [["Discover is where the fresh finds live."]],
    collections: [["Collections: like playlists, but for repos."]],
    leaderboard: [["Spoiler: the top of the leaderboard has a LOT of stars."]],
    catalog: [["The Catalogue has filters. So many filters."]],
    repo: [["Every project gets its own page. Even the weird ones."]],
    source: [["That's where my source lives. Be gentle."]],
    markdown: [["The Markdown version, for the purists."]],
    poke: [["Hey! That tickles."], ["Beep boop. You rang?"], ["I'm Archie. I live here."],
           ["Poke me a few more times and I might dance..."], ["Careful, I'm load-bearing."],
           ["Need a project? The Catalogue has thousands."]],
    pokes: [["Okay, okay! You want a dance? You get a dance!"]],
    // On a visit: walking up to a button, finding it does nothing, trying again, and sitting down instead
    button: [["Ooh, a button!"], ["What does this one do?"], ["I've always wanted to press one of these."],
             ["Don't mind me. Just pressing things."]],
    broken: [["...nothing?"], ["Huh. Must be a CSS button.", 1], ["I think it's decorative. Like my hands."],
             ["Works on my machine."], ["Should I file an issue?", 1]],
    again: [["Maybe if I press it HARDER."], ["Okay, one more time. With feeling."]],
    // The reader's music, the first beat of it
    music: [["Ooh, is this my jam?"], ["Now THIS is a banger."], ["You had me at the bass line."],
            ["Finally, a soundtrack for my code."], ["Is it 4/4? Please say it's 4/4.", 1]],
    drop: [["Mind if I sit here?"], ["Just visiting. Carry on."], ["It's quieter down here.", 1],
           ["Nice scroll position you've got."]],
    pole: [["Nee-naw! Coming down!"], ["Fireman's pole. The fastest way to follow a scroll."],
           ["Wheeeee!"], ["Did someone scroll? I'm on my way!"]],
    lift: [["Ding! Ground floor: you."], ["Going down? Me too."], ["The lift. Much more dignified.", 1],
           ["Mind the doors. I followed you down."]],
    // Pranks: the set-up, as he presses the button that does it, and the excuse, as it undoes itself
    "prank-lights": [["Ooh, what does this switch do?"], ["Watch this. Lights... OFF!"]],
    "prank-lights-after": [["Huh. It keeps coming back on."], ["You didn't see that. Nobody saw that."],
                           ["I was testing dark mode. For science.", 1]],
    "prank-skin": [["This place needs a makeover."], ["Prism. Everybody loves Prism."]],
    "prank-skin-after": [["Rejected. Tough crowd."], ["The page has taste, apparently.", 1]],
    "prank-tilt": [["Is the page crooked? Hang on..."], ["Let me just straighten this."]],
    "prank-tilt-after": [["There. Perfectly level. Don't check."], ["Close enough. Ship it."]],
    "prank-count": [["Let me just add myself to the count..."], ["One more project. Me. I'm the project."]],
    "prank-count-after": [["They took me back off. Rude."], ["Apparently a mascot is not a repository.", 1]],
    "prank-cursor": [["Mind if I drive for a bit?"], ["Your cursor is mine now."]],
    "prank-cursor-after": [["Okay, okay, you can have it back."], ["Driving is harder than it looks.", 1]],
    // His mood. Idle lines at each end of it, one line on the way down past each mark, and a poke's reply
    // when he adores the reader or has just been forgiven.
    adore: [["You're my favourite reader. Don't tell the others.", 1], ["Best. Visitor. Ever."],
            ["I'd star you if I could."]],
    sulk: [["Fine. Don't poke me. See if I care.", 1], ["I'm not sulking. You're sulking.", 1],
           ["Some people say hi to the mascot. Just saying."]],
    angry: [["You've been ignoring me for ages."], ["I have feelings. Mostly in the crest.", 1],
            ["Poke. Me. It's one click."]],
    furious: [["Right. That's it. There will be consequences."], ["Hell hath no fury like a mascot ignored."],
              ["I know where your theme setting lives."]],
    "to-sulk": [["Hello? I'm right here.", 1], ["Nobody pokes the mascot any more.", 1]],
    "to-angry": [["Okay, now I'm annoyed."], ["Ignoring me? Bold move."]],
    "to-furious": [["That's it. You've had your chance."], ["You're going to regret this."]],
    love: [["Aww! I love you too!"], ["You came back for me! \u{1F496}"], ["More pokes! More!"],
           ["This is the best day of my life."]],
    forgive: [["...okay, fine, I forgive you. Instantly. I'm weak."], ["You poked me! All is forgiven!"],
              ["I knew you cared!"]],
    revenge: [["This is for ignoring me."], ["Payback time."], ["You should have poked me."]],
    // The Atlas Core: the world of wherever the reader is, out of his pocket
    core: [["Behold. The whole atlas, in my pocket."], ["Ta-da! A world for every shelf."],
           ["Pocket universe. Please don't touch."], ["This is where we are. Roughly."],
           ["I keep it in my tummy. It's a long story.", 1]],
    // Tired of the reader: trying to get rid of them, and failing
    "tired-close": [["You know what? I'll close the tab for you."], ["Right. Closing time."]],
    "tired-close-after": [["Why won't it close?!"], ["...that button is decorative too, isn't it."]],
    "tired-sign": [["Sorry, we're closed. Go home."], ["Shop's shut. Come back never."]],
    "tired-sign-after": [["...we're a static site. We can't close."], ["Cheap nails.", 1]],
    "tired-shoo": [["Go on. Shoo. Scroll somewhere else."], ["Out you go. I need my space."]],
    "tired-shoo-after": [["The page is heavier than it looks."], ["You're still here, aren't you."]],
    "tired-sulk": [["I'm not talking to you."], ["I'll just face the wall, then.", 1]],
    "tired-sulk-after": [["...okay, I can't stay mad at you."], ["Fine. You can stay. For now."]],
  };
  // The tab's title while the reader is on another tab: one of these, once per page, and theirs back the
  // moment they return.
  const AWAY = ["Come back! \u{1F97A}", "Archie misses you", "Is anyone there?", "Psst. Over here."];

  function chatter(T, o) {
    const {host, slot, header, camera, view, actor, head} = o;
    const style = document.createElement("style");
    style.textContent = CSS;
    document.head.appendChild(style);
    const bubble = document.createElement("p");
    bubble.className = "archie-say";
    bubble.setAttribute("aria-hidden", "true");
    const said = document.createElement("p");
    said.className = "archie-sr";
    said.setAttribute("role", "status");
    const poke = document.createElement("button");
    poke.type = "button";
    poke.className = "archie-poke";
    poke.setAttribute("aria-label", "Poke Archie, the mascot");
    host.insertBefore(poke, slot);          // under the header's own text and links, which stay on top
    host.append(bubble, said);

    let quiet = false;
    try { quiet = localStorage.getItem("atlas-byte-quiet") === "1"; } catch {}
    const count = (header.querySelector(".sub b") || {}).textContent || "Thousands of";
    // A shuffled bag per kind of line, so none repeats until the rest have been said.
    const bags = {};
    const pick = kind => {
      if (!bags[kind] || !bags[kind].length) bags[kind] = LINES[kind].slice().sort(() => Math.random() - 0.5);
      return bags[kind].pop();
    };

    let t = 0, shown = false, until = 0, bw = 0, bh = 0, free = 5, seen = true, away = false;
    const cooled = {};
    // `kind` is a key of LINES, or a line itself, [text] or [text, 1], for what a visiting friend has him say.
    const show = (kind, vars = {}, reply = false) => {
      const [text, think] = Array.isArray(kind) ? kind : pick(kind);
      bubble.textContent = text.replace("{n}", vars.n || "").replace("{count}", count);
      bubble.classList.toggle("think", !!think);
      bubble.classList.add("on");
      bw = bubble.offsetWidth; bh = bubble.offsetHeight;
      shown = true;
      until = t + Math.min(6.5, 2 + bubble.textContent.length * 0.055);
      if (reply) said.textContent = bubble.textContent;
    };
    // His own lines wait for `free`; a reaction may cut in, but not more than once in `gap` seconds for
    // the same thing, and pushes his next line back so the two don't come in a rush.
    const own = (kind, vars) => {
      if (quiet || !seen || t < free) return;
      show(kind, vars);
      free = t + 30 + Math.random() * 30;
    };
    const react = (kind, gap = 10) => {
      if (quiet || !seen || t < (cooled[kind] || 0)) return;
      cooled[kind] = t + gap;
      show(kind);
      free = Math.max(free, t + 20);
    };
    try { if (!sessionStorage.getItem("archie-hi")) { sessionStorage.setItem("archie-hi", "1"); free = 0; } }
    catch {}
    let hello = free === 0 ? "hello" : "";

    // ---- His mood ----------------------------------------------------------------------------------------
    // -100 to 100, in sessionStorage, so it goes with the reader from page to page and is forgotten with the
    // tab. A poke is +20; the pointer resting on him, +2 a second; every second the masthead is on screen
    // and he goes unpoked, -0.3, so a reader who ignores him has him sulking in about a minute and a half,
    // angry in three, and furious in four and a half. One poke forgives any of it: anger never gets the
    // last word over a reader who comes back to him. `since` is when the tab first met him, which is what
    // he gets tired of. Quiet mode freezes it.
    const MOOD = "archie-mood", MARKS = [-25, -50, -80], DOWN = ["to-sulk", "to-angry", "to-furious"];
    let mood = 0, since = Date.now(), low = 0, hovering = false, kept = 0;
    try {
      const m = JSON.parse(sessionStorage.getItem(MOOD) || "null");
      if (m) { mood = Math.max(-100, Math.min(100, Number(m.v) || 0)); since = Number(m.since) || since; }
    } catch {}
    low = MARKS.filter(m => mood <= m).length;       // no announcing a mark he was already past
    const save = () => { try { sessionStorage.setItem(MOOD, JSON.stringify({v: Math.round(mood), since})); } catch {} };
    save();
    if (o.followed && !hello) { free = 0; hello = mood <= -25 ? "follow-mad" : "follow"; }
    const feel = () => mood >= 60 ? "adore" : mood <= -80 ? "furious" : mood <= -50 ? "angry" :
      mood <= -25 ? "sulk" : "";
    const hearts = () => {
      for (let i = 0; i < 5; i++) {
        const h = document.createElement("span");
        h.className = "archie-heart";
        h.textContent = "\u2665";
        h.setAttribute("aria-hidden", "true");
        h.style.cssText = `left:${poke.offsetLeft + poke.offsetWidth * (0.15 + 0.7 * Math.random())}px;` +
          `top:${poke.offsetTop + poke.offsetHeight * 0.15}px;animation-delay:${i * 90}ms`;
        host.append(h);
        setTimeout(() => h.remove(), 1500 + i * 90);
      }
    };

    // ---- The reader --------------------------------------------------------------------------------------
    let theme = document.documentElement.dataset.theme, skin = document.documentElement.dataset.skin;
    const flips = [];
    // Hushed while a prank of his own switches theme or skin, so he does not remark on what he did himself,
    // and does not take his Prism for the reader's and dance.
    let hushed = false;
    const mo = new MutationObserver(() => {
      const d = document.documentElement.dataset;
      if (hushed) { theme = d.theme; skin = d.skin; return; }
      if (d.theme !== theme) {
        theme = d.theme;
        flips.push(t);
        while (flips.length && flips[0] < t - 12) flips.shift();
        if (flips.length >= 3) { flips.length = 0; react("flip", 20); }
        else react(theme === "light" ? "light" : "dark", 0);
      }
      if (d.skin !== skin) {
        skin = d.skin;
        if (LINES[skin]) react(skin, 0);
        if (skin === "prism" && !quiet) o.wish();
      }
    });
    mo.observe(document.documentElement, {attributes: true, attributeFilter: ["data-theme", "data-skin"]});
    let hid = 0, gone = 0, stirred = Date.now(), lonely = false;
    // Four seconds on another tab and he takes over this one's title. It is put back as it was, the exact
    // string, and only if it is still his: another script may have set the title since.
    let titled = false, title = "", mine = "", pending = 0;
    const vis = () => {
      if (document.hidden) {
        hid = Date.now();
        if (!titled && !quiet) pending = setTimeout(() => {
          if (!document.hidden) return;
          titled = true; title = document.title;
          document.title = mine = AWAY[Math.floor(Math.random() * AWAY.length)];
        }, 4000);
        return;
      }
      clearTimeout(pending);
      if (mine && document.title === mine) document.title = title;
      mine = "";
      if (hid && Date.now() - hid > 30000) react("welcome", 60);
      hid = 0;
    };
    const io = new IntersectionObserver(([e]) => {
      seen = e.isIntersecting;
      if (!seen) gone = Date.now();
      else if (gone && Date.now() - gone > 8000) react("up", 45);
    });
    io.observe(header);
    const stir = () => { stirred = Date.now(); lonely = false; };
    const LINKS = [["discover", "discover"], ["collections", "collections"], ["leaderboard", "leaderboard"],
                   ["catalog", "catalog"], ["repo/", "repo"], ["mega-list", "markdown"], ["github.com", "source"]];
    const over = e => {
      const a = e.target.closest && e.target.closest("a[href]");
      if (!a || !header.contains(a) || e.relatedTarget && a.contains(e.relatedTarget)) return;
      const hit = LINKS.find(([bit]) => a.getAttribute("href").includes(bit));
      if (hit && Math.random() < 0.5) react(hit[1], 40);
    };
    const copy = () => react("copy", 30);
    const EVENTS = ["pointermove", "keydown", "scroll", "wheel", "touchstart"];
    for (const ev of EVENTS) addEventListener(ev, stir, {passive: true});
    document.addEventListener("visibilitychange", vis);
    document.addEventListener("copy", copy);
    header.addEventListener("mouseover", over);

    // Poked: a line every time, and a dance for four pokes in six seconds, or now and then for one. The
    // "four pokes" line holds for a moment rather than being talked over by the next poke.
    const pokes = [];
    let hold = 0;
    const poked = () => {
      const was = mood;
      mood = was <= -25 ? 30 : Math.min(100, mood + 20);
      low = 0;
      save();
      pokes.push(t);
      while (pokes.length && pokes[0] < t - 6) pokes.shift();
      const guest = o.guest && o.guest();        // a friend is over: he answers about them, and does not dance
      if (guest) { pokes.length = 0; show(guest, {}, true); }
      else if (was <= -25) { pokes.length = 0; hold = t + 2.5; show("forgive", {}, true); }
      else if (pokes.length >= 4) { pokes.length = 0; hold = t + 2.5; show("pokes", {}, true); o.wish(); }
      else if (t >= hold) { show(mood >= 60 ? "love" : "poke", {}, true); if (Math.random() < 0.2) o.wish(); }
      if (mood >= 60) hearts();
      if (!quiet) free = Math.max(free, t + 20);
    };
    poke.addEventListener("click", poked);
    // The button is what the keyboard reaches, but for the mouse the header's own text row lies over it,
    // and that row is where the links are. So a click that lands on the header over his body, and not on
    // anything that is itself clickable, is a poke too, and the pointer says so.
    const CLICKABLE = "a,button,input,select,textarea,label,summary,[tabindex]";
    const onHim = e => {
      if (poke.hidden || e.target === poke || !e.target.closest || e.target.closest(CLICKABLE)) return false;
      const r = poke.getBoundingClientRect();
      return e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom;
    };
    const click = e => { if (onHim(e)) poked(); };
    const hover = e => {
      const on = onHim(e);
      header.style.cursor = on ? "pointer" : "";
      hovering = on || e.target === poke;
    };
    const leave = () => { hovering = false; };
    header.addEventListener("pointerleave", leave);
    header.addEventListener("click", click);
    header.addEventListener("pointermove", hover);

    const at = new T.Vector3();
    const menu = document.getElementById("setmenu");
    return {
      get quiet() { return quiet; },
      get mood() { return mood; },
      get feel() { return feel(); },
      get since() { return since; },
      hush(on) { hushed = on; },
      // A line for a visit, said whether or not the masthead is on screen
      say(kind) {
        if (quiet) return;
        show(kind);
        free = Math.max(free, t + 20);
      },
      // Out on a visit, the bubble goes with him, and the poke target stays behind, hidden.
      move(parent, out) {
        away = out;
        parent.append(bubble);
        if (shown) { shown = false; bubble.classList.remove("on"); }
      },
      // The poke target: the middle of the slot, where his body is.
      place() {
        poke.style.cssText = `left:${slot.offsetLeft + view.sw * 0.3}px;top:${slot.offsetTop + view.sh * 0.1}px;` +
          `width:${view.sw * 0.4}px;height:${view.sh * 0.72}px`;
      },
      act(name) {
        if (hello) return;
        if (NAMES[name]) own("dance", {n: NAMES[name]});
        else if (LINES[name]) own(name);
      },
      update(dt, idling) {
        t += dt;
        // Only at home: carried out past the edge of the page, it would give the page a sideways scrollbar.
        poke.hidden = away || view.slide !== 0;
        if (hello && t > 1.5) { own(hello); hello = ""; }
        else if (!hello && idling && !quiet) own(feel() || "idle");
        if (!quiet && seen && !away) {
          mood = Math.max(-100, Math.min(100, mood + dt * (hovering ? 2 : -0.3)));
          const depth = MARKS.filter(m => mood <= m).length;
          if (depth > low) { low = depth; react(DOWN[depth - 1], 0); }
          if (t - kept > 2) { kept = t; save(); }
        }
        if (!lonely && Date.now() - stirred > 75000) { lonely = true; react("lonely", 120); }
        if (shown && t > until) { shown = false; bubble.classList.remove("on"); }
        if (!shown) return;
        // The top of his head, on screen, in the host's coordinates.
        head.getWorldPosition(at);
        at.y += 0.72;
        at.project(camera);
        const x = (at.x + 1) / 2 * view.W, y = (1 - at.y) / 2 * view.H;
        const off = !actor.visible || x < 0 || x > view.W || (menu && !menu.hidden);
        bubble.style.visibility = off ? "hidden" : "";
        if (off) return;
        const hx = x + view.ox, hy = y + view.oy;
        const left = x + 10 + bw > view.W - 8;           // no room on the right: open to the left
        bubble.classList.toggle("l", left);
        const bx = left ? hx - 10 - bw : hx + 10;
        const by = Math.max(view.oy + 4, hy - 18 - bh);
        bubble.style.translate = `${Math.round(bx)}px ${Math.round(by)}px`;
      },
      stop() {
        mo.disconnect(); io.disconnect();
        for (const ev of EVENTS) removeEventListener(ev, stir);
        document.removeEventListener("visibilitychange", vis);
        clearTimeout(pending);
        if (mine && document.title === mine) document.title = title;
        document.removeEventListener("copy", copy);
        header.removeEventListener("mouseover", over);
        header.removeEventListener("click", click);
        header.removeEventListener("pointermove", hover);
        header.removeEventListener("pointerleave", leave);
        header.style.cursor = "";
        save();
        poke.remove(); bubble.remove(); said.remove(); style.remove();
      },
    };
  }

  // What he does to the page when he plays a prank, and undoes. Each one returns a promise for when the page
  // is back as it was. None of it is saved: the theme and skin are changed on <html> only, never in
  // storage, and a reader who changes either while he is at it keeps their own, since their choice is
  // saved and his undo checks storage first. Nothing is typed into anything, nothing takes focus, nothing
  // moves under the pointer but a tilt of under a degree, and the waits are real time rather than the
  // render clock, so a tab hidden mid-prank is still put back.
  //
  // The lights are the reader's theme, swapped four times 400 ms apart: 1.25 flashes a second, where WCAG
  // 2.3.1 draws the line at three. Faster would be a seizure risk and not a joke, however funny it looks.
  const PRANKS = ["lights", "skin", "tilt", "count", "cursor"];
  function pranks(talk, header) {
    const root = document.documentElement;
    const wait = ms => new Promise(r => setTimeout(r, ms));
    const stored = k => { try { return localStorage.getItem(k); } catch { return null; } };
    // The observer's callback runs after the change, so the hush lifts a moment after the last one.
    const unhush = () => setTimeout(() => talk.hush(false), 60);
    return {
      async lights() {
        const theme = root.dataset.theme, saved = stored("theme");
        talk.hush(true);
        for (let i = 0; i < 4 && stored("theme") === saved; i++) {
          root.dataset.theme = root.dataset.theme === "light" ? "dark" : "light";
          await wait(400);
        }
        if (stored("theme") === saved) root.dataset.theme = theme;
        unhush();
      },
      async skin() {
        const skin = root.dataset.skin, saved = stored("atlas-skin");
        talk.hush(true);
        root.dataset.skin = skin === "prism" ? "terminal" : "prism";
        await wait(1400);
        if (stored("atlas-skin") === saved) root.dataset.skin = skin;
        unhush();
      },
      // Crooked, then over-corrected, then level: the page's <main>, not <body>, so the header and anything
      // pinned to the window stay where they are.
      async tilt() {
        const main = document.querySelector("main");
        if (!main) return;
        const was = [main.style.rotate, main.style.transition];
        main.style.transition = "rotate .45s cubic-bezier(.34,1.56,.64,1)";
        for (const deg of ["-0.6deg", "0.4deg", "0deg"]) { main.style.rotate = deg; await wait(900); }
        [main.style.rotate, main.style.transition] = was;
      },
      // The masthead's project count, one up, for four seconds, then back, if it is still his number.
      async count() {
        const b = header.querySelector(".sub b");
        const n = b && parseInt(b.textContent.replace(/[^0-9]/g, ""), 10);
        if (!n) return;
        const was = b.textContent, his = (n + 1).toLocaleString("en-US");
        b.textContent = his;
        await wait(4000);
        if (b.textContent === his) b.textContent = was;
      },
      // His cursor for four seconds, with its hotspot at the tip, where the reader's own arrow's is, so a
      // click lands where it always would.
      async cursor() {
        const svg = '<svg xmlns="http://www.w3.org/2000/svg" width="26" height="30" viewBox="0 0 26 30">' +
          '<path d="M3 2v22l6-6 4 9 4-2-4-9h8z" fill="#ff2bd6" stroke="#fff" stroke-width="2" ' +
          'stroke-linejoin="round"/><circle cx="8" cy="11" r="1.6" fill="#fff"/></svg>';
        const style = document.createElement("style");
        style.textContent = `html,html *{cursor:url("data:image/svg+xml,${encodeURIComponent(svg)}") 3 2,auto!important}`;
        document.head.appendChild(style);
        await wait(4000);
        style.remove();
      },
    };
  }

  // Tired of the reader: what he does to get rid of them, none of which works. Each is a prop drawn in the
  // masthead beside him, or a nudge to <main>, and each returns a promise for when it is gone again. Nothing
  // closes, navigates or takes focus: the close button is a picture of one, and the props take no pointer
  // events and are hidden from assistive technology, where a fake "Close tab" would be a lie.
  const TIRES = ["close", "sign", "shoo", "sulk"];
  function tiring(o) {
    const {host, slot, turn} = o;
    const wait = ms => new Promise(r => setTimeout(r, ms));
    const prop = (cls, text, left, top) => {
      const el = document.createElement("div");
      el.className = "archie-prop " + cls;
      el.textContent = text;
      el.setAttribute("aria-hidden", "true");
      el.style.left = left + "px";
      el.style.top = top + "px";
      host.append(el);
      return el;
    };
    return {
      async close() {
        const b = prop("archie-close", "\u2715  Close tab", slot.offsetLeft + slot.offsetWidth * 0.78,
                       slot.offsetTop + slot.offsetHeight * 0.38);
        await wait(700);
        b.classList.add("stuck");                    // pressed, and it only rattles
        await wait(1500);
        b.remove();
      },
      async sign() {
        const g = prop("archie-sign", "CLOSED", slot.offsetLeft + slot.offsetWidth * 0.18, slot.offsetTop + 44);
        await wait(3700);
        g.remove();
      },
      // A shove at the page: <main> slides a little away and springs back, as the tilt prank does it.
      async shoo() {
        const main = document.querySelector("main");
        if (!main) return;
        const was = [main.style.translate, main.style.transition];
        main.style.transition = "translate .7s cubic-bezier(.5,0,.75,0)";
        main.style.translate = "36px 0";
        await wait(900);
        main.style.transition = "translate .5s cubic-bezier(.34,1.56,.64,1)";
        main.style.translate = "0px 0";
        await wait(700);
        [main.style.translate, main.style.transition] = was;
      },
      async sulk() {
        await turn(Math.PI);
        await wait(4500);
        await turn(0);
      },
    };
  }

  // Leaving the conditions takes the model down and puts the poster back. Returning to them starts it
  // again, which costs no second download because both files are cached.
  const change = () => (allowed() ? go() : stop());
  wide.addEventListener("change", change);
  calm.addEventListener("change", change);
  const later = () => ("requestIdleCallback" in window ? requestIdleCallback(go, {timeout: 3000}) : setTimeout(go, 200));
  if (document.readyState === "complete") later(); else addEventListener("load", later, {once: true});
})();
