"""Unit tests for `scripts/19c_live.py`, the star/push sidecar every detail page reads -- JFH-222.

`docs/repo/detail.js` used to fetch the whole of `docs/data.json` -- 162,473 bytes on the wire, eighteen
columns of 1,294 rows -- to read three values out of one row, on every one of 1,294 pages. It now fetches
`docs/live.json`, which is those three values and nothing else, at 21,791 bytes gzipped.

Everything that can go wrong with that is silent, which is why this file exists rather than a note in a
commit message. Six groups:

  the reader     -- `rows()` resolving three columns by name out of a `data.json` whose column list grows
                    from under it: `25_velocity.py` appends `d7` and `d30` *after* `19_pages.py` writes the
                    file, so a position is not a stable way to find a column. And what it says when a
                    column it needs is not there, which is the one failure that would otherwise produce a
                    perfectly valid sidecar full of nulls and 1,294 pages reading "No stars recorded".

  the document   -- `sidecar()`: the key set against the rows it was given in *both* directions, a zero
                    star count and an empty push date surviving as themselves rather than being dropped,
                    the snapshot travelling with the pair it qualifies, and the two hard stops -- a dataset
                    with no snapshot, and two rows for one repository, which a `dict` would otherwise
                    resolve by publishing one repository's numbers under the other's name.

  the bytes      -- determinism, which is what `detail-churn.mjs` exists for on the other side of this
                    change. Keys sorted by `nwo` and not left in `data.json`'s star-descending row order,
                    so the same 1,294 repositories serialise to the same bytes however the ranking moved;
                    no spaces, no `\\u` escapes, and no newline of any kind, so `core.autocrlf` has nothing
                    to rewrite on a Windows checkout.

  the stage      -- `main()` against a scratch `docs/`, twice over, and what it says when the dataset it
                    reads is not there. Nothing here writes to the real `docs/`.

  the committed  -- that `docs/live.json` in this checkout is byte-identical to what this stage produces
     pair          from `docs/data.json` in this checkout, and that its key set is exactly the set of
                   detail pages under `docs/repo/`, asserted in both directions. A page whose `nwo` is
                   missing from the sidecar renders without stars; a sidecar key with no page is dead
                   weight. Both are invisible from outside, and the acceptance criteria named them.

  the wiring     -- textual tripwires on the four files that have to agree about one filename, and on the
                    cadence the whole design rests on: `22_detail.py` runs weekly, `data.json` is rebuilt
                    daily, so the sidecar is a stage of its own that runs in *both* workflows. If it ever
                    stops appearing in `daily.yml`, the detail pages go back to showing star counts up to
                    six days behind the index -- with no error anywhere -- so that is asserted here rather
                    than trusted. So is the claim `19c_live.py`'s docstring makes about `19b_refresh.py`:
                    that the cache-free render path rewrites `data.json` without invalidating the sidecar.
                    That one is checked by running it, not by reading it.

What this cannot see: whether the numbers are true. `stars` and `pushed` come from a `gh api graphql`
crawl that stages 14+ need `cache/` for, and `cache/` is gitignored -- so the committed dataset is the only
one available offline and this harness only ever asserts that the sidecar says what that dataset says.
Nor anything in a browser: that `docs/sw.js` really caches the file offline is `pwa-check.mjs`, which has
an origin and a service worker to ask.

Run: python tests/live_test.py
"""
from __future__ import annotations

import copy
import fnmatch
import gzip
import importlib.util
import io
import json
import os
import re
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
DOCS = ROOT / "docs"


def load(name: str, filename: str):
    """`importlib`, because every stage in this pipeline is named with a leading digit and `import`
    cannot reach an identifier that starts with one. The same load the stages use on each other."""
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


