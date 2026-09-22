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
                     on screen, the share sharing its category has to close a fifth of the gap between
                     what two rows drawn at random would share and 1.0. The *share of the gap* and not a
                     multiple of chance, because chance moves with the category distribution and a
                     multiple of it silently demands more purity as the corpus concentrates -- which is
                     exactly what happened on 2026-09-21. A layout that collapsed, or one seeded off the
                     clock, closes none of the gap while every shape assertion above still passes.
  the retrieval   -- the queries this feature exists for, scored on what a reader sees: of the ten rows
                     each query returns, how many name the topic the query asked about. Never on a
                     similarity and no longer on one fixture repository's rank either -- the corpus went
                     from 1,294 rows to 8,856 and every absolute measure of one project's place in it,
                     rank included, turned into a measure of how crowded its neighbourhood is.
  the regression  -- that these queries really do return nothing under the substring filter the page
                     ships today. Without this the retrieval group proves the index works and not that
                     it was ever needed, and it is the half that will look wrong to a later reader. Five
                     of the eight, printing the ones that have stopped being zero-result and why.

What this cannot see: whether the vectors are *good*. Ranking quality is bounded by how much text each
row has, and with a cold `cache/readmes/` every row falls back to a ~24-token blurb -- so the retrieval
group is deliberately scored as a proportion rather than as a set of individual musts. A cold-cache
build genuinely is worse at this than a warm one, and a test that demanded warm-cache rankings from a
cold-cache index would fail for a reason that has nothing to do with the code. `meta.json` names which
build it was: `indexed_from_readme` is 0 on the committed 1,294-row index and 7,965 of 8,856 on the first
weekly to complete, which is the largest single change to the corpus this file has ever scored.

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

