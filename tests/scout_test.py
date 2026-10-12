"""Unit tests for the scout, `scripts/12_scout.py`, and for how the rest of the pipeline takes it in.

The scout is the one source in the atlas that nobody curates: GitHub search decides what is in it, and a
regex over topics decides where each repo is filed. So everything it does is a rule, and every rule here
is asserted by a fixture that is clean in every respect but the one the rule is about -- delete the rule
and that fixture sails through, which is the failure this file exists to report. Nothing here touches the
network: the search transport, the clock and `sleep` are all replaced, and every path the stage writes is
repointed into a scratch directory before the first call, so a broken rule cannot reach the committed
`state/` or the shared `cache/`.

Nine groups:

  the rules      -- `verdict()`, one exclusion at a time: fork, archived, disabled, mirror, no description,
                    spam (the `ReverseEngineerAnything/REA` download-bait clone of `morluto/rea` is the
                    reference fixture, given enough stars to pass every threshold), off-topic, an awesome
                    list, a list already in SOURCES. Then both bars at their boundaries: the young window's
                    first and last day and its 300-star floor, the any-age tier's 2,000-star floor, its ERA
                    floor and its narrower topic set.
  the sections   -- `section_of()`: most-topics-wins, the tie going to the earlier family, the generic and
                    harness fallbacks in that order, and that the ten sections are exactly the ten
                    `("scout", ...)` keys in `taxonomy.SECTIONS`, each mapping to itself, folded into <= 8
                    buckets.
  the ledger     -- `merge_repos()`: sticky membership (absence is not evidence; aging out is not a
                    reason), leaving only on a quality failure observed today, renames followed by id,
                    re-filing when topics change. And the two levers a person has over a sticky set:
                    the `ignore` key, which keeps a repo out for good, and `--reset`, which applies a
                    tightened rule to what is already scouted.
  the document   -- `render()` is a pure function of the ledger, parses through the real
                    `10_parse_sources.parse` into one `repo` row per scouted repo in its own section, holds
                    no date and no star count, and is byte-identical however the search results were
                    ordered. `content_digest` ignores CRLF.
  failure        -- a search that errors, rate-limits past its retries, comes back incomplete or is
                    rejected leaves both ledgers byte-identical and re-renders the same document, including
                    onto a cold cache where the document is gone; the list half fails with the rising half.
  the transport  -- pacing, a rate limit waited out, a 422 never retried, pagination and the 1,000 cap.
  candidates     -- first-seen preserved across runs, today's values refreshed, SOURCES and stale or small
                    lists excluded, an awesome list a rising query found counted too, and the summary that
                    reaches $GITHUB_STEP_SUMMARY.
  the gate       -- `watch_sources.py` against a scratch ledger: the scout's first digest is a move, a
                    recorded one is not, a different set is, the same set re-rendered or in CRLF is not, a
                    missing document is not, and `head()` is never asked about the scout. `pull_sources.py`
                    leaves it alone.
  downstream     -- `taxonomy.by_repo` does not let a scouted listing out-vote a curator, and
                    `16_build_all.repo_pool` does not let it replace a curator's blurb, while a repo only
                    the scout has keeps both. And the wiring: the stage runs before the parser in both
                    workflows and before the watch in the daily, and the committed ledger parses.

Needs openpyxl for the last group, as `media_test.py` does; everything else is standard library.

Run: python tests/scout_test.py
"""
from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import json
import os
import random
import re
import sys
import tempfile
import zlib
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

spec = importlib.util.spec_from_file_location("scout_for_test", SCRIPTS / "12_scout.py")
s = importlib.util.module_from_spec(spec)
sys.modules["scout_for_test"] = s
spec.loader.exec_module(s)

import taxonomy as tax  # noqa: E402
import buckets  # noqa: E402

TMP = Path(tempfile.mkdtemp(prefix="scout_test_", dir=os.environ.get("AAA_TMP") or None))
s.REPOS = TMP / "state" / "scout-repos.json"
s.LISTS = TMP / "state" / "scout-lists.json"
s.DOC = TMP / "cache" / "sources" / "scout.md"

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


def group(title: str) -> None:
    print(f"\n── {title} " + "─" * max(3, 92 - len(title)))


TODAY = date(2026, 10, 11)
CUTOFF = TODAY - timedelta(days=s.YOUNG_DAYS)          # 2026-04-14, the first day inside the window
CURATED = s.curated_nwos()


def repo(name: str, stars: int = 900, created: str = "2026-08-01", topics=("ai-agents",),
         desc: str = "An agent that files your expense reports", pushed: str = "2026-10-01", **kw) -> dict:
    """One search result, shaped like the API's: clean in every respect unless a keyword says otherwise."""
    owner, rname = name.split("/")
    return dict({"id": zlib.crc32(name.lower().encode()), "full_name": name, "name": rname,
                 "stargazers_count": stars, "created_at": f"{created}T00:00:00Z",
                 "pushed_at": f"{pushed}T00:00:00Z", "topics": list(topics), "description": desc,
                 "fork": False, "archived": False, "disabled": False, "mirror_url": None}, **kw)


def verdict(item, today=TODAY):
    return s.verdict(item, today, CURATED)


# ======================================================================================== the rules
group("the rules")
base = repo("acme/taxbot")
eq("the clean fixture qualifies", verdict(base), "")
eq("a fork is excluded", verdict(dict(base, fork=True)), "fork")
eq("an archived repo is excluded", verdict(dict(base, archived=True)), "archived")
eq("a disabled repo is excluded", verdict(dict(base, disabled=True)), "disabled")
eq("a mirror (mirror_url) is excluded", verdict(dict(base, mirror_url="https://git.example/x")), "mirror")
eq("a mirror (says so) is excluded", verdict(dict(base, description="Mirror of foo/agent, synced hourly")),
   "mirror")
eq("no description is excluded", verdict(dict(base, description="")), "no description")
eq("a whitespace description is no description", verdict(dict(base, description="   ")), "no description")
eq("a null description is no description", verdict(dict(base, description=None)), "no description")