b19c = load("b19c_for_test", "19c_live.py")
# For `segment()` and nothing else: the rule that turns an `nwo` into the two path segments of its detail
# page -- lowercased, a leading dot rewritten to `dot-`. Imported rather than copied because a copy is what
# makes the page-set comparison below start agreeing with itself instead of with the generator. It is the
# third reader of that rule; `detail-churn.mjs` has the second, in JavaScript, and says so.
b22 = load("b22_for_test", "22_detail.py")
b19b = load("b19b_for_live_test", "19b_refresh.py")

TMP = Path(tempfile.mkdtemp(prefix="live_test_", dir=os.environ.get("AAA_TMP") or None))

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
    """The exception and the message it carries -- for a hard stop, both are the deliverable."""
    global ok, bad
    try:
        fn()
    except kind as e:
        ok += 1
        return str(e)
    bad += 1
    print(f"FAIL {name} did not raise {kind.__name__}")
    return ""


def same(name: str, got: str, want: str) -> None:
    """`eq` for the two comparisons whose operands are 57 KB.

    Printing both sides of those is 114 KB of JSON in the log and no information: what you need is where
    they first diverge and what is on either side of it. Which repository moved, in other words, since the
    thing this guards is a sidecar that stopped matching the dataset it is derived from.
    """
    global ok, bad
    if got == want:
        ok += 1
        return
    bad += 1
    at = next((i for i in range(min(len(got), len(want))) if got[i] != want[i]), min(len(got), len(want)))
    lo = max(0, at - 60)
    print(f"FAIL {name}\n  they diverge at byte {at:,} of {len(want):,}"
          f"{'' if len(got) == len(want) else f' (got {len(got):,} bytes, want {len(want):,})'}"
          f"\n  got  ...{got[lo:at + 40]}...\n  want ...{want[lo:at + 40]}...")


def says(name: str, text: str, needle: str) -> None:
    """Clipped, because two of the haystacks here are whole workflow files and a failure that prints
    daily.yml at you is a failure you have to scroll past to read the next one."""
    global ok, bad
    if needle in text:
        ok += 1
    else:
        bad += 1
        clip = text if len(text) <= 240 else text[:240] + f"... [{len(text):,} chars]"
        print(f"FAIL {name}\n  {needle!r} is not in:\n  {clip!r}")


def dataset(triples, snapshot="2026-01-02", cols=None) -> dict:
    """A `data.json` in miniature: `(nwo, stars, pushed)`, in whatever column order is asked for.

    The default column list is deliberately not the three this stage reads. It is `name` first and
    `blurb` last, so a stage that resolved by position instead of by name gets a name where it wanted an
    `nwo` and fails visibly rather than plausibly.
    """
    cols = cols or ["name", "nwo", "stars", "blurb", "pushed"]
    rows = []
    for nwo, stars, pushed in triples:
        cell = {"name": nwo.split("/")[-1], "nwo": nwo, "stars": stars, "pushed": pushed,
                "blurb": "", "d7": "", "d30": "", "first_seen": ""}
        rows.append([cell.get(c, "") for c in cols])
    return {"cols": cols, "rows": rows, "snapshot": snapshot}


THREE = [("Owner/One", 1234, "2026-01-01"), ("owner/two", 0, "2025-12-31"), ("Z/three", 7, "")]

# ---- the reader: three columns found by name, in a column list that grows from under it ---------------
eq("rows() hands back (nwo, stars, pushed) for every row",
   b19c.rows(dataset(THREE)), [("Owner/One", 1234, "2026-01-01"), ("owner/two", 0, "2025-12-31"),
                               ("Z/three", 7, "")])
eq("...resolved by name, so a different column order is the same answer",
   b19c.rows(dataset(THREE, cols=["pushed", "stars", "blurb", "nwo", "name"])),
   b19c.rows(dataset(THREE)))
# The real hazard, not a hypothetical one: `25_velocity.py` appends `d7` and `d30` to `cols` after
# `19_pages.py` has written the file, in both workflows, and this stage runs between the two.
eq("...and columns appended after the file was written do not move the three that matter",
   b19c.rows(dataset(THREE, cols=["name", "nwo", "stars", "blurb", "pushed", "d7", "d30"])),
   b19c.rows(dataset(THREE)))
