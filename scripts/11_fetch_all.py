"""Fetch metadata + README for every repo across all source lists.

Reuses 02_fetch.py's batching wholesale -- the only new job is collapsing every
row the parser emitted down to the distinct repos behind them, so a project
listed by six lists is still fetched once.

It also owns the one decision about failures that no single repo can make: whether this run's errors
are a few repos that are gone, or GitHub refusing the run as a whole. See `recover`.
"""
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
READMES = CACHE / "readmes"
READMES.mkdir(parents=True, exist_ok=True)

spec = importlib.util.spec_from_file_location("fetch02", Path(__file__).parent / "02_fetch.py")
f2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f2)

BATCH = 20

# --- the mass-failure guard: the numbers, in one place --------------------------------------------
# A run stops when more than this many of the repos it asked about failed for a reason that is not about
# the repo: fifty, or a tenth of the run, whichever is more. Fifty because a few dozen transient misses in
# a twelve-thousand-repo crawl are noise the next run absorbs; a tenth because past that the published
# atlas is visibly emptier than yesterday's. tests/drift_test.py asserts both sides of both numbers.
MASS_FAILURE_FLOOR = 50
MASS_FAILURE_SHARE = 0.10
# Before stopping, the failures that can resolve on their own are asked again, after each of these waits
# in turn. Twenty-one minutes in all, against a daily job timeout of 180, so the worst case still leaves
# the site stages their time. A rate limit whose reset GitHub reports waits for that reset instead, but
# never longer than MAX_WAIT: past fifteen minutes the next scheduled run is the better retry.
RETRY_WAITS = (60, 240, 900)
MAX_WAIT = 900

# How each kind of failure reads in 02_fetch.gh's message, which carries gh's stderr. Lower-cased.
GONE = ("not found", "http 404", "http 451", "repository access blocked", "could not resolve")
AUTH = ("bad credentials", "http 401", "requires authentication", "gh auth login", "not logged",
        "authentication token")
RATE = ("rate limit", "http 429", "secondary rate", "abuse detection", "retry-after", "retry after")


def kind(error: str) -> str:
    """`gone`, `auth`, `rate` or `other` for one repo's error.

    The three that are not `gone` call for different things. `auth` is a token GitHub will not accept,
    which no amount of waiting fixes and which fails every request alike. `rate` is a token GitHub has
    accepted and is throttling, which waiting does fix. `other` -- a 502, a timeout, a reset connection --
    usually fixes itself too, so it is retried with the rate limits.
    """
    e = (error or "").lower()
    for name, marks in (("gone", GONE), ("auth", AUTH), ("rate", RATE)):
        if any(m in e for m in marks):
            return name
    return "other"


def failing(want: list[dict], meta: dict) -> dict[str, list[str]]:
    """Repos this run asked about that errored, by `kind`, leaving out the ones that are gone."""
    out: dict[str, list[str]] = {"auth": [], "rate": [], "other": []}
    for w in want:
        err = (meta.get(w["nwo"]) or {}).get("error")
        if err is not None and kind(err) != "gone":
            out[kind(err)].append(w["nwo"])
    return out


def threshold(asked: int) -> float:
    return max(MASS_FAILURE_FLOOR, MASS_FAILURE_SHARE * asked)


def mass_failure(want: list[dict], meta: dict) -> str | None:
    """Why this run must not publish, or None. Reads the failures as they stand; `recover` retries first."""
    f = failing(want, meta)
    bad = f["auth"] + f["rate"] + f["other"]
    if len(bad) <= threshold(len(want)):
        return None
    if len(f["auth"]) > threshold(len(want)):
        why = ("GitHub rejected the token itself (a 401 or bad credentials), so no request this run made "
               "could have succeeded. Check GH_TOKEN; waiting will not help")
    elif f["rate"]:
        why = (f"{len(f['rate'])} were rate limits that outlasted every retry, and {len(f['other'])} other "
               f"errors not about the repo")
    else:
        why = "the errors are not about the repos -- GitHub having a bad hour, most likely"
    return (f"{len(bad)} of the {len(want)} repos asked about failed for a reason that is not about the "
            f"repo, over the limit of {threshold(len(want)):.0f} (first: "
            f"{meta[bad[0]]['error'][:160]!r}). {why}. Publishing would strip their metadata from the "
            f"atlas, so this stops and the next run asks again.")


