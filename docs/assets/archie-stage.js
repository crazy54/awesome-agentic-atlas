// The pals' stage: where Archie, Zip and Brick play their bits over the page. Imported by archie.js
// (`stage()`), which hands its own Archie off to it for the length of a bit, the way a visit does, and gets
// him back after. The bits themselves are `archie-bits.js`; the models, props, the Atlas Core and its worlds
// are built by art/pals/ (see art/pals/README.md) into assets/pals/.
//
// THE STAGE IS THE WINDOW. One canvas, fixed over the whole window, taking no pointer events and hidden from
// assistive technology, made when a bit starts and taken down when it ends. Its camera is orthographic and
// counts in CSS pixels, with y going up: a point x across and y down the window is (x, -y) in the scene. So
// a bit can stand Archie on the top edge of an element by reading its getBoundingClientRect() and nothing
// else, and two pals stand where they stand without a perspective pulling them apart. (The banner's own
// camera is a long 70 mm lens, which is most of the way to orthographic already, so the cast looks the
// same in both.) A pal is drawn `ppm` CSS pixels to the metre: 62.5 by default, which puts Archie's 2.4 m
// at 150 px, a visit's size.
//
// WHAT A BIT MAY DO. Everything a bit draws is decorative and aria-hidden, and takes no pointer events: the
// reader's cursor, buttons, text and ratings are never touched, and a prop that stands for one of them is a
// picture of it. A bit can borrow the page for a moment -- the theme, the way the lights prank does -- only
// through `s.page`, which puts it back exactly, storage first, and never more than three flashes a second.
// Any click, Escape or Tab ends a bit at once (WCAG 2.2.2: nothing moves for more than five seconds that the
// reader cannot stop): the cast leaves and the page is put back. So does Quiet mode, the tab going to the
// background, or the reader scrolling the bit's element out of view.
const PPM = 62.5;
const NS = "http://www.w3.org/2000/svg";                                   // CSS px per metre, for a bit that doesn't say
const CSS = `
.pals-stage{position:fixed;left:0;top:0;width:100%;height:100%;pointer-events:none;z-index:29}
.pals-stage canvas{position:absolute;left:0;top:0;pointer-events:none}
.pals-say{position:absolute;max-width:220px;margin:0;padding:6px 10px;border-radius:12px;background:#fff;
  color:#111;font:600 13px/1.3 system-ui,sans-serif;box-shadow:0 4px 14px rgba(0,0,0,.25);opacity:0;
  translate:-50% -100%;transition:opacity .2s;pointer-events:none;white-space:pre-line}
.pals-say.on{opacity:1}
.pals-say::after{content:"";position:absolute;left:50%;bottom:-6px;translate:-50% 0;border:6px solid transparent;
  border-bottom:0;border-top-color:#fff}
.pals-sign{position:absolute;pointer-events:none;font:800 15px/1.1 system-ui,sans-serif;letter-spacing:.02em}
@media (prefers-reduced-motion: reduce){.pals-stage{display:none}}
`;

// What each pal is, for the stage: its file, how tall it stands (metres, head top), and its walk: the clip,
// and the ground speed the clip was made for (metres a second), so its feet don't skate.
export const CAST = {
  archie: {glb: "archie.glb", extra: ["archie-dances.glb"], height: 2.25, walk: "walk", speed: 0.6 / (0.62 * 0.8)},
  zip: {glb: "pals/zip.glb", height: 1.75, walk: "walk", speed: 1.2},
  brick: {glb: "pals/brick.glb", height: 2.75, walk: "walk", speed: 0.9},
};

