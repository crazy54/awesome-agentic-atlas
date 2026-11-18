"""GitLab's public API, paced, retried and cached: the one door every GitLab read in the pipeline goes through.

GitHub reads go through `gh`, which brings its own token and its own idea of a rate limit. GitLab has no
equivalent on the runner, and nothing here needs one: everything the atlas shows about a public GitLab
project is readable anonymously (see handbook/gitlab.md for the field-by-field survey). So this is
a small client over `urllib`, with three jobs.

* **Pacing.** GitLab.com's documented anonymous limits are per IP: 500 requests a minute for the API
  as a whole, and 400 every ten minutes for the projects list (`GET /api/v4/projects`). Requests are
  spaced `MIN_GAP` apart, the list endpoint by its own longer `LIST_GAP`, and the `RateLimit-Remaining`
  / `RateLimit-Reset` headers GitLab sends on every answer decide any longer wait. A short 429 is
  waited out (`Retry-After` first); a 5xx or a dropped connection is retried with a backoff; a 4xx that
  is not a rate limit is the query's fault and is never retried.

  The limit that actually binds is a third one. Measured on 2026-11-18, about fifty anonymous requests
  into the first scan, every endpoint started answering 429 under `ratelimit-name:
  unauthenticated_traffic_per_ip` with a `Retry-After` reaching to the top of the hour -- the "60 each
  hour" GitLab's rate-limit page lists for anonymous traffic. A wait that long is not waited: it raises
  at once (see `request`), so a capped run fails in seconds and its caller keeps what it had. On a CI
  runner the cap is shared with every other job on the same egress IP, so anonymous is a fallback,
  not a plan; that is why the token below matters more than its description suggests.

* **A token if there is one.** `GITLAB_TOKEN` in the environment is sent as `PRIVATE-TOKEN` and lifts
  the limits to the authenticated ones (2,000 a minute; projects list 2,000 per ten minutes). It also
  reveals fields an anonymous read cannot see -- `mirror`, `import_url`, `forked_from_project` on REST --
  but nothing in the pipeline depends on those: GraphQL's `isForked` and `importStatus` are anonymous,
  and the mirror rule is built from what everyone can read. So every stage *works* without it -- it
  just cannot do much in an hour -- and adding it is the owner's decision (it would be a repo secret, a
  `read_api` personal access token from any free GitLab account).

* **A response cache** under `cache/gitlab/http/`, one file per request, keyed by a hash of the method,
  URL and body, for local tuning only: used, read and written, only when `ttl` is above zero, and then
  read back only when younger than `ttl` seconds. A person tuning the rules passes a day and re-runs the
  scan for free -- which, at sixty requests an hour, is the only way a full anonymous sweep finishes at
  all. A build passes nothing: `cache/` is the Actions cache too, and a few hundred response files a day
  that nothing reads would only grow it. `cache/` is gitignored, so nothing here is ever committed.

Errors are `GitLabError`. A caller decides what a failed read means; for the intake stage it means "change
nothing", exactly as a failed search does for the GitHub scout.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache" / "gitlab" / "http"

HOST = "gitlab.com"
API = f"https://{HOST}/api/v4"
GRAPHQL = f"https://{HOST}/api/graphql"
USER_AGENT = "awesome-agentic-atlas (+https://aaa.jeremyfhall.com)"

MIN_GAP = 0.25            # seconds between any two requests: 240/minute, under half the 500/minute IP limit
LIST_GAP = 1.6            # between two projects-list requests: 375 per ten minutes against a limit of 400
RETRIES = 4
MAX_WAIT = 120            # the longest single rate-limit wait honoured before giving up
TIMEOUT = 60


class GitLabError(RuntimeError):
    """A read that cannot be trusted. Whatever the caller was building from it should stay as it was."""


def http(method: str, url: str, body: bytes | None, headers: dict) -> tuple[int, dict, bytes]:
    """One request, as (status, lower-cased headers, body). An HTTP error is an answer, not an
    exception: the status decides whether it is retried. Only a transport failure raises."""
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status, {k.lower(): v for k, v in r.headers.items()}, r.read()
    except urllib.error.HTTPError as e:
        return e.code, {k.lower(): v for k, v in (e.headers or {}).items()}, e.read() or b""
    except (urllib.error.URLError, OSError, TimeoutError) as e:
        raise GitLabError(f"no answer from {urllib.parse.urlsplit(url).netloc}: "
                          f"{type(e).__name__} {e}") from None


class Client:
    """Paced, retried, cached reads. Every collaborator is injectable so the tests need no network."""

    def __init__(self, transport=http, sleep=time.sleep, clock=time.time, ttl: float = 0,
                 cache: Path | None = CACHE, token: str | None = None, log=print):
        self.transport, self.sleep, self.clock, self.log = transport, sleep, clock, log
        self.ttl, self.cache = ttl, cache
        self.token = os.environ.get("GITLAB_TOKEN") if token is None else token
        self.requests = 0          # sent over the network
        self.cached = 0            # answered from the cache
        self.last = None
        self.last_list = None
        self.remaining = None
        self.reset = 0.0

    # --- cache ------------------------------------------------------------------------------------
    def _key(self, method: str, url: str, body: bytes | None) -> Path | None:
        if self.cache is None:
            return None
        h = hashlib.sha256(f"{method} {url}\n".encode() + (body or b"")).hexdigest()
        return self.cache / h[:2] / f"{h}.json"

    def _cached(self, path: Path | None):
        if path is None or self.ttl <= 0 or not path.exists():
            return None
        if self.clock() - path.stat().st_mtime > self.ttl:
            return None
        try:
            hit = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        self.cached += 1
        return hit["headers"], hit["data"]

    def _store(self, path: Path | None, url: str, headers: dict, data) -> None:
        if path is None or self.ttl <= 0:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        keep = {k: v for k, v in headers.items() if k.startswith(("x-", "link"))}
        path.write_text(json.dumps({"url": url, "headers": keep, "data": data}, ensure_ascii=False),
                        encoding="utf-8")

    # --- pacing -----------------------------------------------------------------------------------
    def _pace(self, listing: bool) -> None:
        now = self.clock()
        if self.remaining is not None and self.remaining <= 2:
            # The window is all but spent: wait for its reset, then forget it, so the next answer's
            # headers say what the new window holds rather than this wait repeating for ever.
            self.sleep(min(max(self.reset - now, 0) + 1, MAX_WAIT))
            self.remaining = None
            now = self.clock()
        gaps = [(self.last, MIN_GAP)] + ([(self.last_list, LIST_GAP)] if listing else [])
        wait = max((g - (now - t) for t, g in gaps if t is not None), default=0)
        if wait > 0:
            self.sleep(wait)

    # --- one read ---------------------------------------------------------------------------------
    def request(self, method: str, url: str, payload: dict | None = None) -> tuple[dict, object]:
        """(headers, decoded JSON) for one read, from the cache when it is fresh enough."""
        body = json.dumps(payload).encode() if payload is not None else None
        key = self._key(method, url, body)
        hit = self._cached(key)
        if hit is not None:
            return hit
        listing = urllib.parse.urlsplit(url).path.rstrip("/").endswith("/api/v4/projects")
        headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
        if body is not None:
            headers["Content-Type"] = "application/json"
        if self.token:
            headers["PRIVATE-TOKEN"] = self.token
        why = "no attempt made"
        for attempt in range(RETRIES):
            self._pace(listing)
            self.last = self.clock()
            if listing:
                self.last_list = self.last
            self.requests += 1
            try:
                status, h, raw = self.transport(method, url, body, headers)
            except GitLabError as exc:
                why = str(exc)
                self.sleep(5 * (attempt + 1))
                continue
            if "ratelimit-remaining" in h:
                try:
                    self.remaining = int(h["ratelimit-remaining"])
                    self.reset = float(h.get("ratelimit-reset") or 0)
                except ValueError:
                    self.remaining = None
            if status == 200:
                try:
                    data = json.loads(raw.decode("utf-8")) if raw else None
                except (UnicodeDecodeError, json.JSONDecodeError):
                    why = "an unreadable 200"
                    self.sleep(5 * (attempt + 1))
                    continue
                self._store(key, url, h, data)
                return h, data
            if status == 429 or (status == 403 and h.get("ratelimit-remaining") == "0"):
                why = f"HTTP {status} rate limited"
                after = h.get("retry-after")
                wait = float(after) if after and after.isdigit() else max(self.reset - self.clock(), 0) + 1
                if wait > MAX_WAIT:
                    # The hourly anonymous cap (`unauthenticated_traffic_per_ip`) answers with a
                    # Retry-After of up to an hour. Sleeping through that would hold the daily job for
                    # an hour to learn nothing new, so it is a failed read, said plainly, now.
                    raise GitLabError(f"rate limited by {h.get('ratelimit-name') or 'GitLab'} for "
                                      f"{wait / 60:.0f} more minutes; {self.requests} requests sent "
                                      f"this run" + ("" if self.token else
                                                     " (anonymous: set GITLAB_TOKEN to lift the cap)"))
                self.log(f"  rate limited; waiting {min(max(wait, 1), MAX_WAIT):.0f}s")
                self.sleep(min(max(wait, 1), MAX_WAIT))
                self.remaining = None
                continue
            if status >= 500:
                why = f"HTTP {status}"
                self.sleep(5 * (attempt + 1))
                continue
            raise GitLabError(f"HTTP {status} for {url}: {raw[:160].decode('utf-8', 'replace')}")
        raise GitLabError(f"{url}: {why} after {RETRIES} attempts")

    def get(self, path: str, **params) -> tuple[dict, object]:
        q = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None}, doseq=True)
        return self.request("GET", f"{API}{path}" + (f"?{q}" if q else ""))

    def graphql(self, query: str, variables: dict | None = None) -> dict:
        _, data = self.request("POST", GRAPHQL, {"query": query, "variables": variables or {}})
        if not isinstance(data, dict):
            raise GitLabError("GraphQL answered with no object")
        if data.get("errors") and not data.get("data"):
            raise GitLabError(f"GraphQL: {str(data['errors'])[:200]}")
        return data.get("data") or {}

    def pages(self, path: str, until=None, max_pages: int = 20, **params) -> list[dict]:
        """Every item of a paginated list, following `X-Next-Page`. `until(item)` stops early once an
        item satisfies it -- the star floor, on a list ordered by stars, so a topic with 5,000 projects
        costs one page when only the first 40 clear the bar."""
        out: list[dict] = []
        page = 1
        for _ in range(max_pages):
            h, data = self.get(path, page=page, per_page=100, **params)
            batch = data if isinstance(data, list) else []
            for it in batch:
                if until and until(it):
                    return out
                out.append(it)
            nxt = str(h.get("x-next-page") or "").strip()
            if not batch or not nxt.isdigit():
                return out
            page = int(nxt)
        return out


# --- the README as a description ------------------------------------------------------------------
_MD_NOISE = re.compile(r"!\[[^\]]*\]\([^)]*\)|<[^>]+>|\[!\[.*?\]\(.*?\)\]\(.*?\)")
_MD_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")


def readme_summary(text: str, limit: int = 300) -> str:
    """The first line of prose in a README, as plain text, or "".

    GitLab projects leave the description empty far more often than GitHub repos do -- `gitlab-org/ai/
    lazy-mcp` and a dozen other agentic projects with stars had none on 2026-11-18 -- and say what they
    are in the README instead. Both GitLab stages use this for a project with no description: the scout
    to judge it (the off-topic and spam rules read the description), and the fetch to give the row the
    blurb a GitHub repo's description would have. Headings, badges, images, HTML, tables, code fences
    and link-only lines are skipped; the first remaining paragraph line wins.
    """
    fenced = False
    for raw in (text or "").splitlines():
        line = raw.strip()
        if line.startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced or not line or line.startswith(("#", "|", ">", "---", "===", "[!", "<!--")):
            continue
        plain = _MD_LINK.sub(r"\1", _MD_NOISE.sub("", line)).replace("**", "").replace("`", "").strip(" *-_=")
        if len(plain) < 12 or not any(c.isalpha() for c in plain):
            continue
        return plain if len(plain) <= limit else plain[: limit - 1].rsplit(" ", 1)[0] + "…"
    return ""

