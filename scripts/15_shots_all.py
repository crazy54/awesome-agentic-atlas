"""One image per listed row, for both themes, in four escalating tiers.

1. README image  -- a real screenshot the author chose. Best case.
2. og:image      -- for hosted products, the card the site publishes about itself.
                    One HTTP request instead of a four-second browser render.
3. live capture  -- headless Chromium against the URL, for sites with no card.
4. generated card-- a themed tile with the item's name. Used for items that are a
                    folder inside a repo, and for sites that refuse all of the
                    above. Clearly a label rather than a fake screenshot.

Every image is letterboxed onto the exact same canvas so Excel can anchor it to
one cell without distortion, and so filtered rows collapse cleanly.
"""
import concurrent.futures as cf
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chrome  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
SHOTS = CACHE / "shots"
SHOTS.mkdir(parents=True, exist_ok=True)

BOX = (300, 150)
LIGHT_BG = (252, 252, 251)
DARK_BG = (26, 26, 25)
LIGHT_INK = (11, 11, 11)
DARK_INK = (255, 255, 255)
LIGHT_DIM = (137, 135, 129)
DARK_DIM = (137, 135, 129)

TIMEOUT = 12
MAX_BYTES = 12_000_000
MAX_HTML = 600_000
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
      "Accept": "text/html,image/*,*/*;q=0.8"}

CHROME = chrome.PATH

# Social and chat links never render anything useful headless.
SKIP_HOST = ("discord.gg", "discord.com", "x.com", "twitter.com", "t.me", "linkedin.com",
             "youtube.com", "youtu.be", "reddit.com", "medium.com", "substack.com",
             "arxiv.org", "docs.google.com", "notion.so")

OG = re.compile(r"<meta[^>]+(?:property|name)=[\"'](?:og:image(?::secure_url)?|twitter:image"
                r"(?::src)?)[\"'][^>]*>", re.I)
CONTENT = re.compile(r"content=[\"'](?P<v>[^\"']+)[\"']", re.I)
MD_IMG = re.compile(r"!\[[^\]]*\]\((?P<u>[^)\s]+)")
HTML_IMG = re.compile(r"<img[^>]+src=[\"'](?P<u>[^\"']+)[\"']", re.I)
RASTER = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".bmp")


def fetch(url: str, cap: int = MAX_BYTES) -> bytes | None:
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=TIMEOUT) as r:
            if r.status != 200:
                return None
            data = r.read(cap + 1)
            return data if 0 < len(data) <= cap else None
    except Exception:
        return None


def open_image(data: bytes) -> Image.Image | None:
    try:
        im = Image.open(BytesIO(data))
        im.load()
    except Exception:
        return None
    if getattr(im, "n_frames", 1) > 1:
        try:
            im.seek(0)
        except Exception:
            pass
    return im


def wide_enough(im: Image.Image) -> bool:
    w, h = im.size
    return w >= 300 and h >= 120 and 1.15 <= w / h <= 5.0


