"""A semantic index the browser can query offline, with no model download and no backend.

The search box on `docs/index.html` is a substring filter wearing a search box's clothes. `match()`
splits the query on spaces and requires *every* word to appear as a raw substring of one concatenated
`hay` field; the only fuzziness anywhere is `near()`, a trigram fallback that looks at `name` alone. It
is exact and fast and it answers the wrong question. Measured against the committed 1,294-row build,
eight of thirty-seven queries a visitor would plausibly type return nothing at all:

  sandbox                             64 hits      keep my agent from deleting files      0 hits
  pr review                           53 hits      something to review PRs                0 hits
  pdf                                  9 hits      chat with my pdfs                      0 hits
  testing                             16 hits      agent that writes tests                0 hits

The pattern is the whole problem: the keyword is in the corpus and the sentence is not. Every visitor
who types the way people talk lands on an empty table in a catalogue that held what they wanted. This
stage builds the index that fixes it.

  docs/search/meta.json    dimensions, quantisation scale, corpus fingerprint, which text was indexed
  docs/search/vocab.json   the token strings the client tokenises with, in the table's own order
  docs/search/vocab.bin    int8, one vector per token -- the query encoder's lookup table
  docs/search/docs.bin     int8, one vector per row of docs/data.json, in that exact order
  docs/search/near.bin     uint16, the NEAR nearest neighbours of every row, precomputed
  docs/search/xy.bin       int16, two per row: where that project sits on the map

ONE TOKENISER, WRITTEN HERE, BECAUSE THE CLIENT ONLY GETS PART OF THE VOCABULARY. The obvious build is
to segment with the model's own tokeniser and ship a pruned table, and it is quietly broken: this stage
would cut `kubernetes` as the single token the full 29,528-entry vocabulary has for it, while a browser
holding only the 12,000 tokens worth shipping would fall back to `kub ##ern ##etes`. Same word, two
segmentations, two vectors, and a document side that indexed a token the query side cannot produce. So
the vocabulary is pruned *first* and both sides then segment against the pruned set with the greedy
WordPiece in `wordpiece()` below -- the reference implementation the page's encoder is a transcription
of, and the reason `tests/semantic_test.py` can score a query using nothing but the shipped artefacts.
Every single-character token is force-kept so that any word remains segmentable rather than becoming
`[UNK]`.

WHY A STATIC EMBEDDING TABLE AND NOT A TRANSFORMER. The document vectors could be built by anything,
because they are built here, once, by a machine with a cache and no deadline. The *query* is the hard
half: it has to be encoded in the reader's browser, on a page whose CSS and JavaScript are inline
precisely so that the first paint costs one request, and it has to keep working offline because the
service worker promises it will. Running a real sentence transformer there means shipping WASM and tens
of megabytes of weights, on a page whose entire current payload is 91 KB. So the model is a
`model2vec` static table (`minishlab/potion-base-8M`, MIT): a plain matrix with one vector per
WordPiece token, distilled so that a *weighted mean of token vectors* lands near where the transformer
would have put the sentence. That turns the client-side encoder into tokenise, look up, average --
about forty lines of JavaScript over a table this stage prunes for it, no runtime, nothing to compile.

FOUR MEASURED DECISIONS. Each of these was the other way round first, and the corpus argued.

  * Damped IDF, not plain averaging and not full IDF. This corpus has one word in three fifths of its
    documents -- `agent` is in 779 of 1,294 -- plus `agents`, `ai`, `llm` and `claude` behind it. A
    plain mean of token vectors is therefore mostly a vector meaning "an AI agent", which every row
    also is, and the discriminative signal is what is left over: "chat with my pdfs" returned
    `ChatArena` and `ChatDev`. Weighting each token by its full corpus IDF over-corrects, because it
    hands the sentence to its rarest token and drops the topic: it moved "keep my agent from deleting
    files" off governance tooling entirely. `sqrt(idf)` was the setting that fixed the first without
    buying the second -- "something to review PRs" goes from PR-Agent at 0.512, barely ahead of the
    noise, to 0.711 against a 0.358 runner-up.

  * Punctuation and stopwords are dropped before pooling, not after. The first build fed the model
    `"name. blurb. category. lang"` and the four most ubiquitous tokens in the corpus came back as
    `.`, `-`, `,` and `&`. They carry no meaning, they are in every document, and averaged into 24
    tokens of blurb they are a third of the vector.

  * The score is a blend of this index and a lexical score, and neither is allowed to be the whole
    answer. Semantics alone cannot find `k8s`: as a token it is near nothing, and the query returned
    an ESP32 assistant. Lexical alone is what we have today, and it returns zero for every sentence
    above. Blended, `k8s` finds `Kubernetes Agent Sandbox` on the lexical side while "something to
    review PRs" finds PR-Agent on this one. The weights live in the page, not here, because tuning
    them is a page-level judgement -- this stage only has to emit a comparable score.

  * Cutoffs are ranks and percentiles, never absolute similarity. A threshold like "0.35 is a match"
    is fitted to a particular corpus size and distribution, and this corpus is about to sextuple: the
    39-list ingest is merged and unpublished, and the last real run counted 8,293 distinct repos
    against the 1,294 the site serves. Anything numeric that was true at 1,294 rows would have to be
    re-measured at 8,293, so nothing numeric is baked in.

WHAT GETS INDEXED, AND WHY IT SAYS SO OUT LOUD. Relevance is capped by how much text each row has.
A blurb averages 24 tokens, which is enough to place a project and not enough to describe it, so this
stage prefers the README that `02_fetch.py` and `11_fetch_all.py` leave in `cache/readmes/` and falls
back to the blurb per row when one is missing. That fallback is silent in its effect and loud in the
report, because a cold cache and a broken index look identical from the search box: both feel like
search got worse. `meta.json` carries the split so the page and the tests can tell which they have.

THE STALENESS GUARD, which is the one thing here that can corrupt an answer rather than weaken it.
`docs/docs.bin` is row-*ordinal* addressed -- vector `i` belongs to `data.json`'s row `i` -- because an
ordinal is two bytes where `owner/name` is forty. That makes the two files a matched pair: rebuild
`data.json` without rebuilding this, and every vector points at its neighbour's project. The failure
is silent, total, and looks like a ranking bug rather than a stale artifact. So `meta.json` carries the
row count and a digest of the `nwo` column in order, the page checks both before it trusts a byte of
this, and falls back to today's lexical search when they disagree.

  python scripts/27_semantic.py

Reads the committed `docs/data.json`, so it runs from a clone with nothing fetched, like `19b_refresh`
-- it is only the README enrichment that wants the cache. The model is 30 MB, MIT, and rebuildable, so
it is cached under `cache/` with everything else that is none of our business to redistribute, and
fetched on first run.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import struct
import sys
import urllib.request
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "search"
DATA = ROOT / "docs" / "data.json"
READMES = ROOT / "cache" / "readmes"
MODEL = ROOT / "cache" / "m2v"

REPO = "minishlab/potion-base-8M"
FILES = ("model.safetensors", "tokenizer.json")

# Words are cut on whitespace, then punctuation is split off one character at a time, which is what
# BERT-family tokenisers do before WordPiece ever sees a word. Kept as one expression so the page's
# encoder can hold the same one.
WORD = re.compile(r"[a-z0-9]+|[^\sa-z0-9]")

# 96 of the model's 256 dimensions. The table is shipped to the reader, so every dimension is paid for
# 8,293 times over in `docs.bin` and once per token in `vocab.bin`; 96 keeps the pair inside ~2.5 MB at
# the post-ingest corpus size while holding the top principal directions of this corpus specifically,
# which is where a general-purpose model's variance mostly is not.
DIMS = 96
# Tokens shipped for query encoding, most-documented first. A token absent from every document cannot
# move the ranking -- its vector would be dotted against nothing -- so shipping the long tail buys
# payload and no answers. Rare literals keep working: they are what the lexical half is for.
VOCAB = 12_000
# Neighbours precomputed per row, for "more like this" on the 1,141 detail pages without making any of
# them load the whole matrix.
NEAR = 8
# README text is truncated hard. The first couple of thousand characters are the pitch, the badges and
# the install; past that is API reference and changelog, which describe every project the same way.
README_CHARS = 2_000

# ---------------------------------------------------------------------------- the map's coordinates
#
# `xy.bin` is two int16 per row: where that project sits on a plane, so the page can draw the corpus as a
# picture instead of as a list. Solved here rather than in the browser for the reason the whole file
# exists -- this end has numpy and no deadline, and the reader has a paint budget.
#
# It is a force layout on the neighbour graph, not a projection of the vectors, and that difference is the
# difference between a map and an inkblot. Three figures per candidate, all printed on every build and all
# measured on the quantised bytes a reader actually gets:
#
#   purity  of the 8 rows nearest a project on screen, how many share its curated category
#   keep    of its 8 *semantic* neighbours, how many are among those 8 nearest on screen
#   fill    how much of a 48x48 grid over the bounding box has anything in it
#
# Purity is the figure that says whether the picture is honest, because it is scored against a label the
# layout never saw -- `cat`, chosen by a human -- and it has a chance baseline to beat: two rows drawn at
# random from this corpus share a category 11.7% of the time. Measured on the committed 1,294-row index:
#
#   random scatter                  purity 11.6%   keep 0.05/8   fill 27.2%
#   plain 2-component projection    purity 31.4%   keep 0.30/8   fill 31.6%
#   this layout                     purity 60.7%   keep 2.07/8   fill 38.5%
#
# The scatter landing on the baseline is what makes the other two readable rather than merely large. The
# projection is not a *bad* picture -- 31.4% is real structure -- it is that the leading directions of this
# corpus are "is about agents" and "is a list of things", which every row scores highly on, so the topical
# arrangement sits buried under two axes nobody wants to look at.
#
# `keep` is deliberately the weakest of the three and it is not what the epochs were chosen for. The page
# draws each row's true neighbours as edges out of `near.bin`, so a reader is *told* who a project's
# neighbours are; they do not have to be the nearest dots on screen for that to read correctly.
#
# Three things were tried and rejected, each by measurement:
#
#   * Fruchterman-Reingold, which this file had first: keep 0.49/8 at fill 37.4%. Its ideal edge length is
#     sqrt(area/n), and holding a graph open at that length needs repulsion between all pairs -- exactly
#     the term that cannot survive the corpus growing.
#   * A denser layout graph. This end can compute any k, and every increase made it worse: k=16 gives
#     keep 1.39, k=24 gives 1.13, k=32 gives 0.98. The extra links are the weak ones, and averaging a
#     strong neighbour with a weak one blurs the neighbourhood the strong one defined.
#   * More repulsion. 30 negative samples scores keep 2.31 -- better than what ships -- and collapses fill
#     to 1.5%, with the extent blowing out to 354 units: a dense knot with a handful of rows flung far
#     enough to hold the bounding box open. That failure is invisible to `keep` and to every shape
#     assertion in the suite, and it is the whole reason `fill` is measured at all.
LAYOUT_EPOCHS = 500
# Negative samples per edge per epoch. 1,294 rows is 837k pairs and computing all of them is affordable;
# 8,293 rows is 34M pairs per epoch and is not. Sampling makes the cost grow with the number of edges
# rather than with the square of the number of rows, which is the only reason this stage still finishes
# after the 39-list ingest.
LAYOUT_NEG = 15
# 1,500 epochs at 25 samples measures better on keep -- 2.34/8 -- and identically on purity, for rather
# more than five times the arithmetic. The reader cannot perceive the difference and the corpus is about to
# sextuple, so the cheap setting ships. This is the number to raise if the map ever needs to be tighter,
# and keep is the number to raise it against.
LAYOUT_SPREAD = 4.0
LAYOUT_CLIP = 4.0
# Fixed, and load-bearing rather than tidy. `docs/search/` is committed, so a layout seeded off the clock
# would rewrite 5 KB of binary on every build whose input had not changed, and would move every project on
# the map for no reason a reader could see. Verified by building twice and comparing bytes.
LAYOUT_SEED = 20260912

# Words dropped before WordPiece ever sees them, on both sides of the wire. Where they are dropped is the
# entire subtlety, and getting it wrong is measurable.
#
# This list started as a filter on the *vocabulary*: a stopword was not shipped as a token. That does not
# remove it from a query -- it removes the only token that could have represented it, so WordPiece falls
# back to the longest surviving pieces, and those pieces are rare, and rare means high IDF. Measured on
# the shipped table: `should` became `sho` + `##uld` with row norms of 172 and 152, against 179 for `pdf`
# and 152 for `chat`. The two most heavily weighted tokens in "what should I use" were the two halves of
# the least informative word in it. Stopword removal had inverted itself, and nine topicless English
# questions -- "please help me choose", "is this any good", "what do you recommend" -- each came back with
# twelve confident, unrelated projects as a result.
#
# Giving the tokens weight zero instead fixes only the words that happen to exist as whole tokens.
# Measured: that recovered "the" and "is this any good", and left "please help me choose" scoring 0.364,
# because `choose` is not in the model's vocabulary either and fragmented to `cho` + `##ose` exactly as
# before. Any fix that operates on tokens is defeated by the words that have no token.
#
# So the drop happens on the word, before segmentation, in `wordpiece()` -- which is why `meta.json` ships
# this list and why the page and the tests each apply it. A stopword then contributes nothing because it
# never becomes a token at all, and a query made only of stopwords produces no tokens, which `semVector()`
# in the page already declines on a zero norm. No threshold, no heuristic, and nothing to tune. A query
# mixing chatter with a topic keeps the topic: "what should I use to scrape a website" scores as
# "scrape website", which is what the reader meant.
#
# The second group is the vocabulary of asking rather than the vocabulary of software: interrogatives,
# politeness, and the verbs people use to talk *about* searching. None of them describes a project, and a
# corpus of agent tooling is where that is safe to assert -- "recommend" and "explain" would be content
# words in a corpus of book reviews.
STOP = set("""a an the and or of for to in on with by is are be as at from this that it its your you
my our their his her not no all any some more most other into over under out up down off than then so
such can could would should will just also only very much many few own same too s t d ll m o re ve y
use uses used using make makes made get gets got let lets via etc eg ie
what how why when where who whom whose which please thanks thank hi hello hey ok okay sure yes yeah
do does did doing done have having had was were been being am i we he she us if but about me mine
thing things stuff something anything everything nothing someone anyone somebody anybody
better best great nice cool bad worse worst good
need needs needed want wants wanted like likes liked prefer prefers
recommend recommends recommended recommendation suggest suggests suggestion advice
explain explains tell tells show shows help helps helping
find finds looking look looks searching search choose choosing choice pick picks
know knows think thinks say says give gives take takes try tries
shall may might must ought started
there here now today still yet ever never again once
ones two three first second next last others
work works working way ways idea ideas option options""".split())

# Fixtures for the other two copies of `wordpiece`. `meta.json` ships each of these strings beside the
# slot ordinals *this* stage segmented it into, and both readers assert they reproduce them exactly:
# `tests/semantic_test.py` against its own transcription, `tests/probe.mjs` against the page's. That is
# what makes three implementations a redundancy instead of three chances to differ. It is worth the eight
# lines because the failure has no symptom -- a query segmented one way against documents segmented
# another throws nothing, returns a full page of results, and ranks them by noise. Every other assertion
# in the suite passes while it is happening.
#
# Slot ordinals, not token ids: the ordinal into `vocab.json` is what both readers address the table by,
# so a rebuild that reordered the vocabulary without changing the segmentation is also caught here.
#
# Chosen for the branches rather than for coverage of English, and each one measured rather than assumed
# -- two of these say something other than what they were picked to say, and the surprise is the reason
# to ship them. In order:
#
#   sandbox                   one word, two pieces: `sand` + `##box`. The ordinary case.
#   orchestration             a long word that falls apart into continuations rather than matching whole.
#   zzqxwv                    picked as the unsegmentable case; it is not one. It comes out as six
#                             single characters, because the single-character floor above means *no*
#                             ASCII word can fail to segment. That is the floor working, and it is worth
#                             a fixture precisely because it is not the behaviour you would predict from
#                             reading `wordpiece` alone.
#   café                      the real drop-whole case, and the only shape that reaches it. `é` has no
#                             `[a-z0-9]` in it, so it never entered `meaningful` and the floor never
#                             force-kept it; `caf` segments, `é` cannot, and the word is discarded
#                             entire rather than emitted as a partial. A non-ASCII word is the *only*
#                             way to exercise that branch, which is why an English fixture set would
#                             have left it uncovered.
#   chat with my pdfs.        punctuation `WORD` cuts off the end, and two stopwords. Note what the
#                             stopwords do: `with` was pruned as a token and reappears as `wit` + `##h`,
#                             `my` disappears entirely. Pruning a stopword does not remove it from the
#                             query -- it decays into subwords -- so the fixture records that instead of
#                             the "contributes nothing" the STOP list looks like it promises.
#   gpt-4o                    digits butted against letters, with a hyphen between them.
#   Observability Dashboards  capitals, which only the lowercase pass resolves.
#   run agents in parallel    one real query, because the cases above are all edges and a fixture set of
#                             only edges stops describing what the thing is for.
PROBES = (
    "sandbox",
    "orchestration",
    "zzqxwv",
    "café",
    "chat with my pdfs.",
    "gpt-4o",
    "Observability Dashboards",
    "run agents in parallel",
)


def fetch_model() -> None:
    """Pull the table into `cache/` on first run. Nothing here is ours to commit."""
    MODEL.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        dest = MODEL / name
        if dest.exists() and dest.stat().st_size:
            continue
        url = f"https://huggingface.co/{REPO}/resolve/main/{name}"
        print(f"fetching {name} from {REPO}")
        with urllib.request.urlopen(url, timeout=180) as r, dest.open("wb") as f:
            f.write(r.read())


def load_matrix() -> np.ndarray:
    """Read the one tensor out of a safetensors file without a safetensors dependency.

    The format is eight bytes of little-endian header length, that many bytes of JSON naming each
    tensor's dtype, shape and byte range, then the raw buffers. One tensor, so there is nothing to
    dispatch on and no reason to take the dependency.
    """
    raw = (MODEL / "model.safetensors").read_bytes()
    n = struct.unpack("<Q", raw[:8])[0]
    header = json.loads(raw[8:8 + n])
    name = next(k for k in header if k != "__metadata__")
    spec = header[name]
    dtype = {"F32": np.float32, "F16": np.float16}[spec["dtype"]]
    start, end = spec["data_offsets"]
    flat = np.frombuffer(raw[8 + n + start:8 + n + end], dtype=dtype)
    return flat.reshape(spec["shape"]).astype(np.float32)


def load_vocab() -> dict[str, int]:
    """The token strings out of `tokenizer.json`, without a tokeniser library.

    Only the vocabulary is wanted -- the normaliser and pre-tokeniser are reimplemented above so that
    this side and the browser side cannot drift, so the rest of the file is not consulted.
    """
    spec = json.loads((MODEL / "tokenizer.json").read_text(encoding="utf-8"))
    return dict(spec["model"]["vocab"])


def wordpiece(text: str, vocab: dict[str, int]) -> list[int]:
    """Greedy longest-match WordPiece over whatever vocabulary it is handed.

    The reference implementation. `docs/index.html` carries a transcription of this and
    `tests/semantic_test.py` carries another; all three have to agree, because a query segmented one way
    against documents segmented another scores noise. Words that cannot be covered are dropped rather
    than emitted as an unknown token: an `[UNK]` vector is a real direction in the space, and averaging
    it in moves the query somewhere meaningless instead of leaving it where the known words put it.

    `STOP` is applied here, on the whole word, and that placement is load-bearing rather than convenient:
    see the note on STOP for what filtering the vocabulary instead did to "what should I use". A stopword
    dropped before segmentation cannot come back as a rare fragment, because no fragment of it is ever
    looked up.
    """
    out: list[int] = []
    for word in WORD.findall(text.lower()):
        if word in STOP:
            continue
        start, pieces, ok = 0, [], True
        while start < len(word):
            end = len(word)
            while end > start:
                piece = word[start:end] if start == 0 else "##" + word[start:end]
                if piece in vocab:
                    pieces.append(vocab[piece])
                    break
                end -= 1
            if end == start:
                ok = False
                break
            start = end
        if ok:
            out.extend(pieces)
    return out


def doc_text(row: list, ix: dict, cats: list) -> tuple[str, bool]:
    """The text one row is indexed by, and whether its README was there to use.

    Name and category ride along with the README rather than being replaced by it: the name is often
    the only place a project's actual word appears (`Crawlberg` for crawling), and the category is the
    one label a human curated, so it is the highest-signal sentence available for the row.
    """
    get = lambda key: str(row[ix[key]] or "")
    head = f"{get('name')} {cats[row[ix['cat']]]} {get('lang')}"
    path = READMES / (get("nwo").replace("/", "__") + ".md")
    if path.exists():
        try:
            body = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            body = ""
        if body.strip():
            # Fenced code, links and headings are markup, not description. Left in, a project with a
            # long install snippet reads as being *about* shell commands.
            body = re.sub(r"```.*?```", " ", body, flags=re.S)
            body = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", body)
            body = re.sub(r"[#>*_`|\-]+", " ", body)
            return f"{head} {get('blurb')} {body[:README_CHARS]}", True
    return f"{head} {get('blurb')}", False


def edges(near: np.ndarray, n: int) -> tuple[np.ndarray, np.ndarray]:
    """`near.bin` as an undirected edge list, each pair once.

    The table is directed k-nearest: row i names the eight rows most like it, and being in i's eight does
    not put i in yours. A hub -- some widely-applicable agent framework -- is named by hundreds of rows and
    names only eight, and leaving that directed makes the layout treat those hundreds of pulls as
    one-sided. Deduplicating on the unordered pair is also what stops a mutual neighbour being pulled
    twice as hard as a one-way one, which would make popularity look like similarity.
    """
    src = np.repeat(np.arange(n, dtype=np.int64), near.shape[1])
    dst = near.ravel().astype(np.int64)
    keep = src != dst
    src, dst = src[keep], dst[keep]
    lo, hi = np.minimum(src, dst), np.maximum(src, dst)
    # One integer per unordered pair, so `unique` does the deduplication. int64 is checked rather than
    # assumed: at 8,293 rows the largest key is ~69M, and the day this file is handed a corpus where
    # n*n overflows is the day the map silently folds unrelated projects onto each other.
    assert n * n < np.iinfo(np.int64).max, "row count too large for the pair key"
    _, first = np.unique(lo * n + hi, return_index=True)
    return lo[first], hi[first]


def layout(unit: np.ndarray, near: np.ndarray) -> np.ndarray:
    """2D coordinates for every row: the force law UMAP optimises, over `near.bin` read as undirected.

    Attraction pulls each edge together with a gradient that saturates -- 2/(1+d^2) -- so a pair already
    close stops pulling and a pair far apart does not pull arbitrarily hard. Repulsion pushes a row away
    from LAYOUT_NEG rows drawn at random, with 1/((0.001+d^2)(1+d^2)), which is strong at short range and
    negligible at long. Both are clipped, and the whole displacement is scaled by a rate decaying to zero,
    which is what turns a simulation that oscillates for ever into one that comes to rest.

    Seeded from the two leading principal directions rather than from noise. A random start on this graph
    settles somewhere different every run and needs several times the epochs to stop looking knotted; the
    projection is a poor picture on its own and a good *guess*, because the broad topical split is already
    in it and the forces only have to open it out.

    Centring the seed is safe here in a way it explicitly is not for the ranking basis. The note in
    `main()` explains why subtracting the corpus mean destroys retrieval: a query is a three-word vector
    and the mean is a whole-document vector, so the shift dominates whatever the reader typed. Nothing
    projects a query into this space. It is a picture, and for a picture centring is where the origin goes.
    """
    n = unit.shape[0]
    if n < 3:
        return np.zeros((n, 2), dtype=np.float32)

    centred = unit - unit.mean(0)
    _, _, vt = np.linalg.svd(centred, full_matrices=False)
    pos = (centred @ vt[:2].T).astype(np.float32)
    pos /= float(np.abs(pos).max()) or 1.0
    pos *= LAYOUT_SPREAD

    ea, eb = edges(near, n)
    rng = np.random.default_rng(LAYOUT_SEED)
    for epoch in range(LAYOUT_EPOCHS):
        rate = 1.0 - epoch / LAYOUT_EPOCHS

        d = pos[ea] - pos[eb]
        pull = np.clip(d * (-2.0 / (1.0 + (d * d).sum(1, keepdims=True))), -LAYOUT_CLIP, LAYOUT_CLIP)

        # One head per edge, LAYOUT_NEG partners each, drawn uniformly. Uniform rather than
        # degree-weighted on purpose: the hubs are the rows that hundreds of others name, and weighting
        # the draw by degree would push them out to the rim, which is the opposite of where they belong.
        ha = np.repeat(ea, LAYOUT_NEG)
        hb = rng.integers(0, n, len(ea) * LAYOUT_NEG)
        apart = ha != hb
        ha, hb = ha[apart], hb[apart]
        rd = pos[ha] - pos[hb]
        rd2 = (rd * rd).sum(1, keepdims=True)
        push = np.clip(rd * (2.0 / ((0.001 + rd2) * (1.0 + rd2))), -LAYOUT_CLIP, LAYOUT_CLIP)

        disp = np.zeros_like(pos)
        for axis in (0, 1):
            # bincount rather than `np.add.at`, which is unbuffered and measures ~20x slower here. Same
            # arithmetic: every force landing on a row, summed, once per axis.
            disp[:, axis] = (
                np.bincount(ea, weights=pull[:, axis], minlength=n)
                - np.bincount(eb, weights=pull[:, axis], minlength=n)
                + np.bincount(ha, weights=push[:, axis], minlength=n)
            )
        pos += rate * disp

    return pos - pos.mean(0)


def retention(pos: np.ndarray, near: np.ndarray) -> float:
    """Of each row's `NEAR` semantic neighbours, how many are among its `NEAR` nearest on screen.

    The one number that says whether the map is telling the truth. A layout can look beautifully spread
    and still be arbitrary, and nothing else in this stage would notice: `xy.bin` would be the right
    length, every coordinate would be in range, and the picture would be a random scatter of 1,294 dots
    that a reader would try to read meaning into.
    """
    n = pos.shape[0]
    if n <= NEAR:
        return 0.0
    kept = 0
    step = 512
    for start in range(0, n, step):
        block = pos[start:start + step]
        d2 = ((block[:, None, :] - pos[None, :, :]) ** 2).sum(2)
        for r in range(block.shape[0]):
            d2[r, start + r] = np.inf
        close = np.argpartition(d2, NEAR, axis=1)[:, :NEAR]
        for r in range(block.shape[0]):
            kept += len(set(close[r].tolist()) & set(near[start + r].tolist()))
    return kept / n


def purity(pos: np.ndarray, label: np.ndarray, k: int = NEAR) -> tuple[float, float]:
    """Of the `k` rows nearest each row on screen, what share carry the same label -- and by chance.

    The only measurement here scored against something the layout never saw. `retention` asks whether the
    picture agrees with the vectors it was built from, which a layout can satisfy while still being
    unreadable; this asks whether it agrees with `cat`, the one label a human chose, and that is the
    question a visitor is really asking when they look for a neighbourhood on a map.

    The chance figure is returned alongside rather than left to the reader, because the raw share means
    nothing on its own: with 14 categories at this corpus's very uneven sizes, two rows drawn at random
    already share one 11.7% of the time, and a number that beats nothing needs to be seen next to what it
    beat. A random scatter measures 11.6% against that 11.7%, which is the control that makes the figure
    for a real layout worth quoting.
    """
    n = pos.shape[0]
    if n <= k or not len(label):
        return 0.0, 0.0
    _, counts = np.unique(label, return_counts=True)
    total = counts.sum()
    chance = float(((counts / total) * ((counts - 1) / max(total - 1, 1))).sum())
    same = 0
    step = 512
    for start in range(0, n, step):
        block = pos[start:start + step]
        d2 = ((block[:, None, :] - pos[None, :, :]) ** 2).sum(2)
        for r in range(block.shape[0]):
            d2[r, start + r] = np.inf
        close = np.argpartition(d2, k, axis=1)[:, :k]
        same += int((label[close] == label[start:start + block.shape[0], None]).sum())
    return same / float(n * k), chance


def spread(pos: np.ndarray, cells: int = 48) -> float:
    """The fraction of the bounding box the rows actually occupy, on a `cells` x `cells` grid.

    Distinguishes the two failure modes a single retention figure cannot: a dense blob with four outliers
    holding the box open scores well on neighbours and is unusable, because every row a reader wants to
    click is inside one percent of the pixels.
    """
    n = pos.shape[0]
    if not n:
        return 0.0
    lo, hi = pos.min(0), pos.max(0)
    size = np.maximum(hi - lo, 1e-9)
    grid = np.clip(((pos - lo) / size * cells).astype(np.int32), 0, cells - 1)
    return len(set(map(tuple, grid.tolist()))) / float(cells * cells)


def main() -> None:
    if not DATA.exists():
        sys.exit(f"{DATA} is missing; run 19_pages.py or 19b_refresh.py first.")
    fetch_model()

    data = json.loads(DATA.read_text(encoding="utf-8"))
    ix = {c: i for i, c in enumerate(data["cols"])}
    rows = data["rows"]
    cats = [c["name"] for c in data["cats"]]
    n_docs = len(rows)

    embed = load_matrix()
    full = {s: i for s, i in load_vocab().items() if i < embed.shape[0]}

    # Which tokens are allowed into the vocabulary at all. Continuations (`##ing`) stay: dropping them
    # would silently truncate every word the tokeniser split, and they are how a static table gets any
    # morphology at all. Bare punctuation goes, because `.`, `-`, `,` and `&` are in nearly every document
    # and dominated the first build's pooling.
    #
    # Stopwords are excluded here too, and that is now redundant rather than load-bearing: `wordpiece()`
    # drops them by word before it looks anything up, so a stopword token could never be reached even if it
    # were shipped. Excluded anyway, because a token nothing can look up is payload the reader downloads
    # for no reason. This filter is emphatically *not* what makes stopwords harmless -- believing that it
    # was is the bug described in the note on STOP.
    meaningful = {
        s: i for s, i in full.items()
        if s.startswith("##") or (re.search(r"[a-z0-9]", s) and s not in STOP)
    }

    texts, from_readme = [], 0
    for row in rows:
        text, used = doc_text(row, ix, cats)
        texts.append(text.lower())
        from_readme += used

    # Pass one, over the whole vocabulary, exists only to rank tokens by how many documents want them.
    # Nothing downstream uses this segmentation, because the browser will never be able to reproduce it.
    df = Counter()
    for text in texts:
        df.update(set(wordpiece(text, meaningful)))

    # Prune, then force-keep every single character and its continuation. Without that floor a word
    # whose pieces all fell outside the budget becomes unsegmentable and is dropped, so a rare literal
    # would vanish from the query instead of degrading into subwords.
    ranked = [tid for tid, _ in df.most_common(VOCAB)]
    floor = [i for s, i in meaningful.items() if len(s.lstrip("#")) == 1]
    ranked = list(dict.fromkeys(ranked + floor))
    inv = {i: s for s, i in full.items()}
    pruned = {inv[t]: t for t in ranked}

    # Pass two is the one that counts: re-segment every document against exactly the vocabulary the
    # reader will hold, and recompute the weights over *that* segmentation so the IDF a query is scored
    # with is the IDF the documents were built with.
    ids_per_doc = [wordpiece(text, pruned) for text in texts]
    df = Counter()
    for ids in ids_per_doc:
        df.update(set(ids))
    # Corpus IDF, damped. See the docstring: this exponent is the difference between a search that
    # knows what a sandbox is and one that only knows everything is an agent.
    weight = np.zeros(embed.shape[0], dtype=np.float32)
    for tid, count in df.items():
        weight[tid] = math.sqrt(math.log(1 + n_docs / (1 + count)))
    # Ordered by document frequency under the segmentation that is actually used, so the shipped table's
    # own prefix stays a usable smaller table if the budget ever shrinks.
    ranked.sort(key=lambda t: (-df.get(t, 0), inv[t]))
    ranked_set = set(ranked)

    # Project onto this corpus's principal directions, and do it on the *token* table so the client and
    # this stage cannot disagree. Pooling is a weighted sum, so pooling projected tokens and projecting
    # a pooled document are the same operation -- the normalisation that follows is the only non-linear
    # step, and both sides do it last, after pooling.
    pooled = np.zeros((n_docs, embed.shape[1]), dtype=np.float32)
    for i, ids in enumerate(ids_per_doc):
        if ids:
            pooled[i] = (embed[ids] * weight[ids][:, None]).sum(0)

    # The basis is fitted to the pooled documents as they are, *not* to their deviations from the corpus
    # mean, and that is a correctness constraint rather than a preference. Mean-centring is the usual
    # next move and it cannot survive the trip to the browser: the mean of this matrix is the scale of a
    # whole document -- a sum over some twenty-odd tokens -- so subtracting it from a three-word query
    # leaves the query as very nearly the negated mean, whatever the reader typed. Measured, with the
    # centre subtracted: nine unrelated queries returned the same four projects, at cosines of 0.74 to
    # 0.87, because every one of them had collapsed onto the same vector. Removing the shift restores
    # the arrangement the ranking was validated against, and it leaves both sides with the same two
    # steps -- sum the token vectors, normalise -- which is what makes a query and a document
    # comparable at all. Normalising last is also why summing and averaging are the same thing here.
    _, _, vt = np.linalg.svd(pooled, full_matrices=False)
    basis = vt[:DIMS].T.astype(np.float32)
    table = (embed[ranked] * weight[ranked][:, None]) @ basis
    slot_of = {tid: slot for slot, tid in enumerate(ranked)}

    # Segmented here rather than in either test, because the point of the fixture is that it is this
    # stage's answer and not a third opinion. `pruned` is keyed by token string over exactly `ranked`, so
    # what the readers hold in `vocab.json` is the same vocabulary this pass segments against.
    probe = [[text, [slot_of[t] for t in wordpiece(text, pruned)]] for text in PROBES]

    def pool(ids: list[int]) -> np.ndarray:
        slots = [slot_of[t] for t in ids if t in ranked_set]
        if not slots:
            return np.zeros(DIMS, dtype=np.float32)
        v = table[slots].sum(0)
        norm = float(np.linalg.norm(v))
        return v / norm if norm else v

    # A scale each, and this is not a tidiness point -- one shared scale silently destroys the index.
    # Documents are unit length so their components sit in [-1, 1], while a token vector is whatever
    # length its IDF made it, which here is nearly two orders of magnitude larger. Quantise both against
    # the larger and every document component rounds to 0 or +/-1: measured, 1,294 rows collapsed onto a
    # handful of distinct vectors, which surfaced as unrelated projects tying to three decimal places on
    # every query. So each matrix is quantised against its own maximum and `meta.json` carries both.
    # The vocabulary's scale then cancels out of the ranking anyway, because the query is normalised
    # after pooling; it is kept honest rather than dropped so the file can be read without knowing that.
    docs = np.stack([pool(ids) for ids in ids_per_doc]) if n_docs else np.zeros((0, DIMS), np.float32)
    doc_scale = float(np.abs(docs).max(initial=0.0)) or 1.0
    vocab_scale = float(np.abs(table).max(initial=0.0)) or 1.0
    docs_q = np.clip(np.rint(docs / doc_scale * 127), -127, 127).astype(np.int8)
    table_q = np.clip(np.rint(table / vocab_scale * 127), -127, 127).astype(np.int8)

    # Neighbours off the quantised vectors, not the float ones, so "more like this" agrees with what
    # the reader's browser will compute from the same bytes.
    near = np.zeros((n_docs, NEAR), dtype=np.uint16)
    unit = np.zeros((n_docs, DIMS), dtype=np.float32)
    if n_docs:
        unit = docs_q.astype(np.float32)
        unit /= np.maximum(np.linalg.norm(unit, axis=1, keepdims=True), 1e-6)
        step = 512
        for start in range(0, n_docs, step):
            sim = unit[start:start + step] @ unit.T
            for r in range(sim.shape[0]):
                sim[r, start + r] = -2.0
            order = np.argsort(-sim, axis=1)[:, :NEAR]
            near[start:start + step] = order.astype(np.uint16)

    # Where each row sits on the map. Quantised to int16 over the larger half-extent of the two axes, so
    # the aspect ratio the layout produced survives the trip -- scaling each axis to its own range would
    # stretch the picture to fill a square and pull apart rows the layout had placed together.
    xy = layout(unit, near)
    xy_scale = float(np.abs(xy).max(initial=0.0)) or 1.0
    xy_q = np.clip(np.rint(xy / xy_scale * 32767), -32767, 32767).astype(np.int16)
    # Measured on the quantised coordinates, which is what a reader gets, and against the plain projection
    # as a control -- a figure with nothing to compare it against does not say whether the solver earned
    # its epochs. Both are printed at the end of the run.
    seen = xy_q.astype(np.float32)
    cat_of = np.array([r[ix["cat"]] for r in rows])
    keep_map, fill_map = retention(seen, near), spread(seen)
    pure_map, chance = purity(seen, cat_of)
    # The control, and it has to be built here rather than quoted from the comment above: a figure with
    # nothing beside it does not say whether the solver earned its epochs, and a figure hard-coded in a
    # comment stops being true the first time the corpus changes.
    if n_docs:
        middled = unit - unit.mean(0)
        flat = middled @ np.linalg.svd(middled, full_matrices=False)[2][:2].T
    else:
        flat = np.zeros((0, 2), np.float32)
    keep_flat, fill_flat = retention(flat, near), spread(flat)
    pure_flat, _ = purity(flat, cat_of)

    # The fingerprint the page checks before it trusts any of this. Row count catches a rebuild that
    # changed length; the digest catches one that only reordered, which is the case that would rank
    # every project as its neighbour and look like a scoring bug.
    fingerprint = hashlib.sha256(
        "\n".join(str(r[ix["nwo"]]) for r in rows).encode("utf-8")
    ).hexdigest()[:16]

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "docs.bin").write_bytes(docs_q.tobytes())
    (OUT / "vocab.bin").write_bytes(table_q.tobytes())
    (OUT / "near.bin").write_bytes(near.tobytes())
    (OUT / "xy.bin").write_bytes(xy_q.tobytes())
    # LF and sorted keys: both files are committed, and the alternative is a diff every time the OS
    # that ran the build changes. Token strings are the tokeniser's own, so the client's WordPiece pass
    # matches this stage's by construction rather than by a second copy of the vocabulary.
    (OUT / "vocab.json").write_text(
        json.dumps({"tokens": [inv[t] for t in ranked]}, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8", newline="\n")
    (OUT / "meta.json").write_text(
        json.dumps({
            "schema": 1,
            "model": REPO,
            "dims": DIMS,
            "doc_scale": doc_scale,
            "vocab_scale": vocab_scale,
            "rows": n_docs,
            "vocab": len(ranked),
            "near": NEAR,
            # The map's quantisation scale. Not the ranking's -- these are pixels, not similarities, and
            # a reader who conflated them would be dividing a coordinate by a cosine.
            "xy_scale": xy_scale,
            "fingerprint": fingerprint,
            "indexed_from_readme": from_readme,
            "probe": probe,
            # Shipped, not transcribed. Every other part of the tokeniser is a transcription in each of
            # the three languages, because an expression cannot be shared across them -- but a word list
            # can be, and this one has to be exact: a query stripped of a different set of words than the
            # documents were is the same silent mis-scoring as a different segmentation. ~1.5 KB, sorted
            # so the committed file does not churn.
            "stop": sorted(STOP),
            "snapshot": data.get("snapshot", ""),
        }, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

    total = 0
    for name in ("meta.json", "vocab.json", "vocab.bin", "docs.bin", "near.bin", "xy.bin"):
        size = (OUT / name).stat().st_size
        total += size
        print(f"docs/search/{name:12s} {size / 1024:9.1f} KB")
    print(f"{'total':25s} {total / 1024:9.1f} KB lazily, after the first paint")
    # `ranked` is the budget's pick plus the single-character floor, so it can exceed the number of
    # tokens the corpus actually uses; reporting it against `len(df)` alone read as "6,298 of 5,338".
    used = sum(1 for t in ranked if df.get(t))
    print(f"{n_docs:,} rows · {DIMS} dims · {len(ranked):,} tokens shipped "
          f"({used:,} the corpus uses, {len(ranked) - used:,} kept so every word stays segmentable) · "
          f"fingerprint {fingerprint}")
    print(f"map: {pure_map:.0%} of each row's {NEAR} on-screen neighbours share its category "
          f"({chance:.0%} by chance), {keep_map:.1f}/{NEAR} semantic neighbours stay adjacent, "
          f"{fill_map:.0%} of the box occupied")
    print(f"     the plain 2-component projection this replaced scores {pure_flat:.0%} / "
          f"{keep_flat:.1f} / {fill_flat:.0%} on the same three")
    if pure_map <= chance * 2:
        print(f"     WARNING: purity is within 2x of chance, so the map is close to arbitrary. Something "
              f"is wrong with the layout or with the vectors it was built from.")
    if from_readme == n_docs:
        print(f"indexed from READMEs for all {n_docs:,} rows")
    else:
        print(f"indexed from READMEs for {from_readme:,}/{n_docs:,} rows; the rest fell back to their "
              f"blurb (~24 tokens). Relevance is capped by that: warm cache/readmes/ and re-run.")


if __name__ == "__main__":
    main()
