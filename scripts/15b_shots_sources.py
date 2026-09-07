"""Images for the source lists themselves, for the Sources sheet.

The listed items get whatever their README offers, but a curated list is best
represented by GitHub's own repo card: name, owner, description and star count in
one uniform tile. Identical-format cards read as a credits page; the same number
of scraped banners would not.

One card per entry in `10_parse_sources.SOURCES`, read from there rather than
listed here. This file used to name eleven repos by hand, which was the same
eleven the workbook gave a sheet of its own -- so when the Sources sheet grew to
credit every list the atlas is built from, twenty-five of its rows had no card
and no stage said so. A list this stage forgets is a blank cell on a credits
page, which is the one place the omission is least visible and worst.
"""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"

spec = importlib.util.spec_from_file_location("s15", Path(__file__).parent / "15_shots_all.py")
s15 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s15)

spec = importlib.util.spec_from_file_location("b10", Path(__file__).parent / "10_parse_sources.py")
b10 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b10)

# dict.fromkeys, not a set: the Sources sheet is in this order and a credits page should not reshuffle
# itself between runs. Two sources could in principle name one repo, hence the dedupe.
NWOS = list(dict.fromkeys(s["nwo"] for s in b10.SOURCES))


def main() -> None:
    out = CACHE / "shots_all.json"
    have = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}
    for nwo in NWOS:
        rec = dict(kind="repo", nwo=nwo, url=f"https://github.com/{nwo}",
                   name=nwo.split("/")[-1], shots=[], unavailable=False)
        res = s15.work(rec)
        have[res["key"]] = res
        print(f"  {res['tier']:12s} {nwo}", flush=True)
    out.write_text(json.dumps(have, indent=1), encoding="utf-8")
    print(f"{len(NWOS)} source cards -> {out.name}")


if __name__ == "__main__":
    main()
