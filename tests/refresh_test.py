"""Unit tests for the staleness guard in `scripts/19b_refresh.py` -- JFH-220.

That stage is the only render path that works without the 64 MB crawl cache, which is why it is the one
anybody reaches for when a committed artifact is behind its generator, and it renders a page out of two
different eras of the repository at once. `__COUNT__` and `__STARS__` are counted from the *committed*
`docs/data.json`; the sentences around them -- "eleven awesome-lists", "all eleven source lists are
credited", `#the-eleven-lists` -- are literals in the *live* `19_pages.PAGE`. Between adding a source and
the next full rebuild those two halves describe different datasets, and the stage would happily publish
the mixture to the deploy branch. `check_sources` refuses instead.

The disagreement is *constructed* here rather than waited for. On this checkout the two agree -- eleven
lists configured, eleven named by the rows -- so a test that only ran the guard would prove nothing about
the branch that matters. Six groups:

  the reader     -- `source_labels` on every `listed_by` shape: several labels per row, the same label in
                    two rows, padding, empty strings, a trailing comma, and a `data.json` that has no
                    such column at all.
  the guard      -- a fabricated dataset against a fabricated `SOURCES`, one too many and one too few,
                    and what the refusal says. Both numbers, both name lists, and the escape hatch.
  the stage      -- `main()` itself, three times over a scratch `docs/`: it refuses and writes nothing;
                    `--allow-stale` renders anyway and says so on stderr; and with the two in agreement
                    it renders as it always did. That last one is the acceptance criterion that matters
                    most -- a guard that breaks the only cache-free render path is worse than the bug.
  the hazard     -- that the mixture is real. Drop a row from the committed data and the rendered count
                    and star total both move; the word "eleven" beside them does not.
  the rows       -- that `refresh_data` hands every cell but `first_seen` straight through, which is why
                    a refresh cannot correct the disagreement on its own.
  the source     -- textual tripwires: the check precedes the first write, and the docstring still says
                    which side of the page comes from which era. Both are the kind of thing a later edit
                    removes without any test noticing.

What this cannot see: whether a real crawl would produce the labels it counts. Stages 14+ need
`cache/records_all.json` and friends, so the only dataset available offline is the committed one, and the
implied source count is an inference from it -- see `check_sources` for exactly what it measures and where
it can be wrong. Nothing here writes to the real `docs/`: `main()` is only ever pointed at a scratch copy,
with `reversion()` stubbed, so a broken guard cannot reach the deployable tree from inside this file.

Standard library only. `19b_refresh` reaches `openpyxl` transitively -- it loads `19_pages`, which loads
`17_markdown`, which loads `16_build_all` -- exactly as `pagemin_test.py` already does; nothing new is
required by this file.

Run: python tests/refresh_test.py
"""
from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import json
import os
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

# `importlib` because the module's name starts with a digit, so `import` cannot reach it -- the same load
# the stage itself uses for `19_pages.py`, and the same one `pagemin_test.py` uses.
spec = importlib.util.spec_from_file_location("b19b_for_test", SCRIPTS / "19b_refresh.py")
b19b = importlib.util.module_from_spec(spec)
sys.modules["b19b_for_test"] = b19b
spec.loader.exec_module(b19b)

# Under `run.mjs` this lands inside the run's own scratch root, which is swept on the way out however the
# run ended. Alone it lands in the OS temp directory.
TMP = Path(tempfile.mkdtemp(prefix="refresh_test_", dir=os.environ.get("AAA_TMP") or None))

ok = bad = 0


def eq(name: str, got, want) -> None:
    global ok, bad
    if got == want:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}\n  got  {got!r}\n  want {want!r}")


def true(name: str, cond, detail: str = "") -> None:
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}" + (f"\n  {detail}" if detail else ""))


def raises(name: str, kind, fn) -> str:
    """The exception and the message it carries -- for a guard, both are the deliverable."""
    global ok, bad
    try:
        fn()
    except kind as e:
        ok += 1
        return str(e)
    bad += 1
    print(f"FAIL {name} did not raise {kind.__name__}")
    return ""


