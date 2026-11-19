"""The merged atlas's rows: one listing per entry, one row per repo, one star count, one order.

Not a stage any more. This file used to end in `main()`, which wrote the two Excel workbooks
(`Awesome-Agentic-Atlas-DARK.xlsx` and `-LIGHT.xlsx`) the weekly job released every Sunday. The
spreadsheet edition was retired in November 2026. The website is the maintained edition, the last
pair of workbooks stays downloadable from release `v2026.10.22` but is never rebuilt, and everything
that only existed to write them went with it: the sheet builders, the eight-hue colour slots, the
cover branding, the image pool (`media.py`), the slicer injector (`18_slicers.py`), the Excel-driving
checks (`08_verify.py`, `09_pdf.py`) and the orchestrators-only builder (`07_build.py`).

What is left is what the other surfaces were already importing from here, because the Markdown edition
and the site have always read the same rows the workbook did rather than re-deriving them, so the
three could never disagree about a count:

  prepare / shot_key        normalise the raw listings and give each one the key its shot is filed under
  canonicalise_nwo          one spelling per repo, through case and renames
  repo_pool / platform_pool one row per repo across every list, earliest listing first, longest blurb
  platform_rows             the rows that qualify for one platform, strongest evidence first
  star_map / combined_stars the only definition of a repo's stars and of the collection's total
  order_rows                a list's own rows in its published order (bucket, then stars)
  SHEETS, LIST_TITLE, ...   which lists get a page of their own, and every list's display name

The filename and the `b16` module name are kept on purpose. `17_markdown`, `19_pages` (through
`b17.b16`), `taxonomy.load`, `devfixture` and their tests all load this file by path, and renaming it
would touch every one of them for no change in behaviour.
"""
import sys
import importlib.util
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import hosts  # noqa: E402
from buckets import bucket_order  # noqa: E402
# Safe to import at module scope: taxonomy only reaches back into this module inside `load()`, which
# nothing here calls, so there is no cycle.
import taxonomy as tax  # noqa: E402

spec = importlib.util.spec_from_file_location("b10", Path(__file__).parent / "10_parse_sources.py")
b10 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b10)


# Which lists get a page of their own and a short display name, in display order. Ten of the
# thirty-nine, and deliberately so. The name is the workbook's (each of these was once a sheet tab),
# kept because the Markdown edition's per-list pages and the site's `listed_by` labels still read it,
# and the pages that cut across every list -- leaderboard, platforms, topics -- already carry every row
# from every source. So this list answers "which lists are worth reading one at a time", which is a
# curation question, and it is not the same question as "which lists is the atlas built from".
# Anything that means the second one must read SOURCES; see LIST_TITLE.
SHEETS = [
    ("agents", "Agents (kyrolabs)", "kyrolabs/awesome-agents",
     "Frameworks, dev tools and agent products, as curated by kyrolabs."),
    ("e2b", "Agents (e2b)", "e2b-dev/awesome-ai-agents",
     "e2b's catalogue of AI agents and the frameworks behind them."),
    ("agents2026", "AI Agents 2026", "caramaschiHG/awesome-ai-agents-2026",
     "A 2026 market survey — commercial products alongside open source."),
    ("claudecode", "Claude Code", "hesreallyhim/awesome-claude-code",
     "Commands, hooks, status lines and tooling for Claude Code."),
    ("opencode", "Opencode", "awesome-opencode/awesome-opencode",
     "Plugins, themes, agents and projects for the opencode terminal agent."),
    ("harness", "Harness Engineering", "ai-boost/awesome-harness-engineering",
     "How agent harnesses are built — primitives, papers and reference implementations."),
    ("patterns", "Agentic Patterns", "nibzard/awesome-agentic-patterns",
     "Named design patterns for agentic systems. Each row is a write-up, not a tool."),
    ("skills", "Agent Skills", "heilcheng/awesome-agent-skills",
     "Skill directories by vendor, plus community-published skills."),
    ("skills_aas", "AAS Skill Sources", "sickn33/agentic-awesome-skills",
     "The upstream repos the Agentic Awesome Skills library aggregates."),
    ("llmapps", "LLM App Templates", "shubhamsaboo/awesome-llm-apps",
     "Runnable example apps. Each row is a folder inside the one repo."),
]
SHEET_TITLE = {k: t for k, t, *_ in SHEETS}

