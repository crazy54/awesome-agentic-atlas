"""Fetch metadata + README for every repo across all source lists.

Reuses 02_fetch.py's batching wholesale -- the only new job is collapsing every
row the parser emitted down to the distinct repos behind them, so a project
listed by six lists is still fetched once.
"""
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
READMES = CACHE / "readmes"
READMES.mkdir(parents=True, exist_ok=True)

spec = importlib.util.spec_from_file_location("fetch02", Path(__file__).parent / "02_fetch.py")
f2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f2)

BATCH = 20
# See the end of `main`. Fifty repos, or a tenth of what this run asked about, whichever is more.
MASS_FAILURE_FLOOR = 50
MASS_FAILURE_SHARE = 0.10
# What GitHub says about a repo that is really gone (02_fetch.gh's message carries gh's stderr).
GONE = ("not found", "http 404", "http 451", "repository access blocked", "could not resolve")


def main() -> None:
    rows = json.loads((CACHE / "entries_all.json").read_text(encoding="utf-8"))
    meta_path = CACHE / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}

    # distinct repos, in first-listed order, that we do not already have
    want: list[dict] = []
    seen: set[str] = set()
    for r in rows:
        nwo = r.get("nwo") or ""
        if not nwo or nwo.lower() in seen:
            continue
        seen.add(nwo.lower())
        if nwo in meta:
            continue
        want.append({"nwo": nwo, "owner": r["owner"], "repo": r["repo"]})

    # the source lists themselves get credited on the Sources sheet
    for nwo in sorted({r["source_nwo"] for r in rows}):
        if nwo not in meta and nwo.lower() not in {w["nwo"].lower() for w in want}:
            owner, repo = nwo.split("/", 1)
            want.append({"nwo": nwo, "owner": owner, "repo": repo})

    print(f"{len(seen)} distinct repos referenced, {len(meta)} cached, {len(want)} to fetch",
          flush=True)

    for start in range(0, len(want), BATCH):
        batch = want[start:start + BATCH]
        try:
            data = f2.graphql_batch(batch)
        except RuntimeError as exc:
            print(f"  batch {start}: graphql failed, per-repo fallback ({str(exc)[:90]})", flush=True)
            data = {}
        for i, e in enumerate(batch):
            node = data.get(f"r{i}") if data else None
            readme_text = ""
            if node:
                readme_text = ((node.get("readme") or {}).get("text")) or ""
                record = {k: v for k, v in node.items() if k != "readme"}
                if not readme_text:
                    readme_text = f2.rest_fallback(e["nwo"]).get("readme") or ""
            else:
                fb = f2.rest_fallback(e["nwo"])
                if "error" in fb:
                    meta[e["nwo"]] = {"error": fb["error"], "readme_bytes": 0}
                    continue
                record = fb["meta"]
                readme_text = fb.get("readme") or ""

            record["readme_bytes"] = len(readme_text)
            meta[e["nwo"]] = record
            if readme_text:
                (READMES / f"{e['nwo'].replace('/', '__')}.md").write_text(
                    readme_text[:f2.MAX_README], encoding="utf-8")

        done = min(start + BATCH, len(want))
        if start % (BATCH * 5) == 0 or done == len(want):
            meta_path.write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
            print(f"  {done}/{len(want)}", flush=True)

    meta_path.write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
    ok = [v for v in meta.values() if "error" not in v]
    print(f"\ndone: {len(meta)} records, {len(ok)} ok, {len(meta) - len(ok)} errors", flush=True)

    # A repo that errors is tolerated one at a time, and has to be: a few percent of any list points at
    # something deleted, renamed past following, or private, and each of those is a row with no stars,
    # not a reason to stop. But the same tolerance turns an outage into a publish. A token that lapsed,
    # a rate limit that outlasted the retries, or GitHub having a bad hour comes back as an error on
    # *every* repo, each one individually acceptable, so the build carried on and would have published
    # thousands of rows with no stars, no README and no platform verdicts -- the atlas emptied out on a
    # green run. A repo that is really gone says so (GONE); anything else is about the request, not the
    # repo. Past the floor, a run where those are a tenth of what it asked about stops here. Safe for the
    # same reason as `13_signals_all`'s stop: nothing is committed or recorded as built until every stage
    # passes, so the next run re-reads the lists and asks again. This one is a guard, not drift: no edit
    # to a list can cause it, and no provisional placement could make the published result right.
    refusal = mass_failure(want, meta)
    if refusal:
        sys.exit(refusal)


def mass_failure(want: list[dict], meta: dict) -> str | None:
    """Why this run must not publish, or None. See the end of `main`."""
    failing = [w["nwo"] for w in want if "error" in meta.get(w["nwo"], {})
               and not any(g in meta[w["nwo"]]["error"].lower() for g in GONE)]
    if len(failing) <= max(MASS_FAILURE_FLOOR, MASS_FAILURE_SHARE * len(want)):
        return None
    return (f"{len(failing)} of the {len(want)} repos asked about failed for a reason that is not "
            f"about the repo (first: {meta[failing[0]]['error'][:160]!r}). That is GitHub or the "
            f"token, not the lists, and publishing would strip their metadata from the atlas. "
            f"Stopping, so the next run asks again.")


if __name__ == "__main__":
    main()
