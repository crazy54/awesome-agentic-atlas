/* The local-AI page's behaviour. Written into docs/local/index.html by scripts/32_local.py, after the
   `lxdata` JSON block and the two vendored modules it reads: LOCALFIT (ds-models' scripts/localfit.mjs) and
   LOCALHW (ds-hardware's scripts/localhw.mjs), both wrapped by that stage.

   Two halves. `LOCALUI` is pure: search, the machine a set of answers describes, the model the fit method
   is handed, the verdicts, the words a reader is shown, the commands, and the URL hash. Each is a function of
   its arguments and the inlined data, which is what lets tests/local-check.mjs assert them directly as well
   as through the DOM. The bottom half wires them to the page and owns all the state.

   No arithmetic about memory or speed lives in this file, and no knowledge of hardware either. Every number
   on a card comes from LOCALFIT -- `bestQuant()`, `assess()`, `fit()`, `budgets()` -- and every machine from
   LOCALHW -- `search()`, `popular()`, `memoryChoices()`, `toMachine()`, `detectHints()`. This file only
   decides which words go round them.

   Every answer lives in the hash (`#d=steam-deck-oled&t=code`), so a result can be sent to a friend and
   reproduces exactly, and a reload keeps your place. `history.replaceState` rather than push: each click
   is a refinement of one question, not a new page, and twenty back presses to leave would be a trap. */
