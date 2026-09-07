"""Unit tests for `scripts/26_indexnow.py` and for `20_landing.py`'s key-file prune.

Three things, and each is a defect this file was written after rather than a property somebody thought
might be worth checking.

`url_for` decides which of the ~1,500 files under `docs/` get told to a search engine, by a rule -- "only
`index.html`" -- that is a one-line function and a paragraph of justification. The justification is the
part that can rot: it claims the mapped set is *exactly* what the two sitemaps list. That is checkable
against the committed site, so it is checked, both directions and by content rather than by count. A page
that stops being submitted and a page submitted without ever reaching a sitemap are both failures here.

`prune_keys` deletes files. It used to delete them by name shape, and `[A-Za-z0-9-]{8,128}` matches the
stem of `security.txt` -- eight in-alphabet characters -- so a plausible addition to the site root would
have been removed on every weekly run. It now judges a key file by its content, which is the one property
a key file actually has, and `security.txt` is asserted by name below because that is the specific file
the review found.

And `post` promises in the module docstring that a bad response is a warning and exit 0. `IncompleteRead`,
`BadStatusLine` and `LineTooLong` descend from `HTTPException`, not `OSError`, and `urllib` re-raises them
out of `getresponse()` unwrapped -- so a truncated response, which is precisely the "search engine having
a bad day" case, used to be an uncaught traceback. The class hierarchy those cases turn on is asserted
here too, so the day it changes this file says so instead of quietly testing nothing.

The real weekly run cannot be reproduced here: stages 14+ need `cache/meta.json`, `cache/records_all.json`
and `cache/shots_all.json` from an authenticated GitHub crawl, and `cache/` is not committed. So
`prune_keys` is driven against a temporary directory by redirecting the one global it reads.

NOTHING HERE TOUCHES THE NETWORK, and that is enforced rather than promised: `socket.socket.connect` is
replaced below with a counter that raises, and the count is asserted to be zero at the end. A test of the
IndexNow client that reached api.indexnow.org would be submitting this repository's real URLs with its
real key every time somebody ran the suite.

Run: python tests/indexnow_test.py
"""
from __future__ import annotations

import contextlib
import http.client
import importlib.util
import io
import os
import re
import socket
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

# ---- the network guard, installed before anything is imported that could use one
reached = []


def _no_network(*a, **k):
    reached.append(a[1:] if len(a) > 1 else a)
    raise AssertionError("indexnow_test.py tried to open a socket; it must not")


socket.socket.connect = _no_network
socket.create_connection = _no_network


def load(name: str, filename: str):
    """`importlib` because these module names start with a digit, so `import` cannot reach them."""
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


b26 = load("b26_for_test", "26_indexnow.py")
b20 = load("b20_for_test", "20_landing.py")
SITE = b26.SITE

ok = bad = 0
TMP = Path(tempfile.mkdtemp(prefix="indexnow_test_", dir=os.environ.get("AAA_TMP") or None))


def eq(name: str, got, want) -> None:
    global ok, bad
    if got == want:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}\n  got  {got!r}\n  want {want!r}")


def true(name: str, cond, detail: str = "") -> None:
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}" + (f"\n  {detail}" if detail else ""))


def raises(name: str, fn, want=SystemExit) -> str:
    global ok, bad
    try:
        fn()
    except want as e:
        ok += 1
        return str(e)
    except Exception as e:  # noqa: BLE001 -- the wrong exception is a different failure from none
        bad += 1
        print(f"FAIL {name} raised {type(e).__name__} rather than {want.__name__}: {e}")
        return ""
    bad += 1
    print(f"FAIL {name} did not raise {want.__name__}")
    return ""


# =====================================================================  1. url_for
# The committed site is the artefact, so the comparison is against the sitemaps as they are in the
# checkout and the paths as git has them -- not against a walk of the working tree, which would fold in
# anything a local build left lying around.
def tracked(*paths: str) -> list[str]:
    try:
        out = subprocess.run(["git", "ls-files", *paths], cwd=ROOT, check=True,
                             capture_output=True, text=True, encoding="utf-8").stdout
    except (OSError, subprocess.CalledProcessError) as e:
        raise SystemExit(f"could not list tracked files, so this harness cannot assert on them: {e}")
    return [ln for ln in out.splitlines() if ln.strip()]


