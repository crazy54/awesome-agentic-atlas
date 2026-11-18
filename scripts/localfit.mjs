// fit.mjs: will this model run on this machine, and how fast?
//
// A small, dependency-free ES module for the local-AI page. It works the same in the browser and in Node, and every
// export is a pure function of its arguments: no globals, no clock, no network. The method, its sources and its
// error bands are written up in team/contracts/fit.md; this file is that document in code, and the two must agree.
//
// The shape of the answer:
//
//   memory need = weights + KV cache (grows with context) + compute buffers   … compared with what the machine can
//                 actually give a model: VRAM less the driver's and desktop's share, or the GPU-wired share of unified
//                 memory, or system RAM less what the OS keeps.
//   decode speed: generating one token reads every active weight once, so tokens/s ≈ effective bandwidth ÷ bytes
//                 read per token, plus a fixed per-layer cost (kernel launches, synchronisation) that dominates on
//                 small models and very fast chips. Both terms are fitted per backend to published llama.cpp numbers
//                 (calibration.mjs).
//   prefill speed: reading the prompt is a big matrix multiply, so it is compute-bound: tokens/s ≈ efficiency ×
//                 FLOPS ÷ (2 × active parameters).
//
// Units: GB means 1e9 bytes everywhere (vendors' convention for VRAM and bandwidth; llama.cpp prints GiB, and the
// calibration converts). Bandwidth is GB/s, compute is TFLOPS.
//
// Inputs are plain objects. `model` follows eng-hf's team/contracts/models.md (config fields flattened), `hardware`
// follows ds-hardware's team/contracts/hardware.md; `normalizeHardware()` is the one place that maps catalogue field
// names onto what this module reads, so a schema change there touches one function here.

export const GB = 1e9;

// ── Quantisation types ───────────────────────────────────────────────────────────────────────────────────────────
//
// bpw: effective bits per weight of a whole GGUF file, as llama.cpp's quantize README measures it on Llama 3.1 8B
//      (https://github.com/ggml-org/llama.cpp/blob/master/tools/quantize/README.md). "Effective" means it already
//      includes the block scales and the tensors a mix keeps at higher precision, so params × bpw / 8 lands within a
//      few per cent of real file sizes. When eng-hf's index has the real file size we use that instead.
// kernel: how much slower than "pure bandwidth" a quant decodes, from the same README's tg128 column (time per token
//      against bytes per token, with F16 and Q8_0 as the 1.0 reference). K-quants cost a little dequantisation
//      compute; the low-bit i-quants cost a lot. Q4_0 and MXFP4 are not in that table; Q4_0 is fitted from the Apple
//      thread, MXFP4 is set equal to Q4_K (an assumption, flagged in fit.md).
// quality: rank used when choosing between quants (higher is closer to the original model). floor marks the lowest
//      quant we will recommend to a beginner without a warning.
export const QUANTS = {
  F16:     { bpw: 16.00, kernel: 1.00, quality: 100, format: 'gguf' },
  BF16:    { bpw: 16.00, kernel: 1.00, quality: 100, format: 'gguf' },
  Q8_0:    { bpw: 8.50,  kernel: 1.00, quality: 95,  format: 'gguf' },
  Q6_K:    { bpw: 6.56,  kernel: 1.10, quality: 90,  format: 'gguf' },
  Q5_K_M:  { bpw: 5.70,  kernel: 1.07, quality: 85,  format: 'gguf' },
  Q5_K_S:  { bpw: 5.57,  kernel: 1.05, quality: 83,  format: 'gguf' },
  Q4_K_M:  { bpw: 4.89,  kernel: 1.14, quality: 78,  format: 'gguf' },
  MXFP4:   { bpw: 4.25,  kernel: 1.14, quality: 78,  format: 'gguf' }, // gpt-oss native; experts only, see bytesRead
  Q4_K_S:  { bpw: 4.67,  kernel: 1.10, quality: 75,  format: 'gguf' },
  Q4_0:    { bpw: 4.55,  kernel: 1.00, quality: 72,  format: 'gguf' }, // kernel refined by calibrate (see CAL)
  IQ4_NL:  { bpw: 4.68,  kernel: 1.10, quality: 75,  format: 'gguf' },
  IQ4_XS:  { bpw: 4.46,  kernel: 1.14, quality: 74,  format: 'gguf' },
  Q3_K_L:  { bpw: 4.30,  kernel: 1.36, quality: 66,  format: 'gguf' },
  Q3_K_M:  { bpw: 4.00,  kernel: 1.40, quality: 62,  format: 'gguf', floor: true },
  IQ3_M:   { bpw: 3.76,  kernel: 1.53, quality: 62,  format: 'gguf', floor: true },
  Q3_K_S:  { bpw: 3.64,  kernel: 1.59, quality: 55,  format: 'gguf' },
  IQ3_XXS: { bpw: 3.25,  kernel: 1.66, quality: 52,  format: 'gguf' },
  Q2_K:    { bpw: 3.16,  kernel: 1.55, quality: 40,  format: 'gguf' },
  IQ2_M:   { bpw: 2.93,  kernel: 1.83, quality: 38,  format: 'gguf' },
  IQ2_XXS: { bpw: 2.38,  kernel: 2.05, quality: 30,  format: 'gguf' },
  IQ1_M:   { bpw: 2.15,  kernel: 2.55, quality: 15,  format: 'gguf' },
  // MLX (Apple). Affine quantisation with group size 64 and an fp16 scale and bias per group: +0.5 bpw.
  // https://ml-explore.github.io/mlx/build/html/python/_autosummary/mlx.core.quantize.html
  'mlx-bf16':  { bpw: 16.0, kernel: 1.00, quality: 100, format: 'mlx' },
  'mlx-8bit':  { bpw: 8.5,  kernel: 1.00, quality: 95,  format: 'mlx' },
  'mlx-6bit':  { bpw: 6.5,  kernel: 1.05, quality: 88,  format: 'mlx' },
  'mlx-4bit':  { bpw: 4.5,  kernel: 1.05, quality: 74,  format: 'mlx' },
  'mlx-3bit':  { bpw: 3.5,  kernel: 1.10, quality: 55,  format: 'mlx' },
};

