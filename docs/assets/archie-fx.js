// Archie's stage effects, under and around him while the light show is up: an LED dance floor, dry-ice fog
// that hugs it, haze, CO2 jets, flame projectors and spark fountains. `archie.js` imports this under its own
// `?v=` and calls `effects()` once the scene is built, then `update()` every frame beside the lights.
//
// Everything here is drawn the way the rest of the light show is: through `rig.glow()`/`rig.lit()`, so on
// the dark theme it is light added to the page and on the light theme a coloured haze laid over it, and
// switching theme mid-dance compiles nothing. The floor and the fog follow the lights up and down; the
// cannons fire on cues in the dance's own beats -- CO2 at the half-way beat, flames on the eighth beat of
// every sixteen, sparks over the last four -- or, to the reader's music, on a strong downbeat, no oftener
// than every eight seconds for CO2 and five for flames.
//
// Nothing strobes. The floor's tiles pulse a fifth of their brightness on the beat, a flame's light rises
// and falls over a third of a second, and no effect lights more than a strip of the header at once, so none
// of it comes near three flashes a second or a large bright area (WCAG 2.3.1).
export function effects(T, scene, rig, edge, canvas) {
  const group = new T.Group();
  group.visible = false;
  scene.add(group);
  const hash = n => { const s = Math.sin(n * 12.9898) * 43758.5453; return s - Math.floor(s); };
  const rnd = (a, b) => a + Math.random() * (b - a);
  const mean = new T.Color(), fire = new T.Color(1, 0.45, 0.08);

  // ---- The floor: half-metre LED tiles under him, lit in the heads' colours, fading out with distance ----
  const pal = [0, 1, 2, 3].map(() => new T.Color());
  const floor = new T.Mesh(new T.PlaneGeometry(1, 1).rotateX(-Math.PI / 2), rig.glow(`
      vec2 g = vW.xz / 0.5, id = floor(g), f = fract(g);
      float frame = smoothstep(0.0, 0.07, f.x) * smoothstep(1.0, 0.93, f.x) * smoothstep(0.0, 0.07, f.y)
                  * smoothstep(1.0, 0.93, f.y);
      float b = floor(beat), ph = fract(beat), on;
      if (mode < 0.5) on = step(0.6, hash(vec3(id, b)));                           // scattered
      else if (mode < 1.5) on = step(0.5, fract(length(id + 0.5 - vec2(cx / 0.5, 0.6)) * 0.3 - beat * 0.5)); // ripples
      else on = mod(id.x + id.y + b, 2.0);                                          // checkerboard
      int k = int(mod(id.x * 3.0 + id.y + floor(beat / 4.0), 4.0));
      c = pal[k];
      vec2 d = vW.xz - vec2(cx, -0.4);
      a = frame * (0.12 + 0.88 * on * (0.8 + 0.2 * exp(-5.0 * ph))) * exp(-dot(d, d) / 7.0) * 0.8;`,
    {beat: {value: 0}, mode: {value: 0}, cx: {value: 0}, pal: {value: pal}},
    "uniform float beat, mode, cx; uniform vec3 pal[4];"));
  floor.position.set(0, 0.004, -0.4);
  floor.scale.set(12, 1, 5);
  group.add(floor);

  // ---- Dry-ice fog: sheets standing on the floor, one behind another, dense at the floor and gone by knee
  // height, rolling sideways, and lit by whatever the lights and the flames are doing ----
  const FOG = `float h = max(vW.y, 0.0);
      float n = 0.6 * noise(vec3(vW.x * 0.8 - time * 0.22 * flow, vW.y * 2.2, vW.z * 0.6 + time * 0.07))
              + 0.4 * noise(vec3(vW.x * 2.1 + time * 0.35 * flow, vW.y * 4.5 - time * 0.2, vW.z));
      vec2 d = vec2(vW.x - cx, 0.0);
      a = exp(-h / 0.22) * smoothstep(0.2, 0.75, n) * smoothstep(0.0, 0.25, vUv.x) * smoothstep(1.0, 0.75, vUv.x)
        * exp(-dot(d, d) / 18.0) * 0.9;
      c = mix(vec3(0.72, 0.78, 0.88), color, 0.55);
      if (haze > 0.5) { c = mix(vec3(0.46, 0.5, 0.58), color * 0.7, 0.35); a *= 0.8; }`;
  const fogs = [-2.0, -1.2, -0.45, 0.45].map((z, i) => {
    const m = new T.Mesh(new T.PlaneGeometry(12, 0.8), rig.glow(FOG, {flow: {value: i % 2 ? 1 : -0.7},
                                                                      cx: {value: 0}}, "uniform float flow, cx;"));
    m.position.set(0, 0.4, z);
    group.add(m);
    return m;
  });

  // ---- Haze: a thin veil behind him, the whole height of the header, in the lights' mean colour ----
  const haze = new T.Mesh(new T.PlaneGeometry(1, 1), rig.glow(`
      a = (0.25 + 0.75 * noise(vec3(vW.x * 0.35 + time * 0.05, vW.y * 0.5 - time * 0.03, time * 0.04)))
        * smoothstep(0.0, 0.3, vUv.x) * smoothstep(1.0, 0.7, vUv.x) * smoothstep(0.0, 0.2, vUv.y) * 0.13;`));
  group.add(haze);

  // ---- Particles: CO2, flames and sparks, simulated here and drawn as points ----
  const DEPTH = `uniform float px; attribute float alpha, size; attribute vec3 tint; varying float vA; varying vec3 vC;
      varying vec2 vS; attribute vec2 seed;
      void main() { vA = alpha; vC = tint; vS = seed; vec4 mv = modelViewMatrix * vec4(position, 1.0);
        gl_PointSize = size * px * projectionMatrix[1][1] / -mv.z; gl_Position = projectionMatrix * mv; }`;
  const swarm = (max, frag) => {
    const geo = new T.BufferGeometry();
    const buf = {position: 3, alpha: 1, size: 1, tint: 3, seed: 2};
    const at = {};
    for (const [k, n] of Object.entries(buf)) {
      at[k] = new T.BufferAttribute(new Float32Array(max * n), n);
      geo.setAttribute(k, at[k]);
    }
    for (let i = 0; i < max; i++) at.seed.array.set([Math.random() * 40, Math.random()], i * 2);
    const mat = rig.lit(new T.ShaderMaterial({
      uniforms: {px: {value: 1}, haze: {value: 0}},
      vertexShader: DEPTH,
      fragmentShader: `uniform float haze; varying float vA; varying vec3 vC; varying vec2 vS;
        ${rig.NOISE}
        void main() { vec2 p = gl_PointCoord - 0.5; float r = length(p) * 2.0;
          vec3 c = vC; float a = 0.0;
          ${frag}
          a *= vA;
          gl_FragColor = haze > 0.5 ? vec4(c, min(a * 0.45, 0.8)) : vec4(c * a * 0.6, 0.0); }`,
      transparent: true, depthWrite: false, blending: T.CustomBlending,
    }));
    const pts = new T.Points(geo, mat);
    pts.frustumCulled = false;
    group.add(pts);
    const vel = new Float32Array(max * 3), age = new Float32Array(max), life = new Float32Array(max);
    let live = 0;
    return {
      mat,
      get live() { return live; },
      // `init(i, p, v)` places particle i, returning its life in seconds.
      emit(count, init) {
        for (let i = 0; i < max && count > 0; i++) {
          if (age[i] < life[i]) continue;
          age[i] = 0;
          life[i] = init(at.position.array.subarray(i * 3, i * 3 + 3), vel.subarray(i * 3, i * 3 + 3));
          count--;
        }
      },
      // `step(t, v, dt)` changes velocity for a particle at its life's fraction t, and `look(t, out)`
      // returns its size and alpha and sets its colour.
      update(dt, step, look, tint) {
        live = 0;
        const P = at.position.array, A = at.alpha.array, S = at.size.array, C = at.tint.array;
        for (let i = 0; i < max; i++) {
          if (age[i] >= life[i]) { A[i] = 0; continue; }
          live++;
          age[i] += dt;
          const t = Math.min(1, age[i] / life[i]), v = vel.subarray(i * 3, i * 3 + 3);
          step(t, v, dt);
          P[i * 3] += v[0] * dt; P[i * 3 + 1] += v[1] * dt; P[i * 3 + 2] += v[2] * dt;
          if (P[i * 3 + 1] < 0) { age[i] = life[i]; A[i] = 0; continue; }
          const [s, a] = look(t, tint);
          S[i] = s; A[i] = a;
          C[i * 3] = tint.r; C[i * 3 + 1] = tint.g; C[i * 3 + 2] = tint.b;
        }
        for (const k of ["position", "alpha", "size", "tint"]) at[k].needsUpdate = true;
      },
    };
  };
  // A soft puff, broken up a little so a cloud of them does not read as a pile of discs.
  const co2 = swarm(700, `a = pow(max(0.0, 1.0 - r), 1.6) * (0.55 + 0.45 * noise(vec3(p * 4.0, vS.x)));
      if (haze > 0.5) c = vec3(0.5, 0.55, 0.64);`);
  // A flame's tongue: hot in the middle, and ragged.
  const flames = swarm(600, `a = pow(max(0.0, 1.0 - r), 1.2) * (0.6 + 0.4 * noise(vec3(p * 5.0, vS.x)));
      if (haze > 0.5) c *= 0.85;`);
  const sparks = swarm(500, `a = pow(max(0.0, 1.0 - r), 3.0) * 1.6;`);
  const tint = new T.Color(), white = new T.Color(1, 1, 1);
  const HOT = [new T.Color(1, 0.95, 0.75), new T.Color(1, 0.62, 0.15), new T.Color(0.85, 0.2, 0.03)];
  const flameColour = (t, out) => (t < 0.35 ? out.copy(HOT[0]).lerp(HOT[1], t / 0.35)
                                            : out.copy(HOT[1]).lerp(HOT[2], (t - 0.35) / 0.65));

  // Where the units stand: a CO2 cannon at each end, a flame projector inside each, and a spark gerb
  // either side of him. The units themselves are not drawn -- on a stage they hide behind its lip -- only
  // what comes out of them.
  const at = {co2: [0, 0], flame: [0, 0], gerb: [0, 0]};
  const Z = {co2: -1.7, flame: -1.35, gerb: -0.9};
  const place = () => {
    const span = Math.min(4.5, (edge.right - edge.left) / 2.8);
    at.co2 = [-span * 0.95, span * 0.95];
    at.flame = [-span * 0.62, span * 0.62];
    at.gerb = [-1.1, 1.1];
    haze.position.set(0, edge.top / 2, -1.9);
    haze.scale.set(span * 2.6, edge.top + 0.4, 1);
  };

  // The flames light him, and the floor: a warm light each side that is only ever up while one is burning.
  // Both are in the scene from the start at zero, for the same reason as the spotlights: adding a light
  // later recompiles every material, and stalls that frame.
  const burn = [0, 0];
  const glowL = [0, 1].map(() => { const l = new T.PointLight(0xff8a2a, 0, 0, 0); scene.add(l); return l; });

  // ---- Cues ----------------------------------------------------------------------------------------
  const blast = {co2: [0, 0], flame: [0, 0], gerb: [0, 0]};     // seconds of firing left, each unit
  let lastBeat = -1, lastCo2 = -1e9, lastFlame = -1e9, fog = 0, floorMode = 0;
  const fireCo2 = t => { blast.co2 = [0.75, 0.75]; lastCo2 = t; };
  const fireFlames = (t, side) => {
    lastFlame = t;
    if (side == null) blast.flame = [0.5, 0.5]; else blast.flame[side] = 0.5;
  };
  const cue = (b, beat, t) => {
    if (beat.kick != null) {                                    // to the reader's music
      if (b % 4 || beat.kick < 0.7) return;
      if (t - lastCo2 > 8 && Math.random() < 0.5) fireCo2(t);
      else if (t - lastFlame > 5) fireFlames(t, Math.random() < 0.5 ? null : Math.floor(Math.random() * 2));
      return;
    }
    const n = beat.n;
    if (b === n / 2) fireCo2(t);
    else if (b % 16 === 8) fireFlames(t, b % 32 === 8 ? null : (b / 16) % 2 | 0);
    if (b === n - 4) blast.gerb = [2.2, 2.2];
  };

  return {
    // `beat` is the dance's position in beats, how many it has (`n`) and, to music, the heard onset's
    // strength (`kick`), or null between dances; `level` is how far the lights are up.
    update(dt, t, cx, beat, level) {
      place();
      if (beat) {
        // Every beat crossed since the last frame is cued, so a slow frame that steps over one still fires it.
        const b = Math.floor(beat.at);
        if (lastBeat >= 0) for (let k = lastBeat + 1; k <= b; k++) cue(k, beat, t);
        lastBeat = b;
        floorMode = Math.floor(hash(Math.floor(b / 8) * 7.1 + 0.3) * 3);
      } else lastBeat = -1;
      // The fog rolls in with the lights and lingers a few seconds after them, as dry ice does.
      fog = level > 0 ? Math.min(1, fog + dt / 1.5) : Math.max(0, fog - dt / 5);
      const busy = co2.live + flames.live + sparks.live > 0 || blast.co2.some(Boolean) || blast.flame.some(Boolean)
        || blast.gerb.some(Boolean);
      group.visible = level > 0 || fog > 0 || busy;
      if (!group.visible) { glowL.forEach(l => { l.intensity = 0; }); return; }
      const px = canvas.height / 2;
      for (const s of [co2, flames, sparks]) s.mat.uniforms.px.value = px;

      mean.setRGB(0, 0, 0);
      rig.heads.forEach((h, i) => { pal[i].copy(h.color); mean.r += h.color.r / 4; mean.g += h.color.g / 4; mean.b += h.color.b / 4; });
      const flare = Math.max(burn[0], burn[1]);
      const fu = floor.material.uniforms;
      fu.level.value = level;
      fu.cx.value = cx;
      fu.mode.value = floorMode;
      if (beat) fu.beat.value = beat.at;
      for (const f of fogs) {
        f.material.uniforms.level.value = fog * 1.6;
        f.material.uniforms.cx.value = cx;
        f.material.uniforms.color.value.copy(mean).lerp(fire, flare * 0.7);
      }
      haze.material.uniforms.level.value = Math.max(level, flare * 0.6);
      haze.material.uniforms.color.value.copy(mean).lerp(fire, flare * 0.6);

      // Firing
      for (let i = 0; i < 2; i++) {
        if (blast.co2[i] > 0) {
          blast.co2[i] = Math.max(0, blast.co2[i] - dt);
          const x = at.co2[i];
          co2.emit(Math.ceil(520 * dt), (p, v) => {
            p[0] = x + rnd(-0.05, 0.05); p[1] = 0.3; p[2] = Z.co2 + rnd(-0.05, 0.05);
            v[0] = rnd(-0.5, 0.5) - Math.sign(x) * 0.4; v[1] = rnd(6.5, 9); v[2] = rnd(-0.4, 0.6);
            return rnd(1.3, 2.1);
          });
        }
        if (blast.flame[i] > 0) {
          blast.flame[i] = Math.max(0, blast.flame[i] - dt);
          const x = at.flame[i];
          flames.emit(Math.ceil(600 * dt), (p, v) => {
            p[0] = x + rnd(-0.06, 0.06); p[1] = 0.17; p[2] = Z.flame + rnd(-0.06, 0.06);
            v[0] = rnd(-0.35, 0.35); v[1] = rnd(4.5, 6.5); v[2] = rnd(-0.3, 0.3);
            return rnd(0.35, 0.6);
          });
        }
        if (blast.gerb[i] > 0) {
          blast.gerb[i] = Math.max(0, blast.gerb[i] - dt);
          const x = at.gerb[i];
          sparks.emit(Math.ceil(260 * dt), (p, v) => {
            p[0] = x; p[1] = 0.25; p[2] = Z.gerb;
            const a = rnd(0, Math.PI * 2), s = rnd(0, 0.9);
            v[0] = Math.cos(a) * s; v[1] = rnd(4, 5.5); v[2] = Math.sin(a) * s * 0.6;
            return rnd(0.8, 1.3);
          });
        }
        // The flame's light: up in a tenth of a second while it burns, down over a third after.
        burn[i] = blast.flame[i] > 0 ? Math.min(1, burn[i] + dt / 0.1) : Math.max(0, burn[i] - dt / 0.35);
        glowL[i].position.set(at.flame[i], 1.1, Z.flame + 0.6);
        glowL[i].intensity = 2.2 * burn[i];
      }

      co2.update(dt, (t, v, dt) => {
        const k = Math.exp(-2.4 * dt);                      // the jet slows fast and spreads as it does
        v[0] = v[0] * k + rnd(-1, 1) * dt * 1.2; v[1] = v[1] * k + 0.4 * dt; v[2] = v[2] * k + rnd(-1, 1) * dt;
      }, (t, out) => {
        out.copy(white).lerp(mean, 0.12);
        return [0.14 + 1.1 * Math.sqrt(t), Math.min(1, t / 0.04) * (1 - t) ** 1.5 * 0.22];
      }, tint);
      flames.update(dt, (t, v, dt) => {
        v[1] += 2.5 * dt;                                   // hot gas rises faster as it goes
        v[0] *= Math.exp(-1.5 * dt); v[2] *= Math.exp(-1.5 * dt);
      }, (t, out) => {
        flameColour(t, out);
        return [0.42 * (1 - t * 0.55), Math.min(1, t / 0.05) * (1 - t) ** 1.2 * 0.95];
      }, tint);
      sparks.update(dt, (t, v, dt) => { v[1] -= 9.8 * dt; }, (t, out) => {
        out.copy(HOT[0]).lerp(HOT[1], t);
        return [0.045, (1 - t) * (0.6 + 0.4 * Math.random())];
      }, tint);
    },
  };
}
