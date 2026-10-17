"""The weekly dead-repo scan: which listed repositories GitHub no longer serves.

A repo that was deleted, made private or disabled still sits in its source list, so the build kept
publishing it: a card with no picture (its Open Graph image 404s), a detail page whose README reader
loads nothing, and "GitHub returned an error" where the platform verdicts should be. Readers noticed.
This stage asks GitHub about every repository the site lists, once a week, and records the ones that
are gone in `state/dead-repos.json`, a committed ledger. `14_classify_all.py` drops every row whose
repo is in the ledger, so the next build publishes none of them -- on the site, in the Markdown
edition and in the workbooks alike.

WHAT COUNTS AS DEAD. GraphQL answers NOT_FOUND for the repo, and then the REST API, asked directly,
answers 404 (gone or private), 451 (taken down) or 403 with a `block` (access blocked) -- REST is asked
because it follows renames, so a repo that moved is alive under its new name and is never recorded. A
repo GitHub has disabled is dead too. An *archived* repo is not: it is read-only, but its page, picture and README still load, and the
list chose to keep it.

WHAT IS NOT DEAD, ON PURPOSE. Anything that failed for a reason that is not about the repo -- a rate
limit, a 5xx, a timeout, bad credentials -- raises, and the run writes nothing. A run that could not
ask must never be mistaken for a run that found nothing alive. As a second guard, a scan that would
newly bury more than MAX_NEW_SHARE of the atlas at once refuses to: that is an outage or a token
problem, not a week of deletions.

COMING BACK. Every repo in the ledger is asked about again each week; one that answers is removed from
it, and the next build lists it again.

    python scripts/dead_repos.py              # scan, update the ledger, print a report
    python scripts/dead_repos.py --dry-run    # scan and report, write nothing
    python scripts/dead_repos.py --status     # read the ledger only: no network

Writes `state/dead-repos.json` and, when run in Actions, a summary to `$GITHUB_STEP_SUMMARY`.
"""
from __future__ import annotations

import datetime as dt
import importlib.util
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "docs" / "data.json"
LEDGER = ROOT / "state" / "dead-repos.json"
BATCH = 50                       # repository nodes per GraphQL query: two small fields each, one point a query
MAX_NEW_SHARE = 0.10             # refuse a scan that would newly bury more than this share of the atlas
GONE = {"404", "451"}            # REST statuses that mean the repo is gone: deleted or private, taken down

FIELDS = """
    nameWithOwner
    isDisabled
"""


