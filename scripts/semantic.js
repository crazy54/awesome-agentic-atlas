// THE QUERY ENCODER FOR `docs/search/`, ONE COPY FOR EVERY PAGE THAT READS IT.
//
// Inlined at build time into two pages: the catalogue (`scripts/19_pages.py`, where search by meaning and the
// map were born) and Lookalikes (`scripts/33_alike.py`). Both used to need it, and the alternative was a
// second transcription of an algorithm that already exists three times -- once per language: the build stage
// `scripts/27_semantic.py` is the reference, `tests/semantic_test.py` is a transcription in Python, and this
// is the browser's. Two browser copies would make four, and the drift between any two of them is the failure
// with no symptom: a query segmented one way against documents segmented another throws nothing, returns a
// full page of results, and ranks them by noise. So this file is the browser's copy, and both pages carry it
// verbatim. `tests/alike_test.py` holds both generators to that, and `tests/probe.mjs` runs `semTokens` from
// the catalogue against the fixtures `27_semantic.py` writes into `meta.json`.
//
// What lives here is the part that has to be identical: the tokeniser, the forward pass, and the guard that
// decides whether the four fetched files may be trusted at all. What does *not* live here is each page's use
// of it -- when to fetch, what to rank, how to blend with a lexical score -- because those are page-level
// judgements and differ on purpose. The catalogue consults meaning only when the words found too little; a
// lookalike search is nothing but meaning.
//
// Plain function declarations and no module syntax, because it is pasted into a classic `<script>` on one
// page and a `<script type="module">` on the other, and both have to define the same names.

// Sanity bound on `meta.dims` before it is used as a stride.
const SEM_DIMS_MAX = 512;
// Its own regex object, and not the one `27_semantic.py` compiles, because this is a transcription rather
// than a shared implementation and there is no way to share one across two languages. The stage has this
// pattern, `tests/semantic_test.py` has it a third time, and all three have to agree.
const SEM_WORD = /[a-z0-9]+|[^\sa-z0-9]/g;

// Greedy longest-match WordPiece, over the pruned vocabulary the page holds and not the model's full one.
// `27_semantic.py` segments the corpus against exactly the tokens shipped in `vocab.json` for the same reason:
// the stage shipped a subset, so it has to *build* against the subset too, or the same word is two different
// token sequences on the two sides. A word no suffix of which is in the vocabulary is dropped whole rather
// than partially, which is why the stage force-keeps every single-character token.
//
// `slot` and `stop` are parameters rather than reads of a loaded index, which makes this the one function
// here with no dependency on state -- and therefore the one a test can call. It is also the function most
// worth calling: `meta.json` ships the stage's own segmentation of a handful of texts, and `tests/probe.mjs`
// runs this code against those fixtures, comparing token ids and nothing else.
function semTokens(text, slot, stop) {
  const out = [];
  for (const word of String(text).toLowerCase().match(SEM_WORD) || []) {
    // Before the lookup, never after, and never by leaving the token out of the vocabulary instead. A
    // stopword whose token is missing does not disappear -- WordPiece re-spells it out of the longest
    // surviving pieces, and those pieces are rare, so it comes back weighted *higher* than the content
    // words. Measured on this corpus: "should" arrived as `sho` + `##uld` at row norms 172 and 152 against
    // 179 for `pdf`. See the note on STOP in 27_semantic.py.
    if (stop && stop.has(word)) continue;
    let start = 0, ok = true;
    const pieces = [];
    while (start < word.length) {
      let end = word.length;
      for (; end > start; end--) {
        const piece = start === 0 ? word.slice(start, end) : "##" + word.slice(start, end);
        const id = slot.get(piece);
        if (id !== undefined) { pieces.push(id); break; }
      }
      if (end === start) { ok = false; break; }
      start = end;
    }
    if (ok) for (const p of pieces) out.push(p);
  }
  return out;
}

// The forward pass, over an index `semDecode` returned. Sum of the token rows, normalised -- the IDF weighting
// and the projection are already baked into the shipped table, so there is nothing to weight here and nothing
// to project. Null when nothing segments, which is also how a topicless question declines: "please help me
// choose" is every word a stopword, so it produces no tokens at all and never reaches the corpus -- a better
// answer than the twelve confident, unrelated projects it used to return.
function semEncode(sem, text) {
  const ids = semTokens(text, sem.slot, sem.stop);
  if (!ids.length) return null;
  const d = sem.dims, v = new Float32Array(d);
  for (const id of ids) {
    const base = id * d;
    for (let k = 0; k < d; k++) v[k] += sem.table[base + k] * sem.vs;
  }
  let n = 0;
  for (let k = 0; k < d; k++) n += v[k] * v[k];
  n = Math.sqrt(n);
  if (!n) return null;
  for (let k = 0; k < d; k++) v[k] /= n;
  return v;
}

