"""Scout GitHub search for agentic repos no curated list has caught yet, and for lists worth adding.

Every other row in the atlas arrives because a curator put it on a list, so the atlas can only be as
current as its slowest curator. `morluto/rea` is the case that made that concrete: 110k stars six months
after it was created, and the lists that first cited it linked a skill folder inside it, which the atlas
files as a zero-star `subpath` row by design. This stage is a second intake path. It asks GitHub search
for what is rising under the topics the atlas covers and writes the answer as one more source document,
so the scouted repos flow through `10_parse_sources.py` and everything after it exactly as a curated
list's entries do.

  12_scout.py             search, update the two ledgers, render the source document
  12_scout.py --offline   no network: render the document from the committed ledger
  12_scout.py --dry-run   search and report, write nothing
  12_scout.py --reset     as the default, but keep only the scouted repos that qualify today
  12_scout.py --status    what the ledgers hold; no network, no writes

Two outputs, for two readers:

  state/scout-repos.json   committed. The scouted set: repo id, section, and the day it was first scouted.
                           `cache/sources/scout.md` is rendered from it and is what the parser reads.
  state/scout-lists.json   committed. Curated lists GitHub has that `SOURCES` does not, for a person to
                           consider adding: stars, description, last push, and when the scout first saw it.

Six decisions worth knowing about:

* **The ledger is sticky.** A repo stays scouted once it qualified, even after it ages out of the
  rising window or stops appearing in today's results. The atlas is a catalogue with indexed detail
  pages, and a scout that forgot a project the day it turned 181 days old would delete a page that was
  correct yesterday. A scouted repo leaves only when today's search *returns* it and it fails a quality
  rule -- archived, now a fork, spam, off-topic -- so leaving needs evidence and absence is not evidence.
  Two consequences a person has to know about. Every rule is one-way: tightening a threshold stops new
  arrivals and removes nothing, so run `--reset` once after tightening one. And deleting a repo from
  the ledger by hand does nothing if it still qualifies; put it under the ledger's `ignore` key, with a
  reason, instead. `state/scout-lists.json` honours the same key for a list someone has declined.

* **A failed search changes nothing.** Any query that errors, rate-limits past its retries or comes
  back `incomplete_results` fails the whole half it belongs to, and that half's ledger is left exactly
  as it was. The document is still rendered -- from the unchanged ledger, so it comes out byte-identical
  to the one the last good run wrote -- rather than emptied, which would delete every scouted row.

* **The gate sees the scout as a list that moved.** A synthetic source has no upstream commit, so
  `watch_sources.py` asks `10_parse_sources.content_digest` for a SHA-256 of the rendered document
  instead, and `--update` records it in `state/first-seen.json` exactly where a list's commit id goes.
  The document carries no timestamps and no star counts, only which repos are in which section, so the
  digest moves when the scouted *set* moves and not when a star count does.

* **Sections are atlas categories.** A repo's section is decided by its own topics, not by which query
  happened to return it: the family whose topics it carries most of, the earlier one in `FAMILIES` on a
  tie, then the generic agent topics, then the harness names. Each section is spelled exactly like the
  `taxonomy.CATEGORIES` entry it maps to, so `taxonomy.SECTIONS` maps every one of them to itself.

* **Quality is a set of named rules, not a score.** See `verdict()`. The search itself already asks for
  `fork:false archived:false`; the rules re-check that and add what search cannot: mirrors, no
  description, spam (the `ReverseEngineerAnything/REA` clone of `morluto/rea` is the reference case),
  and an agentic word in the name or description -- topics alone are not evidence, because topics are
  what an SEO repo stuffs. The any-age tier also requires `created >= ERA`, since an older repo no
  curated list has picked up is, on the sample this was tuned on, nearly always a non-agentic project
  that added `mcp` or `ai-agents` to its topics.

* **A sighting, not a vote.** The scout lists every repo that qualifies, including the ones a curated
  list already has -- that overlap is provenance, and it is what turns a curator's sub-folder row into
  a full repo row with stars. But its section is a regex's guess and its blurb is GitHub's tagline, so
  downstream it never overrules a person: `taxonomy.ADVISORY` makes its category count only for a repo
  no curated listing has filed, and `16_build_all.offer_blurb` lets its blurb fill a gap but never
  replace a curator's. It does still count in `list_count`; see the note on `SOURCES` in
  `10_parse_sources.py`.

Search is 30 requests a minute and 1,000 results a query. Requests are spaced `MIN_GAP` apart and the
`X-RateLimit-*` headers decide any longer wait; a full run is roughly 130 requests, about four and a
half minutes.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
import time
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
STATE = ROOT / "state"
REPOS = STATE / "scout-repos.json"
LISTS = STATE / "scout-lists.json"

_spec = importlib.util.spec_from_file_location("b10_for_scout", HERE / "10_parse_sources.py")
b10 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(b10)

# The scout's own entry in SOURCES. It is a source like any other as far as every later stage knows;
# `synthetic` is what tells pull_sources and watch_sources there is no upstream commit to ask about.
SCOUT = next(s for s in b10.SOURCES if s.get("synthetic"))
DOC = b10.source_path(SCOUT)

# --- the rules ---------------------------------------------------------------------------------
# Rising: created inside the window and past the star bar. Tuned on the 2026-10-11 results: at 300
# stars the window held 1,208 repos, 85% of them on no curated list, and the bottom quartile (300-420)
# was still recognisably agentic work rather than noise.
YOUNG_DAYS = 180
YOUNG_STARS = 300
# Established: any age past a much higher bar, on CORE_TOPICS only, and no older than ERA. Without the
# ERA floor this tier returned Java interview guides, a PAM server and a Go microservice framework, all
# from before 2023 and all wearing `mcp` or `ai-agents` as a topic.
CORE_STARS = 2000
ERA = "2023-01-01"
# Candidate lists: "awesome" in the name, past this bar, pushed inside this many days.
LIST_STARS = 200
LIST_PUSHED_DAYS = 90

# Families, in tie-break order -- the order of `taxonomy.CATEGORIES`, where the specific shelves come
# first. A repo is scored against these by how many of each family's topics it carries.
FAMILIES: list[tuple[str, tuple[str, ...]]] = [
    ("Orchestrators & Multi-Agent", ("multi-agent", "multi-agent-systems", "agent-orchestration")),
    ("Coding Agents", ("coding-agent", "coding-agents", "ai-coding", "ai-coding-agent",
                       "ai-coding-assistant", "vibe-coding")),
    ("Agent Skills", ("agent-skills", "agent-skill", "claude-skills", "claude-code-skills", "skills")),
    ("MCP Servers", ("mcp", "mcp-server", "model-context-protocol")),
    ("Frameworks & SDKs", ("agent-framework", "agentic-framework", "langgraph")),
    ("Context, Memory & RAG", ("rag", "agent-memory", "context-engineering", "llm-memory")),
    ("Sandbox, Security & Governance", ("ai-security", "llm-security", "agent-security",
                                        "prompt-injection", "guardrails", "ai-safety")),
    ("Observability & Evals", ("llm-evaluation", "evals", "llm-observability", "agent-evaluation",
                               "llmops")),
]
# Asked of a repo only when no family above matched. Generic agent topics say a thing is an agent and
# not which kind; a harness name says what it plugs into, which with nothing else to go on makes it an
# add-on for that client.
GENERIC = ("Assistants & Domain Agents",
           ("ai-agents", "ai-agent", "agents", "agent", "agentic-ai", "agentic", "llm-agent",
            "llm-agents", "autonomous-agents", "browser-use", "computer-use", "browser-agent",
            "ai-assistant"))
HARNESS = ("Plugins, Themes & Clients",
           ("claude-code", "codex", "codex-cli", "gemini-cli", "opencode", "cursor", "copilot",
            "claude-code-plugin"))
SECTIONS = [s for s, _ in FAMILIES] + [GENERIC[0], HARNESS[0]]
TOPICS = [t for _, ts in FAMILIES for t in ts] + list(GENERIC[1]) + list(HARNESS[1])

# The any-age tier's topics: the ones whose >=2,000-star results were mostly agentic on inspection.
# `mcp`, `agents` and `rag` are absent on purpose -- they are where the rebranded general-purpose
# software concentrates.
CORE_TOPICS = ("coding-agent", "agent-skills", "claude-skills", "mcp-server", "model-context-protocol",
               "multi-agent", "agent-orchestration", "agent-framework", "agent-memory", "llm-agent",
               "autonomous-agents", "browser-use", "computer-use", "ai-agents", "ai-agent",
               "agentic-ai", "claude-code", "codex")

# Topics that make an "awesome" repo a candidate list worth a person's look.
LIST_TOPICS = ("ai-agents", "ai-agent", "agents", "agentic-ai", "llm", "llm-agent", "multi-agent",
               "mcp", "mcp-server", "model-context-protocol", "claude", "claude-code", "codex",
               "agent-skills", "cursor", "gemini-cli", "copilot", "opencode", "openclaw", "rag",
               "llmops", "prompt-engineering", "vibe-coding", "ai-coding")

# An agentic word in the name or description. ASCII-letter lookarounds rather than \b, because \b
# treats CJK as word characters and "多Agent舆情" would not match. Bare "AI" is deliberately not one:
# it is in the description of a Java interview guide, a front-end checklist and a game engine, all of
# which carried agent topics in the sample this was tuned on. What it costs is a repo that says only
# "AI-powered" and nothing more specific; a curated list can still bring those in.
AGENTIC = re.compile(
    r"(?<![a-z])(?:agents?|agentic|subagents?|mcp|llms?|claude|anthropic|codex|openai|copilot|cursor|"
    r"gemini|grok|opencode|openclaw|skills?|rag|gpt|chatgpt|deepseek|qwen|kimi|harness|prompts?|"
    r"autonomous|vibe[\s-]?cod\w*|ai[\s-]coding|coding[\s-]assistants?|computer[\s-]use|"
    r"model[\s-]context[\s-]protocol)(?![a-z])|智能体|大模型|提示词", re.IGNORECASE)
NAME_AGENTIC = ("agent", "mcp", "claude", "codex", "copilot", "llm", "gpt", "skill", "cursor",
                "gemini", "opencode", "openclaw", "deepseek")
# What the download-bait clones say. The REA clone's description is the reference case: "...Official
# free download. Local zip. Download:".
SPAM = re.compile(
    r"free\s+download|official\s+(?:free\s+)?download|download\s*[:：]|direct\s+download|"
    r"(?<![a-z])(?:crack(?:ed)?|keygen|activator)(?![a-z])|serial\s+key|license\s+key|"
    r"activation\s+(?:key|code)|setup\.exe|local\s+zip|windows\s+1[01]\s*/\s*1[01]", re.IGNORECASE)
SPAM_TOPICS = {"download", "free-download", "crack", "cracked", "keygen", "activator", "license-key",
               "serial-key", "full-version", "unlocked"}
MIRROR = re.compile(r"(?<![a-z])mirror(?:ed)?\s+(?:of|from)(?![a-z])", re.IGNORECASE)

# Rejections a scouted repo can be dropped for. Threshold and age are deliberately not among them:
# see "The ledger is sticky" above.
QUALITY = {"fork", "archived", "mirror", "disabled", "no description", "spam", "off-topic", "list",
           "curated list"}

# --- search ------------------------------------------------------------------------------------
PER_PAGE = 100
MAX_PAGES = 10            # the search API's 1,000-result ceiling
MIN_GAP = 2.0             # seconds between requests: 30/minute is the authenticated search limit
RETRIES = 4
MAX_WAIT = 75             # the longest single rate-limit wait honoured before giving up
DEADLINE = 25 * 60        # the whole search, so a stuck API cannot hold the daily job


def say(msg: str) -> None:
    """Print and flush. A pipe is block-buffered, and four minutes of searching with nothing in the
    Actions log until the end reads exactly like a hang."""
    print(msg, flush=True)


class ScoutError(RuntimeError):
    """A search that cannot be trusted. Whatever half of the run it belongs to keeps its ledger."""


def gh_search(q: str, page: int) -> tuple[int, dict, dict]:
    """One page of repository search through `gh`, as (status, lower-cased headers, body).

    `--include` because the rate-limit headers decide how long to wait, and because `gh` exits 1 on
    any HTTP error: the status line is the only reliable way to tell a 422 (a query we wrote wrong,
    never worth retrying) from a 403 rate limit (always worth waiting out). A transport failure with
    no HTTP response at all -- the TLS handshake timeout seen while tuning this -- raises.
    """
    try:
        out = subprocess.run(
            ["gh", "api", "--include", "-X", "GET", "search/repositories", "-f", f"q={q}",
             "-f", "sort=stars", "-f", "order=desc", "-f", f"per_page={PER_PAGE}",
             "-f", f"page={page}"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ScoutError(f"gh did not answer: {type(exc).__name__}") from None
    text = out.stdout.replace("\r\n", "\n")
    head, sep, body = text.partition("\n\n")
    if not sep or not head.startswith("HTTP/"):
        raise ScoutError(f"no HTTP response: {(out.stderr or out.stdout).strip()[:160]}")
    lines = head.split("\n")
    try:
        status = int(lines[0].split()[1])
    except (IndexError, ValueError):
        raise ScoutError(f"unreadable status line {lines[0][:80]!r}") from None
    headers = {}
    for line in lines[1:]:
        k, _, v = line.partition(":")
        headers[k.strip().lower()] = v.strip()
    try:
        data = json.loads(body) if body.strip() else {}
    except json.JSONDecodeError:
        data = {}
    return status, headers, data


class Search:
    """Paced, retried, paginated search. Every collaborator is injectable so the tests need no network."""

    def __init__(self, transport=gh_search, sleep=time.sleep, clock=time.time, log=say):
        self.transport, self.sleep, self.clock, self.log = transport, sleep, clock, log
        self.requests = 0
        self.started = clock()
        self.last = None
        self.remaining = None
        self.reset = 0.0

    def _wait(self, seconds: float) -> None:
        if self.clock() + seconds - self.started > DEADLINE:
            raise ScoutError(f"search would run past its {DEADLINE // 60}-minute deadline")
        if seconds > 0:
            self.sleep(seconds)

    def _pace(self) -> None:
        if self.remaining == 0:
            # The window is spent: wait for it to reset. Forgotten afterwards, so the next response's
            # headers say what the new window holds rather than this wait repeating for ever.
            self._wait(min(max(self.reset - self.clock(), 0) + 1, MAX_WAIT))
            self.remaining = None
        elif self.last is not None:
            self._wait(max(MIN_GAP - (self.clock() - self.last), 0))

    def page(self, q: str, page: int) -> dict:
        why = "no attempt made"
        for attempt in range(RETRIES):
            self._pace()
            self.last = self.clock()
            self.requests += 1
            try:
                status, headers, data = self.transport(q, page)
            except ScoutError as exc:
                why = str(exc)
                self._wait(5 * (attempt + 1))
                continue
            if "x-ratelimit-remaining" in headers:
                try:
                    self.remaining = int(headers["x-ratelimit-remaining"])
                    self.reset = float(headers.get("x-ratelimit-reset") or 0)
                except ValueError:
                    self.remaining = None
            message = str(data.get("message") or "")
            if status == 200:
                if data.get("incomplete_results"):
                    # Search timed out server-side and returned what it had. A partial page is a
                    # silent omission, which is the one failure this stage exists not to have.
                    why = "incomplete_results"
                    self._wait(5 * (attempt + 1))
                    continue
                return data
            if status in (403, 429) and ("rate limit" in message.lower()
                                         or headers.get("x-ratelimit-remaining") == "0"
                                         or "retry-after" in headers):
                why = f"HTTP {status} rate limited"
                after = headers.get("retry-after")
                wait = float(after) if after and after.isdigit() else max(self.reset - self.clock(), 0) + 1
                self._wait(min(max(wait, MIN_GAP), MAX_WAIT))
                self.remaining = None
                continue
            if status >= 500:
                why = f"HTTP {status}"
                self._wait(5 * (attempt + 1))
                continue
            # 422 and friends: the query is wrong and will be wrong every time.
            raise ScoutError(f"HTTP {status} for {q!r}: {message[:120]}")
        raise ScoutError(f"{q!r} page {page}: {why} after {RETRIES} attempts")

    def all(self, q: str) -> list[dict]:
        items: list[dict] = []
        for n in range(1, MAX_PAGES + 1):
            data = self.page(q, n)
            batch = data.get("items") or []
            items += batch
            total = int(data.get("total_count") or 0)
            if total > PER_PAGE * MAX_PAGES and n == 1:
                self.log(f"  ! {q!r}: {total:,} results, only the top {PER_PAGE * MAX_PAGES:,} by "
                         f"stars are reachable")
            if len(batch) < PER_PAGE or len(items) >= min(total, PER_PAGE * MAX_PAGES):
                break
        return items


# --- queries -----------------------------------------------------------------------------------
def rising_queries(today: date) -> list[str]:
    since = (today - timedelta(days=YOUNG_DAYS)).isoformat()
    young = [f"topic:{t} stars:>={YOUNG_STARS} created:>={since} fork:false archived:false"
             for t in TOPICS]
    core = [f"topic:{t} stars:>={CORE_STARS} created:>={ERA} fork:false archived:false"
            for t in CORE_TOPICS]
    return young + core


def list_queries(today: date) -> list[str]:
    since = (today - timedelta(days=LIST_PUSHED_DAYS)).isoformat()
    return [f"awesome in:name topic:{t} stars:>={LIST_STARS} pushed:>={since} fork:false archived:false"
            for t in LIST_TOPICS]


# --- judging one repo --------------------------------------------------------------------------
def topics_of(item: dict) -> set[str]:
    return {str(t).lower() for t in item.get("topics") or ()}


def is_list(item: dict) -> bool:
    return "awesome" in str(item.get("name") or "").lower()


def agentic(item: dict) -> bool:
    name = str(item.get("name") or "").lower()
    return any(w in name for w in NAME_AGENTIC) or bool(
        AGENTIC.search(f"{item.get('name') or ''} {item.get('description') or ''}"))


def hygiene(item: dict) -> str:
    """The rules a repo and a list share. "" for clean, else the reason it is not."""
    desc = str(item.get("description") or "").strip()
    if item.get("fork"):
        return "fork"
    if item.get("archived"):
        return "archived"
    if item.get("disabled"):
        return "disabled"
    if item.get("mirror_url") or MIRROR.search(desc):
        return "mirror"
    if not desc:
        return "no description"
    if SPAM.search(desc) or topics_of(item) & SPAM_TOPICS:
        return "spam"
    return ""


def tier(item: dict, today: date) -> str:
    """"young", "core", or "" -- which bar this repo clears, if any."""
    stars = int(item.get("stargazers_count") or 0)
    created = str(item.get("created_at") or "")[:10]
    tops = topics_of(item)
    if (created >= (today - timedelta(days=YOUNG_DAYS)).isoformat() and stars >= YOUNG_STARS
            and tops & set(TOPICS)):
        return "young"
    if stars >= CORE_STARS and created >= ERA and tops & set(CORE_TOPICS):
        return "core"
    return ""


def verdict(item: dict, today: date, curated: set[str]) -> str:
    """"" if this search result belongs in the scouted set, else the reason it does not."""
    if str(item.get("full_name") or "").lower() in curated:
        return "curated list"
    bad = hygiene(item)
    if bad:
        return bad
    if is_list(item):
        return "list"
    if not agentic(item):
        return "off-topic"
    if not tier(item, today):
        return "below threshold"
    return ""


def section_of(item: dict) -> str:
    """The family whose topics this repo carries most of; the earlier one on a tie; then the two
    fallbacks, generic agent topics before harness names."""
    tops = topics_of(item)
    best, score = "", 0
    for section, family in FAMILIES:
        n = len(tops & set(family))
        if n > score:
            best, score = section, n
    if best:
        return best
    if tops & set(GENERIC[1]):
        return GENERIC[0]
    if tops & set(HARNESS[1]):
        return HARNESS[0]
    return GENERIC[0]


def list_verdict(item: dict, today: date, curated: set[str]) -> str:
    if str(item.get("full_name") or "").lower() in curated:
        return "already a source"
    bad = hygiene(item)
    if bad:
        return bad
    if not is_list(item):
        return "not a list"
    if int(item.get("stargazers_count") or 0) < LIST_STARS:
        return "below threshold"
    if str(item.get("pushed_at") or "")[:10] < (today - timedelta(days=LIST_PUSHED_DAYS)).isoformat():
        return "stale"
    if not (topics_of(item) & set(LIST_TOPICS) or agentic(item)):
        return "off-topic"
    return ""


# --- the two ledgers ---------------------------------------------------------------------------
def load(path: Path, key: str) -> dict:
    if not path.exists():
        return {"version": 1, key: {}}
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        sys.exit(f"{path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path} does not "
                 f"parse. It is committed, so restore it from git rather than let this stage start "
                 f"over: an empty scouted set would delete every scouted row.")
    state.setdefault("version", 1)
    state.setdefault(key, {})
    return state


def dump(state: dict) -> str:
    # Sorted, one key per line, the same shape as state/first-seen.json: this is committed on every run
    # that changes it, so the diff should be the repos that arrived and nothing else.
    return json.dumps(state, indent=1, sort_keys=True, ensure_ascii=False) + "\n"


def save(path: Path, state: dict) -> bool:
    """Write only when the bytes would change, so an idle day leaves no diff and no mtime churn."""
    text = dump(state)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def ignored(ledger: dict) -> set[str]:
    """Lower-cased names a person has put under the ledger's `ignore` key, by hand, with a reason.

    The one way to overrule the rules. Deleting a scouted repo from `repos` does nothing on its own --
    it still qualifies, so tomorrow's run adds it straight back -- and the same goes for a candidate
    list someone has looked at and declined. `"ignore": {"owner/repo": "why"}` in either ledger keeps it
    out for good, and the stage carries the key across runs untouched.
    """
    return {str(k).lower() for k in (ledger.get("ignore") or {})}


def merge_repos(ledger: dict, items: list[dict], today: date, curated: set[str],
                reset: bool = False) -> dict:
    """The next scouted set, from the last one and everything today's search returned.

    Returns a report: `added`, `dropped` (with reasons), `moved` (section changed), `renamed`.
    Mutates `ledger` in place. Sticky: an entry today's search did not return is left alone -- unless
    `reset`, which keeps only what qualifies today, `since` intact. Stickiness makes every rule one-way
    (tightening a threshold stops new arrivals and removes nothing), so `--reset` is how a tightened
    rule is applied to the repos already scouted.
    """
    repos = ledger["repos"]
    report = {"added": [], "dropped": [], "moved": [], "renamed": []}
    skip = ignored(ledger)
    for nwo in [n for n in repos if n.lower() in skip]:
        repos.pop(nwo)
        report["dropped"].append((nwo, "ignored"))
    by_id = {e.get("id"): nwo for nwo, e in repos.items() if e.get("id") is not None}
    by_lower = {nwo.lower(): nwo for nwo in repos}
    qualified: set[str] = set()
    seen: dict[str, dict] = {}
    for it in items:
        name = str(it.get("full_name") or "")
        if name and "/" in name and name.lower() not in skip:
            seen.setdefault(name, it)
    for name in sorted(seen, key=str.lower):
        it = seen[name]
        why = verdict(it, today, curated)
        # The ledger's spelling of this repo, found by id first so a rename keeps its `since`.
        old = by_id.get(it.get("id")) or by_lower.get(name.lower())
        if old and old != name:
            repos[name] = repos.pop(old)
            by_lower.pop(old.lower(), None)
            by_lower[name.lower()] = name
            report["renamed"].append((old, name))
            old = name
        if old:
            if why in QUALITY:
                repos.pop(old)
                by_lower.pop(old.lower(), None)
                report["dropped"].append((old, why))
                continue
            if not why:
                qualified.add(old)
            entry = repos[old]
            entry["id"] = it.get("id", entry.get("id"))
            section = section_of(it)
            if section != entry.get("section"):
                report["moved"].append((old, entry.get("section"), section))
                entry["section"] = section
            continue
        if why:
            continue
        repos[name] = {"id": it.get("id"), "section": section_of(it), "since": today.isoformat()}
        by_lower[name.lower()] = name
        qualified.add(name)
        report["added"].append(name)
    if reset:
        for nwo in sorted((n for n in repos if n not in qualified), key=str.lower):
            repos.pop(nwo)
            report["dropped"].append((nwo, "reset"))
    return report


def merge_lists(ledger: dict, items: list[dict], today: date, curated: set[str]) -> dict:
    """The next candidate-list set. Not sticky: this is a to-do list, so it is today's answer, with
    each survivor's `first_seen` carried over from the last one."""
    before = ledger["lists"]
    after: dict[str, dict] = {}
    skip = ignored(ledger)
    for it in items:
        name = str(it.get("full_name") or "")
        if not name or name in after or name.lower() in skip or list_verdict(it, today, curated):
            continue
        was = before.get(name) or next((v for k, v in before.items() if k.lower() == name.lower()), {})
        after[name] = {"stars": int(it.get("stargazers_count") or 0),
                       "description": str(it.get("description") or "").strip()[:300],
                       "pushed_at": str(it.get("pushed_at") or "")[:10],
                       "first_seen": was.get("first_seen") or today.isoformat()}
    report = {"added": sorted(set(after) - set(before)), "dropped": sorted(set(before) - set(after))}
    ledger["lists"] = after
    return report


