"""Pull each source list, but only the ones whose head commit moved, and say what changed inside them.

Until this stage existed the pipeline had no way to *get* its own inputs. `01_parse.py` read
`cache/README.md` and `10_parse_sources.py` read `cache/sources/*.md`, and nothing anywhere wrote
either one: on CI they survived only because the rolling Actions cache happened to carry them
forward, and a cold cache meant a `FileNotFoundError` on whichever list came first. So this script is
both the missing fetch stage and the cache that makes re-running it cheap.

  pull_sources.py              pull the lists whose head commit differs from the cached one
  pull_sources.py --force      pull every list, cached commit or not
  pull_sources.py --status     report what is cached; no network
  pull_sources.py --only KEY   one list, by its key in 10_parse_sources.SOURCES

Four decisions worth knowing about:

* **The commit id lives with the bytes, in `cache/sources/index.json`.** `state/first-seen.json`
  already records a SHA per source and is committed, but it means "this commit has been *built*".
  Reusing it here would be a correctness bug, not a shortcut: `cache/` is not committed, so a clone
  with the ledger and no cache would compare equal, skip every pull, and then parse nothing.
  Co-locating the id with the content it describes makes "unchanged" mean "we still have it".

* **Content is fetched pinned at the SHA that was probed**, not at `HEAD`. A list that gets a push
  between the probe and the fetch would otherwise leave the newer bytes filed under the older id, and
  the next run would see a matching id and never correct it.

* **From `raw.githubusercontent.com`, not `gh api repos/{nwo}/readme`.** Above roughly a megabyte the
  API returns a payload whose content field is *empty* rather than an error, so the API path silently
  scores a 1.4 MB list as holding nothing. raw also needs no token, so pulling does not compete with
  the metadata stages for the hourly rate limit.

* **A failed pull records nothing.** Same reasoning as `watch_sources.py --update` running only after
  a successful build: if the id were recorded first, a truncated or unreachable pull would count as
  done for ever and that list's new entries would be lost rather than retried tomorrow.

The diff is over parsed *entries*, not over lines, and it runs the real parsers -- `01_parse.py` for
the orchestrators README, `10_parse_sources.py` for the other ten -- across the cached copy and the
new one. That makes "changed" mean the atlas's view of the list changed, so a reworded heading or a
new badge is correctly silent, and it cannot drift from what the build will actually read.

What the diff finds goes to `cache/collect-queue.json` for the screenshot stage, with the reason.
The two reasons are not the same job. An entry the atlas has never seen has no key in
`cache/shots_all.json`, so `15_shots_all.py` collects it whether or not it is on the queue; it is
listed for the record. `changed` is the case nothing handled before -- an entry that is still listed
under the same URL but whose listing moved -- and that is the one the screenshot stage invalidates.
The queue accumulates across runs because the daily job never captures screenshots; the weekly job
does, and drains it.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
CACHE = ROOT / "cache"

sys.path.insert(0, str(HERE))
import watch_sources  # noqa: E402  -- reused for head(), the one definition of "latest commit id"

# watch_sources has already loaded 10_parse_sources for its own source list. Borrowing its module
# object keeps one SOURCES in the process rather than a second copy of the same file.
b10 = watch_sources.b10

_spec = importlib.util.spec_from_file_location("b01", HERE / "01_parse.py")
b01 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(b01)

SRC = b10.SRC
INDEX = SRC / "index.json"
REPORT = CACHE / "pull-report.json"
QUEUE = CACHE / "collect-queue.json"

TIMEOUT = 30
# Generous on purpose: the largest list the JFH-202 survey measured is 1.4 MB, and the point of this
# stage is that big lists arrive whole. A truncated one looks exactly like the empty-content API bug.
MAX_BYTES = 16_000_000
# A list that suddenly returns a fraction of what it had is a truncated transfer, not an edit.
# Refusing it costs a day of freshness; accepting it silently deletes rows from the atlas.
SHRINK_FLOOR = 0.25
UA = {"User-Agent": "awesome-agentic-atlas pull_sources "
                    "(+https://github.com/crazy54/awesome-agentic-atlas)"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def rel(path: Path) -> str:
    """Cache-relative, so the ledger reads the same on a runner and on a laptop."""
    return path.relative_to(CACHE).as_posix()


# --- the cache ledger ------------------------------------------------------------------------
def load_index() -> dict:
    if not INDEX.exists():
        return {"version": 1, "sources": {}}
    try:
        state = json.loads(INDEX.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        # A half-written ledger is indistinguishable from no ledger. Treating it as none costs one
        # round of pulls; guessing at its contents could skip a list for ever.
        print("  ! index.json unreadable; treating every source as uncached", file=sys.stderr)
        return {"version": 1, "sources": {}}
    state.setdefault("version", 1)
    state.setdefault("sources", {})
    return state


def save_index(state: dict) -> None:
    SRC.mkdir(parents=True, exist_ok=True)
    INDEX.write_text(json.dumps(state, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def content_intact(rec: dict) -> bool:
    """Is every file this record claims still on disk at the size it claims?

    The commit id alone is not enough to skip a pull. `cache/` is pruned, restored partially and
    shared with the workbook job, so "we recorded this commit" and "we still have this commit's
    content" are different facts and only the second one licenses a skip.
    """
    files = rec.get("files") or {}
    if not files:
        return False
    return all((CACHE / name).exists() and (CACHE / name).stat().st_size == want.get("bytes")
               for name, want in files.items())


# --- fetching --------------------------------------------------------------------------------
def readme_path(nwo: str) -> str:
    """The list's README as it is actually named. Only `path` is read, never `content`.

    Casing and extension vary between lists and guessing wrong is a 404 for a list that is perfectly
    fine, so this asks. `content` in the same response is the field that lies about big files;
    `path` is reliable at any size.
    """
    out = subprocess.run(["gh", "api", f"repos/{nwo}/readme", "--jq", ".path"],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    path = out.stdout.strip()
    return path if out.returncode == 0 and path and "\n" not in path else "README.md"


def raw_bytes(nwo: str, sha: str, path: str) -> tuple[bytes | None, str]:
    """(content, reason it is missing). Pinned at `sha`, so the bytes match the id we will record."""
    url = f"https://raw.githubusercontent.com/{nwo}/{sha}/{urllib.parse.quote(path)}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=TIMEOUT) as r:
            if r.status != 200:
                return None, f"HTTP {r.status}"
            data = r.read(MAX_BYTES + 1)
    except Exception as exc:
        return None, f"{type(exc).__name__}"
    if not data:
        return None, "empty"
    if len(data) > MAX_BYTES:
        return None, f"over {MAX_BYTES:,}B cap"
    return data, ""


def files_to_pull(src: dict) -> list[tuple[str, Path]]:
    """(repo path, destination) for everything this source's content lives in.

    A list is usually one README. Not always: `github/awesome-copilot` keeps its ~415 items in four
    files under `docs/` behind a five-row hub table. `paths` on a source dict names those extras,
    which land beside the primary file so one source stays one group of files on disk. The README is
    always pulled regardless, because it is what the parsers read.
    """
    dest = b10.source_path(src)
    out = [(readme_path(src["nwo"]), dest)]
    for p in src.get("paths") or []:
        flat = p.strip("/").replace("/", "__")
        out.append((p, dest.with_name(f"{dest.stem}__{flat}{dest.suffix}")))
    return out


# --- the diff --------------------------------------------------------------------------------
def entries_of(src: dict, text: str) -> dict[str, dict]:
    """`{url_key: {url, shape}}` for one source's content, through the parser the build itself uses.

    `shape` is the part of an entry that would change what the atlas shows for it. Comparing whole
    rows would flag `src_order` on every row below an insertion and call the entire tail changed.
    """
    if src.get("file"):
        rows = b10.parse(src, text)
        keys = ("name", "description", "category", "sub_category", "kind", "nwo", "subpath")
    else:
        # The orchestrators README is the collection's own origin and has its own parser.
        rows = b01.dedupe(b01.parse_text(text), report=False)
        keys = ("name", "description", "category", "status_note")
    return {b10.url_key(r["url"]): {"url": r["url"], "shape": [r[k] for k in keys]} for r in rows}


def diff_entries(old: dict[str, dict], new: dict[str, dict]) -> dict[str, list[str]]:
    return {
        "added": [k for k in new if k not in old],
        "removed": [k for k in old if k not in new],
        "changed": [k for k in new if k in old and new[k]["shape"] != old[k]["shape"]],
    }


# --- the collect queue -----------------------------------------------------------------------
def load_queue() -> dict:
    if not QUEUE.exists():
        return {"version": 1, "pending": {}}
    try:
        q = json.loads(QUEUE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"version": 1, "pending": {}}
    q.setdefault("version", 1)
    q.setdefault("pending", {})
    return q


def save_queue(q: dict) -> None:
    q["updated_at"] = now()
    QUEUE.parent.mkdir(parents=True, exist_ok=True)
    QUEUE.write_text(json.dumps(q, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def queue_entries(items: list[tuple[str, str, str]]) -> int:
    """Add `(url, source key, reason)` to the queue. Returns how many were not already on it.

    A URL already queued keeps its original reason and timestamp: `changed` outranks a later
    `added` from a second list, and the timestamp is when the atlas first needed to look again.
    """
    q = load_queue()
    pending = q["pending"]
    fresh = 0
    for url, source, reason in items:
        key = b10.url_key(url)
        if key in pending:
            continue
        pending[key] = {"url": url, "source": source, "reason": reason, "queued_at": now()}
        fresh += 1
    save_queue(q)
    return fresh


# --- one source ------------------------------------------------------------------------------
def pull_one(src: dict, state: dict, force: bool) -> dict:
    """Probe, maybe pull, diff, and return this source's line of the report.

    `state` is mutated only on a complete success, which is what makes a partial failure retry on the
    next run rather than be recorded as done.
    """
    nwo, key = src["nwo"], src["key"]
    rec = state["sources"].get(nwo) or {}
    have = rec.get("sha")
    line = {"key": key, "nwo": nwo, "was": have, "sha": None, "status": "", "files": [],
            "entries": rec.get("entries", 0), "added": 0, "removed": 0, "changed": 0, "queued": 0}

    sha = watch_sources.head(nwo)
    if sha is None:
        # watch_sources' reasoning, unchanged: a list that 404s today is far likelier to be a
        # transient API problem or a rename than a reason to discard the copy we have.
        line["status"] = "unreachable"
        return line
    line["sha"] = sha

    intact = content_intact(rec)
    if sha == have and intact and not force:
        line["status"] = "unchanged"
        return line

    # Read the cached copy before overwriting it: it is the only "before" picture there is.
    dest = b10.source_path(src)
    old_text = dest.read_text(encoding="utf-8") if dest.exists() else ""
    # Right id, missing bytes. Pull to restore what the cache lost; expect the diff to be empty.
    preset = "refill" if sha == have and not intact else ""

    pulled: list[tuple[Path, bytes]] = []
    for path, target in files_to_pull(src):
        data, why = raw_bytes(nwo, sha, path)
        if data is None:
            line["status"] = f"failed: {path} ({why})"
            return line
        was = (rec.get("files") or {}).get(rel(target), {}).get("bytes") or 0
        # `--force` overrides the floor deliberately. The floor compares against a size the ledger
        # claims, so a wrong claim would otherwise wedge the source for ever: every run, including a
        # forced one, would refuse the pull and leave the same wrong number in place to refuse it
        # again. A list really can be cut down by its author, and this is how an operator says so.
        if was and not force and len(data) < was * SHRINK_FLOOR:
            line["status"] = (f"failed: {path} came back {len(data):,}B, was {was:,}B "
                              f"(--force to accept)")
            return line
        pulled.append((target, data))

    # Everything arrived, so write it all. Content first, ledger last: content on disk without a
    # ledger entry is a wasted pull next run, a ledger entry without content is a silent skip.
    for target, data in pulled:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    line["files"] = [rel(t) for t, _ in pulled]

    new_text = dest.read_text(encoding="utf-8")
    try:
        old = entries_of(src, old_text) if old_text else {}
        new = entries_of(src, new_text)
    except Exception as exc:
        # A list can be rearranged into a shape its strategy no longer fits. That is a parser
        # problem to fix, not a reason to discard a good pull, and 10_parse_sources will say so
        # loudly on the same content in the next stage.
        line["status"] = f"pulled, undiffable ({type(exc).__name__})"
        state["sources"][nwo] = record(key, sha, line["entries"], pulled)
        return line

    d = diff_entries(old, new)
    line["status"] = preset or ("first pull" if not old_text else "changed")
    line.update(added=len(d["added"]), removed=len(d["removed"]),
                changed=len(d["changed"]), entries=len(new))
    # A first pull is a baseline, not a change: every entry in it is "added" and queueing all of them
    # would fill the queue with the whole atlas on a fresh clone, to say something the empty
    # shots_all.json says already. Queue only against a copy there was something to compare with.
    line["queued"] = 0 if not old_text else queue_entries(
        [(new[k]["url"], key, "changed") for k in d["changed"]]
        + [(new[k]["url"], key, "added") for k in d["added"]])
    state["sources"][nwo] = record(key, sha, len(new), pulled)
    return line


def record(key: str, sha: str, entries: int, pulled: list[tuple[Path, bytes]]) -> dict:
    return {"key": key, "sha": sha, "pulled_at": now(), "entries": entries,
            "files": {rel(t): {"bytes": len(d), "digest": hashlib.sha256(d).hexdigest()}
                      for t, d in pulled}}


# --- reporting -------------------------------------------------------------------------------
def show_status() -> None:
    state = load_index()
    srcs = state["sources"]
    print(f"{len(srcs)}/{len(b10.SOURCES)} sources cached in {rel(INDEX)}\n")
    print(f"{'source':14s} {'commit':10s} {'entries':>7s}  {'bytes':>10s}  pulled")
    for src in b10.SOURCES:
        rec = srcs.get(src["nwo"])
        if not rec:
            print(f"{src['key']:14s} {'-':10s} {'-':>7s}  {'-':>10s}  never")
            continue
        size = sum(f.get("bytes", 0) for f in (rec.get("files") or {}).values())
        note = "" if content_intact(rec) else "  (content missing)"
        print(f"{src['key']:14s} {rec['sha'][:9]:10s} {rec.get('entries', 0):7d}  "
              f"{size:10,d}  {rec.get('pulled_at', '?')[:10]}{note}")
    pending = load_queue()["pending"]
    reasons: dict[str, int] = {}
    for v in pending.values():
        reasons[v["reason"]] = reasons.get(v["reason"], 0) + 1
    detail = ", ".join(f"{n} {r}" for r, n in sorted(reasons.items())) or "none"
    print(f"\n{len(pending)} entries queued for collection ({detail}) in {rel(QUEUE)}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--force", action="store_true",
                    help="pull every list whatever the cached commit says, and accept a pull that "
                         "comes back far smaller than the cached copy")
    ap.add_argument("--status", action="store_true", help="report the cache; no network")
    ap.add_argument("--only", metavar="KEY", help="one source, by its key")
    ap.add_argument("--strict", action="store_true",
                    help="exit non-zero if any single list could not be pulled")
    args = ap.parse_args()

    if args.status:
        show_status()
        return

    sources = b10.SOURCES
    if args.only:
        sources = [s for s in sources if s["key"] == args.only]
        if not sources:
            sys.exit(f"no source with key {args.only!r}; "
                     f"try one of: {', '.join(s['key'] for s in b10.SOURCES)}")

    SRC.mkdir(parents=True, exist_ok=True)
    state = load_index()
    lines = []
    for src in sources:
        line = pull_one(src, state, args.force)
        lines.append(line)
        # Saved per source: a run killed by the job timeout keeps whatever it already pulled.
        save_index(state)
        flag = {"unchanged": "  = ", "unreachable": "  ? "}.get(line["status"], "PULL")
        if line["status"].startswith("failed"):
            flag = "FAIL"
        counts = ""
        if line["added"] or line["removed"] or line["changed"]:
            queued = f" ({line['queued']} queued)" if line["queued"] else ""
            counts = f"  +{line['added']} -{line['removed']} ~{line['changed']}{queued}"
        print(f"  {flag} {(line['sha'] or '-')[:9]}  {line['nwo']:52s} {line['status']}{counts}",
              flush=True)

    failed = [ln for ln in lines if ln["status"].startswith("failed")]
    unreachable = [ln for ln in lines if ln["status"] == "unreachable"]
    unchanged = [ln for ln in lines if ln["status"] == "unchanged"]
    # Anything that is not one of those three got its bytes: first pull, changed, refill, undiffable.
    quiet = {"unreachable", "unchanged"}
    pulled = [ln for ln in lines
              if ln["status"] not in quiet and not ln["status"].startswith("failed")]
    added = sum(ln["added"] for ln in lines)
    changed = sum(ln["changed"] for ln in lines)
    removed = sum(ln["removed"] for ln in lines)

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(
        {"ran_at": now(), "forced": args.force, "sources": lines,
         "totals": {"pulled": len(pulled), "unchanged": len(unchanged),
                    "unreachable": len(unreachable), "failed": len(failed),
                    "added": added, "changed": changed, "removed": removed}},
        indent=1, sort_keys=True) + "\n", encoding="utf-8")

    print(f"\n{len(pulled)} pulled · {len(unchanged)} unchanged · "
          f"{len(unreachable)} unreachable · {len(failed)} failed")
    print(f"entries: +{added} added · ~{changed} changed · -{removed} removed")
    print(f"{len(load_queue()['pending'])} queued for collection · report in {rel(REPORT)}")
    for ln in failed:
        print(f"  ! {ln['nwo']}: {ln['status']}", file=sys.stderr)

    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(f"pulled={len(pulled)}\n")
            fh.write(f"changed={str(bool(pulled)).lower()}\n")
            fh.write(f"failed={len(failed)}\n")

    # One unreadable list is not a reason to fail the build: the cached copy is still there and the
    # next run tries again. `--strict` is for running this by hand and wanting to be told.
    if failed and args.strict:
        sys.exit(1)
    if failed and len(failed) == len(lines):
        sys.exit("every source failed to pull; refusing to report success")


if __name__ == "__main__":
    main()
