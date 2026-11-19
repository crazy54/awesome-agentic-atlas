// hardware.mjs: reading the hardware catalogue (hardware.json) for the local-AI page.
//
// Owner: ds-hardware. Contract: team/contracts/hardware.md. Dependency-free ES module of pure functions (plus one
// browser-only function, detectHints), the same in the browser and in Node. Tests: `node test.mjs` in this folder.
//
// What it does, in the order the page uses it:
//   search(cat, query, {tile})      the fuzzy "type your model" picker
//   popular(cat, tile)              the preset chips under the picker
//   memoryChoices(cat, id)          the memory chips ("8 · 16 · 24 GB") and whether we also need system RAM
//   toMachine(cat, selection)       the one object ds-models' fit.mjs reads (normalizeHardware's input), with the
//                                   GPU's share of shared memory worked out by the platform rule
//   detectHints()                   what the browser lets us guess, as suggestions for the user to confirm
//
// The catalogue's memory sizes are the marketed numbers, which are binary (a "16 GB" Mac has 16 GiB). toMachine()
// passes them on unchanged in *_gb (so the page can say "16 GB") and exactly in *_bytes, which is what the fit maths
// should compare model files (decimal bytes) against. Bandwidth is decimal GB/s, as vendors publish it.

export const GIB = 2 ** 30;

// The backends fit.mjs knows how to speed-estimate. Others in the catalogue (opencl, npu, cpu) are informational.
const FIT_BACKENDS = ['cuda', 'rocm', 'vulkan', 'sycl', 'metal', 'mlx'];

const byId = new WeakMap();
export function device(cat, id) {
  if (id && typeof id === 'object') return id;
  let m = byId.get(cat);
  if (!m) { m = new Map(cat.devices.map((d) => [d.id, d])); byId.set(cat, m); }
  return m.get(id) ?? null;
}

// ── Search ───────────────────────────────────────────────────────────────────────────────────────────────────────────
//
// People type "4090", "rtx 4070 laptop", "mba m2", "M3 Max 36GB", "deck oled", "legion go". We normalise case,
// trademark marks and filler words, pull a memory size out of the query, and score every alias:
//   exact (ignoring spaces) 100 · alias starts with the query 80 · every query word starts a word of the alias 60–70 ·
//   alias contains the query 50 · one-typo match on a word of four letters or more 30–45.
// Numbers must match exactly ("4060" never matches "4070"). Then small nudges: the memory size the user typed is (or
// isn't) one of the entry's options, laptop words in the query, the tile, and popularity as the tie-breaker.

const FILLER = /\b(nvidia|geforce|amd|apple|intel|the|my|a|graphics card|gpu|card|with|and|of|ram|memory|unified)\b/g;

