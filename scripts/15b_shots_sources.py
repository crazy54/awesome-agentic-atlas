"""Images for the eleven source lists themselves, for the Sources sheet.

The listed items get whatever their README offers, but a curated list is best
represented by GitHub's own repo card: name, owner, description and star count in
one uniform tile. Eleven identical-format cards read as a credits page; eleven
scraped banners would not.
"""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"

spec = importlib.util.spec_from_file_location("s15", Path(__file__).parent / "15_shots_all.py")
s15 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s15)

NWOS = [
    "andyrewlee/awesome-agent-orchestrators", "kyrolabs/awesome-agents",
    "e2b-dev/awesome-ai-agents", "caramaschiHG/awesome-ai-agents-2026",
    "hesreallyhim/awesome-claude-code", "awesome-opencode/awesome-opencode",
    "ai-boost/awesome-harness-engineering", "nibzard/awesome-agentic-patterns",
    "heilcheng/awesome-agent-skills", "sickn33/agentic-awesome-skills",
    "shubhamsaboo/awesome-llm-apps",
]


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
