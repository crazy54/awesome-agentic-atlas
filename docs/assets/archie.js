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
// `watch`, `sit`, `sleep`, thirteen Fortnite dances (the keys of `BEATS` below) and `walk`, a stride in
// place. Every clip but `walk` starts and ends on the idle's first pose. The director
// below idles for a few loops, then does one act -- a dance under moving-head lights, one of the others,
// or a walk off the edge of the page and a moonwalk back in -- and idles again. He talks as he goes, in
// speech and thought bubbles, and answers when poked: see `chatter()`.
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
    "floss": 12, "take-the-l": 8, "default-dance": 16, "orange-justice": 12, "robot": 8, "electro-shuffle": 10,
    "hype": 8, "boogie-down": 10, "get-griddy": 8, "billy-bounce": 8, "fresh": 8, "scenario": 8, "groove-jam": 10,
  };
  const DANCES = Object.keys(BEATS);
  const OTHERS = ["watch", "sit", "sleep", "walk-off"];

  let started = false;
  const go = () => {
    if (started || !allowed() || !webgl()) return;
    started = true;
    start().catch(() => { stop(); started = false; });   // any failure leaves the poster, where we began
  };
  let stop = () => {};

  async function start() {
    const T = await import("./three-archie.js");
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

    const gltf = await new T.GLTFLoader().loadAsync(new URL("archie.glb", import.meta.url).href);
    if (!allowed()) { started = false; return; }   // the reader resized or changed a setting meanwhile
    const actor = new T.Group();          // what the director moves and turns; the clips animate inside it
    actor.add(gltf.scene);
    scene.add(actor);
    const rig = lights(T, scene);

    // ---- Layout: a screen-wide canvas, and a frustum that keeps the slot's window where the poster was --
    const canvas = renderer.domElement;
    const header = slot.closest("header") || slot.parentElement;
    const host = slot.parentElement;       // the bubble and the poke target sit here, beside the slot
    const edge = {left: -8, right: 8, top: 5};
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
    const direct = async () => {
      if (asked && (DANCES.includes(asked) || OTHERS.includes(asked))) await act(asked);
      for (;;) {
        idling = true;
        await perform("idle", 2 + Math.floor(Math.random() * 2));
        idling = false;
        // A dance half the time, and never the same act twice running, unless the reader asked for one.
        const pool = (wish || Math.random() < 0.5 ? DANCES : OTHERS).filter(n => n !== last);
        wish = null;
        await act(pool[Math.floor(Math.random() * pool.length)]);
      }
    };
    // Asked for a dance (by poking, or by choosing the Prism skin): cut the idle short and dance next.
    // Mid-act, it waits for the act to end.
    const talk = chatter(T, {host, slot, header, camera, view, actor, head: gltf.scene.getObjectByName("head"),
      wish() {
        wish = true;
        if (idling && done) { const d = done; done = null; d(); }
      }});

    // ---- The loop: only ticks while someone can see it, the tab showing and the masthead on screen -----
    let seen = true, raf = 0, then = 0;
    const tick = dt => {
      clock += dt;
      for (let i = waits.length - 1; i >= 0; i--) if (waits[i].pred()) waits.splice(i, 1)[0].res();
      if (speed) frustum(view.slide + speed * view.ppm * dt);
      const dr = turnTo - actor.rotation.y;
      actor.rotation.y += Math.sign(dr) * Math.min(Math.abs(dr), 5 * dt);
      mixer.update(dt);
      const c = current && current.getClip(), n = c && BEATS[c.name];
      rig.update(dt, clock, actor.position.x,
                 n && rig.on ? {at: current.time / c.duration * n, rate: n / c.duration} : null);
      talk.update(dt, idling);
    };
    const frame = now => {
      raf = requestAnimationFrame(frame);
      // Measured off the frame timestamps, capped so that a stalled frame steps the scene by no more than
      // a tenth of a second rather than jumping clips to their ends.
      const dt = then ? Math.min(Math.max((now - then) / 1000, 0), 0.1) : 0;
      then = now;
      tick(dt);
      renderer.render(scene, camera);
    };
    const run = () => {
      const want = seen && !document.hidden;
      if (want && !raf) { then = 0; raf = requestAnimationFrame(frame); }
      if (!want && raf) { cancelAnimationFrame(raf); raf = 0; }
    };
    const io = new IntersectionObserver(([e]) => { seen = e.isIntersecting; run(); });
    io.observe(header);
    document.addEventListener("visibilitychange", run);
    addEventListener("resize", layout);

    play("idle", 1);
    mixer.update(0);
    layout();
    renderer.render(scene, camera);
    slot.appendChild(canvas);
    slot.style.backgroundImage = "none";    // the first frame is up, so the poster can go
    run();
    direct();

    stop = () => {
      cancelAnimationFrame(raf); raf = 0;
      io.disconnect();
      document.removeEventListener("visibilitychange", run);
      removeEventListener("resize", layout);
      waits.length = 0;                     // strands the director's pending act, which is the point
      talk.stop();
      canvas.remove();
      slot.style.backgroundImage = "";
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
  };

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

    let t = 0, shown = false, until = 0, bw = 0, bh = 0, free = 5, seen = true;
    const cooled = {};
    const show = (kind, vars = {}, reply = false) => {
      const [text, think] = pick(kind);
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
    const mo = new MutationObserver(() => {
      const d = document.documentElement.dataset;
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
    let away = 0, gone = 0, stirred = Date.now(), lonely = false;
    const vis = () => {
      if (document.hidden) { away = Date.now(); return; }
      if (away && Date.now() - away > 30000) react("welcome", 60);
      away = 0;
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
      if (pokes.length >= 4) { pokes.length = 0; hold = t + 2.5; show("pokes", {}, true); o.wish(); }
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
        poke.hidden = view.slide !== 0;
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
        document.removeEventListener("copy", copy);
        header.removeEventListener("mouseover", over);
        header.removeEventListener("click", click);
        header.removeEventListener("pointermove", hover);
        header.style.cursor = "";
        poke.remove(); bubble.remove(); said.remove(); style.remove();
      },
    };
  }

  // The light show, the kind an EDM stage hangs over its crowd, for the dances only. When a dance starts, a
  // truss with four moving heads drops in from above the header, bounces to a stop, and the heads come up.
  // Each throws a smoky cone of coloured light, plus a spotlight that actually colours him and a pool on the
  // floor. On the dance's beat the heads snap to new marks, pulse a little, and change colour at every
  // bar. A glow rises behind him. Once the rig is up, a laser "liquid sky" fades in overhead: a sheet of
  // light seen from below, rippling like the surface of the sea seen from under water. When the dance ends
  // it all fades, and the truss is hauled back up.
  //
  // Nothing strobes. A pulse is a fifth of the brightness, a colour change keeps the brightness it had,
  // and a fast dance pulses on every other beat, so no dance comes near three flashes a second. None of
  // this runs for a reader who has asked for reduced motion, because nothing here does.
  function lights(T, scene) {
    const group = new T.Group();
    group.visible = false;
    scene.add(group);
    const PALETTE = [0xff2bd6, 0x22e1ff, 0x8a5bff, 0xffb000].map(c => new T.Color(c));
    const SKY = [new T.Color(0x22e1ff), new T.Color(0x2bff9e)];
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
    const glow = frag => {
      const mat = new T.ShaderMaterial({
        uniforms: {color: {value: new T.Color()}, level: {value: 0}, haze: {value: 0}, time},
        vertexShader: `varying vec2 vUv; varying vec3 vN, vV, vW;
          void main() { vUv = uv; vN = normalize(normalMatrix * normal);
            vec4 w = modelMatrix * vec4(position, 1.0); vW = w.xyz;
            vec4 mv = viewMatrix * w; vV = normalize(-mv.xyz);
            gl_Position = projectionMatrix * mv; }`,
        fragmentShader: `uniform vec3 color; uniform float level, haze, time;
          varying vec2 vUv; varying vec3 vN, vV, vW;
          ${NOISE}
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
    // Two layers of slow noise, folded through a sine into thin bright ridges: caustics, or the lines a laser
    // sheet draws on smoke. Faded out towards every edge of the sheet, so it has no visible border.
    const SKYSHEET = `vec2 p = vW.xz * 0.8;
      float n = noise(vec3(p * 0.6, time * 0.22)) * 6.0 + noise(vec3(p * 1.7 + 3.0, time * 0.37)) * 2.0;
      float ridge = pow(1.0 - abs(sin(n * 3.14159)), 9.0);
      float fade = smoothstep(0.0, 0.2, vUv.x) * smoothstep(1.0, 0.8, vUv.x)
                 * smoothstep(0.0, 0.3, vUv.y) * smoothstep(1.0, 0.7, vUv.y);
      c = mix(color, vec3(1.0), 0.3 * ridge);
      a = (ridge * 0.9 + 0.1 * noise(vec3(p * 2.0, time * 0.3))) * fade;`;

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
    const sky = new T.Mesh(new T.PlaneGeometry(1, 30).rotateX(-Math.PI / 2), glow(SKYSHEET));
    group.add(back, sky);

    const hash = n => { const s = Math.sin(n * 12.9898) * 43758.5453; return s - Math.floor(s); };
    // Where head i points on beat b: somewhere on or around him, a new mark every beat.
    const mark = (b, i, cx, out) => out.set(cx + (hash(b * 4 + i) - 0.5) * 3.4,
                                           0.15 + hash(b * 4 + i + 0.37) * 1.3,
                                           (hash(b * 4 + i + 0.71) - 0.5) * 1.6);
    const smooth = x => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));
    const outBack = x => 1 + 2.2 * (x - 1) ** 3 + 1.2 * (x - 1) ** 2;   // overshoots, then settles at 1
    const from = new T.Vector3(), to = new T.Vector3(), o = new T.Vector3(), d = new T.Vector3();
    const mean = new T.Color();
    let top = 4, span = 3, drop = 0, level = 0, skyLevel = 0;
    return {
      on: false,
      place(edge) {
        top = edge.top - 0.3;
        span = Math.min(4.5, (edge.right - edge.left) / 2.8);
        heads.forEach((h, i) => { h.x = (i - 1.5) / 1.5 * span; });
        bar.scale.x = span * 2 + 0.8;
        sky.scale.x = (edge.right - edge.left) * 3;   // wider than the screen at the back
      },
      // `beat` is the dance's position in beats and its beats a second, or null between dances.
      update(dt, t, cx, beat) {
        time.value = t;
        // The truss drops first and the heads come up once it has landed. Going off, they fade out first
        // and the truss goes up after.
        if (this.on) drop = Math.min(1, drop + dt / 0.6);
        else if (level === 0) drop = Math.max(0, drop - dt / 0.7);
        level = Math.max(0, Math.min(1, level + (this.on && drop === 1 ? 3 : -3) * dt));
        skyLevel = Math.max(0, Math.min(1, skyLevel + (level === 1 ? 1.2 : -3) * dt));
        group.visible = drop > 0;
        if (!group.visible) { for (const h of heads) h.spot.intensity = 0; return; }
        const y = top + (1 - outBack(drop)) * 3;
        bar.position.set(0, y, -1.5);

        let pulse = 1, b = 0, f = 0;
        if (beat) {
          b = Math.floor(beat.at); f = beat.at - b;
          const every = beat.rate > 3 ? 2 : 1;
          pulse = 0.8 + 0.2 * (b % every ? 0 : Math.exp(-6 * f));
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
        sky.position.set(0, 2.65, -12);
        sky.material.uniforms.color.value.copy(SKY[0]).lerp(SKY[1], 0.5 + 0.5 * Math.sin(t * 0.3));
        sky.material.uniforms.level.value = skyLevel;
        sky.visible = skyLevel > 0;
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
