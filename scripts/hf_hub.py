"""A polite, cached reader for the Hugging Face Hub's public API, and a GGUF header parser.

`40_models.py` builds the models index out of about twelve thousand Hub answers: listing pages, one file tree per
repo, one `config.json` per model, and now and then the first two megabytes of a GGUF. Everything here is
about asking for each of those as few times as possible and never fast enough to be told off.

THE BUDGET. Anonymous reads are allowed, and limited in two buckets that every answer reports in a
`RateLimit` header (seen 2026-11-18):

    RateLimit: "api";r=497;t=288          RateLimit-Policy: "fixed window";"api";q=500;w=300
    RateLimit: "resolvers";r=2999;t=279   RateLimit-Policy: "fixed window";"resolvers";q=3000;w=300

`api` is `/api/...` -- listings and trees -- at 500 calls per five-minute window; `resolvers` is
`/{repo}/resolve/...` -- raw files such as `config.json` -- at 3,000. The client reads `r` (calls left) and
`t` (seconds until the window resets) off every answer and, once `r` falls to RESERVE, sleeps until the
window turns over. So it does not discover the limit by hitting it; a 429 is still handled (Retry-After,
else the window) because another process on the same IP shares the bucket. A token (HF_TOKEN) raises the
`api` quota for a signed-in account and lets the fetch read `config.json` from gated repos whose gate that
account has accepted. Nothing here needs one, and none is read unless the variable is set.

THE CACHE. Every answer is written under `cache/hf/` (gitignored, restored from the Actions cache on CI)
as `{"fetched": ISO, "key": KEY, "status": 200, "body": ...}`. A cached answer is reused when
  - its `key` matches what the caller says it should be -- a repo's `sha` for anything read off that
    repo, so a tree or a config is re-read exactly when the repo moved and never otherwise; or
  - for keyless reads (listings), it is younger than `max_age`.
Negative answers (401 gated, 404 gone) are cached the same way, so a gated `config.json` is asked about
once per repo commit, not once per run. `offline=True` serves only the cache and raises on a miss, which is
how the tests and `--offline` run without a network.

Standard library only, like most of the pipeline.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import struct
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HUB = "https://huggingface.co"
UA = "awesome-agentic-atlas-models/1 (+https://aaa.jeremyfhall.com; weekly index of local models)"
RESERVE = 25          # calls left in a window at which the client stops and waits for the next one
MIN_GAP = 0.12        # seconds between any two requests, whatever the bucket says: never a burst
TIMEOUT = 60
RETRIES = 5


class Offline(Exception):
    """A cache miss while offline. The caller asked for something nobody has fetched."""


class HubError(Exception):
    """An answer that is not about the repo: a 5xx that outlasted the retries, a network failure. The
    stage stops on it rather than publish an index with holes it cannot see."""


def utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _parse_ratelimit(value: str | None) -> tuple[str, int, int] | None:
    """`"api";r=497;t=288` -> ("api", 497, 288). None for a header that is absent or not that shape."""
    if not value:
        return None
    m = re.match(r'\s*"?([a-z_-]+)"?\s*;\s*r=(\d+)\s*;\s*t=(\d+)', value)
    return (m.group(1), int(m.group(2)), int(m.group(3))) if m else None


def next_link(value: str | None) -> str | None:
    """The `rel="next"` URL from a Link header, which is how the listing API pages."""
    if not value:
        return None
    for part in value.split(","):
        m = re.match(r'\s*<([^>]+)>\s*;\s*rel="?next"?', part)
        if m:
            return m.group(1)
    return None


class Hub:
    def __init__(self, cache: Path, token: str | None = None, offline: bool = False, log=print):
        self.cache = Path(cache)
        self.token = token if token is not None else (os.environ.get("HF_TOKEN") or None)
        self.offline = offline
        self.log = log
        self.calls = {"api": 0, "resolvers": 0, "other": 0, "cached": 0}
        self._last = 0.0
        self._left: dict[str, tuple[int, float]] = {}   # bucket -> (calls left, monotonic time it resets)

    # -------------------------------------------------------------- the cache
    def _path(self, kind: str, name: str) -> Path:
        safe = re.sub(r"[^A-Za-z0-9._-]+", "~", name)
        if len(safe) > 120:   # Windows paths; the hash keeps it unique
            safe = safe[:100] + "~" + hashlib.sha1(name.encode()).hexdigest()[:12]
        return self.cache / kind / f"{safe}.json"

    def cached(self, kind: str, name: str) -> dict | None:
        p = self._path(kind, name)
        if not p.exists():
            return None
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except ValueError:
            return None   # a torn write from an interrupted run: refetch it

    def store(self, kind: str, name: str, status: int, body, key: str | None = None) -> dict:
        rec = {"fetched": utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), "key": key, "status": status, "body": body}
        p = self._path(kind, name)
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(".tmp")
        tmp.write_text(json.dumps(rec, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        tmp.replace(p)
        return rec

    @staticmethod
    def fresh(rec: dict | None, key: str | None, max_age: float | None) -> bool:
        if not rec:
            return False
        if key is not None:
            return rec.get("key") == key
        if max_age is None:
            return True
        try:
            when = dt.datetime.strptime(rec["fetched"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
        except (KeyError, ValueError):
            return False
        return (utcnow() - when).total_seconds() < max_age

    # -------------------------------------------------------------- the wire
    def _wait(self, bucket: str) -> None:
        gap = time.monotonic() - self._last
        if gap < MIN_GAP:
            time.sleep(MIN_GAP - gap)
        left = self._left.get(bucket)
        if left and left[0] <= RESERVE:
            pause = left[1] - time.monotonic()
            if pause > 0:
                self.log(f"  hub: {left[0]} {bucket} calls left in this window; waiting {pause:.0f}s for the next")
                time.sleep(pause + 1)
            self._left.pop(bucket, None)

    def request(self, url: str, headers: dict | None = None, bucket: str = "api"):
        """(status, headers, body bytes). Retries 429 and 5xx; returns 4xx other than 429 to the caller,
        because 401/403/404 are statements about the repo. Raises HubError when retries run out."""
        if self.offline:
            raise Offline(url)
        hdrs = {"User-Agent": UA, "Accept": "application/json"}
        if self.token and url.startswith(HUB):
            hdrs["Authorization"] = f"Bearer {self.token}"
        hdrs.update(headers or {})
        delay = 5.0
        for attempt in range(RETRIES):
            self._wait(bucket)
            self._last = time.monotonic()
            self.calls[bucket if bucket in self.calls else "other"] += 1
            req = urllib.request.Request(url, headers=hdrs)
            try:
                with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                    status, rh, body = r.status, r.headers, r.read()
            except urllib.error.HTTPError as e:
                status, rh, body = e.code, e.headers, e.read() if e.fp else b""
            except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
                if attempt == RETRIES - 1:
                    raise HubError(f"{url}: {e}") from e
                self.log(f"  hub: {type(e).__name__} on {url[:90]}; retrying in {delay:.0f}s")
                time.sleep(delay)
                delay *= 2
                continue
            rl = _parse_ratelimit(rh.get("RateLimit") if rh else None)
            if rl:
                self._left[rl[0]] = (rl[1], time.monotonic() + rl[2])
            if status == 429:
                wait = rh.get("Retry-After") if rh else None
                pause = float(wait) if wait and wait.isdigit() else (rl[2] + 1 if rl else 60)
                self.log(f"  hub: 429 on {url[:90]}; waiting {pause:.0f}s")
                time.sleep(pause)
                continue
            if status >= 500:
                if attempt == RETRIES - 1:
                    raise HubError(f"{url}: HTTP {status}")
                self.log(f"  hub: HTTP {status} on {url[:90]}; retrying in {delay:.0f}s")
                time.sleep(delay)
                delay *= 2
                continue
            return status, rh, body
        raise HubError(f"{url}: still rate-limited after {RETRIES} tries")

    # -------------------------------------------------------------- what the stage asks for
    def get(self, kind: str, name: str, url: str, key: str | None = None, max_age: float | None = None,
            bucket: str = "api", parse: str = "json", headers: dict | None = None):
        """One cached GET. Returns (status, body) where body is parsed JSON (or text) for a 200 and None
        otherwise."""
        rec = self.cached(kind, name)
        if self.fresh(rec, key, max_age):
            self.calls["cached"] += 1
            return rec["status"], rec["body"]
        if self.offline:
            if rec:   # stale is better than nothing offline, and says so in the count
                self.calls["cached"] += 1
                return rec["status"], rec["body"]
            raise Offline(f"{kind}/{name}")
        status, _, raw = self.request(url, headers=headers, bucket=bucket)
        body = None
        if status == 200:
            text = raw.decode("utf-8", "replace")
            if parse == "json":
                try:
                    body = json.loads(text)
                except ValueError:
                    status, body = 0, None   # an HTML error page with a 200; cache as unusable
            else:
                body = text
        self.store(kind, name, status, body, key)
        return status, body

    def list_models(self, name: str, params: list[tuple[str, str]], pages: int = 1,
                    max_age: float = 20 * 3600, reduce=None) -> list[dict]:
        """A listing: `/api/models?...`, up to `pages` pages of 1,000. The whole result is cached as one
        record under `name`, after `reduce` has cut each entry down to what the stage keeps -- a raw page
        with `expand[]=config` carries every chat template on the Hub and is tens of megabytes."""
        rec = self.cached("list", name)
        if self.fresh(rec, None, max_age) or (self.offline and rec):
            self.calls["cached"] += 1
            return rec["body"]
        if self.offline:
            raise Offline(f"list/{name}")
        url = f"{HUB}/api/models?" + urllib.parse.urlencode(params)
        out: list[dict] = []
        for _ in range(pages):
            status, rh, raw = self.request(url)
            if status != 200:
                raise HubError(f"listing {name}: HTTP {status}: {raw[:200]!r}")
            batch = json.loads(raw.decode("utf-8"))
            out.extend(reduce(x) for x in batch) if reduce else out.extend(batch)
            url = next_link(rh.get("Link"))
            if not url or not batch:
                break
        self.store("list", name, 200, out)
        return out

    def tree(self, repo: str, sha: str | None) -> list[tuple[str, int]] | None:
        """[(path, bytes)] for every file in the repo at any depth, or None if the Hub will not list it.
        Cached under the repo's sha, so it is re-read when, and only when, the repo moved. Sizes are the
        LFS sizes, which for weights are the bytes a download is. The tree pages at 1,000 entries."""
        rec = self.cached("tree", repo)
        if self.fresh(rec, sha, None) or (self.offline and rec):
            self.calls["cached"] += 1
            return [tuple(x) for x in rec["body"]] if rec["body"] is not None else None
        if self.offline:
            raise Offline(f"tree/{repo}")
        url = f"{HUB}/api/models/{repo}/tree/main?recursive=true"
        out: list[tuple[str, int]] = []
        while url:
            status, rh, raw = self.request(url)
            if status != 200:
                self.store("tree", repo, status, None, sha)
                return None
            for x in json.loads(raw.decode("utf-8")):
                if x.get("type") == "file":
                    out.append((x["path"], int((x.get("lfs") or {}).get("size") or x.get("size") or 0)))
            url = next_link(rh.get("Link"))
        self.store("tree", repo, 200, out, sha)
        return out

    def head_bytes(self, repo: str, path: str, n: int, key: str) -> bytes | None:
        """The first `n` bytes of a file, by Range request on the resolver, cached as hex under the repo's
        sha. Used for GGUF headers, so `n` is a couple of megabytes at most and never a model."""
        name = f"{repo}/{path}:{n}"
        rec = self.cached("head", name)
        if self.fresh(rec, key, None) or (self.offline and rec):
            self.calls["cached"] += 1
            return bytes.fromhex(rec["body"]) if rec["body"] else None
        if self.offline:
            raise Offline(f"head/{name}")
        url = f"{HUB}/{repo}/resolve/main/{urllib.parse.quote(path)}"
        status, _, raw = self.request(url, headers={"Range": f"bytes=0-{n - 1}", "Accept": "*/*"},
                                      bucket="resolvers")
        ok = status in (200, 206)
        self.store("head", name, status, raw[:n].hex() if ok else None, key)
        return raw[:n] if ok else None


# ------------------------------------------------------------------ GGUF
# The header layout is llama.cpp's (gguf.md): magic "GGUF", u32 version (2 or 3), u64 tensor count, u64
# key/value count, then the key/values. Each is a u64-length string key, a u32 type and a value. Only the
# scalars are kept; arrays are walked past (the tokenizer's vocabulary is most of a header) and their
# length recorded. A truncated buffer is not an error: the architecture keys come first in every converter
# seen, so the keys read before the cut are returned and the rest are simply missing.
_SCALAR = {0: "<B", 1: "<b", 2: "<H", 3: "<h", 4: "<I", 5: "<i", 6: "<f", 7: "<?", 10: "<Q", 11: "<q", 12: "<d"}


class _Short(Exception):
    pass


def parse_gguf_header(buf: bytes) -> dict:
    """{key: value} for every scalar and string key/value in `buf`, plus `"__arrays__": {key: length}`.
    Raises ValueError if `buf` is not a GGUF at all."""
    if len(buf) < 24 or buf[:4] != b"GGUF":
        raise ValueError("not a GGUF file")
    version = struct.unpack_from("<I", buf, 4)[0]
    if version not in (2, 3):
        raise ValueError(f"GGUF version {version} is not one this parser knows")
    n_kv = struct.unpack_from("<Q", buf, 16)[0]
    pos = 24
    out: dict = {"__version__": version, "__arrays__": {}}

    def take(fmt: str):
        nonlocal pos
        size = struct.calcsize(fmt)
        if pos + size > len(buf):
            raise _Short
        v = struct.unpack_from(fmt, buf, pos)[0]
        pos += size
        return v

    def string() -> str:
        nonlocal pos
        n = take("<Q")
        if pos + n > len(buf):
            raise _Short
        s = buf[pos:pos + n].decode("utf-8", "replace")
        pos += n
        return s

    def value(t: int):
        if t in _SCALAR:
            return take(_SCALAR[t])
        if t == 8:
            return string()
        raise ValueError(f"GGUF value type {t} is not one this parser knows")

    try:
        for _ in range(n_kv):
            key = string()
            t = take("<I")
            if t == 9:
                et, n = take("<I"), take("<Q")
                out["__arrays__"][key] = n
                if et == 8:
                    for _ in range(n):
                        string()
                elif et in _SCALAR:
                    skip = struct.calcsize(_SCALAR[et]) * n
                    if pos + skip > len(buf):
                        raise _Short
                    pos += skip
                else:
                    raise ValueError(f"GGUF array of type {et} is not one this parser knows")
            else:
                out[key] = value(t)
    except _Short:
        out["__truncated__"] = True
    return out


if __name__ == "__main__":
    # `python scripts/hf_hub.py FILE.gguf` prints a local GGUF's scalar header keys: handy for checking
    # what a converter wrote without loading the model.
    if len(sys.argv) == 2:
        with open(sys.argv[1], "rb") as f:
            hdr = parse_gguf_header(f.read(4 << 20))
        for k, v in hdr.items():
            print(k, "=", v)
