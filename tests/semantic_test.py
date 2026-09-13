"""The semantic index, scored using nothing but the bytes a reader downloads -- JFH-293.

`scripts/27_semantic.py` builds `docs/search/` with numpy, a 30 MB model and a corpus of READMEs. The
browser has none of those. It has five files and about forty lines of JavaScript, and the entire premise
of the feature is that those five files are sufficient: tokenise the query against the shipped
vocabulary, add up the shipped token vectors, normalise, dot against the shipped document vectors. So
this file imports neither numpy nor the build stage. It reimplements the reader's half in the standard
library and asserts on the artefacts as committed, which is the only version of the code that a visitor
ever runs.

That makes `wordpiece()` here the third copy of one algorithm -- the stage has one, `docs/index.html`
has one, this file has one -- and the duplication is the point rather than an oversight. A query
segmented one way against documents segmented another scores noise while looking completely healthy, so
the copies exist to be compared. `segmentation_matches_the_stage()` below is what notices when they
drift: `meta.json` ships the stage's own segmentation of eight texts as `probe`, and this file asserts
its transcription reproduces them token id for token id. `tests/probe.mjs` asserts the same fixtures
against the page's `semTokens()`, which is the copy whose drift a reader would actually feel.

Nine groups:

  the shape       -- every file's length agrees with `meta.json`. int8 matrices carry no dimensions of
                     their own, so a wrong `dims` is undetectable from the bytes and catastrophic in
                     use: it reinterprets the whole matrix at an offset.
  the guard       -- the fingerprint and row count match `docs/data.json` as committed. This is the
                     failure that cannot be allowed to be silent: vectors are addressed by row ordinal,
                     so an index built against a different `data.json` returns each project's
                     *neighbour*, confidently, with no error anywhere.
  the arithmetic  -- documents dequantise to unit length, and separate scales survived. Both matrices
                     were quantised against one shared maximum in the first build and 1,294 documents
                     collapsed onto a handful of distinct vectors; the symptom was unrelated projects
                     tying to three decimal places, which is exactly what a test sees as "a ranking".
  the vocabulary  -- every ASCII word is segmentable, so no query silently loses a term.
  the tokeniser   -- this file's transcription reproduces the stage's own segmentation exactly, on the
                     `probe` fixtures in `meta.json`. The one failure in this feature with no symptom:
                     nothing throws, a full page of results comes back, and they are ranked by noise.
  the chatter     -- a question with no topic in it produces no tokens, and therefore no answer. Every
                     word of "please help me choose" is a stopword, and stopwords are dropped before
                     segmentation rather than left out of the vocabulary -- which is what the build used
                     to do, and which re-spelled them as rare, heavily weighted fragments instead. Nine
                     such questions each returned twelve confident, unrelated projects before this.
  the map         -- `xy.bin` is a picture of the corpus and not a random scatter. Asserted against
                     `cat`, the curated label the layout never saw: of the eight rows nearest a project
                     on screen, the share sharing its category has to beat what two rows drawn at random
                     would share. A ratio, never an absolute, for the same reason the retrieval group
                     asserts on rank -- 14 categories at these very uneven sizes put chance at 11.7%
                     today and somewhere else after the ingest. A layout that silently collapsed, or one
                     seeded off the clock, scores 1x here while every shape assertion above still passes.
  the retrieval   -- the queries this feature exists for. Each names a project that ought to surface,
                     and the assertion is on its *rank*, never on a similarity: this corpus is about to
                     go from 1,294 rows to some 8,293, and any absolute threshold true today would be
                     false then.
  the regression  -- that these queries really do return nothing under the substring filter the page
                     ships today. Without this the retrieval group proves the index works and not that
                     it was ever needed, and it is the half that will look wrong to a later reader.

What this cannot see: whether the vectors are *good*. Ranking quality is bounded by how much text each
row has, and with a cold `cache/readmes/` every row falls back to a ~24-token blurb -- so the retrieval
group is deliberately scored as a proportion rather than as a set of individual musts. A cold-cache
build genuinely is worse at this than a warm one, and a test that demanded warm-cache rankings from a
cold-cache index would fail for a reason that has nothing to do with the code.

Standard library only.
"""
from __future__ import annotations