# The reference spam case, verbatim from the API on 2026-10-11, given the stars and the topic it would need
# to clear every threshold -- so the only thing standing between it and the atlas is the spam rule.
REA_CLONE = repo(
    "ReverseEngineerAnything/REA", stars=4_000, created="2026-10-11",
    topics=["ai-agents", "decompilation", "github-rea", "rea-github", "reverse-engineer-anything"],
    desc="REA Reverse Engineer Anything 6.3.0 is the agent RE desk: github rea, rea github, rea reverse "
         "engineer, reverse engineer anything, rea mcp. Oct 10 2026. Windows 10/11 x64. Official free "
         "download. Local zip. Download:🡇")
eq("the REA download-bait clone is spam, at any star count", verdict(REA_CLONE), "spam")
REA = repo("morluto/rea", stars=110_506, created="2026-04-14",
           topics=["agent-skills", "ai-agents", "binary-analysis", "claude-code", "cli", "codex", "mcp",
                   "model-context-protocol", "reverse-engineering", "llm"],
           desc="Reverse engineer anything with agents, from app behavior down to native binaries.")
eq("...while the project it copies qualifies", verdict(REA), "")
for phrase in ("Free download for Windows", "includes keygen", "Activation code included",
               "Run setup.exe to install", "cracked build of an agent", "license key generator"):
    eq(f"spam phrase: {phrase!r}", verdict(dict(base, description=f"An agent tool. {phrase}")), "spam")
eq("spam by topic alone", verdict(dict(base, topics=["ai-agents", "free-download"])), "spam")
eq("'cracking' is a word, not a crack", verdict(dict(base, description="Cracking long tasks with agents")),
   "")

eq("no agentic word anywhere is off-topic",
   verdict(repo("acme/fastjson", desc="A fast JSON parser for Go")), "off-topic")
eq("bare 'AI' is not an agentic word", verdict(repo("acme/sheets", desc="AI-powered spreadsheets")),
   "off-topic")
eq("an agentic name is enough", verdict(repo("acme/agentkit", desc="A fast JSON parser")), "")
eq("CJK beside an ASCII word still matches", verdict(repo("acme/bettafish", desc="人人可用的多Agent舆情分析助手")),
   "")
eq("a CJK agentic word matches", verdict(repo("acme/zhiti", desc="开源智能体平台")), "")
eq("'Model Context Protocol' matches", verdict(repo("acme/bridge", desc="A Model Context Protocol bridge")),
   "")
eq("an awesome list is not a rising repo", verdict(repo("acme/awesome-agents")), "list")
eq("a list in SOURCES is excluded, whatever its casing",
   verdict(repo("Hesreallyhim/Awesome-Claude-Code")), "curated list")

eq("young: 300 stars is in", verdict(dict(base, stargazers_count=300)), "")
eq("young: 299 stars is out", verdict(dict(base, stargazers_count=299)), "below threshold")
eq("young: created on the window's first day is in",
   verdict(dict(base, created_at=f"{CUTOFF.isoformat()}T00:00:00Z")), "")
eq("young: a day earlier is out",
   verdict(dict(base, created_at=f"{(CUTOFF - timedelta(days=1)).isoformat()}T23:59:59Z")),
   "below threshold")
eq("young: needs a scouted topic, not just agentic prose", verdict(dict(base, topics=["python"])),
   "below threshold")
old = repo("acme/oldagent", stars=2_000, created="2024-01-01", topics=["ai-agents"])
eq("core: 2,000 stars at any age is in", verdict(old), "")
eq("core: 1,999 is out", verdict(dict(old, stargazers_count=1_999)), "below threshold")
eq("core: older than ERA is out at any star count",
   verdict(dict(old, stargazers_count=150_000, created_at="2022-12-31T00:00:00Z")), "below threshold")
eq("core: created on ERA itself is in", verdict(dict(old, created_at=f"{s.ERA}T00:00:00Z")), "")
eq("core: `mcp` alone is not a core topic", verdict(dict(old, topics=["mcp"])), "below threshold")
eq("core: `mcp-server` is", verdict(dict(old, topics=["mcp-server"])), "")
eq("tier() names which bar", (s.tier(base, TODAY), s.tier(old, TODAY), s.tier(dict(old, stargazers_count=5),
                                                                                TODAY)),
   ("young", "core", ""))

# ======================================================================================== the sections
group("the sections")
sec = lambda *t: s.section_of(repo("acme/x", topics=t))  # noqa: E731
eq("one family's topic files there", sec("mcp-server"), "MCP Servers")
eq("most topics wins", sec("agent-skills", "mcp", "mcp-server"), "MCP Servers")
eq("a tie goes to the earlier family", sec("agent-skills", "mcp-server"), "Agent Skills")
eq("morluto/rea files under MCP Servers (two MCP topics to one skill topic)", s.section_of(REA),
   "MCP Servers")
eq("a specific family beats any number of generic topics", sec("ai-agents", "agents", "agentic-ai", "rag"),
   "Context, Memory & RAG")
eq("generic topics alone: Assistants & Domain Agents", sec("ai-agents", "llm-agent"),
   "Assistants & Domain Agents")
eq("generic is asked before harness", sec("ai-agents", "claude-code"), "Assistants & Domain Agents")
eq("a harness name alone: Plugins, Themes & Clients", sec("claude-code", "codex"), "Plugins, Themes & Clients")
eq("no topics at all falls to the generic shelf", sec(), "Assistants & Domain Agents")
eq("topics are matched case-insensitively", sec("MCP-Server"), "MCP Servers")

order = [tax.CATEGORIES.index(sct) for sct, _ in s.FAMILIES]
eq("FAMILIES are in CATEGORIES order, which is what makes the tie-break the atlas's own", order, sorted(order))
flat = [t for _, ts in s.FAMILIES for t in ts] + list(s.GENERIC[1]) + list(s.HARNESS[1])
eq("no topic belongs to two families", len(flat), len(set(flat)))
# Read off the queries the builder actually emits, not off the TOPICS constant it is built from: a check
# against the constant would agree with itself whatever rising_queries() did with it.
asked_young = {re.search(r"topic:(\S+)", q).group(1) for q in s.rising_queries(TODAY) if "created:>=2026" in q}
asked_core = {re.search(r"topic:(\S+)", q).group(1) for q in s.rising_queries(TODAY)
              if f"stars:>={s.CORE_STARS}" in q}
eq("every topic a family names gets a young-tier query", asked_young, set(flat))
eq("every core topic gets an any-age query", asked_core, set(s.CORE_TOPICS))
true("every core topic is also a family topic, so a core repo has a section to land in",
     set(s.CORE_TOPICS) <= set(flat))
