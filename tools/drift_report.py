"""Read a provisional parse's drift proposal and say, in a form a workflow and the build-red issue can use, what it holds.

`scripts/drift.py` (eng-pipeline's provisional mode) writes `drift.PROPOSAL` -- `cache/drift-proposal.json` -- on
every run with `AAA_PROVISIONAL=1`: `placements`, the sections it filed for this run only, each with the
`taxonomy.py` line that would make it permanent; `degraded`, the lists that could not be read properly at all
(a pull that failed, a list that shrank or collapsed, a repository renamed or unreachable), which no taxonomy line
fixes; and `fingerprint`, a hash of the sorted placements that is the same for the same drift on every run.
The path is taken from `drift` itself rather than written here, so the two cannot disagree about it.

This prints three things:

  - `$GITHUB_OUTPUT` lines: `placements=N`, `degraded=N`, `fingerprint=...`, and `branch=bot/drift-<fp[:8]>`
    (empty when there are no placements). The canary branches on these.
  - one `drift: ...` line per placement and per degraded list, on stdout. They are what `tools/ci_alert.py`
    quotes in the build-red issue, so the issue names the list, the section and where it was filed without
    anyone opening the run.
  - nothing else, and it always exits 0: whether the job goes red is the workflow's decision, made from the
    counts. A missing proposal is "no drift" -- `drift.py` writes none, or empty lists, when there is none.

  python tools/drift_report.py              # read drift.PROPOSAL
  python tools/drift_report.py some.json    # read another file
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PREFIX = "bot/drift-"


def proposal_path() -> Path:
    sys.path.insert(0, str(ROOT / "scripts"))
    import drift  # noqa: E402  -- scripts/drift.py, for its PROPOSAL path
    return Path(drift.PROPOSAL)


def report(doc: dict) -> tuple[dict, list[str]]:
    """(outputs, log lines) for a proposal document. Pure, for tests/ci_tools_test.py."""
    places, bad = doc.get("placements") or [], doc.get("degraded") or []
    fp = doc.get("fingerprint") or ""
    out = {"placements": len(places), "degraded": len(bad), "fingerprint": fp,
           "branch": PREFIX + fp[:8] if places and fp else ""}
    lines = []
    for p in places:
        where = p.get("category") or "?"
        if p.get("bucket"):
            where += f" / {p['bucket']}"
        lines.append(f"drift: placed ({p.get('source')!r}, {p.get('section')!r}), {p.get('rows', '?')} rows, "
                     f"under {where} by {p.get('basis', '?')}")
    for d in bad:
        lines.append(f"drift: degraded {d.get('source')} ({d.get('nwo', '?')}): {d.get('kind', '?')} -- "
                     f"{str(d.get('detail', ''))[:200]}")
    return out, lines


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else proposal_path()
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        doc = {}
    out, lines = report(doc)
    for l in lines:
        print(l)
    print(f"drift: {out['placements']} placement(s), {out['degraded']} degraded list(s)"
          + (f", fingerprint {out['fingerprint'][:8]}" if out["fingerprint"] else ""))
    target = os.environ.get("GITHUB_OUTPUT")
    if target:
        with open(target, "a", encoding="utf-8") as f:
            for k, v in out.items():
                f.write(f"{k}={v}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
