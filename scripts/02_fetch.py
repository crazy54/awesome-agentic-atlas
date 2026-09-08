"""Fetch repo metadata (stars, language, license, ...) plus README text for every entry.

Batched GraphQL for speed, with a REST fallback for repos whose README is not
literally README.md or that have been renamed/moved.
"""
import json
import random
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
READMES = CACHE / "readmes"
# Created here rather than assumed, because on a cold cache this stage is the first thing in either
# pipeline to touch the directory and `write_text` does not make parents. `cache/` is untracked and
# nothing in the repo ships it, so every checkout starts cold: run 34153712009 of weekly.yml died on
# exactly this line, at stage two of twenty, after spending the GraphQL budget that produced the text
# it was trying to save. The same two lines were already in 11_fetch_all.py, which runs *after* this
# one and so never got the chance to help. `parents=True` also makes `cache/` itself, which is what
# this stage's own `meta.json` write needs and what every later stage assumes somebody made.
READMES.mkdir(parents=True, exist_ok=True)
BATCH = 20
MAX_README = 240_000

# Three attempts per batch, and the reason it is three is arithmetic rather than taste. A full run
# sends about 1,200 batches through here -- 442 from 11_fetch_all.py at twenty repos each, 737 from
# 13_signals_all.py at twelve, the rest from the curated stages -- and those two stages now stop the
# build when any one batch fails outright, which is the right behaviour and also the expensive one.
# On a single attempt a 0.1% per-batch blip reddens the daily build 70% of the time, three weeks a
# month, and 0.5% reddens it 99.8%, which is a red tick every single day and therefore a tick nobody
# reads any more: the silent-empty problem again, wearing the other hat. Cubing the failure takes
# 0.1% to about one red build in two thousand years and 0.5% to one in eighteen, so the blip stops
# mattering and a build that does go red is worth walking over to look at. A fourth attempt buys
# nothing anyone would notice and costs another wait on every genuine outage.
#
# RETRY_BUDGET, not RETRY_ATTEMPTS, is what keeps a real outage inside the job's 180-minute timeout.
# Per batch the ceiling is small, but when GitHub is simply down every batch spends every attempt: at
# the measured 4.4s a signals batch, that stage alone becomes 162 minutes of network plus 55 of
# sleeping, so the retry would convert a clean, well-logged failure into the timeout that the limit
# was raised to avoid -- the quietest failure there is, since a killed job commits nothing and says
# nothing. Hence a sleep allowance for the process rather than for each batch. The first sixty-odd
# batches get their full backoff and every batch after that fails on its first attempt with no wait
# at all: 69 minutes end to end, a log full of the reason, and a non-zero exit. Note the allowance is
# per process, so a workflow that runs five of these stages can spend five lots of it; twenty-five
# minutes of waiting is still nowhere near the limit, and failed calls return far faster than the
# 4.4s a successful one takes, so the figures above are the pessimistic end.
RETRY_ATTEMPTS = 3
RETRY_BASE = 1.5
RETRY_CAP = 45.0
RETRY_BUDGET = 300.0
_retry_spent = 0.0

# Error classes where the identical query might work on the next attempt. Anything GitHub read and
# rejected on its merits is absent on purpose -- see _transient below.
TRANSIENT_TYPES = {"RATE_LIMITED", "SERVICE_UNAVAILABLE", "INTERNAL", "TIMEOUT"}

FIELDS = """
    nameWithOwner
    description
    stargazerCount
    forkCount
    isArchived
    isFork
    createdAt
    pushedAt
    homepageUrl
    primaryLanguage { name }
    licenseInfo { spdxId name }
    defaultBranchRef { name }
    repositoryTopics(first: 20) { nodes { topic { name } } }
    readme: object(expression: "HEAD:README.md") { ... on Blob { text } }
"""


def gh_raw(args: list[str]) -> subprocess.CompletedProcess:
    """The call without the verdict: exists so graphql_batch can read a body gh exited 1 on."""
    return subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")


def gh(args: list[str]) -> str:
    p = gh_raw(args)
    if p.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args[:3])} failed: {p.stderr[:600]}")
    return p.stdout


def _transient(p: subprocess.CompletedProcess, doc) -> bool:
    """Could the identical query plausibly succeed if we simply asked again?

    The line drawn here is between "GitHub read the query and refused it" and "we never got a
    coherent answer, or were told to come back later". A rejected query is rejected the same way for
    ever, so retrying a bad token or a misspelled field only delays the error message by six seconds.
    A 502, a reset connection, a rate limit or half a body is the opposite: the query was fine and the
    minute was bad. Unrecognised-but-coherent JSON is treated as transient on purpose -- being wrong
    that way costs a few seconds and then raises anyway, while being wrong the other way is a red
    build for something that would have worked.
    """
    if not isinstance(doc, dict):
        return True                     # a proxy's HTML, a truncated body, nothing at all
    errs = [e for e in doc.get("errors") or [] if isinstance(e, dict)]
    if any(e.get("type") in TRANSIENT_TYPES for e in errs):
        return True
    status = str(doc.get("status") or "")
    if status.startswith("5") or status == "429":
        return True
    blob = f"{doc.get('message') or ''} {p.stderr or ''}".lower()
    if "secondary rate limit" in blob or "abuse detection" in blob:
        return True
    if status == "403" and "rate limit" in blob:
        return True
    if errs:
        return False                    # undefinedField, a syntax error: read, understood, refused
    if status or doc.get("message"):
        return False                    # REST-shaped refusal: Bad credentials, 404, 422
    return True