def _fetch():
    """02_fetch.py's GraphQL batch, for its one answer to "what does a failed batch mean"."""
    spec = importlib.util.spec_from_file_location("fetch02", Path(__file__).parent / "02_fetch.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_ledger(path: Path | None = None) -> dict:
    path = path or LEDGER
    if not path.exists():
        return {"checked": "", "repos": {}}
    doc = json.loads(path.read_text(encoding="utf-8"))
    doc.setdefault("repos", {})
    return doc


def listed_repos(data_path: Path | None = None) -> list[str]:
    """Every distinct owner/name the published site lists, in a stable order."""
    d = json.loads((data_path or DATA).read_text(encoding="utf-8"))
    i = d["cols"].index("nwo")
    return sorted({r[i] for r in d["rows"] if r[i] and r[i].count("/") == 1})


def rest_status(fetch, nwo: str) -> tuple[str, str]:
    """REST's answer for one repo: ("200", its name now) if it resolves, renamed or not; "404" or "451"
    if it is gone; "blocked" if GitHub has blocked access to it. The status line decides, not gh's exit
    code. Raises on anything that is not a statement about the repo -- a 403 rate limit above all."""
    p = fetch.gh_raw(["api", f"repos/{nwo}", "-i"])
    out = (p.stdout or "").replace("\r\n", "\n")
    head, _, rest = out.partition("\n")
    status = head.split()[1] if head.startswith("HTTP/") and len(head.split()) > 1 else ""
    try:
        body = json.loads(rest.partition("\n\n")[2] or "{}")
    except ValueError:
        body = {}
    body = body if isinstance(body, dict) else {}
    if status == "200" and p.returncode == 0:
        return "200", body.get("full_name") or nwo
    if status in GONE:
        return status, ""
    # A repo disabled for breaking the terms of service answers 403 with a `block` object; a rate limit
    # answers 403 without one.
    if status == "403" and isinstance(body.get("block"), dict):
        return "blocked", ""
    raise RuntimeError(f"repos/{nwo}: HTTP {status or '?'}: {(p.stderr or out)[:200]}")


def scan(nwos: list[str], fetch=None) -> dict[str, dict]:
    """{nwo: {"status": "404" | "451" | "blocked" | "disabled"}} for every one of `nwos` GitHub no longer serves."""
    fetch = fetch or _fetch()
    dead: dict[str, dict] = {}
    for start in range(0, len(nwos), BATCH):
        part = nwos[start:start + BATCH]
        batch = [{"owner": n.split("/")[0], "repo": n.split("/")[1]} for n in part]
        data = fetch.graphql_batch(batch, FIELDS)
        for i, nwo in enumerate(part):
            node = data.get(f"r{i}")
            if node:
                if node.get("isDisabled"):
                    dead[nwo] = {"status": "disabled"}
                continue
            status, _ = rest_status(fetch, nwo)
            if status != "200":
                dead[nwo] = {"status": status}
        print(f"  asked about {min(start + BATCH, len(nwos))}/{len(nwos)}; {len(dead)} gone so far",
              flush=True)
    return dead


def update(ledger: dict, listed: list[str], dead: dict[str, dict], today: str) -> tuple[dict, list, list]:
    """The new ledger, and the repos newly buried and revived. A repo stays in the ledger only while it
    is still gone; `since` is the first scan that found it gone."""
    old = ledger.get("repos", {})
    asked = set(listed) | set(old)
    repos = {}
    for nwo in sorted(asked):
        if nwo in dead:
            prev = old.get(nwo, {})
            repos[nwo] = {"status": dead[nwo]["status"], "since": prev.get("since") or today, "seen": today}
    new = sorted(set(repos) - set(old))
    revived = sorted(set(old) - set(repos))
    return {"checked": today, "repos": repos}, new, revived


def guard(new: list, listed: list[str]) -> None:
    """Refuse a scan that buries too much at once: that is GitHub or the token, not the lists."""
    limit = max(25, int(len(listed) * MAX_NEW_SHARE))
    if len(new) > limit:
        raise SystemExit(f"refusing: this scan would newly mark {len(new)} of {len(listed)} repos dead "
                         f"(limit {limit}). That is an outage or a token problem, not a week of deletions; "
                         f"nothing was written.")


def report(doc: dict, new: list, revived: list, listed_n: int) -> str:
    lines = [f"## Dead repos: {len(doc['repos'])} of {listed_n:,} listed repos are gone from GitHub",
             "", f"Scanned {doc['checked']}. These are left out of the next build of the site, the Markdown "
             f"edition and the workbooks.", ""]
    if new:
        lines += [f"**Newly gone ({len(new)}):**", ""] + [
            f"- [{n}](https://github.com/{n}) ({doc['repos'][n]['status']})" for n in new] + [""]
    if revived:
        lines += [f"**Back again ({len(revived)}), listed from the next build:**", ""] + [
            f"- [{n}](https://github.com/{n})" for n in revived] + [""]
    if not new and not revived:
        lines += ["No change since the last scan.", ""]
    return "\n".join(lines)


def dead_set(path: Path | None = None) -> set[str]:
    """For the build: the repos to leave out. Case-insensitive, as GitHub's names are."""
    return {n.lower() for n in load_ledger(path).get("repos", {})}


def main(argv: list[str]) -> int:
    ledger = load_ledger()
    if "--status" in argv:
        print(f"{len(ledger['repos'])} repos in the ledger, last scan {ledger.get('checked') or 'never'}")
        for n, v in sorted(ledger["repos"].items()):
            print(f"  {n}  {v['status']}  since {v['since']}")
        return 0
    listed = listed_repos()
    nwos = sorted(set(listed) | set(ledger["repos"]))
    print(f"asking GitHub about {len(nwos):,} repos ({len(listed):,} listed, {len(ledger['repos'])} in the ledger)")
    dead = scan(nwos)
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    doc, new, revived = update(ledger, listed, dead, today)
    guard(new, listed)
    text = report(doc, new, revived, len(listed))
    print("\n" + text)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(text + "\n")
    if "--dry-run" in argv:
        print("dry run: nothing written")
        return 0
    LEDGER.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {LEDGER.relative_to(ROOT)}: {len(doc['repos'])} gone, {len(new)} new, {len(revived)} back")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