// The spec for any quant label the index can carry. Unsloth's dynamic quants (UD-Q4_K_XL …) and bartowski's _L
// variants keep a few tensors at higher precision than the base type, so they take the base type's kernel and
// quality and their own real size. MLX labels from the index ('4bit', '8bit', 'mxfp4', '4bit-DWQ') map onto the
// mlx-* rows. Unknown labels get a neutral spec and their bpw from the file size.
export function quantSpec(label) {
  if (!label) return null;
  if (QUANTS[label]) return QUANTS[label];
  let l = String(label).toUpperCase().replace(/^UD-/, '');
  const mlx = /^(\d+)BIT/.exec(l) || (l === 'MXFP4-MLX' ? ['', '4'] : null);
  if (mlx) return QUANTS[`mlx-${mlx[1]}bit`] ?? QUANTS['mlx-4bit'];
  if (l === 'BF16' || l === 'F16' || l === 'FP16') return QUANTS.F16;
  l = l.replace(/^(Q[2-6]_K)_XL$/, '$1_L').replace(/^(Q[2-6]_K)_L$/, (m, b) => ({ Q3_K: 'Q3_K_L', Q6_K: 'Q6_K', Q2_K: 'Q2_K' })[b] ?? `${b}_M`)
    .replace(/^Q8_K_XL$/, 'Q8_0');
  return QUANTS[l] ?? { bpw: null, kernel: 1.15, quality: 60, format: 'gguf' };
}

// Recommendation order for GGUF, best quality first. bestQuant() walks this list.
// MXFP4 is only offered when the index lists it (gpt-oss ships in it; re-quantising MXFP4 experts gains little).
export const GGUF_LADDER = ['Q8_0', 'Q6_K', 'Q5_K_M', 'MXFP4', 'Q4_K_M', 'IQ4_XS', 'Q3_K_M', 'IQ3_M', 'IQ3_XXS', 'Q2_K'];
export const MLX_LADDER = ['mlx-8bit', 'mlx-6bit', 'mlx-4bit', 'mlx-3bit'];

// KV-cache element sizes. llama.cpp's q8_0/q4_0 cache types are its block formats (34 and 18 bytes per 32 values).
// Quantising V needs flash attention; llama.cpp turns FA on automatically where the backend supports it.
export const KV_BYTES = { f16: 2, bf16: 2, q8_0: 34 / 32, q4_0: 18 / 32 };

// ── Calibrated constants ─────────────────────────────────────────────────────────────────────────────────────────
//
// eta: share of theoretical memory bandwidth decode actually achieves; layerMs: fixed milliseconds per layer per
// token. Fitted by tools/calibrate.mjs against calibration.mjs (least squares on log tokens/s); test.mjs re-checks
// the fit and fails if the error drifts past the bands stated in fit.md. ppEta: prefill efficiency against the
// hardware's fp16_tflops (see hardware.md for which TFLOPS figure that is), set from the same scoreboards' pp512.
// kv: how efficiently attention reads the KV cache compared with weights (below 1 = attention costs more per byte
// than its size alone suggests), fitted from the 8k/32k-deep rows; backends without deep rows use 1.
// spread: the ± band (as a ratio) we put around an estimate, from the observed calibration error (p90 of |log err|)
// plus a margin for real-world drift (drivers, thermals, background load) that benchmarks don't have.
export const CAL = {
  metal:          { eta: 0.90, layerMs: 0.150, kv: 0.54, ppEta: 0.63, spread: 0.25 },
  cuda:           { eta: 0.91, layerMs: 0.060, kv: 0.81, ppEta: 1.00, spread: 0.20 },
  vulkan:         { eta: 0.81, layerMs: 0.025, kv: 0.87, ppEta: 0.37, spread: 0.25 }, // kv: no deep rows; CUDA's
  'vulkan-intel': { eta: 0.48, layerMs: 0.025, kv: 0.87, ppEta: 0.08, spread: 0.40 }, // Intel Arc (driver-limited)
  rocm:           { eta: 0.76, layerMs: 0.060, kv: 0.87, ppEta: 0.37, spread: 0.25 },
  sycl:           { eta: 0.55, layerMs: 0.040, kv: 0.87, ppEta: 0.25, spread: 0.40 }, // not calibrated: see fit.md
  cpu:            { eta: 0.58, layerMs: 0.000, kv: 1.00, ppEta: 1.00, spread: 0.50 },
  mlx:            { eta: 0.90, layerMs: 0.150, kv: 0.54, ppEta: 0.63, spread: 0.30 }, // not calibrated: Metal's values
  q4_0Kernel: 0.97,
  // CPU threads sharing a token with the GPU reach a lower share of RAM bandwidth than a CPU-only run (they sync
  // with the GPU every layer, and the expert reads are scattered). Fitted to the single hybrid row in calibration.mjs.
  hybridCpu: 0.83,
  // GTX 10-series and V100 rows decode at ~60% of what their bandwidth predicts (2 rows; see calibration.mjs).
  legacyArch: 0.62,
};
const LEGACY_ARCH = new Set(['pascal', 'volta', 'maxwell', 'kepler']);

// Speed thresholds for the plain-English verdicts, in decode tokens/s. Fluent reading runs at roughly 4–5 words a
// second, about 6–7 tokens (at ~0.75 words a token). "Great" is 10 tok/s, comfortably ahead of the reader, so the
// low end of the ± band still keeps up. Reasoning models write hundreds to thousands of hidden "thinking" tokens
// before the answer, so for them "great" is 20 tok/s (a 1,500-token think then takes about 75 s rather than 150).
// Below 1.5 tok/s a 300-word reply takes over four minutes, which we call too slow to be useful.
export const THRESHOLDS = { great: 10, greatReasoning: 20, usable: 1.5, minContext: 4096, headroomNote: 0.05 };

