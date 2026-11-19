"""Upstream drift: keep publishing when a list changes under us, and keep every decision it forces visible.

Thirty-nine lists the atlas does not control are pulled every day, and each one is free to rename a
heading, translate its README, add a shelf or rearrange itself. Two modules refuse to guess about that,
on principle: `taxonomy.category_of` raises on a `(source, section)` it does not name, because
re-filing is the thing that module exists to make deliberate, and `buckets.py` will not hand a ninth
hue to a palette that has eight. `10_parse_sources.unmapped` asks both questions before the expensive
stages, and until this module existed its answer was `sys.exit(1)`.

That made every curator's edit somebody else's outage. libukai translating eight headings to English
held the site on 2026-11-01 for over two weeks; punkpeye adding "Jobs", awesome-claude-code adding
"Mods", awesome-llm-apps adding "Standalone Apps & Tools" each did the same for a day. Each time the fix
was one line, and each time the site was frozen until somebody wrote it.

So there are two modes, and the difference between them is who makes the decision and when.

  STRICT (the default, and every local run and every test): unchanged. An unmapped section or a ninth
  hue stops the parse and prints what to add.

  PROVISIONAL (`AAA_PROVISIONAL=1`, which the daily and weekly workflows set for the whole job): the
  parse files each unmapped section somewhere defensible *for this run only*, folds a ninth hue into
  the sheet's last bucket, writes every such placement to `cache/provisional.json`, and carries on.
  Nothing is filed for good. `taxonomy.py` and `buckets.py` are not edited -- the placements live in
  the cache, every run recomputes them from scratch, and they disappear the moment a person adds the
  real key. What a person sees instead is a `::warning` per placement, a step-summary block with the
  exact lines to paste, and `cache/drift-proposal.json`, which the CI stream turns into a draft PR by
  running `scripts/apply_drift_proposal.py`.

The env var, not only a flag, because the readers are not the parse. `14_classify_all`, `16_build_all`,
`17_markdown` and `19_pages` each import `taxonomy` and `buckets` in processes of their own, so "honour
the placements for this run" has to be something every stage of the run can see. And honoured *only*
under the var: a `cache/provisional.json` left on a laptop by a CI-style run is inert to every strict
process that opens the same cache, so a stale placement cannot quietly re-file anything later. A strict
parse also deletes the file, for the same reason.

WHERE A PROVISIONAL SECTION GOES, strongest evidence first:

  membership -- most of its entries were filed under one old section in the previous copy of the list,
                and that old section is mapped. A rename or a translation keeps the entries and changes
                the heading, so the entries are the evidence. `pull_sources.py` is the only stage that
                holds both copies at once -- it parses the old and the new to diff them anyway -- so it
                records which old section each new one came from, in `cache/section-moves.json`. Where
                that ledger has nothing -- the change reached the cache before the ledger saw it -- the
                same evidence is read off the atlas's own committed pages, `mega-list/lists/*.md`.
  position   -- the list has the same number of sections in the same slots, and the one this replaced
                is mapped. The fallback for a renamed section whose entries all changed too.
  similar    -- its name is close (difflib, >= SIMILAR) to a section of the same list the taxonomy maps.
                Orphans first -- a mapped section the list no longer produces is what a rename leaves
                behind -- then the list's current mapped sections.
  leftover   -- every other newcomer in the list was traced, and exactly one newcomer and one vanished
                mapped section remain, so they are paired.
  modal      -- none of the above: the category most of the list's rows already land in. This is the
                guess the taxonomy refuses to make permanently, made for one run and labelled as such.

A section that inherits an old section's mapping also inherits its bucket, so a rename keeps its hue.
"""
from __future__ import annotations

import difflib
import hashlib
import html
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"

ENV = "AAA_PROVISIONAL"
PLACEMENTS = CACHE / "provisional.json"
MOVES = CACHE / "section-moves.json"
PROPOSAL = CACHE / "drift-proposal.json"
PROPOSAL_MD = CACHE / "drift-proposal.md"
PULL_REPORT = CACHE / "pull-report.json"