# --- the document --------------------------------------------------------------------------------
def render(ledger: dict) -> str:
    """The synthetic source, as Markdown the bullet parser reads. A pure function of the ledger.

    No dates, no star counts and no descriptions: the document is the scouted *set*, so its digest is
    what tells the daily gate the set moved. The blurb the atlas prints comes from GitHub's own
    description, which `11_fetch_all` refetches every run. A section this module no longer names is
    still rendered, after the known ones, so a renamed family fails loudly in `10_parse_sources`'s
    taxonomy check instead of silently dropping its repos.
    """
    by_section: dict[str, list[str]] = {}
    for nwo, e in ledger["repos"].items():
        by_section.setdefault(e.get("section") or GENERIC[0], []).append(nwo)
    order = SECTIONS + sorted(s for s in by_section if s not in SECTIONS)
    out = ["# Scouted on GitHub", "",
           "Agentic repositories found by GitHub search rather than on a curated list. Generated by",
           "scripts/12_scout.py from state/scout-repos.json -- edit the ledger, not this file.", ""]
    for section in order:
        names = sorted(by_section.get(section, ()), key=lambda n: (n.lower(), n))
        if not names:
            continue
        out += [f"## {section}", ""]
        out += [f"- [{n.split('/', 1)[1]}](https://github.com/{n})" for n in names]
        out.append("")
    return "\n".join(out)