// Speed in words, for the cards (bands from team/local-ai/ux.md, kept here so there is one copy).
export const SPEED_WORDS = [
  { below: 2, words: 'very slow: a word every second or so' },
  { below: 6, words: 'slow: like someone typing' },
  { below: 15, words: 'about as fast as you read' },
  { below: 40, words: 'faster than you can read' },
  { below: Infinity, words: 'near-instant' },
];
export const WORDS_PER_TOKEN = 0.75;
export function speedWords(tps) {
  return SPEED_WORDS.find((b) => tps < b.below).words;
}

export const VERDICT_LABELS = {
  great: 'Runs great',
  slow: 'Runs, slowly',
  tight: 'Fits only with a smaller quant or a shorter context',
  'too-big': 'Too big',
};
export function verdictLabel(v) { return VERDICT_LABELS[v] ?? v; }

// ── Model geometry ───────────────────────────────────────────────────────────────────────────────────────────────

const num = (x) => (typeof x === 'number' && Number.isFinite(x) ? x : null);

// Parameters that are routed experts (MoE), from the config when it has moe_intermediate_size, else inferred from
// total vs active: total = shared + experts, active = shared + experts × k/E  ⇒  experts = (total − active)/(1 − k/E).
export function expertParams(m) {
  const E = num(m.num_experts), k = num(m.num_experts_per_tok);
  if (!E || !k || E <= 1) return 0;
  const H = num(m.hidden_size), I = num(m.moe_intermediate_size), L = num(m.num_hidden_layers);
  if (H && I && L) {
    const moeLayers = L - (num(m.first_k_dense_replace) ?? 0);
    return moeLayers * E * 3 * H * I;
  }
  const total = num(m.params_total), active = num(m.params_active);
  if (total && active && active < total) return (total - active) / (1 - k / E);
  return 0;
}

export function activeParams(m) {
  const total = num(m.params_total) ?? 0;
  const ex = expertParams(m);
  if (!ex) return num(m.params_active) ?? total;
  return total - ex + ex * (m.num_experts_per_tok / m.num_experts);
}

// The input embedding table is a lookup: a token reads one row of it, not the whole table. When the output head is
// tied to it, the full table is read anyway (as the output projection), so nothing is saved.
function embeddingParams(m) {
  if (m.tie_word_embeddings) return 0;
  const V = num(m.vocab_size), H = num(m.hidden_size);
  return V && H ? V * H : 0;
}

// Weight bytes in memory for a model at a quant. Prefers the real file size from the index: either `quant.bytes`
// passed in, or a matching entry in model.quants. Falls back to params × bpw.
export function weightBytes(m, quant) {
  const q = typeof quant === 'string' ? { quant } : quant;
  if (num(q.bytes)) return q.bytes;
  const hit = (m.quants ?? []).find((x) => x.quant === q.quant && num(x.bytes));
  if (hit) return hit.bytes;
  const spec = quantSpec(q.quant);
  if (!spec || !spec.bpw) throw new Error(`unknown quant ${q.quant}`);
  const total = num(m.params_total);
  if (!total) throw new Error(`model ${m.id ?? '?'} has no params_total`);
  if (q.quant === 'MXFP4') {
    // gpt-oss ships experts in MXFP4 and everything else at 8–16 bits; ~8.5 bpw on the rest matches the real files.
    const ex = expertParams(m);
    return (ex * 4.25 + (total - ex) * 8.5) / 8;
  }
  return (total * spec.bpw) / 8;
}

// Bytes read from memory to generate one token: every active weight once, minus the embedding table (one row only).
export function bytesReadPerToken(m, quant) {
  const W = weightBytes(m, quant);
  const qn = typeof quant === 'string' ? quant : quant.quant;
  const total = num(m.params_total);
  const ex = expertParams(m);
  const emb = embeddingParams(m);
  if (!total) return W;
  if (!ex) return W * (1 - emb / total);
  let expBytes, restBytes;
  if (qn === 'MXFP4') {
    expBytes = (ex * 4.25) / 8;
    restBytes = W - expBytes;
  } else {
    expBytes = (W * ex) / total;
    restBytes = W - expBytes;
  }
  const restParams = total - ex;
  const restRead = restBytes * (1 - emb / restParams);
  return restRead + expBytes * (m.num_experts_per_tok / m.num_experts);
}

// Which layers keep a full-length KV cache. Sliding-window layers cap at the window; linear-attention / recurrent
// layers (Mamba, Gated DeltaNet) keep a small fixed state instead. layer_types (HF config) wins when present;
// otherwise sliding_window_pattern N means every Nth layer is global (Gemma 3: 6 → 5 local : 1 global; gpt-oss: 2).
function layerKinds(m) {
  const L = num(m.num_hidden_layers) ?? 0;
  // The index (models.md `dims`) gives counts rather than a per-layer list; order doesn't matter for totals.
  if (num(m.swa_layers) != null || num(m.linear_layers) != null) {
    const sw = num(m.swa_layers) ?? 0, lin = num(m.linear_layers) ?? 0;
    return Array.from({ length: L }, (_, i) => (i < sw ? 'swa' : i < sw + lin ? 'linear' : 'full'));
  }
  if (Array.isArray(m.layer_types) && m.layer_types.length) {
    return m.layer_types.map((t) => (/sliding/.test(t) ? 'swa' : /linear|mamba|recurrent|delta|ssm/.test(t) ? 'linear' : 'full'));
  }
  const pat = num(m.sliding_window_pattern);
  if (num(m.sliding_window) && pat && pat > 1) {
    return Array.from({ length: L }, (_, i) => ((i + 1) % pat === 0 ? 'full' : 'swa'));
  }
  if (num(m.sliding_window) && m.use_sliding_window === true) return Array(L).fill('swa'); // Mistral-7B v0.1 style
  return Array(L).fill('full');
}

