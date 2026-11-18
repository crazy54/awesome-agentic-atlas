/* The local-AI page's behaviour. Written into docs/local/index.html by scripts/32_local.py, after the
   `lxdata` JSON block and the LOCAL FIT script it reads.

   Two halves. `LOCALUI` is pure: search, the machine a set of answers describes, the verdicts, the words a
   reader is shown, the commands, and the URL hash. Each is a function of its arguments and nothing else,
   which is what lets tests/local-check.mjs assert them directly as well as through the DOM. The bottom half
   wires them to the page and owns all the state.

   Every answer lives in the hash (`#d=steam-deck-oled&t=code`), so a result can be sent to a friend and
   reproduces exactly, and a reload keeps your place. `history.replaceState` rather than push: each click
   is a refinement of one question, not a new page, and twenty back presses to leave would be a trap. */
const LOCALUI = ((D, FIT) => {
  const byId = (xs) => Object.fromEntries(xs.map((x) => [x.id, x]));
  const DEV = byId(D.devices), GPU = byId(D.gpus);
  const esc = (s) => String(s === null || s === undefined ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#x27;");
  // One decimal under ten, whole numbers above: "5.6 GB", "19 GB". The precision a reader can use.
  const gb = (x) => (x < 10 ? (Math.round(x * 10) / 10).toFixed(1) : String(Math.round(x)));

  // Search. "mba m2", "MacBook Air M2", "deck oled" and "4070" should all find what a person means, so both
  // sides are folded to lowercase words, the word "apple" and trademark marks are dropped, and a query token
  // matches if it appears in the record's words or in the same words run together ("macbookair").
  const norm = (s) => String(s || "").toLowerCase().replace(/\(tm\)|\(r\)|[®™]|\bapple\b/g, " ")
    .replace(/[^a-z0-9]+/g, " ").trim();
  const hits = (q, rec) => {
    const toks = norm(q).split(" ").filter(Boolean);
    const hay = norm([rec.name].concat(rec.aliases || []).join(" "));
    const run = hay.replace(/ /g, "");
    return toks.every((t) => hay.includes(t) || run.includes(t));
  };
  // Devices of the chosen kind first, then popular ones, then by name. Other kinds are still offered,
  // labelled, because a reader who picked "Laptop" for their MacBook should still find it.
  const search = (q, list, kind, limit = 8) => list
    .filter((r) => hits(q, r))
    // A query that appears whole in one field ("4070 ti super" in that card's name) outranks one whose words
    // are merely all somewhere in the record (the plain 4070, which is also sold as a "Super" and a "Ti").
    .map((r) => [r, (kind && r.kind !== kind ? 8 : 0) +
                    ([r.name].concat(r.aliases || []).some((f) => norm(f).includes(norm(q))) ? 0 : 4) +
                    (norm(r.name).startsWith(norm(q)) ? 0 : 1) + (r.popular ? 0 : 2)])
    .sort((a, b) => a[1] - b[1] || a[0].name.localeCompare(b[0].name))
    .slice(0, limit).map((x) => x[0]);

  // The operating system the browser is running on, as the catalogue spells it. A guess for defaults only;
  // the how-to panel always lets the reader pick another.
  const uaOS = (ua) => /Mac OS X|Macintosh/.test(ua) && !/iPhone|iPad/.test(ua) ? "macos"
    : /Linux|X11|CrOS/.test(ua) && !/Android/.test(ua) ? "linux" : "windows";

  // The machine a set of answers describes, as the fit maths wants it, or null if there is not one yet.
  const machineOf = (s, ua) => {
    if (s.d && DEV[s.d]) {
      const d = DEV[s.d], g = d.gpu ? GPU[d.gpu] : null;
      const ram = d.ram_gb_options.includes(s.r) ? s.r : d.ram_gb_options[0];
      return {name: d.name, kind: d.kind, os: d.os[0], ram_opts: d.ram_gb_options, gpu: g, device: d,
              m: {ram_gb: ram, vram_gb: d.vram_gb, unified: d.unified, backend: g ? g.backend : d.backend,
                  gpu_bw_gbs: g ? g.bw_gbs : d.bw_gbs, cpu_bw_gbs: d.bw_gbs}};
    }
    if (s.g && (s.g === "none" || GPU[s.g])) {
      const g = GPU[s.g] || null, opts = D.custom.ram_gb_options;
      const ram = opts.includes(s.r) ? s.r : 16;
      const vram = g ? (g.vram_gb_options.includes(s.v) ? s.v : g.vram_gb_options[0]) : 0;
      const os = uaOS(ua) === "macos" ? "windows" : uaOS(ua);
      return {name: g ? `PC with ${g.name} ${vram} GB` : "PC with no graphics card", kind: s.k || "gaming",
              os, ram_opts: opts, gpu: g, custom: true,
              m: {ram_gb: ram, vram_gb: vram, unified: false, backend: g ? g.backend : "cpu",
                  gpu_bw_gbs: g ? g.bw_gbs : 0, cpu_bw_gbs: D.custom.cpu_bw_gbs}};
    }
    return null;
  };

  // One sentence on what this machine offers, so every "you have X GB" below has been explained once.
  const machineWords = (mc) => {
    const m = mc.m, b = FIT.budget(m, D.usable), name = esc(mc.name);
    if (m.unified && m.backend === "metal")
      return `Your ${name} has <b>${m.ram_gb} GB</b> of memory, shared by the processor and graphics. ` +
        `macOS lets AI use about <b>${gb(b.gpu)} GB</b> of it and keeps the rest for itself and your apps.`;
    if (m.unified)
      return `Your ${name} shares <b>${m.ram_gb} GB</b> between the processor and graphics. About ` +
        `<b>${gb(b.gpu)} GB</b> can go to AI once the system has its share.`;
    if (m.vram_gb > 0)
      return `Your graphics card has <b>${m.vram_gb} GB</b> of its own memory (about <b>${gb(b.gpu)} GB</b> ` +
        `usable), and that's where AI runs fast. Your <b>${m.ram_gb} GB</b> of RAM can hold overflow ` +
        `(about ${gb(b.cpu)} GB), but much more slowly.`;
    return `No separate graphics card, so AI runs on the processor using your <b>${m.ram_gb} GB</b> of RAM. ` +
      `About <b>${gb(b.cpu)} GB</b> is free for it. It works, just more slowly than on a graphics card.`;
  };

  // Every model against one machine.
  const assess = (m, ctx, qover) => D.models.map((model) =>
    ({model, r: FIT.fit(m, model, {ctx, quant: (qover || {})[model.id]}, D.usable)}));

  // What would make a model that does not fit, fit: the smallest common size that would hold it.
  const SIZES = {unified: [8, 16, 24, 32, 36, 48, 64, 96, 128, 192, 256, 512], vram: [8, 12, 16, 24, 32, 48, 80, 96],
                 ram: [8, 16, 32, 64, 96, 128, 192, 256]};
  const suggest = (m, total) => {
    const fits = (mm) => { const b = FIT.budget(mm, D.usable); return total <= Math.max(b.gpu, b.cpu, b.gpu + (b.gpu ? b.cpu : 0)); };
    if (m.unified) {
      const n = SIZES.unified.find((x) => fits(Object.assign({}, m, {ram_gb: x})));
      return n ? `It would fit on a machine like this with ${n} GB.` : "It's too big for any single home machine.";
    }
    if (m.vram_gb > 0) {
      const n = SIZES.vram.find((x) => x - D.usable.vram_reserve_gb >= total);
      const r = SIZES.ram.find((x) => fits(Object.assign({}, m, {ram_gb: x})));
      return n ? `It would fit on a graphics card with ${n} GB` + (r ? `, or run slowly with ${r} GB of RAM.` : ".")
        : (r ? `It would only run, slowly, with ${r} GB of RAM.` : "It's too big for any single home machine.");
    }
    const r = SIZES.ram.find((x) => fits(Object.assign({}, m, {ram_gb: x})));
    return r ? `It would fit with ${r} GB of RAM, but a graphics card or a Mac would run it far faster.`
      : "It's too big for any single home machine.";
  };

  // The plain-language lines on a card. HTML, because two of them link to an explainer.
  const reason = (m, r) => {
    if (r.verdict === "no")
      return `Needs about <b>${gb(r.need.total)} GB</b>; you have ${gb(r.have)} GB for AI. ` + suggest(m, r.need.total);
    const where = r.place === "split"
      ? `Needs <b>${gb(r.need.total)} GB</b>: about ${gb(r.need.total * r.gpu_frac)} GB on your graphics card, the rest in RAM.`
      : `Needs <b>${gb(r.need.total)} GB</b>, you have <b>${gb(r.have)} GB</b> for AI.`;
    return where;
  };
  const speedLine = (r) => {
    const w = FIT.speedWords(r.tps[1]);
    const wps = w.wps < 10 ? (Math.round(w.wps * 10) / 10).toFixed(1) : String(Math.round(w.wps));
    return `<span data-speed="${w.key}">Speed: ${esc(w.words)} (about ${wps} words a second)</span>`;
  };
  const CATCH = {
    slow: "Slow here: fine for a short question, tiring for a long chat.",
    snug: "A snug fit: close other apps and browser tabs before you start it.",
    split: 'Part of it runs on the processor (<a class="lxwhat" href="#q-offload" data-open="q-offload">offload</a>), which is what slows it down.',
    smaller: 'Squeezed to fit: this is a smaller version (<a class="lxwhat" href="#q-quant" data-open="q-quant">__Q__</a>), a little less sharp than usual.',
  };
  const catches = (r) => r.catches.map((c) => CATCH[c]).concat(r.smaller ? [CATCH.smaller.replace("__Q__", esc(r.quant))] : []);

  // Groups, in the order the page shows them, already filtered by task. `all` lifts the filter.
  const groups = (rows, tasks, all) => {
    const want = (row) => all || !tasks.length || row.model.tasks.some((t) => tasks.includes(t));
    const shown = rows.filter(want), hidden = rows.length - shown.length;
    const by = (v) => shown.filter((x) => x.r.verdict === v);
    const great = by("great").sort((a, b) => b.model.score - a.model.score);
    const ok = by("ok").sort((a, b) => b.model.score - a.model.score);
    const no = by("no").sort((a, b) => a.r.need.total - b.r.need.total);
    // The pick: the best that runs great; failing that, the best that runs without being slow; failing
    // that, the best that runs at all. Never one that does not fit.
    const best = great[0] || ok.find((x) => !x.r.catches.includes("slow")) || ok[0] || null;
    return {great, ok, no, best, hidden};
  };

  // The command for a route, with a pick's own names filled in. Ollama's library tag for the default
  // quant; any other quant goes through Ollama's Hugging Face route, which takes the GGUF repo and quant.
  const fill = (text, model, quant) => {
    const run = model.run, tag = quant === model.default_q || !run.hf_gguf ? run.ollama : `hf.co/${run.hf_gguf}:${quant}`;
    return text.replace(/\{ollama_tag\}/g, esc(tag)).replace(/\{quant\}/g, esc(quant))
      .replace(/\{hf_gguf\}/g, esc(run.hf_gguf || "")).replace(/\{mlx\}/g, esc(run.mlx || ""))
      .replace(/\{lmstudio\}/g, esc(run.lmstudio));
  };
  // The routes a pick can be run by on an OS, beginner's first. MLX only on a Mac with Apple Silicon.
  const routes = (model, os, apple) => ["lmstudio", "ollama", "llamacpp", "mlx"].filter((k) => {
    const h = D.howto[k];
    if (!h.steps[os]) return false;
    if (k === "llamacpp" && !model.run.hf_gguf) return false;
    if (k === "mlx" && (!apple || !model.run.mlx)) return false;
    return true;
  });
  const defaultRoute = (os) => (os === "linux" ? "ollama" : "lmstudio");

  // GPU guess from the WebGL renderer string, matched on the catalogue's `webgl` tokens. The longest
  // matching token wins, so "rtx 4070 ti super" beats "rtx 4070"; ties are all returned, because "Apple M4"
  // is an Air, a Pro and a mini, and that is the reader's to say.
  const guess = (renderer) => {
    const s = String(renderer || "").toLowerCase();
    let best = 0, out = [];
    for (const rec of D.devices.map((d) => ["device", d]).concat(D.gpus.map((g) => ["gpu", g]))) {
      for (const t of rec[1].webgl || []) {
        if (!s.includes(t)) continue;
        if (t.length > best) { best = t.length; out = []; }
        if (t.length === best && !out.some((o) => o[1].id === rec[1].id)) out.push(rec);
      }
    }
    // A graphics card is a better answer than "an everyday laptop" when both match, which they do on a
    // laptop with a discrete card reporting its integrated GPU's name too.
    return out;
  };

  // The hash. Short keys, because people paste these.
  const KEYS = ["k", "d", "g", "v", "r", "t", "n", "c", "w", "o"];
  const parseHash = (h) => {
    const p = new URLSearchParams(String(h || "").replace(/^#/, "")), s = {};
    for (const k of KEYS) if (p.has(k)) s[k] = p.get(k);
    for (const k of ["v", "r", "c"]) if (s[k] !== undefined) { s[k] = Number(s[k]); if (!isFinite(s[k])) delete s[k]; }
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

  return {esc, gb, norm, hits, search, uaOS, machineOf, machineWords, assess, suggest, reason, speedLine,
          catches, groups, fill, routes, defaultRoute, guess, parseHash, hashOf, DEV, GPU};
})(JSON.parse(document.getElementById("lxdata").textContent), LOCALFIT);

(() => {
  const D = JSON.parse(document.getElementById("lxdata").textContent);
  const U = LOCALUI, esc = U.esc, $ = (id) => document.getElementById(id);
  const UA = navigator.userAgent;
  const VERDICT = {great: ["●", "Runs great"], ok: ["◐", "Runs, with a catch"], no: ["○", "Won’t fit"]};
  const TASKS = Object.fromEntries(D.tasks.map((t) => [t.id, t.label]));
  const OSN = {windows: "Windows", macos: "macOS", linux: "Linux", steamos: "Steam Deck"};
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
        : '<li role="option" aria-disabled="true" aria-selected="false"><span>No match. Try fewer words, or enter it yourself below.</span></li>';
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

  const kindLabel = (k) => (D.kinds.find((x) => x.id === k) || {}).label || "";
  combo($("q"), $("qlist"), (q) => U.search(q, D.devices, S.k).map((d) =>
    ({id: d.id, label: d.name, sub: d.kind !== S.k ? kindLabel(d.kind) : (d.year ? String(d.year) : "")})),
    (it) => chooseDevice(it.id));
  combo($("gq"), $("gqlist"), (q) => U.search(q, D.gpus, null).map((g) =>
    ({id: g.id, label: g.name, sub: g.vram_gb_options.join(" / ") + " GB"})), (it) => chooseGPU(it.id));

  // ---- choices
  const chooseKind = (k) => {
    S.k = k;
    const d = S.d && U.DEV[S.d];
    if (d && d.kind !== k) { delete S.d; delete S.r; $("q").value = ""; }
    paintStep1();
    update();
  };
  const chooseDevice = (id) => {
    S.d = id; delete S.g; delete S.v; S.k = U.DEV[id].kind;
    if (!U.DEV[id].ram_gb_options.includes(S.r)) delete S.r;
    $("q").value = U.DEV[id].name; setCustom(false);
    paintStep1(); update();
  };
  const chooseGPU = (id) => {
    S.g = id; delete S.d; if (!D.custom.ram_gb_options.includes(S.r)) delete S.r;
    $("gq").value = id === "none" ? "" : U.GPU[id].name;
    paintStep1(); update();
  };
  const setCustom = (on) => { $("customb").hidden = !on; $("custom").setAttribute("aria-expanded", String(on)); };

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
    const devs = D.devices.filter((d) => d.kind === S.k);
    $("devf").hidden = !devs.length;
    $("qlab").textContent = `Which ${kindLabel(S.k).toLowerCase()}? Start typing its name`;
    const pop = devs.filter((d) => d.popular).slice(0, 8);
    $("pop").innerHTML = pop.length ? '<span class="lxpl">Popular:</span>' + pop.map((d) =>
      `<button class="chip" type="button" data-dev="${esc(d.id)}" aria-pressed="${S.d === d.id}">${esc(d.name)}</button>`).join("") : "";
    if (!devs.length || S.g) setCustom(true);
    const mc = U.machineOf(S, UA);
    $("nogpu").setAttribute("aria-pressed", String(S.g === "none"));
    // VRAM, only for a card sold in more than one size.
    const g = S.g && U.GPU[S.g];
    $("vramf").hidden = !(g && g.vram_gb_options.length > 1);
    if (g && g.vram_gb_options.length > 1)
      radios($("vramo"), "vram", g.vram_gb_options, mc.m.vram_gb, (o) => `${o} GB`, (v) => { S.v = v; paintStep1(); update(); refocus("input[name=vram]:checked"); });
    // RAM, for anything resolved that has a choice.
    $("ramf").hidden = !(mc && mc.ram_opts.length > 1);
    if (mc && mc.ram_opts.length > 1)
      radios($("ramo"), "ram", mc.ram_opts, mc.m.ram_gb, (o) => `${o} GB`, (r) => { S.r = r; paintStep1(); update(); refocus("input[name=ram]:checked"); });
    // Always from the state, so a hash change (a shared link opened in this tab) cannot leave the box
    // naming the previous machine. Typing never reaches here, so nothing a reader is typing is overwritten.
    $("q").value = S.d && U.DEV[S.d] ? U.DEV[S.d].name : "";
    $("gq").value = S.g && U.GPU[S.g] ? U.GPU[S.g].name : "";
    $("gores").hidden = !mc;
    const sum = $("s1sum");
    sum.hidden = !mc;
    if (mc) sum.textContent = mc.custom ? `${mc.name} · ${mc.m.ram_gb} GB RAM` : `${mc.name} · ${mc.m.ram_gb} GB`;
  };

  // ---- results
  const card = (row, mc, open) => {
    const {model, r} = row, v = VERDICT[r.verdict];
    const lines = r.verdict === "no" ? [] : U.catches(r);
    const tasks = model.tasks.map((t) => TASKS[t]).filter(Boolean).join(", ");
    const hf = model.hf ? ` · ${Number(model.hf.downloads || 0).toLocaleString("en")} downloads` : "";
    return `<li class="lxcard" data-model="${esc(model.id)}" data-verdict="${r.verdict}">` +
      `<div class="lxch"><h4>${esc(model.name)}</h4><span class="lxv" data-v="${r.verdict}"><i aria-hidden="true">${v[0]}</i>${v[1]}</span></div>` +
      `<p class="lxblurb">${esc(model.blurb)}</p>` +
      `<p class="lxwhy"><span>${U.reason(mc.m, r)}</span>${r.tps ? U.speedLine(r) : ""}</p>` +
      (lines.length ? `<ul class="lxcatch">${lines.map((l) => `<li>${l}</li>`).join("")}</ul>` : "") +
      `<p class="lxmeta">Good for: ${esc(tasks)} · Licence: ${esc(model.license)}${hf}</p>` +
      (S.n ? numbers(row, mc) : "") +
      (r.verdict === "no" ? "" :
        `<button class="lxhow" type="button" aria-expanded="${open ? "true" : "false"}" aria-controls="how-${esc(model.id)}" data-how="${esc(model.id)}">How to run it</button>` +
        `<div class="lxhowb" id="how-${esc(model.id)}"${open ? "" : " hidden"}>${open ? howto(model, r, mc) : ""}</div>`) +
      "</li>";
  };

  const numbers = (row, mc) => {
    const {model, r} = row, n = r.need, gb = U.gb;
    const where = {gpu: mc.m.unified ? "all in shared memory" : "all on the graphics card", cpu: "on the processor",
                   split: `split: ${Math.round(r.gpu_frac * 100)}% on the graphics card, the rest on the processor`}[r.place] || "doesn't fit";
    const qs = model.quants.map((q) => `<option value="${esc(q.q)}"${q.q === r.quant ? " selected" : ""}>${esc(q.q)} (${gb(q.gb)} GB)</option>`).join("");
    return `<dl class="lxnums">` +
      `<dt>Version</dt><dd><label class="sr" for="qv-${esc(model.id)}">Quantisation for ${esc(model.name)}</label>` +
      `<select id="qv-${esc(model.id)}" data-quant="${esc(model.id)}">${qs}</select></dd>` +
      `<dt>Weights</dt><dd>${gb(n.weights)} GB</dd>` +
      `<dt>Context cache</dt><dd>${gb(n.kv)} GB at ${(r.ctx / 1024) | 0}k tokens</dd>` +
      `<dt>Working memory</dt><dd>${gb(n.overhead)} GB</dd>` +
      `<dt>Total</dt><dd>${gb(n.total)} GB of ${gb(r.have)} GB${r.tps ? ` (${Math.round(r.headroom * 100)}% to spare)` : ""}</dd>` +
      `<dt>Runs</dt><dd>${where}</dd>` +
      (r.tps ? `<dt>Speed</dt><dd>${r.tps[0].toFixed(0)}–${r.tps[2].toFixed(0)} tokens/s (estimate)</dd>` : "") +
      `<dt>Size</dt><dd>${model.params_b}B parameters${model.active_b < model.params_b ? `, ${model.active_b}B active per token` : ""}</dd>` +
      `</dl>`;
  };

  const howto = (model, r, mc) => {
    const apple = mc.m.unified && mc.m.backend === "metal";
    const os = S.o && D.howto.ollama.steps[S.o] ? S.o : mc.os;
    const rs = U.routes(model, os, apple);
    const route = rs.includes(S.w) ? S.w : (rs.includes(U.defaultRoute(os)) ? U.defaultRoute(os) : rs[0]);
    const h = D.howto[route];
    const oses = ["windows", "macos", "linux", "steamos"];
    const steps = h.steps[os].map((st) => Array.isArray(st)
      ? `<div class="lxcmd"><code>${U.fill(st[1], model, r.quant)}</code><button class="lxcopy" type="button" data-copy>Copy</button></div>`
      : `<li>${U.fill(st, model, r.quant)}</li>`);
    // Commands sit inside the step before them, so the list numbers stay the steps a person does.
    const ol = [];
    for (const s of steps) { if (s.startsWith("<li>")) ol.push(s); else if (ol.length) ol[ol.length - 1] = ol[ol.length - 1].replace(/<\/li>$/, s + "</li>"); else ol.push(`<li>${s}</li>`); }
    const size = model.quants.find((q) => q.q === r.quant).gb, mins = Math.max(1, Math.round(size * 8000 / 50 / 60));
    return `<div class="lxroutes" role="group" aria-label="How to run it"><span class="lxpl">Use</span>` +
      rs.map((k) => `<button class="chip" type="button" data-route="${k}" aria-pressed="${k === route}">${esc(D.howto[k].label)}</button>`).join("") + `</div>` +
      `<p class="lxpitch">${esc(h.pitch)}</p>` +
      `<div class="lxroutes" role="group" aria-label="Your operating system"><span class="lxpl">On</span>` +
      oses.filter((o) => h.steps[o]).map((o) => `<button class="chip" type="button" data-os="${o}" aria-pressed="${o === os}">${OSN[o]}</button>`).join("") + `</div>` +
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
    const mc = U.machineOf(S, UA), out = $("results");
    if (!mc) { $("mach").textContent = "Pick your computer above and the answers appear here."; out.innerHTML = ""; return; }
    $("mach").innerHTML = U.machineWords(mc);
    const g = U.groups(U.assess(mc.m, ctx, qover), S.t, showAll);
    // The pick's how-to opens by itself, because most readers should stop there. When the pick changes, the
    // old one's panel closes with it, unless the reader opened it themselves.
    const bestId = g.best && g.best.model.id;
    if (bestId !== autoBest) { if (autoBest) opened.delete(autoBest); if (bestId) opened.add(bestId); autoBest = bestId; }
    const list = (rows) => `<ul class="lxcards">${rows.map((x) => card(x, mc, opened.has(x.model.id) && x.model.id !== bestId)).join("")}</ul>`;
    const greatRest = g.great.filter((x) => x.model.id !== bestId);
    const cap = moreGreat ? greatRest.length : 5;
    let html = "";
    if (g.best) html += `<div class="lxbest" id="best"><p>Our pick for you</p><ul class="lxcards">${card(g.best, mc, opened.has(bestId))}</ul></div>`;
    else html += `<p class="lxnote">Nothing we recommend fits on this machine as it is. The smallest models need about 1.5 GB free; see what would make one fit below.</p>`;
    if (S.t.length || g.hidden) html += `<p class="lxnote">` + (S.t.length && !showAll
      ? `Showing models good for ${esc(S.t.map((t) => TASKS[t].toLowerCase()).join(" or "))}. ${g.hidden} others hidden. <button class="lxlink" type="button" id="showall">Show all models</button>`
      : `Showing every model. <button class="lxlink" type="button" id="showall">Only ${esc(S.t.map((t) => TASKS[t].toLowerCase()).join(" or "))}</button>`) + "</p>";
    if (greatRest.length) html += `<section class="lxgroup" aria-labelledby="hg"><h3 id="hg"><span aria-hidden="true">${VERDICT.great[0]}</span> ${g.best && g.best.r.verdict === "great" ? "Also runs great" : "Runs great"} <span class="ct">${greatRest.length}</span></h3>${list(greatRest.slice(0, cap))}` +
      (greatRest.length > cap ? `<p class="lxmore"><button class="chip" type="button" id="moregreat">Show ${greatRest.length - cap} more</button></p>` : "") + "</section>";
    const okRest = g.ok.filter((x) => x.model.id !== bestId);
    if (okRest.length) html += `<section class="lxgroup" aria-labelledby="ho"><h3 id="ho"><span aria-hidden="true">${VERDICT.ok[0]}</span> Runs, with a catch <span class="ct">${okRest.length}</span></h3>${list(okRest)}</section>`;
    if (g.no.length) html += `<details class="lxgroup lxnofit" id="nofit"><summary><span aria-hidden="true">${VERDICT.no[0]}</span> ${g.no.length} bigger model${g.no.length === 1 ? "" : "s"} won’t fit</summary>${list(g.no)}</details>`;
    const wasOpen = $("nofit") && $("nofit").open;
    out.innerHTML = html;
    if (wasOpen && $("nofit")) $("nofit").open = true;
    $("live").textContent = `For ${mc.name} with ${mc.m.ram_gb} GB: ${g.great.length} run great, ${g.ok.length} with a catch, ${g.no.length} won’t fit.` +
      (g.best ? ` Our pick is ${g.best.model.name}.` : "");
  };

  // ---- events, delegated, so re-rendered cards need no re-wiring
  // No focus move on change: arrow keys walk a radio group by changing it, and stealing focus to the search
  // box on every arrow press would make the tiles impossible to browse by keyboard. The search is next in
  // tab order anyway.
  document.querySelectorAll("input[name=kind]").forEach((i) => i.addEventListener("change", () => chooseKind(i.value)));
  $("gobtn").addEventListener("click", () => { $("s3").scrollIntoView({block: "start", behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth"}); $("s3h").focus({preventScroll: true}); });
  $("pick").addEventListener("click", (e) => { const b = e.target.closest("[data-dev]"); if (b) chooseDevice(b.dataset.dev); });
  $("custom").addEventListener("click", () => { const on = $("customb").hidden; setCustom(on); if (on) $("gq").focus(); });
  $("nogpu").addEventListener("click", () => chooseGPU("none"));
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
      if (open) { opened.add(id); const mc = U.machineOf(S, UA); const row = U.assess(mc.m, S.c || D.default_ctx, qover).find((x) => x.model.id === id); panel.innerHTML = howto(row.model, row.r, mc); }
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

  // ---- help me find out
  const findOS = (os) => {
    $("fos").innerHTML = ["windows", "macos", "linux", "steamos"].map((o) =>
      `<button class="chip" type="button" data-fos="${o}" aria-pressed="${o === os}">${OSN[o]}</button>`).join("");
    $("fsteps").innerHTML = D.find_out[os].map((s) => `<li>${esc(s)}</li>`).join("");
  };
  $("fos").addEventListener("click", (e) => { const b = e.target.closest("[data-fos]"); if (b) { findOS(b.dataset.fos); b.focus(); refocus(`[data-fos="${b.dataset.fos}"]`); } });
  findOS(U.uaOS(UA));
  $("guess").addEventListener("click", () => {
    let renderer = "";
    try {
      const gl = document.createElement("canvas").getContext("webgl");
      const ext = gl && gl.getExtension("WEBGL_debug_renderer_info");
      renderer = gl ? gl.getParameter(ext ? ext.UNMASKED_RENDERER_WEBGL : gl.RENDERER) : "";
    } catch (e) {}
    const found = U.guess(renderer), out = $("guessout");
    const mem = navigator.deviceMemory ? ` Your browser also says you have at least ${navigator.deviceMemory} GB of memory (it never reports more than 8).` : "";
    if (!found.length) {
      out.innerHTML = `Your browser didn’t name a graphics chip we know${renderer ? ` (it said “${esc(renderer)}”)` : ""}. The steps below will tell you.${esc(mem)}`;
      return;
    }
    out.innerHTML = `Looks like: ` + found.map(([t, r]) => `<button class="chip" type="button" data-guess="${t}:${esc(r.id)}">${esc(r.name)}</button>`).join("") +
      ` Tap the right one to use it.${esc(mem)}`;
  });
  $("guessout").addEventListener("click", (e) => {
    const b = e.target.closest("[data-guess]");
    if (!b) return;
    const [t, id] = b.dataset.guess.split(":");
    if (t === "device") { S.k = U.DEV[id].kind; chooseDevice(id); }
    else { if (!S.k || S.k === "mac" || S.k === "handheld") S.k = "gaming"; setCustom(true); chooseGPU(id); }
    refocus("#s3h");
  });

  addEventListener("hashchange", () => { S = U.parseHash(location.hash); paintStep1(); update(); });
  paintStep1(); update();
})();