def says(name: str, text: str, needle: str) -> None:
    global ok, bad
    if needle in text:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}\n  {needle!r} is not in:\n  {text!r}")


def dataset(*listed_by: str) -> dict:
    """A `data.json` in miniature: one row per argument, `listed_by` written as the build writes it.

    Only the columns the guard and the row walk touch. `lists` is filled to match its row rather than
    left at zero, because the committed file's own invariant is that the two agree -- asserted below on
    all 1,294 real rows -- and a fixture that breaks it would be testing a shape that cannot occur.
    """
    cols = ["name", "nwo", "cat", "targets", "stars", "lists", "listed_by"]
    rows = [[f"repo{i}", f"owner{i}/repo{i}", 0, [], 100 * i,
             len([n for n in lb.split(",") if n.strip()]), lb]
            for i, lb in enumerate(listed_by)]
    return {"cols": cols, "rows": rows, "snapshot": "2026-09-03"}


# ---- the reader: every shape `listed_by` comes in
eq("one row naming one list", b19b.source_labels(dataset("Orchestrators")), {"Orchestrators"})
eq("one row naming three lists",
   b19b.source_labels(dataset("AI Agents 2026, Agents (kyrolabs), Orchestrators")),
   {"AI Agents 2026", "Agents (kyrolabs)", "Orchestrators"})
eq("two rows naming the same list count it once",
   b19b.source_labels(dataset("Opencode", "Opencode")), {"Opencode"})
eq("overlapping rows are unioned, not summed",
   b19b.source_labels(dataset("A, B", "B, C")), {"A", "B", "C"})
# The build joins with ", " and a label may contain neither leading nor trailing space of its own, so the
# strip is what makes "A, B" and "A,B" the same two lists rather than three.
eq("the separator's padding is not part of the label",
   b19b.source_labels(dataset("A,B", " A , B ")), {"A", "B"})
eq("a row that names no list contributes nothing", b19b.source_labels(dataset("A", "")), {"A"})
eq("a trailing comma is not a twelfth list", b19b.source_labels(dataset("A, B,")), {"A", "B"})
eq("no rows imply no lists", b19b.source_labels(dataset()), set())
says("a data.json with no listed_by column says so rather than counting zero",
     raises("a data.json with no listed_by column", ValueError,
            lambda: b19b.source_labels({"cols": ["name", "nwo"], "rows": [["a", "b"]]})),
     "listed_by")

# ---- the guard, on a disagreement that does not exist on this checkout and has to be built
ELEVEN = [f"owner{i}/list{i}" for i in range(11)]
agree = dataset(*[f"List {i}" for i in range(11)])
eq("eleven lists in the rows and eleven configured is agreement",
   b19b.check_sources(agree, ELEVEN), 11)
quiet = io.StringIO()
with contextlib.redirect_stderr(quiet):
    b19b.check_sources(agree, ELEVEN)
eq("agreement says nothing at all", quiet.getvalue(), "")

# One list added to the checkout and not yet crawled: the window this ticket is about.
twelve = ELEVEN + ["owner11/list11"]
refusal = raises("a twelfth configured list refuses to render", SystemExit,
                 lambda: b19b.check_sources(agree, twelve))
says("the refusal names the number the rows imply", refusal, "built from 11 source list(s)")
says("the refusal names the number the checkout configures", refusal, "configures 12")
says("the refusal names the file whose rows it counted", refusal, "docs/data.json")
says("the refusal names the module it compared them against", refusal, "scripts/10_parse_sources.py")
says("the refusal lists the labels the rows carry", refusal, "List 0")
says("the refusal lists the sources configured now", refusal, "owner11/list11")
says("the refusal points at the rebuild that resolves it", refusal, "rebuild")
says("the refusal points at the escape hatch", refusal, "--allow-stale")
says("the refusal says which tokens are the mixed ones", refusal, "__COUNT__")