true("each young query carries the window, the star bar and the hygiene qualifiers",
     all(f"stars:>={s.YOUNG_STARS} created:>={CUTOFF.isoformat()} fork:false archived:false" in q
         for q in s.rising_queries(TODAY) if "created:>=2026" in q))
scout_keys = {sec_ for (k, sec_) in tax.SECTIONS if k == s.SCOUT["key"]}
eq("taxonomy.SECTIONS names exactly the scout's sections, both directions", scout_keys, set(s.SECTIONS))
eq("...each one maps to the category it is spelled as",
   {x: tax.SECTIONS[(s.SCOUT["key"], x)] for x in s.SECTIONS}, {x: x for x in s.SECTIONS})
true("...and each is a real category", set(s.SECTIONS) <= set(tax.CATEGORIES))
fold = buckets.bucket_map(s.SCOUT["key"])
eq("buckets fold every section", set(fold), set(s.SECTIONS))
true("...into at most eight buckets", len(set(fold.values())) <= 8, str(set(fold.values())))
eq("taxonomy.ADVISORY is exactly the synthetic sources",
   tax.ADVISORY, {x["key"] for x in s.b10.SOURCES if x.get("synthetic")})

# ======================================================================================== the ledger
group("the ledger")


def ledger(**repos) -> dict:
    return {"version": 1, "repos": repos}


pool = [base, REA, REA_CLONE, repo("acme/awesome-agents"), dict(repo("acme/forked"), fork=True),
        repo("acme/small", stars=10), base]                    # base twice: two queries returned it
L = ledger()
rep = s.merge_repos(L, pool, TODAY, CURATED)
eq("only the qualifying repos are added, once each", sorted(L["repos"]), ["acme/taxbot", "morluto/rea"])
eq("...and the report says so", rep["added"], ["acme/taxbot", "morluto/rea"])
eq("an entry records id, section and the day it was scouted",
   L["repos"]["morluto/rea"], {"id": REA["id"], "section": "MCP Servers", "since": "2026-10-11"})
before = copy.deepcopy(L)
rep2 = s.merge_repos(L, list(reversed(pool)), TODAY + timedelta(days=1), CURATED)
eq("the same results a day later change nothing", L, before)
eq("...and report nothing", (rep2["added"], rep2["dropped"], rep2["moved"], rep2["renamed"]),
   ([], [], [], []))
s.merge_repos(L, [base], TODAY + timedelta(days=2), CURATED)
true("sticky: a repo today's search did not return stays", "morluto/rea" in L["repos"])
aged = dict(REA, created_at="2026-04-14T00:00:00Z", stargazers_count=500)
s.merge_repos(L, [aged], date(2027, 3, 1), CURATED)
true("sticky: a returned repo that has aged out of every bar stays", "morluto/rea" in L["repos"])
eq("...with its original `since`", L["repos"]["morluto/rea"]["since"], "2026-10-11")
for why, mutate in (("archived", dict(archived=True)), ("fork", dict(fork=True)),
                    ("spam", dict(description="An agent. Official free download")),
                    ("off-topic", dict(description="A JSON parser", name="taxjson")),
                    ("mirror", dict(mirror_url="https://example.org/m.git")),
                    ("no description", dict(description=""))):
    L2 = ledger(**{"acme/taxbot": {"id": base["id"], "section": "Assistants & Domain Agents",
                                   "since": "2026-10-01"}})
    r = s.merge_repos(L2, [dict(base, **mutate)], TODAY, CURATED)
    eq(f"a scouted repo seen today as {why} leaves", (L2["repos"], r["dropped"]), ({}, [("acme/taxbot", why)]))
L3 = ledger(**{"acme/taxbot": {"id": base["id"], "section": "Assistants & Domain Agents", "since": "2026-10-01"}})
s.merge_repos(L3, [dict(base, name="awesome-taxbot", full_name="acme/awesome-taxbot")], TODAY, CURATED)
eq("a scouted repo renamed into an awesome list leaves the scouted set", L3["repos"], {})
L4 = ledger(**{"acme/taxbot": {"id": base["id"], "section": "Assistants & Domain Agents", "since": "2026-10-01"}})
r4 = s.merge_repos(L4, [dict(base, full_name="acme-labs/taxbot")], TODAY, CURATED)
eq("a rename is followed by id, keeping `since`", L4["repos"],
   {"acme-labs/taxbot": {"id": base["id"], "section": "Assistants & Domain Agents", "since": "2026-10-01"}})
eq("...and reported", r4["renamed"], [("acme/taxbot", "acme-labs/taxbot")])
L5 = ledger(**{"Acme/TaxBot": {"section": "Assistants & Domain Agents", "since": "2026-10-01"}})
s.merge_repos(L5, [base], TODAY, CURATED)
eq("a casing change with no id on record is the same repo", list(L5["repos"]), ["acme/taxbot"])
L6 = ledger(**{"acme/taxbot": {"id": base["id"], "section": "Assistants & Domain Agents", "since": "2026-10-01"}})
r6 = s.merge_repos(L6, [dict(base, topics=["ai-agents", "agent-memory"])], TODAY, CURATED)
eq("new topics re-file a scouted repo", L6["repos"]["acme/taxbot"]["section"], "Context, Memory & RAG")
eq("...and the move is reported", r6["moved"],
   [("acme/taxbot", "Assistants & Domain Agents", "Context, Memory & RAG")])

entry = {"id": base["id"], "section": "Assistants & Domain Agents", "since": "2026-10-01"}
L7 = ledger(**{"acme/taxbot": dict(entry)})
L7["ignore"] = {"Acme/TaxBot": "not an agent, on inspection"}
r7 = s.merge_repos(L7, [base], TODAY, CURATED)
eq("`ignore` removes a scouted repo that still qualifies, whatever the casing", L7["repos"], {})
eq("...and says why", r7["dropped"], [("acme/taxbot", "ignored")])
s.merge_repos(L7, [base], TODAY + timedelta(days=1), CURATED)
eq("...and keeps it out on the next run", L7["repos"], {})
eq("...and the note survives a save", json.loads(s.dump(L7))["ignore"], {"Acme/TaxBot": "not an agent, on inspection"})
L8 = ledger(**{"acme/taxbot": dict(entry), "morluto/rea": {"id": REA["id"], "section": "MCP Servers",
                                                             "since": "2026-10-11"}})