def locs(*names: str) -> set[str]:
    found = set()
    for n in names:
        found |= set(re.findall(r"<loc>([^<]+)</loc>",
                                (ROOT / "docs" / n).read_text(encoding="utf-8")))
    return found


docs_files = tracked("docs")
sitemap_urls = locs("sitemap.xml", "sitemap-repos.xml")
mapped = {u for u in (b26.url_for(p) for p in docs_files) if u is not None}

# Both non-empty first. `set() == set()` is true, and a symmetric-difference assertion between two empty
# sets is the exact shape of a test that passes because it ran on nothing -- see tests/README.md.
true("there are tracked files under docs/ to map", len(docs_files) > 1_000, str(len(docs_files)))
true("the sitemaps list URLs", len(sitemap_urls) > 1_000, str(len(sitemap_urls)))

eq("every sitemap URL is mapped by url_for", sorted(sitemap_urls - mapped), [])
eq("and url_for maps nothing the sitemaps do not list", sorted(mapped - sitemap_urls), [])
eq("so the two sets are the same size", len(mapped), len(sitemap_urls))
# Asserted as a number as well, because the two sets being equal is also true if a stage broke and both
# collapsed together. This one is a floor, not a pin, for the reason pagemin_test.py gives: it must not
# fail on an honest new page. 1,452 is what the review measured.
true("...and it is the whole site, not a handful", len(mapped) >= 1_452, f"{len(mapped):,}")
true("every mapped URL is under SITE, which is what check() refuses to submit without",
     all(u.startswith(SITE) for u in mapped) and mapped)

# ---- the root, which is the one case that is not a prefix strip
eq("the root page is SITE itself, with no trailing index.html", b26.url_for("docs/index.html"), SITE)
true("...and SITE already ends in a slash, so that URL has no double one",
     "//" not in b26.url_for("docs/index.html")[len("https://"):])
eq("a topic page is its directory", b26.url_for("docs/topic/agents/index.html"), SITE + "topic/agents/")
eq("a crossing is its directory too", b26.url_for("docs/topic/agents/target/cli/index.html"),
   SITE + "topic/agents/target/cli/")
eq("a detail page is its directory", b26.url_for("docs/repo/owner__name/index.html"),
   SITE + "repo/owner__name/")
eq("a Windows-shaped path maps the same as a posix one",
   b26.url_for("docs\\topic\\agents\\index.html"), SITE + "topic/agents/")
eq("surrounding whitespace is not part of the path", b26.url_for("  docs/index.html\n"), SITE)

# ---- a non-index .html, which is the case the two-branch spelling exists for
eq("a non-index .html at the root is not a page", b26.url_for("docs/notindex.html"), None)
eq("...nor in a directory", b26.url_for("docs/topic/notindex.html"), None)
eq("a file merely ending in index.html is not a directory index",
   b26.url_for("docs/topic/agents/notindex.html"), None)
eq("and neither is a directory called index.html/something",
   b26.url_for("docs/index.html/inner.html"), None)

# ---- everything that must map to None. Every one of these is a real committed path or a real shape.
for path in ("docs/data.json", "docs/sw.js", "docs/pages.css", "docs/detail.css", "docs/detail.js",
             "docs/robots.txt", "docs/sitemap.xml", "docs/sitemap-repos.xml",
             "docs/manifest.webmanifest", "docs/og/agents.png", "docs/og/cards.json",
             "docs/feed.xml", "docs/feed.json", "docs/icon-192.png",
             f"docs/{b20.b19.indexnow_key_file()}"):
    eq(f"{path} is not a page", b26.url_for(path), None)

# ---- outside docs/ nothing is a page, however page-shaped it looks
for path in ("mega-list/topics/agents.md", "mega-list/index.md", "state/first_seen.json",
             "README.md", "scripts/19_pages.py", "index.html", "notdocs/index.html",
             "docs-notes/index.html"):
    eq(f"{path} is outside the site", b26.url_for(path), None)

