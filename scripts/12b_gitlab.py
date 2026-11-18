"""Scout gitlab.com for agentic projects, the way 12_scout.py scouts GitHub.

The atlas was built from GitHub because that is where the lists point, and the lists point there
because that is where most of the work is. Not all of it: GitLab's own agent platform, a good share of
the European and the self-hosting crowd, and projects whose maintainers left GitHub on principle all
live on gitlab.com, and no curated list in `SOURCES` links more than two of them. This stage is the
intake path for those. It asks GitLab's public API for projects under the topics and words the atlas
covers, judges each one by rules modelled on the GitHub scout's, and writes the survivors as one more
synthetic source document, so they flow through `10_parse_sources.py` and every stage after it exactly
as a scouted GitHub repo does: categories, targets, platform verdicts, detail pages and search.

  12b_gitlab.py             search (one rotation slice without a token, everything with one), update the
                            ledger, render the source document
  12b_gitlab.py --all       every query this run, whatever the budget
  12b_gitlab.py --offline   no network: render the document from the committed ledger
  12b_gitlab.py --dry-run   search and report, write nothing
  12b_gitlab.py --measure   search everything, judge it, and print the numbers and a sample; writes
                            nothing (the scan the owner was shown before this was built)
  12b_gitlab.py --status    what the ledger holds; no network, no writes

Output: `state/gitlab-repos.json`, committed -- the scouted set (`repos`), candidate lists hosted on
GitLab (`lists`), and the hand-kept `ignore` key -- and `cache/sources/gitlab.md`, rendered from it, which
is what the parser reads. Every row it adds has a host-qualified `nwo`, `gitlab.com/<full path>`; see
`hosts.py` for why that and not a column, and handbook/gitlab.md for the whole contract.

What is the same as the GitHub scout, deliberately, because the reasons carry over unchanged:

* **The ledger is sticky.** A project leaves only when a search this run *returns* it failing a quality
  rule. Absence is not evidence, and it matters even more here than on GitHub, because of the next point.
* **A sighting, not a vote.** The source is in `taxonomy.ADVISORY`, so its regex-chosen section only
  files a project no curator has filed, and its blurb never replaces a curator's.
* **Sections are the scout's.** `section_of` is `12_scout.section_of`, on topics normalised the way
  GitLab spells them (`MCP Server` and `mcp_server` are both `mcp-server`).
* **The document is the set.** No stars, no dates; its digest moves only when membership does, which is
  what `watch_sources.py` gates the daily build on.

What is different, and why:

* **The budget.** Anonymous gitlab.com is capped at roughly sixty requests an hour per IP (measured
  2026-11-18; see `gitlab_api.py`), and a full sweep is about that much on its own. So without a token
  each run takes the next `ANON_BUDGET` requests' worth of queries in a fixed rotation keyed by the day,
  and the sticky ledger accumulates the sweep over a few days; with `GITLAB_TOKEN` set every query runs
  every time. Any query that fails just contributes nothing: because merging is monotone except for a
  drop that a returned result proved, a partial run is as safe to keep as a whole one, which is why
  this stage does not throw the run away the way the GitHub scout throws away a failed half.
* **The bars are GitLab's.** Stars on gitlab.com run one to two orders of magnitude below GitHub for
  the same kind of project -- the most-starred `ai-agents` project had 352 on the day this was tuned --
  so the floors are set from GitLab's own distribution (see `STARS` and `ACTIVE_DAYS`), not copied.
* **Mirrors are a first-class rule.** A great many GitLab projects are mirrors or one-time imports of a
  GitHub repository, and the atlas already has the GitHub side. Anonymous reads cannot see GitLab's own
  `mirror` flag, so `mirror_of` judges from what everyone can read: the description, the README's
  opening, and whether the project's own `owner/name` is a repository the atlas already indexes.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import gitlab_api as gl  # noqa: E402
import hosts  # noqa: E402

STATE = ROOT / "state"
LEDGER = STATE / "gitlab-repos.json"
DATA = ROOT / "docs" / "data.json"            # what the atlas already indexes, for the mirror rule
DOC = ROOT / "cache" / "sources" / "gitlab.md"  # 10_parse_sources.source_path of the "gitlab" source

_spec = importlib.util.spec_from_file_location("scout_for_gitlab", HERE / "12_scout.py")
sc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sc)

# --- the bars ------------------------------------------------------------------------------------
# Tuned on the 2026-11-18 sweep; the numbers behind each are in handbook/gitlab.md.
STARS = 5                 # the floor for any project
ACTIVE_DAYS = 365         # ...and it must have had activity (a push, an issue, a merge) this recently
CORE_STARS = 25           # past this a project qualifies however quiet it has gone, back to ERA
ERA = sc.ERA
LIST_STARS = 5            # an awesome-list on GitLab worth a person's look

# --- the rotation --------------------------------------------------------------------------------
ANON_BUDGET = 40          # requests per anonymous run: two thirds of the hourly cap, leaving the
                          # fetch stage room in the same hour
MAX_PAGES = 5             # per query; ordered by stars and cut at the floor, so rarely more than one

# Topics, as the GitHub scout names them plus the general ones GitLab projects lean on more. Matched
# against GitLab's topic list by their normalised spelling, because GitLab topics are free text and
# its topic filter is exact and case-sensitive: `mcp-server` returns nothing, `MCP-server` returns 101.
EXTRA_TOPICS = ("llm", "llms", "claude", "openai", "langchain", "ollama", "local-llm", "llm-tools",
                "mcp-servers", "gpt", "chatgpt", "prompt-engineering", "agentic-workflow",
                "duo", "gitlab-duo")
TOPICS = tuple(dict.fromkeys([*sc.TOPICS, *sc.CORE_TOPICS, *EXTRA_TOPICS]))
# Words for GitLab's project search, which matches name, path and description. These reach the
# projects nobody tagged, which on GitLab is most of them.
WORDS = ("agent", "agentic", "mcp", "llm", "claude", "codex", "copilot", "rag", "gpt", "openai",
         "gemini", "ollama", "langchain", "prompt", "skills", "cursor", "opencode", "autonomous",
         "model context protocol", "awesome")
# Seeds for the topic-name lookup: one `/topics?search=` each, a substring match, so `agent` finds
# `ai-agents`, `Multi-Agent` and `agent-memory` alike. Each is as specific as it can be while still
# covering its family, because a broad one is pages of noise: `browser` alone was five pages of
# browser-extension topics, and `security` would be worse.
TOPIC_SEEDS = ("agent", "mcp", "llm", "claude", "codex", "copilot", "rag", "gpt", "openai", "langchain",
               "ollama", "skill", "ai-coding", "vibe", "prompt", "eval", "guardrail", "ai-security",
               "ai-safety", "context-engineering", "cursor", "gemini", "opencode", "duo", "autonomous",
               "computer-use", "browser-use")


def say(msg: str) -> None:
    print(msg, flush=True)


def norm_topic(t: str) -> str:
    """GitLab's free-text topic as the scout's vocabulary spells it."""
    return re.sub(r"[\s_]+", "-", str(t).strip().lower())


# --- judging one project ---------------------------------------------------------------------------
def item(p: dict) -> dict:
    """A REST project from `/projects` in the shape the scout's rules read, with GitLab's own fields
    kept beside them. Fork, archive and import state are filled in later by `enrich`."""
    return {"id": p.get("id"), "full_name": p.get("path_with_namespace") or "",
            "name": p.get("path") or "", "title": p.get("name") or "",
            "description": (p.get("description") or "").strip(),
            "stargazers_count": int(p.get("star_count") or 0),
            "forks": int(p.get("forks_count") or 0),
            "created_at": p.get("created_at") or "", "pushed_at": p.get("last_activity_at") or "",
            "topics": sorted({norm_topic(t) for t in p.get("topics") or p.get("tag_list") or ()}),
            "avatar": p.get("avatar_url") or "", "readme_url": p.get("readme_url") or "",
            "fork": None, "archived": bool(p.get("archived")), "import_status": "", "readme": ""}


# The README's opening, where a mirror says so. Only the first 1,500 characters: a project that cites
# GitHub somewhere in its install section is not a mirror for that.
README_MIRROR = re.compile(
    r"(?<![a-z])(?:mirror(?:ed)?|read-?only\s+copy|moved\s+to|development\s+(?:happens|has\s+moved))"
    r"[^.\n]{0,80}github\.com/(?P<nwo>[A-Za-z0-9-]+/[A-Za-z0-9_.-]+)", re.IGNORECASE)
GH_LINK = re.compile(r"github\.com/(?P<nwo>[A-Za-z0-9-]+/[A-Za-z0-9_.-]+?)(?:\.git)?(?=[/)\s\"'#?]|$)")


def mirror_of(it: dict, indexed: dict[str, str]) -> str:
    """The GitHub repository this GitLab project is a copy of, or "".

    Four tests, from what an anonymous reader can see:
      1. the description says "mirror of/from" (the scout's own MIRROR rule);
      2. the README's opening says it is a mirror, a read-only copy, or that development moved, next to
         a github.com link -- that link is the answer;
      3. its own `owner/name` (the last two path segments) is a repository the atlas already indexes;
      4. the README's opening links a github.com repository with the same name, and that repository
         is one the atlas already indexes.
    3 and 4 are about the atlas, not about mirroring as such: a GitLab project whose GitHub twin is
    already a row would be the same project twice, whichever of the two is the copy.
    """
    head = (it.get("readme") or "")[:1500]
    if sc.MIRROR.search(it.get("description") or ""):
        m = GH_LINK.search(it.get("description") or "") or GH_LINK.search(head)
        return m.group("nwo") if m else "(described as a mirror)"
    m = README_MIRROR.search(head)
    if m:
        return m.group("nwo")
    parts = it["full_name"].split("/")
    tail = "/".join(parts[-2:]).lower()
    if tail in indexed:
        return indexed[tail]
    name = parts[-1].lower()
    for m in GH_LINK.finditer(head):
        nwo = m.group("nwo").rstrip(".")
        if nwo.split("/")[-1].lower() == name and nwo.lower() in indexed:
            return indexed[nwo.lower()]
    return ""


def hygiene(it: dict, indexed: dict[str, str]) -> str:
    """The scout's hygiene, on GitLab's fields, plus the GitHub-twin rule. "" for clean."""
    if it.get("fork"):
        return "fork"
    if it.get("archived"):
        return "archived"
    if mirror_of(it, indexed):
        return "mirror"
    if not it.get("description"):
        return "no description"
    if sc.SPAM.search(it["description"]) or set(it["topics"]) & sc.SPAM_TOPICS:
        return "spam"
    return ""


def is_list(it: dict) -> bool:
    return "awesome" in f"{it.get('name')} {it.get('title')}".lower()


def agentic(it: dict) -> bool:
    """The scout's test -- an agentic word in the name or description, never topics alone -- read over
    GitLab's path and its display name both, since GitLab keeps them separately."""
    return sc.agentic({"name": it.get("name"), "description": it.get("description")}) or \
        sc.agentic({"name": it.get("title"), "description": ""})


def tier(it: dict, today: date) -> str:
    """"active", "core", or "": which bar this project clears."""
    stars = it["stargazers_count"]
    pushed = str(it.get("pushed_at") or "")[:10]
    created = str(it.get("created_at") or "")[:10]
    if stars >= STARS and pushed >= (today - timedelta(days=ACTIVE_DAYS)).isoformat():
        return "active"
    if stars >= CORE_STARS and created >= ERA:
        return "core"
    return ""


def verdict(it: dict, today: date, indexed: dict[str, str]) -> str:
    """"" if this project belongs in the scouted set, else the reason it does not."""
    bad = hygiene(it, indexed)
    if bad:
        return bad
    if is_list(it):
        return "list"
    if not agentic(it):
        return "off-topic"
    if not tier(it, today):
        return "below threshold"
    return ""


def prejudge(it: dict, today: date) -> str:
    """The verdict from the list endpoint's fields alone, before `enrich` has said whether a project is a
    fork or what its README says: "" or "list" if it needs enriching to be judged, else a reason that
    holds whatever enrichment would say. This is what keeps the enrich bill to the projects that could
    qualify -- a few dozen requests rather than one per twenty-five projects the word searches return,
    most of which have no agentic word or no stars -- and it is sound because every reason it returns
    is one `verdict` would return too, or (for a fork or a mirror that is also off-topic) one that has
    the same effect: not added, and dropped if scouted."""
    if not it.get("description"):
        # GitLab projects often leave the description empty and say what they are in the README, which
        # `enrich` reads and `gitlab_api.readme_summary` turns into one. That is worth a request only for
        # a project whose name already says it is agentic and that clears a bar.
        return "" if agentic(it) and tier(it, today) and not is_list(it) else "no description"
    if sc.SPAM.search(it["description"]) or set(it["topics"]) & sc.SPAM_TOPICS:
        return "spam"
    if is_list(it):
        return "list"
    if not agentic(it):
        return "off-topic"
    if not tier(it, today):
        return "below threshold"
    return ""


def judge(it: dict, today: date, indexed: dict[str, str]) -> str | None:
    """`verdict` for an enriched project, `prejudge`'s reason for one that did not need enriching, and
    None for one that needed it and did not get it (a refused batch): that one is judged on nothing."""
    if it.get("fork") is not None:
        return verdict(it, today, indexed)
    pre = prejudge(it, today)
    return pre if pre not in ("", "list") else None


def list_verdict(it: dict, indexed: dict[str, str]) -> str:
    bad = hygiene(it, indexed)
    if bad:
        return bad
    if not is_list(it):
        return "not a list"
    if it["stargazers_count"] < LIST_STARS:
        return "below threshold"
    if not (set(it["topics"]) & set(sc.LIST_TOPICS) or agentic(it)):
        return "off-topic"
    return ""


def section_of(it: dict) -> str:
    return sc.section_of({"topics": it["topics"]})


QUALITY = {"fork", "archived", "mirror", "no description", "spam", "off-topic", "list"}


# --- what the atlas already has ------------------------------------------------------------------
def indexed_repos(path: Path = DATA) -> dict[str, str]:
    """Lower-cased GitHub `owner/repo` -> its spelling, for every repository row the atlas publishes."""
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    at = data["cols"].index("nwo")
    return {r[at].lower(): r[at] for r in data["rows"] if r[at] and hosts.is_github(r[at])}


# --- searching -------------------------------------------------------------------------------------
def queries(known: dict[str, int] | None = None) -> list[tuple[str, str]]:
    """Every query in rotation order: ("topics", seed) lookups, which decide which topic spellings
    exist, then the word searches, then one ("topic", name) per spelling already known -- the ledger's
    `topics` key, which the lookups keep filling. Known spellings are in the plan rather than only
    appended when a lookup finds them, because an anonymous run is one slice of the rotation: a slice
    that holds a lookup is rarely the slice that would have room for the queries it found. A spelling
    a lookup finds this run is still queried this run if the budget allows (`sweep`)."""
    return ([("topics", s) for s in TOPIC_SEEDS] + [("search", w) for w in WORDS]
            + [("topic", t) for t in sorted(known or (), key=str.lower)])


def floor_hit(p: dict) -> bool:
    return int(p.get("star_count") or 0) < min(STARS, LIST_STARS)


def run_query(client: gl.Client, kind: str, arg: str) -> list[dict]:
    if kind == "topics":
        return client.pages("/topics", search=arg, max_pages=2)
    common = dict(order_by="star_count", sort="desc", archived="false", visibility="public",
                  max_pages=MAX_PAGES, until=floor_hit)
    if kind == "search":
        return client.pages("/projects", search=arg, **common)
    return client.pages("/projects", topic=arg, **common)


def sweep(client: gl.Client, today: date, everything: bool, budget: int = ANON_BUDGET,
          log=say, known: dict[str, int] | None = None) -> tuple[dict[str, dict], dict]:
    """Run this run's share of the queries. Returns (projects by full path, report).

    With a token, or `everything`, every query. Without, a slice of the rotation starting at today's
    offset and stopping once `budget` requests are spent, so consecutive days cover consecutive slices
    and the whole set comes round every few days. A query that fails is logged and skipped: see "A
    partial run is safe" in the module docstring. A run whose very first request is refused (the IP's
    hourly cap already spent by someone else on a shared runner) therefore just finds nothing.
    """
    found: dict[str, dict] = {}
    spellings: dict[str, int] = dict(known or {})
    plan = queries(known)
    start = 0 if everything or client.token else today.toordinal() % len(plan)
    order = plan[start:] + plan[:start]
    done, failed = [], []
    capped = not (everything or client.token)
    i = 0
    while i < len(order):
        kind, arg = order[i]
        i += 1
        if capped and client.requests >= budget:
            break
        try:
            got = run_query(client, kind, arg)
        except gl.GitLabError as exc:
            failed.append((kind, arg, str(exc)))
            log(f"  !! {kind} {arg!r}: {exc}")
            if "rate limited" in str(exc):
                break          # every later query would be refused the same way
            continue
        done.append((kind, arg))
        if kind == "topics":
            new = [t["name"] for t in got
                   if norm_topic(t.get("name")) in TOPICS and int(t.get("total_projects_count") or 0)]
            for name in new:
                if name not in spellings:
                    spellings[name] = int(next(t for t in got if t["name"] == name)
                                          ["total_projects_count"])
                    order.append(("topic", name))
            log(f"  {len(new):5d}  topic spellings for {arg!r}")
            continue
        for p in got:
            it = found.setdefault(p["path_with_namespace"], item(p))
            it.setdefault("via", []).append(f"{kind}:{arg}")
        log(f"  {len(got):5d}  {kind} {arg!r}")
    return found, {"done": done, "failed": failed, "spellings": spellings,
                   "left": len(order) - i, "requests": client.requests, "cached": client.cached}


ENRICH = """query($paths: [String!]) {
  projects(fullPaths: $paths, first: 100) {
    nodes { fullPath archived isForked importStatus
            repository { rootRef blobs(paths: ["README.md"]) { nodes { rawTextBlob } } } }
  }
}"""
ENRICH_BATCH = 25         # READMEs ride along, so a batch is kept small enough to stay inside the
                          # anonymous GraphQL complexity and response-size limits


def enrich(client: gl.Client, items: list[dict], log=say) -> int:
    """Fill in fork, archive and import state and the README's opening, which the list endpoint does
    not return anonymously, for `items` in place. Returns how many were answered; an item a failed
    batch left unanswered keeps `fork` None, and `merge` neither adds nor drops on it."""
    answered = 0
    for start in range(0, len(items), ENRICH_BATCH):
        batch = items[start:start + ENRICH_BATCH]
        try:
            data = client.graphql(ENRICH, {"paths": [b["full_name"] for b in batch]})
        except gl.GitLabError as exc:
            log(f"  !! enrich {start}: {exc}")
            if "rate limited" in str(exc):
                break
            continue
        by = {n["fullPath"].lower(): n for n in ((data.get("projects") or {}).get("nodes") or ())}
        for b in batch:
            n = by.get(b["full_name"].lower())
            if not n:
                continue
            blobs = (((n.get("repository") or {}).get("blobs") or {}).get("nodes") or [])
            b.update(fork=bool(n.get("isForked")), archived=bool(n.get("archived")),
                     import_status=n.get("importStatus") or "",
                     readme=(blobs[0].get("rawTextBlob") or "")[:4000] if blobs else "")
            if not b["description"] and b["readme"]:
                # No description: the README's first line of prose stands in for one, so the rules
                # that read a description read something (see `prejudge`).
                b["description"] = gl.readme_summary(b["readme"])
            answered += 1
    return answered


# --- the ledger ------------------------------------------------------------------------------------
def load(path: Path = LEDGER) -> dict:
    if not path.exists():
        return {"version": 1, "repos": {}, "lists": {}}
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        sys.exit(f"{path.name} does not parse. It is committed, so restore it from git rather than let "
                 f"this stage start over: an empty scouted set would delete every GitLab row.")
    state.setdefault("version", 1)
    state.setdefault("repos", {})
    state.setdefault("lists", {})
    return state


def save(state: dict, path: Path = LEDGER) -> bool:
    return sc.save(path, state)


def merge(ledger: dict, found: dict[str, dict], today: date, indexed: dict[str, str]) -> dict:
    """The next scouted set and candidate lists, from the last ones and this run's answers.

    The scout's `merge_repos`, by GitLab project id so a moved project keeps its `since`, with one
    addition: a project `enrich` could not answer for is judged on nothing and so changes nothing.
    Candidate lists are sticky too, unlike the scout's, because a rotation slice that did not include
    the `awesome` search is not evidence that a list went away.
    """
    repos, lists = ledger["repos"], ledger["lists"]
    skip = sc.ignored(ledger)
    report = {"added": [], "dropped": [], "moved": [], "renamed": [], "lists_added": [],
              "unjudged": 0, "why": {}}
    by_id = {e.get("id"): k for k, e in repos.items() if e.get("id") is not None}
    by_lower = {k.lower(): k for k in repos}
    for path in sorted(found, key=str.lower):
        it = found[path]
        why = judge(it, today, indexed)
        if why is None:
            report["unjudged"] += 1
            continue
        if path.lower() in skip:
            continue
        report["why"][why or "kept"] = report["why"].get(why or "kept", 0) + 1
        if why == "list" and not list_verdict(it, indexed):
            was = lists.get(path) or {}
            if not was:
                report["lists_added"].append(path)
            lists[path] = {"id": it["id"], "stars": it["stargazers_count"],
                           "description": it["description"][:300],
                           "pushed_at": str(it["pushed_at"])[:10],
                           "first_seen": was.get("first_seen") or today.isoformat()}
        old = by_id.get(it["id"]) or by_lower.get(path.lower())
        if old and old != path:
            repos[path] = repos.pop(old)
            by_lower.pop(old.lower(), None)
            by_lower[path.lower()] = path
            report["renamed"].append((old, path))
            old = path
        if old:
            if why in QUALITY:
                repos.pop(old)
                by_lower.pop(old.lower(), None)
                report["dropped"].append((old, why))
                continue
            entry = repos[old]
            entry["id"] = it["id"]
            section = section_of(it)
            if section != entry.get("section"):
                report["moved"].append((old, entry.get("section"), section))
                entry["section"] = section
            continue
        if why:
            continue
        repos[path] = {"id": it["id"], "section": section_of(it), "since": today.isoformat()}
        by_lower[path.lower()] = path
        report["added"].append(path)
    for path in [k for k in repos if k.lower() in skip]:
        repos.pop(path)
        report["dropped"].append((path, "ignored"))
    return report


# --- the document ----------------------------------------------------------------------------------
def render(ledger: dict, on: bool = True) -> str:
    """The synthetic source, as Markdown the bullet parser reads. A pure function of the ledger -- and
    of the flag: off, it is the heading and nothing else, so even a stale ledger adds no rows."""
    out = ["# Scouted on GitLab", "",
           "Agentic projects on gitlab.com found by GitLab's own search. Generated by",
           "scripts/12b_gitlab.py from state/gitlab-repos.json -- edit the ledger, not this file.", ""]
    if not on:
        return "\n".join(out)
    by_section: dict[str, list[str]] = {}
    for path, e in ledger["repos"].items():
        by_section.setdefault(e.get("section") or sc.GENERIC[0], []).append(path)
    for section in sc.SECTIONS + sorted(s for s in by_section if s not in sc.SECTIONS):
        names = sorted(by_section.get(section, ()), key=lambda n: (n.lower(), n))
        if names:
            out += [f"## {section}", ""]
            out += [f"- [{n.rsplit('/', 1)[1]}](https://gitlab.com/{n})" for n in names]
            out.append("")
    return "\n".join(out)


def write_doc(ledger: dict, on: bool | None = None) -> bool:
    text = render(ledger, hosts.enabled() if on is None else on)
    if DOC.exists() and DOC.read_bytes() == text.encode("utf-8"):
        return False
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_bytes(text.encode("utf-8"))
    return True


# --- reporting -------------------------------------------------------------------------------------
def summary(report: dict, sweep_report: dict, ledger: dict, found: dict[str, dict]) -> str:
    out = ["### GitLab scout", ""]
    out.append(f"{len(ledger['repos']):,} scouted · +{len(report['added'])} new · "
               f"-{len(report['dropped'])} dropped · {len(report['moved'])} re-filed · "
               f"{len(report['renamed'])} renamed · {len(ledger['lists'])} candidate lists")
    out.append(f"{len(sweep_report['done'])} queries answered, {len(sweep_report['failed'])} failed, "
               f"{sweep_report['left']} left for later runs · {sweep_report['requests']} requests"
               + (f" · {report['unjudged']} projects unjudged" if report.get("unjudged") else ""))
    if report["added"]:
        out += ["", "| new today | stars | section |", "|---|---:|---|"]
        top = sorted(report["added"], key=lambda n: (-found[n]["stargazers_count"], n.lower()))[:15]
        out += [f"| [{n}](https://gitlab.com/{n}) | {found[n]['stargazers_count']:,} | "
                f"{ledger['repos'][n]['section']} |" for n in top]
    for n, why in report["dropped"][:15]:
        out.append(f"- dropped {n}: {why}")
    for kind, arg, why in sweep_report["failed"][:5]:
        out.append(f"- failed {kind} {arg!r}: {why[:120]}")
    return "\n".join(out) + "\n"


def measure(found: dict[str, dict], today: date, indexed: dict[str, str]) -> str:
    """The numbers the owner asked for before anything was built, from one full sweep."""
    why: dict[str, list[str]] = {}
    for path, it in found.items():
        v = judge(it, today, indexed)
        why.setdefault("unjudged" if v is None else v or "kept", []).append(path)
    keep = why.get("kept", [])
    mirrors = why.get("mirror", [])
    twins = [p for p in mirrors if mirror_of(found[p], indexed).lower() in indexed]
    out = [f"{len(found):,} projects returned by the sweep", ""]
    for k in sorted(why, key=lambda k: -len(why[k])):
        out.append(f"  {len(why[k]):5d}  {k}")
    out += ["", f"mirrors: {len(mirrors)}, of which {len(twins)} copy a repository the atlas already "
                f"indexes", ""]
    per: dict[str, int] = {}
    for p in keep:
        per[section_of(found[p])] = per.get(section_of(found[p]), 0) + 1
    out.append(f"{len(keep)} would be scouted:")
    for s in sc.SECTIONS:
        if per.get(s):
            out.append(f"  {per[s]:5d}  {s}")
    tiers: dict[str, int] = {}
    for p in keep:
        tiers[tier(found[p], today)] = tiers.get(tier(found[p], today), 0) + 1
    out.append(f"  by bar: {tiers}")
    out += ["", "| project | stars | last activity | section | description |", "|---|---:|---|---|---|"]
    for p in sorted(keep, key=lambda p: (-found[p]["stargazers_count"], p.lower()))[:60]:
        it = found[p]
        out.append(f"| [{p}](https://gitlab.com/{p}) | {it['stargazers_count']} | "
                   f"{str(it['pushed_at'])[:10]} | {section_of(it)} | "
                   f"{it['description'][:80].replace('|', '/')} |")
    if twins:
        out += ["", "Mirrors of indexed repositories (sample):"]
        out += [f"- {p} -> github.com/{mirror_of(found[p], indexed)}" for p in sorted(twins)[:20]]
    return "\n".join(out) + "\n"


def run(today: date, client: gl.Client, everything: bool = False, dry_run: bool = False,
        log=say) -> dict:
    ledger = load()
    indexed = indexed_repos()
    found, sw = sweep(client, today, everything, log=log, known=ledger.get("topics"))
    enrich(client, [it for it in found.values() if prejudge(it, today) in ("", "list")], log=log)
    report = merge(ledger, found, today, indexed)
    # Sticky as well: a spelling stays known once a lookup has seen it, with its latest project count.
    ledger["topics"] = {**(ledger.get("topics") or {}), **sw["spellings"]}
    wrote = {}
    if not dry_run:
        wrote = {"ledger": save(ledger), "doc": write_doc(ledger)}
    return {"report": report, "sweep": sw, "ledger": ledger, "found": found, "wrote": wrote,
            "indexed": indexed}


def status() -> None:
    ledger = load()
    per: dict[str, int] = {}
    for e in ledger["repos"].values():
        per[e.get("section")] = per.get(e.get("section"), 0) + 1
    print(f"{len(ledger['repos']):,} scouted GitLab projects in {LEDGER.relative_to(ROOT).as_posix()}"
          f" · flag intake.gitlab is {'on' if hosts.enabled() else 'off'}")
    for s in sc.SECTIONS:
        if per.get(s):
            print(f"  {per[s]:5d}  {s}")
    print(f"{len(ledger['lists']):,} candidate lists")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--offline", action="store_true", help="no network: render from the ledger")
    ap.add_argument("--dry-run", action="store_true", help="search and report, write nothing")
    ap.add_argument("--all", action="store_true", help="every query, whatever the anonymous budget")
    ap.add_argument("--measure", action="store_true",
                    help="every query, then the numbers and a sample; writes nothing")
    ap.add_argument("--status", action="store_true", help="report the ledger; no network")
    ap.add_argument("--ttl", type=float, default=0,
                    help="reuse cached API answers younger than this many hours (local tuning only)")
    args = ap.parse_args()

    if args.status:
        status()
        return
    if args.offline or not (hosts.enabled() or args.measure or args.dry_run):
        # Flag off: no network at all, and the document is the empty heading, so the source the
        # parser would read (if the flag were on) holds nothing stale. Flag on with --offline: the
        # committed ledger, rendered.
        changed = write_doc(load())
        print(f"{len(load()['repos']):,} scouted GitLab projects"
              + ("" if hosts.enabled() else " (flag intake.gitlab off: document left empty)")
              + f" -> {DOC.relative_to(ROOT).as_posix()} ({'rewritten' if changed else 'unchanged'})")
        return

    today = date.today()
    client = gl.Client(ttl=args.ttl * 3600)
    result = run(today, client, everything=args.all or args.measure,
                 dry_run=args.dry_run or args.measure)
    if args.measure:
        print(measure(result["found"], today, result["indexed"]))
    text = summary(result["report"], result["sweep"], result["ledger"], result["found"])
    print(text)
    out = os.environ.get("GITHUB_STEP_SUMMARY")
    if out and not (args.dry_run or args.measure):
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(text)


if __name__ == "__main__":
    main()