def write_doc(ledger: dict) -> bool:
    text = render(ledger)
    if DOC.exists() and DOC.read_bytes() == text.encode("utf-8"):
        return False
    DOC.parent.mkdir(parents=True, exist_ok=True)
    # LF on every platform: the bytes are what the gate digests, and the cache is shared with CI.
    DOC.write_bytes(text.encode("utf-8"))
    return True


# --- reporting -----------------------------------------------------------------------------------
def curated_nwos() -> set[str]:
    return {s["nwo"].lower() for s in b10.SOURCES if not s.get("synthetic")}


def summary(rising: dict, lists: dict, repos: dict, cands: dict, stars: dict[str, int]) -> str:
    """Markdown for $GITHUB_STEP_SUMMARY and the log: what moved, and the candidates worth a look."""
    out = ["### Scout", ""]
    if rising.get("error"):
        out.append(f"**Rising repos: search failed, kept the previous {len(repos):,}** -- "
                   f"{rising['error']}")
    else:
        out.append(f"Rising repos: {len(repos):,} scouted · +{len(rising['added'])} new · "
                   f"-{len(rising['dropped'])} dropped · {len(rising['moved'])} re-filed · "
                   f"{len(rising.get('renamed', ()))} renamed")
        if rising["added"]:
            out += ["", "| new today | stars | section |", "|---|---:|---|"]
            top = sorted(rising["added"], key=lambda n: (-stars.get(n, 0), n.lower()))[:15]
            out += [f"| [{n}](https://github.com/{n}) | {stars.get(n, 0):,} | "
                    f"{repos[n]['section']} |" for n in top]
        for n, why in rising["dropped"][:15]:
            out.append(f"- dropped {n}: {why}")
        for old, new in rising.get("renamed", [])[:15]:
            out.append(f"- renamed {old} -> {new}")
    out.append("")
    if lists.get("error"):
        out.append(f"**Candidate lists: search failed, kept the previous {len(cands):,}** -- "
                   f"{lists['error']}")
    else:
        out.append(f"Candidate lists not in SOURCES: {len(cands):,} · +{len(lists['added'])} new "
                   f"· -{len(lists['dropped'])} gone")
    if cands:
        out += ["", "| list | stars | pushed | first seen | description |", "|---|---:|---|---|---|"]
        top = sorted(cands, key=lambda n: (-cands[n]["stars"], n.lower()))[:15]
        for n in top:
            c = cands[n]
            desc = c["description"].replace("|", "\\|")[:90]
            new = " (new)" if n in lists.get("added", ()) else ""
            out.append(f"| [{n}](https://github.com/{n}){new} | {c['stars']:,} | {c['pushed_at']} | "
                       f"{c['first_seen']} | {desc} |")
    return "\n".join(out) + "\n"