# The key file must never be submitted, and it is the one None above that would be a real bug: submitting
# it is not a wasted URL, it is telling an engine to index a credential. Asserted against the live name.
true("the live key file is not in the submitted set",
     SITE + b20.b19.indexnow_key_file() not in mapped)

# ---- parse_changed and ordered, which is what a workflow actually hands over
eq("a name-status listing keeps the status letter",
   b26.parse_changed("M\tdocs/index.html\nA\tdocs/topic/a/index.html"),
   {SITE: "M", SITE + "topic/a/": "A"})
eq("a bare path list is read as modified", b26.parse_changed("docs/index.html"), {SITE: "M"})
eq("assets in the listing are dropped, not submitted",
   b26.parse_changed("M\tdocs/data.json\nM\tdocs/sw.js"), {})
eq("a rename record is read as a change to the new path",
   b26.parse_changed("R100\tdocs/topic/a/index.html\tdocs/topic/b/index.html"),
   {SITE + "topic/b/": "R"})
eq("a delete beats a modify for the same URL, whichever order they arrive in",
   b26.parse_changed("D\tdocs/index.html\nM\tdocs/index.html"), {SITE: "D"})
eq("...and in the other order", b26.parse_changed("M\tdocs/index.html\nD\tdocs/index.html"),
   {SITE: "D"})
eq("blank lines are not paths", b26.parse_changed("\n\nM\tdocs/index.html\n\n"), {SITE: "M"})
eq("the root sorts first, so a dry run is diffable",
   b26.ordered({SITE + "topic/z/": "M", SITE: "M", SITE + "topic/a/": "M"}),
   [SITE, SITE + "topic/a/", SITE + "topic/z/"])

# The fault cases: a URL off-site is a bug here, not a transient, and must stop the run rather than earn
# a 422 for the whole batch.
msg = raises("a URL that is not on this site is refused",
             lambda: b26.check([SITE, "https://elsewhere.example/x"]))
true("...naming the URL and the site", "elsewhere.example" in msg and SITE in msg, msg)
eq("an on-site batch passes check", b26.check([SITE, SITE + "topic/a/"]), None)
raises("a malformed key is a fault, not a warning", lambda: b20.b19.indexnow_key("no"))
raises("...and so is an empty one", lambda: b20.b19.indexnow_key(""))

# `keyLocation` is the field this deployment cannot omit, and it must point at the key file's directory.
body = b26.payload([SITE], "abcdefgh")
eq("the payload names the host bare, with no scheme or path", body["host"], "crazy54.github.io")
eq("keyLocation is the key file under SITE", body["keyLocation"], SITE + "abcdefgh.txt")
true("...which is a directory every submitted URL is under",
     all(u.startswith(body["keyLocation"].rsplit("/", 1)[0] + "/") for u in mapped))