def _retry_wait(p: subprocess.CompletedProcess, attempt: int) -> float:
    """How long to hold off: what GitHub asked for if it said, otherwise exponential with jitter.

    Sleeping a flat two seconds on an hourly budget that has not turned over yet just spends the
    remaining attempts on the same answer, so a rate limit is asked about rather than guessed at.
    `gh` prints only the response body, and the GraphQL rate-limit body does not carry its own reset,
    but `/rate_limit` does and querying it is documented not to count against any limit. Capped
    regardless: if the window is half an hour out, waiting RETRY_CAP and then failing the batch is
    the honest outcome -- 13_signals_all.py will put it back in the queue for the next run.
    """
    hint = None
    m = re.search(r"retry[- ]after:?\s*(\d+)", f"{p.stderr or ''} {p.stdout or ''}", re.I)
    if m:
        hint = float(m.group(1))
    elif "RATE_LIMITED" in (p.stdout or ""):
        try:
            reset = json.loads(gh(["api", "rate_limit"]))["resources"]["graphql"]["reset"]
            hint = float(reset) - time.time()
        except (RuntimeError, ValueError, KeyError, TypeError):
            hint = None
    if hint is not None:
        return max(0.5, min(hint, RETRY_CAP) + random.random())
    # Jitter is a spread, not a decoration: every batch in a run hits the same endpoint from the same
    # runner, so a fixed backoff would march them all back into whatever just failed in lockstep.
    return max(0.5, min(RETRY_BASE * 2 ** (attempt - 1), RETRY_CAP) * (0.5 + random.random()))


def graphql_batch(batch: list[dict], fields: str = FIELDS) -> dict:
    """One aliased query for the whole batch. `fields` so 03/03b/13 share the triage below.

    The default is this stage's own FIELDS, which is what 11_fetch_all.py wants and why it can keep
    calling this with one argument. The release and Actions stages ask for different fields off the
    same `repository` nodes, and the only reason they pass their own in here rather than building
    their own query is that there must be exactly one answer in the tree to "what does a non-zero
    exit from `gh api graphql` mean" -- see below for why getting that wrong is expensive.
    """
    parts = []
    for i, e in enumerate(batch):
        owner = e["owner"].replace('"', '')
        repo = e["repo"].replace('"', '')
        parts.append(f'  r{i}: repository(owner: "{owner}", name: "{repo}") {{{fields}}}')
    query = "query {\n" + "\n".join(parts) + "\n}"
    # Not through gh(), and that is the whole point. `gh api graphql` exits 1 when *any* one alias in
    # the batch fails to resolve -- a repo deleted, renamed away or turned private -- even though it
    # has already printed a complete, valid body on stdout with the other nineteen repos present and
    # the dead one as a null. Letting that exit code stand for the call meant one dead repo sent all
    # twenty down rest_fallback at up to two REST requests each. 3.6% of the atlas is unresolvable on
    # any given day, which poisons two batches of twenty in five, so the bill was thousands of REST
    # calls where a few hundred GraphQL queries would do -- against a token that gets 1,000 requests
    # an hour inside Actions.
    #
    # So the body decides, not the exit code -- but only when there is a body. A `data` object means
    # GitHub answered, and every alias it answered for is good. Bad credentials (a 401 whose body has
    # no `data` key at all), a query GitHub rejected, a 5xx, HTML from a proxy, stdout that is not
    # JSON: every one of those still raises. A run that fetched nothing must never be mistaken for a
    # run that found nothing.
    #
    # The loop is here rather than at the five call sites for the same reason the triage is: there
    # must be one answer in the tree to "what does a failed batch mean", and every stage that asks
    # for repository nodes should get the same one.
    global _retry_spent
    for attempt in range(1, RETRY_ATTEMPTS + 1):
        p = gh_raw(["api", "graphql", "-f", f"query={query}"])
        try:
            doc = json.loads(p.stdout)
        except ValueError:
            doc = None
        # NOT_FOUND is the only error class ridden past, and it is per alias by construction: GitHub
        # leaves that alias null, the caller sees no node and falls back to REST for that one repo,
        # which is where renames get followed and where a genuinely dead repo earns its error record.
        # Unchanged from before, in other words. Anything else in `errors` -- RATE_LIMITED above all
        # -- is not a fact about one repo, so it fails the batch the way it always did.
        fatal = []
        if isinstance(doc, dict):
            fatal = [err for err in doc.get("errors") or []
                     if isinstance(err, dict) and err.get("type") != "NOT_FOUND"]
        if isinstance(doc, dict) and isinstance(doc.get("data"), dict) and not fatal:
            return doc["data"]

        why = (json.dumps(fatal[0]) if fatal else (p.stderr or p.stdout or "no output").strip())[:600]
        # Three ways out without sleeping: attempts exhausted, an error that will read the same next
        # time, or the process having already spent its whole sleep allowance on earlier batches.
        if attempt == RETRY_ATTEMPTS or not _transient(p, doc) or _retry_spent >= RETRY_BUDGET:
            raise RuntimeError(f"gh api graphql failed: {why}")
        wait = _retry_wait(p, attempt)
        _retry_spent += wait
        # stderr, and loudly: a retry that nobody sees is a signal thrown away. If these start
        # appearing in the daily log we want to know while the build is still green, because the
        # thing three attempts buys is exactly the thing that hides a rate that is climbing.
        print(f"  retrying {len(batch)}-repo batch, attempt {attempt + 1}/{RETRY_ATTEMPTS} "
              f"in {wait:.1f}s: {why[:160]}", file=sys.stderr, flush=True)
        time.sleep(wait)