// The four fetched files, checked and decoded, or a throw saying which check failed. Every reader of
// `docs/search/` goes through this, because every reader has the same reason to distrust it.
//
// THE STALENESS GUARD, which is the one failure that must not be quiet. The vectors are addressed by row
// *ordinal*: `docs.bin` is row 0, row 1, row 2 with nothing naming them. An index built against a different
// `data.json` therefore does not error, does not look wrong, and returns each project's neighbour with total
// confidence. `meta.json` carries a SHA-256 of the `nwo` column it was built from and this recomputes it from
// `nwos`, the page's own rows in `data.json` order. `crypto.subtle` needs a secure context, so on `file://`
// the guard falls back to the row count alone -- which catches the ordinary case, a rebuilt crawl of a
// different size.
async function semDecode(files, nwos) {
  const {meta, vocab, table, docs} = files;
  const dims = meta.dims | 0;
  if (!(dims > 0 && dims <= SEM_DIMS_MAX)) throw new Error("meta.dims is " + meta.dims);
  // The row count first because it is free and catches the common case; the fingerprint second because it
  // is the only test that catches a rebuild of the *same* size in a different order, which is the one that
  // silently returns the wrong project for every query.
  if (meta.rows !== nwos.length)
    throw new Error("index has " + meta.rows + " rows, data.json has " + nwos.length);
  if (globalThis.crypto && crypto.subtle) {
    const body = new TextEncoder().encode(nwos.join("\n"));
    const hash = [...new Uint8Array(await crypto.subtle.digest("SHA-256", body))]
      .map(b => b.toString(16).padStart(2, "0")).join("").slice(0, 16);
    if (hash !== meta.fingerprint)
      throw new Error("data.json is " + hash + ", index was built against " + meta.fingerprint);
  }
  if (docs.byteLength !== meta.rows * dims) throw new Error("docs.bin is " + docs.byteLength + " B");
  if (table.byteLength !== vocab.tokens.length * dims)
    throw new Error("vocab.bin is " + table.byteLength + " B");
  // The two scales, checked because they are the one input that would otherwise reach the arithmetic
  // unvalidated -- and NaN does not fail closed here, it fails *open* and silent. A missing scale makes every
  // score NaN, every cutoff comparison false, and every sort comparator NaN, so a whole result list comes out
  // in arbitrary order with no exception and nothing that looks degraded. Unreachable from `27_semantic.py`,
  // which always writes both; reachable from a truncated or hand-edited meta.json, which is exactly what a
  // guard is for.
  for (const [k, v] of [["doc_scale", meta.doc_scale], ["vocab_scale", meta.vocab_scale]])
    if (!(typeof v === "number" && isFinite(v) && v > 0)) throw new Error("meta." + k + " is " + v);
  return {
    dims,
    slot: new Map(vocab.tokens.map((t, i) => [t, i])),
    // Shipped rather than transcribed a fourth time, and applied by `semTokens` before it looks anything up.
    // Absent in a schema 1 index built before this existed, which degrades to the old behaviour rather than
    // throwing -- an empty set simply strips nothing.
    stop: new Set(meta.stop || []),
    table: new Int8Array(table),
    docs: new Int8Array(docs),
    // int8 was quantised against two separate maxima -- one shared scale crushed every unit-length document
    // component to 0 or +/-1 and collapsed 1,294 rows onto a handful of distinct vectors.
    ds: meta.doc_scale / 127,
    vs: meta.vocab_scale / 127,
    // Kept for the catalogue's map, which is the other reader of this directory and validates nothing of its
    // own. `rows` and `near` are the two lengths `xy.bin` and `near.bin` have to have; `xy_scale` is the one
    // number that turns their int16s back into positions. Carried here rather than re-fetched there because
    // `meta.json` is where the fingerprint lives, and a second fetch is a second chance for the two readers
    // to be looking at different metadata.
    rows: meta.rows, near: meta.near | 0, xys: meta.xy_scale,
  };
}