# =====================================================================  2. prune_keys
# `OUT` is a module global read inside `prune_keys`, so redirecting it is the whole of the setup. The real
# `docs/` is never written to by anything below.
KEY = "0123456789abcdef0123456789abcdef"
OLD = "fedcba9876543210fedcba9876543210"
real_out = b20.OUT
keys_dir = TMP / "docs"
keys_dir.mkdir()
b20.OUT = keys_dir
try:
    def write(name: str, text: str) -> Path:
        p = keys_dir / name
        p.write_text(text, encoding="utf-8")
        return p

    # The current key file, as `main` writes it: the key and nothing else, which is what makes content
    # identity a usable test.
    current = write(f"{KEY}.txt", b20.key_text(KEY))
    old = write(f"{OLD}.txt", OLD)
    robots = write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")
    # The file the old name-shape test would have eaten. `security` is eight characters, all of them in
    # `[A-Za-z0-9-]`, so it matched the key pattern exactly.
    security = write("security.txt", "Contact: mailto:security@example.com\nExpires: 2027-01-01T00:00:00Z\n")
    # Same trap, a different length, and a name nobody has thought of yet -- the property is that content
    # decides, so any in-alphabet stem is safe as long as it is not its own content.
    policy = write("ai-policy.txt", "Crawling for training is not permitted.\n")
    # A key-shaped stem whose content is a *different* valid key. Still not a key file: the file format is
    # that the name and the content agree, and a file where they disagree was not written by this stage.
    mismatch = write("aaaaaaaaaaaa.txt", OLD)
    # A trailing newline is tolerated. `key_text` writes none, but autocrlf, an editor or a `git`
    # round-trip can add one, and deleting a rotated key file must not depend on that.
    stray_nl = write("bbbbbbbbbbbb.txt", "bbbbbbbbbbbb\r\n")

    true("the current key file reads as a key file", b20.is_key_file(current))
    true("a rotated key file does too", b20.is_key_file(old))
    true("...even with a trailing newline", b20.is_key_file(stray_nl))
    true("robots.txt does not -- and not because of its length", not b20.is_key_file(robots))
    true("security.txt does not, though its stem matches the key pattern",
         not b20.is_key_file(security))
    true("...and the stem really does match, so the content test is what spares it",
         bool(b20.b19.INDEXNOW_RE.match("security")))
    true("a longer in-alphabet stem does not either", not b20.is_key_file(policy))
    true("a file whose name and content disagree is not a key file", not b20.is_key_file(mismatch))

    keep = {current.resolve(), robots.resolve()}
    gone = b20.prune_keys(keep)

    eq("exactly the rotated key files are removed", sorted(p.name for p in gone),
       sorted([f"{OLD}.txt", "bbbbbbbbbbbb.txt"]))
    true("the rotated key file is gone from disk", not old.exists())
    true("the current key file survives", current.exists())
    eq("...unchanged", current.read_text(encoding="utf-8"), KEY)
    true("robots.txt survives", robots.exists())
    true("docs/security.txt survives", security.exists())
    # Read defensively: when this assertion is the one failing, the file is gone, and a `FileNotFoundError`
    # here would take the tally with it and turn five legible failures into a traceback.
    eq("...byte for byte", security.read_text(encoding="utf-8") if security.exists() else "(deleted)",
       "Contact: mailto:security@example.com\nExpires: 2027-01-01T00:00:00Z\n")
    true("ai-policy.txt survives", policy.exists())
    true("a name/content mismatch survives", mismatch.exists())

    # Idempotent, which is what makes a rerun of the stage safe: the second pass has nothing left to do.
    eq("a second prune removes nothing", b20.prune_keys(keep), [])
    eq("...and the directory still holds everything that survived", sorted(p.name for p in keys_dir.iterdir()),
       sorted(["ai-policy.txt", "aaaaaaaaaaaa.txt", f"{KEY}.txt", "robots.txt", "security.txt"]))

    # `keep` is the authority, and it is the half that makes this safe against a mistake in `is_key_file`:
    # a file this run wrote is never a candidate however its content reads.
    resurrected = write(f"{OLD}.txt", OLD)
    eq("a key file in keep is not deleted, even though it reads as a stale one",
       b20.prune_keys(keep | {resurrected.resolve()}), [])
    true("...so it is still there", resurrected.exists())
    eq("and with an empty keep set even the current key file goes",
       sorted(p.name for p in b20.prune_keys(set())), sorted([f"{KEY}.txt", f"{OLD}.txt"]))

    # A directory whose name ends in `.txt` is matched by the glob and must not be a candidate: it cannot
    # be read as text, and an unlink on it would be an error rather than a prune.
    (keys_dir / "cccccccccccc.txt").mkdir()
    true("a directory named like a key file is not one", not b20.is_key_file(keys_dir / "cccccccccccc.txt"))
    eq("...and is left alone", b20.prune_keys(set()), [])
    true("...still a directory", (keys_dir / "cccccccccccc.txt").is_dir())
finally:
    b20.OUT = real_out

# The committed artefacts, read-only: the real key file must satisfy the test that keeps it alive, and
# the real robots.txt must fail it. If autocrlf or an editor ever put a stray byte in the key file, the
# next weekly run would delete the credential it just wrote, and this is where that shows up.
true("the committed key file would survive its own prune",
     b20.is_key_file(real_out / b20.b19.indexnow_key_file()))
true("the committed robots.txt is not mistaken for a key file",
     not b20.is_key_file(real_out / "robots.txt"))
