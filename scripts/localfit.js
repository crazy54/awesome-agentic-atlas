/* LOCAL FIT. Will this model run on this machine, and how fast? Pure functions, no DOM, no fetch.

   The browser half of the maths behind docs/local/. `scripts/localfit.py` is the same arithmetic in Python,
   which the generator uses for the no-script cheat sheet, and `tests/local_test.py` runs both over a grid of
   machines and models and fails on the first number where they disagree. Two copies is the cost of a page
   that answers with no server, and a copy nobody compares is how two answers to one question appear.

   PLACEHOLDER MATHS. This is ds-app's first cut, written to the interface agreed with ds-models
   (`team/contracts/fit.md`), so the page could be built before the real method landed. ds-models' module
   replaces this file's body. The exports and the shapes they return are the contract and stay put.

   The model, in one paragraph. A model needs its weights (the file you download) plus a cache that grows
   with the context it is asked to hold, plus a fixed working buffer. A machine offers a budget: a share of
   its graphics memory, or of its unified memory on a Mac or an APU, and on a PC with a graphics card,
   ordinary RAM as an overflow at a much slower speed. Generating one token reads every active weight once,
   so the speed is memory bandwidth divided by the bytes read per token, at an efficiency well short of the
   datasheet. That last step is why a mixture-of-experts model, which reads a tenth of itself per token, is
   fast for its size. */