def reset_wait(now: float | None = None) -> float | None:
    """Seconds until an exhausted rate limit resets, by GitHub's own account; None if none is exhausted
    or GitHub will not say (which is itself what an exhausted secondary limit looks like)."""
    out = subprocess.run(
        ["gh", "api", "rate_limit", "--jq",
         "[.resources.core, .resources.graphql] | map(select(.remaining == 0) | .reset) | max // 0"],
        capture_output=True, text=True)
    try:
        reset = int(out.stdout.strip() or 0)
    except ValueError:
        return None
    if out.returncode != 0 or not reset:
        return None
    return max(0.0, reset - (now if now is not None else time.time()) + 5)


def recover(want: list[dict], meta: dict, fetch, sleep=time.sleep, wait_for_reset=reset_wait,
            log=print) -> str | None:
    """Ask again about the failures that can resolve on their own, then decide. Returns `mass_failure`.

    A repo that errors is tolerated one at a time, and has to be: a few percent of any list points at
    something deleted, renamed past following, or private, and each of those is a row with no stars, not
    a reason to stop. But the same tolerance turns an outage into a publish. A token that lapsed, a rate
    limit, or GitHub having a bad hour comes back as an error on *every* repo, each one individually
    acceptable, so the build carried on and would have published thousands of rows with no stars, no
    README and no platform verdicts -- the atlas emptied out on a green run.

    So past the threshold this run does not publish, but it does not give up at the first sign either,
    because the two causes differ. An auth failure stops at once: the token is wrong, every retry would
    fail the same way, and twenty minutes of waiting would only delay the message. A rate limit or a
    transient error is retried -- just those repos, after each wait in RETRY_WAITS, or until GitHub's
    reported reset -- and the run stops only if the failures are still over the threshold after the last
    round. Stopping is safe for the same reason as `13_signals_all`'s: nothing is committed or recorded
    as built until every stage passes, so the next run re-reads the lists and asks again. A guard, not
    drift: no edit to a list causes it, and no provisional placement could make the result right.
    """
    for round_, wait in enumerate(RETRY_WAITS, start=1):
        f = failing(want, meta)
        bad = f["auth"] + f["rate"] + f["other"]
        if len(bad) <= threshold(len(want)):
            return None
        if len(f["auth"]) > threshold(len(want)):
            break
        retry = f["rate"] + f["other"]
        if f["rate"]:
            told = wait_for_reset()
            if told is not None:
                wait = max(wait, told)
        wait = min(wait, MAX_WAIT)
        log(f"  {len(bad)} of {len(want)} failed for a reason not about the repo "
            f"({len(f['rate'])} rate-limited, {len(f['other'])} other, {len(f['auth'])} auth); "
            f"retry {round_}/{len(RETRY_WAITS)} of {len(retry)} in {wait:.0f}s", flush=True)
        sleep(wait)
        for n in retry:
            meta.pop(n, None)
        fetch([w for w in want if w["nwo"] in set(retry)], meta)
    return mass_failure(want, meta)


def fetch(want: list[dict], meta: dict, save=None) -> None:
    """Metadata and README for each of `want`, into `meta` and cache/readmes/. `save` checkpoints."""
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
        if save and (start % (BATCH * 5) == 0 or done == len(want)):
            save()
            print(f"  {done}/{len(want)}", flush=True)


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

    def save() -> None:
        meta_path.write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")

    fetch(want, meta, save)
    refusal = recover(want, meta, lambda w, m: fetch(w, m, save))
    save()
    ok = [v for v in meta.values() if "error" not in v]
    print(f"\ndone: {len(meta)} records, {len(ok)} ok, {len(meta) - len(ok)} errors", flush=True)
    if refusal:
        sys.exit(refusal)


if __name__ == "__main__":
    main()