// KV-cache bytes at a context length.
//   standard / GQA / MQA: 2 (K and V) × kv_heads × head_dim × bytes per element, per layer per token.
//   MLA (DeepSeek V2/V3, Kimi K2): llama.cpp caches the compressed latent, kv_lora_rank + qk_rope_head_dim values
//   per layer per token, which is what makes a 671B model's 128k context affordable.
export function kvBytes(m, context, kvQuant = 'f16') {
  const el = KV_BYTES[kvQuant] ?? 2;
  const kinds = layerKinds(m);
  if (num(m.kv_lora_rank)) {
    const per = (m.kv_lora_rank + (num(m.qk_rope_head_dim) ?? 64)) * el;
    return kinds.length * per * context;
  }
  const kvh = num(m.num_key_value_heads) ?? num(m.num_attention_heads) ?? 0;
  const hd = num(m.head_dim) ?? (num(m.hidden_size) && num(m.num_attention_heads) ? m.hidden_size / m.num_attention_heads : 0);
  const perTokLayer = 2 * kvh * hd * el;
  const win = num(m.sliding_window) ?? context;
  let bytes = 0;
  for (const k of kinds) {
    if (k === 'full') bytes += perTokLayer * context;
    else if (k === 'swa') bytes += perTokLayer * Math.min(context, win + 512); // llama.cpp keeps window + one ubatch
  }
  // Recurrent layers hold a fixed state (tens of MB for the models in the index); a flat allowance covers it.
  if (kinds.includes('linear')) bytes += 0.1 * GB;
  return bytes;
}

// Scratch memory the runtime needs on top of weights and KV: llama.cpp's compute buffer, sized for the worst case of
// one micro-batch (512 tokens) with all-token logits (n_vocab floats each) plus activations. Measured compute buffers
// for 7–8B models with flash attention are 0.25–0.5 GB; this formula gives 0.45 GB for Llama 3.1 8B.
export function computeBufferBytes(m) {
  const V = num(m.vocab_size) ?? 32000, H = num(m.hidden_size) ?? 4096;
  // Vision models also load a projector (mmproj): its real size when the index has it, else 0.6 GB (typical for
  // the SigLIP-class encoders in Gemma 3 and Qwen-VL), plus its own activations.
  const proj = m.vision ? (num(m.mmproj_bytes) ?? 0.6 * GB) + 0.2 * GB : 0;
  return 512 * (V * 4 + H * 64) + 0.05 * GB + proj;
}

// Maps one row of eng-hf's docs/models.json (team/contracts/models.md) onto the config-style fields this module
// reads. `row` is the row as an object (cols applied); its variants and files may still be arrays, in which case
// pass the file's variant_cols and file_cols. The result keeps every quant file the index lists, with its real
// size, so weightBytes() never has to estimate for a model the index covers.
export function normalizeModel(row, variantCols, fileCols) {
  const d = row.dims ?? {};
  const asObj = (cols, r) => (Array.isArray(r) && cols ? Object.fromEntries(cols.map((c, i) => [c, r[i]])) : r);
  const variants = (row.variants ?? []).map((v) => asObj(variantCols, v));
  const quants = [];
  let mmproj = null;
  for (const v of variants) {
    if (v.fmt !== 'gguf' && v.fmt !== 'mlx') continue;
    if (v.fmt === 'gguf' && num(v.mmproj) && (mmproj == null || v.mmproj < mmproj)) mmproj = v.mmproj;
    for (const f0 of v.files ?? []) {
      const f = asObj(fileCols, f0);
      if (!num(f.bytes)) continue;
      const label = f.q;
      let quant = label;
      if (v.fmt === 'mlx') {
        const bits = /(\d+)bit/i.exec(label)?.[1] ?? (/mxfp4/i.test(label) ? '4' : /bf16|fp16/i.test(label) ? 'bf16' : null);
        if (!bits) continue;
        quant = bits === 'bf16' ? 'mlx-bf16' : `mlx-${bits}bit`;
      } else if (!QUANTS[label]) {
        // Keep the label (it is the download name) but make sure quantSpec can read it.
        quant = label;
      }
      // First listed variant wins for a given quant: variants are ordered biggest audience first.
      if (!quants.some((q) => q.quant === quant && q.format === v.fmt)) {
        quants.push({ format: v.fmt, quant, label, repo: v.repo, by: v.by, bytes: f.bytes });
      }
    }
  }
  const moe = row.moe ?? null;
  return {
    id: row.id, name: row.name, family: row.family, license: row.license, uses: row.uses ?? [],
    params_total: num(row.params), params_active: num(row.active),
    num_hidden_layers: num(d.layers), hidden_size: num(d.hidden), num_attention_heads: num(d.heads),
    num_key_value_heads: num(d.kv_heads), head_dim: num(d.head_dim), vocab_size: num(d.vocab),
    sliding_window: num(d.swa), swa_layers: num(d.swa_layers), linear_layers: num(d.linear_layers),
    kv_lora_rank: num(d.kv_lora_rank), qk_rope_head_dim: num(d.rope_dim),
    moe_intermediate_size: num(d.moe_ffn), first_k_dense_replace: num(d.dense_layers),
    tie_word_embeddings: d.tied ?? false,
    num_experts: num(moe?.experts), num_experts_per_tok: num(moe?.per_tok),
    max_context: num(row.ctx),
    vision: (row.uses ?? []).includes('vision'), reasoning: (row.uses ?? []).includes('reasoning'),
    mmproj_bytes: mmproj, ollama: row.ollama ?? null, gated: row.gated ?? false,
    quants,
  };
}

// ── Hardware ─────────────────────────────────────────────────────────────────────────────────────────────────────

