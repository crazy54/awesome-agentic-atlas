"""Download and thumbnail one representative screenshot per repo.

Candidates come from the README in preference order. We reject logos/icons by
shape and size, take the first frame of animated GIFs, and flatten transparency
onto each theme's background so a transparent PNG doesn't glow white on the
dark sheet.
"""
import json
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
SHOTS = CACHE / "shots"
# Same reason as 02_fetch.py's: on a cold cache this is the first stage to write into cache/shots,
# PIL's `save` will not make the parent, and 15_shots_all.py's identical mkdir runs two stages later.
SHOTS.mkdir(parents=True, exist_ok=True)

BOX = (300, 150)          # thumbnail bounding box in px
MAX_BYTES = 14_000_000
TIMEOUT = 25
WORKERS = 8

LIGHT_BG = (255, 255, 255)
DARK_BG = (24, 27, 36)

UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/png,image/*,*/*;q=0.8",
}


def fetch(url: str) -> bytes | None:
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            if r.status != 200:
                return None
            data = r.read(MAX_BYTES + 1)
            return data if 0 < len(data) <= MAX_BYTES else None
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError, ValueError):
        return None


def looks_like_screenshot(im: Image.Image) -> bool:
    w, h = im.size
    if w < 300 or h < 120:
        return False           # icons, inline logos, tiny diagrams
    ratio = w / h
    return 1.15 <= ratio <= 5.0  # screenshots and terminal captures are wide


def thumb(im: Image.Image, bg: tuple[int, int, int]) -> Image.Image:
    im = ImageOps.exif_transpose(im)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        flat = Image.new("RGB", im.size, bg)
        flat.paste(im, mask=im.split()[-1])
        im = flat
    else:
        im = im.convert("RGB")
    im.thumbnail(BOX, Image.LANCZOS)
    return im


def has_alpha(im: Image.Image) -> bool:
    return im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)


def process(rec: dict) -> dict:
    safe = rec["nwo"].replace("/", "__")
    strict_hit = None
    loose_hit = None

    for url in rec.get("shots") or []:
        data = fetch(url)
        if not data:
            continue
        try:
            im = Image.open(BytesIO(data))
            im.load()
        except Exception:
            continue
        if getattr(im, "n_frames", 1) > 1:
            im.seek(0)  # first frame of a demo GIF
        if looks_like_screenshot(im):
            strict_hit = (url, im)
            break
        if loose_hit is None:
            loose_hit = (url, im)

    hit = strict_hit or loose_hit
    if not hit:
        return {"nwo": rec["nwo"], "shot_light": "", "shot_dark": "", "shot_url": "", "shot_quality": "none"}

    url, im = hit
    alpha = has_alpha(im)
    light = thumb(im.copy(), LIGHT_BG)
    lp = SHOTS / f"{safe}__light.jpg"
    light.save(lp, "JPEG", quality=84, optimize=True)

    if alpha:
        dark = thumb(im.copy(), DARK_BG)
        dp = SHOTS / f"{safe}__dark.jpg"
        dark.save(dp, "JPEG", quality=84, optimize=True)
    else:
        dp = lp  # opaque image looks the same on both themes

    return {
        "nwo": rec["nwo"],
        "shot_light": str(lp),
        "shot_dark": str(dp),
        "shot_url": url,
        "shot_quality": "good" if strict_hit else "weak",
    }


def main() -> None:
    recs = json.loads((CACHE / "records.json").read_text(encoding="utf-8"))
    todo = [r for r in recs if r.get("shots")]
    print(f"downloading screenshots for {len(todo)} repos ({WORKERS} workers)...")

    out = {}
    done = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for res in ex.map(process, todo):
            out[res["nwo"]] = res
            done += 1
            if done % 25 == 0:
                print(f"  {done}/{len(todo)}")

    (CACHE / "shots.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    good = sum(1 for v in out.values() if v["shot_quality"] == "good")
    weak = sum(1 for v in out.values() if v["shot_quality"] == "weak")
    none = len(recs) - good - weak
    total_mb = sum(p.stat().st_size for p in SHOTS.glob("*.jpg")) / 1e6
    print(f"\ngood {good} | weak {weak} | none {none}  ({total_mb:.1f} MB of thumbnails)")
    missing = [r["name"] for r in recs if out.get(r["nwo"], {}).get("shot_quality", "none") == "none"]
    print(f"\nno usable screenshot ({len(missing)}): {', '.join(missing[:40])}")


if __name__ == "__main__":
    main()
