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
// The model is `art/archie/archie.py`. Its clips are `idle` (a four-second loop: sway, foot tap, blinks),
// `watch`, `sit`, `sleep`, `press` and `shrug`, thirteen Fortnite dances of 15 or 16 seconds each (the keys
// of `BEATS` below) and `walk`, a stride in place. Every clip but `walk` starts and ends on the idle's first
// pose. The director below idles for a few loops, then does one act -- a dance under moving-head lights, a
// video wall and lasers over the page, on an LED floor in dry-ice fog with CO2, flames and sparks on cue
// (`archie-fx.js`), one of the others, or a walk off the edge of the page and a moonwalk
// back in -- and idles again. He talks as he goes, in speech and thought bubbles, and answers when poked:
// see `chatter()`. A reader who scrolls on down the page gets a visit now and then: see "Visits". Now and
// then, instead of an act, he plays a prank on the page, and it never quite works: see `pranks()`. And now
// and then a friend of his drops by and makes mischief of their own, which he tells them off for: see
// "Friends" below and `archie-friends.js`.
//
// THE CANVAS IS WIDER THAN THE SLOT. It spans the viewport's width and the header's height, so that he can
// walk out of the banner and so that the lights have somewhere to come from. The camera is the one the poster
// is rendered with: Blender's (0.9, -6.2, 1.55) aimed at z 1.08, a 70 mm lens on a 36 mm sensor, converted to
// glTF's Y-up. `layout()` gives it an off-centre frustum whose slot-sized window is exactly the poster's
// frame, so at rest he stands in the same pixels the poster did and the swap between them does not jump. If
// you move the camera here, move it in `stage()` too. The canvas takes no pointer events, so the header's
// links work through it; the one thing that does is a button over his body, for poking him.
(() => {
  const slot = document.querySelector(".mhmascot");
  if (!slot) return;
  const wide = matchMedia("(min-width: 900px)");
  const calm = matchMedia("(prefers-reduced-motion: no-preference)");
  const allowed = () => wide.matches && calm.matches;
  const webgl = () => {
    try { return !!document.createElement("canvas").getContext("webgl2"); } catch { return false; }
  };

  // The walk's ground speed, in metres a second, and it has to be the clip's: `STRIDE` = 32 degrees of leg
  // swing on a 0.57 m leg is 2 x 0.57 x sin 32 = 0.60 m a step, two steps in `WALK` = 24 frames at 30 fps.
  // Any other number and the feet skate.
  const WALK_SPEED = 1.5;
  const FOV = 2 * Math.atan(18 / 70);                  // radians, vertical, as the poster's camera
  // The dances, each with the number of beats its clip counts, which is what the lights keep time to.
  // They come from the clip functions in `archie.py`; change a dance's rhythm there and change it here.
  const BEATS = {
    "floss": 48, "take-the-l": 32, "default-dance": 48, "orange-justice": 48, "robot": 32, "electro-shuffle": 30,
    "hype": 32, "boogie-down": 30, "get-griddy": 32, "billy-bounce": 32, "fresh": 32, "scenario": 32, "groove-jam": 32,
  };
  const DANCES = Object.keys(BEATS);
  const OTHERS = ["watch", "sit", "sleep", "walk-off"];
  // A number in [0, 1) that looks random but is the same every time for the same n: the lights' marks.
  const hash = n => { const s = Math.sin(n * 12.9898) * 43758.5453; return s - Math.floor(s); };
  const smooth = x => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));

  // ---- Music ----------------------------------------------------------------------------------------
  // "Dance with me" (`archie-dance.js`) listens to the reader's music and tells this script about it in two
  // document events: `archie:music` {on, source} when music mode starts or stops, and `archie:beat`
  // {strength, bpm, at} on every onset it hears, `at` on the performance.now() clock. While music mode is on,
  // `window.archieMusic` has level() and bass() for reading every frame. The listeners are here rather than
  // in start(), so that a reader who turned the music on before the model loaded is dancing when it does.
  const music = {on: !!window.archieMusic, at: -1e9, bpm: null, kick: 0, fresh: false};
  document.addEventListener("archie:music", e => {
    music.on = !!(e.detail && e.detail.on);
    if (!music.on) { music.at = -1e9; music.bpm = null; }
  });
  document.addEventListener("archie:beat", e => {
    const d = e.detail || {};
    music.at = typeof d.at === "number" ? d.at : performance.now();
    if (d.bpm) music.bpm = d.bpm;
    music.kick = Math.max(0, Math.min(1, typeof d.strength === "number" ? d.strength : 1));
    music.fresh = true;
  });
  const loudness = () => {
    try { const m = window.archieMusic; return m ? Math.max(0, Math.min(1, m.level())) : 0; } catch { return 0; }
  };

  let started = false, pals = null;          // `pals`: the friends' visit controller, see "Friends"
  const go = () => {
    if (started || !allowed() || !webgl()) return;
    started = true;
    // Any failure leaves the poster, where we began, but says why: a half-cached release fails here, silently
    // otherwise.
    start().catch(e => { console.warn("Archie stayed a poster:", e); stop(); started = false; });
  };
  let stop = () => {};

  async function start() {
    // The page loads this script as `archie.js?v=<hash>`, the hash covering all three of its files, and the
    // same query goes on the two it loads. A release then changes all three URLs at once, so the HTTP cache
    // can never pair this script with an older renderer or model, or the reverse.
    const V = new URL(import.meta.url).search;
    // The stage effects (`archie-fx.js`: the dance floor, fog, haze, CO2, flames and sparks) come with it.
    const [T, FX] = await Promise.all([import(`./three-archie.js${V}`), import(`./archie-fx.js${V}`)]);
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

    const gltf = await new T.GLTFLoader().loadAsync(new URL(`archie.glb${V}`, import.meta.url).href);
    if (!allowed()) { started = false; return; }   // the reader resized or changed a setting meanwhile
    const actor = new T.Group();          // what the director moves and turns; the clips animate inside it
    actor.add(gltf.scene);
    scene.add(actor);
    const rig = lights(T, scene);

    // ---- Layout: a screen-wide canvas, and a frustum that keeps the slot's window where the poster was --
    const canvas = renderer.domElement;
    const header = slot.closest("header") || slot.parentElement;
    const host = slot.parentElement;       // the bubble and the poke target sit here, beside the slot
    const laser = lasers(header);
    const edge = {left: -8, right: 8, top: 5};
    const fx = FX.effects(T, scene, rig, edge, canvas);
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
    const worldAt = (x, y, W, H, z) => {                // canvas pixel -> the point on the plane at depth z
      const p = new T.Vector3(x / W * 2 - 1, 1 - y / H * 2, 0.5).unproject(camera);
      const d = p.sub(camera.position);
      return camera.position.clone().addScaledVector(d, (z - camera.position.z) / d.z);
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
      const feet = s.top - top + s.height * 0.84;
      edge.left = worldAt(0, feet, W, H, 0).x;
      edge.right = worldAt(W, feet, W, H, 0).x;
      edge.top = worldAt(view.cx, 0, W, H, -1.5).y;
      rig.place(edge);
      frustum(view.slide);
      // Canvas pixels -> the host's own coordinates, for the bubble and the poke target
      const hr = host.getBoundingClientRect();
      view.ox = -hr.left; view.oy = top - hr.top;
      talk.place();
    };

    // ---- Clips ----------------------------------------------------------------------------------------
    const mixer = new T.AnimationMixer(gltf.scene);
    const clip = Object.fromEntries(gltf.animations.map(a => [a.name, a]));
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
      return a;
    };
    mixer.addEventListener("finished", () => { const d = done; done = null; d && d(); });
    const perform = (name, reps = 1) => new Promise(res => { play(name, reps); done = res; });

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
      // Back in from the other side, facing the way he left and gliding backwards: the reversed walk.
      frustum(-view.cx - view.sw / 2);
      actor.rotation.y = turnTo = -Math.PI / 2;
      actor.visible = true;
      play("walk", Infinity).timeScale = -1;
      speed = WALK_SPEED;
      await until(() => view.slide >= 0);
      speed = 0;
      frustum(0);
      play("idle", 1);
      talk.act("back");
      await turn(0);
    };
    let last = "", idling = false, wish = null;
    // Music on, and a beat in the last two seconds: he dances, back to back, with no idles, visits or
    // walk-offs, and goes back to the director's own choices two seconds after the music stops. Not with
    // the masthead off screen, where nobody would see it and the loop would never stop.
    const grooving = () => music.on && seen && mode === "home" && performance.now() - music.at < 2000;
    const act = async name => {
      last = name;
      talk.act(name);
      if (name === "walk-off") return walkOff();
      rig.on = DANCES.includes(name);
      await perform(name);
      rig.on = false;
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
    const prankable = () => !talk.quiet && seen && mode === "home" && !music.on && !grooving() &&
      !pranking && !(pals && pals.busy) && Date.now() - lastPrank >= PRANK_GAP;
    let pranking = false;
    const prank = async name => {
      pranking = true;
      try { await prankOnce(name); } finally { pranking = false; }
    };
    const prankOnce = async name => {
      trick = trick || pranks(talk, header);
      if (!tricks.length) tricks = PRANKS.slice().sort(() => Math.random() - 0.5);
      name = name || tricks.pop();
      lastPrank = Date.now(); last = "prank";
      talk.say("prank-" + name);
      await perform("press");
      await trick[name]();
      talk.say("prank-" + name + "-after");
      await perform("shrug");
    };
    const direct = async () => {
      if (asked && (DANCES.includes(asked) || OTHERS.includes(asked))) await act(asked);
      if (forced && prankable()) await prank(forced);
      for (;;) {
        if (!grooving()) {
          idling = true;
          await perform("idle", 2 + Math.floor(Math.random() * 2));
          idling = false;
        }
        if (prankable() && Math.random() < 0.3) { await prank(); continue; }
        // A dance half the time, and never the same act twice running, unless the reader asked for one or
        // the music did.
        let pool = (wish || grooving() || Math.random() < 0.5 ? DANCES : OTHERS).filter(n => n !== last);
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
    const onScreen = r => r.top > 60 && r.bottom < innerHeight - 10 && r.left > 90 && r.right < innerWidth - 10;
    const pickTarget = () => {
      const all = [...document.querySelectorAll("main button, main [role=button]")].filter(b => {
        const r = b.getBoundingClientRect();
        return r.width >= 18 && r.width <= 320 && r.height >= 16 && r.height <= 80 && onScreen(r);
      });
      // He comes in from the left, so a button on the left half is a shorter walk
      const near = all.filter(b => b.getBoundingClientRect().left < innerWidth * 0.55);
      const from = near.length ? near : all;
      return from.length && Math.random() < 0.75 ? from[Math.floor(Math.random() * from.length)] : null;
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
      view.cx = x - grip.x; view.cy = y - grip.y;
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
    const visit = async () => {
      mode = "visit"; aborted = false; idling = false;
      const held = done; done = null;
      target = pickTarget();
      seat = innerWidth * (0.25 + Math.random() * 0.5);
      document.body.appendChild(layer);
      layer.appendChild(canvas);
      talk.move(layer, true);
      view.slide = 0;
      visitLayout();
      // In from just off the left of the window, facing right for the button; to sit, from the nearer side.
      const from = target || seat < innerWidth / 2 ? 1 : -1;
      frustum(from > 0 ? -view.cx - view.sw / 2 : view.W - view.cx + view.sw / 2);
      actor.rotation.y = turnTo = from * Math.PI / 2;
      play("walk", Infinity).timeScale = HURRY;
      speed = from * WALK_SPEED * HURRY;
      await vuntil(() => from * view.slide >= 0);
      speed = 0;
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
        talk.say("drop");
        await vperform("sit");
      }
      // Off by the nearer side of the window
      const way = view.cx < view.W / 2 ? -1 : 1;
      await vturn(way * Math.PI / 2);
      if (!aborted) play("walk", Infinity).timeScale = HURRY;
      speed = way * WALK_SPEED * HURRY;
      await vuntil(() => way < 0 ? view.cx + view.slide < -view.sw / 2 : view.cx + view.slide > view.W + view.sw / 2);
      // Home, whether he walked off or the visit was cut short, and back into the idle he left.
      speed = 0; target = null;
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
      timer = setTimeout(maybeVisit, asked === "visit" ? 1500 : 20000 + Math.random() * 25000);
    };
    const maybeVisit = () => {
      if (seen || mode === "visit" || document.hidden || talk.quiet) return;
      if (!idling || !done || music.on || Date.now() - scrolled < 1500 || Date.now() - lastVisit < 90000) {
        timer = setTimeout(maybeVisit, 3000);       // mid-act, mid-scroll or too soon: ask again shortly
        return;
      }
      visit();
      run();
    };
    const onScroll = () => { scrolled = Date.now(); };
    addEventListener("scroll", onScroll, {passive: true});

    // Asked for a dance (by poking, or by choosing the Prism skin): cut the idle short and dance next.
    // Mid-act, it waits for the act to end.
    const talk = chatter(T, {host, slot, header, camera, view, actor, head: gltf.scene.getObjectByName("head"),
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
    // looks like himself. Every light, the wall and the lasers take their beat from the clip's position, so
    // keeping the clip on the music keeps all of them on it. On each onset the clip's phase is compared
    // with the music's, and half the difference is made up over the next beat.
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
      grooved = g;
      if (n) current.timeScale = g && music.bpm ? tempo(c, n) : 1;
      mixer.update(dt);
      music.kick *= Math.exp(-6 * dt);
      const kick = g ? music.kick : null, loud = g ? loudness() : null;
      rig.update(dt, clock, actor.position.x,
                 n && rig.on ? {at: current.time / c.duration * n, rate: n / c.duration * current.timeScale,
                                kick, loud} : null);
      laser.update(dt, n && rig.on ? {at: current.time / c.duration * n, kick} : null, rig.level, beams());
      fx.update(dt, clock, actor.position.x, n && rig.on ? {at: current.time / c.duration * n, n, kick} : null,
                rig.level);
      talk.update(dt, idling);
      if (!seen && mode === "home" && idling) run();
    };
    // The truss's heads, where they are on the page, for the lasers
    const spots = [], hp = new T.Vector3();
    const beams = () => {
      if (!rig.level) return spots;
      const r = canvas.getBoundingClientRect();
      rig.heads.forEach((h, i) => {
        hp.copy(h.body.position).project(camera);
        spots[i] = {x: r.left + (hp.x + 1) / 2 * r.width, y: r.top + (1 - hp.y) / 2 * r.height,
                    rgb: h.color.getStyle().slice(4, -1)};
      });
      return spots;
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
      if (!want && raf) { cancelAnimationFrame(raf); raf = 0; laser.hide(); }
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
    import(`./archie-friends.js${V}`).then(F => {
      if (!started || stopped) return;
      pals = F.friends({header, slot, say: line => talk.say(line),
        free: () => !talk.quiet && seen && mode === "home" && idling && !pranking && !music.on && !grooving() &&
          actor.visible && view.slide === 0});
    }).catch(e => console.warn("Archie's friends stayed home:", e));
    let stopped = false;

    stop = () => {
      stopped = true;
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
      laser.stop();
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
.archie-sr{position:absolute;width:1px;height:1px;margin:0;overflow:hidden;clip-path:inset(50%);
  white-space:nowrap}`;

  const NAMES = {
    "floss": "the Floss", "take-the-l": "Take the L", "default-dance": "the Default",
    "orange-justice": "Orange Justice", "robot": "the Robot", "electro-shuffle": "the Electro Shuffle",
    "hype": "Hype", "boogie-down": "Boogie Down", "get-griddy": "the Griddy", "billy-bounce": "the Billy Bounce",
    "fresh": "Fresh", "scenario": "Scenario", "groove-jam": "Groove Jam",
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
           ["Merge conflicts are just git saying hi.", 1], ["Rate my visor. Go on. Very reflective."]],
    dance: [["Time for {n}!"], ["Lights! Camera! {n}!"], ["Deploying {n} to production."],
            ["DJ, drop the beat. It's {n} time."], ["Nobody asked for {n}. Too bad!"]],
    sit: [["Just resting my visor.", 1], ["So this is what 'blocked on review' feels like.", 1]],
    sleep: [["zzz... merge conflicts... zzz", 1], ["zzz... 404... zzz", 1], ["zzz... one more commit... zzz", 1]],
    watch: [["Is it Friday yet?"], ["The build has been running for how long?", 1]],
    leave: [["brb, CI is red."], ["Be right back, someone @-mentioned me."],
            ["Off to fetch more awesome-lists!"]],
    back: [["Did you miss me?"], ["Moonwalking is a valid deploy strategy."],
           ["I'm back! Nothing's on fire. Probably."]],
    light: [["Light mode! My visor has never been so shiny."], ["Whoa, bright! Adjusting visor..."]],
    dark: [["Ahh, the dark side. Easier on the circuits."], ["Lights down. Now it's a party."]],
    flip: [["It's a theme switch, not a fidget toy! ...okay, it is a bit fun."]],
    glass: [["Ooh, frosted glass. Very fancy."]],
    terminal: [["Terminal mode. I feel like I should be hacking something."]],
    prism: [["Prism?! Now THIS is a rave."]],
    graphite: [["Back to Graphite. Classic, like a good README."]],
    // The four newer skins; their copy is the designer's, from `ARCHIE` in `archie-friends-data.js`
    sherbet: [["Sherbet! My visor feels fizzy."]],
    riso: [["Riso! Everything's slightly misaligned. On purpose."]],
    blueprint: [["Blueprint. Finally, I can see how I was built."]],
    aurora: [["Aurora! Okay, this one's pretty."]],
    welcome: [["Welcome back! I didn't touch anything. Probably."], ["Oh hi! I was definitely not napping."]],
    up: [["Oh hey, you came back up!"], ["A visitor from further down the page!"]],
    lonely: [["...is this thing on?", 1], ["*taps visor* ...hello?", 1]],
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
    let hello = free === 0;

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
      pokes.push(t);
      while (pokes.length && pokes[0] < t - 6) pokes.shift();
      const guest = o.guest && o.guest();        // a friend is over: he answers about them, and does not dance
      if (guest) { pokes.length = 0; show(guest, {}, true); }
      else if (pokes.length >= 4) { pokes.length = 0; hold = t + 2.5; show("pokes", {}, true); o.wish(); }
      else if (t >= hold) { show("poke", {}, true); if (Math.random() < 0.2) o.wish(); }
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
    const hover = e => { header.style.cursor = onHim(e) ? "pointer" : ""; };
    header.addEventListener("click", click);
    header.addEventListener("pointermove", hover);

    const at = new T.Vector3();
    const menu = document.getElementById("setmenu");
    return {
      get quiet() { return quiet; },
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
        if (hello && t > 1.5) { hello = false; own("hello"); }
        else if (!hello && idling && !quiet) own("idle");
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
        header.style.cursor = "";
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

  // The light show, the kind an EDM stage hangs over its crowd, for the dances only. When a dance starts, a
  // truss with four moving heads drops in from above the header, bounces to a stop, and the heads come up.
  // Each throws a smoky cone of coloured light, plus a spotlight that actually colours him and a pool on the
  // floor. On the dance's beat the heads snap to new marks, pulse a little, and change colour at every
  // bar. A glow rises behind him, and an LED video wall hangs from the truss and drops in with it. The wall
  // shows an equaliser, rings, plasma, chevrons or a starburst: a new one every bar, all of them on the beat.
  // The lasers leave the scene altogether and go over the page: see `lasers()`. When the dance ends it all
  // fades, and the truss is hauled back up with the wall.
  //
  // Nothing strobes. A pulse is a fifth of the brightness, a colour change keeps the brightness it had,
  // and a fast dance pulses on every other beat, so no dance comes near three flashes a second. None of
  // this runs for a reader who has asked for reduced motion, because nothing here does.
  function lights(T, scene) {
    const group = new T.Group();
    group.visible = false;
    scene.add(group);
    const PALETTE = [0xff2bd6, 0x22e1ff, 0x8a5bff, 0xffb000].map(c => new T.Color(c));
    const time = {value: 0};
    const glows = [];

    // Every glowing surface here is one of these: the fragment sets `a`, how bright it is, and may change
    // `c` from the material's colour.
    //
    // On the dark theme they are light: colour added, alpha left alone. The canvas is transparent and
    // premultiplied, so a glow that wrote alpha would be an opaque dark shape over the page; with alpha 0
    // its colour adds to whatever the page shows behind it. On the light theme, adding light to a
    // near-white page gives white glare, so there they are a coloured haze laid over it instead. Only
    // blend factors and a uniform change, so switching theme mid-dance compiles nothing.
    const NOISE = `float hash(vec3 p) { p = fract(p * 0.3183099 + 0.1); p *= 17.0;
        return fract(p.x * p.y * p.z * (p.x + p.y + p.z)); }
      float noise(vec3 x) { vec3 i = floor(x), f = fract(x); f = f * f * (3.0 - 2.0 * f);
        return mix(mix(mix(hash(i), hash(i + vec3(1, 0, 0)), f.x),
                       mix(hash(i + vec3(0, 1, 0)), hash(i + vec3(1, 1, 0)), f.x), f.y),
                   mix(mix(hash(i + vec3(0, 0, 1)), hash(i + vec3(1, 0, 1)), f.x),
                       mix(hash(i + vec3(0, 1, 1)), hash(i + vec3(1, 1, 1)), f.x), f.y), f.z); }`;
    const tint = mat => {
      const light = document.documentElement.dataset.theme === "light";
      mat.uniforms.haze.value = light ? 1 : 0;
      mat.blendSrc = light ? T.SrcAlphaFactor : T.OneFactor;
      mat.blendDst = light ? T.OneMinusSrcAlphaFactor : T.OneFactor;
      mat.blendSrcAlpha = light ? T.OneFactor : T.ZeroFactor;
      mat.blendDstAlpha = light ? T.OneMinusSrcAlphaFactor : T.OneFactor;
    };
    const glow = (frag, uniforms = {}, defs = "") => {
      const mat = new T.ShaderMaterial({
        uniforms: {color: {value: new T.Color()}, level: {value: 0}, haze: {value: 0}, time, ...uniforms},
        vertexShader: `varying vec2 vUv; varying vec3 vN, vV, vW;
          void main() { vUv = uv; vN = normalize(normalMatrix * normal);
            vec4 w = modelMatrix * vec4(position, 1.0); vW = w.xyz;
            vec4 mv = viewMatrix * w; vV = normalize(-mv.xyz);
            gl_Position = projectionMatrix * mv; }`,
        fragmentShader: `uniform vec3 color; uniform float level, haze, time;
          varying vec2 vUv; varying vec3 vN, vV, vW;
          ${NOISE}
          ${defs}
          void main() { vec3 c = color; float a = 0.0;
            ${frag}
            a *= level;
            gl_FragColor = haze > 0.5 ? vec4(c, min(a * 0.45, 0.8)) : vec4(c * a * 0.6, 0.0); }`,
        transparent: true, depthWrite: false, side: T.DoubleSide, blending: T.CustomBlending,
      });
      tint(mat);
      glows.push(mat);
      return mat;
    };
    new MutationObserver(() => glows.forEach(tint))
      .observe(document.documentElement, {attributes: true, attributeFilter: ["data-theme"]});

    // Brightest down the middle of the cone and at the fixture, falling away at the edges and the far end,
    // and broken up by drifting smoke, which is what makes a transparent cone read as a beam in haze.
    const BEAM = `a = pow(abs(dot(vN, vV)), 2.0) * pow(vUv.y, 1.6)
        * (0.5 + 0.5 * noise(vW * 1.7 + vec3(0.0, -time * 0.3, time * 0.2)));`;
    const POOL = `a = pow(max(0.0, 1.0 - length(vUv - 0.5) * 2.0), 2.0) * 0.9;`;
    const BACK = `vec2 q = (vUv - 0.5) * 2.0;
      a = pow(max(0.0, 1.0 - length(q * vec2(1.0, 1.7))), 1.5)
        * (0.35 + 0.65 * noise(vec3(vW.xy * 0.9, time * 0.2))) * 0.3;`;
    // The video wall: a grid of round LEDs, each showing one sample of a picture. `modeA` fades into `modeB`
    // over a bar's first beat; `beat` is the dance's position in beats, and `eq` the equaliser's sixteen
    // bars, which the script sets because they jump on the beat.
    const SCREENS = `uniform vec2 grid; uniform float beat, modeA, modeB, fade, eq[16];
      vec3 hue(float x) { return 0.55 + 0.45 * cos(6.28318 * (x + vec3(0.0, 0.33, 0.67))); }
      vec3 screen(float m, vec2 q) {
        vec2 p = (q - 0.5) * vec2(grid.x / grid.y, 1.0);
        if (m < 0.5) {                                   // equaliser
          float x = fract(q.x * 16.0), h = eq[int(q.x * 16.0)];
          return step(q.y, h) * step(0.14, x) * step(x, 0.86) * mix(vec3(0.1, 1.0, 0.6), vec3(1.0, 0.2, 0.8), q.y);
        }
        if (m < 1.5) {                                   // a ring out from the middle every beat
          float d = length(p);
          return hue(d * 0.6 - beat * 0.25) * pow(0.5 + 0.5 * cos((d * 3.0 - beat) * 6.28318), 6.0);
        }
        if (m < 2.5) {                                   // plasma
          float v = sin(p.x * 5.0 + time) + sin(p.y * 7.0 - time * 1.3) + sin((p.x + p.y) * 4.0 + time * 0.7)
                  + sin(length(p) * 8.0 - time * 2.0);
          return hue(v * 0.15 + time * 0.05) * (0.55 + 0.45 * sin(v * 2.0));
        }
        if (m < 3.5) {                                   // chevrons marching up, a step a beat
          float v = fract((abs(p.x) * 0.8 - p.y) * 2.0 - beat * 0.5);
          return hue(floor(beat / 4.0) * 0.25 + p.x * 0.1) * smoothstep(0.55, 0.45, v);
        }
        float r = atan(p.y, p.x) + beat * 0.3927;        // a starburst turning a sixteenth a beat
        return hue(length(p) * 0.4 + beat * 0.1) * smoothstep(0.35, 0.65, 0.5 + 0.5 * cos(r * 8.0))
             * smoothstep(0.02, 0.2, length(p));
      }`;
    const WALL = `vec2 g = vUv * grid, q = (floor(g) + 0.5) / grid;
      vec3 v = mix(screen(modeA, q), screen(modeB, q), fade);
      float m = max(max(v.r, v.g), max(v.b, 1e-3));
      float led = m * smoothstep(0.5, 0.28, length(fract(g) - 0.5));
      c = v / m;
      a = led * 1.3;
      // Pale light vanishes into a light page, so there the LEDs are deeper and the panel shows, faintly.
      if (haze > 0.5) { c = mix(vec3(0.08, 0.09, 0.12), c * c, min(1.0, led * 2.0)); a = max(led * 2.2, 0.2); }`;
    // The fixtures themselves, dark metal, so the truss reads as hardware against the masthead.
    const metal = new T.MeshStandardMaterial({color: 0x16181d, metalness: 0.8, roughness: 0.35});
    const bar = new T.Mesh(new T.BoxGeometry(1, 0.07, 0.07), metal);
    group.add(bar);
    const L = 10;
    const cone = new T.CylinderGeometry(0.03, 0.7, L, 40, 1, true);
    cone.translate(0, -L / 2, 0);
    cone.rotateX(-Math.PI / 2);                         // apex at the origin, pointing down +Z for lookAt()
    const can = new T.CylinderGeometry(0.1, 0.13, 0.26, 20).rotateX(Math.PI / 2);
    const face = new T.CircleGeometry(0.095, 20).translate(0, 0, 0.131);
    const rod = new T.BoxGeometry(0.03, 0.2, 0.03);
    const heads = [0, 1, 2, 3].map(() => {
      const beam = new T.Mesh(cone, glow(BEAM));
      const body = new T.Mesh(can, metal);
      const lens = new T.Mesh(face, new T.MeshBasicMaterial({color: 0xffffff}));
      body.add(lens);
      const hang = new T.Mesh(rod, metal);
      const pool = new T.Mesh(new T.CircleGeometry(0.6, 32).rotateX(-Math.PI / 2), glow(POOL));
      // The spotlights stay in the scene at zero rather than being hidden with the rig: three.js compiles
      // its shaders for the number of lights, so adding four at the first dance would stall that frame.
      const spot = new T.SpotLight(0xffffff, 0, 0, 0.16, 0.6, 0);
      group.add(beam, body, hang, pool);
      scene.add(spot, spot.target);
      return {beam, body, lens, hang, pool, spot, x: 0, aim: new T.Vector3(), color: new T.Color()};
    });
    const back = new T.Mesh(new T.PlaneGeometry(9, 5), glow(BACK));
    const eq = new Array(16).fill(0);
    const wall = new T.Mesh(new T.PlaneGeometry(1, 1), glow(WALL, {
      grid: {value: {x: 60, y: 30}}, beat: {value: 0}, modeA: {value: 2}, modeB: {value: 2}, fade: {value: 1},
      eq: {value: eq}}, SCREENS));
    // Its frame, in the truss's metal: top, bottom and the two sides.
    const rails = [0, 1, 2, 3].map(() => new T.Mesh(new T.BoxGeometry(1, 1, 0.06), metal));
    group.add(back, wall, ...rails);

    // Where head i points on beat b: somewhere on or around him, a new mark every beat.
    const mark = (b, i, cx, out) => out.set(cx + (hash(b * 4 + i) - 0.5) * 3.4,
                                           0.15 + hash(b * 4 + i + 0.37) * 1.3,
                                           (hash(b * 4 + i + 0.71) - 0.5) * 1.6);
    const outBack = x => 1 + 2.2 * (x - 1) ** 3 + 1.2 * (x - 1) ** 2;   // overshoots, then settles at 1
    const from = new T.Vector3(), to = new T.Vector3(), o = new T.Vector3(), d = new T.Vector3();
    const mean = new T.Color();
    let top = 4, span = 3, drop = 0, level = 0, ww = 4, wh = 2;
    const screenFor = bar => Math.floor(hash(bar * 3.7 + 0.5) * 5);
    return {
      on: false,
      heads,
      get level() { return level; },
      // For `archie-fx.js`, so that its effects are drawn, and follow the theme, the way these are.
      glow, NOISE,
      lit(mat) { tint(mat); glows.push(mat); return mat; },
      place(edge) {
        top = edge.top - 0.3;
        span = Math.min(4.5, (edge.right - edge.left) / 2.8);
        heads.forEach((h, i) => { h.x = (i - 1.5) / 1.5 * span; });
        bar.scale.x = span * 2 + 0.8;
        // From just under the truss to just off the floor, and never much wider than it is tall
        ww = Math.min(span * 1.4, 6);
        wh = Math.max(1, top - 0.42);
        wall.scale.set(ww, wh, 1);
        wall.material.uniforms.grid.value = {x: Math.round(ww / 0.075), y: Math.round(wh / 0.075)};
      },
      // `beat` is the dance's position in beats and its beats a second, or null between dances.
      update(dt, t, cx, beat) {
        time.value = t;
        // The truss drops first and the heads come up once it has landed. Going off, they fade out first
        // and the truss goes up after.
        if (this.on) drop = Math.min(1, drop + dt / 0.6);
        else if (level === 0) drop = Math.max(0, drop - dt / 0.7);
        level = Math.max(0, Math.min(1, level + (this.on && drop === 1 ? 3 : -3) * dt));
        group.visible = drop > 0;
        if (!group.visible) { for (const h of heads) h.spot.intensity = 0; return; }
        const y = top + (1 - outBack(drop)) * 3;
        bar.position.set(0, y, -1.5);

        let pulse = 1, b = 0, f = 0;
        if (beat) {
          b = Math.floor(beat.at); f = beat.at - b;
          const every = beat.rate > 3 ? 2 : 1;
          // To music, the flash is the onset that was heard, as hard as it was heard.
          pulse = beat.kick != null ? 0.75 + 0.35 * beat.kick : 0.8 + 0.2 * (b % every ? 0 : Math.exp(-6 * f));
        }
        mean.setRGB(0, 0, 0);
        heads.forEach((h, i) => {
          h.hang.position.set(h.x, y - 0.1, -1.5);
          h.body.position.set(h.x, y - 0.3, -1.5);
          h.beam.position.copy(h.body.position);
          if (beat) {
            // Snap to the beat's mark over its first third, and hold.
            mark(b - 1, i, cx, from);
            mark(b, i, cx, to);
            h.aim.lerpVectors(from, to, smooth(f / 0.3));
            // A new colour every bar of four, cross-faded over half a beat.
            const bar4 = Math.floor(b / 4) + i;
            h.color.copy(PALETTE[(bar4 + 3) % 4]).lerp(PALETTE[bar4 % 4], smooth(((b % 4) + f) / 0.5));
          } else if (!h.aim.lengthSq()) {
            mark(0, i, cx, h.aim);
            h.color.copy(PALETTE[i]);
          }
          h.body.lookAt(h.aim);
          h.beam.lookAt(h.aim);
          h.beam.scale.set(1, 1, h.beam.position.distanceTo(h.aim) * 1.25 / L);
          h.beam.material.uniforms.color.value.copy(h.color);
          h.beam.material.uniforms.level.value = level * pulse;
          h.lens.material.color.copy(h.color).multiplyScalar(0.25 + 0.75 * level * pulse);
          h.spot.position.copy(h.body.position);
          h.spot.target.position.copy(h.aim);
          h.spot.color.copy(h.color);
          h.spot.intensity = 6 * level * pulse;
          // The pool is where the beam's line meets the floor.
          o.copy(h.body.position);
          d.subVectors(h.aim, o);
          h.pool.visible = d.y < -1e-3;
          if (h.pool.visible) {
            h.pool.position.copy(o).addScaledVector(d, -o.y / d.y).setY(0.01);
            h.pool.material.uniforms.color.value.copy(h.color);
            h.pool.material.uniforms.level.value = level * pulse;
          }
          mean.r += h.color.r / 4; mean.g += h.color.g / 4; mean.b += h.color.b / 4;
        });
        back.position.set(cx, 1.3, -2.4);
        back.material.uniforms.color.value.copy(mean);
        back.material.uniforms.level.value = level * pulse;
        // The wall hangs from the truss, so it drops and bounces with it.
        const wt = y - 0.12, u = wall.material.uniforms;
        wall.position.set(0, wt - wh / 2, -2.2);
        rails[0].position.set(0, wt, -2.2); rails[0].scale.set(ww + 0.1, 0.05, 1);
        rails[1].position.set(0, wt - wh, -2.2); rails[1].scale.set(ww + 0.1, 0.05, 1);
        rails[2].position.set(-ww / 2, wt - wh / 2, -2.2); rails[2].scale.set(0.05, wh, 1);
        rails[3].position.set(ww / 2, wt - wh / 2, -2.2); rails[3].scale.set(0.05, wh, 1);
        if (beat) {
          const bar4 = Math.floor(b / 4);
          u.beat.value = beat.at;
          u.modeA.value = screenFor(bar4 - 1);
          u.modeB.value = screenFor(bar4);
          u.fade.value = smooth((b % 4) + f);
          // Each bar of the equaliser jumps to a new height on the beat and sags until the next.
          // To music, as loud as the music is.
          const vol = beat.loud != null ? 0.35 + 0.75 * beat.loud : 1;
          for (let i = 0; i < 16; i++) {
            eq[i] = Math.min(1, (0.2 + 0.75 * hash(b * 16 + i * 1.31)) * (0.55 + 0.45 * Math.exp(-5 * f)) * vol);
          }
        } else {
          for (let i = 0; i < 16; i++) eq[i] *= Math.exp(-2 * dt);
        }
        u.level.value = level * 0.8;
      },
    };
  }

  // The lasers: from each head on the truss, beams that leave the masthead and play over whatever part of the
  // page the reader can see. They fan, wave, scissor, converge on a point that wanders the screen, or spin,
  // a new pattern every bar, cross-faded over its first beat, and they move with the beat.
  //
  // They are a 2D canvas fixed over the viewport, not part of the scene: the scene's canvas is only the
  // header's height. It takes no pointer events, and it is only there while a dance's lights are up and
  // the masthead, where Archie is, is at the top of the window: scroll most of it away and they fade out,
  // so a reader who has moved on to the page below is not danced at. As with the rest of the rig, nothing
  // strobes: the beams sweep, and a beat's pulse is a fifth of their brightness. On the dark theme they are
  // light, screened over the page; on the light theme, where light would not show, they are ink,
  // multiplied into it.
  function lasers(header) {
    const cv = document.createElement("canvas");
    cv.setAttribute("aria-hidden", "true");
    cv.style.cssText = "position:fixed;left:0;top:0;width:100%;height:100%;pointer-events:none;z-index:30;" +
      "display:none";
    document.body.appendChild(cv);
    const g = cv.getContext("2d");
    let fade = 0, B = 0, W = 0, H = 0;
    const TAU = Math.PI * 2;
    // Each pattern gives the angles, from straight down and positive to the right, of emitter e's beams at
    // beat B, given how many emitters there are (n) and where this one is on screen (x, y). In order: a fan
    // swinging, a wave, scissors, all of them on one wandering point, and spinning spokes.
    const PATTERNS = [
      (e, B) => [-2, -1, 0, 1, 2].map(k => k * 0.2 + 0.55 * Math.sin(B * Math.PI / 4 + e * Math.PI / 2)),
      (e, B) => [0, 1, 2, 3, 4, 5, 6].map(k => (k / 6 - 0.5) * 1.5 + 0.3 * Math.sin(B * Math.PI / 2 + k * 0.8 + e)),
      (e, B, n) => { const s = e < n / 2 ? 1 : -1, a = s * 0.75 * Math.sin(B * Math.PI / 4);
                     return [a, a + s * 0.22]; },
      (e, B, n, x, y) => {
        const tx = W * (0.5 + 0.4 * Math.sin(B * Math.PI / 8)), ty = H * (0.55 + 0.35 * Math.sin(B * Math.PI / 4 + 1));
        const a = Math.atan2(tx - x, ty - y);
        return [a - 0.05, a, a + 0.05];
      },
      (e, B) => [0, 1, 2, 3, 4, 5].map(k => k * TAU / 6 + B * Math.PI / 8 * (e % 2 ? 1 : -1)),
    ];
    const beam = (x, y, a, rgb, alpha, sheet) => {
      const L = Math.hypot(W, H) * 1.2, ex = x + Math.sin(a) * L, ey = y + Math.cos(a) * L;
      // A spinning beam fades out as it swings up past the horizontal, rather than going over the header.
      alpha *= smooth((Math.cos(a) + 0.1) / 0.3);
      if (alpha <= 0.004) return;
      const grad = g.createLinearGradient(x, y, ex, ey);
      grad.addColorStop(0, `rgba(${rgb},${alpha})`);
      grad.addColorStop(1, `rgba(${rgb},0)`);
      g.strokeStyle = grad;
      g.globalAlpha = 0.16; g.lineWidth = 8; g.beginPath(); g.moveTo(x, y); g.lineTo(ex, ey); g.stroke();
      g.globalAlpha = 1; g.lineWidth = 1.6; g.stroke();
      if (sheet) {                                  // a thin sheet of light between this beam and the next
        const bx = x + Math.sin(sheet) * L, by = y + Math.cos(sheet) * L;
        g.fillStyle = grad; g.globalAlpha = 0.07;
        g.beginPath(); g.moveTo(x, y); g.lineTo(ex, ey); g.lineTo(bx, by); g.fill();
        g.globalAlpha = 1;
      }
    };
    const draw = (p, pts, alpha) => {
      pts.forEach((pt, e) => {
        const as = PATTERNS[p](e, B, pts.length, pt.x, pt.y);
        as.forEach((a, k) => beam(pt.x, pt.y, a, pt.rgb, alpha, p === 0 && k < as.length - 1 && as[k + 1]));
      });
    };
    return {
      // `pts` are the heads, on screen, with their colours; `level` how far the lights are up.
      update(dt, beat, level, pts) {
        const r = header.getBoundingClientRect();
        const want = level > 0 && r.bottom > r.height * 0.6 ? level : 0;
        fade += Math.max(-3 * dt, Math.min(3 * dt, want - fade));
        if (fade <= 0.001) { cv.style.display = "none"; return; }
        if (cv.style.display) cv.style.display = "";
        if (W !== innerWidth || H !== innerHeight) { W = cv.width = innerWidth; H = cv.height = innerHeight; }
        B = beat ? beat.at : B + dt * 2;
        const light = document.documentElement.dataset.theme === "light";
        cv.style.mixBlendMode = light ? "multiply" : "screen";
        g.globalCompositeOperation = "source-over";
        g.clearRect(0, 0, W, H);
        g.globalCompositeOperation = light ? "source-over" : "lighter";
        g.lineCap = "round";
        const pulse = !beat ? 1 : beat.kick != null ? 0.75 + 0.35 * beat.kick : 0.8 + 0.2 * Math.exp(-6 * (beat.at % 1));
        const bar = Math.floor(B / 4), x = smooth(B % 4);
        const p = Math.floor(hash(bar * 5.3 + 0.2) * PATTERNS.length);
        const q = Math.floor(hash((bar - 1) * 5.3 + 0.2) * PATTERNS.length);
        const a = fade * pulse * (light ? 0.75 : 0.85);
        if (x < 1 && q !== p) draw(q, pts, a * (1 - x));
        draw(p, pts, q !== p ? a * x : a);
      },
      hide() { cv.style.display = "none"; fade = 0; },
      stop() { cv.remove(); },
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
