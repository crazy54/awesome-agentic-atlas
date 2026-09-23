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
// The model is `art/archie/archie.py`, and it carries five clips: `idle`, a four-second loop with a sway, a
// foot tap and blinks, plus `watch`, `dance`, `sit` and `sleep`. Each of those four starts and ends on the
// idle's first pose. Archie idles for a few loops, plays one of the others (never the same one twice
// running), and goes back to idling.
//
// The camera is the one the poster is rendered with: Blender's (0.9, -6.2, 1.55) aimed at z 1.08, with a
// 70 mm lens on a 36 mm sensor, converted to glTF's Y-up. If you move it here, move it in `stage()` too, or
// the swap from poster to model will jump.
(() => {
  const slot = document.querySelector(".mhmascot");
  if (!slot) return;
  const wide = matchMedia("(min-width: 900px)");
  const calm = matchMedia("(prefers-reduced-motion: no-preference)");
  const allowed = () => wide.matches && calm.matches;
  const webgl = () => {
    try { return !!document.createElement("canvas").getContext("webgl2"); } catch { return false; }
  };

  let started = false;
  const go = () => {
    if (started || !allowed() || !webgl()) return;
    started = true;
    start().catch(() => stop());          // any failure leaves the poster, which is where we began
  };
  let stop = () => {};

  async function start() {
    const T = await import("./three-archie.js");
    const renderer = new T.WebGLRenderer({alpha: true, antialias: true, powerPreference: "low-power"});
    renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 2));
    renderer.outputColorSpace = T.SRGBColorSpace;
    renderer.toneMapping = T.NoToneMapping;   // the poster is Blender's "Standard" view, which is none either
    renderer.setClearColor(0x000000, 0);

    const scene = new T.Scene();
    const pmrem = new T.PMREMGenerator(renderer);
    scene.environment = pmrem.fromScene(new T.RoomEnvironment(), 0.04).texture;
    scene.environmentIntensity = 0.55;
    pmrem.dispose();
    // The poster's three area lights, in glTF's axes: key upper left, cool fill right, warm rim behind.
    for (const [x, y, z, i, c] of [[-2.2, 3, 3, 2.6, 0xfff2e0], [2.8, 1.4, 2.2, 0.8, 0xbfd1ff],
                                   [0.6, 2.8, -3, 2.2, 0xffbf66]]) {
      const l = new T.DirectionalLight(c, i);
      l.position.set(x, y, z);
      scene.add(l);
    }
    const camera = new T.PerspectiveCamera(2 * Math.atan(18 / 70) * 180 / Math.PI, 1, 0.1, 50);
    camera.position.set(0.9, 1.55, 6.2);
    camera.lookAt(0, 1.08, 0);

    const gltf = await new T.GLTFLoader().loadAsync(new URL("archie.glb", import.meta.url).href);
    if (!allowed()) { started = false; return; }   // the reader resized or changed a setting meanwhile
    scene.add(gltf.scene);
    const mixer = new T.AnimationMixer(gltf.scene);
    const clip = Object.fromEntries(gltf.animations.map(a => [a.name, a]));
    const extras = ["watch", "dance", "sit", "sleep"].filter(n => clip[n]);
    let last = "";
    let current = null;
    const play = (name, reps) => {
      const a = mixer.clipAction(clip[name]);
      a.reset();
      a.setLoop(reps > 1 ? T.LoopRepeat : T.LoopOnce, reps);
      a.clampWhenFinished = true;
      if (current && current !== a) a.crossFadeFrom(current, 0.2, false);
      a.play();
      current = a;
    };
    const next = () => {
      if (current === mixer.existingAction(clip.idle) && extras.length) {
        const pick = extras.filter(n => n !== last);
        last = pick[Math.floor(Math.random() * pick.length)];
        play(last, 1);
      } else {
        play("idle", 2 + Math.floor(Math.random() * 3));
      }
    };
    mixer.addEventListener("finished", next);
    play("idle", 2);

    const canvas = renderer.domElement;
    canvas.style.cssText = "position:absolute;inset:0;width:100%;height:100%";
    renderer.setSize(240, 240, false);
    const fit = () => {
      const w = slot.clientWidth || 240, h = slot.clientHeight || 240;
      renderer.setSize(w, h, false);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
    };

    // Only ticks while someone can see it: the tab is showing and the masthead is on screen.
    const timer = new T.Timer();
    let seen = true, raf = 0;
    const frame = (now) => {
      raf = requestAnimationFrame(frame);
      timer.update(now);
      mixer.update(Math.min(timer.getDelta(), 0.1));
      renderer.render(scene, camera);
    };
    const run = () => {
      const want = seen && !document.hidden;
      if (want && !raf) { timer.reset(); raf = requestAnimationFrame(frame); }
      if (!want && raf) { cancelAnimationFrame(raf); raf = 0; }
    };
    const io = new IntersectionObserver(([e]) => { seen = e.isIntersecting; run(); });
    io.observe(slot);
    document.addEventListener("visibilitychange", run);

    fit();
    renderer.render(scene, camera);
    slot.appendChild(canvas);
    slot.style.backgroundImage = "none";    // the first frame is up, so the poster can go
    run();

    stop = () => {
      cancelAnimationFrame(raf); raf = 0;
      io.disconnect();
      document.removeEventListener("visibilitychange", run);
      canvas.remove();
      slot.style.backgroundImage = "";
      renderer.dispose();
      started = false;
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