const LOCALFIT = (() => {
  // How much of the datasheet bandwidth a real decode loop gets. 0.6 is the middle of what llama.cpp
  // measures across CUDA, Metal and Vulkan for a Q4 model; CPU decode is worse, because the cores share the
  // memory controller with everything else the machine is doing.
  const EFF_GPU = 0.6, EFF_CPU = 0.5;
  // The working buffer: compute scratch, the tokenizer, the runtime itself. Fixed, not a share of the
  // weights, because it barely moves between a 1B and a 30B model.
  const OVERHEAD_GB = 0.6;
  // The stated error on a speed estimate. Shown as a range, never as one number.
  const SPREAD = [0.7, 1.3];
  // "Great" means it runs at reading speed or faster and leaves room for the rest of the machine.
  const GREAT_TPS = 6, GREAT_HEADROOM = 0.15;

  // The memory this machine can give a model. `rules` is the catalogue's `usable` block: one rule per
  // platform, not per device, so a new laptop added to the catalogue needs no new arithmetic.
  const budget = (m, rules) => {
    const r = rules, ram = m.ram_gb;
    const sys = Math.max(ram * r.system_min_frac, ram - r.system_reserve_gb);
    if (m.unified && m.backend === "metal") {
      // macOS lets the GPU wire about two-thirds of memory on smaller Macs and three-quarters on bigger
      // ones, by default. It can be raised, and the numbers view says so; the default is what a beginner has.
      return {gpu: ram * (ram >= r.apple_big_from_gb ? r.apple_big_frac : r.apple_small_frac), cpu: 0};
    }
    if (m.unified) return {gpu: Math.max(0, Math.min(ram * r.unified_max_frac, ram - r.unified_reserve_gb)), cpu: 0};
    if (m.vram_gb > 0) return {gpu: Math.max(0, m.vram_gb - r.vram_reserve_gb), cpu: sys};
    return {gpu: 0, cpu: sys};
  };

  // The context cache: keys and values, for every layer, for every token held, at two bytes a number.
  const kvGB = (model, ctx) => 2 * model.layers * model.kv_heads * model.head_dim * ctx * 2 / 1e9;

  const need = (model, quant, ctx) => {
    const kv = kvGB(model, ctx);
    return {weights: quant.gb, kv, overhead: OVERHEAD_GB, total: quant.gb + kv + OVERHEAD_GB};
  };

  // Tokens a second, as [low, mid, high]. `gpuFrac` is the share of the model on the fast memory.
  const speed = (m, model, quant, place, gpuFrac) => {
    const bytes = quant.gb * (model.active_b / model.params_b);
    const gpuBW = (m.gpu_bw_gbs || 0) * EFF_GPU, cpuBW = (m.cpu_bw_gbs || 0) * EFF_CPU;
    let secs;
    if (place === "gpu") secs = bytes / gpuBW;
    else if (place === "cpu") secs = bytes / cpuBW;
    else secs = gpuFrac * bytes / gpuBW + (1 - gpuFrac) * bytes / cpuBW;
    const mid = 1 / secs;
    return [mid * SPREAD[0], mid, mid * SPREAD[1]];
  };

  // The whole answer for one model at one quant. `place` is where it runs: all on the accelerator ("gpu",
  // which on a Mac or a handheld is the shared memory), on the processor alone ("cpu"), or "split" between
  // a graphics card and RAM, which is what offload means.
  const fitQuant = (m, model, quant, ctx, rules) => {
    const b = budget(m, rules), n = need(model, quant, ctx);
    let place = null, space = 0, gpuFrac = 0;
    if (b.gpu > 0 && n.total <= b.gpu) { place = "gpu"; space = b.gpu; gpuFrac = 1; }
    else if (b.gpu === 0 && n.total <= b.cpu) { place = "cpu"; space = b.cpu; }
    else if (b.gpu > 0 && b.cpu > 0 && n.total <= b.gpu + b.cpu) {
      place = "split"; space = b.gpu + b.cpu; gpuFrac = b.gpu / n.total;
    }
    const have = place ? space : b.gpu + b.cpu;
    if (!place) return {verdict: "no", quant: quant.q, ctx, need: n, have, place: null, gpu_frac: 0,
                        tps: null, headroom: 1 - n.total / Math.max(have, 1e-9), catches: []};
    const tps = speed(m, model, quant, place, gpuFrac);
    const headroom = 1 - n.total / space;
    const catches = [];
    if (tps[1] < GREAT_TPS) catches.push("slow");
    if (headroom < GREAT_HEADROOM) catches.push("snug");
    if (place === "split") catches.push("split");
    const verdict = tps[1] >= GREAT_TPS && headroom >= GREAT_HEADROOM ? "great" : "ok";
    return {verdict, quant: quant.q, ctx, need: n, have, place, gpu_frac: gpuFrac, tps, headroom, catches};
  };

  // The quant to recommend. The model's default (almost always Q4_K_M, the sweet spot) if it fits at all;
  // otherwise the largest smaller one that does, marked, because below four bits a model gets noticeably
  // worse and the reader should know they are getting the squeezed version. `opts.quant` forces one.
  const fit = (m, model, opts, rules) => {
    const ctx = (opts && opts.ctx) || 8192;
    const qs = model.quants.slice().sort((a, b) => a.bits - b.bits);
    if (opts && opts.quant) {
      const q = qs.find((x) => x.q === opts.quant);
      if (q) return Object.assign(fitQuant(m, model, q, ctx, rules), {smaller: false});
    }
    const def = qs.find((x) => x.q === model.default_q) || qs[qs.length - 1];
    const first = fitQuant(m, model, def, ctx, rules);
    if (first.verdict !== "no") return Object.assign(first, {smaller: false});
    for (const q of qs.filter((x) => x.bits < def.bits && x.bits >= 3).reverse()) {
      const r = fitQuant(m, model, q, ctx, rules);
      if (r.verdict !== "no") return Object.assign(r, {smaller: true});
    }
    return Object.assign(first, {smaller: false});
  };

  // Speed in words a reader can picture. About 0.75 English words a token; people read 4 to 5 words a
  // second, so reading speed is about 6 tokens a second.
  const BANDS = [[2, "crawl", "very slow: a word every second or so"],
                 [6, "type", "slow: like someone typing"],
                 [15, "read", "about as fast as you read"],
                 [40, "fast", "faster than you can read"],
                 [Infinity, "instant", "near-instant"]];
  const speedWords = (tps) => {
    for (const [top, key, words] of BANDS) if (tps < top) return {key, words, wps: tps * 0.75};
    return null;
  };

  return {budget, kvGB, need, speed, fitQuant, fit, speedWords,
          consts: {EFF_GPU, EFF_CPU, OVERHEAD_GB, SPREAD, GREAT_TPS, GREAT_HEADROOM}};
})();