eq("an empty dataset reads as no rows rather than as an error", b19c.rows(dataset([])), [])

no_stars = dataset(THREE, cols=["name", "nwo", "blurb", "pushed"])
msg = raises("a dataset with no stars column is a hard stop", SystemExit,
             lambda: b19c.rows(no_stars))
says("...and the refusal names the column that is missing", msg, "stars")
says("...and prints the columns it did find, so the cause is in the message", msg, "nwo, blurb, pushed")
says("...and says it will not invent them", msg, "cannot invent")
msg = raises("a dataset with none of the three is a hard stop", SystemExit,
             lambda: b19c.rows({"cols": ["blurb"], "rows": [], "snapshot": "x"}))
for col in ("nwo", "stars", "pushed"):
    says(f"...and the refusal names {col}", msg, col)

# ---- the document ------------------------------------------------------------------------------------
doc = b19c.sidecar(dataset(THREE))
eq("the document is exactly a snapshot and a repos map", sorted(doc), ["repos", "snapshot"])
eq("the snapshot travels with the pair it qualifies", doc["snapshot"], "2026-01-02")
# Both directions, which is acceptance criterion 5 in miniature: a row with no key renders a page without
# stars, and a key with no row is dead weight. Set equality alone would pass on a duplicate, so the count
# is asserted beside it.
eq("every row given has a key", set(doc["repos"]), {n for n, _, _ in THREE})
eq("...and there are no keys beyond them", len(doc["repos"]), len(THREE))
eq("the value is the pair, in that order", doc["repos"]["Owner/One"], [1234, "2026-01-01"])
# Not dropped and not blanked. `!row[0]` in the page is what turns 0 into "No stars recorded", so a 0 that
# arrived as "" or as null would render the same and mean something different.
eq("a zero star count survives as the integer zero", doc["repos"]["owner/two"][0], 0)
eq("...as an int, not as a string", type(doc["repos"]["owner/two"][0]).__name__, "int")
eq("an empty push date survives as the empty string", doc["repos"]["Z/three"][1], "")
eq("...and its star count is still there beside it", doc["repos"]["Z/three"][0], 7)
eq("keys are sorted, so the file does not depend on how the rows were ranked",
   list(doc["repos"]), sorted(doc["repos"]))

msg = raises("a dataset with no snapshot is a hard stop", SystemExit,
             lambda: b19c.sidecar({"cols": ["nwo", "stars", "pushed"], "rows": []}))
says("...and the refusal says why the snapshot is not optional", msg, "qualifier")
says("...and what publishing without it would claim", msg, "live")

dupe = dataset([("a/b", 1, "2026-01-01"), ("a/b", 2, "2026-01-02")])
msg = raises("two rows for one repository is a hard stop", SystemExit,
             lambda: b19c.sidecar(dupe))
says("...and the refusal names the repository", msg, "'a/b'")
says("...and says what the silent version of it would have published", msg, "replace")

# ---- the bytes: determinism, which is the property detail-churn.mjs guards on the other side ----------
body = b19c.dumps(doc)
true("the serialisation has no space after a separator", ", " not in body and '": ' not in body, body[:80])
true("...no newline of any kind, so autocrlf has nothing to rewrite on Windows",
     "\n" not in body and "\r" not in body)
eq("...and it round-trips", json.loads(body), doc)
eq("dumps is a pure function of its argument", b19c.dumps(doc), b19c.dumps(b19c.sidecar(dataset(THREE))))
uni = b19c.dumps(b19c.sidecar(dataset([("café/résumé", 1, "2026-01-01")])))
true("non-ASCII is written as itself rather than escaped", "\\u" not in uni and "café" in uni, uni)