# Each case is a query that returns nothing, or nearly nothing, from the page's current substring filter
# (that is the regression group's claim, and it is measured rather than assumed); a repository that is a
# good answer to it, kept for context; and a pattern naming the topic the query is about, in the words a
# project about that topic uses. Matched on `nwo` rather than the display name because a name is editable
# upstream and `owner/name` is the key everything else in the atlas is indexed by.
#
# THE ASSERTION IS ON THE TOPIC, NOT ON THE REPOSITORY, AND THAT CHANGED IN THIS FILE'S SECOND YEAR OF
# LIFE. It used to require each named repository inside a fixed rank -- top 5, top 10, top 20 -- and the
# docstring said out loud why that was the wrong shape ("any absolute threshold true today would be false
# then") while doing it anyway one level up: a rank is absolute too. The 2026-09-21 ingest took the corpus
# from 1,294 rows to 8,856 and five of the eight cases "failed" with a top ten full of better answers than
# the fixture's own. `something to review PRs` returned three PR-review agents above `pr-agent`;
# `chat with my pdfs` returned a literal chat-with-your-PDFs app at rank two and put the fixture at 71.
# What the fixture rank had been measuring was how alone its repository was in the corpus.
#
# So the measurement is: of the eighty rows these eight queries put in front of a reader, how many name the
# thing the reader asked about. Measured 51 of 80 on the committed 1,294-row index, 64 of 80 on the 8,856-row
# one -- it got better, not worse -- against 5 to 7 of 80 for a ranking drawn at random, which is what every
# failure this group exists for degrades to. The patterns are the test author's, written from the query and
# never shown to the index, so they cannot be satisfied by the index agreeing with itself.
CASES = [
    ("something to review PRs", "The-PR-Agent/pr-agent", r"\bpr\b|pull[- ]request|review"),
    ("scrape websites", "xberg-io/plugins", r"scrap|crawl|web ?page|website"),
    ("run agents in parallel", "actionbook/actionbook",
     r"parallel|concurren|multi[- ]?agent|orchestrat|swarm|fleet|worktree"),
    ("sandbox my agent safely", "kubernetes-sigs/agent-sandbox", r"sandbox|isolat|secur|safe|contain"),
    ("chat with my pdfs", "xwmxcz/papers-skill", r"pdf|document|paper"),
    ("agent that writes tests", "mgechev/skillgrade", r"\btest|spec|\bqa\b|coverage|e2e"),
    ("turn speech into text", "cjpais/Handy",
     r"speech|voice|transcri|audio|dictat|\btts\b|\bstt\b|whisper|podcast"),
    ("observability dashboards", "vivekchand/clawmetry",
     r"observab|dashboard|telemetr|metric|monitor|otel|grafana|trace"),
]
# Half of the eighty. Deliberately well under both measured builds and six times the random null, because
# what this has to separate is a working index from a broken one, and the gap between those two is the
# 45 rows between 51 and 6 rather than the 13 between 51 and 64.
ON_TOPIC = 40
# And how many of the eight the substring filter has to be unable to answer at all. Five, down from six: the
# ingest that grew the corpus 6.8x gave `scrape websites` three literal matches it did not have before. That
# is a fact about the corpus, not about this code, and it is why the weight of this group now sits on
# ON_TOPIC above -- see "the regression" at the bottom of `main`.
ZERO_RESULT = 5


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
    # And the extent is the corpus's, not a few outliers'. The page fits the map to its bounding box, so
    # the check above is satisfied by eight rows at the rim and 8,850 in a dot at the centre -- which is
    # what shipped at 8,858 rows, with the 1st-99th percentile spanning ~2,000 of 65,534.
    def body(vals: list[int]) -> int:
        s = sorted(vals)
        return s[int(len(s) * 0.99)] - s[int(len(s) * 0.01)] if s else 0
    body_x, body_y = body([x for x, _ in at]), body([y for _, y in at])
    h.check("the body of the corpus fills the map, not just its outliers", min(body_x, body_y) > 16384,
            f"the 1st-99th percentile spans {body_x} x {body_y} of a possible 65,534")

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
        # HOW FAR ACROSS THE AVAILABLE GAP, NOT HOW MANY TIMES CHANCE. This was `pure >= chance * 2.5`,
        # measured at 5.2x on the committed index, and a multiple of chance is not a scale-free number: the
        # most any layout can score is 1/chance, so the headroom above the floor is a function of the
        # *category distribution* and not of the layout at all. The 2026-09-21 ingest concentrated that
        # distribution hard -- the largest category went from 278 of 1,294 rows (21%) to 4,537 of 8,856
        # (51%), which took chance from 11.7% to 29.0% and the ceiling from 8.5x to 3.4x -- so 2.5x quietly
        # became a demand for 72.5% purity from a 2-D projection of 8,856 points, and the map failed a bar
        # it had never been asked to clear.
        #
        # The gap from chance to 1.0 is the room a layout actually has, and the share of it taken is
        # invariant: 0.55 on the 1,294-row index (60.5% against 11.7%), 0.31 on the 8,856-row one (51.1%
        # against 29.0%), and 0.00 for the null -- measured, by shuffling the positions between rows and
        # re-running this exact statistic, which scored 28.2% against a 29.0% chance. A floor of 0.20 is
        # nineteen standard deviations clear of that null and clears both real builds.
        lift = (pure - chance) / (1.0 - chance) if chance < 1.0 else 0.0
        h.check(f"the map groups like with like ({pure:.0%} of neighbours share a category, "
                f"{chance:.0%} by chance)", lift >= 0.20,
                f"{pure:.1%} against {chance:.1%} by chance closes {lift:.2f} of the gap between them, "
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
    # What a card shows: the three fields a reader can see before clicking. Not `lang` or `listed_by`, which
    # the page's substring filter does search and which would let "secur" be satisfied by the name of the
    # list a project was found in rather than by anything the project does.
    about = [" ".join(str(r[ix[k]] or "") for k in ("name", "nwo", "blurb")).lower()
             for r in data["rows"]]
    on_topic = 0
    for query, nwo, pattern in CASES:
        rx = re.compile(pattern)
        ranked = [i for _, i in score(query)[:10]]
        hit = [i for i in ranked if rx.search(about[i])]
        on_topic += len(hit)
        # The fixture repository's rank, reported and not asserted. It is the record of what this group used
        # to check and it is still the first thing to look at when the number above drops -- but a rank in a
        # corpus that grew 6.8x measures crowding, so it is context for a human rather than a threshold.
        target = where.get(nwo.lower())
        if target is None:
            where_it_is = f"{nwo} is no longer in the corpus"
        else:
            full = [i for _, i in score(query)]
            place = full.index(target) + 1
            where_it_is = f"{nwo} is at {place} of {rows}"
        print(f"  {len(hit):2}/10 on topic for {query!r} -- {where_it_is}")
    h.check(f"the eight queries put {on_topic} on-topic projects in their top tens",
            on_topic >= ON_TOPIC,
            f"only {on_topic} of 80, against {ON_TOPIC} required and 5 to 7 for a random ranking -- "
            f"the index is returning rows that do not name what was asked for")

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
        n = sum(1 for h_ in hay if all(w in h_ for w in words))
        if not n:
            still_zero += 1
        else:
            # Printed rather than silent, because this is the number that decays as the corpus grows and the
            # only way a later reader can see it moving. `run agents in parallel` has never been zero-result
            # -- three common words, 13 incidental matches at 1,294 rows and 23 at 8,856 -- and `scrape
            # websites` stopped being one in the 2026-09-21 ingest.
            print(f"  {query!r} is no longer zero-result: {n} row(s) match every word")
    h.check("these queries return nothing from the substring filter", still_zero >= ZERO_RESULT,
            f"only {still_zero} of {len(CASES)} are zero-result today, against {ZERO_RESULT} required")

    print(f"\n{h.passed} passed, {len(h.failed)} failed")
    for line in h.failed:
        print(f"  {line}")
    return 1 if h.failed else 0


if __name__ == "__main__":
    sys.exit(main())
