"""Parse awesome-agent-orchestrators README into structured entries."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "cache" / "README.md"

# Category order as it appears in the README, with short keys used for theming.
CAT_KEYS = {
    "Parallel Coding Agents — Terminal (TUI/CLI)": "terminal",
    "Parallel Coding Agents — Desktop & Web": "desktop",
    "Multi-Agent Swarms": "swarms",
    "Autonomous Loop Runners": "loops",
    "Autonomous Task Runners": "tasks",
    "Agent Infrastructure & Primitives": "infra",
    "Personal Assistants": "assistants",
    "Resting": "resting",
}

ENTRY_RE = re.compile(r"^-\s+\[(?P<name>[^\]]+)\]\((?P<url>https?://[^)]+)\)\s*-\s*(?P<desc>.*)$")
REPO_RE = re.compile(r"^https?://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/#?]+)")
RESTING_NOTE_RE = re.compile(r"_\((?P<note>[^)]*)\)_\s*$")


def parse_text(text: str) -> list[dict]:
    """Entries in README order. Takes the text rather than reading SRC so pull_sources.py can run
    this same parser over the previous commit's copy and diff the two."""
    entries, category, order = [], None, 0

    for line in text.splitlines():
        if line.startswith("## "):
            heading = line[3:].strip()
            category = heading if heading in CAT_KEYS else None
            continue
        if category is None:
            continue
        m = ENTRY_RE.match(line.strip())
        if not m:
            continue

        desc = m.group("desc").strip()
        note = ""
        nm = RESTING_NOTE_RE.search(desc)
        if nm:
            note = nm.group("note").strip()
            desc = desc[: nm.start()].strip()

        rm = REPO_RE.match(m.group("url"))
        if not rm:
            continue

        order += 1
        entries.append(
            {
                "order": order,
                "name": m.group("name").strip(),
                "url": m.group("url").rstrip("/"),
                "owner": rm.group("owner"),
                "repo": rm.group("repo"),
                "nwo": f"{rm.group('owner')}/{rm.group('repo')}",
                "category": category,
                "cat_key": CAT_KEYS[category],
                "description": desc,
                "status_note": note,
            }
        )

    return entries


def dedupe(entries: list[dict], report: bool = True) -> list[dict]:
    """One row per owner/repo, keeping the first listing."""
    seen, unique = set(), []
    for e in entries:
        key = e["nwo"].lower()
        if key in seen:
            if report:
                print(f"  ! duplicate skipped: {e['nwo']} ({e['category']})")
            continue
        seen.add(key)
        unique.append(e)
    return unique


def main() -> None:
    if not SRC.exists():
        sys.exit(f"{SRC.relative_to(ROOT).as_posix()} is not there. Run "
                 f"`python scripts/pull_sources.py` first -- cache/ is not committed.")
    unique = dedupe(parse_text(SRC.read_text(encoding="utf-8")))

    out = ROOT / "cache" / "entries.json"
    out.write_text(json.dumps(unique, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"parsed {len(unique)} entries -> {out}")
    for cat, key in CAT_KEYS.items():
        n = sum(1 for e in unique if e["cat_key"] == key)
        print(f"  {n:4d}  {cat}")


if __name__ == "__main__":
    main()
