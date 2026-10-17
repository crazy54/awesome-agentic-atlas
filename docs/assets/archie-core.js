// The Atlas Core: the ball in Archie's belly that unfolds into a stage for a miniature world, and the world
// it shows is the page the reader is on (archie-stage.js `where()`): the whole atlas on the index, a topic's
// world on that topic's pages and on its projects' pages, the catalogue's filtered topic, Discover's
// carousel of picks, the collections' shelf, and a lost little island on the 404 page. Imported by archie.js,
// which calls `tick()` every frame and `show()` for the `core` act.
//
// The Core is art/pals/core.py (assets/pals/core.glb), the worlds art/pals/worlds.py (assets/pals/worlds/
// <slug>.glb). The Core is not parented to a bone: each frame it is put where its bone is -- his `core`
// bone, docked, or his left hand's `grip_L`, held -- but kept upright and facing the way he does. The world
// is not drawn here at all: the Core is a few pixels across in the banner and fewer in the corner dock, so
// the world is projected -- drawn on the pals' stage (archie-stage.js `project()`) at a size the reader can
// read, floating over wherever the Core is on the page, a beam of light down to it.
//
// Glow is drawn additively: every material whose name starts `holo` (the Core's lights, the worlds'
// holograms) is swapped for an unlit one that adds its colour, so it reads as light on any page colour.
//
// The `core-show` clip (art/pals/clips/archie_base.py) says when the hand-offs happen: CORE below.
const CORE = {grab: 0.62, unfold: 1.35, fold: 6.05, dock: 7.5};   // archie_base.py CORE_GRAB .. CORE_DOCK
const ABOVE = 0.07;          // the beam's foot: this far above the ball's centre, metres
const DOCK_OUT = 0.018;      // the ball's centre ahead of his `core` bone, docked
const PALM = 0.085;          // ... and above `grip_L`, along the palm's normal, held

export function atlas(o) {
  const {T, V, base, loader, model, where, project, toPage, size} = o;
  const url = f => new URL(f + V, base).href;
  const grip = model.getObjectByName("grip_L"), dock = model.getObjectByName("core");
  const v = new T.Vector3(), n = new T.Vector3(), sc = new T.Vector3(), q = new T.Quaternion();
  let core = null, held = false, show = null;
  const foot = new T.Vector3();

  const holo = root => root.traverse(m => {
    if (!m.isMesh) return;
    const swap = mat => {
      if (!mat || !/^holo/i.test(mat.name)) return mat;
      const c = mat.emissive && mat.emissive.getHex() ? mat.emissive.clone() : mat.color.clone();
      c.multiplyScalar(Math.min(1.6, Math.max(1, mat.emissiveIntensity || 1)));
      return new T.MeshBasicMaterial({color: c, transparent: true, opacity: mat.opacity < 1 ? mat.opacity : 0.85,
        blending: T.AdditiveBlending, depthWrite: false, side: T.DoubleSide, name: mat.name});
    };
    m.material = Array.isArray(m.material) ? m.material.map(swap) : swap(m.material);
  });
  const rig = g => {
    const mixer = new T.AnimationMixer(g.scene);
    const clips = Object.fromEntries(g.animations.map(c => [c.name, c]));
    const play = (name, loop = false) => {
      const c = clips[name];
      if (!c) return null;
      mixer.stopAllAction();
      const a = mixer.clipAction(c);
      a.reset();
      a.setLoop(loop ? T.LoopRepeat : T.LoopOnce, loop ? Infinity : 1);
      a.clampWhenFinished = true;
      a.play();
      return a;
    };
    return {scene: g.scene, mixer, clips, play};
  };

  const ready = loader.loadAsync(url("pals/core.glb")).then(g => {
    holo(g.scene);
    core = rig(g);
    core.root = new T.Group();
    core.root.add(core.scene);
    core.stage = g.scene.getObjectByName("stage");
    model.add(core.root);
    core.play("closed");
    place();
    return core;
  });

  // Where the ball goes this frame, in his model's own space: upright, facing as he faces.
  function place() {
    if (!core) return;
    const b = held ? grip : dock;
    if (!b) return;
    b.getWorldPosition(v);
    if (held) {
      b.getWorldQuaternion(q);
      n.set(0, 0, 1).applyQuaternion(q);              // the palm's normal
      v.addScaledVector(n, PALM * model.getWorldScale(sc).x);
    }
    model.worldToLocal(v);
    if (!held) v.z += DOCK_OUT;
    core.root.position.copy(v);
    core.root.quaternion.identity();
  }

  // The `core` act's side of the Core, driven by where the `core-show` clip has got to (`t`, seconds).
  async function begin() {
    await ready;
    const here = where();
    show = {stage: 0, here, proj: null};
    return here;
  }
  function follow(t) {
    if (!show || !core) return;
    const s = show;
    if (s.stage === 0 && t >= CORE.grab) { held = true; s.stage = 1; }
    if (s.stage === 1 && t >= CORE.unfold) { core.play("unfold"); s.stage = 2; }
    if (s.stage === 2 && t >= CORE.unfold + 0.9) {
      core.play("open-idle", true);
      s.stage = 3;
      project(s.here.world).then(h => {
        if (!h) return;
        if (show !== s || s.stage > 3) { h.hide(0.05); return; }
        s.proj = h;
        setTimeout(() => s.proj && s.proj.idle(), 800);
      });
    }
    if (s.stage === 3 && t >= CORE.fold - 0.35) { if (s.proj) s.proj.hide(0.35); s.proj = null; s.stage = 4; }
    if (s.stage === 4 && t >= CORE.fold) { core.play("fold"); s.stage = 5; }
    if (s.stage === 5 && t >= CORE.dock) { held = false; s.stage = 6; }
    if (s.proj) {
      core.root.getWorldPosition(foot);
      foot.y += ABOVE * model.getWorldScale(sc).y;
      const p = toPage(foot);
      // which side of his body the Core is on, on the page: his left hand holds it, his left is screen
      // right when he faces the reader
      grip.getWorldPosition(v);
      const c = toPage(model.getWorldPosition(n));
      s.proj.at(p.x, p.y, size(), toPage(v).x >= c.x ? 1 : -1);
    }
  }
  function end() {
    if (show && show.proj) show.proj.hide(0.2);
    if (core) core.play("closed");
    held = false;
    show = null;
  }

  return {
    ready,
    // every frame: the Core's and the world's clips, the act's timeline, and where the ball is
    tick(dt, action) {
      if (!core) return;
      if (show && action && action.getClip().name === "core-show") follow(action.time);
      core.mixer.update(dt);
      place();
    },
    begin, end,
    get world() { return show ? show.here.world : null; },
    get busy() { return !!show; },
  };
}
