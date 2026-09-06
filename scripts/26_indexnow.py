"""Tell IndexNow which URLs this build changed. Bing and Yandex; no account, no verification, no wait.

`docs/sitemap.xml` and `docs/sitemap-repos.xml` list 1,452 URLs between them and, until JFH-206, nothing
had ever told a search engine either file exists. `robots.txt` cannot: its `Sitemap:` directive is only
read when a crawler fetches `robots.txt` for a host it already crawls, and this is a *project* Pages site
under `/awesome-agentic-atlas/`, so the only robots.txt a crawler looks for is `crazy54.github.io/robots.txt`
-- which 404s. That leaves two routes, and they are not alternatives:

  * Search Console and Bing Webmaster Tools take the *whole* sitemap, once, and need a verified property,
    which needs a human with the account. `19_pages.verification()` is the build's half of that.
  * IndexNow takes the *delta*, on every build, and needs nothing but a key you invent yourself. This file.

The second is the one that scales, and it is the one a build can do unattended. A daily run changes one or
two URLs and submits one or two; the weekly run that rewrites all 1,294 detail pages submits those. Nothing
here reasons about what changed -- `daily.yml` and `weekly.yml` stage `docs/` and then hand over the staged
diff, which is the only place in the system that knows the answer exactly.

  python scripts/26_indexnow.py --changed <file>            # a `git diff --name-status` listing
  python scripts/26_indexnow.py --changed <file> --dry-run   # print the payload, post nothing
  python scripts/26_indexnow.py --url <url> --dry-run        # explicit URLs, for checking the payload

THE SUBDIRECTORY RULE, WHICH IS THE ONE THING THAT MAKES OR BREAKS THIS

IndexNow scopes a key to the directory its key file sits in. A key at the host root may submit any URL on
the host; a key in a subdirectory may only submit URLs beneath that subdirectory, and the request has to
carry `keyLocation` saying where the file is. We cannot write to `crazy54.github.io/` -- that host root
belongs to a user Pages site that does not exist -- so `20_landing.py` puts the key file inside
`/awesome-agentic-atlas/` and every payload here names it. Every URL this site publishes is under that
prefix by construction, so the narrower scope costs nothing. It is asserted rather than assumed below:
a URL outside `SITE` would earn a 422 for the whole batch, taking the good URLs down with it.

This is the same trap `20_landing.robots()` documents and the opposite outcome. robots.txt at a project
Pages path is inert and stays inert until a custom domain appears. IndexNow at a project Pages path works,
today, because the protocol has a supported answer for exactly this case.

WHAT A BAD RESPONSE MEANS AND WHAT IT DOES NOT

A non-2xx from the endpoint, or no response at all, is a warning and exit 0. A search engine being down,
rate-limiting, or rejecting a key it has not fetched yet is not a reason to fail a build whose actual job
-- publishing the site -- already succeeded, and this step runs *after* the push for that reason. A 403 or
422 does deserve a human, so both are surfaced as workflow warnings with the documented meaning spelled
out rather than a bare status line.

What does exit non-zero is a fault on this side: a malformed key, or a URL that is not on this site. Those
cannot be fixed by retrying and would submit a credential or a URL that is wrong every run until noticed.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

# No `OUT` and no `ROOT`. This stage reads nothing off disk except the changed-file listing it is handed:
# the URLs come from that listing and the key comes from `19_pages.py`, so there is no path here that
# could disagree with what was published.
HERE = Path(__file__).resolve().parent

# The same dynamic load every stage downstream of `19_pages.py` uses -- the module name is not an
# identifier, so `import` cannot reach it. One thing is wanted from it and it is wanted badly: the key,
# through `indexnow_key()`, so that the value in the payload and the value in the file `20_landing.py`
# published are the same string. A key spelled in two files is a 403 nobody can debug.
spec = importlib.util.spec_from_file_location("b19", HERE / "19_pages.py")
b19 = importlib.util.module_from_spec(spec)
sys.modules["b19"] = b19
spec.loader.exec_module(b19)

SITE = b19.b17.SITE

# The shared endpoint. A POST here is forwarded to every participating engine -- Bing, Yandex, Seznam,
# Naver -- which is one request instead of one per vendor and no list of vendors to keep current.
# `--endpoint` exists so a run can be pointed at `https://www.bing.com/indexnow` alone if the shared host
# is ever the thing that is broken.
ENDPOINT = "https://api.indexnow.org/indexnow"

# The protocol's own ceiling. Reached only by a weekly run, which rewrites 1,294 detail pages plus 156
# facet pages; a daily run submits one or two URLs. Chunked anyway, because the run that will exceed it is
# the run nobody is watching.
BATCH = 10_000

# What the documented status codes mean, so a log line says something a reader can act on. Anything not
# listed is reported as-is.
MEANING = {
    200: "OK -- the URLs were accepted.",
    202: "Accepted -- received, and the key is still being validated. Normal on a first submission.",
    400: "Bad request -- the payload was rejected as malformed. This is a bug here, not a transient.",
    403: "Forbidden -- the key was not accepted. The key file at keyLocation must be reachable and must "
         "contain exactly the key. On a first run this can also mean Pages has not deployed it yet.",
    422: "Unprocessable -- a URL does not belong to the host, or is outside the directory the key file "
         "sits in. Every URL must be under the keyLocation directory.",
    429: "Too many requests -- rate limited. Nothing to fix; the next build will submit again.",
}


# ------------------------------------------------------------------ the changed set
def url_for(path: str) -> str | None:
    """The public URL of one repository path, or None if that path is not a page.

    Only `index.html` files map to a URL, and that is the whole rule. It is not a shortcut: every
    crawlable HTML document this site publishes is a directory index -- the root, 14 topic pages, 130
    crossings, 12 target pages, 1,294 detail pages -- and that set is exactly what the two sitemaps list.
    Everything else `docs/` holds is either an asset (`data.json`, `sw.js`, `pages.css`, `og/*.png`, the
    icons), a feed, or a protocol file (`robots.txt`, the sitemaps, the key file itself). Submitting any of
    those would spend a build's IndexNow budget telling Bing about a stylesheet.

    Deletions are mapped like anything else. IndexNow is a ping for content "added, updated, or deleted",
    and a page whose facet stopped existing is precisely a URL an engine should come back to and find gone.
    """
    p = path.strip().replace("\\", "/")
    if not p.startswith("docs/"):
        return None
    rel = p[len("docs/"):]
    # Spelled as two cases rather than one suffix strip, because `endswith("index.html")` is also true of
    # `notindex.html` and would hand back a URL for a file that is not a directory index.
    if rel == "index.html":
        return SITE
    if rel.endswith("/index.html"):
        return SITE + rel[:-len("index.html")]
    return None


def parse_changed(text: str) -> dict[str, str]:
    """Read a `git diff --name-status` listing into {url: status letter}.

    Tolerant of a bare path list as well, so the file can be produced by `--name-only` or by hand without
    this becoming a second thing to get right. Rename records are not expected -- both workflows pass
    `--no-renames`, which spells a rename as a delete plus an add, and that is the pair IndexNow wants
    anyway -- but an `R100 old new` line is read as a change to the new path rather than dropped.
    """
    status: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        parts = line.split("\t")
        code, path = (parts[0], parts[-1]) if len(parts) > 1 else ("M", parts[0])
        url = url_for(path)
        if url is None:
            continue
        # A path seen twice keeps the stronger claim: a delete is the one status that changes what an
        # engine should do with the URL, so it wins over a modify.
        if status.get(url) != "D":
            status[url] = code[:1]
    return status


def ordered(status: dict[str, str]) -> list[str]:
    """Root first, then sorted -- `20_landing.sitemap()`'s order, which makes a dry run diffable."""
    return sorted(status, key=lambda u: (u != SITE, u))


