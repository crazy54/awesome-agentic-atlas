"""Unit tests for the GitLab index: `scripts/hosts.py`, `gitlab_api.py`, `12b_gitlab.py`, `11b_fetch_gitlab.py`
and the places the rest of the pipeline takes a GitLab row in.

GitLab rows are the first rows in the atlas that are not GitHub's, so the risk is less in any one rule than
in a GitHub assumption somewhere downstream meeting a `gitlab.com/group/project` nwo and quietly doing the
wrong thing -- a GitHub social card for a repository GitHub has never heard of, a detail page at the wrong
depth, two scouts overwriting each other's ledger entry. Each assertion below is a fixture clean in every
respect but the one it is about, in `scout_test.py`'s manner. Nothing touches the network: the transport,
the clock and `sleep` are injected, and every path a stage writes is repointed into a scratch directory.

Groups:

  identity      -- `hosts`: which forge an nwo names, qualify/path/owner/name, every URL builder for both
                   forges, `from_url` on project, nested, folder, `.git` and reserved URLs, the flag.
  the parser    -- `10_parse_sources.repo_of` and `parse`: a gitlab.com link is a host-qualified repo row
                   with the flag on, and the website it always was with it off.
  the rules     -- `12b_gitlab.verdict` one exclusion at a time, the mirror tests, both bars at their
                   edges, sections from GitLab's free-text topics.
  the ledger    -- `merge`: sticky, unjudged projects change nothing, a quality failure drops, a move is
                   followed by id, `ignore`, candidate lists.
  the document  -- `render` is pure, parses into GitLab repo rows the taxonomy maps, and is empty with the
                   flag off.
  the sweep     -- rotation by day without a token, the budget, a rate limit ending the run, every query
                   with a token, a failed query contributing nothing.
  the client    -- pacing, a short 429 waited out, an hour-long one raised at once, a 404 never retried, a
                   5xx retried, pagination and the early stop.
  the fetch     -- `11b`: GitHub-shaped records, licence recognition, a refused batch changing nothing, the
                   last good answer standing in, a missing project recorded as gone.
  downstream    -- page paths and depths, image candidates, the dead-repo scan, the watch ledger key.
  the wiring    -- the flag ships off, the stages are in both workflows in order, taxonomy and buckets.

Run: python tests/gitlab_test.py
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import hosts  # noqa: E402
import gitlab_api as gl  # noqa: E402


def load(alias: str, name: str):
    spec = importlib.util.spec_from_file_location(alias, SCRIPTS / name)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[alias] = mod
    spec.loader.exec_module(mod)
    return mod


g = load("gitlab_scout_for_test", "12b_gitlab.py")
f = load("gitlab_fetch_for_test", "11b_fetch_gitlab.py")
b10 = g.sc.b10

TMP = Path(tempfile.mkdtemp(prefix="gitlab_test_", dir=os.environ.get("AAA_TMP") or None))
g.LEDGER = TMP / "state" / "gitlab-repos.json"
g.DOC = TMP / "cache" / "sources" / "gitlab.md"
g.DATA = TMP / "data.json"

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


class flag:
    """The `intake.gitlab` flag forced on or off for a block, whatever config/app-flags.json says."""

    def __init__(self, on: bool):
        self.on = on

    def __enter__(self):
        self.was = hosts._ENABLED
        hosts._ENABLED = self.on

    def __exit__(self, *exc):
        hosts._ENABLED = self.was


# ======================================================================================== identity
group("identity")
GH, GLN = "openai/codex", "gitlab.com/gitlab-org/ai/duo-workflow"
eq("a GitHub nwo is on github.com", hosts.host_of(GH), "github.com")
eq("a host-qualified nwo is on its host", hosts.host_of(GLN), "gitlab.com")
eq("...case-insensitively", hosts.host_of("GitLab.com/a/b"), "gitlab.com")
eq("a GitHub owner with a hyphen is still GitHub (no dot, no host)", hosts.host_of("open-ai/x"), "github.com")
true("is_github: yes for owner/repo", hosts.is_github(GH))
true("is_github: no for gitlab.com/...", not hosts.is_github(GLN))
eq("qualify is the identity on GitHub", hosts.qualify("github.com", "openai/codex"), GH)
eq("qualify prefixes any other host", hosts.qualify("gitlab.com", "/gitlab-org/ai/duo-workflow/"), GLN)
eq("path_of strips the host", hosts.path_of(GLN), "gitlab-org/ai/duo-workflow")
eq("path_of is the nwo on GitHub", hosts.path_of(GH), GH)
eq("owner_of is everything before the name (GitLab)", hosts.owner_of(GLN), "gitlab.com/gitlab-org/ai")
eq("owner_of on GitHub is the owner", hosts.owner_of(GH), "openai")
eq("name_of is the last segment", (hosts.name_of(GLN), hosts.name_of(GH)), ("duo-workflow", "codex"))
eq("owner_of + name_of rebuild the nwo", f"{hosts.owner_of(GLN)}/{hosts.name_of(GLN)}", GLN)
eq("web_url, GitLab", hosts.web_url(GLN), "https://gitlab.com/gitlab-org/ai/duo-workflow")
eq("web_url, GitHub", hosts.web_url(GH), "https://github.com/openai/codex")
eq("clone_url, GitLab", hosts.clone_url(GLN), "https://gitlab.com/gitlab-org/ai/duo-workflow.git")
eq("raw_base, GitLab, uses /-/raw/", hosts.raw_base(GLN, "main"),
   "https://gitlab.com/gitlab-org/ai/duo-workflow/-/raw/main/")
eq("raw_base, GitHub, is raw.githubusercontent.com", hosts.raw_base(GH, ""),
   "https://raw.githubusercontent.com/openai/codex/HEAD/")
eq("blob_base, GitLab", hosts.blob_base(GLN), "https://gitlab.com/gitlab-org/ai/duo-workflow/-/blob/HEAD/")
eq("blob_base, GitHub", hosts.blob_base(GH, "dev"), "https://github.com/openai/codex/blob/dev/")
eq("tree_url, GitLab", hosts.tree_url(GLN, "main", "/docs/"),
   "https://gitlab.com/gitlab-org/ai/duo-workflow/-/tree/main/docs")
eq("a GitHub repo has a social card", hosts.social_card(GH), "https://opengraph.githubassets.com/1/openai/codex")
eq("a GitLab project has none", hosts.social_card(GLN), "")
eq("label", (hosts.label(GH), hosts.label(GLN)), ("GitHub", "GitLab"))
true("README cache files never collide across forges",
     hosts.readme_file("gitlab.com/openai/codex") != hosts.readme_file(GH)
     and "/" not in hosts.readme_file(GLN))
eq("quote_path encodes the path as one segment", hosts.quote_path(GLN), "gitlab-org%2Fai%2Fduo-workflow")

with flag(True):
    eq("from_url: a project", hosts.from_url("https://gitlab.com/fforster/gitlab-mcp"),
       ("gitlab.com/fforster/gitlab-mcp", ""))
    eq("from_url: a nested project", hosts.from_url("https://gitlab.com/gitlab-org/ai/duo-workflow/"),
       (GLN, ""))
    eq("from_url: a folder inside a project is the project plus its rest",
       hosts.from_url("https://gitlab.com/a/b/-/tree/main/skills/x"), ("gitlab.com/a/b", "tree/main/skills/x"))
    eq("from_url: .git is dropped", hosts.from_url("https://gitlab.com/a/b.git"), ("gitlab.com/a/b", ""))
    eq("from_url: a query string is dropped", hosts.from_url("https://gitlab.com/a/b?tab=readme"),
       ("gitlab.com/a/b", ""))
    eq("from_url: www. is accepted", hosts.from_url("https://www.gitlab.com/a/b"), ("gitlab.com/a/b", ""))
    eq("from_url: gitlab.com's own pages are not projects", hosts.from_url("https://gitlab.com/explore/projects"),
       None)
    eq("from_url: a user or group page alone is not a project", hosts.from_url("https://gitlab.com/fforster"), None)
    eq("from_url: about.gitlab.com is not gitlab.com", hosts.from_url("https://about.gitlab.com/gitlab-duo/"),
       None)
    eq("from_url: GitHub is not this function's", hosts.from_url("https://github.com/a/b"), None)
with flag(False):
    eq("from_url says None for everything while the flag is off",
       hosts.from_url("https://gitlab.com/fforster/gitlab-mcp"), None)
    eq("...unless forced", hosts.from_url("https://gitlab.com/a/b", force=True), ("gitlab.com/a/b", ""))

# ======================================================================================== the parser
group("the parser")
with flag(True):
    eq("repo_of: a gitlab.com project is (host+namespace, name, rest)",
       b10.repo_of("https://gitlab.com/gitlab-org/ai/duo-workflow"), ("gitlab.com/gitlab-org/ai", "duo-workflow", ""))
    eq("repo_of: GitHub is unchanged", b10.repo_of("https://github.com/openai/codex"), ("openai", "codex", ""))
    src = dict(key="mcp_x", nwo="someone/awesome-mcp", mode={"bullet"}, cat_at=2)
    rows = b10.parse(src, "## Servers\n\n- [gitlab-mcp](https://gitlab.com/fforster/gitlab-mcp) - MCP for GitLab\n"
                          "- [skills](https://gitlab.com/a/b/-/tree/main/skills) - a folder\n")
    eq("a curated gitlab.com link becomes a repo row with a host-qualified nwo",
       [(r["kind"], r["nwo"], r["owner"], r["repo"]) for r in rows],
       [("repo", "gitlab.com/fforster/gitlab-mcp", "gitlab.com/fforster", "gitlab-mcp"),
        ("subpath", "gitlab.com/a/b", "gitlab.com/a", "b")])
with flag(False):
    rows = b10.parse(src, "## Servers\n\n- [gitlab-mcp](https://gitlab.com/fforster/gitlab-mcp) - MCP\n")
    eq("with the flag off it is the website it always was", [(r["kind"], r["nwo"], r["website"]) for r in rows],
       [("site", "", "https://gitlab.com/fforster/gitlab-mcp")])

# ======================================================================================== the rules
group("the rules")
TODAY = date(2026, 11, 18)
INDEXED = {"openai/codex": "openai/codex", "acme/agentkit": "acme/AgentKit"}


def proj(path: str, stars: int = 40, desc: str = "An MCP server for your issue tracker", topics=("mcp",),
         pushed: str = "2026-11-01", created: str = "2025-03-01", **kw) -> dict:
    """One project as `12b_gitlab.item` + `enrich` leave it: clean unless a keyword says otherwise."""
    it = g.item({"id": abs(hash(path)) % 10 ** 9, "path_with_namespace": path, "path": path.rsplit("/", 1)[-1],
                 "name": path.rsplit("/", 1)[-1], "description": desc, "star_count": stars,
                 "created_at": f"{created}T00:00:00Z", "last_activity_at": f"{pushed}T00:00:00Z",
                 "topics": list(topics)})
    it.update(fork=False, archived=False, import_status="none", readme="# tool\n\nIt does things.\n")
    it.update(kw)
    return it


def verdict(it, today=TODAY):
    return g.verdict(it, today, INDEXED)


base = proj("tracker/mcp-tracker")
eq("the clean fixture qualifies", verdict(base), "")
eq("a fork is excluded", verdict(dict(base, fork=True)), "fork")
eq("an archived project is excluded", verdict(dict(base, archived=True)), "archived")
eq("a mirror that says so in its description", verdict(dict(base, description="Mirror of the GitHub MCP tool")),
   "mirror")
eq("a mirror that says so in its README's opening", verdict(dict(
    base, readme="# tool\n\nThis is a read-only mirror of https://github.com/acme/tool, please file issues there.")),
   "mirror")
eq("...but not for a github.com link far down the README", verdict(dict(
    base, readme="# tool\n\n" + "words " * 400 + "\nmirrored from github.com/acme/tool")), "")
eq("a project whose owner/name is an indexed GitHub repo is its twin",
   verdict(proj("openai/codex", desc="Codex, the coding agent")), "mirror")
eq("...the last two segments of a nested path count", verdict(proj("mirrors/acme/agentkit", desc="agent kit")),
   "mirror")
eq("...and a README pointing at an indexed GitHub repo of the same name",
   verdict(proj("someone/agentkit", desc="An agent kit", readme="See https://github.com/acme/AgentKit for docs")),
   "mirror")
eq("...but a README naming an indexed repo of another name is not", verdict(dict(
    base, readme="Built on https://github.com/openai/codex")), "")
eq("mirror_of names the GitHub side", g.mirror_of(proj("openai/codex", desc="x"), INDEXED), "openai/codex")
eq("no description is excluded", verdict(dict(base, description="")), "no description")
eq("spam is excluded (the scout's own rule)", verdict(dict(base, description="Agent tool free download: setup.exe")),
   "spam")
eq("an awesome list is a list, not a project", verdict(proj("x/awesome-mcp", desc="A list of MCP servers")), "list")
eq("topics alone are not evidence", verdict(proj("x/pg-helper", desc="Postgres helper scripts", topics=("ai-agents",))),
   "off-topic")
eq("GitLab's display name counts as the name", verdict(proj("x/tool", desc="Postgres helpers", title="Agent Tool")),
   "")
edge = (TODAY - timedelta(days=g.ACTIVE_DAYS)).isoformat()
eq("the active bar: the floor, active on the window's first day", verdict(dict(
    base, stargazers_count=g.STARS, pushed_at=edge)), "")
eq("...one star short", verdict(dict(base, stargazers_count=g.STARS - 1)), "below threshold")
eq("...quiet for one day too long, and under the core bar", verdict(dict(
    base, stargazers_count=g.CORE_STARS - 1, pushed_at=(TODAY - timedelta(days=g.ACTIVE_DAYS + 1)).isoformat())),
   "below threshold")
eq("the core bar keeps a quiet project with enough stars", verdict(dict(
    base, stargazers_count=g.CORE_STARS, pushed_at="2024-01-01")), "")
eq("...but not one from before ERA", verdict(dict(
    base, stargazers_count=g.CORE_STARS, pushed_at="2024-01-01", created_at="2022-12-31T00:00:00Z")),
   "below threshold")
eq("GitLab's topic spellings are normalised", g.item({"topics": ["MCP Server", "Agent_Skills", "LLMs"]})["topics"],
   ["agent-skills", "llms", "mcp-server"])
eq("the section is the scout's, read off normalised topics", g.section_of(proj("x/y", topics=("MCP-server",))),
   "MCP Servers")
eq("...and the scout's fallback for no family", g.section_of(proj("x/y", topics=())), "Assistants & Domain Agents")
eq("a list worth a look", g.list_verdict(proj("x/awesome-agents", desc="Awesome AI agents"), INDEXED), "")
eq("...below the list bar", g.list_verdict(proj("x/awesome-agents", stars=g.LIST_STARS - 1, desc="Awesome agents"),
                                           INDEXED), "below threshold")

# ======================================================================================== the ledger
group("the ledger")
led = {"version": 1, "repos": {}, "lists": {}}
a, b = proj("tracker/mcp-tracker"), proj("team/agent-runner", desc="Runs agents in CI", topics=("ai-agents",))
rep = g.merge(led, {a["full_name"]: a, b["full_name"]: b}, TODAY, INDEXED)
eq("two clean projects are added", sorted(rep["added"]), ["team/agent-runner", "tracker/mcp-tracker"])
eq("...each with its section and today's date", led["repos"]["tracker/mcp-tracker"],
   {"id": a["id"], "section": "MCP Servers", "since": "2026-11-18"})
rep = g.merge(led, {}, TODAY + timedelta(days=30), INDEXED)
eq("absence is not evidence: a run that found nothing keeps everything", sorted(led["repos"]),
   ["team/agent-runner", "tracker/mcp-tracker"])
quiet = dict(a, stargazers_count=1, pushed_at="2020-01-01")
rep = g.merge(led, {a["full_name"]: quiet}, TODAY, INDEXED)
eq("falling below a bar is not a reason to leave", "tracker/mcp-tracker" in led["repos"], True)
unread = dict(a, fork=None, archived=True)
rep = g.merge(led, {a["full_name"]: unread}, TODAY, INDEXED)
eq("a project enrich could not answer for is judged on nothing", (rep["unjudged"], "tracker/mcp-tracker" in led["repos"]),
   (1, True))
eq("prejudge: a project that could qualify needs enriching", g.prejudge(a, TODAY), "")
eq("prejudge: one with no agentic word does not", g.prejudge(proj("x/pg-scripts", desc="Postgres scripts"), TODAY),
   "off-topic")
true("only what could qualify is sent to enrich (the anonymous budget's main saving)",
     g.prejudge(dict(a, stargazers_count=0), TODAY) == "below threshold")
rep = g.merge(led, {a["full_name"]: dict(a, archived=True)}, TODAY, INDEXED)
eq("a quality failure observed this run drops it", rep["dropped"], [("tracker/mcp-tracker", "archived")])
eq("prejudge: an agentic name with no description is worth enriching (its README may say what it is)",
   g.prejudge(dict(a, description=""), TODAY), "")
rep = g.merge(led, {b["full_name"]: dict(b, fork=None, description="", stargazers_count=0)}, TODAY, INDEXED)
eq("...and so does one prejudge alone can see, with no enrichment at all", rep["dropped"],
   [("team/agent-runner", "no description")])
led2 = {"version": 1, "repos": {"old/path": {"id": 7, "section": "MCP Servers", "since": "2026-01-01"}}, "lists": {}}
moved = dict(proj("new/path"), id=7)
rep = g.merge(led2, {"new/path": moved}, TODAY, INDEXED)
eq("a moved project is followed by id and keeps its since", (rep["renamed"], led2["repos"]["new/path"]["since"]),
   ([("old/path", "new/path")], "2026-01-01"))
led3 = {"version": 1, "repos": {"x/y": {"id": 1, "section": "MCP Servers", "since": "2026-01-01"}}, "lists": {},
        "ignore": {"x/y": "not agentic, on inspection", "z/w": "spam"}}
rep = g.merge(led3, {"z/w": proj("z/w")}, TODAY, INDEXED)
eq("the ignore key removes and keeps out", (sorted(led3["repos"]), rep["added"]), ([], []))
true("...and survives the merge", "ignore" in led3)
lst = proj("x/awesome-agents", desc="Awesome AI agents")
g.merge(led, {lst["full_name"]: lst}, TODAY, INDEXED)
eq("a candidate list is recorded, not scouted", ("x/awesome-agents" in led["lists"], "x/awesome-agents" in led["repos"]),
   (True, False))
g.merge(led, {}, TODAY + timedelta(days=1), INDEXED)
true("...and is sticky: a slice without the awesome search keeps it", "x/awesome-agents" in led["lists"])

# ======================================================================================== the document
group("the document")
doc_led = {"version": 1, "lists": {}, "repos": {
    "tracker/mcp-tracker": {"id": 1, "section": "MCP Servers", "since": "2026-11-18"},
    "gitlab-org/ai/duo-workflow": {"id": 2, "section": "Coding Agents", "since": "2026-11-17"},
    "Zeta/Agent-Runner": {"id": 3, "section": "Assistants & Domain Agents", "since": "2026-11-16"}}}
text = g.render(doc_led)
eq("render is a pure function of the ledger, in any insertion order",
   g.render({"repos": dict(reversed(list(doc_led["repos"].items())))}), text)
true("no dates and no star counts in the document", "2026" not in text and "stars" not in text.lower())
with flag(True):
    gsrc = next(s for s in b10.SOURCES if s["key"] == "gitlab") if any(s["key"] == "gitlab" for s in b10.SOURCES) \
        else dict(key="gitlab", nwo="crazy54/awesome-agentic-atlas", mode={"bullet"}, cat_at=2, synthetic=True)
    parsed = b10.parse(gsrc, text)
eq("it parses into one GitLab repo row per project, in its section",
   sorted((r["kind"], r["nwo"], r["category"]) for r in parsed),
   [("repo", "gitlab.com/Zeta/Agent-Runner", "Assistants & Domain Agents"),
    ("repo", "gitlab.com/gitlab-org/ai/duo-workflow", "Coding Agents"),
    ("repo", "gitlab.com/tracker/mcp-tracker", "MCP Servers")])
tax = g.sc.b10  # noqa: F841  (the taxonomy is imported below)
import taxonomy  # noqa: E402
eq("...whose sections the taxonomy maps", sorted({(r["source"], r["category"]) for r in parsed} - set(taxonomy.SECTIONS)),
   [])
eq("with the flag off the document is the heading alone", g.render(doc_led, on=False).count("- ["), 0)
g.write_doc(doc_led, on=True)
eq("write_doc writes LF bytes, and a second write is a no-op", (g.DOC.read_bytes().count(b"\r"), g.write_doc(doc_led, on=True)),
   (0, False))

# ======================================================================================== the sweep
group("the sweep")


class FakeClient:
    """Answers every query from a table; records the order; can refuse from the nth request on."""

    def __init__(self, token=None, refuse_from=None, fail=()):
        self.token, self.refuse_from, self.fail = token, refuse_from, set(fail)
        self.requests = self.cached = 0
        self.asked = []

    def pages(self, path, until=None, max_pages=20, **params):
        self.requests += 1
        key = params.get("search") or params.get("topic")
        self.asked.append((path, key))
        if self.refuse_from is not None and self.requests >= self.refuse_from:
            raise gl.GitLabError("rate limited by unauthenticated_traffic_per_ip for 40 more minutes")
        if key in self.fail:
            raise gl.GitLabError("HTTP 500 for x after 4 attempts")
        if path == "/topics":
            return [{"name": "MCP-server", "total_projects_count": 101}] if key == "mcp" else []
        return [{"id": 9, "path_with_namespace": f"found/{key.replace(' ', '-')}", "path": "p", "name": "p",
                 "description": "an agent", "star_count": 9, "topics": []}]


plan = g.queries()
day = date(2026, 11, 20)
c = FakeClient()
found, sw = g.sweep(c, day, everything=False, budget=5, log=lambda m: None)
eq("anonymous: the rotation starts at today's offset", c.asked[0][1], plan[day.toordinal() % len(plan)][1])
eq("...and stops once the budget is spent", c.requests, 5)
c2 = FakeClient()
g.sweep(c2, day + timedelta(days=1), everything=False, budget=5, log=lambda m: None)
eq("...and the next day starts one query further on", c2.asked[0][1], plan[(day.toordinal() + 1) % len(plan)][1])
c = FakeClient(token="t")
found, sw = g.sweep(c, day, everything=False, log=lambda m: None)
eq("with a token every query runs, from the first", (c.asked[0][1], sw["left"]), (plan[0][1], 0))
true("...including one topic query per spelling the lookups found", ("/projects", "MCP-server") in c.asked)
eq("known topic spellings are in the rotation itself, not only after a lookup",
   g.queries({"MCP-server": 101, "ai-agents": 311})[-2:], [("topic", "ai-agents"), ("topic", "MCP-server")])
c = FakeClient(token="t")
found, sw = g.sweep(c, day, everything=True, log=lambda m: None, known={"ai-agents": 311})
eq("...and a spelling found this run is queried once, beside the known ones",
   sorted(k for p_, k in c.asked if p_ == "/projects" and k in ("ai-agents", "MCP-server")), ["MCP-server", "ai-agents"])
eq("...and reported for the ledger", sw["spellings"], {"ai-agents": 311, "MCP-server": 101})
c = FakeClient(token="t", refuse_from=3)
found, sw = g.sweep(c, day, everything=True, log=lambda m: None)
eq("a rate limit ends the run at once rather than asking again", (c.requests, len(sw["failed"])), (3, 1))
c = FakeClient(token="t", fail={"agent"})
found, sw = g.sweep(c, day, everything=True, log=lambda m: None)
true("a failed query contributes nothing and the rest still run",
     "found/agent" not in found and "found/mcp" in found
     and sw["failed"] and all(arg == "agent" for _k, arg, _w in sw["failed"]))

for md, want in (("# Lazy MCP\n\n[![ci](https://b/x.svg)](https://c)\n\nLoads MCP servers on demand, for agents.\n",
                  "Loads MCP servers on demand, for agents."),
                 ("<div align=center>\n<img src=x>\n</div>\n\n**An [agent](https://x) runner** for CI\n",
                  "An agent runner for CI"),
                 ("```\npip install a-long-enough-name\n```\n| a | table |\nThe actual sentence here.",
                  "The actual sentence here."),
                 ("# Title only\n\n## Install\n", "")):
    eq(f"readme_summary: {want or 'nothing'}", gl.readme_summary(md), want)


class EnrichClient:
    token = "t"

    def graphql(self, q, v):
        return {"projects": {"nodes": [{"fullPath": "x/claude-modular", "archived": False, "isForked": False,
                                        "importStatus": "none", "repository": {"blobs": {"nodes": [
                                            {"rawTextBlob": "# claude-modular\n\nModular Claude Code agent configs."}]}}}]}}


nodesc = proj("x/claude-modular", desc="")
g.enrich(EnrichClient(), [nodesc], log=lambda m: None)
eq("enrich gives a project with no description its README's first line", nodesc["description"],
   "Modular Claude Code agent configs.")
eq("...which then qualifies on it", verdict(nodesc), "")

# ======================================================================================== the client
group("the client")


class Clock:
    def __init__(self):
        self.t = 1000.0
        self.slept = []

    def __call__(self):
        return self.t

    def sleep(self, s):
        self.slept.append(round(s, 2))
        self.t += s


def client_with(answers, **kw):
    clock = Clock()
    sent = []

    def transport(method, url, body, headers):
        sent.append((method, url, headers))
        a = answers.pop(0)
        if isinstance(a, Exception):
            raise a
        return a
    c = gl.Client(transport=transport, sleep=clock.sleep, clock=clock, cache=None, token=kw.get("token", ""),
                  log=lambda m: None)
    return c, clock, sent


ok200 = (200, {"ratelimit-remaining": "400"}, b"[]")
c, clock, sent = client_with([ok200, ok200, ok200])
c.get("/projects", search="a")
c.get("/projects", search="b")
c.get("/topics", search="c")
true("projects-list requests are spaced LIST_GAP apart", gl.LIST_GAP in clock.slept, str(clock.slept))
eq("...and others only MIN_GAP", clock.slept[-1], round(gl.MIN_GAP, 2))
eq("an anonymous client sends no token", "PRIVATE-TOKEN" in sent[0][2], False)
c, clock, sent = client_with([ok200], token="glpat-x")
c.get("/topics")
eq("a token is sent as PRIVATE-TOKEN", sent[0][2].get("PRIVATE-TOKEN"), "glpat-x")
c, clock, sent = client_with([(429, {"retry-after": "7"}, b""), ok200])
c.get("/topics")
eq("a short 429 is waited out and retried", (7.0 in clock.slept, len(sent)), (True, 2))
c, clock, sent = client_with([(429, {"retry-after": "2826", "ratelimit-name": "unauthenticated_traffic_per_ip"}, b"")])
try:
    c.get("/topics")
    true("an hour-long 429 raises at once", False)
except gl.GitLabError as exc:
    true("an hour-long 429 raises at once, naming the limit", "unauthenticated_traffic_per_ip" in str(exc)
         and len(sent) == 1 and not any(s > gl.MAX_WAIT for s in clock.slept), str(exc))
c, clock, sent = client_with([(404, {}, b'{"message":"404 Project Not Found"}')])
try:
    c.get("/projects/x")
    true("a 404 raises", False)
except gl.GitLabError as exc:
    true("a 404 raises without a retry", "HTTP 404" in str(exc) and len(sent) == 1)
c, clock, sent = client_with([(502, {}, b""), ok200])
c.get("/topics")
eq("a 5xx is retried", len(sent), 2)
c, clock, sent = client_with([gl.GitLabError("no answer"), gl.GitLabError("no answer"),
                              gl.GitLabError("no answer"), gl.GitLabError("no answer")])
try:
    c.get("/topics")
    true("a transport that never answers raises after RETRIES", False)
except gl.GitLabError:
    eq("a transport that never answers raises after RETRIES", len(sent), gl.RETRIES)
p1 = (200, {"x-next-page": "2"}, json.dumps([{"star_count": 9}, {"star_count": 8}]).encode())
p2 = (200, {"x-next-page": ""}, json.dumps([{"star_count": 7}, {"star_count": 2}]).encode())
c, clock, sent = client_with([p1, p2])
eq("pages follows X-Next-Page and stops at `until`",
   [i["star_count"] for i in c.pages("/projects", until=lambda i: i["star_count"] < 5)], [9, 8, 7])
c, clock, sent = client_with([(200, {}, json.dumps({"errors": [{"message": "complexity"}]}).encode())])
try:
    c.graphql("{ x }")
    true("a GraphQL answer that is all errors raises", False)
except gl.GitLabError:
    true("a GraphQL answer that is all errors raises", True)
tmpc = TMP / "http"
cc = gl.Client(transport=lambda *a: ok200, sleep=lambda s: None, cache=tmpc, ttl=0, token="", log=lambda m: None)
cc.get("/topics")
eq("with no ttl nothing is written to the response cache (a build's case)", list(tmpc.rglob("*.json")), [])
cc.ttl = 3600
cc.get("/topics")
cc.get("/topics")
eq("with a ttl the second identical read is answered from it", (cc.requests, cc.cached), (2, 1))

# ======================================================================================== the fetch
group("the fetch")
node = {"fullPath": "Team/Agent-Runner", "description": " Runs agents ", "starCount": 12, "forksCount": 3,
        "archived": False, "isForked": False, "createdAt": "2025-01-02T00:00:00Z",
        "lastActivityAt": "2026-11-10T00:00:00Z", "topics": ["ai-agents", "MCP Server"],
        "webUrl": "https://gitlab.com/Team/Agent-Runner", "avatarUrl": "https://gitlab.com/uploads/a.png",
        "languages": [{"name": "Go", "share": 30.0}, {"name": "Python", "share": 70.0}],
        "repository": {"rootRef": "main", "blobs": {"nodes": [
            {"path": "README.md", "rawTextBlob": "# Agent Runner"},
            {"path": "LICENSE", "rawTextBlob": "Apache License\n Version 2.0, January 2004"}]}}}
rec, readme = f.record(node)
eq("the record is GitHub-shaped", {k: rec[k] for k in ("nameWithOwner", "stargazerCount", "forkCount", "isFork",
                                                       "isArchived", "pushedAt", "defaultBranchRef")},
   {"nameWithOwner": "gitlab.com/Team/Agent-Runner", "stargazerCount": 12, "forkCount": 3, "isFork": False,
    "isArchived": False, "pushedAt": "2026-11-10T00:00:00Z", "defaultBranchRef": {"name": "main"}})
eq("...the primary language is the largest share", rec["primaryLanguage"], {"name": "Python"})
eq("...topics in GitHub's nesting", rec["repositoryTopics"]["nodes"][1], {"topic": {"name": "MCP Server"}})
eq("...the licence is recognised from its text", rec["licenseInfo"]["spdxId"], "Apache-2.0")
eq("...the README comes back beside it", readme, "# Agent Runner")
eq("...and the GitLab-only fields are kept", (rec["host"], rec["avatarUrl"] != ""), ("gitlab.com", True))
for text_, want in (("MIT License\n\nPermission is hereby granted, free of charge, to any person", "MIT"),
                    ("GNU AFFERO GENERAL PUBLIC LICENSE\n Version 3 ... GNU GENERAL PUBLIC LICENSE", "AGPL-3.0"),
                    ("GNU LESSER GENERAL PUBLIC LICENSE\n                       Version 3, 29 June 2007", "LGPL-3.0"),
                    ("GNU GENERAL PUBLIC LICENSE\n                       Version 2, June 1991", "GPL-2.0"),
                    ("Redistribution and use in source and binary forms ... Neither the name of", "BSD-3-Clause"),
                    ("Redistribution and use in source and binary forms, with or without", "BSD-2-Clause"),
                    ("Mozilla Public License Version 2.0", "MPL-2.0"),
                    ("This is free and unencumbered software released into the public domain.", "Unlicense"),
                    ("All rights reserved by Acme.", "NOASSERTION")):
    eq(f"license_of: {want}", (f.license_of(text_) or {}).get("spdxId"), want)
eq("license_of: no file is no licence", f.license_of(""), None)
eq("wanted: distinct GitLab rows only, first-listed order",
   f.wanted([{"nwo": "openai/codex"}, {"nwo": "gitlab.com/a/b"}, {"nwo": "gitlab.com/A/B"}, {"nwo": "gitlab.com/c/d"}]),
   ["gitlab.com/a/b", "gitlab.com/c/d"])


class GQL:
    def __init__(self, answers):
        self.answers, self.requests, self.token = answers, 0, None

    def graphql(self, q, v):
        self.requests += 1
        a = self.answers.pop(0)
        if isinstance(a, Exception):
            raise a
        return a


n2 = dict(node, fullPath="c/d")
got, rd, missing = f.fetch(GQL([{"projects": {"nodes": [node, n2]}}]),
                           ["gitlab.com/team/agent-runner", "gitlab.com/c/d", "gitlab.com/gone/x"], log=lambda m: None)
eq("a project the batch answered is fetched (matched case-insensitively)", sorted(got),
   ["gitlab.com/c/d", "gitlab.com/team/agent-runner"])
eq("one an answered batch did not contain is missing", missing, {"gitlab.com/gone/x"})
got, rd, missing = f.fetch(GQL([gl.GitLabError("rate limited by x for 30 more minutes")]),
                           ["gitlab.com/a/b"], log=lambda m: None)
eq("a refused batch contributes to nothing", (got, missing), ({}, set()))

# main(), against scratch files: the last good answer stands in for a refused read.
f.ENTRIES, f.META, f.READMES, f.LAST_GOOD = (TMP / "entries_all.json", TMP / "meta.json", TMP / "readmes",
                                             TMP / "gitlab" / "meta.json")
f.ENTRIES.write_text(json.dumps([{"nwo": "gitlab.com/a/b"}, {"nwo": "gitlab.com/new/one"},
                                 {"nwo": "openai/codex"}]), encoding="utf-8")
f.META.write_text(json.dumps({"openai/codex": {"stargazerCount": 1}}), encoding="utf-8")
f.LAST_GOOD.parent.mkdir(parents=True, exist_ok=True)
f.LAST_GOOD.write_text(json.dumps({"gitlab.com/a/b": {"nameWithOwner": "gitlab.com/a/b", "stargazerCount": 5}}),
                       encoding="utf-8")


class RefusingClient:
    def __init__(self, *a, **kw):
        self.requests, self.token = 0, None

    def graphql(self, q, v):
        self.requests += 1
        raise gl.GitLabError("rate limited by unauthenticated_traffic_per_ip for 50 more minutes")


real_client, f.gl.Client = f.gl.Client, RefusingClient
argv, sys.argv = sys.argv, ["11b_fetch_gitlab.py"]
try:
    import contextlib
    import io
    with contextlib.redirect_stdout(io.StringIO()):
        f.main()
finally:
    f.gl.Client, sys.argv = real_client, argv
meta = json.loads(f.META.read_text(encoding="utf-8"))
eq("refused: a project read before keeps its last good answer", meta.get("gitlab.com/a/b", {}).get("stargazerCount"), 5)
eq("...one never read is absent (and 14_classify_all leaves it out)", "gitlab.com/new/one" in meta, False)
eq("...and the GitHub records are untouched", meta.get("openai/codex"), {"stargazerCount": 1})

# ======================================================================================== downstream
group("downstream")
b22 = load("detail_for_gitlab_test", "22_detail.py")
b20 = sys.modules.get("b20") or load("landing_for_gitlab_test", "20_landing.py")
eq("repo_path: GitHub is the two-segment path it always was", b20.repo_path("OpenAI/Codex"), "repo/openai/codex/")
eq("repo_path: GitLab is host and every segment", b20.repo_path(GLN), "repo/gitlab.com/gitlab-org/ai/duo-workflow/")
row = {"nwo": GLN, "name": "duo-workflow", "img": "", "url": hosts.web_url(GLN)}
rp, rg = b22.Repo(row, TMP / "docs"), b22.Repo(dict(row, nwo="openai/codex"), TMP / "docs")
eq("Repo.parts: one segment per nwo segment", rp.parts, ["repo", "gitlab.com", "gitlab-org", "ai", "duo-workflow"])
eq("...and agrees with repo_path", "/".join(rp.parts) + "/", b20.repo_path(GLN))
eq("rel climbs to docs/ from any depth", (rp.rel(), rg.rel()), ("../../../../../", "../../../"))
eq("up climbs to docs/repo/, where detail.css lives", (rp.up("detail.css"), rg.up("detail.css")),
   ("../../../../detail.css", "../../detail.css"))
eq("kin_href from a deep page to a shallow one", rp.kin_href(rg), "../../../../openai/codex/")
eq("kin_href from a shallow page to a deep one", rg.kin_href(rp), "../../gitlab.com/gitlab-org/ai/duo-workflow/")
eq("a GitLab page with no picture has no shot (and so no GitHub card)", rp.shot, "")
eq("a GitHub page with no picture has its social card", rg.shot, "https://opengraph.githubassets.com/1/openai/codex")
eq("the page knows its forge", (rp.forge, rp.github, rg.forge), ("GitLab", False, "GitHub"))

c4 = load("classify_for_gitlab_test", "04_classify.py")
shots = c4.shot_candidates("![demo](docs/demo.png)\n![shot](/uploads/abc123/screen.png)\n"
                           "![b](https://gitlab.com/a/b/-/blob/main/x.jpg)",
                           {"nwo": "gitlab.com/a/b", "name": "b"}, "main")
eq("README images on GitLab resolve to its raw, upload and blob->raw URLs", sorted(shots),
   sorted(["https://gitlab.com/a/b/-/raw/main/docs/demo.png", "https://gitlab.com/a/b/uploads/abc123/screen.png",
           "https://gitlab.com/a/b/-/raw/main/x.jpg"]))
eq("...and a GitHub README is unchanged", c4.shot_candidates("![d](docs/demo.png)", {"nwo": "a/b", "name": "b"}, "main"),
   ["https://raw.githubusercontent.com/a/b/main/docs/demo.png"])

dr = load("dead_for_gitlab_test", "dead_repos.py")


class DeadClient:
    def __init__(self, rest):
        self.rest, self.got = rest, []

    def graphql(self, q, v):
        return {"projects": {"nodes": [{"fullPath": "alive/one"}]}}

    def get(self, path, **kw):
        self.got.append(path)
        status = self.rest[path]
        if status != 200:
            raise gl.GitLabError(f"HTTP {status} for {path}: x")
        return {}, {}


dc = DeadClient({"/projects/moved%2Fone": 200, "/projects/gone%2Fone": 404})
eq("scan_gitlab: GraphQL alive, REST 200 alive (moved), REST 404 gone",
   dr.scan_gitlab(["gitlab.com/alive/one", "gitlab.com/moved/one", "gitlab.com/gone/one"], dc),
   {"gitlab.com/gone/one": {"status": "404"}})
try:
    dr.scan_gitlab(["gitlab.com/odd/one"], DeadClient({"/projects/odd%2Fone": 429}))
    true("scan_gitlab raises on a read that is not about the project", False)
except gl.GitLabError:
    true("scan_gitlab raises on a read that is not about the project", True)
data = {"cols": ["name", "nwo"], "rows": [["a", "openai/codex"], ["b", "gitlab.com/x/y"], ["c", "gitlab.com/a/b/c"]]}
(TMP / "d.json").write_text(json.dumps(data), encoding="utf-8")
eq("the GitHub half still lists GitHub only", dr.listed_repos(TMP / "d.json"), ["openai/codex"])
eq("the GitLab half lists GitLab only", dr.listed_gitlab(TMP / "d.json"), ["gitlab.com/a/b/c", "gitlab.com/x/y"])

ws = load("watch_for_gitlab_test", "watch_sources.py")
scout_src = {"key": "scout", "nwo": "crazy54/awesome-agentic-atlas", "synthetic": True}
gl_src = {"key": "gitlab", "nwo": "crazy54/awesome-agentic-atlas", "synthetic": True}
eq("the watch ledger keeps the scout's key and gives GitLab's its own",
   (ws.ledger_id(scout_src), ws.ledger_id(gl_src)),
   ("crazy54/awesome-agentic-atlas", "crazy54/awesome-agentic-atlas#gitlab"))
eq("...and a list's key is its nwo", ws.ledger_id({"key": "agents", "nwo": "kyrolabs/awesome-agents"}),
   "kyrolabs/awesome-agents")
(TMP / "data.json").write_text(json.dumps({"cols": ["nwo"], "rows": [["OpenAI/Codex"], ["gitlab.com/a/b"]]}),
                               encoding="utf-8")
eq("indexed_repos: GitHub rows, lower-cased to their spelling", g.indexed_repos(TMP / "data.json"),
   {"openai/codex": "OpenAI/Codex"})

# ======================================================================================== the wiring
group("the wiring")
flags = json.loads((ROOT / "config" / "app-flags.json").read_text(encoding="utf-8"))
eq("the intake.gitlab flag ships off, so this merges dark", flags.get("intake.gitlab"), 0)
schema = json.loads((ROOT / "config" / "app-flags.schema.json").read_text(encoding="utf-8"))
true("...and the schema describes it", any(x["key"] == "intake.gitlab" for x in schema["flags"]))
with flag(False):
    off = load("b10_off_for_gitlab_test", "10_parse_sources.py")
with flag(True):
    on = load("b10_on_for_gitlab_test", "10_parse_sources.py")
eq("flag off: no GitLab source in SOURCES", [s["key"] for s in off.SOURCES if s["key"] == "gitlab"], [])
eq("flag on: the GitLab source is last and synthetic",
   (on.SOURCES[-1]["key"], on.SOURCES[-1].get("synthetic"), on.SOURCES[-2]["key"]), ("gitlab", True, "scout"))
eq("...and its file is the document 12b writes", on.source_path(on.SOURCES[-1]).name, "gitlab.md")
eq("taxonomy maps the GitLab scout's ten sections to themselves",
   sorted(v for (k, s_), v in taxonomy.SECTIONS.items() if k == "gitlab" and v == s_), sorted(g.sc.SECTIONS))
true("taxonomy.ADVISORY holds the GitLab scout", "gitlab" in taxonomy.ADVISORY)
import buckets  # noqa: E402
eq("buckets fold it as the scout's", buckets.BUCKETS.get("gitlab"), buckets.BUCKETS["scout"])
daily = (ROOT / ".github" / "workflows" / "daily.yml").read_text(encoding="utf-8")
weekly = (ROOT / ".github" / "workflows" / "weekly.yml").read_text(encoding="utf-8")


def at(text, needle):
    return text.find(needle)


for name, text_ in (("daily", daily), ("weekly", weekly)):
    true(f"{name}: the GitLab scout runs before the parser",
         0 <= at(text_, "python scripts/12b_gitlab.py") < at(text_, "python scripts/10_parse_sources.py"))
    true(f"{name}: the GitLab fetch runs after the GitHub fetch and before the classifier",
         at(text_, "python scripts/11_fetch_all.py") < at(text_, "python scripts/11b_fetch_gitlab.py")
         < at(text_, "python scripts/14_classify_all.py"))
    true(f"{name}: GITLAB_TOKEN is passed, optionally", "GITLAB_TOKEN: ${{ secrets.GITLAB_TOKEN }}" in text_)
true("daily: the GitLab scout runs before the watch step",
     0 <= at(daily, "python scripts/12b_gitlab.py") < at(daily, "run: python scripts/watch_sources.py"))
committed = ROOT / "state" / "gitlab-repos.json"
if committed.exists():
    led = json.loads(committed.read_text(encoding="utf-8"))
    eq("the committed ledger files every project under a section the stage names",
       {e.get("section") for e in led["repos"].values()} - set(g.sc.SECTIONS), set())
    eq("...and is stored in the stage's sorted form", committed.read_text(encoding="utf-8").replace("\r\n", "\n"),
       g.sc.dump(led))

print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