HUES = 8
# Half of a new section's entries from one old section is a rename; less is a reshuffle, and reading a
# reshuffle as a rename would carry one shelf's category onto entries mostly drawn from others.
MEMBERSHIP = 0.5
# difflib's ratio. 0.75 accepts "Testing & Evaluation" for "Testing and Evaluation" (0.86) and
# "Open-Source Software" for "Open Source Software" (0.95), and rejects "Jobs" for "Docs" (0.75 is
# exactly where four-letter words start matching each other, so the comparison is strict `>`).
SIMILAR = 0.75


def enabled() -> bool:
    return os.environ.get(ENV, "").strip().lower() in {"1", "true", "yes", "on"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def warn(title: str, message: str) -> None:
    """A workflow annotation on Actions, a plain stderr line anywhere else.

    Annotations are what make a provisional run impossible to miss: they show on the run's summary page
    and on the commit, not only deep in a log nobody opens on a green day. Commas and newlines in the
    title would end it early, so they are flattened rather than escaped.
    """
    title = title.replace("\n", " ").replace(",", ";").replace("::", ":")
    message = message.replace("%", "%25").replace("\r", "").replace("\n", "%0A")
    if os.environ.get("GITHUB_ACTIONS") == "true":
        print(f"::warning title={title}::{message}", flush=True)
    else:
        print(f"  ! {title}: {message.replace('%0A', ' ').replace('%25', '%')}", file=sys.stderr, flush=True)


def summary(markdown: str) -> None:
    out = os.environ.get("GITHUB_STEP_SUMMARY")
    if out:
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(markdown.rstrip() + "\n\n")


def utf8_console() -> None:
    """Headings are not all ASCII -- libukai's were Chinese until 2026-10 -- and a Windows console
    encodes stdout as cp1252, so printing one raises UnicodeEncodeError in the middle of a warning.
    The runner is UTF-8 already; this makes a local run agree with it rather than crash on the report."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


# --- the before picture: which old section each new one came from --------------------------------
def lineage(old: list[tuple[str, str]], new: list[tuple[str, str]]) -> dict[str, dict]:
    """`{new section: {"from", "basis", "shared", "of"}}` for each section the new copy has and the old
    one did not, where the evidence names an old section it replaced.

    `old` and `new` are `(entry key, section)` pairs in list order, from the same parser the build uses.
    A section name present in both copies is not a rename and is never reported, whatever moved into it.
    """
    before = list(dict.fromkeys(sec for _, sec in old))
    after = list(dict.fromkeys(sec for _, sec in new))
    was = {k: sec for k, sec in old}
    members: dict[str, list[str]] = defaultdict(list)
    for k, sec in new:
        members[sec].append(k)

    out: dict[str, dict] = {}
    for sec in after:
        if sec in before:
            continue
        keys = members[sec]
        came = Counter(was[k] for k in keys if k in was)
        if came:
            src, n = came.most_common(1)[0]
            if n / len(keys) >= MEMBERSHIP:
                out[sec] = {"from": src, "basis": "membership", "shared": n, "of": len(keys)}
                continue
        # Same shape, one slot renamed: the section that used to sit here and is gone now.
        if len(before) == len(after):
            i = after.index(sec)
            if before[i] not in after:
                out[sec] = {"from": before[i], "basis": "position", "slot": i + 1, "of": len(after)}
    return out


def load_moves(path: Path | None = None) -> dict[str, dict[str, dict]]:
    path = path or MOVES
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("sources", {})
    except (OSError, json.JSONDecodeError, AttributeError):
        return {}


def record_moves(source: str, sha: str | None, found: dict[str, dict], path: Path | None = None) -> None:
    """Merge one pull's lineage into the ledger. Accumulates, because the evidence is only ever seen once.

    The pull that observes a rename is the only one that has the old copy to compare against; the next
    day the list is "unchanged" and there is nothing to diff. So an observation is kept until a newer
    one about the same section replaces it. The file lives in `cache/`, which the rolling Actions cache
    carries from one green run to the next -- and a provisional run is a green one, which is what lets
    the evidence outlive the day it was seen.
    """
    if not found:
        return
    path = path or MOVES
    moves = load_moves(path)
    mine = moves.setdefault(source, {})
    for sec, ev in found.items():
        mine[sec] = dict(ev, seen=now(), sha=sha)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"version": 1, "sources": moves}, indent=1, sort_keys=True,
                               ensure_ascii=False) + "\n", encoding="utf-8")


# The second "before" picture, and the one that survives anything that happens to the cache. The first
# trial of this module (run 44348469978, 2026-11-18) placed libukai's eight headings by the mode, not by
# membership, because the copy it pulled that day was not the change: an earlier run had already pulled
# the translated README into the rolling cache, before `section-moves.json` existed to record what it
# replaced. Any drift that lands on a day the ledger misses -- a cache that did not restore, a run that
# died after the pull -- would be the same. But the build commits its own record of every list it
# publishes: `mega-list/lists/*.md` is one page per list, each entry a `- **[name](url)**` line under the
# `## section` it was published in. That is yesterday's membership, in the repository, so it is read as
# membership evidence whenever the ledger has none. Membership only: the page orders its sections by
# where their rows first fall in the build, not by the list's own order, so it says nothing about slots.
MEGA_LISTS = ROOT / "mega-list" / "lists"
_CURATED = re.compile(r"Curated by \*\*\[(?P<nwo>[^\]]+)\]\(")
_ENTRY = re.compile(r"^- \*\*\[.*?\]\((?P<url>[^)\s]+)\)\*\*")


def published_pairs(nwo: str, key, folder: Path | None = None,
                    title: str | None = None) -> list[tuple[str, str]]:
    """`(entry key, section)` for one list as the atlas last published it, from its committed pages.

    Found by the repository its pages credit, and -- where more than one list credits the same one --
    by the page title too. Two synthetic sources do: the GitHub scout and the GitLab intake both name
    this repository, deliberately, because it is where their documents come from. The title alone is
    not the key because a list with a workbook sheet publishes under the sheet's name (16_build_all's
    SHEETS: "Agents (kyrolabs)", not SOURCES' "AI Agents (kyrolabs)"), and that table lives in a module
    this one does not import. So: a unique repository decides on its own; a shared one needs the title
    to match a page's `# title` exactly; and a shared one with no matching title gives no evidence,
    rather than another list's.
    """
    def part(p: Path) -> tuple[str, int]:
        # `paginate` names a list's parts `x.md`, `x-2.md`, `x-3.md`; plain sorting puts `-2` first.
        m = re.fullmatch(r"(.*)-(\d+)", p.stem)
        return (m[1], int(m[2])) if m else (p.stem, 1)

    groups: dict[str, list[str]] = defaultdict(list)
    for p in sorted((folder or MEGA_LISTS).glob("*.md"), key=part):
        text = p.read_text(encoding="utf-8")
        m = _CURATED.search(text[:4000])
        if m and m["nwo"].lower() == nwo.lower():
            # Every part of a paginated list repeats the list's `# title` as its first line.
            groups[text.split("\n", 1)[0].removeprefix("# ").strip()].append(text)
    if len(groups) == 1:
        pages = next(iter(groups.values()))
    else:
        pages = groups.get(title or "", [])
    out = []
    for text in pages:
        sec = None  # each part restates the heading of the section it opens with
        for line in text.splitlines():
            if line.startswith("## "):
                sec = html.unescape(line[3:].strip())
            elif sec and sec != "Contents":
                m = _ENTRY.match(line)
                if m:
                    out.append((key(m["url"]), sec))
    return out


def published_moves(rows: list[dict], sources: dict[str, tuple[str, str]], sections: dict, moves: dict,
                    key, folder: Path | None = None) -> dict[str, dict[str, dict]]:
    """`moves`, with membership evidence from the published pages added for sections it has none for.

    `sources` is `{source key: (nwo, title)}`. Only lists with a section the taxonomy does not name are
    read -- on a day with no drift this reads no file at all -- and the ledger's own observations always
    win: they were made against the actual previous copy, the pages against the last *build*.
    """
    want = {r["source"] for r in rows if (r["source"], r["category"]) not in sections}
    out = {k: dict(v) for k, v in moves.items()}
    for src in sorted(want):
        nwo, title = sources.get(src) or (None, None)
        old = published_pairs(nwo, key, folder, title) if nwo else []
        if not old:
            continue
        new = [(key(r["url"]), r["category"]) for r in rows if r["source"] == src and r.get("url")]
        for sec, ev in lineage(old, new).items():
            if ev["basis"] == "membership" and sec not in out.get(src, {}):
                out.setdefault(src, {})[sec] = dict(ev, via="published")
    return out


# --- placing --------------------------------------------------------------------------------------
def _chain(source: str, section: str, sections: dict, moves: dict) -> tuple[str, dict, list[str]] | None:
    """Follow recorded renames back to a mapped section: (category, first hop's evidence, the path).

    A chain because drift compounds while nobody is looking: a heading translated on Monday and reworded
    on Thursday is two hops, and only the far end of the chain is in SECTIONS.
    """
    path, cur, first = [section], section, None
    mine = moves.get(source, {})
    while cur in mine and len(path) < 10:
        ev = mine[cur]
        first = first or ev
        cur = ev["from"]
        if cur in path:
            return None
        path.append(cur)
        if (source, cur) in sections:
            return sections[(source, cur)], first, path
    return None


def _modal(source: str, counts: Counter, sections: dict, categories: list[str],
           everything: Counter) -> tuple[str, dict]:
    """The category most of this list's rows land in today, by the mapped sections only.

    Falls back to the categories this list's keys name in SECTIONS (a list whose every heading changed
    at once has no mapped row today, but it still has a history), and then to the atlas-wide mode. The
    last is not reachable for a list that has ever been mapped, which is all of them: a new list joins
    SOURCES in a PR, with its keys, and the strict tests refuse it otherwise.
    """
    rank = {c: i for i, c in enumerate(categories)}
    votes: Counter = Counter()
    for sec, n in counts.items():
        if (source, sec) in sections:
            votes[sections[(source, sec)]] += n
    how = "rows"
    if not votes:
        votes = Counter(cat for (s, _), cat in sections.items() if s == source)
        how = "keys"
    if not votes:
        votes, how = everything, "atlas"
    best = min(votes, key=lambda c: (-votes[c], rank.get(c, 99)))
    return best, {"basis_of": how, "votes": votes[best], "of": sum(votes.values())}


def place(rows: list[dict], sections: dict[tuple[str, str], str],
          buckets: dict[str, list[tuple[str, list[str]]]], moves: dict[str, dict],
          categories: list[str]) -> list[dict]:
    """Every decision upstream drift forces on this run, as records. Pure: reads nothing from disk.

    `rows` are `10_parse_sources` rows (`source`, `category`) in parse order; `sections` and `buckets`
    are `taxonomy.SECTIONS` and `buckets.BUCKETS`; `moves` is `load_moves()`.

    One record per `(source, section)` that needs one, carrying `category` when the taxonomy does not
    name the section and `bucket` when the palette needs it folded; whichever the record does not need
    is None. A source with no drift contributes nothing, and a strict run with no records is a pass.
    """
    order: dict[str, list[str]] = defaultdict(list)
    counts: dict[str, Counter] = defaultdict(Counter)
    for r in rows:
        src, sec = r["source"], r["category"]
        if sec not in counts[src]:
            order[src].append(sec)
        counts[src][sec] += 1
    everything: Counter = Counter()
    for src, c in counts.items():
        for sec, n in c.items():
            if (src, sec) in sections:
                everything[sections[(src, sec)]] += n

    out: list[dict] = []
    for src, secs in order.items():
        fold = {s: b for b, members in buckets.get(src, []) for s in members}
        mapped_here = [s for (k, s) in sections if k == src]
        orphans = [s for s in mapped_here if s not in counts[src]]
        placed: dict[str, dict] = {}

        for sec in secs:
            if (src, sec) in sections:
                continue
            rec = {"source": src, "section": sec, "rows": counts[src][sec], "category": None,
                   "basis": None, "evidence": {}, "bucket": None, "bucket_basis": None}
            hit = _chain(src, sec, sections, moves)
            if hit:
                rec["category"], ev, path = hit
                rec["basis"] = ev["basis"]
                rec["evidence"] = dict({k: v for k, v in ev.items() if k not in ("seen", "sha")},
                                       was=path[-1], path=path)
            else:
                near = None
                for pool in (orphans, [s for s in secs if (src, s) in sections]):
                    scored = sorted(((difflib.SequenceMatcher(None, sec.lower(), s.lower()).ratio(), s)
                                     for s in pool), reverse=True)
                    if scored and scored[0][0] > SIMILAR:
                        near = scored[0]
                        break
                if near:
                    rec["category"] = sections[(src, near[1])]
                    rec["basis"] = "similar"
                    rec["evidence"] = {"was": near[1], "ratio": round(near[0], 2)}
                else:
                    rec["category"], rec["evidence"] = _modal(src, counts[src], sections, categories,
                                                              everything)
                    rec["basis"] = "modal"
            placed[sec] = rec

        # The one left over. When every other newcomer has been traced to the section it replaced, and
        # exactly one newcomer and exactly one vanished mapped section remain, they are each other: the
        # list lost one shelf and gained one. That is how libukai's "Video Tutorials" is found -- two of
        # its three entries are new, so membership cannot see it, and the trial's restored cache had no
        # slot order to read -- and it is still only a pairing, labelled as such, for a person to confirm.
        claimed = {r["evidence"].get("was") for r in placed.values()}
        guessed = [r for r in placed.values() if r["basis"] == "modal"]
        spare = [s for s in orphans if s not in claimed]
        if len(guessed) == 1 and len(spare) == 1:
            rec = guessed[0]
            rec["category"], rec["basis"] = sections[(src, spare[0])], "leftover"
            rec["evidence"] = {"was": spare[0], "traced": len(placed) - 1}
        for rec in placed.values():
            was = rec["evidence"].get("was")
            if was in fold:
                rec["bucket"], rec["bucket_basis"] = fold[was], "inherited"

        # The palette, counted the way `16_build_all.group_styles` hands out slots: every bucket the map
        # names, present today or not, then each other bucket in the order its rows first appear.
        named = [b for b, _ in buckets.get(src, [])]
        own = [s for s in secs if fold.get(s) is None and (placed.get(s) or {}).get("bucket") is None]
        extra = list(dict.fromkeys(b for b in own if b not in named))
        if len(named) + len(extra) > HUES:
            # Sections the taxonomy already maps keep their hues ahead of the newcomers: a fold is a
            # demotion, and the section that arrived today is the one to demote.
            extra.sort(key=lambda s: ((src, s) not in sections, secs.index(s)))
            keep = extra[:max(HUES - len(named), 0)]
            # The last bucket. In a curated map that is the catch-all every map in buckets.py ends on
            # ("Workflow, UI & Media", "Tooling & Courses", "Guides & Collections"); in a list with no
            # map it is the eighth section's own name. Either way the row still prints its own section,
            # so the identity is carried by the text, as the palette method requires.
            last = (named + keep)[HUES - 1]
            # A list with no map needs one written, not a section added to one, so the fold carries the
            # whole map it implies: each kept section its own bucket, in the order they appear, and the
            # folded ones in the last. `apply_drift_proposal.py` writes it out verbatim.
            whole = None if named else (
                [[s, [s]] for s in keep[:-1]] + [[last, [last] + extra[len(keep):]]])
            for s in extra[len(keep):]:
                rec = placed.get(s) or {"source": src, "section": s, "rows": counts[src][s],
                                        "category": None, "basis": "mapped", "evidence": {},
                                        "bucket": None, "bucket_basis": None}
                rec["bucket"], rec["bucket_basis"] = last, "fold"
                if whole:
                    rec["new_map"] = whole
                placed[s] = rec
        out += list(placed.values())
    for rec in out:
        rec["taxonomy_line"] = taxonomy_line(rec)
        rec["buckets_note"] = buckets_note(rec)
    return out


def taxonomy_line(rec: dict) -> str | None:
    if rec["category"] is None:
        return None
    return f"    ({rec['source']!r}, {rec['section']!r}): {rec['category']!r},".replace("'", '"')


def buckets_note(rec: dict) -> str | None:
    if rec["bucket"] is None:
        return None
    if rec.get("new_map"):
        return (f"BUCKETS has no map for {rec['source']!r}: add one with {len(rec['new_map'])} buckets, "
                f"folding {rec['section']!r} into {rec['bucket']!r}").replace("'", '"')
    return (f"BUCKETS[{rec['source']!r}]: add {rec['section']!r} to the {rec['bucket']!r} bucket"
            .replace("'", '"'))


def describe(rec: dict) -> str:
    """One sentence of evidence, for the annotation and the summary table."""
    ev = rec["evidence"]
    b = rec["basis"]
    if b == "membership":
        hops = " -> ".join(reversed(ev.get("path", [])))
        return (f"{ev['shared']} of its {ev['of']} entries were listed under {ev['was']!r} "
                + ("on the atlas's last published page for this list" if ev.get("via") == "published"
                   else "in the previous copy")
                + (f" ({hops})" if len(ev.get("path", [])) > 2 else ""))
    if b == "position":
        return (f"it took slot {ev['slot']} of {ev['of']}, which was {ev['was']!r}; the list kept "
                f"its shape")
    if b == "leftover":
        return (f"the other {ev['traced']} new section(s) were traced to what they replaced, and "
                f"{ev['was']!r} is the one mapped section the list no longer has")
    if b == "similar":
        return f"its name is {ev['ratio']:.0%} similar to {ev['was']!r}"
    if b == "modal":
        return (f"no rename evidence; {rec['category']!r} is where most of this list already files "
                f"({ev['votes']} of {ev['of']} {ev['basis_of']})")
    return "already mapped by the taxonomy"


# --- honouring the placements in later stages -----------------------------------------------------
_loaded: list[dict] | None = None


def placements() -> list[dict]:
    """This run's placements, or none at all outside provisional mode. Read once per process."""
    global _loaded
    if not enabled():
        return []
    if _loaded is None:
        try:
            _loaded = json.loads(PLACEMENTS.read_text(encoding="utf-8")).get("placements", [])
        except (OSError, json.JSONDecodeError, AttributeError):
            _loaded = []
    return _loaded


def category(source: str, section: str) -> str | None:
    for p in placements():
        if p["source"] == source and p["section"] == section and p["category"]:
            return p["category"]
    return None


def bucket_overrides(source: str) -> dict[str, str]:
    return {p["section"]: p["bucket"] for p in placements() if p["source"] == source and p["bucket"]}


def reset() -> None:
    """Forget what was read, so a test can change the env or the file within one process."""
    global _loaded
    _loaded = None


# --- writing it all down --------------------------------------------------------------------------
def degraded_from_pull(path: Path | None = None) -> list[dict]:
    """The lists today's pull could not take, from `pull_sources.py`'s report: kept at yesterday's copy."""
    try:
        rep = json.loads((path or PULL_REPORT).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    out = []
    for ln in rep.get("sources", []):
        st = ln.get("status") or ""
        kind = ("unreachable" if st == "unreachable" else
                "parse-collapse" if st.startswith("failed") and "parsed" in st else
                "shrink" if st.startswith("failed") and "came back" in st else
                "pull-failed" if st.startswith("failed") else
                "undiffable" if st.startswith("pulled, undiffable") else None)
        if kind:
            out.append({"source": ln.get("key"), "nwo": ln.get("nwo"), "kind": kind, "detail": st})
        if ln.get("renamed_to"):
            out.append({"source": ln.get("key"), "nwo": ln.get("nwo"), "kind": "renamed",
                        "detail": f"GitHub now serves {ln['nwo']} as {ln['renamed_to']}; update its "
                                  f"`nwo` in 10_parse_sources.SOURCES"})
    return out


def fingerprint(recs: list[dict]) -> str:
    """The same drift on consecutive days has the same id, so the CI stream can open one PR, not seven."""
    keys = sorted((r["source"], r["section"], r["category"] or "", r["bucket"] or "") for r in recs)
    return hashlib.sha256(json.dumps(keys, ensure_ascii=False).encode("utf-8")).hexdigest()


def markdown(recs: list[dict], degraded: list[dict]) -> str:
    lines = []
    if recs:
        lines += [f"### Upstream drift: {len(recs)} provisional placement(s)", "",
                  "This build published, with these sections filed **for this run only**. Nothing is "
                  "re-filed for good until the lines below are added, by hand or by running "
                  "`python scripts/apply_drift_proposal.py` over this run's `cache/drift-proposal.json`.",
                  "", "| list | section | rows | filed under | colour | why |", "|---|---|---|---|---|---|"]
        for r in recs:
            cat = r["category"] or "(already mapped)"
            col = (f"{r['bucket']} ({r['bucket_basis']})" if r["bucket"] else "own")
            cell = describe(r).replace("|", "\\|")
            lines.append(f"| `{r['source']}` | {r['section']} | {r['rows']} | {cat} | {col} | {cell} |")
        tax = [r["taxonomy_line"] for r in recs if r["taxonomy_line"]]
        if tax:
            lines += ["", "`scripts/taxonomy.py`, in `SECTIONS`, each in its list's block:", "", "```python",
                      *tax, "```"]
        bk = [r["buckets_note"] for r in recs if r["buckets_note"]]
        if bk:
            lines += ["", "`scripts/buckets.py`:", "", *[f"- {b}" for b in bk]]
    if degraded:
        lines += ["", f"### Upstream drift: {len(degraded)} list(s) held at their previous copy", "",
                  "| list | what happened |", "|---|---|"]
        lines += [f"| `{d['source']}` ({d['nwo']}) | {d['kind']}: {d['detail']} |" for d in degraded]
    return "\n".join(lines)


def publish(recs: list[dict], degraded: list[dict], provisional: bool) -> None:
    """Write the run's placements and the proposal, and say so as loudly as the platform allows.

    `cache/provisional.json` is what later stages honour; `cache/drift-proposal.json` is what a person
    or the CI stream acts on. Two files because they have different lives: the first must not exist
    after a strict run, the second is a report and is always rewritten, empty on a clean day, so a
    consumer never acts on yesterday's proposal.
    """
    PROPOSAL.parent.mkdir(parents=True, exist_ok=True)
    fp = fingerprint(recs) if recs else None
    doc = {"version": 1, "generated_at": now(), "run": os.environ.get("GITHUB_RUN_ID"),
           "provisional": provisional, "fingerprint": fp, "placements": recs, "degraded": degraded}
    PROPOSAL.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    md = markdown(recs, degraded)
    PROPOSAL_MD.write_text(md + "\n", encoding="utf-8")
    if provisional and recs:
        PLACEMENTS.write_text(json.dumps({"version": 1, "generated_at": doc["generated_at"],
                                          "fingerprint": fp, "placements": recs},
                                         indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    else:
        PLACEMENTS.unlink(missing_ok=True)
    reset()

    if not provisional:
        return
    for r in recs:
        what = (f"filed under {r['category']!r} for this run" if r["category"] else "")
        if r["bucket"]:
            what += (" and " if what else "") + f"coloured with the {r['bucket']!r} bucket"
        paste = "; ".join(x for x in (r["taxonomy_line"] and r["taxonomy_line"].strip(),
                                      r["buckets_note"]) if x)
        warn(f"Provisional: {r['source']} / {r['section']}",
             f"{r['rows']} row(s) {what}, because {describe(r)}. Make it permanent: {paste}")
    for d in degraded:
        warn(f"Held at previous copy: {d['source']}", f"{d['nwo']}: {d['kind']}: {d['detail']}")
    if md:
        summary(md)
