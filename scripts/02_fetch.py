"""Fetch repo metadata (stars, language, license, ...) plus README text for every entry.

Batched GraphQL for speed, with a REST fallback for repos whose README is not
literally README.md or that have been renamed/moved.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
READMES = CACHE / "readmes"
BATCH = 20
MAX_README = 240_000

FIELDS = """
    nameWithOwner
    description
    stargazerCount
    forkCount
    isArchived
    isFork
    createdAt
    pushedAt
    homepageUrl
    primaryLanguage { name }
    licenseInfo { spdxId name }
    defaultBranchRef { name }
    repositoryTopics(first: 20) { nodes { topic { name } } }
    readme: object(expression: "HEAD:README.md") { ... on Blob { text } }
"""


def gh(args: list[str]) -> str:
    p = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args[:3])} failed: {p.stderr[:600]}")
    return p.stdout


def graphql_batch(batch: list[dict]) -> dict:
    parts = []
    for i, e in enumerate(batch):
        owner = e["owner"].replace('"', '')
        repo = e["repo"].replace('"', '')
        parts.append(f'  r{i}: repository(owner: "{owner}", name: "{repo}") {{{FIELDS}}}')
    query = "query {\n" + "\n".join(parts) + "\n}"
    raw = gh(["api", "graphql", "-f", f"query={query}"])
    doc = json.loads(raw)
    return doc.get("data") or {}


def rest_fallback(nwo: str) -> dict:
    """REST follows repo renames and finds README under any filename/casing."""
    out = {}
    try:
        repo = json.loads(gh(["api", f"repos/{nwo}"]))
        out["meta"] = {
            "nameWithOwner": repo.get("full_name"),
            "description": repo.get("description"),
            "stargazerCount": repo.get("stargazers_count"),
            "forkCount": repo.get("forks_count"),
            "isArchived": repo.get("archived"),
            "isFork": repo.get("fork"),
            "createdAt": repo.get("created_at"),
            "pushedAt": repo.get("pushed_at"),
            "homepageUrl": repo.get("homepage"),
            "primaryLanguage": {"name": repo.get("language")} if repo.get("language") else None,
            "licenseInfo": {"spdxId": (repo.get("license") or {}).get("spdx_id")} if repo.get("license") else None,
            "defaultBranchRef": {"name": repo.get("default_branch")},
            "repositoryTopics": {"nodes": [{"topic": {"name": t}} for t in repo.get("topics") or []]},
        }
    except RuntimeError as exc:
        out["error"] = str(exc)[:300]
        return out
    try:
        out["readme"] = gh(["api", f"repos/{nwo}/readme", "-H", "Accept: application/vnd.github.raw"])
    except RuntimeError:
        out["readme"] = ""
    return out


def main() -> None:
    entries = json.loads((CACHE / "entries.json").read_text(encoding="utf-8"))
    force = "--force" in sys.argv
    meta_path = CACHE / "meta.json"
    meta = {} if force else json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}

    todo = [e for e in entries if e["nwo"] not in meta]
    print(f"{len(entries)} entries, {len(todo)} to fetch")

    for start in range(0, len(todo), BATCH):
        batch = todo[start : start + BATCH]
        try:
            data = graphql_batch(batch)
        except RuntimeError as exc:
            print(f"  batch {start} graphql error, falling back per-repo: {exc[:120] if isinstance(exc, str) else exc}")
            data = {}
        for i, e in enumerate(batch):
            node = data.get(f"r{i}") if data else None
            readme_text = ""
            if node:
                readme_text = ((node.get("readme") or {}).get("text")) or ""
                record = {k: v for k, v in node.items() if k != "readme"}
                if not readme_text:
                    fb = rest_fallback(e["nwo"])
                    readme_text = fb.get("readme") or ""
            else:
                fb = rest_fallback(e["nwo"])
                if "error" in fb:
                    print(f"  ! {e['nwo']}: {fb['error'][:100]}")
                    meta[e["nwo"]] = {"error": fb["error"], "readme_bytes": 0}
                    continue
                record = fb["meta"]
                readme_text = fb.get("readme") or ""

            record["readme_bytes"] = len(readme_text)
            meta[e["nwo"]] = record
            if readme_text:
                safe = e["nwo"].replace("/", "__")
                (READMES / f"{safe}.md").write_text(readme_text[:MAX_README], encoding="utf-8")
        done = min(start + BATCH, len(todo))
        print(f"  fetched {done}/{len(todo)}")
        meta_path.write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")

    meta_path.write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")

    ok = [v for v in meta.values() if "error" not in v]
    no_readme = [k for k, v in meta.items() if v.get("readme_bytes", 0) == 0]
    print(f"\ndone: {len(ok)} ok, {len(meta) - len(ok)} errors, {len(no_readme)} without README")
    for k in no_readme:
        print(f"  no readme: {k}")
    top = sorted(((v.get("stargazerCount") or 0, k) for k, v in meta.items()), reverse=True)[:10]
    print("\ntop 10 by stars:")
    for stars, k in top:
        print(f"  {stars:7,d}  {k}")


if __name__ == "__main__":
    main()