export function normalize(s) {
  return String(s ?? '').toLowerCase()
    .replace(/\(tm\)|\(r\)|™|®/g, ' ')
    .replace(/["'’`]/g, '')
    .replace(/[_/,+()\[\]:;|]/g, ' ')
    .replace(/-/g, ' ')
    .replace(FILLER, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}
const compact = (s) => s.replace(/\s+/g, '');

// "m3 max 36gb" → { text: "m3 max", memory_gb: 36 }. Accepts "36gb", "36 gb", "36g", "36 gig".
export function parseQuery(query) {
  let q = String(query ?? '').toLowerCase();
  let memory_gb = null;
  const m = /(?:^|\s)(\d{1,3})\s*(?:gb|g|gig|gigs)\b/.exec(q);
  if (m) { memory_gb = Number(m[1]); q = q.replace(m[0], ' '); }
  const laptop = /\b(laptop|mobile|notebook|max ?q)\b|\b\d{3,4}m\b/.test(q);
  const desktop = /\bdesktop\b/.test(q);
  q = q.replace(/\b(laptop|notebook|desktop)\b/g, (w) => (w === 'notebook' ? 'laptop' : w));
  return { text: normalize(q), memory_gb, laptop, desktop };
}

function editDistanceAtMost1(a, b) {
  if (a === b) return true;
  if (Math.abs(a.length - b.length) > 1) return false;
  let i = 0, j = 0, edits = 0;
  while (i < a.length && j < b.length) {
    if (a[i] === b[j]) { i++; j++; continue; }
    if (++edits > 1) return false;
    if (a.length > b.length) i++; else if (b.length > a.length) j++; else { i++; j++; }
  }
  return edits + (a.length - i) + (b.length - j) <= 1;
}

function aliasScore(qText, alias) {
  const a = normalize(alias);
  if (!a || !qText) return 0;
  const qc = compact(qText), ac = compact(a);
  if (qc === ac) return 100;
  // A prefix only counts if it doesn't cut a number in half ("406" must not match "4060").
  if (ac.startsWith(qc) && !(/\d$/.test(qc) && /^\d/.test(ac.slice(qc.length)))) {
    return 80 - Math.min(20, (ac.length - qc.length) * 0.5);
  }
  const qt = qText.split(' '), at = a.split(' ');
  const starts = qt.filter((t) => at.some((w) => w === t || (!/^\d+$/.test(t) && w.startsWith(t)))).length;
  if (starts === qt.length) return 60 + 10 * (qt.length / at.length);
  // The query says more than the alias: "ryzen 7 7840u" contains the alias "7840u". Only for aliases with a number
  // or two words, so a bare word like "ally" doesn't claim every query that mentions it.
  if (at.every((w) => qt.includes(w)) && (at.length >= 2 || /\d/.test(a))) return 55 + 10 * (at.length / qt.length);
  if (qc.length >= 4 && ac.includes(qc) && !/\d/.test(ac[ac.indexOf(qc) + qc.length] ?? '') && !/\d/.test(ac[ac.indexOf(qc) - 1] ?? '')) return 50;
  // Typos: every query word matches some alias word exactly, by prefix, or within one edit (alphabetic words ≥ 4).
  let fuzzy = 0;
  for (const t of qt) {
    if (at.some((w) => w === t || (!/^\d+$/.test(t) && w.startsWith(t)))) { fuzzy += 1; continue; }
    if (t.length >= 4 && !/\d/.test(t) && at.some((w) => w.length >= 4 && editDistanceAtMost1(t, w))) { fuzzy += 0.75; continue; }
    return 0;
  }
  return 30 + 15 * (fuzzy / qt.length) * (qt.length / at.length);
}

export function search(cat, query, { tile = null, limit = 8 } = {}) {
  const q = parseQuery(query);
  if (!q.text) return [];
  const results = [];
  for (const d of cat.devices) {
    let best = 0;
    for (const s of [d.name, d.short, ...(d.aliases ?? [])]) best = Math.max(best, aliasScore(q.text, s));
    if (best <= 0) continue;
    let score = best;
    const opts = d.memory?.options_gb ?? [];
    if (q.memory_gb != null) score += opts.includes(q.memory_gb) ? 8 : d.kind === 'cpu' ? 0 : -15;
    const isLaptop = d.form === 'laptop' || (d.tiles?.length === 1 && d.tiles[0] === 'laptop' && d.kind === 'gpu');
    if (q.laptop) score += isLaptop ? 10 : d.kind === 'gpu' ? -10 : 0;
    else if (isLaptop && tile !== 'laptop') score -= 8;
    if (q.desktop && isLaptop) score -= 10;
    if (tile) score += d.tiles?.includes(tile) ? 4 : -25;
    score += (d.popularity?.tier ?? 1) * 1.5 + Math.min(4, d.popularity?.steam_share_pct ?? 0) * 0.5
      + Math.max(0, (d.release_year ?? 2015) - 2015) * 0.05; // newer first, as a last tie-breaker
    results.push({ id: d.id, name: d.name, kind: d.kind, tiles: d.tiles, score: Math.round(score * 10) / 10,
      memory_gb: q.memory_gb != null && opts.includes(q.memory_gb) ? q.memory_gb : null });
  }
  results.sort((a, b) => b.score - a.score || a.name.localeCompare(b.name));
  return results.slice(0, limit);
}

// ── Presets and memory choices ──────────────────────────────────────────────────────────────────────────────────────

export function popular(cat, tile) {
  return cat.presets.filter((p) => !tile || p.tile === tile || device(cat, p.device)?.tiles?.includes(tile));
}

export const SYSTEM_RAM_OPTIONS = [8, 16, 32, 48, 64, 96, 128, 192, 256];

// What to ask after the device: its memory options, and whether we also need the machine's system RAM (a graphics
// card has its own VRAM; the rest of the PC's memory is separate and matters for offload).
export function memoryChoices(cat, id) {
  const d = device(cat, id);
  if (!d) return null;
  const m = d.memory ?? {};
  const vram = m.kind === 'vram';
  return {
    label: vram ? 'Graphics memory (VRAM)' : m.kind === 'system' ? 'Memory (RAM)' : 'Memory',
    options_gb: [...(m.options_gb ?? [])].sort((a, b) => a - b),
    default_gb: m.default_gb ?? m.options_gb?.[0] ?? null,
    ask: (m.options_gb?.length ?? 0) > 1,
    needs_system_ram: vram && !d.system_ram,
    system_ram: d.system_ram ?? (vram ? { options_gb: SYSTEM_RAM_OPTIONS, default_gb: 16 } : null),
    // Shared-memory chips sold with either socketed DDR5 or soldered LPDDR5X: offer the kinds, fastest last.
    memory_kinds: m.kinds ?? null,
    needs_ram_kind: d.kind === 'cpu',
  };
}

// For a Mac product, the memory option picks the chip bin (M3 Max 36 GB is the 30-core, 300 GB/s part).
export function resolveChip(cat, id, memory_gb) {
  const d = device(cat, id);
  if (!d) return null;
  if (d.configs?.length) {
    const c = d.configs.find((x) => x.memory_gb === memory_gb) ?? d.configs[0];
    return device(cat, c.chip);
  }
  return d;
}

// ── GPU share of shared memory: the platform rules ──────────────────────────────────────────────────────────────────

// Apple's default Metal working set: 2/3 of RAM up to 32 GB, 3/4 from 36 GB (every logged datapoint, macOS 13–15).
// With opts.macos26, the larger shares logged on macOS 26, interpolated by RAM.
export function appleGpuShareGB(ramGB, { macos26 = false } = {}) {
  if (macos26) {
    const t = [[8, 0.667], [16, 0.74], [24, 0.74], [32, 0.78], [48, 0.78], [64, 0.81], [128, 0.84], [512, 0.906]];
    let f = t[0][1];
    for (let i = 0; i < t.length; i++) {
      if (ramGB >= t[i][0]) f = t[i][1];
      if (i + 1 < t.length && ramGB > t[i][0] && ramGB < t[i + 1][0]) {
        f = t[i][1] + (t[i + 1][1] - t[i][1]) * (ramGB - t[i][0]) / (t[i + 1][0] - t[i][0]);
        break;
      }
    }
    return ramGB * f;
  }
  return ramGB <= 32 ? ramGB * (2 / 3) : ramGB * 0.75;
}

// Returns { gb, raised_gb, rule, raise } for an integrated GPU, or null for discrete / CPU-only.
export function gpuShare(cat, d, ramGB, os, { macos26 = false } = {}) {
  const ruleId = d.memory?.gpu_share;
  if (!ruleId) return null;
  const rule = cat.platform_rules[ruleId];
  const win = os === 'windows';
  switch (ruleId) {
    case 'apple-metal': {
      const headroom = Math.max(4, 0.12 * ramGB);
      return { gb: appleGpuShareGB(ramGB, { macos26 }), raised_gb: ramGB - headroom, rule: ruleId,
        raise: { how: rule.raise.note, command: rule.raise.command.replace('{mb}', String(Math.floor((ramGB - headroom) * 1024))) } };
    }
    case 'amd-halo':
      return { gb: ramGB * 0.5, raised_gb: win ? ramGB * rule.raised.windows_fraction : ramGB - rule.raised.linux_reserve_gb,
        rule: ruleId, raise: { how: win ? rule.raise.windows : rule.raise.linux } };
    case 'amd-apu': {
      const max = d.gpu_memory?.max_gb;
      return { gb: ramGB * 0.5, raised_gb: win && max ? Math.max(ramGB * 0.5, max) : null, rule: ruleId,
        raise: { how: win ? (d.gpu_memory?.setting ?? rule.raise.windows) : rule.raise.linux } };
    }
    case 'steam-deck':
      return { gb: rule.fixed_gb, raised_gb: null, rule: ruleId, raise: null };
    case 'intel-igpu':
    case 'windows-shared':
      return { gb: ramGB * rule.default_fraction, raised_gb: null, rule: ruleId, raise: rule.raise ? { how: rule.raise.windows } : null };
    case 'nvidia-unified-linux':
      return { gb: ramGB, raised_gb: null, rule: ruleId, raise: null };
    default:
      return null;
  }
}

// ── toMachine ────────────────────────────────────────────────────────────────────────────────────────────────────────
//
// selection: {
//   device:     catalogue id (or entry): a GPU, a chip, a system, or 'cpu-only'
//   memory_gb:  the device's memory option (VRAM for a GPU; RAM for a Mac, handheld, APU)
//   ram_gb:     system RAM, for a discrete GPU (or 'cpu-only')
//   ram_kind:   a ram_kinds id ('ddr5-5600-2ch'), or a memory.kinds type ('LPDDR5X-7500') for shared-memory chips
//   os:         'windows' | 'linux' | 'macos' | 'steamos' (default: the device's first OS)
//   ram_sticks: 1 or 2+ (optional): one stick = single channel, half the bandwidth
//   gpus:       extra discrete GPUs [{ device, memory_gb, count }] for multi-GPU rigs
//   raised:     true if the user has raised the GPU share (Mac sysctl, AMD VGM, ttm.pages_limit); default false
//   macos26:    true to use macOS 26's larger default GPU share
// }
// Returns the object fit.mjs's normalizeHardware() reads, plus exact byte counts and the notes the page shows.
export function toMachine(cat, sel) {
  const d0 = device(cat, sel.device);
  if (!d0) throw new Error(`unknown device ${sel.device}`);
  const notes = [];
  const memGB = sel.memory_gb ?? d0.memory?.default_gb;
  const chip = resolveChip(cat, d0, memGB) ?? d0;
  const d = d0.kind === 'system' && d0.configs ? chip : d0;
  const os = sel.os ?? d0.os?.[0] ?? 'windows';
  const ramKinds = new Map(cat.ram_kinds.map((r) => [r.id, r]));

  const backendsFor = (entry) => {
    const b = entry.backends ?? {};
    const key = (per) => per[os] ?? (os === 'steamos' ? per.linux : undefined);
    return Object.keys(b).filter((k) => FIT_BACKENDS.includes(k) && key(b[k]) && key(b[k]) !== 'no');
  };
  const gpuOf = (entry, vramGB, integrated, bw) => ({
    vendor: entry.gpu.vendor,
    name: entry.gpu.name ?? entry.name,
    integrated,
    vram_gb: integrated ? null : vramGB,
    vram_bytes: integrated ? null : vramGB * GIB,
    vram_bandwidth_gbs: bw,
    fp16_tflops: entry.gpu.fp16_tflops ?? null,
    arch: entry.gpu.arch ?? null,
    backends: backendsFor(entry),
  });

  let m;
  const isDiscrete = d.memory?.kind === 'vram';
  if (isDiscrete || d.kind === 'cpu') {
    // A graphics card (or nothing) plus the PC's own RAM.
    const ramGB = sel.ram_gb ?? (d.kind === 'cpu' ? sel.memory_gb : null) ?? d.system_ram?.default_gb ?? 16;
    const year = d.release_year ?? 2023;
    const kindId = sel.ram_kind ?? d.system_ram?.ram_kind ?? (year >= cat.ram_defaults.cutoff_year ? cat.ram_defaults.new : cat.ram_defaults.old);
    // "How many RAM sticks?" (ds-app's optional question): one stick is one channel, which halves bandwidth.
    let kindIdFinal = kindId;
    if (sel.ram_sticks === 1 && /-2ch$/.test(kindId)) kindIdFinal = kindId.replace(/-2ch$/, '-1ch');
    if (sel.ram_sticks >= 2 && /-1ch$/.test(kindId)) kindIdFinal = kindId.replace(/-1ch$/, '-2ch');
    const rk = ramKinds.get(kindIdFinal);
    if (!sel.ram_kind) notes.push(`Assumed ${rk.label} for the main memory.`);
    const gpus = [];
    if (isDiscrete) {
      const vram = memGB;
      gpus.push(gpuOf(d, vram, false, d.memory.bandwidth_gbps));
      for (const extra of sel.gpus ?? []) {
        const e = device(cat, extra.device);
        if (!e || e.memory?.kind !== 'vram') continue;
        for (let i = 0; i < (extra.count ?? 1); i++) gpus.push(gpuOf(e, extra.memory_gb ?? e.memory.default_gb, false, e.memory.bandwidth_gbps));
      }
    }
    m = {
      unified: false, ram_gb: ramGB, ram_bytes: ramGB * GIB, ram_bandwidth_gbs: rk.bandwidth_gbps, ram_kind: kindIdFinal,
      gpus, gpu_usable_gb: null, gpu_usable_bytes: null, gpu_usable_raised_gb: null, can_raise: false,
    };
    if (d.memory?.bandwidth_assumed) notes.push('This machine’s graphics memory speed is unpublished, so its speed estimate is rough.');
  } else {
    // One memory pool shared by processor and graphics: Macs, APUs, handhelds, Spark, Jetson.
    const ramGB = memGB;
    let bw = d0.kind === 'system' && !d0.configs ? d0.memory.bandwidth_gbps : d.memory.bandwidth_gbps;
    const byOpt = d.memory?.bandwidth_by_option_gbps;
    if (byOpt && byOpt[String(ramGB)]) bw = byOpt[String(ramGB)];
    if (sel.ram_kind) {
      const k = (d.memory.kinds ?? []).find((x) => x.type === sel.ram_kind) ?? ramKinds.get(sel.ram_kind);
      if (k) bw = k.bandwidth_gbps;
    }
    const useGpu = d.gpu && d.gpu.use_for_ai !== false && (d0.memory?.gpu_share ?? d.memory?.gpu_share);
    const shareSrc = d0.memory?.gpu_share ? d0 : d;
    const share = useGpu ? gpuShare(cat, shareSrc, ramGB, os, { macos26: sel.macos26 }) : null;
    const usable = share ? (sel.raised && share.raised_gb ? share.raised_gb : share.gb) : null;
    if (share?.raise && !sel.raised) notes.push(share.raise.command
      ? `The graphics side can use about ${usable.toFixed(1)} GB by default. To give it more: ${share.raise.command} (${share.raise.how})`
      : `The graphics side can use about ${usable.toFixed(1)} GB by default. To give it more: ${share.raise.how}`);
    m = {
      unified: Boolean(useGpu), ram_gb: ramGB, ram_bytes: ramGB * GIB, ram_bandwidth_gbs: bw, ram_kind: sel.ram_kind ?? null,
      gpus: useGpu ? [gpuOf(d0.kind === 'system' && !d0.configs ? d0 : d, null, true, bw)] : [],
      gpu_usable_gb: usable != null ? Math.round(usable * 100) / 100 : null,
      gpu_usable_bytes: usable != null ? Math.round(usable * GIB) : null,
      gpu_usable_raised_gb: share?.raised_gb != null ? Math.round(share.raised_gb * 100) / 100 : null,
      // The page shows the "I've raised the limit" toggle only when raising changes something.
      can_raise: share?.raised_gb != null && share.raised_gb > share.gb + 0.01,
      gpu_share_rule: share?.rule ?? null,
    };
  }
  const cpu = { ...(d0.cpu ?? d.cpu ?? {}) };
  const label = d0.kind === 'gpu'
    ? `${d0.short}${(d0.memory.options_gb.length > 1) ? ` ${memGB} GB` : ''} + ${m.ram_gb} GB RAM`
    : `${d0.short ?? d0.name}, ${m.ram_gb} GB`;
  return {
    id: d0.id, name: d0.name, label, chip: d !== d0 ? d.id : (d0.chip ?? null), os,
    ...m,
    gpu: m.gpus[0] ?? null,
    cpu,
    notes: [...notes, ...(d0.notes ?? []), ...(d !== d0 ? (d.notes ?? []) : [])],
    confidence: [d0.confidence, d.confidence].includes('low') ? 'low' : [d0.confidence, d.confidence].includes('medium') ? 'medium' : 'high',
  };
}

// ── Browser hints ───────────────────────────────────────────────────────────────────────────────────────────────────
//
// What a browser honestly tells us (researched 2026-11-18; sources in hardware.md §5):
// - WebGL UNMASKED_RENDERER_WEBGL names the GPU in Chrome/Edge only: "ANGLE (NVIDIA, NVIDIA GeForce RTX 4060 Laptop
//   GPU (0x000028E0) Direct3D11 vs_5_0 ps_5_0, D3D11)" on Windows, "ANGLE (Apple, ANGLE Metal Renderer: Apple M1 Pro,
//   …)" on a Mac. Safari always says "Apple GPU". Firefox substitutes a representative bucket ending ", or similar",
//   which must never be read as the real model.
// - WebGPU adapter.info gives vendor and architecture only (Chrome), nothing (Firefox), or the first word of the GPU
//   name (Safari). It never gives memory.
// - navigator.deviceMemory (Chromium only) is rounded down at ties and capped: 2/4/8/16/32 from Chrome 147, 8 before.
// - No browser API reports VRAM.
// So every hint is a suggestion the user confirms, and nothing is sent anywhere.

// Parses a WebGL renderer string. Returns { text, vendor, bucketed, generic, pci, steamDeck } where text is the GPU
// name to search for (or null).
export function parseRenderer(raw) {
  const s = String(raw ?? '').trim();
  const out = { raw: s, text: null, vendor: null, bucketed: false, generic: false, pci: null, steamDeck: null };
  if (!s) return out;
  if (/,? or similar$/i.test(s) || /^Generic Renderer$/i.test(s)) { out.bucketed = true; }
  if (/^Apple GPU$/i.test(s)) { out.vendor = 'apple'; out.generic = true; return out; }
  let inner = s;
  const angle = /^ANGLE \(([^,]+),\s*(.+?)(?:,\s*[^,]*)?\)(?:,? or similar)?$/i.exec(s);
  if (angle) { out.vendor = angle[1].trim().toLowerCase(); inner = angle[2]; }
  const pci = /\(0x([0-9a-f]{4,8})\)/i.exec(inner);
  if (pci) out.pci = pci[1].toLowerCase().replace(/^0000/, '');
  inner = inner.replace(/ANGLE Metal Renderer:\s*/i, '')
    .replace(/\(0x[0-9a-f]+\)/ig, '')
    .replace(/Direct3D1[01].*$/i, '')
    .replace(/OpenGL.*$|Vulkan.*$|\(LLVM.*$|, Unspecified Version.*$|, Version .*$/i, '')
    .replace(/\(TM\)|\(R\)/gi, '')
    .replace(/\s+/g, ' ').trim();
  const deck = /custom (?:gpu|apu) (0405|0932)|vangogh/i.exec(s);
  if (deck) out.steamDeck = deck[1] === '0932' ? 'steam-deck-oled' : deck[1] === '0405' ? 'steam-deck-lcd' : 'steam-deck';
  if (!out.vendor) out.vendor = /nvidia|geforce/i.test(inner) ? 'nvidia' : /amd|radeon/i.test(inner) ? 'amd' : /intel/i.test(inner) ? 'intel' : /apple/i.test(inner) ? 'apple' : null;
  if (!out.bucketed && inner && !/^(AMD Radeon Graphics|Radeon Graphics|Intel Graphics|Mesa|llvmpipe|SwiftShader|Microsoft Basic Render)/i.test(inner)) out.text = inner;
  if (out.bucketed) out.text = null;
  return out;
}

// Turns a parsed renderer (plus OS) into ranked catalogue candidates. Pure, so it can be tested in Node.
export function hintCandidates(cat, parsed, { os = null } = {}) {
  if (parsed.steamDeck) {
    const ids = parsed.steamDeck === 'steam-deck' ? ['steam-deck-lcd', 'steam-deck-oled'] : [parsed.steamDeck];
    return ids.map((id) => ({ id, name: device(cat, id).name, confidence: ids.length === 1 ? 'likely' : 'maybe' }));
  }
  if (!parsed.text) return [];
  const tile = parsed.vendor === 'apple' || os === 'macos' ? 'mac' : null;
  const res = search(cat, parsed.text, { tile, limit: 3 }).filter((r) => r.score >= 55);
  return res.map((r, i) => ({ id: r.id, name: r.name, confidence: i === 0 && r.score >= 95 ? 'likely' : 'maybe' }));
}

// deviceMemory → what it can honestly mean. The spec rounds to a power of two (ties round down) and Chrome caps it.
export function ramHint(deviceMemory, chromeMajor = null) {
  if (typeof deviceMemory !== 'number' || !(deviceMemory > 0)) return null;
  const cap = chromeMajor != null && chromeMajor < 147 ? 8 : 32;
  if (deviceMemory >= cap) return { hint_gb: deviceMemory, meaning: `at least ${deviceMemory} GB`, at_least: deviceMemory };
  return { hint_gb: deviceMemory, meaning: `about ${deviceMemory} GB (it could be up to ${deviceMemory * 1.5} GB: browsers round down)`, at_least: deviceMemory };
}

export function osFromUA(ua, platform) {
  const p = String(platform ?? '').toLowerCase(), u = String(ua ?? '');
  if (p.includes('win') || /Windows NT/.test(u)) return 'windows';
  if (p.includes('mac') || /Mac OS X|Macintosh/.test(u)) return 'macos';
  if (p.includes('chrome os') || /CrOS/.test(u)) return 'chromeos';
  if (p.includes('linux') || /Linux|X11/.test(u)) return 'linux';
  return null;
}

// Browser only. Never throws, never prompts, sends nothing. Returns hints for the page to offer, not answers.
export async function detectHints(cat, env = globalThis) {
  const nav = env.navigator ?? {};
  const out = { os: null, arch: null, windows11: null, gpu: null, ram: null, cores: null, sources: [], notes: [] };
  try {
    out.os = osFromUA(nav.userAgent, nav.userAgentData?.platform ?? nav.platform);
    if (nav.userAgentData?.getHighEntropyValues) {
      const h = await nav.userAgentData.getHighEntropyValues(['architecture', 'bitness', 'platformVersion']);
      out.arch = h.architecture || null;
      if (out.os === 'windows' && h.platformVersion) out.windows11 = Number(h.platformVersion.split('.')[0]) >= 13;
      out.sources.push('ua-ch');
    }
  } catch { /* UA-CH can be blocked by permissions policy */ }
  let renderer = null;
  try {
    const canvas = env.document?.createElement('canvas');
    const gl = canvas?.getContext('webgl') ?? canvas?.getContext('experimental-webgl');
    const ext = gl?.getExtension('WEBGL_debug_renderer_info');
    if (ext) renderer = gl.getParameter(ext.UNMASKED_RENDERER_WEBGL);
  } catch { /* WebGL off */ }
  let adapter = null;
  try {
    const a = await nav.gpu?.requestAdapter?.({ powerPreference: 'high-performance' });
    if (a?.info) adapter = { vendor: a.info.vendor || null, architecture: a.info.architecture || null };
  } catch { /* WebGPU off */ }
  const parsed = parseRenderer(renderer);
  if (parsed.steamDeck) out.os = 'steamos';
  const candidates = hintCandidates(cat, parsed, { os: out.os });
  out.gpu = { text: parsed.text, vendor: parsed.vendor ?? adapter?.vendor ?? null, architecture: adapter?.architecture ?? null,
    bucketed: parsed.bucketed, generic: parsed.generic, candidates };
  if (renderer) out.sources.push('webgl');
  if (adapter) out.sources.push('webgpu');
  if (parsed.bucketed) out.notes.push('Your browser hides the exact graphics chip (Firefox does this for privacy), so we can’t guess it.');
  if (parsed.generic && parsed.vendor === 'apple') out.notes.push('Safari doesn’t say which Apple chip this is. About This Mac does.');
  if (out.os === 'windows' && candidates.length && /intel|radeon(?! rx)/i.test(parsed.text ?? '')) {
    out.notes.push('Laptops with two graphics chips often show the built-in one here. Check Task Manager for a GeForce or Radeon RX.');
  }
  if (out.os === 'macos' && out.arch === 'x86') out.notes.push('This looks like an Intel Mac: local AI runs only on the processor there.');
  const chromeMajor = Number((/Chrom(?:e|ium)\/(\d+)/.exec(nav.userAgent ?? '') ?? [])[1]) || null;
  out.ram = ramHint(nav.deviceMemory, chromeMajor);
  if (out.ram) out.sources.push('deviceMemory');
  if (typeof nav.hardwareConcurrency === 'number') out.cores = nav.hardwareConcurrency;
  return out;
}
