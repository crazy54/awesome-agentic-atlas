"""Turn parsed rows + fetched signals into the final record per listed item.

Reuses 04_classify.py unchanged for the hard part (OS support, install command,
screenshot candidates) and adds the handling the multi-source lists need:

* kind "repo"    -- a standalone project. Full classification, same as before.
* kind "subpath" -- an item *inside* a repo (a template folder, a pattern doc).
  Its parent's OS support is not its own, so those columns stay blank rather
  than inherit a claim that was never made about it.
* kind "site"    -- a hosted product with no repo. No stars, no README, so no
  OS verdict; the row carries its URL and a live screenshot instead.
"""
import importlib.util
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from buckets import bucket_map, bucket_order  # noqa: E402
import signals as sig  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
READMES = CACHE / "readmes"

spec = importlib.util.spec_from_file_location("cls04", Path(__file__).parent / "04_classify.py")
c4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c4)

DASH = "—"


def blank_os(reason: str) -> dict:
    return dict(win_native=DASH, win_wsl2=DASH, macos=DASH, linux=DASH,
                docker=DASH, cloud=DASH, gh_action=DASH,
                os_summary=DASH, os_confidence="n/a", os_evidence=reason)


def main() -> None:
    rows = json.loads((CACHE / "entries_all.json").read_text(encoding="utf-8"))
    meta = json.loads((CACHE / "meta.json").read_text(encoding="utf-8"))
    rel = json.loads((CACHE / "releases.json").read_text(encoding="utf-8"))
    acts = json.loads((CACHE / "actions.json").read_text(encoding="utf-8"))

    records = []
    for r in rows:
        bm = bucket_map(r["source"])
        rec = dict(r)
        rec["section"] = r["category"]
        rec["bucket"] = bm.get(r["category"], r["category"])

        nwo = r.get("nwo") or ""
        m = meta.get(nwo, {}) if nwo else {}
        has_meta = bool(nwo) and "error" not in m

        # --- fields that exist for anything backed by a repo -------------
        if has_meta:
            branch = ((m.get("defaultBranchRef") or {}).get("name")) or "HEAD"
            rec.update(
                stars=m.get("stargazerCount") or 0,
                forks=m.get("forkCount") or 0,
                archived=bool(m.get("isArchived")),
                language=((m.get("primaryLanguage") or {}).get("name")) or "",
                license=((m.get("licenseInfo") or {}).get("spdxId")) or "",
                homepage=(m.get("homepageUrl") or "").strip(),
                pushed_at=(m.get("pushedAt") or "")[:10],
                created_at=(m.get("createdAt") or "")[:10],
                gh_description=m.get("description") or "",
                branch=branch,
                readme_bytes=m.get("readme_bytes", 0),
                unavailable=False,
            )
        else:
            rec.update(stars=0, forks=0, archived=False, language="", license="",
                       homepage=r.get("website", ""), pushed_at="", created_at="",
                       gh_description="", branch="HEAD", readme_bytes=0,
                       unavailable=bool(nwo))

        md = ""
        if has_meta:
            p = READMES / f"{nwo.replace('/', '__')}.md"
            if p.exists():
                md = p.read_text(encoding="utf-8", errors="replace")

        # --- per-kind treatment -----------------------------------------
        if r["kind"] == "repo" and has_meta:
            entry = {"name": r["name"], "url": r["url"], "owner": r["owner"],
                     "repo": r["repo"], "nwo": nwo, "category": r["category"],
                     "description": r["description"], "status_note": ""}
            # sig.is_action, not the raw value: actions.json entries are dicts now (they carry the
            # push time the answer was observed at), and bool() of any dict is True.
            rec.update(c4.classify(entry, m, rel.get(nwo, {}), md, sig.is_action(acts.get(nwo))))
            rec["shots"] = c4.shot_candidates(md, entry, rec["branch"])
            rec["stars_kind"] = "own"

        elif r["kind"] == "subpath":
            rec.update(blank_os("Item inside a larger repo — the parent's platform "
                                "support is not a claim about this item"))
            path = r.get("subpath", "")
            # tree/HEAD/<dir> -> the directory a user actually needs
            inner = path.split("/", 2)[-1] if path.startswith(("tree/", "blob/")) else path
            rec["install_cmd"] = (f"git clone https://github.com/{nwo}.git && cd "
                                  f"{nwo.split('/')[-1]}/{inner}" if inner else
                                  f"git clone https://github.com/{nwo}.git")
            rec["install_method"] = "in-repo"
            rec["shots"] = []
            rec["parent_stars"] = m.get("stargazerCount") or 0
            rec["stars"] = 0
            rec["stars_kind"] = "parent"

        elif r["kind"] == "repo" and not has_meta:
            rec.update(blank_os("GitHub returned an error — repo deleted, renamed or private"))
            rec["install_cmd"] = ""
            rec["install_method"] = "unavailable"
            rec["shots"] = []
            rec["stars_kind"] = "none"

        else:  # site
            rec.update(blank_os("Hosted product, not a public repo — no README to read"))
            rec["install_cmd"] = r["url"]
            rec["install_method"] = "website"
            rec["shots"] = []
            rec["stars_kind"] = "none"

        rec.setdefault("parent_stars", 0)
        rec.setdefault("install_cmd", "")
        rec.setdefault("install_method", "")
        rec.setdefault("shots", [])
        # the list's own blurb is usually better written than the repo's
        rec["blurb"] = (r["description"] or rec.get("gh_description") or "").strip()
        records.append(rec)

    out = CACHE / "records_all.json"
    out.write_text(json.dumps(records, indent=1, ensure_ascii=False), encoding="utf-8")

    print(f"classified {len(records)} rows -> {out}\n")
    print(f"{'source':13s} {'rows':>5s} {'stars>0':>7s} {'win Y/L':>9s} {'install':>7s} "
          f"{'shots':>5s}  buckets")
    for src in dict.fromkeys(r["source"] for r in records):
        rs = [r for r in records if r["source"] == src]
        print(f"{src:13s} {len(rs):5d} {sum(1 for r in rs if r['stars'] > 0):7d} "
              f"{sum(1 for r in rs if r['win_native'] == 'Yes'):4d}/"
              f"{sum(1 for r in rs if r['win_native'] == 'Likely'):<4d} "
              f"{sum(1 for r in rs if r['install_cmd']):7d} "
              f"{sum(1 for r in rs if r['shots']):5d}  {len(bucket_order(src)) or '?'}")
    unmapped = {(r['source'], r['section']) for r in records if r['bucket'] == r['section']
                and r['section'] not in bucket_order(r['source'])}
    if unmapped:
        print("\nsections with no bucket (they keep their own name):")
        for s, c in sorted(unmapped):
            print(f"  {s:13s} {c}")


if __name__ == "__main__":
    main()
