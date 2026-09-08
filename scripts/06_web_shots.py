"""Fill screenshot gaps for repos whose README had no usable image.

Pass 1: capture the project's own website with headless Chromium.
Pass 2: fall back to GitHub's Open Graph repo card, so every row shows something.
"""
import json
import re
import subprocess
import sys
import tempfile
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chrome  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
SHOTS = CACHE / "shots"
# 05_shots.py runs first and creates this, but only writes when a README actually yielded an image --
# a run where none did leaves the directory absent, and this stage is then the first to write into it.
SHOTS.mkdir(parents=True, exist_ok=True)
CHROME = chrome.PATH

BOX = (300, 150)
LIGHT_BG = (255, 255, 255)
DARK_BG = (24, 27, 36)
WORKERS = 4

# Homepages that are not a product page worth screenshotting.
SKIP_HOST = re.compile(r"(discord\.(gg|com)|x\.com|twitter\.com|github\.com|t\.me|linkedin\.com|youtube\.com|reddit\.com)", re.I)

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"}


def save_pair(im: Image.Image, safe: str, tag: str) -> tuple[str, str]:
    im = im.convert("RGB")
    im.thumbnail(BOX, Image.LANCZOS)
    lp = SHOTS / f"{safe}__{tag}.jpg"
    im.save(lp, "JPEG", quality=84, optimize=True)
    return str(lp), str(lp)


def capture_site(rec: dict) -> dict | None:
    url = (rec.get("homepage") or "").strip()
    # No browser on this machine means pass 1 has nothing to do; pass 2's Open Graph card still runs.
    if not CHROME or not url or SKIP_HOST.search(url):
        return None
    if not url.startswith("http"):
        url = "https://" + url
    safe = rec["nwo"].replace("/", "__")
    out = SHOTS / f"{safe}__site.png"

    with tempfile.TemporaryDirectory() as profile:
        cmd = [
            str(CHROME), "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
            "--disable-dev-shm-usage", "--no-first-run", "--disable-extensions",
            f"--user-data-dir={profile}", "--window-size=1280,800",
            "--virtual-time-budget=8000", f"--screenshot={out}", url,
        ]
        try:
            subprocess.run(cmd, capture_output=True, timeout=75)
        except subprocess.TimeoutExpired:
            return None

    if not out.exists() or out.stat().st_size < 6000:
        out.unlink(missing_ok=True)
        return None
    try:
        im = Image.open(out)
        im.load()
    except Exception:
        out.unlink(missing_ok=True)
        return None

    # A near-uniform page means an error/blank render, not a real site.
    small = im.convert("RGB").resize((32, 20))
    px = list(small.getdata())
    if len({p for p in px}) < 6:
        out.unlink(missing_ok=True)
        return None

    lp, dp = save_pair(im, safe, "site")
    out.unlink(missing_ok=True)
    return {"nwo": rec["nwo"], "shot_light": lp, "shot_dark": dp, "shot_url": url,
            "shot_quality": "site", "shot_kind": "website"}


def capture_card(rec: dict) -> dict | None:
    """GitHub's Open Graph card: name, description, stars, language."""
    safe = rec["nwo"].replace("/", "__")
    url = f"https://opengraph.githubassets.com/1/{rec['nwo']}"
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=25) as r:
            data = r.read(6_000_000)
        im = Image.open(BytesIO(data))
        im.load()
    except Exception:
        return None
    lp, dp = save_pair(im, safe, "card")
    return {"nwo": rec["nwo"], "shot_light": lp, "shot_dark": dp, "shot_url": rec["url"],
            "shot_quality": "card", "shot_kind": "repo card"}


def main() -> None:
    recs = json.loads((CACHE / "records.json").read_text(encoding="utf-8"))
    shots = json.loads((CACHE / "shots.json").read_text(encoding="utf-8"))

    for nwo, v in shots.items():
        v.setdefault("shot_kind", "readme" if v.get("shot_quality") in ("good", "weak") else "")

    def needs(r):
        return shots.get(r["nwo"], {}).get("shot_quality", "none") in ("none", "weak")

    # ---- pass 1: project websites
    todo = [r for r in recs if needs(r) and r.get("homepage") and not SKIP_HOST.search(r["homepage"])]
    print(f"pass 1: capturing {len(todo)} project websites with headless Chromium...")
    got = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for i, res in enumerate(ex.map(capture_site, todo), 1):
            if res:
                shots[res["nwo"]] = res
                got += 1
            if i % 8 == 0:
                print(f"  {i}/{len(todo)} ({got} captured)")
    print(f"  captured {got}/{len(todo)} websites")
    (CACHE / "shots.json").write_text(json.dumps(shots, indent=1, ensure_ascii=False), encoding="utf-8")

    # ---- pass 2: repo cards for whatever is still missing
    todo2 = [r for r in recs if shots.get(r["nwo"], {}).get("shot_quality", "none") == "none"]
    print(f"\npass 2: generating {len(todo2)} GitHub repo cards...")
    got2 = 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        for res in ex.map(capture_card, todo2):
            if res:
                shots[res["nwo"]] = res
                got2 += 1
    print(f"  generated {got2}/{len(todo2)} cards")

    (CACHE / "shots.json").write_text(json.dumps(shots, indent=1, ensure_ascii=False), encoding="utf-8")

    kinds = {}
    for r in recs:
        k = shots.get(r["nwo"], {}).get("shot_kind") or "none"
        kinds[k] = kinds.get(k, 0) + 1
    mb = sum(p.stat().st_size for p in SHOTS.glob("*.jpg")) / 1e6
    print(f"\nimage coverage: {kinds}  ({mb:.1f} MB)")
    still = [r["name"] for r in recs if not shots.get(r["nwo"], {}).get("shot_light")]
    print(f"no image at all ({len(still)}): {', '.join(still)}")


if __name__ == "__main__":
    main()