# The other direction, which is the same bug and is easy to leave out: a list removed from the checkout
# while the rows that came from it are still committed.
ten = ELEVEN[:-1]
says("a removed list refuses too, and names both sides",
     raises("a removed configured list refuses to render", SystemExit,
            lambda: b19b.check_sources(agree, ten)),
     "built from 11 source list(s); scripts/10_parse_sources.py configures 10")

# ---- the escape hatch: possible, never accidental, never quiet
loud = io.StringIO()
with contextlib.redirect_stderr(loud):
    passed = b19b.check_sources(agree, twelve, allow_stale=True)
eq("--allow-stale returns the implied count instead of exiting", passed, 11)
says("--allow-stale still says what it is doing", loud.getvalue(), "--allow-stale")
says("...on stderr, with both numbers", loud.getvalue(), "configures 12")
says("...and names the contradiction rather than reporting success",
     loud.getvalue(), "disagree")
out = io.StringIO()
with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
    b19b.check_sources(agree, twelve, allow_stale=True)
eq("the warning is on stderr, not mixed into the stage's own report", out.getvalue(), "")

# ---- the stage: `main()` end to end, three times, never against the real docs/
REAL = json.loads((ROOT / "docs" / "data.json").read_text(encoding="utf-8"))
REAL_BYTES = (ROOT / "docs" / "data.json").read_bytes()
# The scratch copy is seeded pretty-printed rather than as the committed bytes, which looks like a
# pointless difference and is the thing that makes "a refused run wrote nothing" mean anything. The stage
# writes `separators=(",", ":")`, and on this checkout the ledger dates every repo to the baseline, so a
# *completed* refresh of the committed file reproduces it byte for byte -- a comparison against the
# committed bytes would pass whether the write happened or not. Indented in, compact out: any write at all
# shows up. The stage reads it with `json.loads`, which does not care.
SEED = json.dumps(REAL, indent=1).encode("utf-8")


def run_main(argv: list[str], sources: list[str],
             out: Path | None = None) -> tuple[Path, list, io.StringIO, io.StringIO]:
    """`main()` against a scratch `docs/` holding a copy of the committed data.

    `OUT` is repointed and `reversion()` is stubbed, so this exercises the guard, the row walk, the render
    and the write in one pass without the deployable tree being reachable at all. That is not
    belt-and-braces: if the guard ever stops firing, the assertion below it fails, and the run that fails
    it must not be the run that rewrites `docs/index.html` and re-hashes the service worker.
    """
    if out is None:
        out = Path(tempfile.mkdtemp(prefix="docs_", dir=TMP))
        (out / "data.json").write_bytes(SEED)
    called: list = []

    def stub_reversion() -> None:
        # The real one shells out to `24_pwa.py`, which hashes the working tree and rewrites the *real*
        # `docs/sw.js` -- it takes no output directory and there is nothing to pass it one through. So it
        # is recorded rather than run, and it leaves behind the file `main()` goes on to stat.
        called.append("reversion")
        (out / "sw.js").write_text('const VERSION = "stub";\n', encoding="utf-8")

    keep_out, keep_src, keep_argv = b19b.OUT, b19b.b10.SOURCES, sys.argv
    keep_rev = b19b.reversion
    b19b.OUT, b19b.b10.SOURCES = out, [{"nwo": n} for n in sources]
    b19b.reversion = stub_reversion
    sys.argv = ["19b_refresh.py", *argv]
    stdout, stderr = io.StringIO(), io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            b19b.main()
    finally:
        b19b.OUT, b19b.b10.SOURCES, sys.argv = keep_out, keep_src, keep_argv
        b19b.reversion = keep_rev
    return out, called, stdout, stderr


