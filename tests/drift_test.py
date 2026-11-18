"""Upstream drift, `scripts/drift.py`, and every stage it changes: the build keeps publishing when a list
changes under it, and every decision that forces is visible.

Until this existed one curator's renamed heading stopped the daily build: libukai translating eight
headings to English held the site for over two weeks. So the two properties under test pull against each
other, and both are asserted. A provisional build (`AAA_PROVISIONAL=1`, which only the workflows set)
must not stop on drift; and nothing may be re-filed for good, silently, or outside such a build -- a strict
run, which is every local run and every test, stops exactly as it always did.

Nothing here touches the network or the shared `cache/`: every path drift.py and pull_sources.py write is
repointed into `build-tmp/drift-test`, GitHub is a fake, and the env var is set and cleared per case.

Eight groups:

  the evidence   -- `lineage()`: a heading renamed with its entries is a membership rename, one renamed with
                    new entries in a list of the same shape is a positional one, a reshuffle below half is
                    neither, and a section whose name survived is never reported. The libukai translation of
                    2026-10 is the reference fixture. `record_moves` accumulates across pulls.
  placing        -- `place()`: membership, a two-hop chain, position, a close name (orphans first), the
                    list's modal category by rows and then by keys, and no records at all on a clean day.
  the palette    -- a ninth hue folds into the last bucket of a curated map, newcomers fold before mapped
                    sections, a list with no map gets a whole one proposed, a rename inherits its bucket,
                    and slots are counted the way `16_build_all.group_styles` hands them out.
  honouring      -- `taxonomy.category_of` and `buckets.bucket_map` use the placements under the env var and
                    ignore the same file without it; the curated map wins where both name a section.
  the parse      -- `10_parse_sources.unmapped`: strict exits 1 and writes no placements; provisional returns,
                    writes them, annotates each one, fills the step summary and the proposal; a clean run
                    writes an empty proposal and deletes a stale placements file.
  the pull       -- `pull_sources.pull_one` against a fake GitHub: a translation records its lineage, a copy
                    that parses to under a quarter of the last is refused and yesterday's bytes restored,
                    `--force` takes it, and a renamed list repo is fetched under its new name and reported.
  the proposal   -- `apply_drift_proposal.py` writes each key at the end of its own list's block, after a
                    value on its own line, into the named bucket, or as a whole new map; twice is once.
  guards         -- the fetch stops when most failures are not about the repo and carries on when they are
                    404s; both workflows set the env var for the whole job; the Markdown stage unescapes an
                    upstream `\\|` in prose.

Run: python tests/drift_test.py
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import sys
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
import apply_drift_proposal as apply  # noqa: E402
import buckets  # noqa: E402
import drift  # noqa: E402
import taxonomy as tax  # noqa: E402

ok = bad = 0


def true(name: str, cond, detail: str = "") -> None:
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}" + (f"\n  {detail}" if detail else ""))


def eq(name: str, got, want) -> None:
    true(name, got == want, f"got  {got!r}\n  want {want!r}")


def load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def quiet(fn, *a, **k):
    out, err = StringIO(), StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        result = fn(*a, **k)
    return result, out.getvalue(), err.getvalue()


def section(title: str) -> None:
    print(f"\n── {title} {'─' * max(0, 96 - len(title))}")


drift.utf8_console()

# Every path the module writes, into scratch. Under ROOT so the stages' relative_to(ROOT) messages work.
TMP = ROOT / "build-tmp" / "drift-test"
shutil.rmtree(TMP, ignore_errors=True)
TMP.mkdir(parents=True)
drift.PLACEMENTS, drift.MOVES = TMP / "provisional.json", TMP / "section-moves.json"
drift.PROPOSAL, drift.PROPOSAL_MD, drift.PULL_REPORT = (TMP / "drift-proposal.json",
                                                        TMP / "drift-proposal.md", TMP / "pull-report.json")
SAVED_ENV = {k: os.environ.get(k) for k in (drift.ENV, "GITHUB_ACTIONS", "GITHUB_STEP_SUMMARY")}


def env(**kv) -> None:
    for k, v in kv.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v
    drift.reset()


env(AAA_PROVISIONAL=None, GITHUB_ACTIONS=None, GITHUB_STEP_SUMMARY=None)

# The libukai list as it was, and as it became on 2026-10-25: the same eight shelves in the same order,
# translated, with two entries added and one dropped. The keys stand in for entry URLs.
CN = ["官方文档", "图文教程", "视频教程", "编程开发", "内容创作", "产品使用", "其他类型", "测试与评测"]
EN = ["Official Documentation", "Written Tutorials", "Video Tutorials", "Programming & Development",
      "Content Creation", "Product Usage", "Other Types", "Testing and Evaluation"]
CAT = ["Docs, Learning & Lists", "Docs, Learning & Lists", "Docs, Learning & Lists", "Agent Skills",
       "Agent Skills", "Agent Skills", "Agent Skills", "Observability & Evals"]
SIZES = [3, 2, 1, 6, 7, 5, 4, 5]
old_pairs = [(f"e{i}-{j}", CN[i]) for i, n in enumerate(SIZES) for j in range(n)]
new_pairs = [(k, EN[CN.index(s)]) for k, s in old_pairs]
# Video Tutorials gains two new entries (so only a third of it is old: position, not membership).
new_pairs += [("v-new-1", EN[2]), ("v-new-2", EN[2])]
SECTIONS_CN = {("skills_libukai", s): c for s, c in zip(CN, CAT)}


def rows_of(pairs, source="skills_libukai"):
    return [{"source": source, "category": s} for _, s in pairs]


# ── the evidence ──────────────────────────────────────────────────────────────────────────────────
section("the evidence")
lin = drift.lineage(old_pairs, new_pairs)
eq("every translated heading is traced to the one it replaced", {k: v["from"] for k, v in lin.items()},
   dict(zip(EN, CN)))
eq("...by its entries where most of them carried over",
   {k for k, v in lin.items() if v["basis"] == "membership"}, set(EN) - {"Video Tutorials"})
eq("...and by its slot where they did not (1 of 3 old)", lin["Video Tutorials"],
   {"from": "视频教程", "basis": "position", "slot": 3, "of": 8})
eq("membership evidence counts what it saw", (lin["Content Creation"]["shared"], lin["Content Creation"]["of"]),
   (7, 7))

eq("a section whose name survived is never reported, whatever moved into it",
   drift.lineage([("a", "X"), ("b", "Y")], [("a", "X"), ("b", "X")]), {})
eq("a reshuffle below half is not a rename, and a changed shape has no slot to go by",
   drift.lineage([("a", "X"), ("b", "Y"), ("c", "Z")], [("a", "N"), ("x", "N"), ("y", "N"), ("b", "Y")]), {})
eq("a brand-new shelf in a list that grew has no evidence at all",
   drift.lineage([("a", "X")], [("a", "X"), ("n", "Jobs")]), {})

moves_path = TMP / "moves-a.json"
drift.record_moves("skills_libukai", "sha1", {k: lin[k] for k in EN[:4]}, moves_path)
drift.record_moves("other", "sha2", {"B": {"from": "A", "basis": "membership", "shared": 1, "of": 1}},
                   moves_path)
drift.record_moves("skills_libukai", "sha3", {k: lin[k] for k in EN[4:]}, moves_path)
got = drift.load_moves(moves_path)
eq("record_moves accumulates: a later pull adds to what earlier ones saw",
   (sorted(got["skills_libukai"]), sorted(got["other"])), (sorted(EN), ["B"]))
eq("...and stamps each observation with the commit it was seen at",
   (got["skills_libukai"][EN[0]]["sha"], got["skills_libukai"][EN[7]]["sha"]), ("sha1", "sha3"))
drift.record_moves("x", "sha4", {}, TMP / "never.json")
true("...and writes nothing when there is nothing to record", not (TMP / "never.json").exists())
eq("an unreadable ledger is an empty one", drift.load_moves(TMP / "nope.json"), {})

# ── placing ───────────────────────────────────────────────────────────────────────────────────────
section("placing")
moves = {"skills_libukai": lin}
recs = drift.place(rows_of(new_pairs), SECTIONS_CN, {}, moves, tax.CATEGORIES)
eq("libukai: each English heading takes its Chinese predecessor's category -- PR #105, derived",
   {r["section"]: r["category"] for r in recs}, dict(zip(EN, CAT)))
eq("...with the basis said", {r["section"]: r["basis"] for r in recs}["Video Tutorials"], "position")
eq("...and rows counted", {r["section"]: r["rows"] for r in recs}["Video Tutorials"], 3)
eq("...and the line to paste, in the file's own style",
   recs[0]["taxonomy_line"], '    ("skills_libukai", "Official Documentation"): "Docs, Learning & Lists",')
true("...and a sentence of evidence for each", all(drift.describe(r) for r in recs))

eq("a clean list needs no records", drift.place(rows_of(old_pairs), SECTIONS_CN, {}, {}, tax.CATEGORIES), [])

two_hop = {"s": {"C": {"from": "B", "basis": "membership", "shared": 2, "of": 2},
                 "B": {"from": "A", "basis": "position", "slot": 1, "of": 1}}}
r = drift.place([{"source": "s", "category": "C"}], {("s", "A"): "MCP Servers"}, {}, two_hop, tax.CATEGORIES)[0]
eq("a rename of a rename follows the chain to the mapped end", (r["category"], r["evidence"]["path"]),
   ("MCP Servers", ["C", "B", "A"]))
loop = {"s": {"C": {"from": "B", "basis": "position"}, "B": {"from": "C", "basis": "position"}}}
r = drift.place([{"source": "s", "category": "C"}, {"source": "s", "category": "D"}],
                {("s", "D"): "MCP Servers"}, {}, loop, tax.CATEGORIES)[0]
eq("...and a chain that loops is no evidence (falls back to the mode)", r["basis"], "modal")

secs = {("s", "Testing and Evaluation"): "Observability & Evals", ("s", "Tools"): "Frameworks & SDKs",
        ("s", "Servers"): "MCP Servers"}
rows = [{"source": "s", "category": c} for c in ["Testing & Evaluation", "Tools", "Servers", "Servers"]]
r = drift.place(rows, secs, {}, {}, tax.CATEGORIES)[0]
eq("a close name to a section the list no longer produces carries its category",
   (r["basis"], r["category"], r["evidence"]["was"]), ("similar", "Observability & Evals",
                                                        "Testing and Evaluation"))
r = drift.place([{"source": "s", "category": c} for c in ["Tool", "Tools", "Servers"]],
                {("s", "Tools"): "Frameworks & SDKs", ("s", "Servers"): "MCP Servers"}, {}, {},
                tax.CATEGORIES)[0]
eq("...and failing an orphan, a close name to a current sibling", (r["basis"], r["category"]),
   ("similar", "Frameworks & SDKs"))
r = drift.place([{"source": "s", "category": c} for c in ["Jobs", "Docs", "Servers", "Servers"]],
                {("s", "Docs"): "Docs, Learning & Lists", ("s", "Servers"): "MCP Servers"}, {}, {},
                tax.CATEGORIES)[0]
eq("'Jobs' is not 'Docs': short words do not match each other", r["basis"], "modal")
eq("...and with nothing to go on it takes the list's modal category by rows",
   (r["category"], r["evidence"]["basis_of"], r["evidence"]["votes"]), ("MCP Servers", "rows", 2))
r = drift.place([{"source": "s", "category": "Z"}],
                {("s", "Old1"): "Coding Agents", ("s", "Old2"): "MCP Servers", ("s", "Old3"): "MCP Servers"},
                {}, {}, tax.CATEGORIES)[0]
eq("a list with no mapped row today falls back to the categories its keys name",
   (r["category"], r["evidence"]["basis_of"]), ("MCP Servers", "keys"))
r = drift.place([{"source": "s", "category": "A"}, {"source": "s", "category": "B"}],
                {("s", "A"): "MCP Servers", ("s", "B"): "Coding Agents", ("s", "Q"): "x"}, {}, {}, tax.CATEGORIES)
eq("a tie goes to the earlier category, as in taxonomy.by_repo",
   drift._modal("s", __import__("collections").Counter({"A": 1, "B": 1}),
                {("s", "A"): "MCP Servers", ("s", "B"): "Coding Agents"}, tax.CATEGORIES,
                __import__("collections").Counter())[0], "Coding Agents")

# The published pages: yesterday's membership, committed, for drift the cache ledger never saw. This is
# the case the first trial (run 44348469978) hit: the restored cache already held the translated README.
pages = TMP / "mega-lists"
pages.mkdir()
(pages / "agent-skills-libukai.md").write_text(
    "# Agent Skills (libukai)\n\nCurated by **[libukai/awesome-agent-skills](https://github.com/libukai/"
    "awesome-agent-skills)** — all credit.\n\n## Contents\n\n- [编程开发](#编程开发) (2)\n\n"
    "## 编程开发\n\n- **[a](https://github.com/x/A)** — one\n  <sub>★ 1</sub>\n"
    "- **[b](https://github.com/x/b/)** — two\n\n"
    "## Docs &amp; Videos\n\n- **[c](https://example.com/c)** — three\n", encoding="utf-8")
(pages / "agent-skills-libukai-2.md").write_text(
    "# Agent Skills (libukai)\n\nPage **2** of 2.\n\nCurated by **[libukai/awesome-agent-skills](https://x)** — \n\n"
    "## 测试与评测\n\n- **[d](https://github.com/x/d)** — four\n", encoding="utf-8")
(pages / "other.md").write_text("Curated by **[someone/else](https://x)**\n\n## 编程开发\n\n"
                                "- **[z](https://github.com/x/z)** — not this list\n", encoding="utf-8")
uk = b10_url_key = lambda u: u.strip().lower().rstrip("/")  # noqa: E731  -- 10_parse_sources.url_key
pp = drift.published_pairs("libukai/awesome-agent-skills", uk, pages)
eq("the published pages are read back into (entry, section): every part of the list, no other list",
   pp, [("https://github.com/x/a", "编程开发"), ("https://github.com/x/b", "编程开发"),
        ("https://example.com/c", "Docs & Videos"), ("https://github.com/x/d", "测试与评测")])
eq("...and a list whose page title differs from its SOURCES title (a workbook sheet's) is still found by "
   "its unique repository", drift.published_pairs("libukai/awesome-agent-skills", uk, pages, "AI Skills (CN)"),
   pp)

# Two lists crediting one repository -- the GitHub scout and the GitLab intake both name this one.
shared = TMP / "mega-shared"
shared.mkdir()
for fname, title, url in (("scouted-on-github.md", "Scouted on GitHub", "https://github.com/s/one"),
                          ("scouted-on-github-2.md", "Scouted on GitHub", "https://github.com/s/two"),
                          ("scouted-on-gitlab.md", "Scouted on GitLab", "https://gitlab.com/g/one")):
    (shared / fname).write_text(f"# {title}\n\nCurated by **[crazy54/awesome-agentic-atlas](https://x)**\n\n"
                                f"## MCP Servers\n\n- **[x]({url})** — y\n", encoding="utf-8")
eq("a shared repository is told apart by the page title: the scout gets both its parts and nothing else",
   [k for k, _ in drift.published_pairs("crazy54/awesome-agentic-atlas", uk, shared, "Scouted on GitHub")],
   ["https://github.com/s/one", "https://github.com/s/two"])
eq("...and the GitLab intake gets only its own",
   [k for k, _ in drift.published_pairs("crazy54/awesome-agentic-atlas", uk, shared, "Scouted on GitLab")],
   ["https://gitlab.com/g/one"])
eq("...and a shared repository with no matching title gives no evidence rather than another list's",
   drift.published_pairs("crazy54/awesome-agentic-atlas", uk, shared, "Something Else"), [])
cur = [{"source": "skills_libukai", "category": s, "url": u} for s, u in
       (("Programming & Development", "https://github.com/x/a"),
        ("Programming & Development", "https://github.com/x/B"),
        ("Testing and Evaluation", "https://github.com/x/d"), ("Docs and Videos", "https://example.com/c"))]
psecs = {("skills_libukai", "编程开发"): "Agent Skills", ("skills_libukai", "测试与评测"): "Observability & Evals",
         ("skills_libukai", "Docs & Videos"): "Docs, Learning & Lists"}
SRCS = {"skills_libukai": ("libukai/awesome-agent-skills", "Agent Skills (libukai)")}
pm = drift.published_moves(cur, SRCS, psecs, {}, uk, pages)
eq("with no ledger, the pages supply membership evidence for each renamed section",
   {k: (v["from"], v["via"]) for k, v in pm["skills_libukai"].items()},
   {"Programming & Development": ("编程开发", "published"), "Testing and Evaluation": ("测试与评测", "published"),
    "Docs and Videos": ("Docs & Videos", "published")})
ledger = {"skills_libukai": {"Testing and Evaluation": {"from": "other", "basis": "position"}}}
pm2 = drift.published_moves(cur, SRCS, psecs, ledger, uk, pages)
eq("...but the ledger's own observation wins where it has one", pm2["skills_libukai"]["Testing and Evaluation"],
   {"from": "other", "basis": "position"})
eq("...and the ledger passed in is not modified", list(ledger["skills_libukai"]), ["Testing and Evaluation"])
eq("...and a list with nothing unmapped is not read at all",
   drift.published_moves([dict(cur[0], category="编程开发")], SRCS, psecs, {}, uk, pages), {})
r = drift.place(cur, psecs, {}, pm, tax.CATEGORIES)
true("...and describe() says the evidence came from the published page",
     "last published page" in drift.describe(next(x for x in r if x["section"] == "Docs and Videos")))

# The one left over: libukai's Video Tutorials, which neither membership nor (in the trial) slots could see.
no_video = {"skills_libukai": {k: v for k, v in lin.items() if k != "Video Tutorials"}}
r = {x["section"]: x for x in drift.place(rows_of(new_pairs), SECTIONS_CN, {}, no_video, tax.CATEGORIES)}
eq("the last unresolved newcomer pairs with the last unclaimed orphan",
   (r["Video Tutorials"]["basis"], r["Video Tutorials"]["category"], r["Video Tutorials"]["evidence"]["was"]),
   ("leftover", "Docs, Learning & Lists", "视频教程"))
eq("...so all eight libukai sections match PR #105 with no position evidence at all",
   {k: v["category"] for k, v in r.items()}, dict(zip(EN, CAT)))
two_left = {"skills_libukai": {k: v for k, v in lin.items() if k not in ("Video Tutorials", "Other Types")}}
r = {x["section"]: x for x in drift.place(rows_of(new_pairs), SECTIONS_CN, {}, two_left, tax.CATEGORIES)}
eq("...but two of each is not a pairing: both stay modal",
   (r["Video Tutorials"]["basis"], r["Other Types"]["basis"]), ("modal", "modal"))

# ── the palette ───────────────────────────────────────────────────────────────────────────────────
section("the palette")
eight = [(f"B{i}", [f"s{i}"]) for i in range(1, 9)]
smap = {("p", f"s{i}"): "Coding Agents" for i in range(1, 9)}
rows = [{"source": "p", "category": f"s{i}"} for i in range(1, 9)] + [{"source": "p", "category": "Mods"}]
recs = drift.place(rows, smap, {"p": eight}, {}, tax.CATEGORIES)
r = next(x for x in recs if x["section"] == "Mods")
eq("a ninth hue in a curated map folds into its last bucket", (r["bucket"], r["bucket_basis"]), ("B8", "fold"))
eq("...and the newcomer still gets a category", r["category"], "Coding Agents")
eq("...and the note says where to add it", r["buckets_note"], 'BUCKETS["p"]: add "Mods" to the "B8" bucket')

seven_named = [(f"B{i}", [f"s{i}"]) for i in range(1, 8)] + [("Absent", ["gone"])]
rows = [{"source": "p", "category": f"s{i}"} for i in range(1, 8)] + [{"source": "p", "category": "New"}]
smap2 = {("p", f"s{i}"): "Coding Agents" for i in range(1, 8)} | {("p", "New"): "Coding Agents"}
recs = drift.place(rows, smap2, {"p": seven_named}, {}, tax.CATEGORIES)
eq("slots count every bucket a map names, present or not (16_build_all's count, not the old one)",
   [(x["section"], x["bucket"]) for x in recs], [("New", "Absent")])
eq("...and a section the taxonomy maps but no bucket holds is a palette-only record",
   (recs[0]["category"], recs[0]["basis"], recs[0]["taxonomy_line"]), (None, "mapped", None))

nine = [f"t{i}" for i in range(1, 10)]
rows = [{"source": "q", "category": s} for s in nine[:4] + ["Newcomer"] + nine[4:8]]
recs = drift.place(rows, {("q", s): "Coding Agents" for s in nine[:8]}, {}, {}, tax.CATEGORIES)
eq("with no map, the newcomer is the one folded even when it arrived in the middle",
   [(x["section"], x["bucket"]) for x in recs if x["bucket"]], [("Newcomer", "t8")])
eq("...and the whole map it implies is proposed, eight buckets, the fold in the last",
   recs[0]["new_map"], [[s, [s]] for s in nine[:7]] + [["t8", ["t8", "Newcomer"]]])
true("...and the note says a map is needed", "has no map" in recs[0]["buckets_note"], recs[0]["buckets_note"])

rows = [{"source": "p", "category": f"s{i}"} for i in range(2, 9)] + [{"source": "p", "category": "S-one"}]
recs = drift.place(rows, smap, {"p": eight},
                   {"p": {"S-one": {"from": "s1", "basis": "position", "slot": 1, "of": 8}}}, tax.CATEGORIES)
eq("a renamed section inherits its predecessor's bucket, so it keeps its hue",
   [(x["section"], x["bucket"], x["bucket_basis"]) for x in recs], [("S-one", "B1", "inherited")])

# ── honouring ─────────────────────────────────────────────────────────────────────────────────────
section("honouring")
drift.PLACEMENTS.write_text(json.dumps({"placements": [
    {"source": "skills_libukai", "section": "Brand New", "category": "Agent Skills", "bucket": None},
    {"source": "claudecode", "section": "Fresh", "category": None, "bucket": "Workflow, UI & Media"},
    {"source": "claudecode", "section": "Mods", "category": None, "bucket": "Security"}]}), encoding="utf-8")
rec = {"source": "skills_libukai", "section": "Brand New"}
env(AAA_PROVISIONAL=None)
try:
    tax.category_of(rec)
    true("strict: category_of still raises with a placements file on disk", False)
except KeyError as e:
    true("strict: category_of still raises with a placements file on disk", "SECTIONS" in str(e))
true("strict: bucket_map ignores the folds", "Fresh" not in buckets.bucket_map("claudecode"))
env(AAA_PROVISIONAL="1")
eq("provisional: category_of returns the run's placement", tax.category_of(rec), "Agent Skills")
eq("provisional: bucket_map carries the fold", buckets.bucket_map("claudecode").get("Fresh"),
   "Workflow, UI & Media")
eq("...and the curated map wins where both name a section", buckets.bucket_map("claudecode")["Mods"],
   "Workflow, UI & Media")
eq("...and a mapped section is untouched", tax.category_of({"source": "skills_libukai", "section": "官方文档"}),
   "Docs, Learning & Lists")
try:
    tax.category_of({"source": "skills_libukai", "section": "Never Placed"})
    true("provisional: a section nobody placed still raises", False)
except KeyError:
    true("provisional: a section nobody placed still raises", True)
for val in ("0", "", "false"):
    env(AAA_PROVISIONAL=val)
    true(f"AAA_PROVISIONAL={val!r} is strict", not drift.enabled() and drift.placements() == [])
env(AAA_PROVISIONAL=None)

# ── the parse ─────────────────────────────────────────────────────────────────────────────────────
section("the parse")
b10 = load("b10", "10_parse_sources.py")
real = [{"source": "skills_libukai", "category": s} for s in CN]
drifted = real + [{"source": "skills_libukai", "category": "Jobs Board"}]
drift.PLACEMENTS.write_text("{}", encoding="utf-8")
step = TMP / "step-summary.md"
env(AAA_PROVISIONAL=None, GITHUB_ACTIONS="true", GITHUB_STEP_SUMMARY=str(step))
try:
    _, out, err = quiet(b10.unmapped, drifted)
    true("strict: an unmapped section exits", False)
except SystemExit as e:
    true("strict: an unmapped section exits 1", e.code == 1, repr(e.code))
true("strict: no placements file is left for anything to honour", not drift.PLACEMENTS.exists())
doc = json.loads(drift.PROPOSAL.read_text(encoding="utf-8"))
eq("strict: the proposal is still written, as a report", [r["section"] for r in doc["placements"]],
   ["Jobs Board"])
true("strict: and is marked not provisional", doc["provisional"] is False)
true("strict: annotates nothing (it is a stop, not a warning)", not step.exists())

env(AAA_PROVISIONAL="1")
recs, out, err = quiet(b10.unmapped, drifted)
eq("provisional: returns the placements instead of exiting", [r["section"] for r in recs], ["Jobs Board"])
eq("...filed under the list's mode", recs[0]["category"], "Agent Skills")
true("...says PROVISIONAL on stdout", "PROVISIONAL: 1 placement" in out, out)
placed = json.loads(drift.PLACEMENTS.read_text(encoding="utf-8"))
eq("...writes the placements file the later stages honour", [p["section"] for p in placed["placements"]],
   ["Jobs Board"])
eq("...which category_of then honours", tax.category_of({"source": "skills_libukai", "section": "Jobs Board"}),
   "Agent Skills")
ann = [ln for ln in out.splitlines() if ln.startswith("::warning ")]
eq("...one ::warning annotation per placement", len(ann), 1)
true("...naming the list, the section and the line to paste",
     "skills_libukai / Jobs Board" in ann[0] and '("skills_libukai", "Jobs Board"): "Agent Skills",' in ann[0],
     ann[0] if ann else out)
true("...with no comma in the annotation title (it would end the title)",
     "," not in ann[0].split("::", 2)[1], ann[0])
summ = step.read_text(encoding="utf-8")
true("...and a step-summary block with the table and the taxonomy line",
     "provisional placement" in summ and '("skills_libukai", "Jobs Board"): "Agent Skills",' in summ, summ)
doc = json.loads(drift.PROPOSAL.read_text(encoding="utf-8"))
true("...and a proposal with a fingerprint", doc["provisional"] and re.fullmatch(r"[0-9a-f]{64}", doc["fingerprint"]))
fp1 = doc["fingerprint"]
quiet(b10.unmapped, drifted)
eq("the same drift tomorrow has the same fingerprint (one PR, not seven)",
   json.loads(drift.PROPOSAL.read_text(encoding="utf-8"))["fingerprint"], fp1)

step.unlink()
recs, out, err = quiet(b10.unmapped, real)
eq("a clean provisional run places nothing", recs, [])
true("...deletes yesterday's placements", not drift.PLACEMENTS.exists())
doc = json.loads(drift.PROPOSAL.read_text(encoding="utf-8"))
eq("...and rewrites the proposal empty, so nobody acts on yesterday's",
   (doc["placements"], doc["degraded"], doc["fingerprint"]), ([], [], None))
true("...and annotates nothing", "::warning" not in out and not step.exists())

drift.PULL_REPORT.write_text(json.dumps({"sources": [
    {"key": "a", "nwo": "o/a", "status": "unreachable"},
    {"key": "b", "nwo": "o/b", "status": "failed: README.md came back 10B, was 9,000B (--force to accept)"},
    {"key": "c", "nwo": "o/c", "status": "failed: parsed 3 entries, was 300 -- restructured upstream? (--force to accept)"},
    {"key": "d", "nwo": "o/d", "status": "failed: README.md (HTTPError)"},
    {"key": "e", "nwo": "o/e", "status": "changed", "renamed_to": "n/e"},
    {"key": "f", "nwo": "o/f", "status": "unchanged"}]}), encoding="utf-8")
eq("degraded lists are read off the pull report, each kind told apart",
   [(d["source"], d["kind"]) for d in drift.degraded_from_pull()],
   [("a", "unreachable"), ("b", "shrink"), ("c", "parse-collapse"), ("d", "pull-failed"), ("e", "renamed")])
recs, out, err = quiet(b10.unmapped, real)
eq("...and each one is annotated, on a run with no placements at all",
   len([ln for ln in out.splitlines() if ln.startswith("::warning title=Held at previous copy")]), 5)
true("...and listed in the summary", "held at their previous copy" in step.read_text(encoding="utf-8"))
drift.PULL_REPORT.unlink()
env(AAA_PROVISIONAL=None, GITHUB_ACTIONS=None, GITHUB_STEP_SUMMARY=None)

# ── the pull ──────────────────────────────────────────────────────────────────────────────────────
section("the pull")
ps = load("ps", "pull_sources.py")
PCACHE = TMP / "cache"
(PCACHE / "sources").mkdir(parents=True)
FAKE = dict(key="fake", nwo="o/list", title="Fake", short="Fake", file="fake.md", mode={"bullet"}, cat_at=2)
target = PCACHE / "sources" / "fake.md"
keep = (ps.CACHE, ps.QUEUE, ps.b10.source_paths, ps.watch_sources.head, ps.readme_info, ps.raw_bytes)
ps.CACHE, ps.QUEUE = PCACHE, PCACHE / "collect-queue.json"
ps.b10.source_paths = lambda src: [target] if src is FAKE else keep[2](src)


def readme_md(heads: list[str], per: int, prefix: str = "r") -> bytes:
    out = ["# Fake list"]
    for h, head in enumerate(heads):
        out.append(f"## {head}")
        out += [f"- [{prefix}{h}-{j}](https://github.com/x/{prefix}{h}-{j}) - a thing" for j in range(per)]
    return ("\n".join(out) + "\n").encode("utf-8")


served = {"bytes": b"", "as": None, "fetched": []}
ps.watch_sources.head = lambda nwo: "b" * 40
ps.readme_info = lambda nwo: ("README.md", served["as"])


def fake_raw(nwo, sha, path):
    served["fetched"].append(nwo)
    return served["bytes"], ""


ps.raw_bytes = fake_raw
try:
    target.write_bytes(readme_md(["Uno", "Dos"], 6))
    state = {"sources": {"o/list": {"sha": "a" * 40, "files": {"sources/fake.md": {"bytes": 1}}}}}
    served["bytes"] = readme_md(["One", "Two"], 6)
    line, _, _ = quiet(ps.pull_one, FAKE, state, False)
    eq("a translated list pulls normally", line["status"], "changed")
    eq("...and its lineage is recorded for the parse",
       {k: v["from"] for k, v in drift.load_moves()["fake"].items()}, {"One": "Uno", "Two": "Dos"})

    before = target.read_bytes()
    rec_before = json.dumps(state["sources"]["o/list"], sort_keys=True)
    state["sources"]["o/list"]["sha"] = "c" * 40
    rec_before = json.dumps(state["sources"]["o/list"], sort_keys=True)
    served["bytes"] = readme_md(["One"], 1).replace(b"## One", b"#### One") + b"x" * len(before)
    line, _, _ = quiet(ps.pull_one, FAKE, state, False)
    true("a full-size copy that parses to under a quarter of the last is refused",
         line["status"].startswith("failed: parsed 1 entries, was 12"), line["status"])
    eq("...yesterday's bytes are back on disk", target.read_bytes(), before)
    eq("...and nothing is recorded, so tomorrow tries again",
       json.dumps(state["sources"]["o/list"], sort_keys=True), rec_before)
    line, _, _ = quiet(ps.pull_one, FAKE, state, True)
    true("--force takes it", not line["status"].startswith("failed"), line["status"])

    target.write_bytes(readme_md(["One", "Two"], 6))
    state["sources"]["o/list"]["sha"] = "d" * 40
    served["bytes"], served["as"], served["fetched"] = readme_md(["One", "Two"], 6, "z"), "New/list", []
    line, _, _ = quiet(ps.pull_one, FAKE, state, False)
    eq("a renamed list repo is reported under its new name", line.get("renamed_to"), "New/list")
    eq("...and fetched from it, not through the redirect", served["fetched"], ["New/list"])
    served["as"] = "O/List"
    state["sources"]["o/list"]["sha"] = "e" * 40
    line, _, _ = quiet(ps.pull_one, FAKE, state, False)
    true("...but a change of case is not a rename", "renamed_to" not in line)
finally:
    ps.CACHE, ps.QUEUE, ps.b10.source_paths, ps.watch_sources.head, ps.readme_info, ps.raw_bytes = keep

# ── the proposal ──────────────────────────────────────────────────────────────────────────────────
section("the proposal")
TAX = '''SECTIONS: dict = {
    # one/list
    ("one", "A"): "Coding Agents",
    ("one", "B"): "MCP Servers",

    # two/list
    ("two", "Long"):
        "Sandbox, Security & Governance",
}
'''
BUCK = '''BUCKETS = {
    "one": [
        ("First", ["A"]),
        ("Catch-all", [
            "B", "C"]),
    ],
}
'''
P = [{"source": "one", "section": "Jobs", "category": "Coding Agents", "bucket": "Catch-all"},
     {"source": "two", "section": "Next", "category": "MCP Servers", "bucket": None},
     {"source": "three", "section": "首页", "category": "Agent Skills", "bucket": None},
     {"source": "one", "section": "Mods", "category": None, "bucket": "First"},
     {"source": "four", "section": "t9", "category": None, "bucket": "t8",
      "new_map": [["t1", ["t1"]], ["t8", ["t8", "t9"]]]}]
t, done = apply.add_sections(TAX, P)
lines = t.split("\n")
eq("a key lands at the end of its own list's block",
   lines[lines.index('    ("one", "B"): "MCP Servers",') + 1], '    ("one", "Jobs"): "Coding Agents",')
eq("...after a value on its own line, not between the key and it",
   lines[lines.index('        "Sandbox, Security & Governance",') + 1], '    ("two", "Next"): "MCP Servers",')
true("...a list with no block gets one, before the brace, unescaped",
     '    ("three", "首页"): "Agent Skills",\n}' in t, t)
eq("...and only category placements touch taxonomy.py", len(done), 3)
eq("applying twice is applying once", apply.add_sections(t, P), (t, []))
ns: dict = {}
exec(t.replace("SECTIONS: dict", "SECTIONS"), ns)
eq("...and the result is Python with every key in it", len(ns["SECTIONS"]), 6)

b, done = apply.add_buckets(BUCK, P)
ns = {}
exec(b, ns)
eq("a section joins a multi-line bucket", dict(ns["BUCKETS"]["one"])["Catch-all"], ["Jobs", "B", "C"])
eq("...and a single-line one", dict(ns["BUCKETS"]["one"])["First"], ["Mods", "A"])
eq("...and a list with no map gets the whole map proposed", ns["BUCKETS"]["four"],
   [("t1", ["t1"]), ("t8", ["t8", "t9"])])
eq("applying twice is applying once", apply.add_buckets(b, P), (b, []))

# ── guards ────────────────────────────────────────────────────────────────────────────────────────
section("guards")
f11 = load("f11", "11_fetch_all.py")
want = [{"nwo": f"o/r{i}"} for i in range(1000)]
gone = {f"o/r{i}": {"error": "gh api repos/o/r failed: gh: Not Found (HTTP 404)"} for i in range(300)}
eq("hundreds of 404s are repos that are gone, not an outage", f11.mass_failure(want, gone), None)
limit = {f"o/r{i}": {"error": "gh api graphql failed: API rate limit exceeded"} for i in range(150)}
true("a tenth of the run failing for a reason not about the repo stops it",
     "150 of the 1000" in (f11.mass_failure(want, limit) or ""), str(f11.mass_failure(want, limit)))
few = {f"o/r{i}": {"error": "HTTP 502"} for i in range(40)}
eq("...but not under the floor", f11.mass_failure(want[:100], few), None)

# The threshold, at both edges of both numbers: max(50, 10% of the run).
eq("the threshold is the floor for a small run", f11.threshold(100), 50)
eq("...and a tenth of a large one", f11.threshold(1000), 100)
err = lambda n: {f"o/r{i}": {"error": "HTTP 502"} for i in range(n)}  # noqa: E731
eq("100 of 1000 is at the threshold, not over it", f11.mass_failure(want, err(100)), None)
true("101 of 1000 is over it", f11.mass_failure(want, err(101)) is not None)
eq("50 of 200 is at the floor", f11.mass_failure(want[:200], err(50)), None)
true("51 of 200 is over it", f11.mass_failure(want[:200], err(51)) is not None)

eq("each failure is told apart by kind",
   [f11.kind(e) for e in ("gh: Not Found (HTTP 404)", "gh: Bad credentials (HTTP 401)",
                          "API rate limit exceeded for installation", "You have exceeded a secondary rate limit",
                          "HTTP 502: Bad Gateway", "To get started with GitHub CLI, please run: gh auth login")],
   ["gone", "auth", "rate", "rate", "other", "auth"])


class Crawl:
    """`fetch` for `recover`: a GitHub that refuses the first `bad_rounds` retries the way `say` does."""

    def __init__(self, say: str, bad_rounds: int):
        self.say, self.bad_rounds, self.calls = say, bad_rounds, []

    def __call__(self, w, m):
        self.calls.append(len(w))
        for x in w:
            m[x["nwo"]] = {"error": self.say} if len(self.calls) <= self.bad_rounds else {"stargazerCount": 1}


def run_recover(meta, crawl, reset=None):
    slept: list[float] = []
    out = f11.recover(want, meta, crawl, sleep=slept.append, wait_for_reset=lambda: reset,
                      log=lambda *a, **k: None)
    return out, slept


auth = {f"o/r{i}": {"error": "gh: Bad credentials (HTTP 401)"} for i in range(400)}
crawl = Crawl("gh: Bad credentials (HTTP 401)", 99)
out, slept = run_recover(dict(auth), crawl)
true("an auth failure stops at once, saying it is the token", out and "GH_TOKEN" in out, str(out))
eq("...without waiting or retrying: no wait fixes a token", (slept, crawl.calls), ([], []))

rl = {f"o/r{i}": {"error": "API rate limit exceeded"} for i in range(400)}
crawl = Crawl("API rate limit exceeded", 1)
meta = dict(rl)
out, slept = run_recover(meta, crawl)
eq("a rate limit that clears on the second retry does not stop the run", out, None)
eq("...after backing off on the schedule", slept, list(f11.RETRY_WAITS[:2]))
eq("...asking again about the failing repos only", crawl.calls, [400, 400])
true("...whose metadata is then real", all("error" not in meta[f"o/r{i}"] for i in range(400)))

crawl = Crawl("API rate limit exceeded", 1)
out, slept = run_recover(dict(rl), crawl, reset=600)
eq("a reset GitHub reports is waited for, when it is longer than the backoff", slept[0], 600)
crawl = Crawl("API rate limit exceeded", 1)
out, slept = run_recover(dict(rl), crawl, reset=99999)
eq("...but never past MAX_WAIT", slept[0], f11.MAX_WAIT)

crawl = Crawl("API rate limit exceeded", 99)
out, slept = run_recover(dict(rl), crawl)
true("a rate limit that outlasts every retry stops the run, and says so",
     out and "outlasted every retry" in out, str(out))
eq("...after every wait in the schedule, and no more", slept, list(f11.RETRY_WAITS))
true("...in under the daily job's timeout", sum(f11.RETRY_WAITS) <= 30 * 60)

mixed = {**{f"o/r{i}": {"error": "gh: Not Found (HTTP 404)"} for i in range(300)},
         **{f"o/r{i}": {"error": "HTTP 502"} for i in range(300, 330)}}
crawl = Crawl("HTTP 502", 99)
out, slept = run_recover(dict(mixed), crawl)
eq("under the threshold nothing is retried at all: the run proceeds as it always did",
   (out, slept, crawl.calls), (None, [], []))

for wf in ("daily.yml", "weekly.yml"):
    text = (ROOT / ".github" / "workflows" / wf).read_text(encoding="utf-8")
    job_env = text.split("\n    env:\n", 1)[1].split("\n    steps:", 1)[0] if "\n    env:\n" in text else ""
    true(f"{wf}: AAA_PROVISIONAL is set for the whole build job", 'AAA_PROVISIONAL: "1"' in job_env)
    true(f"{wf}: ...and the parse runs inside it",
         "python scripts/10_parse_sources.py" in text.split("\n    steps:", 1)[1])

md_src = (SCRIPTS / "17_markdown.py").read_text(encoding="utf-8")
md_ns: dict = {"re": re}
exec(md_src[md_src.index("def norm("):md_src.index("def stars(")], md_ns)
eq("Markdown prose: an upstream \\| in a description is a plain pipe outside a table",
   md_ns["prose"]("a \\| b"), "a | b")
eq("...and one escape, not two, inside one", md_ns["prose"]("a \\| b | c", table=True), "a \\| b \\| c")

# The real tree: whatever is on disk today must load strict and pass the palette check.
_, out, _ = quiet(buckets.check)
true("buckets.py as committed passes its own check", "sources, buckets per sheet" in out)

for k, v in SAVED_ENV.items():
    env(**{k: v})
shutil.rmtree(TMP, ignore_errors=True)
print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