// Where the reader is, for a bit's `pages` and for the Atlas Core's world: the page family from the
// canonical URL (every page family has one), and the topic it is about when it is about one -- a topic or
// target page by its path, a project's page by the topic link in its breadcrumb, the catalogue by the
// topic in its hash.
export function where(doc = document, loc = location) {
  const canon = doc.querySelector('link[rel="canonical"]');
  const path = canon ? new URL(canon.href).pathname : loc.pathname.replace(/^\/awesome-agentic-atlas/, "");
  const seg = path.split("/").filter(Boolean);
  const topicLink = () => {
    const a = doc.querySelector('a[href*="topic/"]');
    const m = a && a.getAttribute("href").match(/topic\/([a-z0-9-]+)\//);
    return m ? m[1] : null;
  };
  if (!seg.length) return {page: "home", topic: null, world: "home"};
  if (seg[0] === "topic") return {page: "topic", topic: seg[1] || null, world: seg[1] || "home"};
  if (seg[0] === "repo") {
    const t = seg.length > 2 ? topicLink() : null;
    return {page: seg.length > 2 ? "repo" : "repos", topic: t, world: t || "home"};
  }
  if (seg[0] === "catalog") {
    const m = loc.hash.match(/topic=([a-z0-9-]+)/);
    return {page: "catalog", topic: m ? m[1] : null, world: m ? m[1] : "home"};
  }
  if (seg[0] === "discover") return {page: "discover", topic: null, world: "discover"};
  if (seg[0] === "collections") return {page: "collections", topic: null, world: "collections"};
  if (seg[0] === "target") return {page: "target", topic: null, world: seg[1] === "mcp" ? "mcp-servers" : "home"};
  if (/^404|not found/i.test(doc.title)) return {page: "lost", topic: null, world: "lost"};
  return {page: seg[0], topic: null, world: "home"};
}

export function stage(o) {
  const {T, V, base} = o;                           // three, the release's `?v=` query, assets/ URL
  const url = f => new URL(f + V, base).href;
  const loader = new T.GLTFLoader().setMeshoptDecoder(T.MeshoptDecoder);
  const files = new Map();
  const fetchGLB = f => {
    if (!files.has(f)) files.set(f, loader.loadAsync(url(f)));
    return files.get(f);
  };

  const style = document.createElement("style");
  style.textContent = CSS;
  document.head.appendChild(style);

  let layer = null, renderer = null, scene = null, camera = null, raf = 0, then = 0, W = 1, H = 1, svgLayer = null;
  let clock = 0, running = null, aborted = false;
  const waits = [], tickers = new Set(), actors = {}, mixers = new Set();

  // ---- the clock: waits measured on the render clock, so a hidden tab pauses a bit rather than skipping it
  const until = pred => new Promise(res => {
    if (aborted || pred()) return res();
    waits.push({pred, res});
  });
  const after = secs => { const at = clock + secs; return until(() => clock >= at); };

  const open = () => {
    if (layer) return;
    layer = document.createElement("div");
    layer.className = "pals-stage";
    layer.setAttribute("aria-hidden", "true");
    renderer = new T.WebGLRenderer({alpha: true, antialias: true, powerPreference: "low-power"});
    renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 1.5));
    renderer.outputColorSpace = T.SRGBColorSpace;
    renderer.toneMapping = T.NoToneMapping;
    renderer.setClearColor(0x000000, 0);
    renderer.localClippingEnabled = true;
    layer.appendChild(renderer.domElement);
    svgLayer = document.createElementNS(NS, "svg");
    svgLayer.setAttribute("style", "position:absolute;left:0;top:0;width:100%;height:100%;overflow:visible;" +
                          "pointer-events:none");
    layer.appendChild(svgLayer);
    document.body.appendChild(layer);
    scene = new T.Scene();
    const pmrem = new T.PMREMGenerator(renderer);
    scene.environment = pmrem.fromScene(new T.RoomEnvironment(), 0.04).texture;
    scene.environmentIntensity = 0.7;
    pmrem.dispose();
    // The banner's three lights (archie.js start()), by direction: key upper left, cool fill right, warm rim
    // behind. Directional, so the scene's pixel units don't matter to them.
    for (const [x, y, z, i, c] of [[-2.2, 3, 3, 2.6, 0xfff2e0], [2.8, 1.4, 2.2, 0.7, 0xbfd1ff],
                                   [0.6, 2.8, -3, 2.4, 0xffbf66]]) {
      const l = new T.DirectionalLight(c, i);
      l.position.set(x, y, z);
      scene.add(l);
    }
    camera = new T.OrthographicCamera(0, 1, 0, -1, -4000, 4000);
    camera.position.set(0, 0, 1000);
    size();
    addEventListener("resize", size);
    then = performance.now();
    raf = requestAnimationFrame(frame);
  };
  const size = () => {
    W = document.documentElement.clientWidth;
    H = innerHeight;
    renderer.setSize(W, H, false);
    renderer.domElement.style.cssText = `width:${W}px;height:${H}px`;
    camera.left = 0; camera.right = W; camera.top = 0; camera.bottom = -H;
    camera.updateProjectionMatrix();
  };
  const close = () => {
    cancelAnimationFrame(raf);
    raf = 0;
    removeEventListener("resize", size);
    for (const a of Object.values(actors)) { a.bubble.remove(); scene && scene.remove(a.root); }
    if (renderer) { renderer.dispose(); renderer.forceContextLoss(); }
    if (layer) layer.remove();
    layer = renderer = scene = camera = null;
  };
  // Capture mode (for recording a bit frame by frame, art/pals/README.md): the window's own frames do
  // nothing and `step(dt)` advances the stage instead, so a recording is the same however slowly it is
  // taken.
  let manual = false, pending = 0, stepped = [];
  const frame = now => {
    raf = requestAnimationFrame(frame);
    const dt = Math.min(0.1, (now - then) / 1000);
    then = now;
    if (manual) {
      // a step asked for is taken inside a frame, so the compositor shows what it drew
      if (pending) { advance(pending); pending = 0; for (const r of stepped.splice(0)) r(); }
      return;
    }
    if (document.hidden) return;
    advance(dt);
  };
  const advance = dt => {
    clock += dt;
    for (const m of mixers) m.update(dt);
    for (const f of [...tickers]) f(dt);
    for (let i = waits.length - 1; i >= 0; i--) {
      if (aborted || waits[i].pred()) { const w = waits[i]; waits.splice(i, 1); w.res(); }
    }
    for (const a of Object.values(actors)) a.place();
    for (const a of attachments) a.update();
    if (renderer) renderer.render(scene, camera);
  };

  // ---- the cast --------------------------------------------------------------------------------------
  const v3 = new T.Vector3();
  class Actor {
    constructor(name, gltf, spec) {
      this.name = name;
      this.spec = spec;
      this.root = new T.Group();                     // where on the page: x across, y down (negated)
      this.turn = new T.Group();                     // which way he faces: 0 the reader, +-1 screen right/left
      this.root.add(this.turn);
      this.turn.add(gltf.scene);
      this.model = gltf.scene;
      this.mixer = new T.AnimationMixer(gltf.scene);
      this.clips = {};
      for (const c of gltf.animations) this.clips[c.name] = c;
      this.x = 0; this.y = 0; this.ppm = PPM; this.facing = 0; this.turnTo = 0; this.current = null;
      this.done = null;
      this.mixer.addEventListener("finished", e => {
        if (e.action !== this.current) return;
        const d = this.done; this.done = null; d && d();
      });
      this.bubble = document.createElement("p");
      this.bubble.className = "pals-say";
      this.bones = {};
      gltf.scene.traverse(n => { if (n.isBone || n.type === "Object3D" || n.isGroup) this.bones[n.name] = n; });
    }
    add(clips) { for (const c of clips) this.clips[c.name] = c; }
    at(x, y, ppm = this.ppm) { this.x = x; this.y = y; this.ppm = ppm; this.place(); return this; }
    place() {
      this.root.position.set(this.x, -this.y, 0);
      this.root.scale.setScalar(this.ppm);
      // turn, eased: a quarter turn in about a fifth of a second
      const d = this.turnTo - this.turn.rotation.y;
      this.turn.rotation.y += Math.abs(d) < 0.01 ? d : d * 0.25;
      if (this.bubble.classList.contains("on")) {
        const h = this.headAt();
        this.bubble.style.left = h.x + "px";
        this.bubble.style.top = (h.y - 10) + "px";
      }
    }
    // Facing: 0 the reader, 1 screen right, -1 screen left, or any angle in radians with `rad`.
    face(dir, rad) { this.facing = dir; this.turnTo = rad !== undefined ? rad : dir * Math.PI / 2; return until(() => Math.abs(this.turn.rotation.y - this.turnTo) < 0.02); }
    has(name) { return !!this.clips[name]; }
    play(name, {loop = false, reps = 1, fade = 0.2, speed = 1, clamp = true} = {}) {
      const clip = this.clips[name];
      if (!clip) { console.warn(`pals: ${this.name} has no clip ${name}`); return null; }
      const a = this.mixer.clipAction(clip);
      a.reset();
      a.timeScale = speed;
      a.setLoop(loop ? T.LoopRepeat : reps > 1 ? T.LoopRepeat : T.LoopOnce, loop ? Infinity : reps);
      a.clampWhenFinished = clamp;
      if (this.current && this.current !== a) a.crossFadeFrom(this.current, fade, false);
      a.play();
      this.current = a;
      return a;
    }
    // Play a clip through and resolve at its end (or at once, cut short, if the bit is stopped).
    perform(name, opts = {}) {
      return new Promise(res => {
        if (aborted || !this.play(name, opts)) return res();
        this.done = res;
        waits.push({pred: () => aborted, res});
      });
    }
    // Walk to x (CSS px) along the ground he is on, at the speed his walk clip was made for.
    async walkTo(x, {speed = 1, clip} = {}) {
      const dir = Math.sign(x - this.x);
      if (!dir) return;
      await this.face(dir);
      const c = clip || this.spec.walk;
      this.play(c, {loop: true, speed});
      const v = this.spec.speed * speed;              // metres a second
      const tick = dt => { this.x += dir * v * this.ppm * dt; if (dir * (x - this.x) <= 0) this.x = x; };
      tickers.add(tick);
      await until(() => this.x === x);
      tickers.delete(tick);
    }
    // Seconds into the clip he is playing.
    time() { return this.current ? this.current.time : 0; }
    // Hide everything of him right of page x (CSS px): walking through a doorway. `null` to stop.
    clipRight(x) {
      const planes = x === null ? [] : [new T.Plane(new T.Vector3(-1, 0, 0), x)];
      this.model.traverse(n => {
        if (!n.isMesh) return;
        for (const m of Array.isArray(n.material) ? n.material : [n.material]) {
          m.clippingPlanes = planes;
          m.needsUpdate = true;
        }
      });
    }
    bone(name) { return this.bones[name] || null; }
    // Where a bone is on the page, in CSS px (x across, y down).
    pageAt(name) {
      const b = this.bone(name);
      if (!b) return {x: this.x, y: this.y};
      b.getWorldPosition(v3);
      return {x: v3.x, y: -v3.y};
    }
    headAt() {
      const p = this.pageAt("head");
      return {x: p.x, y: p.y - this.ppm * 0.62};
    }
    say(text, secs) {
      this.bubble.textContent = text;
      layer.appendChild(this.bubble);
      this.bubble.classList.add("on");
      this.place();
      const s = secs || Math.min(5, 1.6 + text.length * 0.05);
      return after(s).then(() => this.bubble.classList.remove("on"));
    }
    hush() { this.bubble.classList.remove("on"); }
    show(on) { this.root.visible = on; }
  }

  const load = async name => {
    if (actors[name]) return actors[name];
    const spec = CAST[name];
    const g = await fetchGLB(spec.glb);
    const a = new Actor(name, g, spec);
    for (const f of spec.extra || []) {
      try { a.add((await fetchGLB(f)).animations); } catch (e) { console.warn(`pals: ${f}`, e); }
    }
    actors[name] = a;
    return a;
  };

  // ---- props -----------------------------------------------------------------------------------------
  class Prop {
    constructor(name, gltf) {
      this.name = name;
      this.root = new T.Group();
      this.model = gltf.scene;
      this.root.add(this.model);
      this.mixer = new T.AnimationMixer(gltf.scene);
      this.clips = Object.fromEntries(gltf.animations.map(c => [c.name, c]));
      mixers.add(this.mixer);
      this.holder = null;
    }
    // On the page at (x, y) CSS px, `ppm` px to the metre (default: the cast's).
    at(x, y, ppm = PPM) { this.detach(); scene.add(this.root); this.root.position.set(x, -y, 0); this.root.scale.setScalar(ppm); return this; }
    // In a pal's hand (or on any of his bones), at the bone's own origin.
    hold(actor, bone = "grip_R", offset = [0, 0, 0], rot = [0, 0, 0]) {
      const b = actor.bone(bone);
      if (!b) return this;
      this.detach();
      b.add(this.root);
      this.root.position.set(...offset);
      this.root.rotation.set(...rot);
      this.root.scale.setScalar(1);
      this.holder = b;
      return this;
    }
    detach() { if (this.root.parent) this.root.parent.remove(this.root); this.holder = null; }
    play(name, opts = {}) {
      const c = this.clips[name];
      if (!c) return null;
      const a = this.mixer.clipAction(c);
      a.reset();
      a.setLoop(opts.loop ? T.LoopRepeat : T.LoopOnce, opts.loop ? Infinity : 1);
      a.clampWhenFinished = true;
      a.play();
      return a;
    }
    remove() { this.detach(); mixers.delete(this.mixer); }
  }
  const prop = async name => new Prop(name, await fetchGLB(`pals/props/${name}.glb`));

  // ---- the page, borrowed and given back -------------------------------------------------------------
  const undos = [];
  const root = document.documentElement;
  const stored = k => { try { return localStorage.getItem(k); } catch { return null; } };
  const page = {
    rect: q => { const e = typeof q === "string" ? document.querySelector(q) : q; return e ? e.getBoundingClientRect() : null; },
    // The theme flipped `n` times, 400 ms apart (1.25 flashes a second), and back unless the reader chose
    // one meanwhile -- the lights prank's rule (archie.js pranks()).
    async flicker(n = 4, ms = 400) {
      const theme = root.dataset.theme, saved = stored("theme");
      const undo = () => { if (stored("theme") === saved) root.dataset.theme = theme; };
      undos.push(undo);
      for (let i = 0; i < n && stored("theme") === saved && !aborted; i++) {
        root.dataset.theme = root.dataset.theme === "light" ? "dark" : "light";
        await after(ms / 1000);
      }
      undo();
    },
    undo: fn => undos.push(fn),
  };

  // ---- drawing over the cast: lines a pal draws, doors, signs -------------------------------------------
  const svgEl = (tag, attrs = {}) => {
    const e = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
    return e;
  };
  const tick = f => { tickers.add(f); return () => tickers.delete(f); };
  const fading = (el, secs) => {
    const at = clock;
    const off = tick(() => {
      const u = Math.min(1, (clock - at) / secs);
      el.setAttribute("opacity", String(1 - u));
      if (u >= 1) { off(); el.remove(); }
    });
    return after(secs);
  };
  const svg = {
    // A stroke that grows as points are added: what a marker leaves behind.
    path({stroke = "#1b1b1f", width = 4} = {}) {
      const el = svgEl("path", {fill: "none", stroke, "stroke-width": width, "stroke-linecap": "round",
                                "stroke-linejoin": "round"});
      svgLayer.appendChild(el);
      const pts = [];
      return {
        el,
        add(p) {
          const last = pts[pts.length - 1];
          if (last && Math.hypot(p.x - last.x, p.y - last.y) < 1.5) return;
          pts.push({x: p.x, y: p.y});
          el.setAttribute("d", "M" + pts.map(q => `${q.x.toFixed(1)} ${q.y.toFixed(1)}`).join(" L"));
        },
        box() {
          const xs = pts.map(q => q.x), ys = pts.map(q => q.y);
          const left = Math.min(...xs), right = Math.max(...xs), top = Math.min(...ys), bottom = Math.max(...ys);
          return {left, right, top, bottom, width: right - left, height: bottom - top};
        },
        fade: secs => fading(el, secs),
      };
    },
    // A door drawn into a box: a dark doorway, and a panel over it hinged on its far (right) edge that
    // swings open towards the reader (it narrows to its hinge) and shut again.
    door(b, {fill = "#f2efe8", stroke = "#1b1b1f"} = {}) {
      const g = svgEl("g");
      const hole = svgEl("rect", {x: b.left, y: b.top, width: b.width, height: b.height, fill: "#0d0e12", opacity: 0});
      const panel = svgEl("rect", {x: b.left, y: b.top, width: b.width, height: b.height, fill, stroke,
                                   "stroke-width": 3, opacity: 0});
      const knob = svgEl("circle", {cx: b.left + b.width * 0.16, cy: b.top + b.height * 0.52, r: 4, fill: stroke,
                                    opacity: 0});
      g.append(hole, panel, knob);
      svgLayer.insertBefore(g, svgLayer.firstChild);
      // Swung on the stage's clock rather than by a CSS transition, so a captured frame shows it where it is.
      let k = 1;
      const set = v => {
        k = v;
        const m = `matrix(${v} 0 0 1 ${b.right * (1 - v)} 0)`;   // scaleX about the hinge
        panel.setAttribute("transform", m);
        knob.setAttribute("transform", m);
      };
      const swing = (to, secs) => {
        const from = k, at = clock;
        const off = tick(() => {
          const u = Math.min(1, (clock - at) / secs), e = 1 - Math.pow(1 - u, 3);
          set(from + (to - from) * e);
          if (u >= 1) off();
        });
      };
      return {
        open(secs) {
          for (const e of [hole, panel, knob]) e.setAttribute("opacity", 1);
          swing(-0.18, secs);
          return after(secs);
        },
        close(secs) { swing(1, secs); return after(secs); },
        fade: secs => fading(g, secs),
        el: g,
      };
    },
    clear() { while (svgLayer && svgLayer.firstChild) svgLayer.firstChild.remove(); },
  };

  // ---- the Atlas Core's projection ---------------------------------------------------------------------
  // The world the Core shows (art/pals/worlds.py), drawn on this stage at a size the reader can read --
  // the Core itself is a few pixels across in the banner -- floating over wherever the Core is on the page,
  // with a beam of light down to it. archie-core.js calls `project(name)` when the Core opens and moves the
  // handle every frame; the projection never runs during a bit, and a bit ends it.
  const holoMats = root => root.traverse(m => {
    if (!m.isMesh) return;
    const swap = mat => {
      if (!mat || !/^holo/i.test(mat.name)) return mat;
      const c = mat.emissive && mat.emissive.getHex() ? mat.emissive.clone() : mat.color.clone();
      return new T.MeshBasicMaterial({color: c, transparent: true, opacity: 0.85, blending: T.AdditiveBlending,
                                      depthWrite: false, side: T.DoubleSide, name: mat.name});
    };
    m.material = Array.isArray(m.material) ? m.material.map(swap) : swap(m.material);
  });
  let projection = null;
  async function project(name, inBit = false) {
    if (running && !inBit) return null;
    let g;
    try { g = await fetchGLB(`pals/worlds/${name}.glb`); }
    catch { if (name === "home") return null; return project("home", inBit); }
    if (running && !inBit) return null;
    open();
    const root = new T.Group(), tilt = new T.Group();
    root.add(tilt);
    tilt.add(g.scene);
    tilt.rotation.x = 0.42;                          // seen from a little above, as on the sheet
    holoMats(g.scene);
    scene.add(root);
    const mixer = new T.AnimationMixer(g.scene);
    mixers.add(mixer);
    const clips = Object.fromEntries(g.animations.map(c => [c.name, c]));
    // A world is shared by every projection of it (one GLB, cached), so a projection takes the scene for
    // its length and hands it back.
    const play = (c, loop) => {
      if (!clips[c]) return;
      mixer.stopAllAction();
      const a = mixer.clipAction(clips[c]);
      a.reset().setLoop(loop ? T.LoopRepeat : T.LoopOnce, loop ? Infinity : 1);
      a.clampWhenFinished = true;
      a.play();
    };
    const beam = svgEl("polygon", {fill: "url(#pals-beam)", opacity: "0.55"});
    if (!svgLayer.querySelector("#pals-beam")) {
      const defs = svgEl("defs");
      const grad = svgEl("linearGradient", {id: "pals-beam", x1: "0", y1: "1", x2: "0", y2: "0"});
      grad.append(svgEl("stop", {offset: "0", "stop-color": "#2fe3f1", "stop-opacity": "0.75"}),
                  svgEl("stop", {offset: "1", "stop-color": "#2fe3f1", "stop-opacity": "0"}));
      defs.append(grad);
      svgLayer.prepend(defs);
    }
    svgLayer.appendChild(beam);
    play("appear");
    let born = clock, k = 0, gone = false, last = null;
    // Up and out to one side of the Core (the hand's side, `side`, unless the window's edge is too close),
    // so the beam and the world clear his face; the beam runs from the Core to the world's disc.
    const draw = () => {
      if (!last) return;
      const [x, y, size, want] = last, r = size / 2;
      const side = want > 0 ? (x + r * 2.5 < W - 8 ? 1 : -1) : (x - r * 2.5 > 8 ? -1 : 1);
      // kept on screen: beside his head, if there is no room above it
      const cx = x + side * r * 1.35 * k, cy = Math.max(r * 1.3 + 6, y - r * 1.1 * k);
      root.position.set(cx, -cy, 0);
      root.scale.setScalar(Math.max(1e-4, r * k));
      const dx = r * 0.85 * k, dy = r * 0.32 * k;
      beam.setAttribute("points", `${x - 2},${y} ${x + 2},${y} ${cx + dx},${cy + dy} ${cx - dx},${cy + dy}`);
    };
    const grow = tick(() => { if (!gone) k = 1 - Math.pow(1 - Math.min(1, (clock - born) / 0.5), 3); draw(); });
    const h = {
      root, world: g.scene, play,
      // the Core's point on the page, the world's width there (CSS px), and the side of him it is held on
      // (+1 screen right); called every frame
      at(x, y, size, side = 1) { last = [x, y, size, side]; },
      idle() { play("idle", true); },
      async hide(secs = 0.3) {
        if (gone) return;
        gone = true;
        const from = k, t0 = clock;
        await until(() => { k = from * Math.max(0, 1 - (clock - t0) / secs); return clock - t0 >= secs; });
        grow();
        if (scene) scene.remove(root);
        mixers.delete(mixer);
        beam.remove();
        projection = null;
        if (!running) close();
      },
      // straight onto the page at (x, y) and a width, with no beam: a world that has left the Core
      free(x, y, size) { last = null; beam.remove(); root.position.set(x, -y, 0); root.scale.setScalar(size / 2); k = 1; },
    };
    projection = h;
    return h;
  }

  // ---- tools for a bit: any of the pals' files, glow, things that ride on a pal --------------------------
  const glb = path => fetchGLB(path);                 // assets-relative ("pals/core.glb"), cached
  const attachments = new Set();
  const av = new T.Vector3(), aq = new T.Quaternion(), mq = new T.Quaternion();
  // Keep `obj` on `actor`'s `bone` every frame: at the bone (plus `offset`, metres, in the bone's own frame),
  // and either turned with it, or `upright` (turned only as the pal faces). Returns its remover.
  const attach = (obj, actor, bone, {offset = [0, 0, 0], upright = true} = {}) => {
    const b = actor.bone(bone);
    if (!b) return () => {};
    if (obj.parent !== actor.model) actor.model.add(obj);
    const off = new T.Vector3(...offset);
    const a = {obj, update() {
      b.updateWorldMatrix(true, false);
      av.copy(off).applyMatrix4(b.matrixWorld);
      actor.model.worldToLocal(av);
      obj.position.copy(av);
      if (upright) obj.quaternion.identity();
      else {
        b.getWorldQuaternion(aq);
        actor.model.getWorldQuaternion(mq);
        obj.quaternion.copy(mq.invert().multiply(aq));     // the bone's turn, in the model's own frame
      }
    }};
    attachments.add(a);
    a.update();
    return () => attachments.delete(a);
  };

  // ---- running a bit ---------------------------------------------------------------------------------
  const stop = () => { aborted = true; };
  const onKey = e => { if (e.key === "Escape" || e.key === "Tab") stop(); };
  const onClick = () => stop();
  const onHide = () => { if (document.hidden) stop(); };

  async function run(bit, ctx = {}) {
    if (running) return false;
    if (projection) await projection.hide(0.15);
    running = bit.name;
    aborted = false;
    open();
    addEventListener("pointerdown", onClick, true);
    addEventListener("keydown", onKey, true);
    document.addEventListener("visibilitychange", onHide);
    const cast = {};
    try {
      for (const n of bit.cast) {
        const a = await load(n);
        a.ppm = bit.ppm || PPM;
        // its clips for this bit: `packs` if the bit names them, else pals/bits/<bit>@<pal>.glb (a pal with
        // no pieces of his own in a bit has no file, which is fine: he plays his everyday clips)
        const pack = bit.packs ? bit.packs[n] : `pals/bits/${bit.name}@${n}.glb`;
        for (const f of pack ? [pack] : []) {
          try { a.add((await fetchGLB(f)).animations); } catch (e) { console.warn(`pals: ${f}`, e); }
        }
        mixers.add(a.mixer);
        scene.add(a.root);
        a.show(false);
        cast[n] = a;
      }
      const s = {cast, ...cast, after, until, page, prop, svg, glb, attach, holo: holoMats,
                 project: name => project(name, true), add: o => scene.add(o),
                 mixer: root => { const m = new T.AnimationMixer(root); mixers.add(m); return m; },
                 W: () => W, H: () => H, clock: () => clock,
                 get alive() { return !aborted; }, tick,
                 ctx, scene, T};
      await bit.play(s);
    } catch (e) {
      console.warn(`pals: ${bit.name} stopped:`, e);
    } finally {
      for (const u of undos.splice(0).reverse()) { try { u(); } catch {} }
      for (const a of Object.values(cast)) {
        a.hush(); a.mixer.stopAllAction(); mixers.delete(a.mixer); a.current = null; a.clipRight(null);
      }
      svg.clear();
      tickers.clear();
      attachments.clear();
      if (projection) { const pj = projection; projection = null; try { pj.root.removeFromParent(); } catch {} }
      removeEventListener("pointerdown", onClick, true);
      removeEventListener("keydown", onKey, true);
      document.removeEventListener("visibilitychange", onHide);
      close();
      running = null;
    }
    return !aborted;
  }

  // Whether a bit could start now: its page, and its own `ready()` against the page as it is.
  const can = (bit, here = where()) => !running && (!bit.pages || bit.pages.includes(here.page)) &&
    (!bit.ready || !!bit.ready({page}));

  // What is on, for the admin panel and the browser checks (window.archieStage, set by archie.js).
  const status = () => ({bit: running, clock: +clock.toFixed(2), aborted,
    cast: Object.fromEntries(Object.values(actors).filter(a => a.root.parent).map(a => [a.name, {
      x: Math.round(a.x), y: Math.round(a.y), facing: a.facing,
      clip: a.current ? a.current.getClip().name : null, t: a.current ? +a.current.time.toFixed(2) : 0}]))});

  const capture = on => { manual = !!on; };
  const step = dt => new Promise(res => {
    if (!manual || !layer) return res();
    pending += dt;
    stepped.push(res);
  });

  return {run, stop, can, load, where, status, capture, step, project,
          get busy() { return !!running; }, get playing() { return running; }};
}