LIVE = [s["nwo"] for s in b19b.b10.SOURCES]
# A red here is not a broken harness. It means this checkout is *inside* the window JFH-220 is about:
# `10_parse_sources.SOURCES` has moved and `docs/data.json` has not caught up, so `19b_refresh.py` will
# refuse until the next full rebuild writes the rows from a crawl. That is the designed behaviour, and this
# is the earliest place anybody would find out about it -- earlier than reaching for the stage and being
# told no, and much earlier than the deploy branch. The two numbers in the failure say which way round it
# is; if the intermediate state is deliberate, `--allow-stale` is how the stage is reached meanwhile.
eq("the checkout configures exactly the lists the committed rows were built from",
   len(LIVE), len(b19b.source_labels(REAL)))

# 1. the disagreement, through the stage rather than through the function
stale_out = Path(tempfile.mkdtemp(prefix="docs_", dir=TMP))
(stale_out / "data.json").write_bytes(SEED)
refused = raises("the stage refuses when the checkout has a list the rows do not", SystemExit,
                 lambda: run_main([], LIVE + ["owner/newly-added-list"], stale_out))
says("...and the refusal names the list that was added", refused, "owner/newly-added-list")
# The page is the artifact this ticket is about, so the assertion is that it was never written -- not
# merely that the exit code was non-zero.
true("a refused run writes no index.html", not (stale_out / "index.html").exists())
eq("a refused run leaves data.json byte-identical", (stale_out / "data.json").read_bytes(), SEED)

# 2. the same disagreement, waved through on purpose
waved, called, w_out, w_err = run_main(["--allow-stale"], LIVE + ["owner/newly-added-list"])
true("--allow-stale renders the page anyway", (waved / "index.html").exists())
says("--allow-stale warns while it does it", w_err.getvalue(), "--allow-stale")
eq("--allow-stale still re-versions the service worker", called, ["reversion"])
says("the mixed page really does carry the committed row count",
     (waved / "index.html").read_text(encoding="utf-8"), f"{len(REAL['rows']):,} agentic AI projects")

# 3. the agreeing case, which is the acceptance criterion: the stage still works
fresh, called, f_out, f_err = run_main([], LIVE)
true("the stage renders normally when the two agree", (fresh / "index.html").exists())
eq("...and says nothing on stderr", f_err.getvalue(), "")
eq("...and re-versions the worker exactly once", called, ["reversion"])
says("...and reports the source count it checked", f_out.getvalue(),
     f"rows from {len(LIVE)} source list(s)")
says("...and still reports the row count", f_out.getvalue(), f"{len(REAL['rows']):,} rows from")
fresh_data = json.loads((fresh / "data.json").read_text(encoding="utf-8"))
eq("...and rewrites data.json with the same rows it read", len(fresh_data["rows"]), len(REAL["rows"]))
eq("...and with the same source labels", b19b.source_labels(fresh_data), b19b.source_labels(REAL))
true("...and a page that is a page", (fresh / "index.html").read_text(encoding="utf-8")
     .startswith("<!doctype html>"))
true("nothing here touched the committed data.json",
     (ROOT / "docs" / "data.json").read_bytes() == REAL_BYTES)

# ---- the invariant that makes counting labels sound, on the real 1,294 rows
cols = REAL["cols"]
lb_at, n_at = cols.index("listed_by"), cols.index("lists")
eq("every committed row names at least one list",
   [r[1] for r in REAL["rows"] if not r[lb_at].strip()], [])
eq("every committed row's list count equals the labels it carries",
   [r[1] for r in REAL["rows"]
    if r[n_at] != len([n for n in r[lb_at].split(",") if n.strip()])], [])
true("the committed rows name more than one list, so the check is not trivially satisfied",
     len(b19b.source_labels(REAL)) > 1)

