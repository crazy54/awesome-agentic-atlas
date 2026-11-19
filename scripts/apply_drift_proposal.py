"""Write a provisional build's placements into taxonomy.py and buckets.py, for a person to review.

A provisional build (`drift.py`) files an unmapped section for one run and says where. This is the
other half: it turns `cache/drift-proposal.json` into the edit that makes those placements permanent,
in the place a person would have made it -- each `SECTIONS` key at the end of its own list's block,
each folded section inside the bucket it was folded into -- so the result is a reviewable diff and not
a pile of lines appended at the bottom of a dict.

It does not decide anything. The placements are the build's, every one of them labelled with its
evidence, and the diff this writes is a *proposal*: the CI stream opens it as a draft PR, and the
person reviewing it is the one who re-files a section the evidence got wrong. A modal placement --
"no rename evidence; this is where most of the list files" -- is the one most worth a second look, and
the PR body (`cache/drift-proposal.md`) says which those are.

  python scripts/apply_drift_proposal.py                 # apply cache/drift-proposal.json
  python scripts/apply_drift_proposal.py PROPOSAL.json   # apply another one
  python scripts/apply_drift_proposal.py --check         # say what it would change, write nothing

Idempotent: a key already in SECTIONS, or a section already in its bucket, is skipped, so running it
over the same proposal twice -- or over a proposal a person has half applied by hand -- is safe. After
writing it re-imports both modules in a fresh interpreter and runs `buckets.check()`, and exits 1 if
either file no longer imports or any placement is still unmapped, so a bad edit cannot reach a PR.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TAXONOMY = HERE / "taxonomy.py"
BUCKETS = HERE / "buckets.py"
sys.path.insert(0, str(HERE))
import drift  # noqa: E402


def q(s: str) -> str:
    """A Python string literal in the files' own style: double quotes, no ASCII-escaping of headings."""
    return json.dumps(s, ensure_ascii=False)


def dict_span(lines: list[str], opener: str) -> tuple[int, int]:
    """(first line, closing-brace line) of a top-level `NAME... = {` block."""
    start = next(i for i, ln in enumerate(lines) if ln.startswith(opener))
    end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("}"))
    return start, end


def add_sections(text: str, recs: list[dict]) -> tuple[str, list[str]]:
    lines = text.split("\n")
    done = []
    for r in recs:
        if not r.get("category"):
            continue
        start, end = dict_span(lines, "SECTIONS")
        key = f"({q(r['source'])}, {q(r['section'])})"
        if any(ln.strip().startswith(key + ":") for ln in lines[start:end]):
            continue
        new = f"    {key}: {q(r['category'])},"
        mine = [i for i in range(start, end) if lines[i].lstrip().startswith(f"({q(r['source'])}, ")]
        if mine:
            at = mine[-1] + 1
            # A key whose value would not fit sits on the next line (`agentsec_recon` has five); the
            # insertion goes after the value, not between the key and it.
            if lines[mine[-1]].rstrip().endswith(":"):
                at += 1
        else:
            at = end
            lines[at:at] = ["", f"    # {r['source']} (added by a provisional build; name its list here)"]
            at += 2
        lines[at:at] = [new]
        done.append(new.strip())
    return "\n".join(lines), done


def add_buckets(text: str, recs: list[dict]) -> tuple[str, list[str]]:
    lines = text.split("\n")
    done = []
    for r in recs:
        if not r.get("bucket"):
            continue
        start, end = dict_span(lines, "BUCKETS")
        head = next((i for i in range(start, end) if lines[i].startswith(f"    {q(r['source'])}: [")), None)
        if head is None:
            if not r.get("new_map"):
                continue
            block = [f"    {q(r['source'])}: ["] + [
                f"        ({q(b)}, [{', '.join(q(s) for s in secs)}])," for b, secs in r["new_map"]] + ["    ],"]
            lines[end:end] = block
            done.append(f"{r['source']}: new map, {len(r['new_map'])} buckets")
            continue
        stop = next(i for i in range(head + 1, end) if lines[i].startswith("    ],"))
        # The bucket's opening line is `("Name", [` whether its members follow on the same line or below.
        pat = re.compile(r"^\s*\(" + re.escape(q(r["bucket"])) + r",\s*\[")
        row = next((i for i in range(head, stop) if pat.match(lines[i])), None)
        if row is None:
            continue
        # Already a member? Scan from the bucket's line to the line that closes its list.
        close = next(i for i in range(row, stop + 1) if "])" in lines[i])
        if any(q(r["section"]) in ln for ln in lines[row:close + 1]):
            continue
        m = pat.match(lines[row])
        lines[row] = lines[row][:m.end()] + q(r["section"]) + ", " + lines[row][m.end():]
        lines[row] = lines[row].replace(", ]", "]")
        done.append(f"{r['source']}: {r['section']!r} -> {r['bucket']!r}")
    return "\n".join(lines), done


def verify(recs: list[dict]) -> list[str]:
    """Re-import both modules from disk in a clean interpreter and ask whether the proposal took."""
    keys = [[r["source"], r["section"]] for r in recs if r.get("category")]
    code = (
        "import json, sys; sys.path.insert(0, sys.argv[1]); import buckets, taxonomy\n"
        "buckets.check()\n"
        "keys = json.loads(sys.argv[2])\n"
        "missing = [k for k in keys if tuple(k) not in taxonomy.SECTIONS]\n"
        "print(json.dumps(missing))\n")
    out = subprocess.run([sys.executable, "-c", code, str(HERE), json.dumps(keys, ensure_ascii=False)],
                         capture_output=True, text=True, encoding="utf-8",
                         env={**__import__("os").environ, drift.ENV: ""})
    if out.returncode != 0:
        return [f"the edited modules do not load: {(out.stderr or out.stdout).strip()[-400:]}"]
    missing = json.loads(out.stdout.strip().splitlines()[-1])
    return [f"still unmapped after the edit: {k[0]} / {k[1]}" for k in missing]


def main() -> int:
    drift.utf8_console()
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("proposal", nargs="?", default=str(drift.PROPOSAL))
    ap.add_argument("--check", action="store_true", help="report what would change; write nothing")
    args = ap.parse_args()

    doc = json.loads(Path(args.proposal).read_text(encoding="utf-8"))
    recs = doc.get("placements") or []
    if not recs:
        print("nothing to apply: the proposal has no placements")
        return 0

    tax_text, tax_done = add_sections(TAXONOMY.read_text(encoding="utf-8"), recs)
    buck_text, buck_done = add_buckets(BUCKETS.read_text(encoding="utf-8"), recs)
    for line in tax_done:
        print(f"  taxonomy.py  + {line}")
    for line in buck_done:
        print(f"  buckets.py   + {line}")
    if not tax_done and not buck_done:
        print("nothing to apply: every placement is already in taxonomy.py and buckets.py")
        return 0
    if args.check:
        return 0

    # Written with the newline the files already use, so the diff is the added lines and nothing else.
    for path, text in ((TAXONOMY, tax_text), (BUCKETS, buck_text)):
        nl = "\r\n" if b"\r\n" in path.read_bytes() else "\n"
        path.write_bytes(text.replace("\r\n", "\n").replace("\n", nl).encode("utf-8"))

    problems = verify(recs)
    for p in problems:
        print(f"  ! {p}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