# Every source's display name, which is not the same set as SHEETS. `listed_by` on the leaderboard,
# the topic pages and the four platform pages is built from this: those pages hold rows from every
# list in `SOURCES`, so a map covering only the ten in SHEETS left every other list printing
# a raw internal key -- a reader saw "Listed by: cc_toolkit_rohitg00" where the other rows said
# "Claude Code". SHEETS wins where it has an entry, so the ten already-shipped names do not move, and
# `orchestrators` keeps the short label it has always been published under rather than its SOURCES
# title. Everything else takes the title its SOURCES entry already declares.
# The sources that are not lists. The scout (`12_scout.py`) is a search, not a curator, so it decides
# which repos are in the atlas but never counts toward `list_count` or `listed_by`: those are the
# consensus the site sells -- "named by three lists" -- and a search agreeing with a list is not a second
# opinion. A repo only the scout found has `list_count` 0 and an empty `listed_by`, and every surface says
# "found by GitHub search" for it instead of a count.
SYNTHETIC = frozenset(s["key"] for s in b10.SOURCES if s.get("synthetic"))
LIST_TITLE = {**{s["key"]: s["title"] for s in b10.SOURCES},
              "orchestrators": "Orchestrators", **SHEET_TITLE}


# One page per platform, built from every list at once. Order is install-base order,
# which is also the order the counts come out in.
PLATFORMS = [
    ("Windows", "win_native",
     "runs natively on Windows, or is reachable through WSL2",
     "Native first, then WSL2-only, each block by stars. A Homebrew-only project that ships a "
     "Windows build shows its releases page instead of a command that cannot run here."),
    ("macOS", "macos",
     "runs on macOS — Apple silicon or Intel",
     "Confirmed first, then inferred, each block by stars. Confirmation means a .dmg/.pkg asset or "
     "explicit README prose; inference from a portable runtime alone only ever earns Likely."),
    ("Linux", "linux",
     "runs on Linux",
     "Confirmed first, then inferred, each block by stars. Nearly every container and CI path "
     "implies Linux, so this is the widest of the four — filter on Conf. to tighten it."),
    ("Docker", "docker",
     "ships a container image, a Dockerfile or a compose file",
     "For building a container environment. Membership is evidence-based, not aspirational: a row "
     "is here because something in the repo or its README actually names a container."),
]

DASH = "—"


# ------------------------------------------------------------------ one row per repo
def _thin(rec) -> bool:
    """A listing with nothing of its own to report: a folder in someone else's repo, or a dead link."""
    return rec.get("kind") == "subpath" or bool(rec.get("unavailable"))


def offer_blurb(a: dict, r: dict) -> None:
    """Longest blurb wins, except that an advisory listing's never displaces one already there.

    A scouted listing has no blurb of its own -- the scout writes no descriptions -- so what it offers
    is GitHub's description of the repo, which is also what a curated listing falls back to when its
    curator wrote nothing. Measured on length alone it would replace a curator's sentence with the
    repo's own tagline whenever the tagline is longer, which is the opposite of the rule `14_classify_all`
    states: the list's own blurb is usually the better-written one. So it only fills a gap.
    """
    blurb = r.get("blurb") or r.get("description") or ""
    if r.get("source") in tax.ADVISORY and a.get("blurb"):
        return
    if len(blurb) > len(a.get("blurb") or ""):
        a["blurb"] = blurb


def repo_pool(records, orch, label, keep=None):
    """One row per repo across every list, merged: earliest listing wins, longest blurb wins.

    `keep` decides which listings are eligible. Two callers want different answers to that and both
    are right: a platform page must drop the listings that have no OS support of their own, while a
    topic page must keep them, because a skill that lives in a folder still belongs on the Agent
    Skills page even though nothing about it can be measured or ranked.
    """
    pool: dict[str, dict] = {}
    for r in [dict(x, source="orchestrators") for x in orch] + records:
        nwo = r.get("nwo")
        if not nwo or (keep is not None and not keep(r)):
            continue
        a = pool.get(nwo)
        if a is None:
            a = pool[nwo] = dict(r, sources=set())
        elif _thin(a) and not _thin(r):
            # Promote: the row this repo was first seen as cannot report its own stars or platforms,
            # and a later listing can. Never fires for `platform_pool`, whose `keep` makes every
            # eligible listing a full one; it exists for the pools that keep the thin listings.
            a = pool[nwo] = dict(r, sources=a["sources"], blurb=a.get("blurb") or "")
        if r["source"] not in SYNTHETIC:
            a["sources"].add(r["source"])
        offer_blurb(a, r)
    out = []
    for nwo, a in pool.items():
        a["list_count"] = len(a["sources"])
        a["listed_by"] = ", ".join(sorted(label.get(s, s) for s in a["sources"]))
        a["shot_key"] = a.get("shot_key") or nwo.replace("/", "__")
        a["blurb"] = a["blurb"] or a.get("description") or ""
        for k in ("win_native", "win_wsl2", "macos", "linux", "docker", "cloud"):
            a[k] = a.get(k) or DASH
        out.append(a)
    return out