def rest_fallback(nwo: str) -> dict:
    """REST follows repo renames and finds README under any filename/casing."""
    out = {}
    try:
        repo = json.loads(gh(["api", f"repos/{nwo}"]))
        out["meta"] = {
            "nameWithOwner": repo.get("full_name"),
            "description": repo.get("description"),
            "stargazerCount": repo.get("stargazers_count"),
            "forkCount": repo.get("forks_count"),
            "isArchived": repo.get("archived"),
            "isFork": repo.get("fork"),
            "createdAt": repo.get("created_at"),
            "pushedAt": repo.get("pushed_at"),
            "homepageUrl": repo.get("homepage"),
            "primaryLanguage": {"name": repo.get("language")} if repo.get("language") else None,
            "licenseInfo": {"spdxId": (repo.get("license") or {}).get("spdx_id")} if repo.get("license") else None,
            "defaultBranchRef": {"name": repo.get("default_branch")},
            "repositoryTopics": {"nodes": [{"topic": {"name": t}} for t in repo.get("topics") or []]},
        }
    except RuntimeError as exc:
        out["error"] = str(exc)[:300]
        return out
    try:
        out["readme"] = gh(["api", f"repos/{nwo}/readme", "-H", "Accept: application/vnd.github.raw"])
    except RuntimeError:
        out["readme"] = ""
    return out


def main() -> None:
    entries = json.loads((CACHE / "entries.json").read_text(encoding="utf-8"))
    force = "--force" in sys.argv
    meta_path = CACHE / "meta.json"
    meta = {} if force else json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}

    todo = [e for e in entries if e["nwo"] not in meta]
    print(f"{len(entries)} entries, {len(todo)} to fetch")

    for start in range(0, len(todo), BATCH):
        batch = todo[start : start + BATCH]
        try:
            data = graphql_batch(batch)
        except RuntimeError as exc:
            print(f"  batch {start} graphql error, falling back per-repo: {exc[:120] if isinstance(exc, str) else exc}")
            data = {}
        for i, e in enumerate(batch):
            node = data.get(f"r{i}") if data else None
            readme_text = ""
            if node:
                readme_text = ((node.get("readme") or {}).get("text")) or ""
                record = {k: v for k, v in node.items() if k != "readme"}
                if not readme_text:
                    fb = rest_fallback(e["nwo"])
                    readme_text = fb.get("readme") or ""
            else:
                fb = rest_fallback(e["nwo"])
                if "error" in fb:
                    print(f"  ! {e['nwo']}: {fb['error'][:100]}")
                    meta[e["nwo"]] = {"error": fb["error"], "readme_bytes": 0}
                    continue
                record = fb["meta"]
                readme_text = fb.get("readme") or ""

            record["readme_bytes"] = len(readme_text)
            meta[e["nwo"]] = record
            if readme_text:
                safe = e["nwo"].replace("/", "__")
                (READMES / f"{safe}.md").write_text(readme_text[:MAX_README], encoding="utf-8")
        done = min(start + BATCH, len(todo))
        print(f"  fetched {done}/{len(todo)}")
        meta_path.write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")

    meta_path.write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")

    ok = [v for v in meta.values() if "error" not in v]
    no_readme = [k for k, v in meta.items() if v.get("readme_bytes", 0) == 0]
    print(f"\ndone: {len(ok)} ok, {len(meta) - len(ok)} errors, {len(no_readme)} without README")
    for k in no_readme:
        print(f"  no readme: {k}")
    top = sorted(((v.get("stargazerCount") or 0, k) for k, v in meta.items()), reverse=True)[:10]
    print("\ntop 10 by stars:")
    for stars, k in top:
        print(f"  {stars:7,d}  {k}")


if __name__ == "__main__":
    main()
