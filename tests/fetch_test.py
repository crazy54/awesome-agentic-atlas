"""The batch fetch's failure handling in `scripts/02_fetch.py`, against a fake `gh`.

Every stage that asks GitHub for repository nodes goes through `graphql_batch`: 02_fetch, 03_releases,
03b_actions, 11_fetch_all and 13_signals_all. A batch that fails for good takes the daily build down, on
purpose, so what counts as "for good" decides whether the site updates. Nothing else in the suite can
see that, because the real call needs a token and a network. So `gh_raw` is replaced here with a fake
that answers the way GitHub does, and `time.sleep` with a no-op.

Four groups:

  the split     -- a batch GitHub keeps timing out on (502/504, or a TIMEOUT error) is split and each half
                   asked separately, and the caller gets back one `data` dict with every alias where its
                   position says it should be. This is daily run 35881532013, where one 15-repo batch in
                   03_releases.py got 502, 504, 502 and failed the build.
  what is not   -- a rate limit, a query GitHub rejected, and a single repo that times out on its own.
                   Each one raises, as it did before the split existed, and none of them is asked about
                   more often than it was.
  the allowance -- once the per-process split budget is spent, a timing-out batch raises after its
                   three attempts with no split, so an outage costs what it did before.
  unchanged     -- a good batch is one call, and a NOT_FOUND alias is still ridden past as a null node.

Run: python tests/fetch_test.py
"""
from __future__ import annotations

import importlib.util
import io
import json
import re
import subprocess
import sys
from contextlib import redirect_stderr
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
spec = importlib.util.spec_from_file_location("fetch02", SCRIPTS / "02_fetch.py")
f2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f2)
f2.time.sleep = lambda s: None

ok = bad = 0


def true(name: str, cond, detail: str = "") -> None:
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}" + (f"\n  {detail}" if detail else ""))


ALIAS = re.compile(r'(r\d+): repository\(owner: "([^"]+)", name: "([^"]+)"\)')


class FakeGh:
    """Answers `gh api graphql` the way GitHub does, decided by `rule(aliases)`.

    `rule` gets the list of (alias, owner, name) in the query and returns one of:
      "ok"         -- a full `data` body, one node per alias carrying its own name
      "502"/"504"  -- what gh prints for a gateway timeout: exit 1, `gh: HTTP 502` on stderr, HTML body
      "timeout"    -- a JSON body with a TIMEOUT error and no data
      "ratelimit"  -- a JSON body with a RATE_LIMITED error
      "rejected"   -- an undefinedField error: read, understood, refused
    """

    def __init__(self, rule):
        self.rule = rule
        self.calls: list[int] = []   # the size of each query asked

    def __call__(self, args):
        if args[:2] == ["api", "rate_limit"]:
            # _retry_wait asks this after a RATE_LIMITED. A reset of "now" means no wait.
            import time
            body = {"resources": {"graphql": {"reset": int(time.time())}}}
            return subprocess.CompletedProcess(args, 0, json.dumps(body), "")
        query = next(a for a in args if a.startswith("query="))
        aliases = ALIAS.findall(query)
        self.calls.append(len(aliases))
        verdict = self.rule(aliases)
        cp = lambda rc, out, err="": subprocess.CompletedProcess(args, rc, out, err)
        if verdict == "ok":
            data = {a: ({"nameWithOwner": f"{o}/{n}"} if n != "gone" else None) for a, o, n in aliases}
            errs = [{"type": "NOT_FOUND", "path": [a]} for a, o, n in aliases if n == "gone"]
            body = {"data": data, **({"errors": errs} if errs else {})}
            return cp(1 if errs else 0, json.dumps(body))
        if verdict in ("502", "504"):
            return cp(1, "<html><body>Bad gateway</body></html>", f"gh: HTTP {verdict}")
        if verdict == "timeout":
            return cp(1, json.dumps({"data": None, "errors": [{"type": "TIMEOUT", "message": "took too long"}]}))
        if verdict == "ratelimit":
            return cp(1, json.dumps({"errors": [{"type": "RATE_LIMITED", "message": "API rate limit exceeded"}]}))
        if verdict == "rejected":
            return cp(1, json.dumps({"errors": [{"type": "undefinedField", "message": "no such field"}]}))
        raise AssertionError(verdict)


def batch(n: int, names=None) -> list[dict]:
    names = names or [f"repo{i}" for i in range(n)]
    return [{"owner": "o", "repo": names[i], "nwo": f"o/{names[i]}"} for i in range(n)]


def run(fake: FakeGh, b: list[dict], splits: int = f2.SPLIT_BUDGET):
    """One graphql_batch call against `fake`, with a fresh allowance. Returns (data, error, stderr)."""
    f2.gh_raw = fake
    f2._splits_left = splits
    f2._retry_spent = 0.0
    err = io.StringIO()
    with redirect_stderr(err):
        try:
            return f2.graphql_batch(b, "nameWithOwner"), None, err.getvalue()
        except RuntimeError as exc:
            return None, exc, err.getvalue()


def aligned(data: dict, b: list[dict]) -> list[str]:
    """Every alias whose node is not the repo at that position in the batch the caller passed."""
    return [f"r{i}" for i, e in enumerate(b)
            if (data.get(f"r{i}") or {}).get("nameWithOwner") != e["nwo"]]