# The exact perturbation `detail-churn.mjs` applies for its run C: every star count moved, every push date
# moved, the snapshot moved. There the answer must be "nothing changed"; here it must be "only the values
# changed", because this file is the one that carries them -- and the *keys* must still land in the same
# places, or a day of ranking churn is a 57 KB delta instead of a few hundred bytes.
churned = [(n, s + 91_337, "2099-12-30" if p else "") for n, s, p in THREE]
cdoc = b19c.sidecar(dataset(churned, snapshot="2099-12-31"))
eq("a day on which every number moved leaves the key sequence untouched",
   list(cdoc["repos"]), list(doc["repos"]))
true("...and the values are what moved", cdoc["repos"]["Owner/One"] != doc["repos"]["Owner/One"])
eq("the row order in data.json does not reach the bytes",
   b19c.dumps(b19c.sidecar(dataset(list(reversed(THREE))))), body)
eq("...nor does the column order",
   b19c.dumps(b19c.sidecar(dataset(THREE, cols=["pushed", "nwo", "d30", "stars", "name"]))), body)

# ---- the stage, against a scratch docs/ --------------------------------------------------------------
scratch = TMP / "docs"
scratch.mkdir(parents=True)
(scratch / "data.json").write_text(json.dumps(dataset(THREE)), encoding="utf-8")


def run_stage(*argv) -> str:
    out = io.StringIO()
    argv_was, sys.argv = sys.argv, ["19c_live.py", *argv]
    try:
        with redirect_stdout(out):
            b19c.main()
    finally:
        sys.argv = argv_was
    return out.getvalue()


log = run_stage("--out", str(scratch))
dest = scratch / "live.json"
true("main() writes the sidecar into --out", dest.exists(), str(dest))
eq("...with exactly the bytes dumps() produces", dest.read_bytes().decode("utf-8"), body)
true("...and nothing else", sorted(p.name for p in scratch.iterdir()) == ["data.json", "live.json"],
     str(sorted(p.name for p in scratch.iterdir())))
raw_first = dest.read_bytes()
true("...with no CR and no LF in the file on disk",
     b"\r" not in raw_first and b"\n" not in raw_first)
run_stage("--out", str(scratch))
eq("running it twice writes identical bytes", dest.read_bytes(), raw_first)
says("the log reports the wire size, not only the raw one", log, "gzipped")
says("...and the ratio the stage exists for", log, "fewer bytes")
says("...and that the service worker does not precache it", log, "not precached")

other = TMP / "other.json"
other.write_text(json.dumps(dataset([("x/y", 5, "2026-02-02")], snapshot="2026-02-03")), encoding="utf-8")
run_stage("--out", str(scratch), "--data", str(other))
eq("--data reads that dataset instead of DIR/data.json",
   json.loads(dest.read_text(encoding="utf-8")),
   {"snapshot": "2026-02-03", "repos": {"x/y": [5, "2026-02-02"]}})
msg = raises("a --data that is not there is a hard stop", SystemExit,
             lambda: run_stage("--out", str(scratch), "--data", str(TMP / "nope.json")))
says("...and the refusal names the stage that writes it", msg, "19_pages.py")
# Restored, so the assertions below read the committed pair rather than this fixture. Nothing above ever
# pointed --out at the real docs/, and this is the line that says so out loud.
true("nothing in this file has written to the real docs/",
     json.loads((DOCS / "live.json").read_text(encoding="utf-8"))["repos"] != {"x/y": [5, "2026-02-02"]})

# ---- the committed pair: no drift between docs/data.json and docs/live.json --------------------------
REAL = json.loads((DOCS / "data.json").read_text(encoding="utf-8"))
committed = (DOCS / "live.json").read_bytes()
true("docs/live.json is committed", committed != b"")
# The whole of acceptance criterion 2, and stronger than the "same in-memory rows" it asked for: it is a
# statement about the two files that are actually served rather than about how they were made.
same("docs/live.json is byte-identical to a fresh derivation from docs/data.json",
     committed.decode("utf-8"), b19c.dumps(b19c.sidecar(copy.deepcopy(REAL))))
