"""Has any source list moved? One commit SHA each, compared against the ledger.

The point of the cron is to notice new entries, and the cheapest possible test for "is there anything
to notice" is the head commit of each source repo: one API call per list in `SOURCES` below, no clone,
no Markdown parse -- which stays cheap as lists are added, where reparsing them would not. If
none of them moved, nothing the pipeline reads has changed and a rebuild would produce a byte-identical
site -- so the daily job stops here and commits nothing.

Two modes, deliberately separate:

  watch_sources.py            report only. Writes `changed=` to $GITHUB_OUTPUT and prints the table.
  watch_sources.py --update   record the SHAs into state/first-seen.json.

They are separate because the recorded SHA means "this commit has been built", not "this commit has been
seen". Recording it before the build means a build that then fails would never be retried -- the next
run would compare against the SHA it failed on and decide there was nothing to do. So the workflow
reports first, builds, and only records on success.

A synthetic source -- the scout, `scripts/12_scout.py` -- has no upstream commit, so its slot in the
ledger holds `10_parse_sources.content_digest` of the document the scout wrote instead: `sha256:<hex>`
of the rendered set of scouted repos. "Moved" then means what it means for a list: the build would read
something it has not built. The rules carry over unchanged. The digest is read off the document on disk,
so this has to run after the scout and the scout has to run first in the job; a missing document is
reported and treated as unchanged, like an unreachable list; and `--update` records the digest of the
document that was built, read again at the end of a successful run.
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent

spec = importlib.util.spec_from_file_location("newness", HERE / "newness.py")
newness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(newness)

spec = importlib.util.spec_from_file_location("b10", HERE / "10_parse_sources.py")
b10 = importlib.util.module_from_spec(spec)
sys.modules["b10"] = b10
spec.loader.exec_module(b10)

# The parser is the single definition of which lists this project is built from, so the watcher reads
# it rather than keeping a second copy that could drift out of step with it.
SOURCES = [(s["key"], s["nwo"]) for s in b10.SOURCES]
SYNTHETIC = {s["nwo"]: s for s in b10.SOURCES if s.get("synthetic")}


def head(nwo: str) -> str | None:
    """Head commit of the default branch, or None if the repo is gone, renamed or rate-limited.

    None is not a change. A list that 404s today is far more likely to be a transient API problem or a
    rename than a reason to rebuild, and treating it as movement would rebuild the whole atlas daily.
    """
    out = subprocess.run(
        ["gh", "api", f"repos/{nwo}/commits?per_page=1", "--jq", ".[0].sha"],
        capture_output=True, text=True)
    sha = out.stdout.strip()
    if out.returncode != 0 or len(sha) != 40:
        print(f"  ?? {nwo}: {(out.stderr or 'no sha').strip().splitlines()[0][:90]}",
              file=sys.stderr)
        return None
    return sha


def digest(nwo: str) -> str | None:
    """A synthetic source's stand-in for `head()`: the digest of the document it wrote, or None."""
    d = b10.content_digest(SYNTHETIC[nwo])
    if d is None:
        print(f"  ?? {nwo}: no {SYNTHETIC[nwo]['key']} document in cache/sources/ -- scripts/12_scout.py "
              f"writes it and runs before this step", file=sys.stderr)
    return d


def short(ident: str) -> str:
    """Nine characters of either kind of id, so the table lines up: a commit SHA, or a digest's hex."""
    return ident.split(":", 1)[-1][:9]


def main() -> None:
    update = "--update" in sys.argv
    state = newness.load()
    known = state["sources"]

    moved, checked, failed = [], {}, []
    for key, nwo in SOURCES:
        sha = digest(nwo) if nwo in SYNTHETIC else head(nwo)
        if sha is None:
            failed.append(nwo)
            continue
        checked[nwo] = sha
        was = known.get(nwo)
        if was != sha:
            moved.append((nwo, was, sha))
        print(f"  {'NEW ' if was != sha else '  = '} {short(sha)}  {nwo}"
              + ("  (scouted)" if nwo in SYNTHETIC else "")
              + (f"  (was {short(was)})" if was and was != sha else "")
              + ("  (first time seen)" if not was else ""))

    changed = bool(moved)
    print(f"\n{len(checked)}/{len(SOURCES)} lists reachable · "
          f"{len(moved)} moved · changed={str(changed).lower()}")
    if failed:
        print(f"unreachable, treated as unchanged: {', '.join(failed)}")

    if update:
        known.update(checked)
        newness.save(state)
        print(f"recorded {len(checked)} SHAs in {newness.PATH.relative_to(ROOT).as_posix()}")

    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(f"changed={str(changed).lower()}\n")
            fh.write(f"moved={json.dumps([n for n, _w, _s in moved])}\n")


if __name__ == "__main__":
    main()
