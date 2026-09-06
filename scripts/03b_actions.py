"""Detect GitHub Actions definitively: an action.yml/action.yaml at the repo root."""
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
BATCH = 25

# See 13_signals_all.py: 02_fetch.py owns the single answer to what a non-zero exit from
# `gh api graphql` means, and a batched query that does not go through it will sooner or later throw
# away twenty-four good repos because the twenty-fifth was deleted.
spec = importlib.util.spec_from_file_location("fetch02", Path(__file__).parent / "02_fetch.py")
f2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f2)

FIELDS = """
    yml: object(expression: "HEAD:action.yml") { __typename }
    yaml: object(expression: "HEAD:action.yaml") { __typename }
"""


def main() -> None:
    entries = json.loads((CACHE / "entries.json").read_text(encoding="utf-8"))
    meta = json.loads((CACHE / "meta.json").read_text(encoding="utf-8"))
    entries = [e for e in entries if "error" not in meta.get(e["nwo"], {})]

    out = {}
    failed = 0
    for start in range(0, len(entries), BATCH):
        batch = entries[start : start + BATCH]
        try:
            data = f2.graphql_batch(batch, FIELDS)
        except RuntimeError as exc:
            # `False` for a repo we never got an answer about reads exactly like a repo that has no
            # action.yml, so a failed batch records nothing and the run is written off below.
            failed += 1
            print(f"  batch {start} failed: {str(exc)[:120]}")
            continue
        for i, e in enumerate(batch):
            n = data.get(f"r{i}")
            if n is None:
                continue  # deleted since 02_fetch ran; next run's meta.json filters it out
            out[e["nwo"]] = bool(n.get("yml") or n.get("yaml"))
        print(f"  {min(start + BATCH, len(entries))}/{len(entries)}")

    # No write at all when something failed, which is where this stage differs from 03_releases.py and
    # 13_signals_all.py. Those two merge into a file they also read, so a batch they skip stays missing
    # and comes back in `todo`; this one rebuilds actions.json from nothing every run and writes it
    # whole, so a short version written here would delete answers an earlier run got right -- and
    # 13_signals_all.py, which extends this same file, would then have to refetch them. Leaving the
    # file alone loses nothing, and since this stage never resumes -- it always redoes all of
    # entries.json -- "retry the failed batch" and "run it again" were already the same thing.
    if failed:
        print(f"\n{failed} batch(es) of {BATCH} failed; actions.json left as it was. "
              f"04_classify would have read the gap as {failed * BATCH} projects that ship no action.yml.")
        sys.exit(1)

    (CACHE / "actions.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    hits = sorted(k for k, v in out.items() if v)
    print(f"\n{len(hits)} repos ship an action.yml:")
    for h in hits:
        print(f"  {h}")


if __name__ == "__main__":
    main()
