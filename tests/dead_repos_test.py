"""The weekly dead-repo scan, `scripts/dead_repos.py`, and the build's use of its ledger -- against a fake
GitHub.

The scan decides which repositories the site stops listing, so the two ways it can be wrong are both
bad: a repo recorded dead that is alive (a rename, a rate limit, an outage) disappears from the atlas,
and a dead one left out of the ledger keeps its pictureless card. The real call needs a token and a
network, so the 02_fetch module the scan uses is replaced here with a fake that answers the way GitHub
does -- GraphQL with a null node for NOT_FOUND, REST through `gh api -i` with the status line first.

Five groups:

  the verdict  -- alive, disabled, 404, 451 and blocked are told apart; a rename is alive; a rate limit,
                  a 5xx and a failed GraphQL batch raise instead of answering.
  the batches  -- every repo is asked about once, fifty to a GraphQL query, and REST only for the nulls.
  the ledger   -- newly dead, still dead (keeping its first date) and back again; ledger repos the site
                  no longer lists are still asked about, which is how one comes back.
  the guard    -- a scan that would bury too much of the atlas at once refuses and writes nothing.
  the build    -- 14_classify_all.py leaves every ledger repo out, matched without regard to case, and
                  keeps everything else, including rows with no repo at all.

Run: python tests/dead_repos_test.py
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))
import dead_repos as dr  # noqa: E402

ok = bad = 0


def true(name: str, cond, detail: str = "") -> None:
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}" + (f"\n  {detail}" if detail else ""))


def raises(name: str, fn, kind=Exception) -> None:
    try:
        fn()
    except kind:
        true(name, True)
        return
    except Exception as e:  # the wrong kind is as much a failure as none
        true(name, False, f"raised {type(e).__name__}: {e}")
        return
    true(name, False, "did not raise")


def http(status: str, body: dict, rc: int | None = None, crlf: bool = False) -> subprocess.CompletedProcess:
    """What `gh api -i` prints: the status line, headers, a blank line, the body. gh exits 1 on >= 400."""
    reason = {"200": "OK", "403": "Forbidden", "404": "Not Found", "451": "Unavailable For Legal Reasons",
              "500": "Internal Server Error"}.get(status, "")
    nl = "\r\n" if crlf else "\n"
    out = nl.join([f"HTTP/2.0 {status} {reason}", "Content-Type: application/json; charset=utf-8",
                   "X-Github-Request-Id: 0000:0000", ""]) + nl + json.dumps(body)
    code = rc if rc is not None else (0 if status.startswith("2") else 1)
    return subprocess.CompletedProcess(["gh"], code, out, "" if code == 0 else f"gh: HTTP {status}")


class FakeGitHub:
    """The two calls the scan makes. `world` maps a name to what GitHub would say about it:
       "alive" | "disabled"            -- GraphQL returns a node
       "renamed:<new>"                 -- GraphQL NOT_FOUND, REST 200 under the new name
       "404" | "451" | "blocked"       -- GraphQL NOT_FOUND, REST says so
       "ratelimit" | "500"             -- GraphQL NOT_FOUND, REST fails for a reason not about the repo
    Anything not in `world` is alive."""

    def __init__(self, world: dict[str, str], graphql_fails: bool = False):
        self.world, self.graphql_fails = world, graphql_fails
        self.queries: list[int] = []
        self.rest: list[str] = []

    def graphql_batch(self, batch, fields):
        self.queries.append(len(batch))
        if self.graphql_fails:
            raise RuntimeError("gh api graphql failed: HTTP 502")
        data = {}
        for i, e in enumerate(batch):
            nwo = f"{e['owner']}/{e['repo']}"
            say = self.world.get(nwo, "alive")
            data[f"r{i}"] = ({"nameWithOwner": nwo, "isDisabled": say == "disabled"}
                             if say in ("alive", "disabled") else None)
        return data

    def gh_raw(self, args):
        nwo = args[1].removeprefix("repos/")
        self.rest.append(nwo)
        say = self.world.get(nwo, "alive")
        if say.startswith("renamed:"):
            return http("200", {"full_name": say.split(":", 1)[1]}, crlf=True)
        if say in ("404", "451"):
            return http(say, {"message": "Not Found" if say == "404" else "Repository access blocked"})
        if say == "blocked":
            return http("403", {"message": "Repository access blocked", "block": {"reason": "tos"}})
        if say == "ratelimit":
            return http("403", {"message": "API rate limit exceeded for installation ID 1."})
        if say == "500":
            return http("500", {"message": "Server Error"})
        return http("200", {"full_name": nwo})


def quiet(fn, *a, **k):
    with redirect_stdout(StringIO()):
        return fn(*a, **k)


# ---- the verdict ------------------------------------------------------------------------------------
world = {"a/disabled": "disabled", "a/moved": "renamed:b/moved", "a/gone": "404", "a/dmca": "451",
         "a/tos": "blocked"}
names = ["a/alive", "a/disabled", "a/moved", "a/gone", "a/dmca", "a/tos"]
fake = FakeGitHub(world)
dead = quiet(dr.scan, names, fetch=fake)
true("a live repo is not recorded", "a/alive" not in dead)
true("a renamed repo is alive under its new name, not dead under its old one", "a/moved" not in dead)
true("a disabled repo is dead", dead.get("a/disabled") == {"status": "disabled"}, str(dead))
true("a 404 is dead", dead.get("a/gone") == {"status": "404"}, str(dead))
true("a 451 is dead", dead.get("a/dmca") == {"status": "451"}, str(dead))
true("a 403 carrying a `block` is dead", dead.get("a/tos") == {"status": "blocked"}, str(dead))
true("nothing else is", set(dead) == {"a/disabled", "a/gone", "a/dmca", "a/tos"}, str(sorted(dead)))

raises("a 403 rate limit raises: it is not a statement about the repo",
       lambda: quiet(dr.scan, ["a/x"], fetch=FakeGitHub({"a/x": "ratelimit"})), RuntimeError)
raises("a 500 raises", lambda: quiet(dr.scan, ["a/x"], fetch=FakeGitHub({"a/x": "500"})), RuntimeError)
raises("a GraphQL batch that fails raises, and nothing is concluded from it",
       lambda: quiet(dr.scan, ["a/x"], fetch=FakeGitHub({}, graphql_fails=True)), RuntimeError)


class Exit0On404(FakeGitHub):
    def gh_raw(self, args):
        p = super().gh_raw(args)
        return subprocess.CompletedProcess(p.args, 0, p.stdout, p.stderr)


true("the status line decides, not gh's exit code: a 404 that exits 0 is still a 404",
     quiet(dr.scan, ["a/gone"], fetch=Exit0On404({"a/gone": "404"})) == {"a/gone": {"status": "404"}})
true("...and a 200 with a body that is not JSON is alive under its old name",
     dr.rest_status(type("F", (), {"gh_raw": staticmethod(
         lambda a: subprocess.CompletedProcess(["gh"], 0, "HTTP/2.0 200 OK\n\nnot json", ""))})(), "a/x")
     == ("200", "a/x"))

# ---- the batches ------------------------------------------------------------------------------------
many = [f"o/r{i:03d}" for i in range(120)]
fake = FakeGitHub({"o/r007": "404", "o/r077": "renamed:o/new"})
dead = quiet(dr.scan, many, fetch=fake)
true("120 repos are three GraphQL queries of at most fifty", fake.queries == [50, 50, 20], str(fake.queries))
true("REST is asked only about the repos GraphQL could not find", fake.rest == ["o/r007", "o/r077"],
     str(fake.rest))
true("and the one 404 among them is the one recorded", dead == {"o/r007": {"status": "404"}}, str(dead))

# ---- the ledger -------------------------------------------------------------------------------------
old = {"checked": "2026-10-10", "repos": {
    "x/still": {"status": "404", "since": "2026-09-01", "seen": "2026-10-10"},
    "x/back": {"status": "404", "since": "2026-10-03", "seen": "2026-10-10"},
    "x/unlisted": {"status": "451", "since": "2026-08-01", "seen": "2026-10-10"}}}
listed = ["x/alive", "x/still", "x/new"]
found = {"x/still": {"status": "404"}, "x/new": {"status": "disabled"}, "x/unlisted": {"status": "451"}}
doc, new, revived = dr.update(old, listed, found, "2026-10-17")
true("a newly dead repo is new, dated today", new == ["x/new"] and doc["repos"]["x/new"] ==
     {"status": "disabled", "since": "2026-10-17", "seen": "2026-10-17"}, str(doc))
true("a repo still dead keeps the date it was first found dead",
     doc["repos"]["x/still"] == {"status": "404", "since": "2026-09-01", "seen": "2026-10-17"},
     str(doc["repos"].get("x/still")))
true("a ledger repo that answers again is revived and leaves the ledger",
     revived == ["x/back"] and "x/back" not in doc["repos"], str(revived))
true("a ledger repo the site no longer lists stays while it is still dead",
     doc["repos"].get("x/unlisted", {}).get("since") == "2026-08-01")
true("a live repo is never in the ledger", "x/alive" not in doc["repos"])
true("the scan is dated", doc["checked"] == "2026-10-17")
_, n2, r2 = dr.update(doc, listed, found, "2026-10-24")
true("the same answer next week is no change", n2 == [] and r2 == [], f"{n2} {r2}")

# ---- the guard --------------------------------------------------------------------------------------
atlas = [f"o/r{i}" for i in range(1000)]
true("25 new is allowed on any size of atlas", dr.guard([f"n{i}" for i in range(25)], atlas[:10]) is None)
raises("26 new on a small atlas is refused", lambda: dr.guard([f"n{i}" for i in range(26)], atlas[:10]),
       SystemExit)
true("10% of a large atlas is allowed", dr.guard([f"n{i}" for i in range(100)], atlas) is None)
raises("more than 10% is refused", lambda: dr.guard([f"n{i}" for i in range(101)], atlas), SystemExit)

with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    data = tmp / "data.json"
    data.write_text(json.dumps({"cols": ["name", "nwo"], "rows": [
        [f"r{i}", f"o/r{i}"] for i in range(200)] + [["dup", "o/r1"], ["site", ""], ["sub", "o/r2/tree/x"]]}),
        encoding="utf-8")
    true("the listed set is distinct owner/name pairs off data.json", dr.listed_repos(data) == sorted(
        f"o/r{i}" for i in range(200)), str(len(dr.listed_repos(data))))

    ledger = tmp / "state" / "dead-repos.json"
    ledger.parent.mkdir()
    dr.DATA, dr.LEDGER, dr.ROOT = data, ledger, tmp
    gone = {f"o/r{i}": "404" for i in range(30)}
    dr._fetch = lambda: FakeGitHub(gone)
    raises("a run that would bury 30 of 200 at once refuses", lambda: quiet(dr.main, []), SystemExit)
    true("...and writes no ledger", not ledger.exists())

    gone = {"o/r3": "404", "o/r4": "disabled"}
    dr._fetch = lambda: FakeGitHub(gone)
    quiet(dr.main, ["--dry-run"])
    true("a dry run writes nothing", not ledger.exists())
    quiet(dr.main, [])
    written = json.loads(ledger.read_text(encoding="utf-8"))
    true("a real run writes the ledger", sorted(written["repos"]) == ["o/r3", "o/r4"], str(written))
    true("dead_set reads it", dr.dead_set(ledger) == {"o/r3", "o/r4"})
    true("dead_set without a ledger is empty, so a fresh checkout builds everything",
         dr.dead_set(tmp / "nope.json") == set())

# ---- the build --------------------------------------------------------------------------------------
spec = importlib.util.spec_from_file_location("cls14", SCRIPTS / "14_classify_all.py")
c14 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c14)

with tempfile.TemporaryDirectory() as tmp:
    cache = Path(tmp)

    def row(name, nwo, kind="repo"):
        return {"name": name, "url": f"https://github.com/{nwo}" if nwo else "https://example.com",
                "source": "test", "category": "Things", "description": name, "kind": kind, "nwo": nwo,
                "owner": nwo.split("/")[0] if nwo else "", "repo": nwo.split("/")[-1] if nwo else ""}

    rows = [row("Dead", "Gone/Repo"), row("Also dead", "gone/sub", kind="subpath"),
            row("Alive", "alive/repo"), row("Site", "", kind="site")]
    for name, value in [("entries_all.json", rows), ("meta.json", {}), ("releases.json", {}),
                        ("actions.json", {})]:
        (cache / name).write_text(json.dumps(value), encoding="utf-8")
    c14.CACHE = cache
    c14.dead_set = lambda: {"gone/repo", "gone/sub"}
    log = StringIO()
    with redirect_stdout(log):
        c14.main()
    out = json.loads((cache / "records_all.json").read_text(encoding="utf-8"))
    kept = [r["name"] for r in out]
    true("the build leaves out a ledger repo whatever its case", "Dead" not in kept, str(kept))
    true("...and an item inside a dead repo", "Also dead" not in kept, str(kept))
    true("...and keeps the rest, sites included", kept == ["Alive", "Site"], str(kept))
    true("...and says how many it left out", "left out 2 rows of 2 dead repos" in log.getvalue(),
         log.getvalue()[:200])

print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