gone = dict(base, stargazers_count=120)               # returned, but under every bar now
r8 = s.merge_repos(L8, [gone, REA], TODAY, CURATED, reset=True)
eq("--reset keeps only what qualifies today", sorted(L8["repos"]), ["morluto/rea"])
eq("...reporting the rest", r8["dropped"], [("acme/taxbot", "reset")])
eq("...and a survivor keeps its `since`", L8["repos"]["morluto/rea"]["since"], "2026-10-11")
L9 = ledger(**{"acme/taxbot": dict(entry), "absent/one": {"section": "MCP Servers", "since": "2026-10-01"}})
s.merge_repos(L9, [base], TODAY, CURATED, reset=True)
eq("--reset also drops what today's search did not return at all", sorted(L9["repos"]), ["acme/taxbot"])

# ======================================================================================== the document
group("the document")
items = [repo(f"own{i % 7}/agent-{i}", topics=[random.Random(i).choice(s.TOPICS)]) for i in range(60)]
items += [REA, base]
A, B = ledger(), ledger()
s.merge_repos(A, items, TODAY, CURATED)
shuffled = items[:]
random.Random(3).shuffle(shuffled)
s.merge_repos(B, shuffled, TODAY, CURATED)
eq("the ledger does not depend on the order results arrived in", s.dump(A), s.dump(B))
eq("...nor does the document", s.render(A), s.render(B))
eq("the document is a pure function of the ledger", s.render(A), s.render(json.loads(s.dump(A))))
# A ledger is a dict, and its key order is whatever built it: the merge's, json's case-sensitive sort,
# or a hand edit. The document has to be the same for all of them.
cased = ledger(**{"Zeta/Agent": {"section": "MCP Servers"}, "alpha/mcp": {"section": "MCP Servers"},
                  "Beta/mcp-kit": {"section": "MCP Servers"}})
eq("the document does not depend on the ledger's key order",
   s.render(cased), s.render(ledger(**dict(reversed(list(cased["repos"].items()))))))
eq("...and lists a section's repos case-insensitively by name",
   [r["nwo"] for r in s.b10.parse(s.SCOUT, s.render(cased))], ["alpha/mcp", "Beta/mcp-kit", "Zeta/Agent"])
doc = s.render(A)
rows = s.b10.parse(s.SCOUT, doc)
eq("it parses into exactly the scouted repos", sorted(r["nwo"] for r in rows), sorted(A["repos"]))
eq("...every one a `repo` row from the scout", {(r["kind"], r["source"]) for r in rows}, {("repo", "scout")})
eq("...each in the section its ledger entry names",
   {r["nwo"]: r["category"] for r in rows}, {n: e["section"] for n, e in A["repos"].items()})
eq("...with no description of its own, so the repo's description is the blurb",
   {r["description"] for r in rows}, {""})
true("it carries no date", not re.search(r"20\d\d-\d\d-\d\d", doc))
# The fixture's names carry at most two digits, so any longer number would be a star count or an id.
true("...and no star count or id", not re.search(r"(?<![\w-])\d{3,}(?![\w-])", doc),
     str(re.findall(r"(?<![\w-])\d{3,}(?![\w-])", doc)[:5]))
known = s.render(ledger(**{"a/b": {"section": "MCP Servers"}, "c/d": {"section": "Retired Family"}}))
true("a section no family names any more is still rendered, after the known ones",
     "## Retired Family" in known and known.index("## MCP Servers") < known.index("## Retired Family"))
src = dict(s.SCOUT)
(TMP / "digest").mkdir()
keep_src = s.b10.SRC
s.b10.SRC = TMP / "digest"
(s.b10.SRC / src["file"]).write_bytes(doc.encode())
lf = s.b10.content_digest(src)
(s.b10.SRC / src["file"]).write_bytes(doc.replace("\n", "\r\n").encode())
eq("content_digest ignores CRLF", s.b10.content_digest(src), lf)
true("...is labelled", lf.startswith("sha256:") and len(lf) == 7 + 64)
(s.b10.SRC / src["file"]).write_bytes((doc + "- [x](https://github.com/x/x)\n").encode())
true("...and moves when the set does", s.b10.content_digest(src) != lf)
(s.b10.SRC / src["file"]).unlink()
eq("...and is None with no document", s.b10.content_digest(src), None)
s.b10.SRC = keep_src


# ======================================================================================== failure
group("failure")


class Clock:
    def __init__(self):
        self.t = 1_800_000_000.0
        self.slept: list[float] = []

    def time(self) -> float:
        return self.t

    def sleep(self, secs: float) -> None:
        self.slept.append(secs)
        self.t += secs


class Fake:
    """GitHub search over a fixture set: topic qualifier honoured, star/date qualifiers deliberately not,
    so the client-side rules are what filter. `fail(q, page)` may return a response or raise."""

    def __init__(self, items, fail=None, clock=None):
        self.items, self.fail, self.clock = items, fail, clock
        self.calls: list[tuple[str, int, float]] = []

    def __call__(self, q: str, page: int):
        self.calls.append((q, page, self.clock.t if self.clock else 0.0))
        if self.fail:
            got = self.fail(q, page)
            if got is not None:
                return got
        topic = re.search(r"topic:(\S+)", q).group(1)
        hits = [i for i in self.items if topic in i["topics"]
                and ("awesome in:name" not in q or "awesome" in i["name"].lower())]
        hits.sort(key=lambda i: (-i["stargazers_count"], i["full_name"]))
        at = (page - 1) * s.PER_PAGE
        return 200, {"x-ratelimit-remaining": "29", "x-ratelimit-reset": "0"}, \
            {"total_count": len(hits), "incomplete_results": False, "items": hits[at:at + s.PER_PAGE]}


def search(items, fail=None):
    clock = Clock()
    fake = Fake(items, fail, clock)
    return s.Search(transport=fake, sleep=clock.sleep, clock=clock.time, log=lambda *a: None), fake, clock


def quiet(*_a) -> None:
    pass


LIST = repo("acme/awesome-agent-tools", stars=400, topics=["ai-agents", "awesome-list"],
            desc="A curated list of agent tools")
DAY1 = [base, REA, REA_CLONE, LIST, repo("acme/memo", topics=["agent-memory"])]


def reset() -> None:
    for p in (s.REPOS, s.LISTS, s.DOC):
        if p.exists():
            p.unlink()