def run(today: date, search: Search, dry_run: bool = False, reset: bool = False, log=say) -> dict:
    """The whole stage. Returns what happened, for the caller and the tests."""
    curated = curated_nwos()
    repos = load(REPOS, "repos")
    cands = load(LISTS, "lists")
    stars: dict[str, int] = {}

    rising: dict = {}
    pool: list[dict] = []
    try:
        for q in rising_queries(today):
            got = search.all(q)
            pool += got
            log(f"  {len(got):5d}  {q}")
        rising = merge_repos(repos, pool, today, curated, reset=reset)
        stars = {str(i.get("full_name")): int(i.get("stargazers_count") or 0) for i in pool}
    except ScoutError as exc:
        repos = load(REPOS, "repos")      # untouched: nothing was merged before the failure
        rising = {"error": str(exc)}
        log(f"::warning title=Scout search failed::rising repos kept as they were -- {exc}")

    # The list half reads the rising half's results as well as its own -- an awesome list a rising
    # query returned is as much a candidate as one the list queries did -- so it cannot be trusted
    # without them. A failed rising search fails both halves, which is also the cheaper outcome: a
    # rate limit that stopped the first would stop the second.
    lists: dict = {}
    try:
        if rising.get("error"):
            raise ScoutError("not attempted: the rising search failed first")
        found = list(pool)
        for q in list_queries(today):
            got = search.all(q)
            found += got
            log(f"  {len(got):5d}  {q}")
        lists = merge_lists(cands, found, today, curated)
    except ScoutError as exc:
        cands = load(LISTS, "lists")
        lists = {"error": str(exc)}
        log(f"::warning title=Scout list search failed::candidate lists kept as they were -- {exc}")

    wrote = {}
    if not dry_run:
        wrote = {"repos": save(REPOS, repos), "lists": save(LISTS, cands), "doc": write_doc(repos)}
    return {"rising": rising, "lists": lists, "repos": repos["repos"], "cands": cands["lists"],
            "stars": stars, "wrote": wrote, "requests": search.requests}


