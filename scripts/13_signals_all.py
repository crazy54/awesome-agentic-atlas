"""Release assets and action.yml presence for every repo, in one pass.

03_releases.py and 03b_actions.py each walk the whole repo set; at 1,153 repos
that is two full sets of round trips for data that fits in one query. Same
output files, so 04_classify.py reads them unchanged.

Which repos get queried is scripts/signals.py's rule, shared with those two
stages: anything unseen, anything written before the push stamp existed, and
anything pushed since its entry was written.
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import signals as sig  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
BATCH = 12

FIELDS = """
    releases(last: 4) { nodes { tagName releaseAssets(first: 40) { nodes { name } } } }
    yml: object(expression: "HEAD:action.yml") { __typename }
    yaml: object(expression: "HEAD:action.yaml") { __typename }
"""


def gh(args: list[str]) -> str:
    p = subprocess.run(["gh", *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(f"gh failed: {p.stderr[:300]}")
    return p.stdout


def main() -> None:
    rows = json.loads((CACHE / "entries_all.json").read_text(encoding="utf-8"))
    meta = json.loads((CACHE / "meta.json").read_text(encoding="utf-8"))

    repos: list[dict] = []
    seen: set[str] = set()
    for r in rows:
        nwo = r.get("nwo") or ""
        if not nwo or nwo.lower() in seen or "error" in meta.get(nwo, {"error": 1}):
            continue
        seen.add(nwo.lower())
        repos.append({"nwo": nwo, "owner": r["owner"], "repo": r["repo"]})

    rel_path, act_path = CACHE / "releases.json", CACHE / "actions.json"
    force = "--force" in sys.argv
    # Loaded even under --force -- the force is applied to the predicate below instead. Emptying
    # the dicts would also silently prune every repo the lists have dropped, which is a different
    # decision wearing the same flag, and it is the reason a --force here used to cost a full
    # re-crawl of both signals for every repo rather than only the ones being refreshed.
    rel = json.loads(rel_path.read_text(encoding="utf-8")) if rel_path.exists() else {}
    act = json.loads(act_path.read_text(encoding="utf-8")) if act_path.exists() else {}

    # `pushedAt` is refetched in full every run (02_fetch.py --force, then 11_fetch_all.py), so
    # this is the current value for every repo and the comparison below is against what we saw
    # when the entry was written. Both signals are fetched by one query, so either one being
    # stale queues the repo and both get rewritten.
    pushed = {r["nwo"]: sig.meta_push(meta, r["nwo"]) for r in repos}
    todo = [r for r in repos
            if force
            or sig.stale(rel, r["nwo"], pushed[r["nwo"]])
            or sig.stale(act, r["nwo"], pushed[r["nwo"]])]
    print(f"{len(repos)} repos with metadata, {len(todo)} needing signals", flush=True)

    for start in range(0, len(todo), BATCH):
        batch = todo[start:start + BATCH]
        parts = [f'  r{i}: repository(owner: "{e["owner"]}", name: "{e["repo"]}") {{{FIELDS}}}'
                 for i, e in enumerate(batch)]
        try:
            data = json.loads(gh(["api", "graphql", "-f",
                                  "query=query {\n" + "\n".join(parts) + "\n}"])).get("data") or {}
        except RuntimeError:
            data = {}
        for i, e in enumerate(batch):
            n = (data or {}).get(f"r{i}")
            # See 03_releases.py: a null node means the whole batch errored or GitHub had nothing
            # for this repo, so nothing was learned. Leave the cache as it is and stay queued --
            # stamping an empty answer would freeze twelve false negatives per failed batch until
            # each of those repos next gets pushed.
            if not n:
                continue
            assets, tags = [], []
            for node in ((n.get("releases") or {}).get("nodes") or []):
                tags.append(node.get("tagName") or "")
                assets += [a.get("name") or "" for a in
                           ((node.get("releaseAssets") or {}).get("nodes") or [])]
            rel[e["nwo"]] = {"tags": tags, "assets": assets, sig.STAMP: pushed[e["nwo"]]}
            act[e["nwo"]] = sig.action_entry(bool(n.get("yml") or n.get("yaml")),
                                             pushed[e["nwo"]])

        done = min(start + BATCH, len(todo))
        if start % (BATCH * 8) == 0 or done == len(todo):
            rel_path.write_text(json.dumps(rel, indent=1), encoding="utf-8")
            act_path.write_text(json.dumps(act, indent=1), encoding="utf-8")
            print(f"  {done}/{len(todo)}", flush=True)

    rel_path.write_text(json.dumps(rel, indent=1), encoding="utf-8")
    act_path.write_text(json.dumps(act, indent=1), encoding="utf-8")
    with_assets = sum(1 for v in rel.values() if v.get("assets"))
    print(f"\ndone: {len(rel)} repos, {with_assets} publish release assets, "
          f"{sum(1 for v in act.values() if sig.is_action(v))} are GitHub Actions", flush=True)


if __name__ == "__main__":
    main()