def snapshot() -> tuple:
    return tuple(p.read_bytes() if p.exists() else None for p in (s.REPOS, s.LISTS, s.DOC))


reset()
sr, fake, _ = search(DAY1)
res = s.run(TODAY, sr, log=quiet)
eq("a good run scouts the qualifying repos", sorted(res["repos"]), ["acme/memo", "acme/taxbot", "morluto/rea"])
true("...not the spam clone, end to end", "ReverseEngineerAnything/REA" not in res["repos"])
eq("...and writes both ledgers and the document", res["wrote"], {"repos": True, "lists": True, "doc": True})
eq("the document on disk is the ledger rendered", s.DOC.read_bytes(), s.render(s.load(s.REPOS, "repos")).encode())
good = snapshot()
again, _, _ = search(DAY1)
eq("an identical second run writes nothing", s.run(TODAY, again, log=quiet)["wrote"],
   {"repos": False, "lists": False, "doc": False})
eq("...and every byte is as it was", snapshot(), good)

DAY2 = DAY1 + [repo("acme/newcomer", stars=5_000), repo("acme/awesome-mcp-picks", stars=900,
                                                         topics=["mcp", "awesome-list"])]


def boom(q, page):
    raise s.ScoutError("TLS handshake timeout")


cases = {
    "a transport error on every attempt": boom,
    "HTTP 502 on one query, every attempt":
        lambda q, p: (502, {}, {"message": "Bad gateway"}) if "topic:rag " in q else None,
    "incomplete_results on one query, every attempt":
        lambda q, p: (200, {}, {"total_count": 1, "incomplete_results": True, "items": []})
        if "topic:agent-memory " in q else None,
    "a rejected query (422)":
        lambda q, p: (422, {}, {"message": "Validation Failed"}) if "topic:codex " in q else None,
    "a rate limit that never lifts":
        lambda q, p: (403, {"x-ratelimit-remaining": "0", "x-ratelimit-reset": "0"},
                      {"message": "API rate limit exceeded"}),
}
for label, fail in cases.items():
    sr, fake, _ = search(DAY2, fail)
    res = s.run(TODAY + timedelta(days=1), sr, log=quiet)
    true(f"{label}: the rising half reports the failure", "error" in res["rising"], str(res["rising"])[:200])
    true(f"{label}: ...and so does the list half", "error" in res["lists"], str(res["lists"])[:200])
    eq(f"{label}: both ledgers and the document are byte-identical", snapshot(), good)
    true(f"{label}: ...and nothing new was scouted", "acme/newcomer" not in s.load(s.REPOS, "repos")["repos"])

sr, fake, _ = search(DAY2, cases["incomplete_results on one query, every attempt"])
s.run(TODAY + timedelta(days=1), sr, log=quiet)
eq("an incomplete page is retried before it counts as a failure",
   sum(1 for q, p, _t in fake.calls if "topic:agent-memory " in q), s.RETRIES)
sr, fake, _ = search(DAY2, cases["a rejected query (422)"])
s.run(TODAY + timedelta(days=1), sr, log=quiet)
eq("a 422 is never retried", sum(1 for q, p, _t in fake.calls if "topic:codex " in q), 1)
true("...and stops the search there rather than carrying on",
     not any("topic:codex-cli " in q for q, _p, _t in fake.calls))

s.DOC.unlink()
sr, _, _ = search(DAY2, boom)
s.run(TODAY + timedelta(days=1), sr, log=quiet)
eq("a failed search on a cold cache re-renders the previous document from the ledger, not an empty one",
   snapshot(), good)

saved = snapshot()
sr, _, _ = search(DAY2, lambda q, p: boom(q, p) if "awesome in:name" in q else None)
res = s.run(TODAY + timedelta(days=1), sr, log=quiet)
true("the list half can fail alone", "error" in res["lists"] and "error" not in res["rising"])
true("...and the rising half still lands", "acme/newcomer" in s.load(s.REPOS, "repos")["repos"])
eq("...while the candidate ledger is byte-identical", s.LISTS.read_bytes(), saved[1])

reset()
sr, _, _ = search(DAY2, boom)
res = s.run(TODAY, sr, log=quiet)
eq("a first-ever run that fails writes an empty, valid document rather than none",
   [r["nwo"] for r in s.b10.parse(s.SCOUT, s.DOC.read_text(encoding="utf-8"))], [])

# ======================================================================================== the transport
group("the transport")
sr, fake, clock = search([repo(f"o/agent-{i}", topics=["ai-agents"]) for i in range(5)])
for q in ("topic:ai-agents a", "topic:ai-agents b", "topic:ai-agents c"):
    sr.all(q)
gaps = [b[2] - a[2] for a, b in zip(fake.calls, fake.calls[1:])]
true("requests are at least MIN_GAP apart", all(g >= s.MIN_GAP for g in gaps), str(gaps))

state = {"n": 0}


def limited(q, page):
    state["n"] += 1
    if state["n"] == 1:
        return 403, {"x-ratelimit-remaining": "0", "x-ratelimit-reset": str(clock.t + 30)}, \
            {"message": "API rate limit exceeded for user"}
    return None


sr, fake, clock = search([base], limited)
try:
    got = sr.page("topic:ai-agents x", 1)
except s.ScoutError as exc:
    got = {"items": [], "error": str(exc)}
eq("a rate limit is waited out and the request retried", [i["full_name"] for i in got["items"]],
   ["acme/taxbot"])
true("...waiting until the window resets", any(30 <= w <= s.MAX_WAIT for w in clock.slept), str(clock.slept))
state["n"] = 0


def secondary(q, page):
    state["n"] += 1
    if state["n"] == 1:
        return 403, {"retry-after": "12"}, {"message": "You have exceeded a secondary rate limit"}
    return None


sr, fake, clock = search([base], secondary)
try:
    sr.page("topic:ai-agents x", 1)
except s.ScoutError:
    pass
true("a secondary limit's Retry-After is honoured", 12 in clock.slept, str(clock.slept))


def spent(q, page):
    return 200, {"x-ratelimit-remaining": "0", "x-ratelimit-reset": str(clock.t + 40)}, \
        {"total_count": 0, "incomplete_results": False, "items": []}


sr, fake, clock = search([], spent)
sr.page("topic:ai-agents a", 1)
sr.page("topic:ai-agents b", 1)
true("a spent window is waited out before the next request, not after a 403",
     any(40 <= w <= s.MAX_WAIT for w in clock.slept), str(clock.slept))
