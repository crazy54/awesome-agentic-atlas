// LOOKALIKES: paste a GitHub or GitLab link, or type a project's name, and see the projects that do the same
// thing. `scripts/33_alike.py` inlines this file into `docs/alike/index.html`, after `scripts/semantic.js`,
// whose `semTokens`, `semEncode` and `semDecode` it calls.
//
// Two halves. `ALIKE` is pure: it takes the rows and the decoded index and answers questions -- what did the
// reader paste, which row is it, what is like it, and why -- with no DOM, no fetch and no clock it was not
// handed. `tests/alike-probe.mjs` runs exactly this object under node against the committed `docs/`, which is
// where the ranking's quality is held to account, and `tests/alike-check.mjs` drives the second half -- the
// wiring below it -- in a real browser.
//
// HOW "SIMILAR" IS SCORED, AND WHY EACH TERM IS THERE. Every weight below was the other way round first, and
// the corpus argued. Scored by hand against 32 well-known projects across the fourteen categories, reading
// each one's top ten; the same-category share is quoted beside each step only as a coarse signal, because
// the category is a curator's label and the honest measure is whether the list reads right. The table in the
// pull request that introduced this page is the long form.
//
//   * The README vector alone -- a cosine over `docs.bin`, which is what `near.bin` already precomputes --
//     is what "more like this" would naively be, and it is poor for exactly the famous projects a reader
//     brings: 76 of 320 top-ten slots shared the project's category. `docs.bin` indexes up to 2,000
//     characters of each README, and READMEs open with badges, install lines and "local-first, works with
//     Claude Code and Codex", which makes every coding tool look like every other. Aider's ten nearest were
//     a Chinese orchestration system, an Android harness and a video tool.
//   * So each row also gets a vector of its own name and one-line blurb, encoded here with the same encoder
//     the search box uses, and the two cosines are averaged. The blurb is what a curator wrote to say what a
//     project is, which is the question being asked. 103 of 320 on its own; equal weights measured no worse
//     than any split from 0.4 to 0.7.
//   * Sharing the curated category adds a fixed 0.08 -- about the gap between a good neighbour and a merely
//     plausible one -- and took the same-category count to 242. Not more, because the category can be wrong:
//     `anthropics/claude-code` is filed under Orchestrators with a blurb copied from a plugin, and a heavier
//     boost hands its whole list to Ralph-loop orchestrators. A project the atlas does not hold has no
//     category, so the preference is *voted* instead: the categories of its thirty nearest rows, by share.
//     Voting was tried for in-atlas rows too and measured worse (198 against 253), so a curated label wins
//     where there is one.
//   * Shared words, by damped IDF, the way `27_semantic.py` weights tokens: sqrt(log(n / df)), so "agent" in
//     every other blurb counts for almost nothing and "tracing" or "vector" counts. This is what lifts
//     Helicone and Opik to the top for Langfuse.
//   * A small star prior, 0.01 per decade. Stars are not similarity, and at 0.02 they started to pull
//     AutoGPT into mem0's list; at 0.01 they break ties toward projects people have actually heard of, which
//     is most of what "an alternative" means.
//   * A blurb that calls itself an "alternative to <this>" is lifted by 0.15: it is the one sentence that
//     answers the question outright.
//   * Built on or around it is not an alternative. A row from the same owner, or whose own name contains
//     this project's name (`langfuse-mcp`, `llm-ollama`, `claude-code-action`), is ecosystem: it is moved to
//     a short list of its own rather than ranked against the alternatives. Matching names in the *blurb*
//     was tried and rejected: half of all coding agents describe themselves as "like Claude Code", and that
//     rule threw out exactly the alternatives the reader came for.
//   * Blurbs from one source list end in a run of link labels -- "github | website | docs | discord" -- and
//     those six words made mem0, LlamaIndex and SuperAGI each other's nearest neighbours. They are stripped
//     before encoding (`cleanBlurb`).
//
// Cutoffs are ranks, never similarities, for the reason `27_semantic.py` gives: an absolute threshold is
// fitted to one corpus size, and this corpus has grown eightfold in two months.
const ALIKE = (() => {
  const W = {doc: 0.5, blurb: 0.5, cat: 0.08, targets: 0.03, terms: 0.3, stars: 0.01, alt: 0.15};
  const VOTE = 30;        // nearest rows whose categories vote, for a project the atlas does not hold
  const SHOW = 24;        // lookalikes listed
  const ECO = 6;          // "built on or around it" listed
  const TERMS = 3;        // shared words named in each "why"
  // A word in more than this share of blurbs is not named as a reason. It still scores, by its small weight;
  // it is just not a reason a reader would accept. 5% was tried first and let "llm" (4.8% of blurbs), "tool"
  // (4.4%) and "one" (3.5%) through as the stated reason on a third of Langfuse's list; at 2% the reasons
  // read "observability, traces, evals", which is what the reader would have said themselves.
  const TERM_DF = 0.02;
  // A single-word project name more common than this in blurbs ("agents", "skills") is too generic to mark
  // another row as built around it.
  const NAME_DF = 0.02;
  const ACTIVE_DAYS = 183;
  const LINKS = "(?:github profile|github|website|docs|discord|twitter|x|linkedin|demo|blog|npm|youtube|paper|" +
    "reddit|announcement|twitter announcement|reddit announcement|web|issue tracker|huggingface)";
  const TAIL = new RegExp("(?:\\s+" + LINKS + "\\s*\\|)+\\s*" + LINKS + "\\s*$|\\s+" + LINKS + "\\s*\\|?\\s*$", "i");
  const LINKWORDS = new Set(["github", "website", "docs", "discord", "twitter", "linkedin", "demo", "blog", "npm",
    "youtube", "paper", "reddit", "announcement", "profile", "huggingface"]);
  const TERM = /[a-z0-9][a-z0-9+#-]*[a-z0-9+#]|[a-z0-9]/g;
  // Words rare enough to pass TERM_DF that still say nothing about what a project does -- the vocabulary of
  // blurbs rather than of software. Read off the reasons drawn for the 32 hand-checked projects: "various,
  // applications, large" was mem0's stated reason for SuperAgent. They still score; they are only never
  // *named* as the reason.
  const VAGUE = new Set(("various applications application large enabling enables facilitating providing provides " +
    "rather within without treating clearest seamless seamlessly practical built around single support supports state " +
    "execution design reference official capability capabilities features feature mode layer leveraging designed " +
    "offering offers easy including turns full interface efficient complex cutting-edge example examples format author " +
    "software engineering structure building implementation multiple library streaming behaviors task tasks enhancing " +
    "relevance collaboration development powerful simple lightweight modern based ready production-ready").split(" "));

  const cleanBlurb = (b) => String(b || "").replace(TAIL, "").trim();
  const norm = (s) => String(s || "").toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
  const escRe = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

  // ------------------------------------------------------------------ what did the reader paste
  // One of: a repository on GitHub or GitLab (from a URL in any of the shapes people copy, or a bare
  // `owner/name`), a link that is not a repository, or words. Never a network question: this only reads the
  // string, so it is what the probe asserts every URL shape against.
  function parseInput(raw) {
    let s = String(raw || "").trim();
    if (!s) return {kind: "empty"};
    // `git@github.com:owner/repo.git`, the SSH form a reader copies from the clone button.
    const ssh = s.match(/^git@(github\.com|gitlab\.com):(.+)$/i);
    if (ssh) s = "https://" + ssh[1] + "/" + ssh[2];
    const m = s.match(/^(?:(?:https?:)?\/\/)?(?:www\.)?(github\.com|gitlab\.com)(?:\/(.*))?$/i);
    if (m) {
      const host = m[1].toLowerCase();
      let path = (m[2] || "").split(/[?#]/)[0];
      let parts = path.split("/").filter(Boolean);
      if (host === "gitlab.com") {
        // GitLab puts everything that is not the project behind `/-/`: trees, blobs, issues, merge requests.
        const dash = parts.indexOf("-");
        if (dash >= 0) parts = parts.slice(0, dash);
      } else {
        parts = parts.slice(0, 2);
      }
      if (parts.length) parts[parts.length - 1] = parts[parts.length - 1].replace(/\.git$/i, "");
      parts = parts.filter(Boolean);
      if (parts.length < 2) return {kind: "notrepo", host, path: parts.join("/")};
      const p = parts.join("/");
      return {kind: "repo", host, path: p, nwo: host === "github.com" ? p : host + "/" + p};
    }
    // A bare `owner/name`, which is how GitHub names a repository everywhere. One slash, no spaces, and the
    // characters GitHub allows -- anything else is words that happen to contain a slash ("ci/cd tools").
    const bare = s.replace(/\.git$/i, "").replace(/\/+$/, "");
    if (/^[A-Za-z0-9-]+\/[A-Za-z0-9._-]+$/.test(bare) && !/^\.+$/.test(bare.split("/")[1]))
      return {kind: "repo", host: "github.com", path: bare, nwo: bare, bare: true};
    return {kind: "words", text: s};
  }

  // ------------------------------------------------------------------ the index
  // Everything the ranking reads, built once from `data.json` and (when it decoded) the semantic index. `sem`
  // may be null: a stale or missing index leaves the page working on words and categories alone, and says so.
  function build(d, sem) {
    const cols = d.cols, n = d.rows.length;
    const at = Object.fromEntries(cols.map((c, i) => [c, i]));
    const rows = d.rows.map((a, i) => ({
      i, name: a[at.name], nwo: a[at.nwo], cat: a[at.cat], targets: a[at.targets] || [], stars: a[at.stars] || 0,
      blurb: a[at.blurb] || "", lang: a[at.lang] || "", pushed: a[at.pushed] || "", url: a[at.url] || "",
    }));
    const stop = sem ? sem.stop : new Set();
    const by = new Map(rows.map((r) => [r.nwo.toLowerCase(), r.i]));
    const terms = rows.map((r) => termsOf(r.name + " " + cleanBlurb(r.blurb), stop));
    const df = new Map();
    for (const t of terms) for (const w of t) df.set(w, (df.get(w) || 0) + 1);
    const wt = new Map();
    for (const [w, c] of df) wt.set(w, Math.sqrt(Math.log(n / (1 + c))));
    const lstars = new Float32Array(n);
    rows.forEach((r, i) => { lstars[i] = Math.log10(r.stars + 1); });
    // The name a row goes by, normalised, for both the resolver and the ecosystem rule: its display name and
    // the last segment of its path, which differ for 40% of rows ("Codex CLI" is `openai/codex`).
    const names = rows.map((r) => {
      const repo = r.nwo.split("/").pop();
      return {name: norm(r.name), repo: norm(repo), nwo: norm(r.nwo), owner: ownerOf(r.nwo)};
    });
    const ix = {d, sem, n, rows, by, terms, df, wt, lstars, names, stop,
                cats: d.cats.map((c) => c.name), targets: d.targets.map((t) => t.name)};
    if (sem) {
      const dims = sem.dims;
      ix.dims = dims;
      // The README vectors, unit length. `docs.bin` is unit length before quantisation and not after, so the
      // norm is taken again rather than assumed.
      const U = new Float32Array(n * dims);
      for (let i = 0; i < n; i++) {
        let s = 0;
        for (let k = 0; k < dims; k++) { const v = sem.docs[i * dims + k]; s += v * v; }
        const inv = s ? 1 / Math.sqrt(s) : 0;
        for (let k = 0; k < dims; k++) U[i * dims + k] = sem.docs[i * dims + k] * inv;
      }
      // The blurb vectors: name and cleaned blurb, through the shared encoder. About 11k encodings of two
      // dozen tokens, which is tens of milliseconds once and nothing per search.
      const B = new Float32Array(n * dims);
      rows.forEach((r, i) => {
        const v = semEncode(sem, r.name + " " + cleanBlurb(r.blurb));
        if (v) B.set(v, i * dims);
      });
      ix.U = U; ix.B = B;
    }
    return ix;
  }

  function ownerOf(nwo) {
    const parts = String(nwo).toLowerCase().split("/");
    return parts[0].includes(".") ? parts[0] + "/" + parts[1] : parts[0];
  }

  function termsOf(text, stop) {
    const out = new Set();
    for (const w of String(text).toLowerCase().match(TERM) || []) {
      if (w.length < 3 || /^\d+$/.test(w) || stop.has(w) || LINKWORDS.has(w)) continue;
      out.add(w);
    }
    return out;
  }

  // ------------------------------------------------------------------ which row is it
  // An exact `nwo` first. Otherwise the words are a project's name if they are one: exact on the display name
  // or the repository's own name, then a prefix, then every word present. "claude code" is the case this was
  // written against -- `anthropics/claude-code` and a dozen forks all normalise to it, and the reader means
  // the one with 154,000 stars, not a fork with four.
  function resolve(ix, raw) {
    const p = parseInput(raw);
    if (p.kind === "empty" || p.kind === "notrepo") return p;
    if (p.kind === "repo") {
      const i = ix.by.get(p.nwo.toLowerCase());
      if (i !== undefined) return {kind: "hit", i, input: p};
      // A bare `owner/name` that the atlas does not hold is probably a repository; it is looked up rather
      // than searched as words, and the caller falls back to words if GitHub says no.
      return {kind: "external", host: p.host, path: p.path, nwo: p.nwo, bare: !!p.bare};
    }
    const q = norm(p.text);
    if (!q) return {kind: "words", text: p.text};
    const toks = q.split(" ");
    const exact = [], prefix = [], loose = [];
    for (let i = 0; i < ix.n; i++) {
      const nm = ix.names[i];
      if (nm.name === q || nm.repo === q || nm.nwo === q) exact.push(i);
      else if (nm.name.startsWith(q + " ") || nm.repo.startsWith(q + " ") || nm.name.startsWith(q) && q.length >= 4)
        prefix.push(i);
      else if (toks.length > 1 && toks.every((t) => (" " + nm.name + " " + nm.nwo + " ").includes(" " + t)))
        loose.push(i);
    }
    const byStars = (a, b) => ix.rows[b].stars - ix.rows[a].stars;
    exact.sort(byStars); prefix.sort(byStars); loose.sort(byStars);
    // Obvious when there is one exact match, or when the best-known exact match has ten times the stars of
    // the next one: a reader typing "claude code" is not asking about a fork.
    if (exact.length === 1 || (exact.length > 1 && ix.rows[exact[0]].stars >= 10 * Math.max(1, ix.rows[exact[1]].stars)))
      return {kind: "hit", i: exact[0], input: p, also: exact.slice(1, 4)};
    const choices = [...exact, ...prefix, ...loose].slice(0, 6);
    if (choices.length) return {kind: "choose", choices, text: p.text};
    return {kind: "words", text: p.text};
  }

  // ------------------------------------------------------------------ what is it, as something to rank against
  function sourceRow(ix, i) {
    const r = ix.rows[i];
    const src = {kind: "row", i, cat: r.cat, targets: new Set(r.targets), terms: ix.terms[i], label: r.name,
                 owner: ix.names[i].owner, names: nameKeys(ix, [r.name, r.nwo.split("/").pop()])};
    if (ix.sem) {
      src.doc = ix.U.subarray(i * ix.dims, (i + 1) * ix.dims);
      src.blurb = ix.B.subarray(i * ix.dims, (i + 1) * ix.dims);
    }
    src.altRe = altRe(src.names);
    return src;
  }

  // A project the atlas does not hold, from what its forge says about it: name, description and topics for
  // the blurb side, and its README -- cleaned the way `27_semantic.py` cleans one -- for the README side, so
  // the two halves of the score are compared like with like. Without a README both sides use the blurb,
  // which measured as agreeing with the in-atlas answer on 126 of 320 top-ten slots against 157 with one.
  function sourceRepo(ix, info) {
    const topics = (info.topics || []).join(" ");
    const blurbText = info.name + " " + cleanBlurb(info.description) + " " + topics.replace(/-/g, " ");
    const src = {kind: "external", i: -1, cat: null, targets: new Set(), label: info.name,
                 terms: termsOf(blurbText, ix.stop), owner: ownerOf(info.nwo),
                 names: nameKeys(ix, [info.name, info.nwo.split("/").pop()])};
    if (ix.sem) {
      src.blurb = semEncode(ix.sem, blurbText);
      const body = info.readme ? readmeText(info.readme) : "";
      src.doc = body ? semEncode(ix.sem, info.name + " " + (info.language || "") + " " + blurbText + " " + body) : src.blurb;
    }
    src.altRe = altRe(src.names);
    return src;
  }

  // A description the reader typed. No owner, no name, so no ecosystem: everything is a candidate.
  function sourceText(ix, text) {
    const src = {kind: "text", i: -1, cat: null, targets: new Set(), terms: termsOf(text, ix.stop), label: text,
                 owner: null, names: [], altRe: null};
    if (ix.sem) src.doc = src.blurb = semEncode(ix.sem, text);
    return src;
  }

  function readmeText(md) {
    return String(md).replace(/```[\s\S]*?```/g, " ").replace(/!?\[([^\]]*)\]\([^)]*\)/g, "$1")
      .replace(/<[^>]+>/g, " ").replace(/[#>*_`|\-]+/g, " ").replace(/\s+/g, " ").slice(0, 2000);
  }

  function nameKeys(ix, list) {
    const out = new Set();
    for (const raw of list) {
      const k = norm(raw);
      if (k.length < 3) continue;
      // A single common word is not a name another project can be "built around": `wshobson/agents` would
      // otherwise claim every row with "agents" in its name.
      if (!k.includes(" ") && (ix.df.get(k) || 0) > ix.n * NAME_DF) continue;
      out.add(k);
    }
    return [...out];
  }

  function altRe(names) {
    if (!names.length) return null;
    const alt = names.map((k) => escRe(k).replace(/ /g, "[\\s._-]+")).join("|");
    return new RegExp("(?:alternative|replacement|substitute|clone)s?\\s+(?:to|for|of)\\s+(?:the\\s+)?(?:" + alt +
      ")(?![a-z0-9])|(?:^|[^a-z0-9])(?:" + alt + ")[\\s-]+(?:alternative|clone|replacement)", "i");
  }

  // Ecosystem: same owner, or this row's own name contains the source's name as whole words.
  function isEco(ix, src, j) {
    if (src.kind === "text") return false;
    const nm = ix.names[j];
    if (src.owner && nm.owner === src.owner) return true;
    for (const k of src.names) {
      const hay = " " + nm.name + " " + nm.repo + " ";
      if (hay.includes(" " + k + " ")) return true;
    }
    return false;
  }

  // ------------------------------------------------------------------ the ranking
  // Every row scored; the caller filters and slices, so a filter never re-ranks and never needs a second pass.
  function rank(ix, src) {
    const n = ix.n, s = new Float32Array(n), dims = ix.dims;
    const useVec = !!(ix.sem && src.doc && src.blurb);
    let tot = 0;
    for (const w of src.terms) tot += ix.wt.get(w) || 0;
    tot = tot || 1;
    for (let j = 0; j < n; j++) {
      let v = 0;
      if (useVec) {
        let a = 0, b = 0;
        const base = j * dims;
        for (let k = 0; k < dims; k++) { a += src.doc[k] * ix.U[base + k]; b += src.blurb[k] * ix.B[base + k]; }
        v = W.doc * a + W.blurb * b;
      }
      let lex = 0;
      const tj = ix.terms[j];
      for (const w of src.terms) if (tj.has(w)) lex += ix.wt.get(w) || 0;
      v += W.terms * lex / tot + W.stars * ix.lstars[j];
      if (src.targets.size) {
        const tg = ix.rows[j].targets;
        let inter = 0;
        for (const t of tg) if (src.targets.has(t)) inter++;
        const uni = src.targets.size + tg.length - inter;
        if (uni) v += W.targets * inter / uni;
      }
      s[j] = v;
    }
    if (src.i >= 0) s[src.i] = -Infinity;
    // The category preference: the curated one where there is one, otherwise the vote of the nearest rows.
    const pref = new Float32Array(ix.cats.length);
    if (src.cat !== null && src.cat !== undefined) pref[src.cat] = 1;
    else {
      const top = topK(s, VOTE);
      for (const j of top) pref[ix.rows[j].cat] += 1 / top.length;
    }
    for (let j = 0; j < n; j++) s[j] += W.cat * pref[ix.rows[j].cat];
    const alt = new Uint8Array(n), eco = new Uint8Array(n);
    for (let j = 0; j < n; j++) {
      if (j === src.i) continue;
      if (src.altRe && src.altRe.test(ix.rows[j].blurb)) { alt[j] = 1; s[j] += W.alt; }
      else if (isEco(ix, src, j)) eco[j] = 1;
    }
    const order = [...Array(n).keys()].filter((j) => j !== src.i && isFinite(s[j]))
      .sort((a, b) => s[b] - s[a] || a - b);
    const main = order.filter((j) => !eco[j]), around = order.filter((j) => eco[j]);
    let lead = 0;
    for (let c = 1; c < pref.length; c++) if (pref[c] > pref[lead]) lead = c;
    return {score: s, main, around, alt, pref, lead, vectors: useVec};
  }

  function topK(s, k) {
    const idx = [...Array(s.length).keys()].filter((j) => isFinite(s[j]));
    idx.sort((a, b) => s[b] - s[a]);
    return idx.slice(0, k);
  }

  // The reader's three filters, over an order `rank` produced. `now` is passed, never read, so a test can pin it.
  function filter(ix, order, f, now) {
    const since = now - ACTIVE_DAYS * 86400000;
    return order.filter((j) => {
      const r = ix.rows[j];
      if (f.lang && r.lang !== f.lang) return false;
      if (f.stars && r.stars < f.stars) return false;
      if (f.active && !(r.pushed && Date.parse(r.pushed) >= since)) return false;
      return true;
    });
  }

  // Why row `j` is on the list, in the reader's terms: the category, the harnesses they share, the words.
  function why(ix, src, res, j) {
    const r = ix.rows[j], out = {cat: null, targets: [], terms: [], alt: !!res.alt[j]};
    const want = src.cat !== null && src.cat !== undefined ? src.cat : res.lead;
    if (r.cat === want) out.cat = ix.cats[r.cat];
    for (const t of r.targets) if (src.targets.has(t)) out.targets.push(ix.targets[t]);
    const shared = [];
    for (const w of src.terms) {
      if (ix.terms[j].has(w) && !VAGUE.has(w) && (ix.df.get(w) || 0) <= ix.n * TERM_DF) shared.push(w);
    }
    shared.sort((a, b) => (ix.wt.get(b) || 0) - (ix.wt.get(a) || 0) || (a < b ? -1 : 1));
    out.terms = shared.slice(0, TERMS);
    return out;
  }

  // The languages worth offering in the filter: those among the first hundred lookalikes, most common first.
  function languages(ix, order) {
    const c = new Map();
    for (const j of order.slice(0, 100)) { const l = ix.rows[j].lang; if (l) c.set(l, (c.get(l) || 0) + 1); }
    return [...c].sort((a, b) => b[1] - a[1] || (a[0] < b[0] ? -1 : 1)).map(([l]) => l);
  }

  // ------------------------------------------------------------------ the forges
  // Anonymous, from the reader's browser, because this site has no server: GitHub allows sixty of these an
  // hour per visitor, GitLab more. The README comes from raw.githubusercontent.com, which is not rate-limited
  // at all, so a lookup costs one of the sixty and not two.
  function apiURL(host, path) {
    return host === "gitlab.com"
      ? "https://gitlab.com/api/v4/projects/" + encodeURIComponent(path)
      : "https://api.github.com/repos/" + path.split("/").map(encodeURIComponent).join("/");
  }
  function readmeURL(host, info) {
    return host === "gitlab.com"
      ? "https://gitlab.com/api/v4/projects/" + encodeURIComponent(info.path) + "/repository/files/README.md/raw?ref=" +
        encodeURIComponent(info.branch || "HEAD")
      : "https://raw.githubusercontent.com/" + info.path + "/" + encodeURIComponent(info.branch || "HEAD") + "/README.md";
  }
  // The two forges' answers in one shape.
  function fromAPI(host, j) {
    if (host === "gitlab.com") {
      const path = j.path_with_namespace;
      return {host, path, nwo: "gitlab.com/" + path, name: j.name || path.split("/").pop(), description: j.description || "",
              topics: j.topics || j.tag_list || [], language: "", stars: j.star_count || 0, pushed: (j.last_activity_at || "").slice(0, 10),
              url: j.web_url, branch: j.default_branch, archived: !!j.archived};
    }
    return {host, path: j.full_name, nwo: j.full_name, name: j.name, description: j.description || "", topics: j.topics || [],
            language: j.language || "", stars: j.stargazers_count || 0, pushed: (j.pushed_at || "").slice(0, 10),
            url: j.html_url, branch: j.default_branch, archived: !!j.archived, fork: !!j.fork};
  }
  // What a failed lookup was, from its status and headers, so the page can say it plainly.
  function failure(host, status, headers) {
    const get = (k) => (headers && headers.get ? headers.get(k) : null);
    if (status === 404) return {kind: "missing"};
    if (status === 429 || (status === 403 && (get("x-ratelimit-remaining") === "0" || get("ratelimit-remaining") === "0" || host === "github.com"))) {
      const reset = Number(get("x-ratelimit-reset") || get("ratelimit-reset")) || 0;
      return {kind: "limited", reset: reset ? reset * 1000 : 0};
    }
    if (status === 401 || status === 403) return {kind: "private"};
    return {kind: "error", status};
  }

  // `?repo=` or `?q=`, the two states a link can restore. Anything else is ignored rather than guessed at.
  function readQuery(search) {
    const p = new URLSearchParams(search || "");
    const repo = (p.get("repo") || "").trim(), q = (p.get("q") || "").trim();
    return repo ? {repo} : q ? {q} : {};
  }
  function writeQuery(state) {
    return state.repo ? "?repo=" + encodeURIComponent(state.repo).replace(/%2F/gi, "/")
      : state.q ? "?q=" + encodeURIComponent(state.q) : "";
  }

  // The detail page for a row: `22_detail.py`'s `segment()`, the fifth copy of it. `tests/alike-probe.mjs`
  // resolves this against the committed `docs/repo/` tree for every row, which is the only check that matters.
  const DEVICE_NAMES = ["con", "prn", "aux", "nul", "clock$", ...[1, 2, 3, 4, 5, 6, 7, 8, 9].flatMap((i) => ["com" + i, "lpt" + i])];
  const segment = (s) => {
    if (s.startsWith(".")) s = "dot-" + s.slice(1);
    if (s.endsWith(".")) s = s.slice(0, -1) + "-dot";
    if (DEVICE_NAMES.includes(s.split(".")[0])) s = "dev-" + s;
    return s;
  };
  const detailPath = (nwo) => "repo/" + nwo.toLowerCase().split("/").map(segment).join("/") + "/";

  return {W, SHOW, ECO, ACTIVE_DAYS, parseInput, build, resolve, sourceRow, sourceRepo, sourceText, rank, filter, why,
          languages, cleanBlurb, readmeText, apiURL, readmeURL, fromAPI, failure, readQuery, writeQuery, detailPath,
          norm, termsOf, isEco};
})();

// ======================================================================== the page
// Everything below touches the DOM, and runs only on the page: the probe loads this file under node, where
// there is no `document`, to reach `ALIKE` alone.
if (typeof document !== "undefined" && document.getElementById("lk")) (() => {
  const $ = (id) => document.getElementById(id);
  const UP = document.documentElement.dataset.up || "../";
  const esc = (s) => String(s === null || s === undefined ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
    .replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#x27;");
  const commas = (n) => Number(n || 0).toLocaleString("en-US");
  const form = $("lkform"), box = $("lkq"), out = $("lkout"), live = $("lklive"), status = $("lkstatus");
  const choose = $("lkchoose"), src = $("lksrc"), filters = $("lkfilters"), around = $("lkaround");
  const describe = $("lkdescribe"), dbox = $("lkdq"), dform = $("lkdform");
  let IX = null, CUR = null, RES = null;

  // The live region only announces a change, so a repeat of the same sentence is nudged.
  let lastSaid = "";
  const say = (t) => { live.textContent = t === lastSaid ? t + " " : t; lastSaid = live.textContent; };
  const note = (html, kind) => {
    status.hidden = !html;
    status.innerHTML = html || "";
    status.dataset.kind = kind || "";
    // An error is announced by the alert role it carries; a plain note is not announced twice.
    status.setAttribute("role", kind === "error" ? "alert" : "status");
  };

  // The atlas: `data.json` and the four index files, fetched once. The index is optional -- a stale one is
  // refused by `semDecode` and the page ranks by words and categories, and says so under the results.
  const grab = async (path, how) => {
    const res = await fetch(UP + path);
    if (!res.ok) throw new Error(path + " -> " + res.status);
    return how === "json" ? res.json() : res.arrayBuffer();
  };
  let semNote = "";
  const READY = (async () => {
    const d = await grab("data.json", "json");
    let sem = null;
    try {
      const [meta, vocab, table, docs] = await Promise.all([grab("search/meta.json", "json"),
        grab("search/vocab.json", "json"), grab("search/vocab.bin", "buf"), grab("search/docs.bin", "buf")]);
      sem = await semDecode({meta, vocab, table, docs}, d.rows.map((r) => r[d.cols.indexOf("nwo")]));
    } catch (err) {
      console.warn("lookalikes: similarity index unavailable:", err.message);
      semNote = "The similarity index is out of step with today&rsquo;s data, so these are ranked by shared words and " +
        "category only, which is rougher. It fixes itself at the next rebuild.";
    }
    IX = ALIKE.build(d, sem);
    document.documentElement.classList.add("lkready");
    return IX;
  })();
  READY.catch((err) => {
    note("The atlas didn&rsquo;t load (" + esc(err.message) + "). Check your connection and reload the page.", "error");
  });

  // ---------------------------------------------------------------- the URL is the state
  function go(state, push) {
    const qs = ALIKE.writeQuery(state);
    if (push && location.search !== qs) history.pushState(state, "", location.pathname + qs);
    else history.replaceState(state, "", location.pathname + qs);
  }

  async function run(state, how) {
    if (!state.repo && !state.q) { clear(); return; }
    note("Loading the atlas&hellip;", "busy");
    let ix;
    try { ix = await READY; } catch { return; }
    note("");
    if (state.q) { box.value = box.value || ""; dbox.value = state.q; return showText(ix, state.q, how); }
    box.value = state.repo;
    const r = ALIKE.resolve(ix, state.repo);
    if (r.kind === "hit") return showRow(ix, r.i, how);
    if (r.kind === "external") return lookUp(ix, r, how);
    // `?repo=` naming words: treat it as typed.
    return submit(state.repo, how);
  }

  function clear() {
    CUR = RES = null;
    out.innerHTML = ""; src.innerHTML = ""; around.innerHTML = ""; choose.innerHTML = "";
    src.hidden = filters.hidden = around.hidden = choose.hidden = true;
    note("");
  }

  async function submit(text, how) {
    let ix;
    note("Loading the atlas&hellip;", "busy");
    try { ix = await READY; } catch { return; }
    note("");
    const r = ALIKE.resolve(ix, text);
    choose.hidden = true; choose.innerHTML = "";
    if (r.kind === "empty") { note("Paste a GitHub or GitLab link, or type a project&rsquo;s name.", "error"); box.focus(); return; }
    if (r.kind === "notrepo")
      return fail("That&rsquo;s a link to " + esc(r.host + (r.path ? "/" + r.path : "")) + ", not to one repository. " +
        "Paste a link to the project itself, like <code>" + esc(r.host) + "/owner/project</code>.", true);
    if (r.kind === "hit") { go({repo: ix.rows[r.i].nwo}, how !== "load"); return showRow(ix, r.i, how); }
    if (r.kind === "external") { go({repo: r.nwo}, how !== "load"); return lookUp(ix, r, how); }
    if (r.kind === "choose") return offer(ix, r);
    go({q: r.text}, how !== "load");
    return showText(ix, r.text, how);
  }

  // "Did you mean": the rows the words could name, as buttons, and the words themselves as a description.
  function offer(ix, r) {
    clear();
    choose.hidden = false;
    choose.innerHTML = '<h2 id="lkchooseh" tabindex="-1">Which one did you mean?</h2><ul class="lkpick">' +
      r.choices.map((i) => {
        const row = ix.rows[i];
        return '<li><button type="button" class="lkopt" data-nwo="' + esc(row.nwo) + '"><b>' + esc(row.name) + "</b> " +
          '<span class="lknwo">' + esc(row.nwo) + "</span> <small>" + commas(row.stars) + " stars</small></button></li>";
      }).join("") + "</ul>" +
      '<p class="lkquiet"><button type="button" class="lklink" id="lkasq">Or find projects that do &ldquo;' + esc(r.text) +
      "&rdquo;</button></p>";
    say(r.choices.length + (r.choices.length === 1 ? " project matches" : " projects match") + " “" + r.text + "”. Choose one.");
    $("lkchooseh").focus();
  }

  choose.addEventListener("click", (e) => {
    const b = e.target.closest("button");
    if (!b) return;
    if (b.id === "lkasq") { const t = box.value.trim(); go({q: t}, true); showText(IX, t, "user"); return; }
    if (b.dataset.nwo) { box.value = b.dataset.nwo; go({repo: b.dataset.nwo}, true); showRow(IX, IX.by.get(b.dataset.nwo.toLowerCase()), "user"); }
  });

  // ---------------------------------------------------------------- not in the atlas
  async function lookUp(ix, r, how) {
    clear();
    const forge = r.host === "gitlab.com" ? "GitLab" : "GitHub";
    note("Asking " + forge + " about " + esc(r.path) + "&hellip;", "busy");
    let res;
    try {
      res = await fetch(ALIKE.apiURL(r.host, r.path), {headers: {Accept: "application/json"}});
    } catch {
      return fail(navigator.onLine === false
        ? "You&rsquo;re offline, so we can&rsquo;t ask " + forge + " about a project that isn&rsquo;t in the atlas. " +
          "Projects in the atlas still work offline once you&rsquo;ve opened this page."
        : "We couldn&rsquo;t reach " + forge + " to look up " + esc(r.path) + ". It may be down, or blocked on this network.", true);
    }
    if (!res.ok) {
      const f = ALIKE.failure(r.host, res.status, res.headers);
      if (f.kind === "missing" && r.bare) {
        // A bare `a/b` GitHub has never heard of was probably words with a slash in them.
        go({q: r.path}, false);
        return showText(ix, r.path, how);
      }
      if (f.kind === "missing" || f.kind === "private")
        return fail(forge + " has no public repository at <b>" + esc(r.path) + "</b>. Check the link, or describe what it does.", true);
      if (f.kind === "limited") {
        const when = f.reset ? " It resets at " + new Date(f.reset).toLocaleTimeString([], {hour: "2-digit", minute: "2-digit"}) + "." : "";
        return fail(forge + " only answers 60 anonymous lookups an hour from one connection, and this one has used them." + when +
          " Projects in the atlas don&rsquo;t need a lookup, and describing what it does works now.", true);
      }
      return fail(forge + " answered " + esc(f.status) + " for " + esc(r.path) + ". Try again in a minute, or describe what it does.", true);
    }
    const info = ALIKE.fromAPI(r.host, await res.json());
    // A renamed repository: the forge redirects to the new name, which the atlas may hold.
    const known = ix.by.get(info.nwo.toLowerCase());
    if (known !== undefined) { go({repo: ix.rows[known].nwo}, false); return showRow(ix, known, how); }
    try {
      const rd = await fetch(ALIKE.readmeURL(r.host, info));
      if (rd.ok) info.readme = (await rd.text()).slice(0, 20000);
    } catch { /* no README: the description alone */ }
    note("");
    const s = ALIKE.sourceRepo(ix, info);
    CUR = {src: s, info, title: info.name};
    paintSource(ix, s, info);
    results(ix, how);
  }

  function fail(html, offerDescribe) {
    clear();
    note(html + (offerDescribe ? ' <button type="button" class="lklink" id="lktodesc">Describe what it does instead</button>' : ""), "error");
    say(status.textContent);
    const b = $("lktodesc");
    if (b) b.addEventListener("click", () => { describe.open = true; dbox.focus(); });
  }

  // ---------------------------------------------------------------- the three kinds of source
  function showRow(ix, i, how) {
    clear();
    const s = ALIKE.sourceRow(ix, i), r = ix.rows[i];
    CUR = {src: s, row: r, title: r.name};
    paintSource(ix, s, null, r);
    results(ix, how);
  }

  function showText(ix, text, how) {
    clear();
    const s = ALIKE.sourceText(ix, text);
    if (!s.terms.size && !s.doc) {
      return fail("There&rsquo;s nothing in &ldquo;" + esc(text) + "&rdquo; to search by. Try a few words about what the project does, " +
        "like &ldquo;tracing for LLM apps&rdquo;.", false);
    }
    CUR = {src: s, text, title: "“" + text + "”"};
    src.hidden = false;
    src.innerHTML = '<p class="kick">Projects that do</p><h2 id="lksrch">&ldquo;' + esc(text) + "&rdquo;</h2>";
    results(ix, how);
  }

  function paintSource(ix, s, info, row) {
    src.hidden = false;
    if (row) {
      src.innerHTML = '<p class="kick">Lookalikes of</p><h2 id="lksrch"><a href="' + esc(UP + ALIKE.detailPath(row.nwo)) + '">' +
        esc(row.name) + '</a></h2><p class="lknwo">' + esc(row.nwo) + "</p>" +
        (row.blurb ? '<p class="lkblurb">' + esc(ALIKE.cleanBlurb(row.blurb)) + "</p>" : "") +
        '<p class="lkmeta">' + esc(ix.cats[row.cat]) + (row.lang ? " &middot; " + esc(row.lang) : "") + " &middot; " +
        commas(row.stars) + " stars</p>";
    } else {
      const forge = info.host === "gitlab.com" ? "GitLab" : "GitHub";
      src.innerHTML = '<p class="kick">Lookalikes of</p><h2 id="lksrch"><a href="' + esc(info.url) + '">' + esc(info.name) +
        '</a></h2><p class="lknwo">' + esc(info.path) + " on " + forge + "</p>" +
        (info.description ? '<p class="lkblurb">' + esc(info.description) + "</p>" : "") +
        '<p class="lknot" role="note"><b>This project isn&rsquo;t in the atlas.</b> We read its description' +
        (info.topics.length ? ", topics" : "") + (info.readme ? " and README" : "") + " from " + forge +
        " and compared that with every project we list.</p>";
    }
  }

  // ---------------------------------------------------------------- the list
  function results(ix, how) {
    RES = ALIKE.rank(ix, CUR.src);
    // The language menu describes this list, so it is rebuilt per source; a language the new list does not
    // contain is dropped rather than left selected with nothing under it.
    const sel = $("lklang"), keep = sel.value;
    const langs = ALIKE.languages(ix, RES.main);
    sel.innerHTML = '<option value="">Any language</option>' + langs.map((l) => '<option>' + esc(l) + "</option>").join("");
    sel.value = langs.includes(keep) ? keep : "";
    filters.hidden = false;
    paint(ix, how);
  }

  function current() {
    return {lang: $("lklang").value, stars: Number($("lkstars").value) || 0, active: $("lkactive").checked};
  }

  function paint(ix, how) {
    const f = current();
    const list = ALIKE.filter(ix, RES.main, f, Date.now()).slice(0, ALIKE.SHOW);
    const any = f.lang || f.stars || f.active;
    if (!list.length) {
      out.innerHTML = '<p class="lkempty">Nothing matches those filters. <button type="button" class="lklink" id="lkreset">Clear the filters</button></p>';
      $("lkreset").addEventListener("click", () => { $("lklang").value = ""; $("lkstars").value = "0"; $("lkactive").checked = false; paint(ix, "user"); });
    } else {
      out.innerHTML = '<h2 class="lkh" id="lkresh" tabindex="-1">' + list.length + (list.length === 1 ? " lookalike" : " lookalikes") +
        (any ? ", filtered" : "") + "</h2>" +
        '<ol class="lklist">' + list.map((j) => card(ix, j)).join("") + "</ol>" +
        (RES.vectors ? "" : '<p class="lkquiet">' + semNote + "</p>");
    }
    const eco = CUR.src.kind === "text" ? [] : RES.around.slice(0, ALIKE.ECO);
    around.hidden = !eco.length;
    around.innerHTML = eco.length ? '<h2 class="lkh">Built on or around ' + esc(CUR.title) + "</h2>" +
      '<p class="lkquiet">From the same maintainer, or named after it: add-ons, ports and integrations rather than alternatives.</p>' +
      '<ul class="lkeco">' + eco.map((j) => {
        const r = ix.rows[j];
        return '<li><a href="' + esc(UP + ALIKE.detailPath(r.nwo)) + '">' + esc(r.name) + '</a> <span class="lknwo">' + esc(r.nwo) + "</span></li>";
      }).join("") + "</ul>" : "";
    const top = list.slice(0, 3).map((j) => ix.rows[j].name).join(", ");
    say(list.length ? list.length + " lookalikes of " + CUR.title + (any ? ", filtered" : "") + ". First: " + top + "."
      : "No lookalikes match those filters.");
    if (how === "user" && list.length) $("lkresh").focus({preventScroll: false});
  }

  function card(ix, j) {
    const r = ix.rows[j], w = ALIKE.why(ix, CUR.src, RES, j);
    const reasons = [];
    if (w.alt) reasons.push('<span class="lkwhy-alt">Calls itself an alternative</span>');
    if (w.cat) reasons.push("<span>Also in " + esc(w.cat) + "</span>");
    if (w.targets.length) reasons.push("<span>Both for " + esc(w.targets.join(", ")) + "</span>");
    if (w.terms.length) reasons.push("<span>Shared: " + w.terms.map((t) => "<i>" + esc(t) + "</i>").join(", ") + "</span>");
    const days = r.pushed ? Math.floor((Date.now() - Date.parse(r.pushed)) / 86400000) : null;
    const age = days === null ? "" : days < 1 ? "pushed today" : days < 60 ? "pushed " + days + " days ago"
      : days < 730 ? "pushed " + Math.round(days / 30) + " months ago" : "pushed " + Math.round(days / 365) + " years ago";
    const host = r.nwo.split("/")[0].includes(".") ? "GitLab" : "GitHub";
    return '<li class="lkcard"><div class="lkch"><h3><a href="' + esc(UP + ALIKE.detailPath(r.nwo)) + '">' + esc(r.name) + "</a></h3>" +
      '<span class="lknwo">' + esc(r.nwo) + "</span></div>" +
      (r.blurb ? '<p class="lkblurb">' + esc(ALIKE.cleanBlurb(r.blurb)) + "</p>" : "") +
      (reasons.length ? '<p class="lkwhy"><span class="sr">Why it&rsquo;s here: </span>' + reasons.join("") + "</p>" : "") +
      '<p class="lkmeta">' + commas(r.stars) + " stars" + (r.lang ? " &middot; " + esc(r.lang) : "") + (age ? " &middot; " + age : "") +
      ' &middot; <a href="?repo=' + esc(encodeURIComponent(r.nwo).replace(/%2F/gi, "/")) + '" data-nwo="' + esc(r.nwo) +
      '">Its lookalikes</a> &middot; <a href="' + esc(r.url) + '">' + host + ' <span aria-hidden="true">&nearr;</span></a></p></li>';
  }

  // ---------------------------------------------------------------- wiring
  form.addEventListener("submit", (e) => { e.preventDefault(); submit(box.value, "user"); });
  dform.addEventListener("submit", (e) => {
    e.preventDefault();
    const t = dbox.value.trim();
    if (!t) { dbox.focus(); return; }
    go({q: t}, true);
    READY.then((ix) => showText(ix, t, "user"));
  });
  for (const id of ["lklang", "lkstars", "lkactive"]) $(id).addEventListener("change", () => { if (RES) paint(IX, "filter"); });
  // "Its lookalikes" and the example chips are links, so they work without this; with it they skip the reload.
  document.addEventListener("click", (e) => {
    const a = e.target.closest("a[data-nwo], a[data-ex]");
    if (!a || e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
    e.preventDefault();
    const st = ALIKE.readQuery(a.getAttribute("href"));
    go(st, true);
    if (st.repo) box.value = st.repo;
    run(st, "user");
    window.scrollTo({top: 0});
  });
  window.addEventListener("popstate", () => run(ALIKE.readQuery(location.search), "load"));
  run(ALIKE.readQuery(location.search), "load");
  // For tests and the curious: the loaded index, once it is there.
  window.LOOKALIKES = {ready: READY, get ix() { return IX; }, get res() { return RES; }, get cur() { return CUR; }};
})();