LIVE = json.loads(committed.decode("utf-8"))
eq("...so its snapshot is the dataset's snapshot", LIVE["snapshot"], REAL["snapshot"])
true("...and it has no line endings for autocrlf to rewrite",
     b"\r" not in committed and b"\n" not in committed)
eq("...and its keys are sorted", list(LIVE["repos"]), sorted(LIVE["repos"]))

ix = {c: i for i, c in enumerate(REAL["cols"])}
real_nwo = [r[ix["nwo"]] for r in REAL["rows"]]
eq("every row in docs/data.json has a key in docs/live.json", [n for n in real_nwo if n not in LIVE["repos"]], [])
eq("...and every key in docs/live.json is a row in docs/data.json",
   [n for n in LIVE["repos"] if n not in set(real_nwo)], [])
eq("...and there are exactly as many of one as of the other", len(LIVE["repos"]), len(REAL["rows"]))
true("...and that is 1,294-ish rather than nothing, so none of this passed on two empty sets",
     len(LIVE["repos"]) > 1000, str(len(LIVE["repos"])))
# `.get` and a two-element default rather than `LIVE["repos"][n]`, because the case this whole section is
# here to catch is a key that is not there -- and a harness that raises KeyError on it stops before it can
# report the twelve assertions below.
want_pair = {n: [r[ix["stars"]], r[ix["pushed"]]] for n, r in zip(real_nwo, REAL["rows"])}
got_pair = {n: LIVE["repos"].get(n) or [None, None] for n in real_nwo}
eq("the star count in the sidecar is the star count in the dataset, on every row",
   [n for n in real_nwo if got_pair[n][0] != want_pair[n][0]][:5], [])
eq("...and so is the push date",
   [n for n in real_nwo if got_pair[n][1] != want_pair[n][1]][:5], [])

# ---- the key set against the detail pages, in both directions (acceptance criterion 5) ---------------
#
# `segment()` is imported from `22_detail.py` rather than reimplemented, because the two have to agree
# about one repository in 1,294 -- `zircote/.claude`, whose page is `dot-claude` -- and a private copy of
# that rule is a copy that will one day agree with itself and not with the generator.
def page_parts(nwo: str) -> tuple[str, str]:
    owner, name = nwo.split("/", 1)
    return b22.segment(owner.lower()), b22.segment(name.lower())


pages = {p.parent.relative_to(DOCS / "repo").as_posix()
         for p in (DOCS / "repo").rglob("index.html") if p.parent != DOCS / "repo"}
keyed = {"/".join(page_parts(n)) for n in LIVE["repos"]}
true("there are detail pages on disk to compare against", len(pages) > 1000, str(len(pages)))
eq("every sidecar key has a detail page -- a key with no page is dead weight",
   sorted(keyed - pages)[:5], [])
eq("every detail page has a sidecar key -- a page with no key renders without stars",
   sorted(pages - keyed)[:5], [])
eq("...and the two sets are the same size, so neither comparison hid a collision",
   len(keyed), len(pages))
eq("the slug rule is the generator's own, dots and all",
   page_parts("zircote/.Claude"), ("zircote", "dot-claude"))