import array
import hashlib
import json
import math
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEARCH = ROOT / "docs" / "search"
DATA = ROOT / "docs" / "data.json"

WORD = re.compile(r"[a-z0-9]+|[^\sa-z0-9]")

# Each case is a query that returns *nothing* from the page's current substring filter, and a repo that
# ought to come back for it. Matched on `nwo` rather than the display name because a name is editable
# upstream and `owner/name` is the key everything else in the atlas is indexed by. A case whose repo is
# not in the corpus at all is skipped, not failed -- the source lists are somebody else's, and a project
# leaving one of them is not a bug in this index.
CASES = [
    ("something to review PRs", "The-PR-Agent/pr-agent", 5),
    ("scrape websites", "xberg-io/plugins", 5),
    ("run agents in parallel", "actionbook/actionbook", 10),
    ("sandbox my agent safely", "kubernetes-sigs/agent-sandbox", 10),
    ("chat with my pdfs", "xwmxcz/papers-skill", 10),
    ("agent that writes tests", "mgechev/skillgrade", 10),
    ("turn speech into text", "cjpais/Handy", 20),
    ("observability dashboards", "vivekchand/clawmetry", 10),
]
# Six of eight. The floor is a proportion because relevance is capped by the text available per row, and
# a cold `cache/readmes/` build is honestly worse at this than a warm one; see the docstring.
FLOOR = 6


class Harness:
    def __init__(self) -> None:
        self.passed = 0
        self.failed: list[str] = []

    def check(self, label: str, ok: bool, detail: str = "") -> None:
        if ok:
            self.passed += 1
            print(f"  ok   {label}")
        else:
            self.failed.append(f"{label}: {detail}")
            print(f"  FAIL {label} -- {detail}")


def read_json(path: Path) -> dict:
    """UTF-8, explicitly. The default on Windows is cp1252 and `vocab.json` holds tokens it cannot
    decode, which reads as a corrupt artefact when it is a corrupt *reader*."""
    return json.loads(path.read_text(encoding="utf-8"))


def wordpiece(text: str, vocab: dict[str, int], stop: set[str]) -> list[int]:
    """Greedy longest-match WordPiece. A transcription of `27_semantic.wordpiece`; see the docstring.

    `stop` comes from `meta.json` rather than from a fourth copy of the word list. It is applied to the
    whole word before any lookup, which is the placement that matters: a stopword left out of the
    *vocabulary* is re-spelled from its rarest surviving pieces and comes back weighted higher than the
    content words around it.
    """
    out: list[int] = []
    for word in WORD.findall(text.lower()):
        if word in stop:
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


def segmentation_matches_the_stage(h: "Harness", meta: dict, slot: dict[str, int],
                                   stop: set[str]) -> None:
    """Assert this file's `wordpiece` agrees with the one that built the index, fixture by fixture.

    `27_semantic.py` segments the strings in its `PROBES` with the reference implementation and writes
    each one's slot ordinals into `meta.json` as `probe`. Comparing against that is the only way this
    suite can see tokeniser drift at all: the two implementations are in different languages, so there is
    nothing to share and no import that would fail. Everything else about a drifted tokeniser looks
    healthy -- the files are the right length, the documents are unit length, the fingerprint matches,
    and every query returns a full page of confidently ranked, wrong answers.

    Slot ordinals rather than token strings, because ordinals are what both readers address `vocab.bin`
    by. A rebuild that reordered the vocabulary without changing the segmentation would score noise just
    as thoroughly, and would pass a comparison made on strings.

    One assertion per fixture, not one for the set, so a failure names the string that drifted.
    """
    probe = meta.get("probe")
    if not probe:
        h.check("meta.json ships probe fixtures", False,
                "no `probe` key -- rebuild with scripts/27_semantic.py, or this group asserts nothing")
        return
    for text, expected in probe:
        got = wordpiece(text, slot, stop)
        h.check(f"segments {text!r} the way the stage did", got == list(expected),
                f"stage got {expected}, this file got {got}")


