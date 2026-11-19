"""Fetch metadata and README for every GitLab project the parser emitted, in GitHub's shape.

`11_fetch_all.py` asks GitHub's GraphQL about every `owner/repo` and files each answer in
`cache/meta.json` under the field names GitHub uses -- `stargazerCount`, `pushedAt`, `licenseInfo` and
the rest -- and every later stage reads those names. It skips host-qualified rows (see `hosts.py`),
which is where this stage comes in: it asks gitlab.com's GraphQL about each `gitlab.com/...` row and
writes the answer into the same file, under the same names, so `14_classify_all.py`, `16_build_all.py`
and `19_pages.py` take a GitLab project exactly as they take a GitHub repo and need no second code path.

How each field is filled, from one anonymous GraphQL request per `BATCH` projects:

  nameWithOwner     the host-qualified nwo of `fullPath` -- GitLab's spelling, so a change of case is
                    followed the way `16_build_all.canonicalise_nwo` follows GitHub's
  stargazerCount    `starCount`             forkCount    `forksCount`
  pushedAt          `lastActivityAt`. Not quite the same thing: GitLab's counts issues and merge
                    requests as activity, not only pushes. It is the field GitLab offers, and it is
                    what "pushed" means on a GitLab row (handbook/gitlab.md says so too)
  isArchived        `archived`              isFork       `isForked`
  primaryLanguage   the language with the largest `share` in `languages`
  licenseInfo       recognised from the text of the LICENSE file (`license_of`), because GitLab's
                    GraphQL has no licence field and REST's `?license=true` is one request a project.
                    Unrecognised text is GitHub's own `NOASSERTION`; no file is no licence
  defaultBranchRef  `repository.rootRef`
  repositoryTopics  `topics`, GitLab's own spelling
  readme            the first README-named blob, written to `cache/readmes/` as 11 writes GitHub's

plus three fields only a GitLab record has: `host`, `webUrl` and `avatarUrl` (the project's avatar,
which `15_shots_all.py` can use as the picture of last resort, GitLab having no social card).

**A failed read changes nothing.** Anonymous gitlab.com allows about sixty requests an hour per IP,
shared with whatever else that IP is doing, so a batch can be refused for reasons that have nothing to
do with the projects in it. This stage keeps the last good answer for every GitLab project in
`cache/gitlab/meta.json` and uses it for any project this run could not read. A project with no answer
at all -- refused today and never read before -- is simply absent from `meta.json`, and
`14_classify_all.py` leaves such a GitLab row out of the build rather than publishing it as broken. A
project GitLab positively says nothing about (the batch answered and it was not in it: deleted, made
private, or moved) is recorded as an error, which is the same thing 11 records for a GitHub 404.

  11b_fetch_gitlab.py           fetch every GitLab row in cache/entries_all.json
  11b_fetch_gitlab.py --status  how many GitLab rows there are and what the last-good store holds
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import gitlab_api as gl  # noqa: E402
import hosts  # noqa: E402

CACHE = ROOT / "cache"
ENTRIES = CACHE / "entries_all.json"
META = CACHE / "meta.json"
READMES = CACHE / "readmes"
LAST_GOOD = CACHE / "gitlab" / "meta.json"

BATCH = 25
MAX_README = 240_000          # 02_fetch.MAX_README, so a GitLab README is cut where a GitHub one is

README_NAMES = ("README.md", "readme.md", "Readme.md", "README.markdown", "README.rst", "README.txt",
                "README")
LICENSE_NAMES = ("LICENSE", "LICENSE.md", "LICENSE.txt", "LICENCE", "LICENCE.md", "COPYING",
                 "COPYING.md", "license", "LICENSE-MIT", "LICENSE-APACHE")

QUERY = """query($paths: [String!], $blobs: [String!]!) {
  projects(fullPaths: $paths, first: 100) {
    nodes {
      fullPath description starCount forksCount archived isForked createdAt lastActivityAt
      topics webUrl avatarUrl
      languages { name share }
      repository { rootRef empty blobs(paths: $blobs) { nodes { path rawTextBlob } } }
    }
  }
}"""

# Licence texts by a phrase only that licence's text carries, most specific first: the LGPL and AGPL
# texts both say "GNU GENERAL PUBLIC LICENSE" further down, and the BSD clauses are a subset of each
# other. Enough for the licences that cover nearly every open project; anything else is NOASSERTION,
# which is what GitHub says for a licence it cannot place either.
LICENSES: list[tuple[str, str, re.Pattern]] = [
    ("AGPL-3.0", "GNU Affero General Public License v3.0", re.compile(r"GNU AFFERO GENERAL PUBLIC", re.I)),
    ("LGPL-3.0", "GNU Lesser General Public License v3.0",
     re.compile(r"GNU LESSER GENERAL PUBLIC LICENSE\s+Version 3", re.I)),
    ("LGPL-2.1", "GNU Lesser General Public License v2.1",
     re.compile(r"GNU LESSER GENERAL PUBLIC LICENSE\s+Version 2\.1", re.I)),
    ("GPL-3.0", "GNU General Public License v3.0", re.compile(r"GNU GENERAL PUBLIC LICENSE\s+Version 3", re.I)),
    ("GPL-2.0", "GNU General Public License v2.0", re.compile(r"GNU GENERAL PUBLIC LICENSE\s+Version 2", re.I)),
    ("MPL-2.0", "Mozilla Public License 2.0", re.compile(r"Mozilla Public License,?\s+(?:Version|v\.)\s*2\.0", re.I)),
    ("EUPL-1.2", "European Union Public License 1.2", re.compile(r"European Union Public Licen[cs]e\b.{0,40}1\.2", re.I | re.S)),
    ("Apache-2.0", "Apache License 2.0", re.compile(r"Apache License,?\s+Version 2\.0", re.I)),
    ("Unlicense", "The Unlicense", re.compile(r"free and unencumbered software released into the public domain", re.I)),
    ("ISC", "ISC License", re.compile(r"Permission to use, copy, modify, and(?:/or)? distribute this software for any", re.I)),
    ("MIT", "MIT License", re.compile(r"Permission is hereby granted, free of charge", re.I)),
    ("BSD-3-Clause", 'BSD 3-Clause "New" or "Revised" License',
     re.compile(r"Redistribution and use in source and binary forms.*Neither the name", re.I | re.S)),
    ("BSD-2-Clause", 'BSD 2-Clause "Simplified" License',
     re.compile(r"Redistribution and use in source and binary forms", re.I)),
]


def license_of(text: str) -> dict | None:
    """`licenseInfo` for a LICENSE file's text: GitHub's shape, None for no file."""
    if not text:
        return None
    for spdx, name, rx in LICENSES:
        if rx.search(text[:20_000]):
            return {"spdxId": spdx, "name": name}
    return {"spdxId": "NOASSERTION", "name": "Other"}


def record(node: dict) -> tuple[dict, str]:
    """(meta record, README text) for one GraphQL project node."""
    repo = node.get("repository") or {}
    blobs = {b.get("path"): b.get("rawTextBlob") or "" for b in ((repo.get("blobs") or {}).get("nodes") or ())}
    readme = next((blobs[n] for n in README_NAMES if blobs.get(n)), "")
    lic = next((blobs[n] for n in LICENSE_NAMES if blobs.get(n)), "")
    langs = sorted(node.get("languages") or (), key=lambda l: -(l.get("share") or 0))
    nwo = hosts.qualify(hosts.GITLAB, node["fullPath"])
    return {
        "nameWithOwner": nwo,
        # GitLab's description, or -- for the many projects that leave it empty -- the README's first line
        # of prose, which is what the row's blurb would otherwise lack.
        "description": (node.get("description") or "").strip() or gl.readme_summary(readme),
        "stargazerCount": int(node.get("starCount") or 0),
        "forkCount": int(node.get("forksCount") or 0),
        "isArchived": bool(node.get("archived")),
        "isFork": bool(node.get("isForked")),
        "createdAt": node.get("createdAt") or "",
        "pushedAt": node.get("lastActivityAt") or "",
        # GitLab has no homepage field; a project that has one says so in its README, which is where
        # 04_classify looks for an install line anyway.
        "homepageUrl": "",
        "primaryLanguage": {"name": langs[0]["name"]} if langs else None,
        "licenseInfo": license_of(lic),
        "defaultBranchRef": {"name": repo.get("rootRef")} if repo.get("rootRef") else None,
        "repositoryTopics": {"nodes": [{"topic": {"name": t}} for t in node.get("topics") or ()]},
        "host": hosts.GITLAB,
        "webUrl": node.get("webUrl") or hosts.web_url(nwo),
        "avatarUrl": node.get("avatarUrl") or "",
    }, readme


def wanted(rows: list[dict]) -> list[str]:
    """Distinct GitLab nwos in first-listed order."""
    out, seen = [], set()
    for r in rows:
        nwo = r.get("nwo") or ""
        if nwo and not hosts.is_github(nwo) and nwo.lower() not in seen:
            seen.add(nwo.lower())
            out.append(nwo)
    return out


def fetch(client: gl.Client, nwos: list[str], log=print) -> tuple[dict[str, dict], dict[str, str], set[str]]:
    """({nwo: record}, {nwo: README}, {nwos a batch that answered did not contain}). A refused batch
    contributes to none of the three."""
    got: dict[str, dict] = {}
    readmes: dict[str, str] = {}
    missing: set[str] = set()
    blobs = list(README_NAMES + LICENSE_NAMES)
    for start in range(0, len(nwos), BATCH):
        batch = nwos[start:start + BATCH]
        try:
            data = client.graphql(QUERY, {"paths": [hosts.path_of(n) for n in batch], "blobs": blobs})
        except gl.GitLabError as exc:
            log(f"  batch {start}: {exc}")
            if "rate limited" in str(exc):
                break
            continue
        nodes = {n["fullPath"].lower(): n for n in ((data.get("projects") or {}).get("nodes") or ())}
        for nwo in batch:
            node = nodes.get(hosts.path_of(nwo).lower())
            if node is None:
                missing.add(nwo)
                continue
            got[nwo], readmes[nwo] = record(node)
    return got, readmes, missing


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    rows = json.loads(ENTRIES.read_text(encoding="utf-8")) if ENTRIES.exists() else []
    nwos = wanted(rows)
    last = json.loads(LAST_GOOD.read_text(encoding="utf-8")) if LAST_GOOD.exists() else {}
    if args.status:
        print(f"{len(nwos)} GitLab projects in {ENTRIES.relative_to(ROOT).as_posix()}; "
              f"{len(last)} with a last good answer in {LAST_GOOD.relative_to(ROOT).as_posix()}")
        return
    if not nwos:
        print("no GitLab rows to fetch" + ("" if hosts.enabled() else " (flag intake.gitlab is off)"))
        return

    client = gl.Client()
    got, readmes, missing = fetch(client, nwos)
    meta = json.loads(META.read_text(encoding="utf-8")) if META.exists() else {}
    READMES.mkdir(parents=True, exist_ok=True)
    fresh = stale = gone = absent = 0
    for nwo in nwos:
        if nwo in got:
            rec, text = got[nwo], readmes.get(nwo, "")
            rec["readme_bytes"] = len(text)
            last[nwo] = rec
            fresh += 1
            if text:
                (READMES / hosts.readme_file(nwo)).write_text(text[:MAX_README], encoding="utf-8")
            meta[nwo] = rec
        elif nwo in missing:
            meta[nwo] = {"error": "NOT_FOUND", "readme_bytes": 0}
            gone += 1
        elif nwo in last:
            # Not read this run: yesterday's answer, README and all (the README file from that run is
            # still in cache/readmes/ unless the cache was cold, in which case readme_bytes says so).
            meta[nwo] = dict(last[nwo])
            stale += 1
        else:
            absent += 1
    META.write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
    LAST_GOOD.parent.mkdir(parents=True, exist_ok=True)
    LAST_GOOD.write_text(json.dumps(last, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{len(nwos)} GitLab projects: {fresh} fetched, {stale} from the last good answer, "
          f"{gone} gone, {absent} unread and left out of this build · {client.requests} requests")
    if stale or absent:
        print(f"::warning title=GitLab fetch incomplete::{stale + absent} of {len(nwos)} GitLab projects "
              f"were not read this run ({'anonymous; ' if not client.token else ''}see the log). "
              f"{stale} use their last good answer and {absent} are left out until a run can read them.")


if __name__ == "__main__":
    main()