// What the OS and everyday apps keep for themselves out of system RAM. Judgment, not measurement: a fresh Windows 11
// desktop with a browser open sits at 4–6 GB, macOS at 3–5 GB, a light Linux desktop or SteamOS at 2–3 GB.
export function osReserveGB(os, ramGB) {
  switch (os) {
    case 'windows': return 3.5 + 0.08 * ramGB;
    // macOS compresses and pages out idle apps' memory readily; llama.cpp's gpt-oss guide runs a 13.5 GB footprint
    // (gpt-oss-20b at 32k context) on a 16 GB Mac, so the Mac reserve is the smallest.
    case 'macos': return 2.0 + 0.03 * ramGB;
    default: return 1.5 + 0.05 * ramGB; // linux, steamos
  }
}

// Apple's default GPU wired limit (Metal's recommendedMaxWorkingSetSize, which llama.cpp prints at start-up): two-
// thirds of RAM up to 36 GB (10.67 GB on a 16 GB Mac), three-quarters up to 128 GB (96 GB of 128), and about 80%
// above (154 GB of 192, per llama.cpp's gpt-oss guide, https://github.com/ggml-org/llama.cpp/discussions/15396).
// It can be raised with `sudo sysctl iogpu.wired_limit_mb=<MB>` (macOS 14+); the setting resets on reboot.
export function appleGpuShareGB(ramGB) {
  if (ramGB <= 36) return ramGB * (2 / 3);
  if (ramGB <= 128) return ramGB * 0.75;
  return ramGB * 0.8;
}

// Maps a catalogue entry (team/contracts/hardware.md) onto the fields this module reads. Accepts either the
// catalogue's names or this module's own, so tests and the page's "custom machine" form can pass plain objects.
export function normalizeHardware(h) {
  const mem = h.memory ?? {};
  const ramGB = num(h.ram_gb) ?? num(mem.ram_gb) ?? 16;
  const ramBW = num(h.ram_bandwidth_gbs) ?? num(mem.ram_bandwidth_gbs) ?? 60;
  const unified = Boolean(h.unified ?? mem.unified);
  const os = h.os ?? (Array.isArray(h.os_options) ? h.os_options[0] : undefined) ?? (h.gpu?.vendor === 'apple' ? 'macos' : 'windows');
  const gpus = (Array.isArray(h.gpus) ? h.gpus : h.gpu ? [h.gpu] : []).filter(Boolean);
  let gpu = null;
  if (gpus.length) {
    const g0 = gpus[0];
    const integrated = Boolean(g0.integrated ?? unified);
    const vram = gpus.reduce((s, g) => s + (num(g.vram_gb) ?? 0), 0);
    gpu = {
      vendor: g0.vendor,
      name: g0.name,
      count: gpus.length,
      integrated,
      vram_gb: integrated ? null : vram,
      // Multi-GPU layer split runs the cards one after another, so per-token time is set by the slowest card.
      bandwidth_gbs: Math.min(...gpus.map((g) => num(g.vram_bandwidth_gbs) ?? num(g.bandwidth_gbs) ?? (integrated ? ramBW : 300))),
      fp16_tflops: num(g0.fp16_tflops) ?? null,
      arch: typeof g0.arch === 'string' ? g0.arch.toLowerCase() : null,
      backends: g0.backends ?? defaultBackends(g0.vendor, os),
    };
  }
  let gpuUsableGB = num(h.gpu_usable_gb) ?? num(mem.gpu_usable_gb);
  if (gpu && gpu.integrated && gpuUsableGB == null) {
    if (gpu.vendor === 'apple') gpuUsableGB = appleGpuShareGB(ramGB);
    // AMD/Intel APUs: what the driver lets the GPU address. Windows exposes the BIOS carve-out plus up to half of
    // the remaining RAM as shared memory; Linux's default GTT limit is half of RAM. Strix Halo owners routinely raise
    // either (BIOS UMA up to 96 GB of 128 on Windows; on Linux `options ttm pages_limit=…` lets Vulkan address
    // ~120 GB, per the gpt-oss guide above), which the catalogue records in gpu_usable_gb.
    else gpuUsableGB = ramGB * 0.5;
  }
  return {
    id: h.id, name: h.name, os, ramGB, ramBW, unified, gpu, gpuUsableGB,
    cpuCores: num(h.cpu?.cores_perf) ?? num(h.cpu?.cores) ?? 6,
    cpuTflops: num(h.cpu?.fp32_tflops) ?? null,
  };
}

function defaultBackends(vendor, os) {
  switch (vendor) {
    case 'nvidia': return ['cuda', 'vulkan'];
    case 'amd': return os === 'linux' ? ['vulkan', 'rocm'] : ['vulkan', 'rocm'];
    case 'intel': return ['vulkan', 'sycl'];
    case 'apple': return ['metal', 'mlx'];
    default: return ['vulkan'];
  }
}

// The backend whose numbers we quote: the first the hardware lists that suits the quant's format (MLX quants need
// MLX; GGUF never runs on MLX). Callers can force one with opts.backend.
export function pickBackend(hw, quantName, forced) {
  const fmt = quantSpec(quantName)?.format ?? 'gguf';
  if (!hw.gpu) return 'cpu';
  const list = hw.gpu.backends ?? [];
  if (forced && list.includes(forced)) return forced;
  if (fmt === 'mlx') return list.includes('mlx') ? 'mlx' : null;
  return list.find((b) => b !== 'mlx') ?? 'cpu';
}

// Memory budgets in bytes: what a model may occupy on the GPU (fast pool) and in system RAM (slow pool).
export function budgets(hw) {
  const ramFree = Math.max(0, hw.ramGB - osReserveGB(hw.os, hw.ramGB)) * GB;
  if (!hw.gpu) return { gpu: 0, ram: ramFree, shared: false };
  if (hw.gpu.integrated) {
    // One pool. The GPU may use its share, but never more than RAM minus the OS's share.
    const gpu = Math.min(hw.gpuUsableGB * GB, ramFree);
    return { gpu, ram: ramFree, shared: true };
  }
  // Discrete card: the CUDA/ROCm/Vulkan context takes ~0.3–0.5 GB, and on the card driving the display the desktop
  // compositor and browsers hold more (0.3–1.5 GB on Windows). 0.5 GB + 5% covers the common case.
  const gpu = Math.max(0, hw.gpu.vram_gb * GB - (0.5 * GB + 0.05 * hw.gpu.vram_gb * GB));
  return { gpu, ram: ramFree, shared: false };
}