def platform_pool(records, orch, label):
    """One row per repo across every list — a platform question is about the tool, not the listing.

    Site-only and sub-path entries never reach here: they have no repo of their own, so every OS
    column on them is a dash, and a platform page that listed them would be inviting the reader to
    filter on a value that was never measured.
    """
    return repo_pool(records, orch, label,
                     keep=lambda r: r.get("kind") != "subpath" and not r.get("unavailable"))


def merged_shots(shots, orch_shots):
    """`shots_all` keyed by shot_key, plus the original list's own map re-keyed to match.

    Both maps name files in the same `cache/shots` directory, so the basename is enough to join
    them; the original pipeline just stored absolute paths under different field names.
    """
    out = dict(shots)
    for nwo, v in orch_shots.items():
        key = nwo.replace("/", "__")
        if key in out:
            continue
        light, dark = v.get("shot_light") or "", v.get("shot_dark") or ""
        out[key] = dict(key=key, light=Path(light).name, dark=Path(dark).name,
                        tier=v.get("shot_kind") or "", shot_url=v.get("shot_url") or "")
    return out


RANK = {"Yes": 2, "Likely": 1}


def platform_rows(pool, field):
    """Rows that qualify for one platform, strongest evidence first, then by stars.

    Windows is the one platform with two ways in, so WSL2 counts toward the sort but cannot on its
    own outrank a native build: a reader filtering this page wants the native ones at the top.
    """
    if field == "win_native":
        def score(r):
            return RANK.get(r["win_native"], 0) * 2 + (1 if r["win_wsl2"] == "Yes" else 0)
    else:
        def score(r):
            return RANK.get(r[field], 0)
    rows = [r for r in pool if score(r) > 0]
    rows.sort(key=lambda r: (-score(r), -r.get("stars", 0), r["name"].lower()))
    return rows


def platform_install(r, platform: str) -> str:
    """A `brew install` line is unusable on Windows. Point at the build the project publishes."""
    cmd = r.get("install_cmd") or ""
    if platform == "Windows" and r.get("install_method") == "brew" and r["win_native"] == "Yes":
        return f"{r['url']}/releases/latest"
    return cmd


# ------------------------------------------------------------------ data prep
def prepare(records, shots):
    for r in records:
        if r.get("license") in ("NOASSERTION", "NONE", "", None):
            r["license"] = ""
        r["shot_key"] = shot_key(r)
    return records


def shot_key(rec):
    import hashlib
    if rec["kind"] == "site":
        return "site__" + hashlib.sha1(rec["url"].encode()).hexdigest()[:16]
    base = (rec.get("nwo") or "x").replace("/", "__")
    if rec["kind"] == "subpath":
        return base + "__" + hashlib.sha1(rec["url"].encode()).hexdigest()[:10]
    return base