# ---- the wiring: four files that have to agree about one filename ------------------------------------
NAME = b19c.NAME
eq("the stage publishes the filename the rest of this section is about", NAME, "live.json")
DETAIL_JS = (DOCS / "repo" / "detail.js").read_text(encoding="utf-8")
says("the committed detail.js fetches the sidecar", DETAIL_JS, f'fetch(root + "{NAME}")')
says("...and reads it as a map keyed by nwo", DETAIL_JS, "d.repos[nwo]")
says("...and still renders the snapshot that qualifies the two figures", DETAIL_JS, "d.snapshot")
says("...and declines a shape that is not the pair", DETAIL_JS, "Array.isArray(row)")
# The comments in that file still discuss data.json, and should -- they are the record of what this
# replaced. So the assertion is about the code, with the block comments taken out first.
code = re.sub(r"/\*.*?\*/", "", DETAIL_JS, flags=re.S)
true("...and the code no longer names data.json at all", "data.json" not in code)
true("...which is not vacuous, because the same stripped code does name the sidecar", NAME in code)
# `b22.JS` is the single source of that file; Python universal-newlines both sides of this comparison, so
# it is a comparison of content and not of line endings.
same("the committed detail.js is the one 22_detail.py would write, so docs/ was regenerated",
     DETAIL_JS, b22.JS)

SW = (DOCS / "sw.js").read_text(encoding="utf-8")
says("the committed service worker names the sidecar in its data list", SW, f'"/{NAME}"')
says("...and still names data.json beside it, so the change was additive", SW, '"/data.json"')
says("...and routes that whole list through the cached-data handler", SW,
     "DATA_FILES.some((name) => url.pathname.endsWith(name))")
b24 = load("b24_for_test", "24_pwa.py")
eq("the worker's list has one definition, in 24_pwa.py", b24.DATA_FILES, ["data.json", "live.json"])
eq("...and the served worker is what that definition produces",
   re.search(r"const DATA_FILES = (\[[^\]]*\]);", SW).group(1),
   json.dumps(["/" + f for f in b24.DATA_FILES]))
true("the sidecar is not precached, so no reader pays for it who never opens a detail page",
     NAME not in b24.PRECACHE, str(b24.PRECACHE))

# ---- the cadence the design rests on ----------------------------------------------------------------
#
# This is the part that is worth more than all the string matching above it. The sidecar carries the two
# numbers that move every night. `22_detail.py` runs weekly, by an explicit decision daily.yml spells out
# at length, because its pages are byte-stable against a day of star drift. So the sidecar cannot be
# emitted from that stage without pegging 1,294 pages' star counts up to six days behind the index -- and
# the thing that keeps them in step is nothing more than this stage appearing in both workflows.
DAILY = (ROOT / ".github" / "workflows" / "daily.yml").read_text(encoding="utf-8")
WEEKLY = (ROOT / ".github" / "workflows" / "weekly.yml").read_text(encoding="utf-8")
STAGE = "python scripts/19c_live.py"
for label, wf in (("daily.yml", DAILY), ("weekly.yml", WEEKLY)):
    says(f"{label} runs the sidecar stage", wf, STAGE)
    if STAGE not in wf:
        continue
    # After *both* writers of data.json, not just the first: 19_pages rewrites the file and 25_velocity
    # patches columns into it afterwards, so a sidecar derived between them is a projection of a copy that
    # never shipped. The three fields here survive that patch either way, which is exactly why getting
    # this wrong would be invisible.
    for writer in ("19_pages.py", "25_velocity.py"):
        true(f"...{label} runs it after {writer}, which writes data.json",
             wf.index(f"python scripts/{writer}") < wf.index(STAGE),
             f"19c_live.py is at {wf.index(STAGE)}, {writer} at {wf.index(f'python scripts/{writer}')}")
# The premise. If 22_detail.py ever moves into the daily job the argument above stops applying, and this
# assertion is where that gets noticed rather than in a comment nobody re-reads.
true("22_detail.py is weekly-only, which is why the sidecar is not its output",
     "python scripts/22_detail.py" in WEEKLY and "python scripts/22_detail.py" not in DAILY)