eq("...and only once", len([w for w in clock.slept if w >= 40]), 1)

many = [repo(f"o{i}/agent-{i}", topics=["ai-agents"]) for i in range(250)]
sr, fake, _ = search(many)
eq("pagination collects every page", len(sr.all("topic:ai-agents q")), 250)
eq("...in three requests", len(fake.calls), 3)
huge = [repo(f"o{i}/agent-{i}", topics=["ai-agents"]) for i in range(1_150)]
logged = []
clock = Clock()
fake = Fake(huge, None, clock)
sr = s.Search(transport=fake, sleep=clock.sleep, clock=clock.time, log=logged.append)
eq("the 1,000-result ceiling stops at ten pages", (len(sr.all("topic:ai-agents q")), len(fake.calls)),
   (1_000, 10))
true("...and says what it could not reach", any("1,150 results" in x for x in logged), str(logged))

# ======================================================================================== candidates
group("candidates")
reset()
sr, _, _ = search(DAY1)
s.run(TODAY, sr, log=quiet)
cands = s.load(s.LISTS, "lists")["lists"]
eq("an awesome list is a candidate, with today as first seen", cands.get("acme/awesome-agent-tools"),
   {"stars": 400, "description": "A curated list of agent tools", "pushed_at": "2026-10-01",
    "first_seen": "2026-10-11"})
true("...and never a scouted repo", "acme/awesome-agent-tools" not in s.load(s.REPOS, "repos")["repos"])
later = TODAY + timedelta(days=9)
moved = [x for x in DAY2 if x["full_name"] != LIST["full_name"]] + [
    dict(LIST, stargazers_count=650, pushed_at="2026-10-19T00:00:00Z")]
sr, _, _ = search(moved)
s.run(later, sr, log=quiet)
cands = s.load(s.LISTS, "lists")["lists"]
eq("first_seen survives a later run", cands["acme/awesome-agent-tools"]["first_seen"], "2026-10-11")
eq("...while stars and last push are today's",
   (cands["acme/awesome-agent-tools"]["stars"], cands["acme/awesome-agent-tools"]["pushed_at"]),
   (650, "2026-10-19"))
eq("a list first seen today is dated today", cands["acme/awesome-mcp-picks"]["first_seen"], "2026-10-20")
text = s.LISTS.read_text(encoding="utf-8")
eq("the file is sorted and stable", text, s.dump(json.loads(text)))
keys = list(json.loads(text)["lists"])
eq("...keyed in order", keys, sorted(keys))

declined = {"version": 1, "lists": {}, "ignore": {"acme/awesome-agent-tools": "general-purpose, too broad"}}
s.merge_lists(declined, [LIST], TODAY, CURATED)
eq("a list under `ignore` is not a candidate", declined["lists"], {})

judge = lambda it, today=TODAY: s.list_verdict(it, today, CURATED)  # noqa: E731
eq("a SOURCES list is never a candidate", judge(repo("VoltAgent/awesome-agent-skills", topics=["agent-skills"])),
   "already a source")
eq("a list under the star bar is not", judge(dict(LIST, stargazers_count=199)), "below threshold")
eq("a list not pushed inside the window is not",
   judge(dict(LIST, pushed_at=f"{(TODAY - timedelta(days=s.LIST_PUSHED_DAYS + 1)).isoformat()}T00:00:00Z")),
   "stale")
eq("a list pushed on the window's first day is",
   judge(dict(LIST, pushed_at=f"{(TODAY - timedelta(days=s.LIST_PUSHED_DAYS)).isoformat()}T00:00:00Z")), "")
eq("a repo without 'awesome' in its name is not a list", judge(base), "not a list")
eq("a spam list is not", judge(dict(LIST, description="Awesome agents. Free download")), "spam")
eq("an archived list is not", judge(dict(LIST, archived=True)), "archived")
eq("an off-topic list is not", judge(repo("acme/awesome-css", topics=["css"], desc="Stylesheets")),
   "off-topic")

reset()
pool_only = repo("acme/awesome-agent-memory", stars=300, topics=["agent-memory"], desc="Memory for agents")
true("(fixture: that topic is a rising query and not a list query)",
     "agent-memory" in s.TOPICS and "agent-memory" not in s.LIST_TOPICS)
sr, _, _ = search([pool_only])
s.run(TODAY, sr, log=quiet)
true("a list only a rising query returned is a candidate too",
     "acme/awesome-agent-memory" in s.load(s.LISTS, "lists")["lists"])

lots = {f"o/awesome-{i:02d}": {"stars": 1000 + i, "description": f"list {i} | piped", "pushed_at": "2026-10-01",
                               "first_seen": "2026-10-11"} for i in range(30)}
md = s.summary({"added": [], "dropped": [], "moved": []}, {"added": ["o/awesome-29"], "dropped": []},
               {}, lots, {})
table = [ln for ln in md.splitlines() if ln.startswith("| [o/awesome-")]
eq("the summary lists the top fifteen candidates", len(table), 15)
true("...by stars, highest first", table[0].startswith("| [o/awesome-29]") and "(new)" in table[0], table[0])
true("...with a description's pipe escaped so the row stays one row", "list 29 \\| piped" in table[0], table[0])
fail_md = s.summary({"error": "HTTP 502"}, {"error": "not attempted"}, {"a/b": {}}, {}, {})
true("a failed search says so in the summary", "search failed, kept the previous 1" in fail_md, fail_md)

reset()
step = TMP / "step-summary.md"
keep = (s.Search, s.date, sys.argv, os.environ.get("GITHUB_STEP_SUMMARY"))


class FixedDate(date):
    @classmethod
    def today(cls):
        return TODAY


fixed_search = search(DAY1)[0]          # built before the patch, from the real class
s.Search = lambda: fixed_search
s.date = FixedDate
sys.argv = ["12_scout.py"]
os.environ["GITHUB_STEP_SUMMARY"] = str(step)
try:
    with contextlib.redirect_stdout(io.StringIO()):
        s.main()
finally:
    s.Search, s.date, sys.argv = keep[0], keep[1], keep[2]
    if keep[3] is None:
        os.environ.pop("GITHUB_STEP_SUMMARY", None)
    else:
        os.environ["GITHUB_STEP_SUMMARY"] = keep[3]