def canonicalise_nwo(records, orch, meta) -> int:
    """Give every repo the one name GitHub says it has, so a repo named twice is one row and not two.

    Two different ways the same repo arrives under two names, and both have to be folded or the
    leaderboard ranks it twice, the platform pool counts it twice, and the "listed by N lists"
    consensus score undercounts itself:

      Case. GitHub treats owner/repo case-insensitively, and the source tables were typed by hand, so
        three repos arrive as both `e2b-dev/E2B` and `e2b-dev/e2b`.
      Renames. A repo that moved keeps serving its old URL as a redirect, so lists written at
        different times name it differently and every one of them still works. Twenty repos are in here
        under a stale name -- `OpenDevin/OpenDevin`, `All-Hands-AI/OpenHands` and `OpenHands/OpenHands`
        are one project under three -- and `affaan-m/everything-claude-code` was on the leaderboard
        twice at 246,813 stars each, once as itself and once as `affaan-m/ECC`.

    `meta.json`'s `nameWithOwner` is the API's answer to both at once: it is what the repo is called
    now, whatever was asked for. Where a repo was never fetched there is no answer, and the first
    spelling seen wins so that at least the two spellings agree with each other.

    Called *after* `prepare`, deliberately. `shot_key` is derived from the original spelling and the
    files in cache/shots are named to match, so recomputing it here would break every lookup it fixed.
    """
    # Resolve through at most one hop, then trust the case pass. A rename chain long enough to matter
    # would have to have been re-fetched mid-chain, and following it blindly can loop: two repos that
    # swapped names would point at each other for ever.
    canon: dict[str, str] = {}
    for asked, m in meta.items():
        now = (m or {}).get("nameWithOwner") or asked
        canon[asked.lower()] = ((meta.get(now) or {}).get("nameWithOwner") or now)
    for k, v in list(canon.items()):
        canon.setdefault(v.lower(), v)

    everything = orch + records
    for r in everything:
        if r.get("nwo"):
            canon.setdefault(r["nwo"].lower(), r["nwo"])
    fixed = 0
    for r in everything:
        was = r.get("nwo")
        if not was:
            continue
        now = canon[was.lower()]
        if now != was:
            r["nwo"] = now
            # owner_of/name_of rather than a split on the first slash: a GitLab nwo is host-qualified
            # and its owner is everything before the project's own name (hosts.py).
            r["owner"], r["repo"] = hosts.owner_of(now), hosts.name_of(now)
            # Only the plain repo URL. A link into a subpath or a release keeps its old spelling,
            # which still redirects, because rewriting just the prefix could invent a path.
            if r.get("url") == hosts.web_url(was):
                r["url"] = hosts.web_url(now)
            fixed += 1
    return fixed


def star_map(records, orch, meta) -> dict[str, int]:
    """One star count per repo — the only place this question gets answered.

    Three surfaces printed a combined star figure — the workbook cover (since retired), the Markdown hub
    and the category report — and they were printing 12,494,678, 12,494,028 and 12,494,807. Each had summed a different
    set with a differently-sourced number: the rows the Leaderboard admits, the platform pool, and a
    per-repo maximum across listings. All three were defensible, no two agreed, and for the headline
    number on a cover that is simply wrong. So there is one map, built once, and everything reads it.

    `meta.json` wins, because it is what the API said and it does not vary by which listing was read
    first. Where it has no count — 82 repos, fetched before that field was recorded — the largest figure
    any listing carries stands in, since discarding real data in favour of a zero would be worse.

    Excluded, and both deliberately: a listing whose `kind` is `subpath` is a folder inside someone
    else's repo and has no stars of its own, and an `unavailable` repo has nothing to count. A repo that
    is a subpath on one list and a real entry on another still appears, via the real entry.

    Call after `canonicalise_nwo`, or a repo under two names appears twice.
    """
    meta_ci = {k.lower(): v for k, v in meta.items()}
    best: dict[str, int] = {}
    for r in list(records) + list(orch):
        nwo = r.get("nwo")
        if not nwo or r.get("kind") == "subpath" or r.get("unavailable"):
            continue
        api = (meta.get(nwo) or meta_ci.get(nwo.lower()) or {}).get("stargazerCount")
        best[nwo] = api or max(best.get(nwo, 0), r.get("stars") or 0)
    return {n: s for n, s in best.items() if s > 0}


def combined_stars(records, orch, meta) -> tuple[int, int]:
    """The collection's combined star count, and how many repos it is spread across."""
    stars = star_map(records, orch, meta)
    return sum(stars.values()), len(stars)


def order_rows(rows, source):
    idx = {b: i for i, b in enumerate(bucket_order(source))}
    rows.sort(key=lambda r: (idx.get(r["bucket"], 99), -r["stars"], r.get("src_order", 0),
                             r["name"].lower()))
    seen = {}
    for r in rows:
        seen[r["bucket"]] = seen.get(r["bucket"], 0) + 1
        r["group_rank"] = seen[r["bucket"]]
    return rows