# ---- the hazard itself, so the docstring's claim is checked and not merely asserted
full = b19b.render(copy.deepcopy(REAL))
# The first row, not the last: rows are sorted by descending stars, so dropping the tail could remove a
# repo with no stars and leave the total unchanged, which would make the star assertion vacuous.
lean_data = copy.deepcopy(REAL)
lean_data["rows"] = lean_data["rows"][1:]
lean = b19b.render(lean_data)
stars = sum(r[4] for r in REAL["rows"])
says("__COUNT__ is the committed row count", full, f"{len(REAL['rows']):,} agentic AI projects")
says("__STARS__ is summed over the committed rows", full, f"{stars:,}")
says("dropping a row moves the rendered count", lean, f"{len(REAL['rows']) - 1:,} agentic AI projects")
true("dropping a row moves the rendered star total", f"{stars:,}" not in lean)
# ...and the other half does not move, which is the whole hazard: these words are the template's, and the
# template is the live file. Counted rather than merely found, so a render that lost two of the three
# still fails here.
eq("the prose source count does not move with the rows",
   lean.count("eleven awesome-lists"), full.count("eleven awesome-lists"))
true("the prose source count is in the page at all", full.count("eleven awesome-lists") >= 2,
     f"found {full.count('eleven awesome-lists')}")
says("the footer's own claim is a literal too", lean, "eleven source lists are credited")
says("so is the link out of it", lean, "#the-eleven-lists")
# JFH-220 was filed believing a `__LISTS__` placeholder existed and was filled from the live `SOURCES`.
# It does not exist -- the live half arrives as prose, not as substitution. If a source-count placeholder
# is ever added, the guard in `19b_refresh.py` is what has to know about it, so this fires here rather
# than being discovered on the deploy branch.
tokens = sorted(set(re.findall(r"__[A-Z][A-Z_]*__", b19b.b19.PAGE)))
eq("the template has no source-count placeholder to keep in step",
   [t for t in tokens if "LIST" in t], [])
true("the token scan found the placeholders it was looking through", "__COUNT__" in tokens)

# ---- the rows go through untouched, which is why a refresh cannot fix the disagreement itself
LEDGER = {"baseline": "2026-09-03", "window_days": 14, "repos": {}}
after, live = b19b.refresh_data(copy.deepcopy(REAL), LEDGER)
seen_at = after["cols"].index("first_seen")
eq("refresh_data adds and removes no rows", len(after["rows"]), len(REAL["rows"]))
eq("refresh_data changes no cell but first_seen",
   [(i, after["cols"][j]) for i, (a, b) in enumerate(zip(after["rows"], REAL["rows"]))
    for j, (x, y) in enumerate(zip(a, b)) if x != y and j != seen_at], [])
eq("refresh_data leaves the source labels exactly as committed",
   b19b.source_labels(after), b19b.source_labels(REAL))
eq("...so a refresh cannot change the number the guard checks",
   len(b19b.source_labels(after)), len(b19b.source_labels(REAL)))
eq("a ledger that knows no repo clears every first_seen", {r[seen_at] for r in after["rows"]}, {""})
eq("...and reports nothing inside the window", live, 0)

# ---- the source itself: two tripwires a later edit would otherwise remove silently
SRC = (SCRIPTS / "19b_refresh.py").read_text(encoding="utf-8")
main_src = SRC[SRC.index("def main()"):]
true("main() checks the source count before it writes anything",
     main_src.index("check_sources(") < main_src.index("write_text("))
true("main() offers the escape hatch on the command line", '"--allow-stale"' in main_src)
doc = b19b.__doc__
says("the docstring names the token taken from the committed rows", doc, "__COUNT__")
says("...and the other one", doc, "__STARS__")
says("...and says that side is the committed one", doc, "*committed*")
says("...and says the template is the live one", doc, "*live*")
says("...and names the escape hatch", doc, "--allow-stale")
# `19b_refresh.py`'s own imports, not the ones it inherits: it loads `19_pages`, which reaches `openpyxl`
# three modules down. Nothing new may be added *here* -- this stage is the one that has to run on a bare
# clone with nothing installed and nothing fetched.
THIRD_PARTY = ("requests", "httpx", "openpyxl", "PIL", "yaml", "dateutil", "numpy")
eq("the stage imports nothing third-party of its own",
   [m for m in THIRD_PARTY if f"\nimport {m}" in SRC or f"\nfrom {m}" in SRC], [])

print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