summ = step.read_text(encoding="utf-8") if step.exists() else ""
true("main() appends its summary to $GITHUB_STEP_SUMMARY", "### Scout" in summ, summ[:200])
true("...naming the candidate lists", "acme/awesome-agent-tools" in summ)

# ======================================================================================== the gate
group("the gate")
import watch_sources as ws  # noqa: E402
import pull_sources as ps  # noqa: E402

GATE = TMP / "gate"
(GATE / "sources").mkdir(parents=True)
ws.newness.PATH = GATE / "first-seen.json"
ws.b10.SRC = GATE / "sources"
ws.b10.CACHE = GATE
ws.ROOT = TMP                    # it prints the ledger's path relative to the repository
SCOUT_NWO = s.SCOUT["nwo"]
SCOUT_DOC = GATE / "sources" / s.SCOUT["file"]
asked: list[str] = []


def fake_head(nwo: str) -> str:
    asked.append(nwo)
    return f"{zlib.crc32(nwo.encode()):08x}" * 5        # forty hex characters, fixed per list


def watch(*argv) -> dict:
    out = GATE / "github-output"
    out.write_text("", encoding="utf-8")
    keep_head, keep_argv, keep_out = ws.head, sys.argv, os.environ.get("GITHUB_OUTPUT")
    ws.head, sys.argv = fake_head, ["watch_sources.py", *argv]
    os.environ["GITHUB_OUTPUT"] = str(out)
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            ws.main()
    finally:
        ws.head, sys.argv = keep_head, keep_argv
        if keep_out is None:
            os.environ.pop("GITHUB_OUTPUT", None)
        else:
            os.environ["GITHUB_OUTPUT"] = keep_out
    kv = dict(line.split("=", 1) for line in out.read_text(encoding="utf-8").splitlines() if "=" in line)
    return {"changed": kv.get("changed"), "moved": json.loads(kv.get("moved", "[]"))}


SET1 = s.render(A)
SCOUT_DOC.write_bytes(SET1.encode())
first = watch()
eq("the scout's first document is a move", first["changed"], "true")
true("...named among what moved", SCOUT_NWO in first["moved"])
watch("--update")
recorded = ws.newness.load()["sources"].get(SCOUT_NWO)
eq("--update records the document's digest where a commit id would go", recorded,
   ws.b10.content_digest(ws.SYNTHETIC[SCOUT_NWO]))
eq("after recording, nothing has moved", watch(), {"changed": "false", "moved": []})
SCOUT_DOC.write_bytes(s.render(json.loads(s.dump(A))).encode())
eq("the same set rendered again is not a move", watch()["changed"], "false")
SCOUT_DOC.write_bytes(SET1.replace("\n", "\r\n").encode())
eq("...nor is the same document in CRLF", watch()["changed"], "false")
grown = json.loads(s.dump(A))
grown["repos"]["acme/newcomer"] = {"id": 1, "section": "Coding Agents", "since": "2026-10-12"}
SCOUT_DOC.write_bytes(s.render(grown).encode())
eq("a different scouted set is a move, and only the scout moved", watch(),
   {"changed": "true", "moved": [SCOUT_NWO]})
SCOUT_DOC.write_bytes(SET1.encode())
SCOUT_DOC.unlink()
eq("a missing document is not a move", watch()["changed"], "false")
watch("--update")
eq("...and --update leaves the recorded digest alone", ws.newness.load()["sources"].get(SCOUT_NWO), recorded)
true("head() is never asked about the scout", SCOUT_NWO not in asked and len(asked) > 0, str(asked[-3:]))
eq("every curated list is still asked about", set(asked),
   {x["nwo"] for x in ws.b10.SOURCES if not x.get("synthetic")})

pull_state = {"version": 1, "sources": {}}
probed: list[str] = []
keep_head = ps.watch_sources.head
# None is "unreachable", the answer that makes pull_one stop before fetching anything -- so a pull_one
# that wrongly probed the scout records the probe here and still touches no network.
ps.watch_sources.head = lambda nwo: probed.append(nwo)
try:
    line = ps.pull_one(next(x for x in ps.b10.SOURCES if x.get("synthetic")), pull_state, force=True)
finally:
    ps.watch_sources.head = keep_head
eq("pull_sources leaves the synthetic source alone, even forced", (line["status"], pull_state),
   ("synthetic", {"version": 1, "sources": {}}))
eq("...without asking GitHub for its head commit", probed, [])

# ======================================================================================== downstream
group("downstream")
cur_row = {"source": "agents", "nwo": "acme/taxbot", "section": "Research", "kind": "repo"}
scout_row = {"source": "scout", "nwo": "acme/taxbot", "section": "Coding Agents", "kind": "repo"}
agg = tax.by_repo([cur_row, scout_row])
eq("a scouted listing does not out-vote a curator, even where it would win the tie",
   agg["acme/taxbot"]["category"], "Research & Data Agents")
true("(fixture: the scout's category is earlier in CATEGORIES, so a plain vote would have won)",
     tax.RANK["Coding Agents"] < tax.RANK["Research & Data Agents"])
eq("...though it is still a listing", agg["acme/taxbot"]["listings"], 2)
agg = tax.by_repo([dict(scout_row, nwo="acme/only")])
eq("a repo only the scout has takes the scout's section", agg["acme/only"]["category"], "Coding Agents")

spec16 = importlib.util.spec_from_file_location("b16_for_scout_test", SCRIPTS / "16_build_all.py")
b16 = importlib.util.module_from_spec(spec16)
sys.modules["b16_for_scout_test"] = b16
spec16.loader.exec_module(b16)
curated_rec = {"source": "agents", "nwo": "acme/taxbot", "kind": "repo", "blurb": "Files expenses.",
               "description": "Files expenses."}
scout_rec = {"source": "scout", "nwo": "acme/taxbot", "kind": "repo", "description": "",
             "blurb": "TaxBot is an open-source autonomous agent that files your expense reports for you"}
pool_rows = {r["nwo"]: r for r in b16.repo_pool([curated_rec, scout_rec], [], {})}
eq("a scouted listing does not replace a curator's blurb with a longer tagline",
   pool_rows["acme/taxbot"]["blurb"], "Files expenses.")
