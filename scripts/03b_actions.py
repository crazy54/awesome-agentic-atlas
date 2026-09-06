"""Detect GitHub Actions definitively: an action.yml/action.yaml at the repo root.

Incremental, on the rule in scripts/signals.py: an `action.yml` can only appear or
disappear through a push, so a repo whose `pushedAt` has not moved since its cached
entry was written cannot have changed its answer. That makes push-gating this stage
exactly right rather than merely cheap -- unlike release assets, there is no way to
gain one without a push, so this file has no blind spot.

It also stops the write being destructive. This stage used to rebuild `actions.json`
from scratch over the primary list's ~194 repos, which deleted the ~1,100 entries
13_signals_all.py had written for the other ten lists -- so every daily run threw
away most of the file and 13_signals_all re-crawled it, which was the bulk of the
pipeline's daily GraphQL spend.
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import signals as sig  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
BATCH = 25


def gh(args: list[str]) -> str:
    p = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(p.stderr[:300])
    return p.stdout


def main() -> None:
    entries = json.loads((CACHE / "entries.json").read_text(encoding="utf-8"))
    meta = json.loads((CACHE / "meta.json").read_text(encoding="utf-8"))
    entries = [e for e in entries if "error" not in meta.get(e["nwo"], {})]

    out_path = CACHE / "actions.json"
    force = "--force" in sys.argv
    out = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}

    now = sig.utcnow()
    pushed = {e["nwo"]: sig.meta_push(meta, e["nwo"]) for e in entries}
    # The CI-race term in signals.py deliberately does not apply to this file -- see `_raced_ci`
    # and the docstring above -- so the only terms that can queue a repo here are a moved push, a
    # legacy entry, and the age ceiling.
    why = {e["nwo"]: sig.reason(out, e["nwo"], pushed[e["nwo"]], now) for e in entries}
    todo = [e for e in entries if force or why[e["nwo"]] != sig.FRESH]
    print(f"{len(todo)} of {len(entries)} repos to check for an action.yml"
          f"{sig.breakdown([why[e['nwo']] for e in todo])}")

    for start in range(0, len(todo), BATCH):
        batch = todo[start : start + BATCH]
        parts = [
            f'  r{i}: repository(owner: "{e["owner"]}", name: "{e["repo"]}") {{'
            f' yml: object(expression: "HEAD:action.yml") {{ __typename }}'
            f' yaml: object(expression: "HEAD:action.yaml") {{ __typename }} }}'
            for i, e in enumerate(batch)
        ]
        try:
            data = json.loads(gh(["api", "graphql", "-f", "query=query {\n" + "\n".join(parts) + "\n}"])).get("data") or {}
        except RuntimeError as exc:
            print(f"  batch {start} failed: {exc}")
            data = {}
        for i, e in enumerate(batch):
            n = (data or {}).get(f"r{i}")
            # See 03_releases.py: a null node taught us nothing, so keep whatever is cached and
            # stay queued rather than stamping a guess as though it were an observation.
            if not n:
                continue
            out[e["nwo"]] = sig.action_entry(bool(n.get("yml") or n.get("yaml")),
                                             pushed[e["nwo"]], now)
        print(f"  {min(start + BATCH, len(todo))}/{len(todo)}")
        out_path.write_text(json.dumps(out, indent=1), encoding="utf-8")

    out_path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    # Counted over the whole file, which now spans every list rather than just this stage's, and
    # named only for the repos this run actually looked at -- listing all of them would be a
    # hundred lines of log saying nothing changed.
    hits = sorted(e["nwo"] for e in todo if sig.is_action(out.get(e["nwo"])))
    print(f"\n{sum(1 for v in out.values() if sig.is_action(v))} of {len(out)} cached repos "
          f"ship an action.yml; {len(hits)} of them among the {len(todo)} checked here:")
    for h in hits:
        print(f"  {h}")


if __name__ == "__main__":
    main()