def main() -> int:
    h = Harness()
    if not SEARCH.exists():
        print(f"{SEARCH} is missing; run scripts/27_semantic.py")
        return 1

    meta = read_json(SEARCH / "meta.json")
    tokens = read_json(SEARCH / "vocab.json")["tokens"]
    slot = {t: i for i, t in enumerate(tokens)}
    dims, rows = meta["dims"], meta["rows"]
    doc_scale = meta["doc_scale"] / 127.0
    vocab_scale = meta["vocab_scale"] / 127.0

    docs = array.array("b")
    docs.frombytes((SEARCH / "docs.bin").read_bytes())
    table = array.array("b")
    table.frombytes((SEARCH / "vocab.bin").read_bytes())
    near = array.array("H")
    near.frombytes((SEARCH / "near.bin").read_bytes())
    xy = array.array("h")
    xy.frombytes((SEARCH / "xy.bin").read_bytes())

    print("the shape")
    h.check("docs.bin is rows x dims", len(docs) == rows * dims,
            f"{len(docs)} bytes, expected {rows * dims}")
    h.check("vocab.bin is tokens x dims", len(table) == len(tokens) * dims,
            f"{len(table)} bytes, expected {len(tokens) * dims}")
    h.check("vocab.json matches meta", len(tokens) == meta["vocab"],
            f"{len(tokens)} tokens, meta says {meta['vocab']}")
    h.check("near.bin is rows x near", len(near) == rows * meta["near"],
            f"{len(near)} entries, expected {rows * meta['near']}")
    h.check("xy.bin is rows x 2", len(xy) == rows * 2, f"{len(xy)} entries, expected {rows * 2}")
    h.check("every neighbour is a real row", all(0 <= n < rows for n in near), "index out of range")
    h.check("no row is its own neighbour",
            all(near[i * meta["near"] + k] != i for i in range(rows) for k in range(meta["near"])),
            "a row neighbours itself")

    print("the guard")
    data = read_json(DATA)
    ix = {c: i for i, c in enumerate(data["cols"])}
    fingerprint = hashlib.sha256(
        "\n".join(str(r[ix["nwo"]]) for r in data["rows"]).encode("utf-8")
    ).hexdigest()[:16]
    h.check("row count matches docs/data.json", rows == len(data["rows"]),
            f"index has {rows}, data.json has {len(data['rows'])}")
    h.check("fingerprint matches docs/data.json", fingerprint == meta["fingerprint"],
            f"data.json is {fingerprint}, index was built against {meta['fingerprint']} "
            f"-- re-run scripts/27_semantic.py")

    print("the arithmetic")
    norms = []
    for i in range(rows):
        base = i * dims
        norms.append(math.sqrt(sum((docs[base + d] * doc_scale) ** 2 for d in range(dims))))
    unit = [n for n in norms if abs(n - 1.0) <= 0.02]
    h.check("documents dequantise to unit length", len(unit) >= rows - max(2, rows // 100),
            f"{rows - len(unit)} of {rows} rows are not unit length")
    h.check("the two scales really are separate", meta["doc_scale"] != meta["vocab_scale"],
            "one shared scale crushes the document matrix; see the docstring")
    distinct = len({bytes(docs[i * dims:(i + 1) * dims]) for i in range(rows)})
    h.check("documents are distinct vectors", distinct >= rows * 0.95,
            f"only {distinct} distinct vectors across {rows} rows")

    print("the vocabulary")
    stop = set(meta.get("stop", ()))
    h.check("meta.json ships the stopword list", bool(stop),
            "no `stop` key -- the page would strip nothing and topicless questions would score")
    unsegmentable = [w for w in ("kubernetes", "sandbox", "observability", "zzzqqx", "gpt4o")
                     if not wordpiece(w, slot, stop)]
    h.check("every ascii word segments", not unsegmentable, f"lost {unsegmentable}")
    # The list has to be applied, not merely shipped, and it has to leave content words alone. Asserted
    # in both directions because a stoplist that swallowed "agent" would decline every real query and
    # would still make the group above pass.
    h.check("stopwords are absent from the shipped vocabulary",
            not [w for w in ("the", "should", "please") if w in slot],
            "a stopword has a token, so it can still be looked up")
    h.check("content words are not stopped",
            not [w for w in ("agent", "sandbox", "browser", "review", "speech") if w in stop],
            "a topical word is in the stoplist, which would decline real queries")

    print("the tokeniser")
    segmentation_matches_the_stage(h, meta, slot, stop)

    def score(query: str) -> list[tuple[float, int]]:
        vec = [0.0] * dims
        for s in wordpiece(query, slot, stop):
            base = s * dims
            for d in range(dims):
                vec[d] += table[base + d] * vocab_scale
        norm = math.sqrt(sum(x * x for x in vec))
        if not norm:
            return []
        vec = [x / norm for x in vec]
        out = []
        for i in range(rows):
            base = i * dims
            out.append((sum(docs[base + d] * doc_scale * vec[d] for d in range(dims)), i))
        out.sort(reverse=True)
        return out

    print("the map")
    # `xy_scale` is validated the way the other two scales are, and for the same reason: it is a divisor
    # the page applies to every coordinate, so a zero or a NaN here does not fail, it draws every project
    # on top of the origin or nowhere at all.
    xy_scale = meta.get("xy_scale")
    h.check("meta.json ships a usable xy_scale",
            isinstance(xy_scale, (int, float)) and xy_scale == xy_scale and xy_scale > 0,
            f"xy_scale is {xy_scale!r}")
    at = [(xy[i * 2], xy[i * 2 + 1]) for i in range(rows)]
    h.check("no two projects share a position", len(set(at)) >= rows * 0.99,
            f"only {len(set(at))} distinct positions across {rows} rows")
    span_x = max(x for x, _ in at) - min(x for x, _ in at) if rows else 0
    span_y = max(y for _, y in at) - min(y for _, y in at) if rows else 0
    # Both axes, because a layout that collapsed onto a line keeps a full extent on one of them.
    h.check("the map has extent on both axes", min(span_x, span_y) > 32767,
            f"spans {span_x} x {span_y} of a possible 65,534")

    # Purity: the assertion that the picture means something. Sampled rather than exhaustive -- 1,294 rows
    # is 1.67M distances in pure Python and this harness runs in under a second -- and sampled with a fixed
    # seed so a failure is reproducible rather than a coin toss somebody re-runs until it passes.
    cat_at = ix.get("cat")
    if cat_at is None:
        h.check("docs/data.json carries a cat column", False, "no `cat` column to score the map against")
    else:
        cat = [r[cat_at] for r in data["rows"]]
        counts: dict = {}
        for c in cat:
            counts[c] = counts.get(c, 0) + 1
        chance = sum((n / rows) * ((n - 1) / max(rows - 1, 1)) for n in counts.values()) if rows else 0.0
        sample = random.Random(20260912).sample(range(rows), min(200, rows))
        same = 0
        for i in sample:
            xi, yi = at[i]
            far = sorted(((xi - at[j][0]) ** 2 + (yi - at[j][1]) ** 2, j)
                         for j in range(rows) if j != i)[:8]
            same += sum(1 for _, j in far if cat[j] == cat[i])
        pure = same / float(len(sample) * 8) if sample else 0.0
        # 2.5x. Measured at 5.2x on the committed index -- 60% against 11.7% -- and a random scatter
        # measures 1.0x, so this floor sits well clear of both the real answer and the failure it is for.
        h.check(f"the map groups like with like ({pure:.0%} of neighbours share a category, "
                f"{chance:.0%} by chance)", pure >= chance * 2.5,
                f"{pure:.1%} against {chance:.1%} by chance is {pure / chance:.1f}x, "
                f"which is close enough to arbitrary that the map is not worth drawing")
        # The other direction, and the cheaper one: the rows `near.bin` calls neighbours have to be closer
        # together on the map than two rows picked at random. Purity could in principle be satisfied by a
        # layout that grouped categories while ignoring the graph it was built from.
        rng = random.Random(20260913)
        edge_d = 0.0
        for i in range(rows):
            for k in range(meta["near"]):
                j = near[i * meta["near"] + k]
                edge_d += ((at[i][0] - at[j][0]) ** 2 + (at[i][1] - at[j][1]) ** 2) ** 0.5
        edge_d /= max(rows * meta["near"], 1)
        rand_d = 0.0
        for _ in range(4000):
            i, j = rng.randrange(rows), rng.randrange(rows)
            rand_d += ((at[i][0] - at[j][0]) ** 2 + (at[i][1] - at[j][1]) ** 2) ** 0.5
        rand_d /= 4000
        h.check(f"neighbours land closer than strangers ({edge_d:,.0f} vs {rand_d:,.0f})",
                edge_d < rand_d * 0.5,
                f"a neighbour averages {edge_d:,.0f} away and a random row {rand_d:,.0f}, so the layout "
                f"is not honouring near.bin")

    print("the retrieval")
    where = {str(r[ix["nwo"]]).lower(): i for i, r in enumerate(data["rows"])}
    hits, tried = 0, 0
    for query, nwo, top in CASES:
        target = where.get(nwo.lower())
        if target is None:
            print(f"  skip {query!r} -- {nwo} is not in this corpus")
            continue
        tried += 1
        ranked = [i for _, i in score(query)[:top]]
        if target in ranked:
            hits += 1
            print(f"  ok   {query!r} finds {nwo} at rank {ranked.index(target) + 1}")
        else:
            full = [i for _, i in score(query)]
            place = full.index(target) + 1 if target in full else "unranked"
            print(f"  miss {query!r} wanted {nwo} in the top {top}, it is at {place}")
    # The floor scales with how many cases the corpus can actually host, so a project leaving a source
    # list weakens the assertion rather than breaking it -- but it never reads as a bar it did not clear.
    need = min(FLOOR, tried)
    h.check(f"at least {need} of {tried} natural-language queries land",
            tried > 0 and hits >= need, f"only {hits} of {tried}")

    print("the chatter")
    # Not "ranks them low" -- produces no tokens at all, so `semVector()` in the page returns null and the
    # feature declines before it touches the corpus. That is the whole reason the stoplist is applied to
    # the word instead of to the vocabulary: there is no threshold here to get wrong, and the answer does
    # not drift as the corpus grows. Each of these returned twelve confident, unrelated projects under the
    # build that pruned stopwords from the vocabulary instead.
    for query in ("what should I use", "how do I get started with this", "please help me choose",
                  "the best thing for me", "is this any good", "what do you recommend",
                  "can someone explain", "i need something better", "tell me more about it",
                  "what are the options", "i just want something that works", "the"):
        h.check(f"{query!r} has no topic in it, so it scores nothing", not wordpiece(query, slot, stop),
                f"segmented to {wordpiece(query, slot, stop)}, which would return 12 rows")
    # The other direction, and the one that would break the feature if the list grew carelessly: chatter
    # wrapped around a real topic must keep the topic. "what should I use to scrape a website" is the
    # query this feature exists for, spelled the way people actually type it.
    for query, want in (("what should I use to scrape a website", "scrape"),
                        ("find me a code review bot", "review"),
                        ("recommend a good sandbox", "sandbox"),
                        ("i need something to run tests", "tests")):
        ids = wordpiece(query, slot, stop)
        keeps = set(ids) >= set(wordpiece(want, slot, stop))
        h.check(f"{query!r} still carries {want!r}", bool(ids) and keeps,
                f"segmented to {ids}, which has lost the only topical word in it")

    print("the regression")
    # The page's filter, reproduced: every word of the query must appear as a raw substring of one
    # concatenated field. This is what the eight queries above are measured against.
    hay = [" ".join(str(r[ix[k]] or "") for k in ("name", "nwo", "blurb", "lang", "listed_by")).lower()
           for r in data["rows"]]
    still_zero = 0
    for query, _, _ in CASES:
        words = query.lower().split()
        if not any(all(w in h_ for w in words) for h_ in hay):
            still_zero += 1
    h.check("these queries return nothing from the substring filter", still_zero >= FLOOR,
            f"only {still_zero} of {len(CASES)} are actually zero-result today")

    print(f"\n{h.passed} passed, {len(h.failed)} failed")
    for line in h.failed:
        print(f"  {line}")
    return 1 if h.failed else 0


if __name__ == "__main__":
    sys.exit(main())