# The scout is a source, not a list. "Named by N lists" and the homepage's two-or-more picks are the
# consensus the site sells, and a search agreeing with a curator is not a second opinion.
eq("...and the scout does not count as a second list beside the curator",
   (pool_rows["acme/taxbot"]["sources"], pool_rows["acme/taxbot"]["list_count"]), ({"agents"}, 1))
eq("...or appear among the lists that name it", pool_rows["acme/taxbot"]["listed_by"], "agents")
alone = b16.repo_pool([dict(scout_rec, nwo="acme/alone")], [], {})[0]
eq("a repo only the scout found is in the pool, named by no list",
   (alone["nwo"], alone["list_count"], alone["listed_by"]), ("acme/alone", 0, ""))
eq("16_build_all's SYNTHETIC is exactly the sources SOURCES marks synthetic",
   set(b16.SYNTHETIC), {src["key"] for src in s.b10.SOURCES if src.get("synthetic")})
pool_rows = {r["nwo"]: r for r in b16.repo_pool([dict(curated_rec, blurb="", description=""), scout_rec],
                                                 [], {})}
eq("...but fills a blurb the curator left empty", pool_rows["acme/taxbot"]["blurb"], scout_rec["blurb"])
sub = {"source": "skills_voltagent", "nwo": "morluto/rea", "kind": "subpath", "blurb": "RE skill",
       "description": "RE skill", "name": "reverse-engineer-anything"}
full = {"source": "scout", "nwo": "morluto/rea", "kind": "repo", "description": "", "name": "rea",
        "blurb": "Reverse engineer anything with agents, from app behavior down to native binaries."}
row = b16.repo_pool([sub, full], [], {})[0]
eq("the motivating case: a curator's sub-folder row is promoted to the scout's full repo row",
   (row["kind"], row["name"], row["blurb"]), ("repo", "rea", "RE skill"))
eq("...and is still named by exactly the one list that cited it", (row["list_count"], row["listed_by"]),
   (1, "skills_voltagent"))

group("every surface counts curated lists only")
curated_n = sum(1 for src in s.b10.SOURCES if not src.get("synthetic"))
true("(fixture: the scout is configured, so SOURCES is one longer than the curated lists)",
     len(s.b10.SOURCES) == curated_n + 1)
for stage, text in (("19_pages.py", "LISTS = sum(1 for s in b16.b10.SOURCES if not s.get(\"synthetic\"))"),
                    ("17_markdown.py", "lists=len(per_source) - sum(1 for s in SOURCES if s.get(\"synthetic\")),")):
    true(f"{stage}'s list count leaves the scout out", text in (SCRIPTS / stage).read_text(encoding="utf-8"))
spec20 = importlib.util.spec_from_file_location("b20_for_scout_test", SCRIPTS / "20_landing.py")
b20 = importlib.util.module_from_spec(spec20)
sys.modules["b20_for_scout_test"] = b20
spec20.loader.exec_module(b20)
eq("the site's 'N awesome-lists' is the curated count", b20.LISTS, curated_n)
eq("a facet row with no list says where it came from instead of '0 lists'",
   [b20.lists_label(n) for n in (0, 1, 3)], ["found by search", "1 list", "3 lists"])
# The surfaces written in JavaScript or in f-strings too long to call here, by the words they print for 0.
for stage, words in (("19_pages.py", "was found by the atlas's GitHub search"), ("19_pages.py", '"GitHub search"'),
                     ("19_pages.py", '"found by search"'), ("22_detail.py", "No curated list names this project yet"),
                     ("19d_discover.py", '"found by search"'), ("30_v2.py", "No curated list names it yet"),
                     ("30_v2.py", "found by GitHub search")):
    true(f"{stage} has words for a repo no list names: {words}", words in (SCRIPTS / stage).read_text(encoding="utf-8"))
true("30_v2.py no longer turns a 0 into 1", '"lists") or 1' not in (SCRIPTS / "30_v2.py").read_text(encoding="utf-8"))

group("the wiring")
daily = (ROOT / ".github" / "workflows" / "daily.yml").read_text(encoding="utf-8").splitlines()
weekly = (ROOT / ".github" / "workflows" / "weekly.yml").read_text(encoding="utf-8").splitlines()


def at(lines, needle: str) -> int:
    """The first non-comment line containing `needle`, or -1."""
    return next((i for i, ln in enumerate(lines) if needle in ln and not ln.strip().startswith("#")), -1)


for name, lines in (("daily", daily), ("weekly", weekly)):
    scout_at = at(lines, "python scripts/12_scout.py")
    true(f"{name}: runs the scout", scout_at >= 0)
    true(f"{name}: ...after the cache is restored", at(lines, "Restore build cache") < scout_at)
    true(f"{name}: ...before 10_parse_sources reads its document",
         0 <= scout_at < at(lines, "python scripts/10_parse_sources.py"))
    true(f"{name}: ...and before its digest is recorded",
         scout_at < at(lines, "python scripts/watch_sources.py --update"))
true("daily: the scout runs before the watch step that gates the build on its digest",
     0 <= at(daily, "python scripts/12_scout.py") < at(daily, "run: python scripts/watch_sources.py"))
synth = [x for x in s.b10.SOURCES if x.get("synthetic")]
eq("SOURCES has exactly one synthetic source, the scout", [x["key"] for x in synth], ["scout"])
eq("...and it is last, so a curated listing of the same repo is always met first",
   s.b10.SOURCES[-1]["key"], "scout")
eq("...and its file is the document the stage writes", s.b10.source_path(synth[0]).name, s.DOC.name)

committed = ROOT / "state" / "scout-repos.json"
if committed.exists():
    led = json.loads(committed.read_text(encoding="utf-8"))
    secs = {e.get("section") for e in led["repos"].values()}
    eq("the committed ledger files every repo under a section the stage still names",
       secs - set(s.SECTIONS), set())
    true("...each with an ISO `since`",
         all(re.fullmatch(r"\d{4}-\d\d-\d\d", e.get("since") or "") for e in led["repos"].values()))
    eq("...and is stored in the stage's own sorted form", committed.read_text(encoding="utf-8")
       .replace("\r\n", "\n"), s.dump(led))
    parsed = s.b10.parse(s.SCOUT, s.render(led))
    eq("...and renders into rows the taxonomy maps without exception",
       sorted({(r["source"], r["category"]) for r in parsed} - set(tax.SECTIONS)), [])
else:
    true("state/scout-repos.json is committed", False)

print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
