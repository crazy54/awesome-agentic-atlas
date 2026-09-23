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
// `watch`, `sit`, `sleep`, four dances (`floss`, `take-the-l`, `default-dance`, `orange-justice`) and
// `walk`, a stride in place. Every clip but `walk` starts and ends on the idle's first pose. The director
// below idles for a few loops, then does one act -- a dance under moving-head lights, one of the others,
// or a walk off the edge of the page and a moonwalk back in -- and idles again.
//
// THE CANVAS IS WIDER THAN THE SLOT. It spans the viewport's width and the header's height, so that he can
// walk out of the banner and so that the lights have somewhere to come from. The camera is the one the poster
// is rendered with: Blender's (0.9, -6.2, 1.55) aimed at z 1.08, a 70 mm lens on a 36 mm sensor, converted to
// glTF's Y-up. `layout()` gives it an off-centre frustum whose slot-sized window is exactly the poster's
// frame, so at rest he stands in the same pixels the poster did and the swap between them does not jump. If
// you move the camera here, move it in `stage()` too. The canvas takes no pointer events, so the header's
// links work through it.
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
  const DANCES = ["floss", "take-the-l", "default-dance", "orange-justice"];
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
    const edge = {left: -8, right: 8, top: 5};
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
      const cx = s.left + s.width / 2, cy = s.top - top + s.height / 2;
      const k = camera.near * Math.tan(FOV / 2) / (s.height / 2);   // near-plane metres per CSS pixel
      camera.projectionMatrix.makePerspective(-cx * k, (W - cx) * k, cy * k, -(H - cy) * k,
                                              camera.near, camera.far);
      camera.projectionMatrixInverse.copy(camera.projectionMatrix).invert();
      const feet = s.top - top + s.height * 0.84;
      edge.left = worldAt(0, feet, W, H, 0).x;
      edge.right = worldAt(W, feet, W, H, 0).x;
      edge.top = worldAt(cx, 0, W, H, -1.5).y;
      rig.place(edge);
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
    const walkOff = async () => {
      if (Math.random() < 0.5) await perform("watch");   // late for something
      await turn(Math.PI / 2);                           // face screen right
      play("walk", Infinity);
      speed = WALK_SPEED;
      await until(() => actor.position.x > edge.right + 1.2);
      speed = 0;
      actor.visible = false;
      await after(1.5 + Math.random() * 2);
      // Back in from the other side, facing the way he left and gliding backwards: the reversed walk.
      actor.position.x = edge.left - 1.2;
      actor.rotation.y = turnTo = -Math.PI / 2;
      actor.visible = true;
      play("walk", Infinity).timeScale = -1;
      speed = WALK_SPEED;
      await until(() => actor.position.x >= 0);
      speed = 0;
      actor.position.x = 0;
      play("idle", 1);
      await turn(0);
    };
    let last = "";
    const act = async name => {
      last = name;
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
        await perform("idle", 2 + Math.floor(Math.random() * 2));
        // A dance half the time, and never the same act twice running.
        const pool = (Math.random() < 0.5 ? DANCES : OTHERS).filter(n => n !== last);
        await act(pool[Math.floor(Math.random() * pool.length)]);
      }
    };

    // ---- The loop: only ticks while someone can see it, the tab showing and the masthead on screen -----
    let seen = true, raf = 0, then = 0;
    const tick = dt => {
      clock += dt;
      for (let i = waits.length - 1; i >= 0; i--) if (waits[i].pred()) waits.splice(i, 1)[0].res();
      actor.position.x += speed * dt;
      const dr = turnTo - actor.rotation.y;
      actor.rotation.y += Math.sign(dr) * Math.min(Math.abs(dr), 5 * dt);
      mixer.update(dt);
      rig.update(dt, clock, actor.position.x);
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
      canvas.remove();
      slot.style.backgroundImage = "";
      renderer.dispose();
      started = false;
    };
  }

  // Moving-head fixtures, the kind an EDM stage hangs from its truss: four heads just above the top of the
  // header, each a soft cone of coloured light plus a spotlight that actually colours him, sweeping in
  // crossing figures of eight. Out of sight except during a dance, when they fade up over half a second. The
  // colours drift from one to the next; nothing flashes.
  function lights(T, scene) {
    const group = new T.Group();
    group.visible = false;
    scene.add(group);
    const PALETTE = [0xff2bd6, 0x22e1ff, 0x8a5bff, 0xffb000];
    const L = 10;
    const geo = new T.CylinderGeometry(0.03, 0.7, L, 40, 1, true);
    geo.translate(0, -L / 2, 0);
    geo.rotateX(-Math.PI / 2);                          // apex at the origin, pointing down +Z for lookAt()
    const heads = [0, 1, 2, 3].map(i => {
      const mat = new T.ShaderMaterial({
        uniforms: {color: {value: new T.Color(PALETTE[i])}, level: {value: 0}},
        vertexShader: `varying vec2 vUv; varying vec3 vN, vV;
          void main() { vUv = uv; vN = normalize(normalMatrix * normal);
            vec4 mv = modelViewMatrix * vec4(position, 1.0); vV = normalize(-mv.xyz);
            gl_Position = projectionMatrix * mv; }`,
        // Brightest down the middle of the cone and at the fixture, falling to nothing at the edges and the
        // far end, which is what makes a transparent cone read as a beam in haze.
        fragmentShader: `uniform vec3 color; uniform float level; varying vec2 vUv; varying vec3 vN, vV;
          void main() { float core = pow(abs(dot(vN, vV)), 2.0);
            float along = pow(vUv.y, 1.6);
            gl_FragColor = vec4(color * core * along * level * 0.6, 0.0); }`,
        // Colour added, alpha left alone. The canvas is transparent and premultiplied, so a beam that wrote
        // alpha would be an opaque dark cone over the page; with alpha 0 its colour adds to whatever the
        // page shows behind it, which is what light does.
        transparent: true, depthWrite: false, side: T.DoubleSide, blending: T.CustomBlending,
        blendSrc: T.OneFactor, blendDst: T.OneFactor, blendSrcAlpha: T.ZeroFactor, blendDstAlpha: T.OneFactor,
      });
      const beam = new T.Mesh(geo, mat);
      // The spotlights stay in the scene at zero rather than being hidden with the beams: three.js compiles
      // its shaders for the number of lights, so adding four at the first dance would stall that frame.
      const spot = new T.SpotLight(PALETTE[i], 0, 0, 0.16, 0.6, 0);
      group.add(beam);
      scene.add(spot, spot.target);
      return {beam, spot, mat, x: 0};
    });
    const aim = new T.Vector3();
    const from = new T.Color(), to = new T.Color();
    let level = 0;
    return {
      on: false,
      place(edge) {
        const span = Math.min(5, (edge.right - edge.left) / 2.5);
        heads.forEach((h, i) => {
          h.x = (i - 1.5) / 1.5 * span;
          h.beam.position.set(h.x, edge.top + 0.6, -1.5);
          h.spot.position.copy(h.beam.position);
        });
      },
      update(dt, t, cx) {
        level = Math.max(0, Math.min(1, level + (this.on ? 2 : -2) * dt));
        group.visible = level > 0;
        if (!group.visible) { for (const h of heads) h.spot.intensity = 0; return; }
        const phase = (t / 2.4) % PALETTE.length;
        heads.forEach((h, i) => {
          const s = i % 2 ? -1 : 1;
          aim.set(cx + 1.6 * Math.sin(t * 1.3 + i * 1.7) * s, 0.2 + 0.9 * Math.abs(Math.sin(t * 0.9 + i)),
                  0.9 * Math.sin(t * 2.6 + i * 0.8));
          h.beam.lookAt(aim);
          h.beam.scale.set(1, 1, h.beam.position.distanceTo(aim) * 1.25 / L);
          h.spot.target.position.copy(aim);
          const k = Math.floor(phase + i) % PALETTE.length, f = (phase + i) % 1;
          from.set(PALETTE[k]);
          to.set(PALETTE[(k + 1) % PALETTE.length]);
          h.mat.uniforms.color.value.copy(from).lerp(to, f);
          h.spot.color.copy(h.mat.uniforms.color.value);
          h.mat.uniforms.level.value = level;
          h.spot.intensity = 6 * level;
        });
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