# ------------------------------------------------------------------ the payload
def payload(urls: list[str], key: str) -> dict:
    """One IndexNow request body.

    `host` is the bare hostname with no scheme and no path -- the protocol's own field, and not where the
    subdirectory scope is expressed. That is `keyLocation`'s job, and it is the field this deployment
    cannot omit.
    """
    return {
        "host": urlsplit(SITE).netloc,
        "key": key,
        "keyLocation": SITE + b19.indexnow_key_file(key),
        "urlList": urls,
    }


def check(urls: list[str]) -> None:
    """Refuse to submit a URL that is not on this site. See the module docstring: one stray URL is a 422
    for the whole batch, so this is the difference between "one page was wrong" and "nothing was
    submitted and the log says 422"."""
    stray = [u for u in urls if not u.startswith(SITE)]
    if stray:
        raise SystemExit(
            f"{len(stray)} URL(s) are not under {SITE} and would be rejected for the whole batch: "
            + ", ".join(stray[:5]))


def post(endpoint: str, body: dict, timeout: float) -> tuple[int | None, str]:
    """POST one body. Returns (status or None if nothing answered, a line for the log)."""
    data = json.dumps(body, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(
        endpoint, data=data, method="POST",
        headers={"Content-Type": "application/json; charset=utf-8",
                 "User-Agent": f"awesome-agentic-atlas/26_indexnow (+{SITE})"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, (r.read(2048).decode("utf-8", "replace").strip() or "(empty body)")
    except urllib.error.HTTPError as e:
        return e.code, (e.read(2048).decode("utf-8", "replace").strip() or "(empty body)")
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return None, f"{type(e).__name__}: {e}"


# ------------------------------------------------------------------ entry point
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Submit this build's changed URLs to IndexNow.")
    ap.add_argument("--changed", type=Path,
                    help="file of `git diff --name-status` lines (or bare paths). "
                         "A missing or empty file means nothing changed, which is not an error.")
    ap.add_argument("--url", action="append", default=[],
                    help="submit this URL explicitly. Repeatable. Combines with --changed.")
    ap.add_argument("--dry-run", action="store_true", help="print the payload and post nothing.")
    ap.add_argument("--endpoint", default=ENDPOINT)
    ap.add_argument("--timeout", type=float, default=30.0)
    args = ap.parse_args(argv)

    # Before anything else, and unconditionally: a malformed key is a fault here, and finding it out from
    # a 403 after the payload was built is finding it out from the wrong place.
    key = b19.indexnow_key()

    status: dict[str, str] = {}
    if args.changed:
        if args.changed.exists():
            status.update(parse_changed(args.changed.read_text(encoding="utf-8")))
        else:
            # Not an error, and the workflows depend on it: the step that stages `docs/` writes this file
            # only when it has something to commit, so "absent" is how "nothing was committed" arrives.
            print(f"{args.changed} does not exist, so this build committed nothing under docs/.")
    for u in args.url:
        status.setdefault(u, "M")
    urls = ordered(status)

    if not urls:
        # The no-change case, and it is the common one: `daily.yml` only reaches this step when the gate
        # opened *and* something was committed, but a commit can touch `state/` and `data.json` alone.
        print("No changed URL in this build. Submitting nothing.")
        return 0

    check(urls)
    counts = {c: sum(1 for v in status.values() if v == c) for c in sorted(set(status.values()))}
    print(f"{len(urls)} changed URL(s) · "
          + " ".join(f"{c}={n}" for c, n in counts.items())
          + f" · key file {SITE}{b19.indexnow_key_file(key)}")

    batches = [urls[i:i + BATCH] for i in range(0, len(urls), BATCH)]
    if args.dry_run:
        for n, chunk in enumerate(batches, 1):
            print(f"--- payload {n}/{len(batches)} -> {args.endpoint}")
            print(json.dumps(payload(chunk, key), indent=2))
        return 0

    for n, chunk in enumerate(batches, 1):
        code, body = post(args.endpoint, payload(chunk, key), args.timeout)
        label = f"batch {n}/{len(batches)}, {len(chunk)} URL(s)"
        if code is not None and 200 <= code < 300:
            print(f"{label}: {code} · {MEANING.get(code, body)}")
            continue
        # Not a build failure. See the module docstring: the site is already published, and a search
        # engine's availability is not this pipeline's to guarantee. Surfaced, though -- a 403 that nobody
        # ever reads is the same as not having submitted at all, which is the state this ticket found.
        detail = MEANING.get(code, body) if code is not None else body
        print(f"{label}: {code if code is not None else 'no response'} · {detail}")
        print(f"::warning title=IndexNow submission failed::{label} was not accepted "
              f"({code if code is not None else 'no response'}): {detail} "
              f"The site is published either way; the URLs will be resubmitted by the next build that "
              f"changes them, and Search Console still has the full sitemap.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