print("the split")
for verdict in ("502", "504", "timeout"):
    # GitHub gives up on any query of more than four repos: 15 -> 8 + 7 -> 4 + 4 + 4 + 3.
    fake = FakeGh(lambda al, v=verdict: v if len(al) > 4 else "ok")
    b = batch(15)
    data, exc, log = run(fake, b)
    true(f"a 15-repo batch that keeps getting {verdict} comes back whole, split into halves", exc is None,
         str(exc))
    if data is not None:
        true(f"...with all 15 aliases, each holding the repo at its own position ({verdict})",
             len(data) == 15 and not aligned(data, b), f"{len(data)} aliases, misplaced {aligned(data, b)}")
    true(f"...having asked the full batch three times before splitting it ({verdict})",
         fake.calls[:3] == [15, 15, 15] and fake.calls[3] == 8, str(fake.calls))
    true(f"...and says so on stderr, where the retries are logged ({verdict})",
         "splitting 15-repo batch into 8 + 7" in log, log[:300])

# Uneven sizes, where an off-by-one in the renumbering would show.
for n in (2, 3, 7, 25):
    fake = FakeGh(lambda al: "502" if len(al) > 1 else "ok")
    b = batch(n)
    data, exc, _ = run(fake, b, splits=10**6)
    true(f"a {n}-repo batch split all the way down to single repos keeps every alias in place",
         exc is None and data is not None and len(data) == n and not aligned(data, b),
         str(exc) if exc else f"misplaced {aligned(data, b)}")

# A NOT_FOUND inside a half that did answer is still a null node at the right position.
names = [f"repo{i}" for i in range(10)]
names[7] = "gone"
fake = FakeGh(lambda al: "502" if len(al) > 5 else "ok")
b = batch(10, names)
data, exc, _ = run(fake, b)
true("a deleted repo in the second half is a null node at its own position, not a neighbour's",
     exc is None and data is not None and data.get("r7") is None and
     [k for k in aligned(data, b) if k != "r7"] == [],
     str(exc) if exc else json.dumps(data)[:300])

print("what is not split")
fake = FakeGh(lambda al: "502" if any(n == "repo3" for _, _, n in al) else "ok")
data, exc, _ = run(fake, batch(6))
true("a repo that times out even on its own still fails the batch", exc is not None and data is None)
true("...and the error names the 502, so the log says why", exc is not None and "502" in str(exc), str(exc))

fake = FakeGh(lambda al: "ratelimit")
data, exc, log = run(fake, batch(15))
true("a rate limit raises without splitting, because two halves would spend the limit twice as fast",
     exc is not None and fake.calls == [15, 15, 15] and "splitting" not in log, str(fake.calls))

fake = FakeGh(lambda al: "rejected")
data, exc, log = run(fake, batch(15))
true("a query GitHub rejected is asked once and never split", exc is not None and fake.calls == [15],
     str(fake.calls))

print("the allowance")
fake = FakeGh(lambda al: "502")
data, exc, log = run(fake, batch(15), splits=0)
true("with the split allowance spent, a timing-out batch raises after its three attempts",
     exc is not None and fake.calls == [15, 15, 15] and "splitting" not in log, str(fake.calls))

fake = FakeGh(lambda al: "502")
data, exc, log = run(fake, batch(16), splits=3)
true("an outage stops splitting when the allowance runs out, rather than splitting every batch to single repos",
     exc is not None and f2._splits_left == 0 and len(fake.calls) <= 3 * (1 + 2 * 3),
     f"{len(fake.calls)} calls, {f2._splits_left} splits left")

# The other allowance. Once the process has spent RETRY_BUDGET sleeping, 02_fetch has decided GitHub is
# down and fails each batch on its first attempt. A split there would put the outage's cost back.
fake = FakeGh(lambda al: "502")
f2.gh_raw = fake
f2._splits_left = f2.SPLIT_BUDGET
f2._retry_spent = f2.RETRY_BUDGET
with redirect_stderr(io.StringIO()) as log:
    try:
        f2.graphql_batch(batch(15), "nameWithOwner")
        raised = False
    except RuntimeError:
        raised = True
true("with the retry sleep budget spent, a timing-out batch fails on its first call and is not split",
     raised and fake.calls == [15] and "splitting" not in log.getvalue(), str(fake.calls))
f2._retry_spent = 0.0
true("the allowance is sized for a few slow batches, not for an outage", 4 <= f2.SPLIT_BUDGET <= 64,
     str(f2.SPLIT_BUDGET))

print("unchanged")
fake = FakeGh(lambda al: "ok")
b = batch(20)
data, exc, _ = run(fake, b)
true("a good batch is one call and comes back as-is", exc is None and fake.calls == [20] and not aligned(data, b),
     str(fake.calls))
names = [f"repo{i}" for i in range(5)]
names[2] = "gone"
fake = FakeGh(lambda al: "ok")
data, exc, _ = run(fake, batch(5, names))
true("a NOT_FOUND alias is ridden past as a null node, with gh's exit 1 ignored",
     exc is None and data is not None and data.get("r2") is None and len(fake.calls) == 1, str(exc))

print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