// ── Fit ──────────────────────────────────────────────────────────────────────────────────────────────────────────

// fit(model, quant, hardware, opts) → where the model would live and whether it fits.
//   quant: a quant name ('Q4_K_M', 'mlx-4bit', …) or { quant, bytes } with the real file size.
//   opts.context (tokens, default 8192), opts.kvQuant ('f16' | 'q8_0' | 'q4_0'), opts.backend (force one).
// placement: 'gpu' (all on the fast pool), 'partial' (some layers or experts in system RAM), 'cpu', or 'none'.
export function fit(model, quant, hardware, opts = {}) {
  const hw = hardware.ramGB != null ? hardware : normalizeHardware(hardware);
  const qn = typeof quant === 'string' ? quant : quant.quant;
  // A model can't use more context than it was trained for; asking for 32k on a 4k model means 4k.
  const context = Math.min(opts.context ?? 8192, num(model.max_context) ?? Infinity);
  const kvQuant = opts.kvQuant ?? 'f16';
  const backend = pickBackend(hw, qn, opts.backend);
  const W = weightBytes(model, quant);
  const KV = kvBytes(model, context, kvQuant);
  const BUF = computeBufferBytes(model);
  const total = W + KV + BUF;
  const b = budgets(hw);
  const L = num(model.num_hidden_layers) ?? 32;
  const notes = [];
  const base = { quant: qn, context, kvQuant, backend, weightsGB: W / GB, kvGB: KV / GB, bufferGB: BUF / GB, totalGB: total / GB,
    gpuBudgetGB: b.gpu / GB, ramBudgetGB: b.ram / GB, layers: L };

  if (backend === null) return { ...base, placement: 'none', fits: false, gpuLayers: 0, cpuBytes: 0, gpuBytes: 0,
    notes: ['MLX models run only on Apple Silicon Macs.'] };

  // Everything on the GPU / unified pool.
  if (b.gpu > 0 && total <= b.gpu) {
    return { ...base, placement: 'gpu', fits: true, gpuLayers: L, gpuBytes: W, cpuBytes: 0, headroomGB: (b.gpu - total) / GB, notes };
  }

  // No usable GPU: system RAM only.
  if (b.gpu <= 0 || backend === 'cpu') {
    const fits = total <= b.ram;
    return { ...base, placement: fits ? 'cpu' : 'none', fits, gpuLayers: 0, gpuBytes: 0, cpuBytes: W,
      headroomGB: (b.ram - total) / GB, notes };
  }

  if (b.shared) {
    // Unified memory: spilling past the GPU's share onto CPU threads uses the same RAM, so the ceiling is RAM.
    if (total > b.ram) return { ...base, placement: 'none', fits: false, gpuLayers: 0, gpuBytes: 0, cpuBytes: 0, notes };
    if (hw.gpu.vendor === 'apple') notes.push(`Over macOS's default GPU memory limit (${(b.gpu / GB).toFixed(0)} GB). It can be raised: sudo sysctl iogpu.wired_limit_mb=${Math.floor((b.ram / GB) * 1000)}`);
    else notes.push('Over the GPU memory share; raising it in the BIOS (UMA / dedicated graphics memory) lets it all run on the GPU.');
  }

  // Partial offload. MoE models put their routed experts in RAM first (llama.cpp --n-cpu-moe / -ot exps=CPU, which
  // Ollama and LM Studio also do): attention and shared weights stay on the GPU, and only k/E of the experts are read
  // per token, so the slow pool is touched lightly. Dense models split by whole layers (-ngl).
  const ex = expertParams(model);
  const gpuFixed = KV + BUF; // KV for offloaded layers moves too, but llama.cpp keeps it with the GPU by default
  const avail = b.gpu - gpuFixed;
  if (avail <= 0) {
    const fits = total <= b.ram;
    return { ...base, placement: fits ? 'cpu' : 'none', fits, gpuLayers: 0, gpuBytes: 0, cpuBytes: W, notes };
  }
  let gpuBytes, cpuBytes, gpuLayers;
  if (ex) {
    const expBytes = qn === 'MXFP4' ? (ex * 4.25) / 8 : (W * ex) / model.params_total;
    const rest = W - expBytes;
    if (rest <= avail) {
      gpuBytes = Math.min(W, avail);
      cpuBytes = W - gpuBytes;
      gpuLayers = L;
      notes.push('Keeps attention on the GPU and moves some experts to system RAM (MoE offload).');
    }
  }
  if (gpuBytes == null) {
    const perLayer = W / L;
    gpuLayers = Math.max(0, Math.min(L, Math.floor(avail / perLayer)));
    gpuBytes = gpuLayers * perLayer;
    cpuBytes = W - gpuBytes;
    notes.push(`${gpuLayers} of ${L} layers on the GPU; the rest run from system RAM.`);
  }
  const ramNeed = b.shared ? total : cpuBytes;
  const fits = ramNeed <= b.ram;
  return { ...base, placement: fits ? 'partial' : 'none', fits, gpuLayers, gpuBytes, cpuBytes,
    headroomGB: ((b.shared ? b.ram : b.ram) - ramNeed) / GB, notes };
}

// ── Speed ────────────────────────────────────────────────────────────────────────────────────────────────────────

function kernelFactor(qn) {
  if (qn === 'Q4_0') return CAL.q4_0Kernel;
  return quantSpec(qn)?.kernel ?? 1.1;
}