def status() -> None:
    repos = load(REPOS, "repos")["repos"]
    cands = load(LISTS, "lists")["lists"]
    per = {}
    for e in repos.values():
        per[e.get("section")] = per.get(e.get("section"), 0) + 1
    print(f"{len(repos):,} scouted repos in {REPOS.relative_to(ROOT).as_posix()}")
    for s in SECTIONS + sorted(k for k in per if k not in SECTIONS):
        if per.get(s):
            print(f"  {per[s]:5d}  {s}")
    print(f"{len(cands):,} candidate lists in {LISTS.relative_to(ROOT).as_posix()}")
    same = DOC.exists() and DOC.read_bytes() == render(load(REPOS, "repos")).encode("utf-8")
    print(f"document {DOC.relative_to(ROOT).as_posix()}: "
          + ("current" if same else "stale -- run with --offline" if DOC.exists() else "absent"))


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--offline", action="store_true",
                    help="no network: render the document from the committed ledger")
    ap.add_argument("--dry-run", action="store_true", help="search and report, write nothing")
    ap.add_argument("--status", action="store_true", help="report the ledgers; no network")
    ap.add_argument("--strict", action="store_true", help="exit non-zero if a search failed")
    ap.add_argument("--reset", action="store_true",
                    help="keep only the scouted repos that qualify today -- how a tightened rule reaches "
                         "repos already scouted, since the ledger is otherwise sticky")
    args = ap.parse_args()

    if args.status:
        status()
        return
    if args.offline:
        repos = load(REPOS, "repos")
        changed = write_doc(repos)
        print(f"{len(repos['repos']):,} scouted repos -> {DOC.relative_to(ROOT).as_posix()} "
              f"({'rewritten' if changed else 'unchanged'})")
        return

    today = date.today()
    result = run(today, Search(), dry_run=args.dry_run, reset=args.reset)
    text = summary(result["rising"], result["lists"], result["repos"], result["cands"],
                   result["stars"])
    print(text)
    print(f"{result['requests']} search requests"
          + ("" if args.dry_run else f" · wrote {', '.join(k for k, v in result['wrote'].items() if v) or 'nothing'}"))
    out = os.environ.get("GITHUB_STEP_SUMMARY")
    if out and not args.dry_run:
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(text)
    failed = bool(result["rising"].get("error") or result["lists"].get("error"))
    if failed and args.strict:
        sys.exit(1)


if __name__ == "__main__":
    main()