def case_globs(text: str) -> list[str]:
    """Every glob in a shell `case` pattern list in a workflow file.

    Both workflows assert that each tracked file under `docs/` was rewritten by the build, and both sort
    the ones that were not by matching the path against a list like
    `docs/topic/*|docs/pages.css|docs/repo/*)`. A path that matches is excused; a path that does not fails
    the job by name. So `docs/live.json` matching one of those patterns would turn a frozen sidecar from a
    red build into a file that silently stops being rebuilt -- which is the entire failure mode of this
    ticket, one level up.
    """
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s.endswith(")") or "(" in s or s.startswith("#") or "/" not in s:
            continue
        parts = s[:-1].split("|")
        if all(re.fullmatch(r"[A-Za-z0-9_.*/\[\]-]+", p) for p in parts):
            out.extend(parts)
    return out


for label, wf in (("daily.yml", DAILY), ("weekly.yml", WEEKLY)):
    globs = case_globs(wf)
    # Not vacuous: the extractor has to actually find the patterns before "nothing matched" means anything.
    true(f"{label}'s skip patterns were found at all", any(g.startswith("docs/repo") for g in globs),
         str(globs))
    # A facet page, which both workflows excuse -- daily as weekly-only work, weekly as prunable. Not
    # `docs/repo/detail.js`: weekly's pattern is `docs/repo/*/*` and not `docs/repo/*` on purpose, because
    # detail.js is a fixed path and the per-repo directories are not, and it says so in a comment there.
    true("...and they do match what they are meant to excuse",
         any(fnmatch.fnmatch("docs/topic/agents/index.html", g) for g in globs), str(globs))
    eq(f"...and docs/{NAME} matches none of them, so a build that stopped writing it goes red",
       [g for g in globs if fnmatch.fnmatch(f"docs/{NAME}", g)], [])

# ---- and the one claim in 19c_live.py's docstring that is checkable by running something -------------
#
# `19b_refresh.py` rewrites docs/data.json without running this stage. The docstring says that is safe
# because it only ever changes `first_seen`, `window_days`, `baseline` and `schema_version`, and refuses to
# touch a star count, a push date or the snapshot. Asserted by doing it: a refresh over the committed data
# must leave the sidecar byte-identical.
refreshed, _live = b19b.refresh_data(copy.deepcopy(REAL),
                                     {"baseline": "2000-01-01", "repos": {}, "sources": {}})
same("a cache-free refresh of data.json does not invalidate the sidecar",
     b19c.dumps(b19c.sidecar(refreshed)), committed.decode("utf-8"))
eq("...even though it did rewrite the dataset", "first_seen" in refreshed["cols"], True)

# ---- the source itself ------------------------------------------------------------------------------
SRC = (SCRIPTS / "19c_live.py").read_text(encoding="utf-8")
THIRD_PARTY = ("requests", "httpx", "openpyxl", "PIL", "yaml", "dateutil", "numpy")
eq("the stage imports nothing third-party",
   [m for m in THIRD_PARTY if f"\nimport {m}" in SRC or f"\nfrom {m}" in SRC], [])
true("...and nothing from the pipeline either, so it runs on a bare clone",
     "importlib" not in SRC, "it loads another stage, which this stage has no reason to do")
says("the docstring says which figure to quote", b19c.__doc__, "Content-Encoding: gzip")
says("...and why this is not part of 22_detail.py", b19c.__doc__, "weekly")
says("...and names the ticket", b19c.__doc__, "JFH-222")

# The win, re-measured rather than quoted. A ratio in a docstring is a claim that goes stale; this is the
# same arithmetic against whatever the two files hold today.
wire_live = len(gzip.compress(committed, 9))
wire_data = len(gzip.compress((DOCS / "data.json").read_bytes().replace(b"\r\n", b"\n"), 9))
true("the sidecar is still several times smaller than data.json on the wire",
     wire_data / wire_live > 5, f"{wire_data:,} / {wire_live:,} = {wire_data / wire_live:.2f}x")
print(f"\ndocs/data.json {wire_data:,} B gzipped · docs/{NAME} {wire_live:,} B gzipped · "
      f"{wire_data / wire_live:.1f}x, over {len(LIVE['repos']):,} detail pages")

print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