// speed(model, quant, hardware, opts) → { decodeTps, decodeRange: [lo, hi], prefillTps, bound }.
// opts as fit(); opts.depth is how much of the context is already filled when generating (default: half of it, the
// middle of a typical conversation). The KV cache read at that depth is added to the bytes per token.
export function speed(model, quant, hardware, opts = {}) {
  const hw = hardware.ramGB != null ? hardware : normalizeHardware(hardware);
  const f = opts.fit ?? fit(model, quant, hw, opts);
  const qn = f.quant;
  if (!f.fits) return { decodeTps: 0, decodeRange: [0, 0], prefillTps: 0, bound: 'none' };
  const depth = opts.depth ?? Math.floor(f.context / 2);
  const read = bytesReadPerToken(model, quant);
  const W = weightBytes(model, quant);
  const kvRead = kvBytes(model, depth, f.kvQuant);
  const k = kernelFactor(qn);
  const L = f.layers;
  const calKey = f.backend === 'vulkan' && hw.gpu?.vendor === 'intel' ? 'vulkan-intel' : f.backend;
  const gcal0 = CAL[calKey] ?? CAL.vulkan;
  // Pre-Turing NVIDIA (Pascal, Volta) lacks the int8 tensor paths llama.cpp's CUDA kernels lean on now.
  const gcal = LEGACY_ARCH.has(hw.gpu?.arch) ? { ...gcal0, eta: gcal0.eta * CAL.legacyArch } : gcal0;
  const ccal = CAL.cpu;
  const cpuBW = hw.ramBW;
  const gpuBW = hw.gpu?.bandwidth_gbs ?? cpuBW;
  // Share of the per-token read that lives in each pool. Experts are read k/E as often as dense weights, so a byte
  // of expert in RAM costs less than a byte of attention would.
  let gFrac = 0;
  if (f.placement === 'gpu') gFrac = 1;
  else if (f.placement === 'partial') {
    const ex = expertParams(model);
    if (ex && f.gpuLayers === L) {
      const expBytes = qn === 'MXFP4' ? (ex * 4.25) / 8 : (W * ex) / model.params_total;
      const cpuExpRead = (f.cpuBytes / expBytes) * (expBytes * model.num_experts_per_tok / model.num_experts);
      gFrac = Math.max(0, 1 - cpuExpRead / read);
    } else gFrac = f.gpuBytes / W;
  }
  const readG = read * gFrac, readC = read * (1 - gFrac);
  const kvG = f.placement === 'cpu' ? 0 : kvRead, kvC = f.placement === 'cpu' ? kvRead : 0;
  const tG = gFrac > 0 ? (readG * k + kvG / (gcal.kv ?? 1)) / (gcal.eta * gpuBW * GB) + (L * (f.placement === 'gpu' ? 1 : f.gpuLayers / L) * gcal.layerMs) / 1000 : 0;
  const cpuLayers = f.placement === 'cpu' ? L : f.placement === 'partial' && f.gpuLayers < L ? L - f.gpuLayers : 0;
  const cEta = ccal.eta * (f.placement === 'partial' ? CAL.hybridCpu : 1);
  const tC = readC + kvC > 0 ? (readC * k + kvC) / (cEta * cpuBW * GB) + (cpuLayers * ccal.layerMs) / 1000 : 0;
  // Each pool-to-pool hand-off syncs the devices over PCIe. A dense layer split hands off once per token (~0.5 ms);
  // MoE expert offload hands off twice in every layer whose experts sit in RAM (~0.2 ms per such layer).
  let tX = 0;
  if (f.placement === 'partial' && !hw.gpu?.integrated) {
    if (f.gpuLayers < L) tX = 0.0005;
    else {
      const ex = expertParams(model);
      const expBytes = qn === 'MXFP4' ? (ex * 4.25) / 8 : (W * ex) / model.params_total;
      const moeLayers = L - (num(model.first_k_dense_replace) ?? 0);
      tX = 0.0002 * Math.min(moeLayers, Math.ceil(f.cpuBytes / (expBytes / moeLayers)));
    }
  }
  const t = tG + tC + tX;
  const tps = 1 / t;
  const spread = f.placement === 'gpu' ? gcal.spread : Math.max(gcal.spread, ccal.spread) + 0.1;
  const bound = f.placement === 'gpu' ? 'gpu' : f.placement === 'cpu' ? 'cpu' : 'mixed';

  // Prefill. Compute-bound on the fast device; with weights in RAM, llama.cpp streams them over PCIe once per
  // 512-token micro-batch (~25 GB/s effective on PCIe 4.0 x16), which caps long-prompt speed.
  const P = activeParams(model);
  let pp;
  if (bound === 'cpu' || !hw.gpu) {
    const tf = hw.cpuTflops ?? hw.cpuCores * 0.25; // ~0.25 TFLOPS per performance core (int8 dot-product kernels)
    pp = (ccal.ppEta * tf * 1e12) / (2 * P);
  } else {
    const tf = hw.gpu.fp16_tflops ?? gpuBW / 25; // no figure: bandwidth-scaled guess (≈ consumer cards' ratio)
    pp = (gcal.ppEta * tf * 1e12) / (2 * P);
    if (bound === 'mixed' && !hw.gpu.integrated) pp = 1 / (1 / pp + f.cpuBytes / (25 * GB) / 512);
  }
  return { decodeTps: tps, decodeRange: [tps / (1 + spread), tps * (1 + spread)], prefillTps: pp, bound,
    backend: f.backend, msPerToken: t * 1000 };
}

// ── Verdicts and quant choice ────────────────────────────────────────────────────────────────────────────────────

function ladderFor(model, hw, opts) {
  const isMlx = opts.format === 'mlx';
  const ladder = isMlx ? MLX_LADDER : GGUF_LADDER;
  // If the index lists the quants that actually exist, restrict to those (keeping real sizes).
  const have = (model.quants ?? []).filter((q) => (isMlx ? q.format === 'mlx' : q.format === 'gguf' || !q.format));
  if (have.length) {
    const byName = new Map(have.map((q) => [q.quant, q]));
    const listed = ladder.filter((n) => byName.has(n)).map((n) => byName.get(n));
    if (listed.length) return listed;
  }
  return ladder.filter((n) => n !== 'MXFP4').map((n) => ({ quant: n }));
}