eq("...and the committed key file contains exactly the key, with nothing round it",
   (real_out / b20.b19.indexnow_key_file()).read_bytes(),
   b20.b19.indexnow_key().encode("ascii"))


# =====================================================================  3. a bad response is a warning
# The hierarchy the fix turns on, asserted rather than assumed. These are the reason `HTTPException` has
# to be in the except tuple: `urllib` does not wrap what `getresponse()` raises, so if any of these
# became an `OSError` upstream the extra clause would be redundant -- and if `RemoteDisconnected` stopped
# being one, the old code's apparent coverage would vanish. Either way this says so.
for cls in (http.client.IncompleteRead, http.client.BadStatusLine, http.client.LineTooLong):
    true(f"{cls.__name__} is an HTTPException", issubclass(cls, http.client.HTTPException))
    true(f"...and is not an OSError, so OSError never caught it", not issubclass(cls, OSError))
    true(f"...nor a URLError", not issubclass(cls, urllib.error.URLError))
true("RemoteDisconnected is an OSError, which is why it was already covered",
     issubclass(http.client.RemoteDisconnected, OSError))
true("HTTPException is not an OSError", not issubclass(http.client.HTTPException, OSError))


class Response:
    """A urlopen context manager. `raise_on_read` is the truncation that arrives mid-body."""

    def __init__(self, status=200, body=b"ok", raise_on_read=None):
        self.status, self._body, self._raise = status, body, raise_on_read

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def read(self, n=None):
        if self._raise:
            raise self._raise
        return self._body


calls = []


@contextlib.contextmanager
def opener(behaviour):
    """Replace `urlopen` for the duration. Restored in a `finally`, so one failing case cannot leave a
    stub installed and make every case after it pass for the wrong reason."""
    real = urllib.request.urlopen

    def fake(req, timeout=None):
        calls.append(getattr(req, "full_url", req))
        if isinstance(behaviour, BaseException):
            raise behaviour
        return behaviour

    urllib.request.urlopen = fake
    try:
        yield
    finally:
        urllib.request.urlopen = real


def posted(behaviour):
    with opener(behaviour):
        return b26.post("https://endpoint.example/indexnow", b26.payload([SITE], "abcdefgh"), 5.0)


# ---- out of getresponse(), which is where urllib re-raises unwrapped
code, line = posted(http.client.IncompleteRead(b"half a bo"))
eq("a truncated response is no response, not a traceback", code, None)
true("...and the log line names the class", "IncompleteRead" in line, line)
code, line = posted(http.client.BadStatusLine("\x00garbage"))
eq("a garbled status line is no response", code, None)
true("...named too", "BadStatusLine" in line, line)
code, line = posted(http.client.LineTooLong("status line"))
eq("an over-long header is no response", code, None)
true("...named too", "LineTooLong" in line, line)
code, line = posted(http.client.HTTPException("something else went wrong"))
eq("any other HTTPException is handled by the same clause", code, None)
true("...named too", "HTTPException" in line, line)

# ---- and out of r.read(), which is inside the `with` rather than around it
code, line = posted(Response(raise_on_read=http.client.IncompleteRead(b"part")))
eq("a body that stops halfway through is no response either", code, None)
true("...named too", "IncompleteRead" in line, line)

# ---- the clauses that already worked must still work: order in the tuple matters, because HTTPError is
# both a URLError and an OSError and has to be caught by its own arm to keep its status code.
code, line = posted(urllib.error.HTTPError("https://endpoint.example/indexnow", 403, "Forbidden",
                                           {}, io.BytesIO(b"key not accepted")))
eq("an HTTPError still reports its status", code, 403)
true("...and its body", "key not accepted" in line, line)
code, line = posted(urllib.error.HTTPError("https://endpoint.example/indexnow", 429, "Slow down",
                                           {}, io.BytesIO(b"")))