const LOCALUI = ((D, FIT, HW) => {
  const byId = (xs) => Object.fromEntries(xs.map((x) => [x.id, x]));
  const CAT = D.cat, DEV = byId(CAT.devices), PICK = byId(D.models), TILE = byId(CAT.tiles);
  const GB = 1e9;
  const esc = (s) => String(s === null || s === undefined ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#x27;");
  // One decimal under ten, whole numbers above: "5.6 GB", "19 GB". The precision a reader can use.
  const gb = (x) => (x < 10 ? (Math.round(x * 10) / 10).toFixed(1) : String(Math.round(x)));

  // Search is ds-hardware's (`search()`: aliases, one forgiven typo, memory sizes read out of the query,
  // laptop words, popularity), so nothing here second-guesses it. A query that finds nothing -- a laptop
  // brand like "ThinkPad", which names no chip -- is answered with the way forward, not an empty list.
  const search = (q, tile) => HW.search(CAT, q, {tile, limit: 8});

  // The operating system the browser is running on, as the catalogue spells it. A guess for defaults only;
  // the how-to panel always lets the reader pick another.
  const uaOS = (ua) => HW.osFromUA(ua) || "windows";

  // The machine a set of answers describes, or null if there is not one yet: ds-hardware's `toMachine()`,
  // which is exactly what fit.mjs reads, plus its label, notes and confidence for the page. A memory option
  // the device does not have is dropped rather than obeyed, so a hand-edited link cannot invent a machine.
  const choices = (id) => (DEV[id] ? HW.memoryChoices(CAT, id) : null);
  const machineOf = (s) => {
    if (!s.d || !DEV[s.d]) return null;
    const c = choices(s.d), d = DEV[s.d];
    const mem = c.options_gb.includes(s.mem) ? s.mem : c.default_gb;
    const sys = c.system_ram || null;
    const ram = sys && sys.options_gb.includes(s.ram) ? s.ram : undefined;
    const hw = HW.toMachine(CAT, {device: s.d, memory_gb: mem, ram_gb: ram, ram_kind: s.rk || undefined,
                                  ram_sticks: s.rs || undefined});
    return {name: hw.label, device: d, tile: s.k, os: hw.os, hw, choices: c, mem,
            approx: hw.confidence !== "high", sticks: d.kind === "gpu" || d.kind === "cpu"};
  };
  const apple = (mc) => !!(mc.hw.gpu && mc.hw.gpu.vendor === "apple");
  // The how-to steps' OS for a machine: its own, except ChromeOS, whose Linux container is Linux to every
  // runner the page names.
  const howtoOS = (os) => (os === "chromeos" ? "linux" : os);

  // One sentence on what this machine offers, so every "you have X GB" below has been explained once.
  const machineWords = (mc) => {
    const h = FIT.normalizeHardware(mc.hw), b = FIT.budgets(h), name = esc(mc.device.short || mc.device.name);
    const g = b.gpu / GB, r = b.ram / GB;
    if (apple(mc))
      return `Your ${name} has <b>${h.ramGB} GB</b> of memory, shared by the processor and graphics. ` +
        `macOS lets AI use about <b>${gb(g)} GB</b> of it on the graphics and keeps the rest for itself and your apps.`;
    if (h.gpu && h.gpu.integrated)
      return `Your ${name} shares <b>${h.ramGB} GB</b> between the processor and graphics. About ` +
        `<b>${gb(g)} GB</b> can go to the graphics, where AI runs fastest, once the system has its share.`;
    if (h.gpu)
      return `Your graphics card has <b>${h.gpu.vram_gb} GB</b> of its own memory (about <b>${gb(g)} GB</b> ` +
        `usable), and that's where AI runs fast. Your <b>${h.ramGB} GB</b> of RAM can hold overflow ` +
        `(about ${gb(r)} GB), but much more slowly.`;
    return `No separate graphics card, so AI runs on the processor using your <b>${h.ramGB} GB</b> of RAM. ` +
      `About <b>${gb(r)} GB</b> is free for it. It works, just more slowly than on a graphics card.`;
  };

  // The model the fit method is handed for a pick: eng-hf's index row when it has one (real file sizes, read
  // by ds-models' `normalizeModel()`), otherwise the pick's own fit-ready `model`. Cached: a model is the same
  // object for every machine.
  const HF = D.hf && D.hf.rows ? Object.fromEntries(D.hf.rows.map((r) => {
    const o = Object.fromEntries(D.hf.cols.map((c, i) => [c, r[i]])); return [o.id, o]; })) : {};
  const models = {};
  const modelOf = (p) => {
    if (models[p.id]) return models[p.id];
    const row = HF[p.id];
    const base = row ? FIT.normalizeModel(row, D.hf.variant_cols, D.hf.file_cols) : null;
    return (models[p.id] = base && base.quants.length ? Object.assign(base, {id: p.id}) : p.model);
  };
  const ggufs = (m) => m.quants.filter((q) => !q.format || q.format === "gguf");

  // One pick on one machine: the quant ds-models' policy recommends (or the one the reader forced), and
  // everything the card prints about it. `file` is the quant's own entry, for its label, repo and size.
  // `images` counts the vision projector, which a reader who picked "Understand pictures" will load.
  const judge = (p, hw, ctx, forced, images) => {
    const m = modelOf(p), opts = {context: ctx, images: !!images};
    let r = null;
    if (forced) {
      const q = ggufs(m).find((x) => x.quant === forced);
      if (q) r = Object.assign(FIT.assess(m, q, hw, opts), {quant: q.quant, bytes: q.bytes, belowFloor: false});
    }
    if (!r) r = FIT.bestQuant(m, hw, opts);
    if (!r || r.verdict === "too-big") {
      // Too big at any quant. Sized at the quant Ollama ships, the one a reader would most likely try.
      const q = ggufs(m).find((x) => x.quant === p.default_quant) || ggufs(m)[0];
      return {verdict: "too-big", quant: q.quant, file: q, fit: FIT.fit(m, q, hw, opts), speed: null, notes: []};
    }
    const file = m.quants.find((x) => x.quant === r.quant) || {label: r.quant, repo: (ggufs(m)[0] || {}).repo};
    return {verdict: r.verdict, quant: r.quant, file, fit: r.fit, speed: r.speed, offload: r.offload,
            nearlyFull: r.nearlyFull, belowFloor: r.belowFloor, notes: r.fit.notes || []};
  };
  const assess = (hw, ctx, qover, images) => D.models.map((p) => ({model: p, r: judge(p, hw, ctx, (qover || {})[p.id], images)}));

  // The memory a card says the reader has. One figure per machine, so two cards never quote two different
  // budgets: on shared memory it is everything the system leaves free (the graphics' default share is the
  // smaller figure the machine sentence names, and a card that goes past it says so); with a graphics card it
  // is the card for a model that fits on the card, and card plus RAM for one that does not.
  const have = (f, hw) => (hw.unified || !hw.gpu ? f.ramBudgetGB
    : f.placement === "gpu" ? f.gpuBudgetGB : f.gpuBudgetGB + f.ramBudgetGB);

  // What would make a model that does not fit, fit: the smallest common size of this kind of machine on which
  // ds-models' policy finds a quant that runs. Asked of the fit method, never worked out here. A shared-memory
  // machine is rebuilt by `toMachine()` at the larger size, so its GPU share follows the platform rule; a
  // graphics card or RAM is changed on the machine object in both its GB and its bytes fields.
  const GIB = 2 ** 30;
  const SIZES = {unified: [8, 16, 24, 32, 36, 48, 64, 96, 128, 192, 256, 512], vram: [8, 12, 16, 24, 32, 48, 80, 96],
                 ram: [8, 16, 32, 64, 96, 128, 192, 256]};
  const runsOn = (p, hw, ctx) => { const b = FIT.bestQuant(modelOf(p), hw, {context: ctx}); return b && b.verdict !== "too-big" && !b.belowFloor; };
  const withRam = (hw, gb) => Object.assign({}, hw, {ram_gb: gb, ram_bytes: gb * GIB});
  const withVram = (hw, gb) => {
    const g = Object.assign({}, hw.gpu, {vram_gb: gb, vram_bytes: gb * GIB});
    return Object.assign({}, hw, {gpu: g, gpus: [g].concat((hw.gpus || []).slice(1))});
  };
  const suggest = (p, mc, ctx) => {
    const hw = mc.hw;
    if (hw.unified) {
      const n = SIZES.unified.find((x) => x > hw.ram_gb &&
        runsOn(p, HW.toMachine(CAT, {device: mc.device.id, memory_gb: x}), ctx));
      return n ? `It would fit on a machine like this with ${n} GB.` : "It's too big for any single home machine.";
    }
    if (hw.gpu) {
      const n = SIZES.vram.find((x) => x > hw.gpu.vram_gb && runsOn(p, withVram(hw, x), ctx));
      const r = SIZES.ram.find((x) => x > hw.ram_gb && runsOn(p, withRam(hw, x), ctx));
      return n ? `It would fit on a graphics card with ${n} GB` + (r ? `, or run with ${r} GB of RAM.` : ".")
        : (r ? `It would only run with ${r} GB of RAM.` : "It's too big for any single home machine.");
    }
    const r = SIZES.ram.find((x) => x > hw.ram_gb && runsOn(p, withRam(hw, x), ctx));
    return r ? `It would fit with ${r} GB of RAM, but a graphics card or a Mac would run it far faster.`
      : "It's too big for any single home machine.";
  };

  // The plain-language lines on a card. HTML, because some of them link to an explainer.
  const reason = (row, mc, ctx) => {
    const f = row.r.fit, hw = mc.hw;
    if (row.r.verdict === "too-big")
      return `Needs about <b>${gb(f.totalGB)} GB</b>; you have ${gb(have(f, hw))} GB for AI. ` + suggest(row.model, mc, ctx);
    if (f.placement === "partial" && hw.gpu && !hw.gpu.integrated && !hw.unified)
      return `Needs <b>${gb(f.totalGB)} GB</b>: about ${gb((f.gpuBytes / GB) + f.kvGB + f.bufferGB)} GB on your graphics card, the rest in RAM.`;
    if (f.placement === "partial")
      return `Needs <b>${gb(f.totalGB)} GB</b> of your ${gb(have(f, hw))} GB: more than the graphics may use by default (${gb(f.gpuBudgetGB)} GB), so the processor takes part of it.`;
    return `Needs <b>${gb(f.totalGB)} GB</b>, you have <b>${gb(have(f, hw))} GB</b> for AI` +
      (f.placement === "gpu" && hw.gpu && !hw.gpu.integrated && !hw.unified ? " on your graphics card." : ".");
  };
  const speedLine = (r) => {
    const tps = r.speed.decodeTps, wps = tps * 0.75;
    const w = wps < 10 ? (Math.round(wps * 10) / 10).toFixed(1) : String(Math.round(wps));
    return `<span data-tps="${tps.toFixed(2)}">Speed: ${esc(FIT.speedWords(tps))} (about ${w} words a second)</span>`;
  };
  // The catch lines: ours first, for the things a beginner needs named, then the fit method's own notes
  // verbatim, which are written in plain English for exactly this (fit.md section 6).
  //
  // A reasoning model writes its thinking before its answer, so its wait is the thinking (about 1,000
  // tokens, ds-models' figure) at this machine's speed -- said as seconds, because "slow" alone reads as a
  // contradiction next to "about as fast as you read". Offload is worded by verdict: on a model that still
  // runs great (a mixture-of-experts model, or a Deck's shared memory) it is a fact, not a warning.
  const THINK_TOKENS = 1000;
  const catches = (r, m) => {
    const out = [], tps = r.speed ? r.speed.decodeTps : 0;
    if (m && m.reasoning && tps) {
      const wait = Math.round(THINK_TOKENS / tps / 5) * 5;
      out.push(wait >= 15 ? `It thinks before it answers: on a hard question, expect the first words after about ${wait} seconds.`
        : "It thinks before it answers, and here that takes only a few seconds.");
    }
    if (r.verdict === "slow" && !(m && m.reasoning && tps >= FIT.THRESHOLDS.great))
      out.push("Slow here: fine for a short question, tiring for a long chat.");
    if (r.verdict === "tight" || r.belowFloor)
      out.push(`Squeezed to fit: this is a smaller version (<a class="lxwhat" href="#q-quant" data-open="q-quant">${esc(r.quant)}</a>), noticeably less sharp. A smaller model may answer better.`);
    if (r.offload)
      out.push(r.verdict === "great"
        ? 'Part of it sits in ordinary memory (<a class="lxwhat" href="#q-offload" data-open="q-offload">offload</a>). That&rsquo;s normal for this model, and it still runs well.'
        : 'Part of it runs from ordinary memory (<a class="lxwhat" href="#q-offload" data-open="q-offload">offload</a>), which is what slows it down.');
    // Two of the method's notes are left out: the below-floor one, which the "squeezed" line above already
    // says, and "reading images adds", which is noise to a reader who did not ask about pictures (one who
    // did has the projector counted already, and the note is not written).
    return out.concat(r.notes.filter((n) => !/below the quality we recommend|^Reading images adds/.test(n)).map(esc));
  };

  // How strongly a pick that runs is recommended: `rank()` in scripts/32_local.py, which orders the cheat
  // sheet the same way. The bigger tier first, then ds-models' primary choice for one of the reader's tasks.
  const TIERS = ["tiny", "small", "medium", "large"];
  const rank = (p, tasks) => TIERS.indexOf(p.tier) * 10 +
    ((p.primary_for || []).some((c) => !tasks.length || tasks.includes(c.use)) ? 5 : 0) + p.model.params_total / 1e12;
  const embedOnly = (p) => p.uses.length === 1 && p.uses[0] === "embeddings";

  // Groups, in the order the page shows them, already filtered by task. `all` lifts the filter. Embedding
  // models answer no questions, so they appear only for the reader who asked to search their documents.
  const groups = (rows, tasks, all) => {
    rows = rows.filter((x) => !embedOnly(x.model) || tasks.includes("embeddings"));
    const want = (row) => all || !tasks.length || row.model.uses.some((t) => tasks.includes(t));
    const shown = rows.filter(want), hidden = rows.length - shown.length;
    const by = (vs) => shown.filter((x) => vs.includes(x.r.verdict));
    const r = (x) => rank(x.model, tasks);
    // Among the great, the ones that fit cleanly come first: a model that only runs great by spilling into
    // RAM, or with under 5% to spare, is a fine second choice and a poor first one for a beginner.
    const snag = (x) => (x.r.offload || x.r.nearlyFull ? 1 : 0);
    const great = by(["great"]).sort((a, b) => snag(a) - snag(b) || r(b) - r(a));
    const ok = by(["slow", "tight"]).sort((a, b) => (a.r.verdict === "tight") - (b.r.verdict === "tight") || r(b) - r(a));
    const no = by(["too-big"]).sort((a, b) => a.r.fit.totalGB - b.r.fit.totalGB);
    // The pick: the best that runs great; failing that, the best that runs slowly; failing that, nothing --
    // a model that only fits squeezed is never what we tell a beginner to start with.
    const best = great[0] || ok.find((x) => x.r.verdict === "slow") || null;
    return {great, ok, no, best, hidden};
  };

  // The commands for a pick at the fitted quant, from ds-models' `run` fields and never composed from a model
  // name: Ollama's library tag when the fit chose the quant that tag ships (or its Q8 tag), otherwise the
  // `hf.co/<repo>:<quant>` route the pick gives for any quant; llama.cpp's `-hf` route the same way, with the
  // context the estimate assumed; MLX's own command.
  const commands = (p, r, ctx) => {
    const run = p.run, label = (r.file && r.file.label) || r.quant, o = run.ollama || {}, l = run.llamacpp || {};
    const ollama = r.quant === p.default_quant || !o.any_quant ? (r.quant === "Q8_0" && o.q8_tag ? `ollama run ${o.q8_tag}` : o.pull)
      : r.quant === "Q8_0" && o.q8_tag ? `ollama run ${o.q8_tag}` : o.any_quant.replace("{LABEL}", label);
    const llama = l.any_quant ? `llama-server -hf ${l.any_quant.replace("{LABEL}", label)} --jinja` : l.cmd;
    return {ollama, ollamaHome: ollama.replace(/^ollama /, "~/ollama/bin/ollama "),
            llama: llama ? `${llama} -c ${ctx}` : null, llamaHere: llama ? `./${llama} -c ${ctx}` : null,
            mlx: run.mlx ? run.mlx.cmd : null,
            lmstudio: (run.lmstudio || {}).catalog || (run.lmstudio || {}).search, label};
  };
  const fill = (text, p, r, ctx) => {
    const c = commands(p, r, ctx);
    return text.replace(/\{ollama_cmd\}/g, esc(c.ollama)).replace(/\{ollama_cmd_home\}/g, esc(c.ollamaHome))
      .replace(/\{llama_cmd\}/g, esc(c.llama || "")).replace(/\{llama_cmd_here\}/g, esc(c.llamaHere || ""))
      .replace(/\{mlx_cmd\}/g, esc(c.mlx || "")).replace(/\{lmstudio\}/g, esc(c.lmstudio))
      .replace(/\{qlabel\}/g, esc(c.label)).replace(/\{ctx\}/g, String(ctx));
  };
  // The routes a pick can be run by on an OS, beginner's first. MLX only on a Mac with Apple Silicon.
  const routes = (p, r, os, isApple) => ["lmstudio", "ollama", "llamacpp", "mlx"].filter((k) => {
    if (!D.howto[k].steps[os]) return false;
    if (k === "llamacpp" && !p.run.llamacpp) return false;
    if (k === "mlx" && (!isApple || !p.run.mlx)) return false;
    return true;
  });
  const defaultRoute = (os) => (os === "linux" ? "ollama" : "lmstudio");
  // A route's steps for an OS, as [kind, html]: "li" for a step, "cmd" for a command under it. The context
  // steps appear only when the estimate assumed more context than the runner gives by default. An embedding
  // model has no chat to open, so the steps about chatting are left out and the card says what uses it.
  const CHATTY = /&gt;&gt;&gt;|click Chat|open <b>http/;
  const steps = (route, os, p, r, ctx) => D.howto[route].steps[os].flatMap((st) => {
    if (!Array.isArray(st)) return embedOnly(p) && CHATTY.test(st) ? [] : [["li", fill(st, p, r, ctx)]];
    if ((st[0] === "ctx" || st[0] === "ctxcmd") && (ctx <= D.runner_ctx || embedOnly(p))) return [];
    return [[st[0] === "ctx" ? "li" : "cmd", fill(st[1], p, r, ctx)]];
  });

  // What the browser lets us guess is ds-hardware's `detectHints()`: candidates, never a choice (contract
  // section 7). Only a confirmed pick reaches the hash; a detected string never does.
  const guess = () => HW.detectHints(CAT);

  // The hash. Short keys, because people paste these.
  // `d`, `mem`, `ram` and `rk` are ds-hardware's (contract section 8); `rs` is the RAM-sticks answer.
  const KEYS = ["k", "d", "mem", "ram", "rk", "rs", "t", "n", "c", "w", "o"];
  const parseHash = (h) => {
    const p = new URLSearchParams(String(h || "").replace(/^#/, "")), s = {};
    for (const k of KEYS) if (p.has(k)) s[k] = p.get(k);
    for (const k of ["mem", "ram", "rs", "c"]) if (s[k] !== undefined) { s[k] = Number(s[k]); if (!isFinite(s[k])) delete s[k]; }
    s.t = s.t ? s.t.split(",").filter(Boolean) : [];
    s.n = s.n === "1";
    return s;
  };
  const hashOf = (s) => {
    const p = new URLSearchParams();
    for (const k of KEYS) {
      const v = s[k];
      if (k === "t") { if (v && v.length) p.set("t", v.join(",")); }
      else if (k === "n") { if (v) p.set("n", "1"); }
      else if (v !== undefined && v !== null && v !== "") p.set(k, String(v));
    }
    const out = p.toString().replace(/%2C/g, ",");
    return out ? "#" + out : "";
  };

  return {esc, gb, search, uaOS, choices, machineOf, machineWords, modelOf, judge, assess, have, suggest, howtoOS,
          reason, speedLine, catches, groups, rank, embedOnly, commands, fill, routes, defaultRoute, steps, guess,
          parseHash, hashOf, apple,
          ggufs, DEV, PICK, TILE, CAT};
})(JSON.parse(document.getElementById("lxdata").textContent), LOCALFIT, LOCALHW);

(() => {
  const D = JSON.parse(document.getElementById("lxdata").textContent);
  const U = LOCALUI, esc = U.esc, $ = (id) => document.getElementById(id);
  const UA = navigator.userAgent;
  const TASKS = Object.fromEntries(D.tasks.map((t) => [t.id, t.label]));
  const OSN = {windows: "Windows", macos: "macOS", linux: "Linux", steamos: "Steam Deck", chromeos: "Chromebook"};
  let S = U.parseHash(location.hash);
  let showAll = false, moreGreat = false;
  const qover = {};

  const save = () => {
    const h = U.hashOf(S);
    if (h !== location.hash && !(h === "" && !location.hash))
      history.replaceState(null, "", h || location.pathname + location.search);
  };

  // ---- a combobox, ARIA 1.2 pattern: focus stays in the input, the active option is aria-activedescendant.
  const combo = (input, list, source, onPick) => {
    let items = [], active = -1;
    const close = () => { list.hidden = true; input.setAttribute("aria-expanded", "false"); input.removeAttribute("aria-activedescendant"); active = -1; };
    const paint = () => {
      list.innerHTML = items.length ? items.map((it, i) =>
        `<li role="option" id="${list.id}-${i}" data-i="${i}" aria-selected="${i === active}">` +
        `<span>${esc(it.label)}</span>${it.sub ? `<small>${esc(it.sub)}</small>` : ""}</li>`).join("")
        // innerHTML for the no-match line only, which is this file's own copy and carries entities.
        : '<li role="option" aria-disabled="true" aria-selected="false"><span>Not in our list. A laptop&rsquo;s brand name doesn&rsquo;t tell us its chip: try its graphics card (for example &ldquo;RTX 4060&rdquo;), choose &ldquo;No graphics card&rdquo;, or open &ldquo;Help me find out&rdquo; below.</span></li>';
      list.hidden = false; input.setAttribute("aria-expanded", "true");
      if (active >= 0) { input.setAttribute("aria-activedescendant", `${list.id}-${active}`); list.children[active].scrollIntoView({block: "nearest"}); }
      else input.removeAttribute("aria-activedescendant");
    };
    const open = () => { items = source(input.value); active = -1; paint(); };
    const pick = (i) => { const it = items[i]; if (!it) return; input.value = it.label; close(); onPick(it); };
    input.addEventListener("input", open);
    // A box that already names the chosen machine is selected on focus, so typing replaces it rather than
    // appending to "MacBook Air (M3)" and finding nothing.
    input.addEventListener("focus", () => { if (!input.value) open(); else input.select(); });
    input.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown") { e.preventDefault(); if (list.hidden) open(); active = Math.min(items.length - 1, active + 1); paint(); }
      else if (e.key === "ArrowUp") { e.preventDefault(); active = Math.max(0, active - 1); paint(); }
      else if (e.key === "Enter") { if (!list.hidden && items.length) { e.preventDefault(); pick(active >= 0 ? active : 0); } }
      else if (e.key === "Escape") { if (!list.hidden) { e.preventDefault(); close(); } }
    });
    input.addEventListener("blur", () => setTimeout(close, 120));
    list.addEventListener("mousedown", (e) => e.preventDefault());
    list.addEventListener("click", (e) => { const li = e.target.closest("li[data-i]"); if (li) pick(Number(li.dataset.i)); });
    return {close};
  };

  const tileLabel = (k) => (U.TILE[k] || {}).label || "";
  const WHAT = {gpu: "graphics card", cpu: "", soc: "chip", system: ""};
  combo($("q"), $("qlist"), (q) => U.search(q, S.k).map((r) =>
    ({id: r.id, label: r.name, mem: r.memory_gb,
      sub: r.tiles && !r.tiles.includes(S.k) ? tileLabel(r.tiles[0]) : WHAT[r.kind] || ""})),
    (it) => chooseDevice(it.id, it.mem));

  // ---- choices
  const chooseKind = (k) => {
    S.k = k;
    const d = S.d && U.DEV[S.d];
    if (d && !d.tiles.includes(k)) { delete S.d; delete S.mem; delete S.ram; delete S.rk; delete S.rs; }
    paintStep1();
    update();
  };
  // A choice resets the memory answers that belonged to the previous machine, keeping a typed size
  // ("m3 max 36gb") when search read one out of the query.
  const chooseDevice = (id, mem, ram, rk) => {
    S.d = id; delete S.mem; delete S.ram; delete S.rk; delete S.rs;
    if (mem) S.mem = mem;
    if (ram) S.ram = ram;
    // A preset's memory kind is part of the machine it names ("Desktop, RTX 3060 + 32 GB" is DDR4), so it
    // travels in the hash with it and the picker builds exactly the machine the cheat sheet does.
    if (rk) S.rk = rk;
    const t = U.DEV[id].tiles;
    if (!S.k || !t.includes(S.k)) S.k = t.includes("gaming-pc") && U.DEV[id].kind === "gpu" ? "gaming-pc" : t[0];
    paintStep1(); update();
  };
  const choosePreset = (id) => {
    const p = U.CAT.presets.find((x) => x.id === id);
    if (p) chooseDevice(p.device, p.memory_gb || undefined, p.ram_gb || undefined, p.ram_kind || undefined);
  };

  // Chip rows built as radio groups, so arrow keys move within them the way they do in any OS dialog.
  const radios = (box, name, opts, cur, label, onPick) => {
    box.innerHTML = opts.map((o) => `<label class="chip lxchip"><input type="radio" name="${name}" value="${o}"` +
      `${o === cur ? " checked" : ""}><span>${esc(label(o))}</span></label>`).join("");
    box.querySelectorAll("input").forEach((i) => i.addEventListener("change", () => onPick(Number(i.value))));
  };

  const paintStep1 = () => {
    document.querySelectorAll("input[name=kind]").forEach((i) => { i.checked = i.value === S.k; });
    $("pick").hidden = !S.k;
    if (!S.k) return;
    const gaming = S.k === "gaming-pc";
    $("qlab").textContent = gaming ? "Which graphics card? Start typing its name"
      : `Which ${tileLabel(S.k).toLowerCase()}? Start typing its name`;
    $("q").placeholder = gaming ? "e.g. RTX 4060, RX 7800 XT" : S.k === "mac" ? "e.g. MacBook Air M2"
      : S.k === "handheld" ? "e.g. Steam Deck OLED" : "e.g. RTX 4060 laptop, Ryzen AI Max";
    $("pop").innerHTML = '<span class="lxpl">Popular:</span>' + HWpop(S.k).map((p) =>
      `<button class="chip" type="button" data-preset="${esc(p.id)}" aria-pressed="${presetOn(p)}">${esc(p.label)}</button>`).join("");
    $("nogpu").hidden = !["laptop", "desktop", "gaming-pc", "mini-pc"].includes(S.k);
    $("nogpu").setAttribute("aria-pressed", String(S.d === D.no_gpu));
    const mc = U.machineOf(S);
    const c = mc && mc.choices;
    // The device's own memory: VRAM for a card, the one pool for a Mac or handheld, RAM for no card.
    $("memf").hidden = !(c && c.ask);
    if (c && c.ask) {
      $("meml").textContent = c.label;
      radios($("memo"), "mem", c.options_gb, mc.mem, (o) => `${o} GB`, (v) => { S.mem = v; paintStep1(); update(); refocus("input[name=mem]:checked"); });
    }
    // A graphics card also needs the PC's own RAM, for what does not fit on the card.
    const sys = c && c.system_ram && mc.device.kind === "gpu" ? c.system_ram : null;
    $("ramf").hidden = !sys;
    if (sys) radios($("ramo"), "ram", sys.options_gb, mc.hw.ram_gb, (o) => `${o} GB`, (r) => { S.ram = r; paintStep1(); update(); refocus("input[name=ram]:checked"); });
    // Sticks, only where the RAM is socketed and separate: a desktop's or a gaming laptop's, never a Mac's.
    $("stickf").hidden = !(mc && mc.sticks);
    if (mc && mc.sticks) radios($("sticko"), "rs", [1, 2], S.rs || 2, (o) => (o === 1 ? "One" : "Two or more"),
      (v) => { S.rs = v === 2 ? undefined : 1; paintStep1(); update(); refocus("input[name=rs]:checked"); });
    // Always from the state, so a hash change (a shared link opened in this tab) cannot leave the box
    // naming the previous machine. Typing never reaches here, so nothing a reader is typing is overwritten.
    $("q").value = mc && mc.device.id !== D.no_gpu ? mc.device.name : "";
    $("gores").hidden = !mc;
    const sum = $("s1sum");
    sum.hidden = !mc;
    if (mc) sum.textContent = mc.name;
  };
  const HWpop = (tile) => LOCALHW.popular(U.CAT, tile).filter((p) => p.tile === tile).slice(0, 10);
  const presetOn = (p) => p.device === S.d && (!p.memory_gb || p.memory_gb === (U.machineOf(S) || {}).mem);

  // ---- results
  // Verdicts, as a shape and a word, so colour never carries the meaning alone. The four answers the fit
  // method gives fold into the three groups the page shows: `slow` and `tight` are both "a catch".
  const SHAPE = {great: "●", slow: "◐", tight: "◐", "too-big": "○"};
  const WORD = {great: "Runs great", slow: "Runs, slowly", tight: "Only fits squeezed", "too-big": "Won’t fit"};
  const card = (row, mc, ctx, open) => {
    const {model, r} = row, no = r.verdict === "too-big";
    const lines = no ? [] : U.catches(r, U.modelOf(model));
    const tasks = model.uses.map((t) => TASKS[t]).filter(Boolean).join(", ");
    return `<li class="lxcard" data-model="${esc(model.id)}" data-verdict="${r.verdict}">` +
      `<div class="lxch"><h4>${esc(model.name)}</h4><span class="lxv" data-v="${r.verdict}"><i aria-hidden="true">${SHAPE[r.verdict]}</i>${WORD[r.verdict]}</span></div>` +
      `<p class="lxblurb">${esc(model.why)}</p>` +
      `<p class="lxwhy"><span>${U.reason(row, mc, ctx)}</span>${r.speed ? U.speedLine(r) : ""}</p>` +
      (lines.length ? `<ul class="lxcatch">${lines.map((l) => `<li>${l}</li>`).join("")}</ul>` : "") +
      `<p class="lxmeta">Good for: ${esc(tasks)} · Licence: <span title="${esc(model.license.note || "")}">${esc(model.license.name)}</span></p>` +
      (S.n ? numbers(row, mc) : "") +
      (no ? "" :
        `<button class="lxhow" type="button" aria-expanded="${open ? "true" : "false"}" aria-controls="how-${esc(model.id)}" data-how="${esc(model.id)}">How to run it</button>` +
        `<div class="lxhowb" id="how-${esc(model.id)}"${open ? "" : " hidden"}>${open ? howto(row, mc, ctx) : ""}</div>`) +
      "</li>";
  };

  // The expert view: the fit method's own numbers, unrounded except for display.
  const numbers = (row, mc) => {
    const {model, r} = row, f = r.fit, gb = U.gb, m = U.modelOf(model);
    const shared = mc.hw.unified;
    const where = {gpu: shared ? "all on the graphics, in shared memory" : "all on the graphics card",
                   cpu: "on the processor, from RAM",
                   partial: shared ? "graphics and processor, sharing memory"
                     : `${f.gpuLayers} of ${f.layers} layers on the graphics card, the rest from RAM`}[f.placement] || "doesn’t fit";
    const qs = U.ggufs(m).map((q) => `<option value="${esc(q.quant)}"${q.quant === r.quant ? " selected" : ""}>${esc(q.label || q.quant)} (${gb(q.bytes / 1e9)} GB)</option>`).join("");
    const active = m.params_active && m.params_active < m.params_total ? `, ${(m.params_active / 1e9).toFixed(1)}B active per word` : "";
    const sp = r.speed;
    return `<dl class="lxnums">` +
      `<dt>Version</dt><dd><label class="sr" for="qv-${esc(model.id)}">Quantisation for ${esc(model.name)}</label>` +
      `<select id="qv-${esc(model.id)}" data-quant="${esc(model.id)}">${qs}</select></dd>` +
      `<dt>Weights</dt><dd>${gb(f.weightsGB)} GB</dd>` +
      `<dt>Context cache</dt><dd>${gb(f.kvGB)} GB at ${(f.context / 1024) | 0}k tokens</dd>` +
      `<dt>Working memory</dt><dd>${gb(f.bufferGB)} GB</dd>` +
      `<dt>Total</dt><dd>${gb(f.totalGB)} GB of ${gb(U.have(f, mc.hw))} GB` + (f.fits && f.headroomGB != null ? ` (${gb(f.headroomGB)} GB to spare)` : "") + `</dd>` +
      `<dt>Runs</dt><dd>${where}</dd>` +
      (sp ? `<dt>Writing</dt><dd>${sp.decodeRange[0].toFixed(0)}–${sp.decodeRange[1].toFixed(0)} tokens/s (${esc(sp.backend)}, estimate)</dd>` +
            `<dt>Reading</dt><dd>a 20-page document (10k tokens) in about ${Math.max(1, Math.round(10000 / sp.prefillTps))} s</dd>` : "") +
      `<dt>Size</dt><dd>${(m.params_total / 1e9).toFixed(1)}B parameters${active}</dd>` +
      `</dl>`;
  };

  const howto = (row, mc, ctx) => {
    const {model, r} = row;
    const os = S.o && D.howto.ollama.steps[S.o] ? S.o : U.howtoOS(mc.os);
    const rs = U.routes(model, r, os, U.apple(mc));
    const route = rs.includes(S.w) ? S.w : (rs.includes(U.defaultRoute(os)) ? U.defaultRoute(os) : rs[0]);
    const h = D.howto[route];
    const oses = ["windows", "macos", "linux", "steamos"];
    // Commands sit inside the step before them, so the list numbers stay the steps a person does.
    const ol = [];
    for (const [kind, html] of U.steps(route, os, model, r, ctx)) {
      if (kind === "li") { ol.push(`<li>${html}</li>`); continue; }
      const cmd = `<div class="lxcmd"><code>${html}</code><button class="lxcopy" type="button" data-copy>Copy</button></div>`;
      if (ol.length) ol[ol.length - 1] = ol[ol.length - 1].replace(/<\/li>$/, cmd + "</li>"); else ol.push(`<li>${cmd}</li>`);
    }
    const size = (r.file && r.file.bytes ? r.file.bytes : r.fit.weightsGB * 1e9) / 1e9;
    const mins = Math.max(1, Math.round(size * 8000 / 50 / 60));
    return `<div class="lxroutes" role="group" aria-label="How to run it"><span class="lxpl">Use</span>` +
      rs.map((k) => `<button class="chip" type="button" data-route="${k}" aria-pressed="${k === route}">${esc(D.howto[k].label)}</button>`).join("") + `</div>` +
      `<p class="lxpitch">${esc(h.pitch)}</p>` +
      `<div class="lxroutes" role="group" aria-label="Your operating system"><span class="lxpl">On</span>` +
      oses.filter((o) => h.steps[o]).map((o) => `<button class="chip" type="button" data-os="${o}" aria-pressed="${o === os}">${OSN[o]}</button>`).join("") + `</div>` +
      (U.embedOnly(model) ? `<p class="lxpitch">This model doesn’t chat. It turns your documents into something searchable, for apps such as AnythingLLM or Open WebUI to use once it’s downloaded.</p>` : "") +
      `<ol>${ol.join("")}</ol>` +
      `<p class="lxdl">The first download is about ${U.gb(size)} GB, roughly ${mins} minute${mins === 1 ? "" : "s"} on a 50 Mbit/s connection. After that it works with no internet.</p>`;
  };

  const opened = new Set();
  let autoBest = null;
  const update = () => {
    save();
    document.querySelectorAll("input[name=task]").forEach((i) => { i.checked = S.t.includes(i.value); });
    $("nums").setAttribute("aria-pressed", String(S.n));
    $("nums").textContent = S.n ? "Hide the numbers" : "Show the numbers";
    $("expert").hidden = !S.n;
    const ctx = S.c || D.default_ctx;
    $("ctx").value = String(ctx);
    const mc = U.machineOf(S), out = $("results");
    if (!mc) { $("mach").textContent = "Pick your computer above and the answers appear here."; out.innerHTML = ""; return; }
    // The machine sentence, then ds-hardware's notes about it, and a plain flag on the few entries whose
    // numbers are estimates rather than published specs.
    $("mach").innerHTML = U.machineWords(mc) +
      (mc.approx ? ` <span class="lxapprox">Some of this machine&rsquo;s numbers are estimates, so treat its speeds as approximate.</span>` : "") +
      (mc.hw.notes.length ? `<details class="lxhwnotes"><summary>Good to know about this machine</summary><ul>${mc.hw.notes.map((n) => `<li>${esc(n)}</li>`).join("")}</ul></details>` : "");
    const g = U.groups(U.assess(mc.hw, ctx, qover, S.t.includes("vision")), S.t, showAll);
    // The pick's how-to opens by itself, because most readers should stop there. When the pick changes, the
    // old one's panel closes with it, unless the reader opened it themselves.
    const bestId = g.best && g.best.model.id;
    if (bestId !== autoBest) { if (autoBest) opened.delete(autoBest); if (bestId) opened.add(bestId); autoBest = bestId; }
    const list = (rows) => `<ul class="lxcards">${rows.map((x) => card(x, mc, ctx, opened.has(x.model.id) && x.model.id !== bestId)).join("")}</ul>`;
    const greatRest = g.great.filter((x) => x.model.id !== bestId);
    const cap = moreGreat ? greatRest.length : 5;
    let html = "";
    if (g.best) html += `<div class="lxbest" id="best"><p>Our pick for you</p><ul class="lxcards">${card(g.best, mc, ctx, opened.has(bestId))}</ul></div>`;
    else html += `<p class="lxnote">Nothing we recommend runs well on this machine as it is. Anything that only fits squeezed is below; so is what would make the rest fit.</p>`;
    if (S.t.length || g.hidden) html += `<p class="lxnote">` + (S.t.length && !showAll
      ? `Showing models for: ${esc(S.t.map((t) => TASKS[t]).join(", "))}. ${g.hidden} others hidden. <button class="lxlink" type="button" id="showall">Show all models</button>`
      : `Showing every model. <button class="lxlink" type="button" id="showall">Only the ones for: ${esc(S.t.map((t) => TASKS[t]).join(", "))}</button>`) + "</p>";
    if (greatRest.length) html += `<section class="lxgroup" aria-labelledby="hg"><h3 id="hg"><span aria-hidden="true">${SHAPE.great}</span> ${g.best && g.best.r.verdict === "great" ? "Also runs great" : "Runs great"} <span class="ct">${greatRest.length}</span></h3>${list(greatRest.slice(0, cap))}` +
      (greatRest.length > cap ? `<p class="lxmore"><button class="chip" type="button" id="moregreat">Show ${greatRest.length - cap} more</button></p>` : "") + "</section>";
    const okRest = g.ok.filter((x) => x.model.id !== bestId);
    if (okRest.length) html += `<section class="lxgroup" aria-labelledby="ho"><h3 id="ho"><span aria-hidden="true">${SHAPE.slow}</span> Runs, with a catch <span class="ct">${okRest.length}</span></h3>${list(okRest)}</section>`;
    if (g.no.length) html += `<details class="lxgroup lxnofit" id="nofit"><summary><span aria-hidden="true">${SHAPE["too-big"]}</span> ${g.no.length} bigger model${g.no.length === 1 ? "" : "s"} won’t fit</summary>${list(g.no)}</details>`;
    const wasOpen = $("nofit") && $("nofit").open;
    out.innerHTML = html;
    if (wasOpen && $("nofit")) $("nofit").open = true;
    $("live").textContent = `For ${mc.name}: ${g.great.length} run great, ${g.ok.length} with a catch, ${g.no.length} won’t fit.` +
      (g.best ? ` Our pick is ${g.best.model.name}.` : "");
  };

  // ---- events, delegated, so re-rendered cards need no re-wiring
  // No focus move on change: arrow keys walk a radio group by changing it, and stealing focus to the search
  // box on every arrow press would make the tiles impossible to browse by keyboard. The search is next in
  // tab order anyway.
  document.querySelectorAll("input[name=kind]").forEach((i) => i.addEventListener("change", () => chooseKind(i.value)));
  $("gobtn").addEventListener("click", () => { $("s3").scrollIntoView({block: "start", behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth"}); $("s3h").focus({preventScroll: true}); });
  $("pick").addEventListener("click", (e) => { const b = e.target.closest("[data-preset]"); if (b) choosePreset(b.dataset.preset); });
  $("nogpu").addEventListener("click", () => chooseDevice(D.no_gpu));
  document.querySelectorAll("input[name=task]").forEach((i) => i.addEventListener("change", () => {
    S.t = [...document.querySelectorAll("input[name=task]:checked")].map((x) => x.value); showAll = false; update();
  }));
  $("nums").addEventListener("click", () => { S.n = !S.n; update(); });
  $("ctx").addEventListener("change", () => { S.c = Number($("ctx").value); if (S.c === D.default_ctx) delete S.c; update(); });

  const refocus = (sel) => { const el = document.querySelector(sel); if (el) el.focus(); };
  $("results").addEventListener("click", (e) => {
    const how = e.target.closest("[data-how]");
    if (how) {
      const id = how.dataset.how, panel = $("how-" + id), open = how.getAttribute("aria-expanded") !== "true";
      how.setAttribute("aria-expanded", String(open));
      if (open) {
        opened.add(id);
        const mc = U.machineOf(S), ctx = S.c || D.default_ctx;
        panel.innerHTML = howto({model: U.PICK[id], r: U.judge(U.PICK[id], mc.hw, ctx, qover[id], S.t.includes("vision"))}, mc, ctx);
      }
      else opened.delete(id);
      panel.hidden = !open;
      return;
    }
    const rt = e.target.closest("[data-route],[data-os]");
    if (rt) {
      const id = rt.closest(".lxcard").dataset.model;
      if (rt.dataset.route) S.w = rt.dataset.route; else S.o = rt.dataset.os;
      opened.add(id); update();
      refocus(`.lxcard[data-model="${id}"] [${rt.dataset.route ? "data-route" : "data-os"}="${rt.dataset.route || rt.dataset.os}"]`);
      return;
    }
    const cp = e.target.closest("[data-copy]");
    if (cp) {
      const text = cp.previousElementSibling.textContent;
      const done = () => { cp.textContent = "Copied"; $("live").textContent = "Copied to the clipboard."; setTimeout(() => { cp.textContent = "Copy"; }, 1600); };
      if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, () => { cp.textContent = "Select it"; });
      return;
    }
    if (e.target.id === "showall") { showAll = !showAll; update(); refocus("#showall"); return; }
    if (e.target.id === "moregreat") { moreGreat = true; update(); return; }
  });
  $("results").addEventListener("change", (e) => {
    const q = e.target.closest("[data-quant]");
    if (q) { qover[q.dataset.quant] = q.value; opened.add(q.dataset.quant); update(); refocus(`[data-quant="${q.dataset.quant}"]`); }
  });

  // "What's that?" links open their explainer and move focus to it, rather than jumping to a closed box.
  document.addEventListener("click", (e) => {
    const a = e.target.closest("a[data-open]");
    if (!a) return;
    const box = $(a.dataset.open);
    if (!box) return;
    e.preventDefault(); box.open = true;
    box.scrollIntoView({block: "start", behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth"});
    box.querySelector("summary").focus();
  });

  // ---- help me find out: ds-hardware's steps per OS, each with a description of the screen it shows, and
  // its fallback advice; then its browser hints, offered as buttons to confirm, never applied by themselves.
  const findOS = (os) => {
    const h = U.CAT.help;
    $("fos").innerHTML = ["windows", "macos", "linux", "steamos", "chromeos"].map((o) =>
      `<button class="chip" type="button" data-fos="${o}" aria-pressed="${o === os}">${OSN[o]}</button>`).join("");
    $("fsteps").innerHTML = h[os].steps.map((st) => `<li>${esc(st.text)}` +
      (st.caption ? `<span class="lxcap">What you&rsquo;ll see: ${esc(st.caption)}</span>` : "") + "</li>").join("");
    const fb = h.fallback && (h.fallback.steps || [])[0];
    $("ffall").textContent = fb ? fb.text : "";
  };
  $("fos").addEventListener("click", (e) => { const b = e.target.closest("[data-fos]"); if (b) { findOS(b.dataset.fos); refocus(`[data-fos="${b.dataset.fos}"]`); } });
  findOS(U.uaOS(UA));
  $("guess").addEventListener("click", async () => {
    const out = $("guessout");
    out.textContent = "Looking…";
    const h = await U.guess();
    const cands = (h.gpu && h.gpu.candidates) || [];
    const name = (id) => (U.DEV[id] || {}).name || id;
    out.innerHTML = (cands.length
      ? `<p>Looks like: ${cands.map((c) => `<button class="chip" type="button" data-guess="${esc(c.id)}">${esc(name(c.id))}${c.confidence === "maybe" ? " (maybe)" : ""}</button>`).join("")} Tap the right one to use it.</p>`
      : `<p>Your browser didn&rsquo;t name a graphics chip we know. The steps below will tell you.</p>`) +
      (h.ram && h.ram.meaning ? `<p class="lxquiet">Memory: your browser says ${esc(h.ram.meaning)}.</p>` : "") +
      (h.notes || []).map((n) => `<p class="lxquiet">${esc(n)}</p>`).join("");
    if (h.os && U.CAT.help[h.os]) findOS(h.os);
  });
  $("guessout").addEventListener("click", (e) => {
    const b = e.target.closest("[data-guess]");
    if (!b) return;
    chooseDevice(b.dataset.guess);
    refocus("#s3h");
  });

  addEventListener("hashchange", () => { S = U.parseHash(location.hash); paintStep1(); update(); });
  paintStep1(); update();
})();