// verdict for one (quant, context) choice, looking at the alternatives when it doesn't fit.
export function assess(model, quant, hardware, opts = {}) {
  const hw = hardware.ramGB != null ? hardware : normalizeHardware(hardware);
  const f = fit(model, quant, hw, opts);
  const s = speed(model, quant, hw, { ...opts, fit: f });
  let verdict;
  const great = opts.reasoning ?? model.reasoning ? THRESHOLDS.greatReasoning : THRESHOLDS.great;
  // An offloaded model can still be "great" (MoE offload often is); `offload` lets the page add "with a catch".
  if (f.fits && s.decodeTps >= great) verdict = 'great';
  else if (f.fits && s.decodeTps >= THRESHOLDS.usable) verdict = 'slow';
  else {
    // Does a smaller quant (not below the beginner floor) or a shorter context (not below 4k) rescue it?
    const ladder = ladderFor(model, hw, { format: quantSpec(f.quant)?.format });
    const q0 = quantSpec(f.quant)?.quality ?? 0;
    const floorQ = Math.min(...Object.values(QUANTS).filter((q) => q.floor).map((q) => q.quality));
    const ctxs = [opts.context ?? 8192, THRESHOLDS.minContext].filter((c, i, a) => a.indexOf(c) === i);
    const rescue = [];
    for (const q of ladder) {
      const qq = quantSpec(q.quant)?.quality ?? 0;
      if (qq > q0 || qq < floorQ) continue;
      for (const c of ctxs) {
        if (q.quant === f.quant && c === (opts.context ?? 8192)) continue;
        const f2 = fit(model, q, hw, { ...opts, context: c });
        const s2 = speed(model, q, hw, { ...opts, context: c, fit: f2 });
        if (f2.fits && s2.decodeTps >= THRESHOLDS.usable) rescue.push({ quant: q.quant, context: c, decodeTps: s2.decodeTps });
      }
    }
    verdict = rescue.length ? 'tight' : 'too-big';
    if (rescue.length) f.notes.push(`Try ${rescue[0].quant} at ${rescue[0].context.toLocaleString('en')} tokens of context.`);
    else if (f.fits) f.notes.push('Fits, but would generate under 1.5 tokens a second.');
    return { verdict, label: verdictLabel(verdict), fit: f, speed: s, rescue, ...flags(f) };
  }
  return { verdict, label: verdictLabel(verdict), fit: f, speed: s, rescue: [], ...flags(f) };
}

// Extra facts the page shows as "with a catch": part of the model in system RAM, or memory nearly full.
function flags(f) {
  const budget = f.placement === 'gpu' ? f.gpuBudgetGB : f.ramBudgetGB;
  const nearlyFull = f.fits && budget > 0 && (f.headroomGB ?? 0) < THRESHOLDS.headroomNote * budget;
  if (nearlyFull) f.notes.push('Only just fits: close other apps (browsers especially) before loading it.');
  return { offload: f.placement === 'partial' || f.placement === 'cpu', nearlyFull };
}

// bestQuant(model, hardware, opts) → the quant we would tell a beginner to download, with its fit and speed.
// Policy: the highest-quality quant that runs great entirely on the fast pool with 10% headroom; quality above
// Q6_K is only chosen for models under 10B parameters (small models lose more to quantisation, big ones barely
// notice: see fit.md). If nothing runs great, the best quant at or below Q4_K_M that runs at all, because then
// every token counts. null if nothing fits.
export function bestQuant(model, hardware, opts = {}) {
  const hw = hardware.ramGB != null ? hardware : normalizeHardware(hardware);
  const ladder = ladderFor(model, hw, opts);
  const big = (num(model.params_total) ?? 0) >= 10e9;
  const results = ladder.map((q) => ({ q, a: assess(model, q, hw, opts) }));
  const ok = (r) => {
    if (big && (r.q.quant === 'Q8_0' || r.q.quant === 'mlx-8bit')) return false;
    return r.a.verdict === 'great' && r.a.fit.placement === 'gpu' && r.a.fit.headroomGB >= 0.1 * r.a.fit.totalGB;
  };
  const capped = (r) => !(big && (r.q.quant === 'Q8_0' || r.q.quant === 'mlx-8bit'));
  const floorQ = Math.min(...Object.values(QUANTS).filter((q) => q.floor).map((q) => q.quality));
  const quality = (r) => quantSpec(r.q.quant)?.quality ?? 0;
  const aboveFloor = (r) => quality(r) >= floorQ;
  // When nothing runs great, speed matters more than the last few points of quality: stay at Q4_K_M or below.
  const q4 = QUANTS.Q4_K_M.quality;
  const pick = results.find(ok)
    ?? results.find((r) => r.a.verdict === 'great' && capped(r) && aboveFloor(r))
    ?? results.find((r) => r.a.verdict === 'slow' && quality(r) <= q4 && aboveFloor(r))
    ?? results.find((r) => (r.a.verdict === 'great' || r.a.verdict === 'slow'));
  if (!pick) return null;
  // belowFloor: the only thing that runs is under the beginner floor (Q3_K_M / IQ3_M), where quality drops
  // noticeably. We still return it (the expert view can show it) but the verdict becomes 'tight': it "fits only
  // with a smaller quant" than we would recommend, and the page should suggest a smaller model instead.
  const belowFloor = !aboveFloor(pick);
  const verdict = belowFloor ? 'tight' : pick.a.verdict;
  if (belowFloor) pick.a.fit.notes.push(`Only fits at ${pick.q.quant}, below the quality we recommend; a smaller model will answer better.`);
  return { quant: pick.q.quant, bytes: weightBytes(model, pick.q), belowFloor, ...pick.a, verdict, label: verdictLabel(verdict) };
}