eq("an empty error body is reported as empty rather than crashing", (code, line), (429, "(empty body)"))
eq("a URLError is no response", posted(urllib.error.URLError("dns went away"))[0], None)
eq("a TimeoutError is no response", posted(TimeoutError("timed out"))[0], None)
eq("a ConnectionResetError is no response", posted(ConnectionResetError("reset"))[0], None)
eq("RemoteDisconnected is no response", posted(http.client.RemoteDisconnected("closed"))[0], None)
eq("a 200 is reported with its body", posted(Response(200, b"OK")), (200, "OK"))
eq("an empty 200 body is labelled", posted(Response(200, b"   ")), (200, "(empty body)"))


def run_main(behaviour, argv):
    """`main` under a stubbed opener, with stdout captured. Returns (exit code, output)."""
    buf = io.StringIO()
    with opener(behaviour), contextlib.redirect_stdout(buf):
        rc = b26.main(argv)
    return rc, buf.getvalue()


# The contract end to end: a truncated response reaches the process exit code as 0 and reaches a human as
# a workflow warning. This is the assertion the whole module docstring rests on.
rc, out = run_main(http.client.IncompleteRead(b"half"),
                   ["--url", SITE, "--endpoint", "https://endpoint.example/indexnow", "--timeout", "5"])
eq("a truncated response exits 0", rc, 0)
true("...and is surfaced as a workflow warning", "::warning title=IndexNow submission failed::" in out, out)
true("...naming the exception rather than a bare status", "IncompleteRead" in out, out)
true("...and saying the site is published either way", "published either way" in out, out)

rc, out = run_main(urllib.error.HTTPError("https://endpoint.example/indexnow", 403, "Forbidden", {},
                                          io.BytesIO(b"")),
                   ["--url", SITE, "--endpoint", "https://endpoint.example/indexnow"])
eq("a 403 exits 0 too", rc, 0)
true("...with the documented meaning spelled out, not just the number",
     "keyLocation" in out and "403" in out, out)

rc, out = run_main(Response(200, b"OK"), ["--url", SITE, "--endpoint", "https://x.example/i"])
eq("a 200 exits 0", rc, 0)
true("...with no warning", "::warning" not in out, out)

# Nothing to submit is not an error, and it is the common case: `--changed` naming a file that was never
# written is how "nothing was committed" arrives.
before = len(calls)
rc, out = run_main(Response(), ["--changed", str(TMP / "never-written.txt")])
eq("a missing --changed file exits 0", rc, 0)
true("...and says why", "committed nothing" in out, out)
eq("...having posted nothing", len(calls), before)

empty = TMP / "empty.txt"
empty.write_text("", encoding="utf-8")
before = len(calls)
rc, out = run_main(Response(), ["--changed", str(empty)])
eq("an empty --changed file exits 0", rc, 0)
true("...and submits nothing", "Submitting nothing" in out, out)
eq("...so the endpoint was never called", len(calls), before)

# A listing of assets only is the same case arriving the other way: something was committed, but nothing
# a search engine has any use for.
assets = TMP / "assets.txt"
assets.write_text("M\tdocs/data.json\nM\tdocs/sw.js\n", encoding="utf-8")
before = len(calls)
rc, out = run_main(Response(), ["--changed", str(assets)])
eq("a listing of assets only exits 0", rc, 0)
true("...submitting nothing", "Submitting nothing" in out, out)
eq("...and calling nothing", len(calls), before)

# A dry run builds the payload and posts nothing, which is what makes it safe to check a key by hand.
rc, out = run_main(Response(), ["--url", SITE, "--dry-run"])
eq("a dry run exits 0", rc, 0)
true("...printing the payload", '"keyLocation"' in out and '"urlList"' in out, out)
before = len(calls)
run_main(Response(), ["--url", SITE, "--dry-run"])
eq("...and calling nothing", len(calls), before)

# ---- the guard
eq("no test in this file opened a socket", reached, [])
true("...and every request went to the stub, not to api.indexnow.org",
     all(u.startswith("https://endpoint.example/") or u.startswith("https://x.example/") for u in calls),
     str(calls[:4]))
true("...of which there was at least one, so the stub was actually exercised", len(calls) > 10, str(len(calls)))

print(f"\n  url_for maps {len(mapped):,} of {len(docs_files):,} tracked files under docs/, "
      f"against {len(sitemap_urls):,} sitemap URLs")
print(f"  {len(calls)} stubbed request(s), 0 real ones")

print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
