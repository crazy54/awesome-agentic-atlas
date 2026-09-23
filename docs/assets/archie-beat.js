// The beat detector for "Dance with me", as an AudioWorklet: it runs on the audio thread, so a busy page --
// the 3D model rendering, a slow laptop -- cannot make it miss or smear a beat, and each beat is timed by
// the audio clock rather than by whichever animation frame happened to notice it. `archie-dance.js` loads
// it with `audioWorklet.addModule()`, under the same `?v=` as itself.
//
// Per hop of 256 samples (5.3 ms at 48 kHz) it splits the input at about 150 Hz with two one-pole
// low-passes, and takes each band's amplitude. The onset strength is how much each band rose over the last
// three hops, the bass counted four times the rest -- per band, not per bin, so the treble's width cannot
// outvote the kick. A beat is a peak of that strength above an adaptive threshold (mean + 2 sd of the last
// second, and a third of the recent peak), at least 280 ms after the one before, while the input is louder
// than a quiet room.
//
// It posts {at, strength}: `at` in seconds on the context's clock, at the peak.
class Beat extends AudioWorkletProcessor {
  constructor() {
    super();
    this.a = 1 - Math.exp(-2 * Math.PI * 150 / sampleRate);
    this.l1 = this.l2 = 0;
    this.H = 256; this.n = 0; this.sLo = this.sHi = this.sAll = 0;
    this.lo = [0, 0, 0, 0]; this.hi = [0, 0, 0, 0];
    this.odf = []; this.MAX = Math.round(sampleRate / this.H);      // a second of onset strengths
    this.peak = 0; this.decay = Math.pow(0.5, this.H / sampleRate / 3); // halves in 3 s
    this.rms = 0; this.prev = 0; this.prevAt = 0; this.last = -1;
  }
  process(inputs) {
    const x = inputs[0] && inputs[0][0];
    if (!x) return true;
    for (let i = 0; i < x.length; i++) {
      this.l1 += this.a * (x[i] - this.l1);
      this.l2 += this.a * (this.l1 - this.l2);
      const h = x[i] - this.l2;
      this.sLo += this.l2 * this.l2; this.sHi += h * h; this.sAll += x[i] * x[i];
      if (++this.n === this.H) this.hop(currentTime + (i + 1) / sampleRate);
    }
    return true;
  }
  hop(t) {
    const lo = Math.sqrt(this.sLo / this.H), hi = Math.sqrt(this.sHi / this.H);
    this.rms += (Math.sqrt(this.sAll / this.H) - this.rms) * 0.1;      // about 50 ms
    this.n = 0; this.sLo = this.sHi = this.sAll = 0;
    const odf = (4 * Math.max(0, lo - this.lo[0]) + Math.max(0, hi - this.hi[0])) / 5;
    this.lo.shift(); this.lo.push(lo); this.hi.shift(); this.hi.push(hi);
    const o = this.odf;
    let mean = 0, sd = 0;
    for (const v of o) mean += v;
    mean /= o.length || 1;
    for (const v of o) sd += (v - mean) ** 2;
    sd = Math.sqrt(sd / (o.length || 1));
    this.peak = Math.max(this.peak * this.decay, odf);
    const thr = Math.max(mean + 2 * sd, this.peak / 3);
    // The hop before this one was the peak if it cleared the threshold and this one is lower.
    if (o.length >= this.MAX / 4 && this.prev > thr && odf <= this.prev && this.rms > 0.005 &&
        this.prevAt - this.last >= 0.28) {
      this.last = this.prevAt;
      this.port.postMessage({at: this.prevAt, strength: Math.min(1, this.prev / (2 * thr))});
    }
    o.push(odf);
    if (o.length > this.MAX) o.shift();
    this.prev = odf; this.prevAt = t;
  }
}
registerProcessor("archie-beat", Beat);
