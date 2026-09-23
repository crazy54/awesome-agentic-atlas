// "Dance with me": Archie dances to whatever the reader is playing. Load it as `<script type="module">`
// after `archie.js`; `31_home.py` wires both or neither.
//
// Two ways to hear the music, and the reader picks whichever matches how they are playing it:
//   "Music on this computer" -- `getDisplayMedia` with audio. Chromium shares a tab's sound anywhere, and the
//                               whole system's on Windows and ChromeOS. Offered only where the browser can
//                               capture display audio at all (Chromium's `suppressLocalAudioPlayback`
//                               constraint is the tell); Firefox and Safari share pictures without sound.
//   "Music in the room"      -- the microphone, with echo cancellation, noise suppression and auto gain off,
//                               because all three are built to remove exactly what we are listening for.
//                               Offered only when there is an audio input to open.
// The last choice is remembered and offered first. Nothing is recorded or sent anywhere, and nothing is
// played back: the stream goes into an AnalyserNode, which has no output, and into the beat detector, whose
// output reaches the speakers only as the silence it never writes over.
//
// The beat is found by `archie-beat.js`, an AudioWorklet, so it is heard on the audio thread and timed by
// the audio clock however busy the page is. The first detector here ran on animation frames, and at a
// quarter of the CPU -- a busy runner, or the model rendering on a slow laptop -- it counted hi-hats. The
// tempo is the median of the last twelve gaps between beats, folded into 70-180 BPM, and null until
// there are four.
//
// What it says to `archie.js`, through CustomEvents on `document`:
//   "archie:music"  {on, source: "system"|"mic"}   music mode starts or stops.
//   "archie:beat"   {strength: 0..1, bpm|null, at}  every detected beat, `at` on performance.now() at the
//                                                  onset, which the loader phase-locks his dance to.
// and, only while music mode is on, `window.archieMusic = {level(), bass(), bpm, lastBeat}` for a caller
// that wants to read the music every frame rather than wait for a beat. It is set before "archie:music"
// {on:true} is sent, because the loader reads it at load too and music can start before the model does.
//
// While the model is not live -- `.mhmascot[data-live]` absent, which is the poster -- the slot itself hops
// on each beat, by a class the page's CSS animates. Asked per beat, since the model can come up mid-song.
const BEAT = new URL("archie-beat.js" + new URL(import.meta.url).search, import.meta.url);
(() => {
  const btn = document.getElementById("dancebtn");
  const menu = document.getElementById("dancemenu");
  const slot = document.querySelector(".mhmascot");
  if (!btn || !menu || !slot) return;
  const md = navigator.mediaDevices;
  const Ctx = window.AudioContext || window.webkitAudioContext;
  if (!md || !Ctx || !("AudioWorkletNode" in window)) return;
  const canSystem = typeof md.getDisplayMedia === "function" &&
    !!(md.getSupportedConstraints && md.getSupportedConstraints().suppressLocalAudioPlayback);
  const canMic = typeof md.getUserMedia === "function";
  if (!canSystem && !canMic) return;

  // The same two gates the loader and the slot's CSS use: no mascot below 900px, and no dancing for a
  // reader who has asked for less motion. Watched live, since either can change with the page open.
  const wide = matchMedia("(min-width: 900px)");
  const calm = matchMedia("(prefers-reduced-motion: reduce)");
  const header = document.querySelector("header");
  const status = menu.querySelector(".dancemsg");
  const choices = Array.from(menu.querySelectorAll("[data-src]"));
  const KEY = "archie-dance";
  const LABEL = btn.textContent;
  const RAW = {echoCancellation: false, noiseSuppression: false, autoGainControl: false};

  let stream = null, ctx = null, src = null, beat = null, source = "";
  // Never hidden, only emptied: a live region that is unhidden and filled in one go is not announced.
  const say = text => { status.textContent = text; };

  // ---- The menu. Same shape as Settings: `hidden` is the state, aria-expanded says it, Escape and leaving
  // close it. Its own class on the header rather than Settings' `setopen`, because Settings' outside-click
  // listener removes that one on the very click that opens this menu.
  const setOpen = open => {
    menu.hidden = !open;
    btn.setAttribute("aria-expanded", String(open));
    header && header.classList.toggle("danceopen", open);
  };
  const offer = async () => {
    // A mic that is not there is not offered. Before permission the list has no labels, but it does have
    // one entry per kind that exists, which is all this asks.
    let mic = canMic;
    try { if (mic && md.enumerateDevices) mic = (await md.enumerateDevices()).some(d => d.kind === "audioinput"); }
    catch (e) {}
    let last = "";
    try { last = localStorage.getItem(KEY) || ""; } catch (e) {}
    for (const c of choices) {
      c.hidden = c.dataset.src === "system" ? !canSystem : !mic;
      c.classList.toggle("dancelast", c.dataset.src === last);
    }
    // The remembered one first, so Enter on the first choice is "the same as last time".
    const first = choices.find(c => !c.hidden && c.dataset.src === last) || choices.find(c => !c.hidden);
    if (first) first.parentNode.prepend(first);
    if (!choices.some(c => !c.hidden)) say("This browser has no way to hear music: no shareable audio and no microphone.");
    return first;
  };
  btn.addEventListener("click", async () => {
    if (stream) { stop(); btn.focus(); return; }
    if (!menu.hidden) { setOpen(false); return; }
    say("");
    const first = await offer();
    setOpen(true);
    first && first.focus();
  });
  menu.addEventListener("keydown", ev => {
    if (ev.key === "Escape") { setOpen(false); btn.focus(); }
  });
  for (const kind of ["click", "focusin"])
    document.addEventListener(kind, ev => {
      const inside = ev.target && ev.target.closest && ev.target.closest(".dancewrap");
      if (!menu.hidden && !inside) setOpen(false);
    });
  for (const c of choices) c.addEventListener("click", () => start(c.dataset.src));

  // ---- Listening.
  const open = async which => {
    if (which === "mic") return md.getUserMedia({audio: RAW, video: false});
    // `video: true` because Chromium will not share audio without it; the picture is stopped at once. The
    // reader still has to tick "Share audio" in the picker, and one who does not gets a stream with no
    // audio track, which `start()` says in words rather than dancing to silence.
    const s = await md.getDisplayMedia({video: true, audio: {...RAW, suppressLocalAudioPlayback: false},
                                        systemAudio: "include", selfBrowserSurface: "exclude"});
    for (const t of s.getVideoTracks()) t.stop();
    return s;
  };
  async function start(which) {
    say(which === "mic" ? "Asking for the microphone…" : "Pick the tab or screen that is playing, and tick Share audio.");
    let s;
    try { s = await open(which); }
    catch (e) {
      say(e && e.name === "NotAllowedError" ? "Not allowed, so Archie cannot hear anything. Nothing was shared."
        : e && e.name === "NotFoundError" ? "No microphone was found." : "Could not start listening.");
      return;
    }
    if (!s.getAudioTracks().length) {
      for (const t of s.getTracks()) t.stop();
      say(canMic ? "That share had no sound. Tick Share audio, or try Music in the room."
                 : "That share had no sound. Tick Share audio in the picker.");
      return;
    }
    try { localStorage.setItem(KEY, which); } catch (e) {}
    stream = s; source = which;
    // The browser's own "stop sharing" bar, or an unplugged mic, ends the track; music mode ends with it.
    for (const t of s.getAudioTracks()) t.addEventListener("ended", () => stop());
    ctx = new Ctx();
    if (ctx.state === "suspended") { try { await ctx.resume(); } catch (e) {} }
    src = ctx.createMediaStreamSource(s);
    try { await listen(src, ctx); }            // sets window.archieMusic, which the loader reads first
    catch (e) { stop(true); say("Could not start listening."); return; }
    if (!stream) return;                       // stopped while the detector loaded
    document.dispatchEvent(new CustomEvent("archie:music", {detail: {on: true, source: which}}));
    setOpen(false);
    btn.textContent = "Stop dancing";
    btn.focus();
  }
  // `quiet` for a start that failed before music mode was announced, so there is no "off" to announce.
  function stop(quiet) {
    if (!stream) return;
    for (const t of stream.getTracks()) t.stop();
    if (beat) { beat.port.onmessage = null; beat.disconnect(); }
    try { src && src.disconnect(); } catch (e) {}
    ctx && ctx.close().catch(() => {});
    stream = ctx = src = beat = null;
    delete window.archieMusic;
    slot.classList.remove("beat");
    if (quiet === true) return;
    document.dispatchEvent(new CustomEvent("archie:music", {detail: {on: false, source}}));
    btn.textContent = LABEL;
  }

  // ---- The beat.
  async function listen(node, ac) {
    await ac.audioWorklet.addModule(BEAT);
    if (ac !== ctx) return;                    // stopped while it loaded
    // Level and bass are read when asked, off an analyser, rather than every frame by a loop of this file's.
    const an = ac.createAnalyser();
    an.fftSize = 2048;
    node.connect(an);
    const wave = new Float32Array(an.fftSize), bins = new Uint8Array(an.frequencyBinCount);
    const BASS = Math.max(2, Math.round(160 / (ac.sampleRate / an.fftSize)));
    const gaps = [];
    const m = {bpm: null, lastBeat: 0, prev: -1};
    window.archieMusic = {
      level() {
        an.getFloatTimeDomainData(wave);
        let r = 0;
        for (let i = 0; i < wave.length; i++) r += wave[i] * wave[i];
        return Math.min(1, Math.sqrt(r / wave.length) * 4);
      },
      bass() {
        an.getByteFrequencyData(bins);
        let b = 0;
        for (let i = 1; i <= BASS; i++) b += bins[i];
        return b / (BASS * 255);
      },
      get bpm() { return m.bpm; }, get lastBeat() { return m.lastBeat; }};
    beat = new AudioWorkletNode(ac, "archie-beat", {numberOfInputs: 1, numberOfOutputs: 1});
    node.connect(beat);
    // Pulled by the destination, or a browser may not run it; it writes nothing, so what plays is silence.
    beat.connect(ac.destination);
    beat.port.onmessage = ({data}) => {
      if (m.prev >= 0 && data.at - m.prev < 2) { gaps.push(data.at - m.prev); if (gaps.length > 12) gaps.shift(); }
      m.prev = data.at;
      m.bpm = tempo(gaps);
      // The audio clock's time of the beat, as performance.now(): how long ago it was, by that clock, back
      // from now. A message that waited behind a long frame still arrives with the time the beat happened.
      const at = performance.now() - Math.max(0, ac.currentTime - data.at) * 1000;
      m.lastBeat = at;
      document.dispatchEvent(new CustomEvent("archie:beat", {detail: {strength: data.strength, bpm: m.bpm, at}}));
      if (!slot.hasAttribute("data-live")) bounce();
    };
  }
  const tempo = gaps => {
    if (gaps.length < 4) return null;
    const s = [...gaps].sort((a, b) => a - b), mid = s[s.length >> 1];
    let bpm = 60 / mid;
    while (bpm < 70) bpm *= 2;
    while (bpm > 180) bpm /= 2;
    return Math.round(bpm);
  };
  // Removed, then a layout read, then re-added, so a beat that lands mid-hop restarts it. Re-adding in the
  // next animation frame was the first version, and on a busy page the removal and the re-add fell in the
  // same style pass and the hop was skipped -- 11 hops for 19 beats in dance-check at a quarter CPU.
  const bounce = () => {
    slot.classList.remove("beat");
    void slot.offsetWidth;
    slot.classList.add("beat");
  };
  slot.addEventListener("animationend", () => slot.classList.remove("beat"));

  const gate = () => {
    const ok = wide.matches && !calm.matches;
    btn.hidden = !ok;
    if (!ok) { setOpen(false); stop(); }
  };
  wide.addEventListener("change", gate);
  calm.addEventListener("change", gate);
  gate();
})();