def canvas(im: Image.Image, bg, ink) -> Image.Image:
    """Fit onto exactly BOX, letterboxed -- uniform size is what lets Excel
    anchor every picture to one cell without stretching any of them."""
    im = ImageOps.exif_transpose(im)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        flat = Image.new("RGB", im.size, bg)
        flat.paste(im, mask=im.split()[-1])
        im = flat
    else:
        im = im.convert("RGB")
    im.thumbnail(BOX, Image.LANCZOS)
    out = Image.new("RGB", BOX, bg)
    out.paste(im, ((BOX[0] - im.width) // 2, (BOX[1] - im.height) // 2))
    return out


def font(size: int):
    for name in ("segoeuib.ttf", "seguisb.ttf", "arialbd.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def wrap(draw, text: str, f, width: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines[:3]


def title_card(name: str, sub: str, bg, ink, dim) -> Image.Image:
    """A label tile for rows that have no image of their own."""
    im = Image.new("RGB", BOX, bg)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, BOX[0] - 1, BOX[1] - 1], outline=dim)
    d.rectangle([0, 0, 3, BOX[1] - 1], fill=ink)
    fb, fs = font(19), font(12)
    lines = wrap(d, name, fb, BOX[0] - 34)
    y = (BOX[1] - (len(lines) * 24 + (18 if sub else 0))) // 2
    for ln in lines:
        d.text((18, y), ln, font=fb, fill=ink)
        y += 24
    if sub:
        d.text((18, y + 3), sub[:44], font=fs, fill=dim)
    return im


def key_for(rec: dict) -> str:
    if rec["kind"] == "site":
        return "site__" + hashlib.sha1(rec["url"].encode()).hexdigest()[:16]
    base = (rec.get("nwo") or "x").replace("/", "__")
    if rec["kind"] == "subpath":
        return base + "__" + hashlib.sha1(rec["url"].encode()).hexdigest()[:10]
    return base


def save_pair(key: str, im: Image.Image, alpha: bool) -> dict:
    lp = SHOTS / f"{key}__light.jpg"
    canvas(im.copy(), LIGHT_BG, LIGHT_INK).save(lp, "JPEG", quality=84, optimize=True)
    if alpha:
        dp = SHOTS / f"{key}__dark.jpg"
        canvas(im.copy(), DARK_BG, DARK_INK).save(dp, "JPEG", quality=84, optimize=True)
    else:
        dp = lp
    return {"light": lp.name, "dark": dp.name}


def cards_pair(key: str, name: str, sub: str) -> dict:
    lp = SHOTS / f"{key}__light.jpg"
    dp = SHOTS / f"{key}__dark.jpg"
    title_card(name, sub, LIGHT_BG, LIGHT_INK, LIGHT_DIM).save(lp, "JPEG", quality=88, optimize=True)
    title_card(name, sub, DARK_BG, DARK_INK, DARK_DIM).save(dp, "JPEG", quality=88, optimize=True)
    return {"light": lp.name, "dark": dp.name}


def readme_images(nwo: str, branch: str, inner: str) -> list[str]:
    """Images referenced by a folder's own README, absolutised."""
    base = f"https://raw.githubusercontent.com/{nwo}/{branch}/{inner}".rstrip("/")
    data = fetch(f"{base}/README.md", MAX_HTML)
    if not data:
        return []
    md = data.decode("utf-8", "replace")
    urls = []
    for m in list(MD_IMG.finditer(md)) + list(HTML_IMG.finditer(md)):
        u = m.group("u").strip()
        if u.startswith("http"):
            if "shields.io" in u or "badgen.net" in u or "badge" in u.lower():
                continue
            urls.append(u)
        elif not u.startswith(("#", "data:")):
            urls.append(f"{base}/{u.lstrip('./')}")
    return [u for u in urls if u.lower().split("?")[0].endswith(RASTER)][:6]


def og_image(url: str) -> str:
    data = fetch(url, MAX_HTML)
    if not data:
        return ""
    html = data.decode("utf-8", "replace")
    m = OG.search(html)
    if not m:
        return ""
    c = CONTENT.search(m.group(0))
    if not c:
        return ""
    return urllib.parse.urljoin(url, c.group("v").strip())


def browser_shot(url: str) -> bytes | None:
    # None rather than an exception: tier 3 is optional, and tier 4 always produces something. A runner
    # with no browser installed drops to Open Graph cards instead of failing the build.
    if not CHROME:
        return None
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "s.png"
        cmd = [str(CHROME), "--headless", "--disable-gpu", "--hide-scrollbars",
               "--no-sandbox", "--disable-dev-shm-usage", f"--screenshot={out}",
               "--window-size=1280,720", "--virtual-time-budget=6000",
               "--default-background-color=ffffffff", url]
        try:
            subprocess.run(cmd, capture_output=True, timeout=45)
        except Exception:
            return None
        if not out.exists() or out.stat().st_size < 3000:
            return None
        data = out.read_bytes()
    im = open_image(data)
    if im is None:
        return None
    # a page that never painted comes back as one flat colour
    small = im.convert("RGB").resize((32, 18))
    if len({p for p in small.getdata()}) < 6:
        return None
    return data


def tier_image(rec: dict) -> tuple[Image.Image | None, str, str]:
    """(image, source url, tier) for one record, cheapest tier first."""
    # 1. README images the classifier already picked out
    for u in rec.get("shots") or []:
        data = fetch(u)
        im = open_image(data) if data else None
        if im and wide_enough(im):
            return im, u, "readme"

    # 1b. an in-repo item may have a README of its own
    if rec["kind"] == "subpath" and rec.get("nwo"):
        path = rec.get("subpath", "")
        inner = path.split("/", 2)[-1] if path.startswith(("tree/", "blob/")) else path
        if inner and not inner.endswith(".md"):
            for u in readme_images(rec["nwo"], rec.get("branch") or "HEAD", inner):
                data = fetch(u)
                im = open_image(data) if data else None
                if im and wide_enough(im):
                    return im, u, "readme-sub"

    # 2. the repo card GitHub generates, for anything with a repo
    if rec.get("nwo") and rec["kind"] == "repo" and not rec.get("unavailable"):
        data = fetch(f"https://opengraph.githubassets.com/1/{rec['nwo']}")
        im = open_image(data) if data else None
        if im:
            return im, f"opengraph.githubassets.com/1/{rec['nwo']}", "repo-card"

    # 3. what a hosted product publishes about itself, then a live render
    if rec["kind"] == "site":
        host = urllib.parse.urlparse(rec["url"]).netloc.lower()
        if not any(h in host for h in SKIP_HOST):
            u = og_image(rec["url"])
            if u:
                data = fetch(u)
                im = open_image(data) if data else None
                if im and im.width >= 200:
                    return im, u, "og"
            data = browser_shot(rec["url"])
            im = open_image(data) if data else None
            if im:
                return im, rec["url"], "capture"

    # any loose README image beats a generated card
    for u in rec.get("shots") or []:
        data = fetch(u)
        im = open_image(data) if data else None
        if im:
            return im, u, "readme-loose"
    return None, "", "card"


def work(rec: dict) -> dict:
    key = key_for(rec)
    lp, dp = SHOTS / f"{key}__light.jpg", SHOTS / f"{key}__dark.jpg"
    if lp.exists():
        return {"key": key, "light": lp.name, "dark": (dp if dp.exists() else lp).name,
                "tier": "cached", "shot_url": ""}
    im, url, tier = tier_image(rec)
    if im is None:
        sub = rec.get("nwo") or urllib.parse.urlparse(rec["url"]).netloc
        pair = cards_pair(key, rec["name"], sub)
        return {"key": key, **pair, "tier": "card", "shot_url": ""}
    alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
    pair = save_pair(key, im, alpha)
    return {"key": key, **pair, "tier": tier, "shot_url": url}


QUEUE = CACHE / "collect-queue.json"

# The queue is keyed by 10_parse_sources' notion of "the same entry", and matching it here by eye
# would be a second definition of that, free to drift from the one the puller wrote the keys with.
_spec = importlib.util.spec_from_file_location(
    "b10", Path(__file__).resolve().parent / "10_parse_sources.py")
b10 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(b10)


def stale_keys(jobs: dict[str, dict]) -> tuple[set[str], int]:
    """Keys `pull_sources.py` says to collect again, and how many of its entries were already new.

    A key already in `shots_all.json` is never rebuilt, which is right for the case it was written
    for -- a repo's README banner is the same banner it had last Sunday -- and wrong for an entry
    whose listing has since changed. The queue is the only thing that can tell the two apart.

    Only `changed` invalidates. An `added` entry has no key here yet, so it is already in `todo`;
    re-listing it would at best be redundant and at worst re-render an image for a repo that a second
    list merely started mentioning.
    """
    if not QUEUE.exists():
        return set(), 0
    try:
        pending = json.loads(QUEUE.read_text(encoding="utf-8")).get("pending") or {}
    except (json.JSONDecodeError, OSError):
        return set(), 0
    want = {b10.url_key(v["url"]) for v in pending.values()
            if v.get("reason") == "changed"}
    keys = {k for k, r in jobs.items() if b10.url_key(r["url"]) in want}
    return keys, len(pending) - len(want)


def drain_queue(jobs: dict[str, dict], built: dict) -> int:
    """Forget the queued entries whose image is now on disk; keep the ones that errored.

    Written only after the captures, for the reason `watch_sources.py --update` runs last: a queue
    emptied up front would lose every entry in a run that then died halfway.
    """
    if not QUEUE.exists():
        return 0
    try:
        q = json.loads(QUEUE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return 0
    ok = {k for k, v in built.items()
          if v.get("light") and not str(v.get("tier", "")).startswith("error")}
    done = {b10.url_key(r["url"]) for k, r in jobs.items() if k in ok}
    pending = q.get("pending") or {}
    kept = {k: v for k, v in pending.items() if b10.url_key(v["url"]) not in done}
    q["pending"] = kept
    QUEUE.write_text(json.dumps(q, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return len(pending) - len(kept)


def main() -> None:
    recs = json.loads((CACHE / "records_all.json").read_text(encoding="utf-8"))
    only = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else ""
    if only:
        recs = [r for r in recs if r["source"] == only]

    # one job per distinct image key -- 193 pattern docs in one repo share a card
    jobs: dict[str, dict] = {}
    for r in recs:
        jobs.setdefault(key_for(r), r)
    print(f"{len(recs)} rows -> {len(jobs)} distinct images", flush=True)

    out_path = CACHE / "shots_all.json"
    have = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}

    # The daily job publishes only when this marker says a capture ran to completion. `shots_all.json`
    # itself cannot answer that: it is checkpointed every 50 images so a run that dies two thirds of the
    # way through leaves a file that exists, parses, and is missing thousands of cards. Clearing it here
    # and rewriting it at the end is what makes the resumable partial cache safe to keep -- see the save
    # step in weekly.yml, which now uploads `cache/` even when the job fails.
    done_path = CACHE / "shots_all.done.json"
    done_path.unlink(missing_ok=True)

    # Re-collect what the pull stage flagged: drop the record *and* the images, because work()
    # short-circuits on the light JPEG existing and would otherwise report "cached" and change nothing.
    stale, already_new = stale_keys(jobs)
    for k in stale:
        have.pop(k, None)
        for suffix in ("light", "dark"):
            (SHOTS / f"{k}__{suffix}.jpg").unlink(missing_ok=True)
    if stale or already_new:
        print(f"queue: {len(stale)} listings changed, re-collecting; "
              f"{already_new} new entries need no invalidation", flush=True)

    todo = [r for k, r in jobs.items() if k not in have]
    print(f"{len(have)} already done, {len(todo)} to build", flush=True)

    done = 0
    with cf.ThreadPoolExecutor(max_workers=10) as pool:
        futs = {pool.submit(work, r): r for r in todo}
        for fut in cf.as_completed(futs):
            r = futs[fut]
            try:
                res = fut.result()
            except Exception as exc:
                res = {"key": key_for(r), "light": "", "dark": "", "tier": f"error:{exc}"[:60],
                       "shot_url": ""}
            have[res["key"]] = res
            done += 1
            if done % 50 == 0 or done == len(todo):
                out_path.write_text(json.dumps(have, indent=1), encoding="utf-8")
                print(f"  {done}/{len(todo)}", flush=True)

    out_path.write_text(json.dumps(have, indent=1), encoding="utf-8")
    drained = drain_queue(jobs, have)
    tiers: dict[str, int] = {}
    for v in have.values():
        tiers[v["tier"]] = tiers.get(v["tier"], 0) + 1
    print("\nby tier:")
    for t, n in sorted(tiers.items(), key=lambda kv: -kv[1]):
        print(f"  {n:5d}  {t}")
    missing = sum(1 for r in recs if not have.get(key_for(r), {}).get("light"))
    print(f"\nrows with an image: {len(recs) - missing}/{len(recs)}")
    if drained:
        print(f"{drained} entries collected and cleared from {QUEUE.name}")

    # Only a whole-atlas capture earns the marker. Called with a source filter this stage is a repair
    # tool over one list, and the coverage it reports is about that list, not about what a rebuild
    # would publish.
    if not only:
        done_path.write_text(json.dumps({
            "rows": len(recs),
            "with_image": len(recs) - missing,
            "images": len(jobs),
            "captured_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
