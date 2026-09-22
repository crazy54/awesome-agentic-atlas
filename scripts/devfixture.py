"""Rebuild the three cache files `19_pages.py` needs, out of the site it already published.

WHY THIS EXISTS

Stage 19 is the index. It reads `cache/records_all.json`, `cache/meta.json` and `cache/records.json`
-- the crawl's output -- and none of the three is committed, so on a checkout the one command that can
rewrite `docs/index.html` cannot be run at all. Everything downstream of that is CI-only by
consequence: a redesign of the page, a diff of two renders, a Playwright run against the real markup.
`19b_refresh.py` is the usual way round it and is the wrong tool for a redesign, because it re-renders
the shell over the *committed* rows and refuses outright when those rows and the checkout's `SOURCES`
disagree about how many lists were merged.

The observation this file is built on is that the crawl's output is recoverable, because `19_pages.py`
already published almost all of it. `docs/data.json` is one row per repo with the name, the repo, the
category, the targets, the stars, the list count, the list names, the five OS verdicts, the blurb, the
install command, the language, the licence, the push date, the URL and the social card. That is enough
to invert: one listing per (repo, list) pair reproduces `lists` and `listed_by`, a section that maps to
the row's category reproduces the category vote, `meta.json` is the star map written back out, and a
one-entry shot map reproduces the rows that carry artwork of their own.

So this is a *reconstruction*, not a mock. It writes no HTML and knows nothing about the page: it
hands the real `main()` the three files it asks for and lets the real generator do the work. Whatever
`19_pages.py` says about the tree it is run on is what you get, which is the only property that makes
the output worth diffing.

WHAT IT REFUSES TO DO

It never writes into `cache/`. A real CI run reads that directory, `weekly.yml`'s resume logic treats
"the file is there" as "the stage ran", and a fixture sitting in it would be picked up by a production
build and published as the atlas. Output goes under `build-tmp/` -- untracked, ignored, and the same
scratch directory the suite already uses -- and any `--out` that resolves inside `cache/`, `docs/`,
`state/`, `mega-list/`, `scripts/` or `tests/` is rejected before anything is opened. Writing is
opt-in: with no flags this reports what it would build and exits.

The generator's own writes are redirected the same way. `19_pages.main()` writes `data.json`,
`.nojekyll` and `index.html` into its module-level `OUT`, and `newness.resolve()` appends to the
tracked `state/first-seen.json`; both are pointed at the fixture directory for the duration of the
build, so a run leaves the working tree exactly as it found it.

  python scripts/devfixture.py                        # say what it would write, touch nothing
  python scripts/devfixture.py --build                # write the fixture, then render the index
  python scripts/devfixture.py --build --verify       # ...and diff the result against docs/data.json

WHAT IS AND IS NOT FAITHFUL

Faithful: the row set, the row order, and every published column -- verified by `--verify`, which
decodes both files through their own headers and compares by repo rather than by position, so a
reordered `CATEGORIES` shows up as agreement and not as every row differing. Against the 2026-09-21
snapshot it renders all 8,856 rows and 24,010,256 stars with every one of the sixteen columns
identical on every repo, `first_seen` included -- all 7,572 of that day's stamps come back, because the
tracked ledger is copied rather than rebuilt.

`--verify` still only *fails* on a column it copies. `cat` and `targets` are derived through
`taxonomy.py` on the tree the build ran on, so they are allowed to disagree with an older snapshot, and
against the 1,294-row snapshot published on 2026-09-03 three rows did: they say "antigravity" in their
name and `\bantigravity\b` joined the Gemini/Google pattern on 2026-09-06. That is the fixture working.
The agreement above is not a weaker claim for it -- that snapshot was built by the taxonomy this tree
has -- but a future edit to `taxonomy.py` will reopen the gap, and a report on those two columns means
the tree moved, not that this file is wrong.

Not faithful, and none of it matters to a render: the crawl's full listing set is not here (the fixture
is one listing per published `(repo, list)` pair, 10,787 of them, which is what the page shows),
`snapshot` and `generated` are today rather than the published day, `d7`/`d30` are absent because
`25_velocity.py` appends those after this stage, and a listing's prose is the row's normalised blurb
rather than the README it came from.

One reconstruction is approximate and says so out loud. A listing's category is carried by its
`(source, section)` pair, and some listings name a list that has no section mapping to the category
their repo ended up in -- the repo was filed by a *different* list's vote, and the losing listing's own
section is not recoverable from the published row. Those get a synthetic section registered in
`taxonomy.SECTIONS` for the duration of the build, named `fixture-section-NNN` so it cannot match a
target pattern or the MCP/skill evidence rules. It is 113 pairs over 446 of the 10,787 listings today,
4.1%, and both counts are printed on every run; a jump means the taxonomy moved.
"""
import argparse
import importlib.util
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
DATA = ROOT / "docs" / "data.json"
OUT_DEFAULT = ROOT / "build-tmp" / "devfixture"

# Directories a fixture may never be written into. `cache/` is the dangerous one and the reason this
# list exists: a production build reads it. The rest are here because they are tracked, so a fixture
# landing in one would show up as a diff somebody has to notice, and `docs/` would be *served*.
FORBIDDEN = ("cache", "docs", "state", "mega-list", "scripts", "tests", ".github")

# `19_pages.COLS` order is read off the data file rather than assumed, so a column added upstream does
# not silently shift every field by one. These are the names this file knows how to invert.
NEEDED = ("name", "nwo", "cat", "targets", "stars", "lists", "listed_by", "os", "blurb", "install",
          "lang", "license", "pushed", "url", "img", "first_seen")


def stage():
    """Load `19_pages.py` by path, with its whole import chain, and hand back the modules.

    The generator is the thing under test, so it is loaded from disk exactly as `python
    scripts/19_pages.py` would load it -- no copy, no shim, no edited constant on disk. Importing it
    brings `17_markdown`, `16_build_all`, `taxonomy` and `newness` along with it, and those are the
    module objects whose paths get redirected later; there is only ever one of each in the process, so
    patching an attribute here is seen by every caller.
    """
    sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location("b19", SCRIPTS / "19_pages.py")
    b19 = importlib.util.module_from_spec(spec)
    sys.modules["b19"] = b19
    spec.loader.exec_module(b19)
    return b19


def destination(raw: str) -> Path:
    """The output directory, or a refusal.

    Two ways to be allowed: under `build-tmp/`, or outside the repository altogether (a scratch
    directory on another drive is a legitimate answer). Anything else is rejected by name, because the
    interesting mistake here is not a typo -- it is `--out cache` looking like a reasonable thing to
    type, and a fixture in `cache/` is indistinguishable to `weekly.yml` from a completed crawl.
    """
    out = Path(raw).expanduser().resolve()
    inside = ROOT == out or ROOT in out.parents
    if inside:
        rel = out.relative_to(ROOT)
        top = rel.parts[0] if rel.parts else ""
        if top in FORBIDDEN:
            extra = (" A real CI run reads cache/, and weekly.yml treats a file being there as the "
                     "stage having run, so a fixture in it would be published as the atlas."
                     if top == "cache" else " That directory is tracked.")
            raise SystemExit(f"devfixture: refusing to write into {top}/ -- {out}.{extra}\n"
                             f"            Pass an --out under build-tmp/, or one outside {ROOT}.")
        if top != "build-tmp":
            raise SystemExit(f"devfixture: {out} is inside the repository but not under build-tmp/. "
                             f"Use build-tmp/<name>, or a directory outside {ROOT}.")
    return out


def titles(b16) -> dict[str, str]:
    """Display name -> source key, inverting the map `listed_by` was written through.

    `repo_pool` joins `LIST_TITLE.get(source)` for each list a repo is on, so the published string is
    the only record of *which* lists those were. First key wins where two lists share a title, which
    keeps the choice deterministic; a genuine collision would show up as a short `lists` count under
    `--verify`.
    """
    out: dict[str, str] = {}
    for key, title in b16.LIST_TITLE.items():
        out.setdefault(title, key)
    return out


def sections(tax) -> dict[tuple[str, str], str]:
    """(source, category) -> a section that maps to it, so `category_of` returns that category.

    Two constraints on the choice, and the second one cost six rows before it was written down.

    `SPLIT_BY_EVIDENCE` pairs are skipped as candidates: their category depends on whether the
    listing's prose names a protocol, which is a second rule to satisfy for no gain when some other
    section of the same list maps to the category outright.

    And the section a listing carries is *also* one of the nine text fields `targets_of` searches, so
    picking "Gemini CLI" out of a list that has one puts Gemini on the row whether the repo mentions it
    or not. Which section a losing listing actually had is not in the published row, so this prefers a
    candidate that names no harness -- the neutral choice, which reproduces the published targets
    instead of adding to them. Where every candidate names one, the first still wins and `--verify`
    reports the row.
    """
    candidates: dict[tuple[str, str], list[str]] = {}
    for (src, sec), cat in tax.SECTIONS.items():
        if (src, sec) in tax.SPLIT_BY_EVIDENCE:
            continue
        candidates.setdefault((src, cat), []).append(sec)
    out: dict[tuple[str, str], str] = {}
    for (src, cat), secs in candidates.items():
        # What the list contributes on its own, so this compares the section's effect and not the
        # source's -- `SOURCE_TARGETS` puts a harness on every listing of some lists by design.
        floor = tax.targets_of({"source": src})
        out[(src, cat)] = next(
            (s for s in secs if tax.targets_of({"source": src, "section": s}) == floor), secs[0])
    return out


def reconstruct(data: dict, b19) -> dict:
    """The three cache files, plus a shot map and the synthetic sections the build has to register."""
    b16, tax = b19.b16, b19.tax
    ix = {c: i for i, c in enumerate(data["cols"])}
    missing = [c for c in NEEDED if c not in ix]
    if missing:
        raise SystemExit(f"devfixture: {DATA} has no {', '.join(missing)} column. Its `cols` header is "
                         f"{data['cols']} -- the rows are positional lists read through it, so a "
                         f"renamed column has to be renamed in NEEDED here too.")
    cats = [c["name"] for c in data["cats"]]
    tgts = [t["name"] for t in data["targets"]]
    # {"Y": "Yes", ...}: `row_for` compressed each verdict to one character and the OS columns are read
    # back out of `repo_pool`'s merged row, so they have to go back as the words the generator maps.
    verdicts = {v: k for k, v in reversed(list(b19.VERDICT.items()))}
    key_of, sec_of = titles(b16), sections(tax)

    records: list[dict] = []
    orch: list[dict] = []
    meta: dict[str, dict] = {}
    shots: dict[str, dict] = {}
    synth: dict[tuple[str, str], str] = {}
    approx = 0                       # listings that had to take a synthetic section
    unknown: Counter = Counter()

    for row in data["rows"]:
        nwo = row[ix["nwo"]]
        cat = cats[row[ix["cat"]]]
        stars = row[ix["stars"]] or 0
        # The star map is `meta.json`'s answer and nothing else's, so this is where a row's star count
        # has to go back. `nameWithOwner` is the identity `canonicalise_nwo` folds two spellings
        # through; writing the name back as itself makes that pass a no-op rather than a rename.
        meta[nwo] = {"nameWithOwner": nwo, "stargazerCount": stars}
        img = row[ix["img"]]
        if img:
            # `b17.image` prefers a captured shot over the derived card, so the 686 rows that publish
            # their own artwork need one map entry each. `og` is in `LINKABLE`, which is what lets the
            # URL through.
            shots[nwo.replace("/", "__")] = {"key": nwo.replace("/", "__"), "tier": "og",
                                             "shot_url": img}
        base = {
            "kind": "repo",
            "nwo": nwo,
            "owner": nwo.partition("/")[0],
            "repo": nwo.partition("/")[2],
            "name": row[ix["name"]],
            "url": row[ix["url"]],
            # `blurb` only, and deliberately not `description` as well. `targets_of` searches nine text
            # fields and `description` is one of them while `blurb` is not, so copying the published
            # prose into both puts targets on a row that the real build never found: six rows gained a
            # harness that way, because `repo_pool` picks the *longest* blurb across a repo's listings
            # and that text was never in any listing's `description`. The published targets travel as
            # `topics` instead, which is the one field that carries them exactly.
            "blurb": row[ix["blurb"]],
            "topics": [tgts[i] for i in row[ix["targets"]]],
            "install_cmd": row[ix["install"]],
            "language": row[ix["lang"]],
            "license": row[ix["license"]],
            "pushed_at": row[ix["pushed"]],
            "stars": stars,
        }
        for field, char in zip(b19.OS_FIELDS, row[ix["os"]]):
            base[field] = verdicts.get(char, b19.DASH)

        for label in [p for p in (row[ix["listed_by"]] or "").split(", ") if p]:
            src = key_of.get(label)
            if src is None:
                unknown[label] += 1
                continue
            sec = sec_of.get((src, cat))
            if sec is None:
                # This list has no section that maps to the category the repo was filed under, because
                # another list out-voted it and the losing listing's own section is not in the
                # published row. A synthetic pair keeps the vote unanimous and therefore keeps the
                # category. Digits only, so it cannot match a target pattern or the MCP/skill rules.
                sec = synth.setdefault((src, cat), f"fixture-section-{len(synth):03d}")
                approx += 1
            rec = dict(base, source=src, section=sec)
            if src == "orchestrators":
                # `main()` reads `r["category"]` on the orchestrators records before anything else
                # touches them, and `category_of` prefers `section`, so both carry the same string.
                rec["category"] = sec
                orch.append(rec)
            else:
                records.append(rec)

    if unknown:
        print(f"devfixture: {sum(unknown.values())} listing(s) name a list with no key in "
              f"LIST_TITLE and are dropped: {', '.join(sorted(unknown))}", flush=True)
    return {"records_all": records, "records": orch, "meta": meta, "shots": shots, "approx": approx,
            "synthetic": {(s, c): sec for (s, c), sec in synth.items()}}


def report(fx: dict, data: dict, out: Path, writing: bool) -> None:
    verb = "writes" if writing else "would write"
    listings = len(fx["records_all"]) + len(fx["records"])
    where = DATA.relative_to(ROOT) if ROOT in DATA.parents else DATA
    print(f"{where}: {len(data['rows']):,} rows · {len(data['cats'])} topics · "
          f"{len(data['targets'])} targets · snapshot {data.get('snapshot', '?')}")
    print(f"{verb} into {out}")
    print(f"  cache/records_all.json  {len(fx['records_all']):,} listings")
    print(f"  cache/records.json      {len(fx['records']):,} orchestrators listings")
    print(f"  cache/meta.json         {len(fx['meta']):,} repos, star counts written back")
    print(f"  cache/shots_all.json    {len(fx['shots']):,} rows that publish their own artwork")
    print(f"  state/first-seen.json   copy of the tracked ledger, so `newness` writes here not there")
    share = f" ({fx['approx'] / listings:.1%} of listings)" if listings else ""
    print(f"{listings:,} listings over {len(fx['meta']):,} repos · {len(fx['synthetic'])} synthetic "
          f"section(s) over {fx['approx']:,} listing(s){share} whose list cannot express the category "
          f"their repo was filed under")


def write(fx: dict, out: Path) -> None:
    cache = out / "cache"
    cache.mkdir(parents=True, exist_ok=True)
    for name, obj in (("records_all.json", fx["records_all"]), ("records.json", fx["records"]),
                      ("meta.json", fx["meta"]), ("shots_all.json", fx["shots"])):
        (cache / name).write_text(json.dumps(obj, separators=(",", ":"), ensure_ascii=False),
                                  encoding="utf-8")
    state = out / "state"
    state.mkdir(parents=True, exist_ok=True)
    ledger = ROOT / "state" / "first-seen.json"
    # The real ledger, copied. It already dates every published repo, so `resolve` finds nothing new,
    # stamps nothing, saves nothing and leaves `first_seen` empty on every row -- which is what the
    # published rows say. A blank ledger would instead date all 1,294 to today and mark the whole
    # atlas New for a fortnight.
    # With no ledger to copy, none is written either: `resolve` sees an absent file, takes its
    # bootstrap branch -- baseline today, every repo dated to it, nothing reported New -- and saves it
    # here. Inventing a blank one would skip that branch and mark the whole atlas New instead.
    if ledger.exists():
        shutil.copyfile(ledger, state / "first-seen.json")


def build(fx: dict, out: Path, b19) -> Path:
    """Run the real `19_pages.main()` with every path it touches pointed into the fixture."""
    cache, docs = out / "cache", out / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    b19.CACHE = cache
    b19.b17.CACHE = cache          # `cached()` reads the shot maps through this one
    b19.OUT = docs
    b19.newness.PATH = out / "state" / "first-seen.json"
    b19.tax.SECTIONS.update({(src, sec): cat for (src, cat), sec in fx["synthetic"].items()})
    b19.main()
    return docs / "data.json"


def decode(data: dict) -> dict[str, dict]:
    """A data.json as {nwo: {column: value}}, with the two index columns resolved to names.

    Both sides of a comparison go through their own header, so a reordered `CATEGORIES` or an added
    column is not mistaken for 1,294 changed rows.
    """
    ix = {c: i for i, c in enumerate(data["cols"])}
    cats = [c["name"] for c in data["cats"]]
    tgts = [t["name"] for t in data["targets"]]
    out = {}
    for row in data["rows"]:
        rec = {c: row[i] for c, i in ix.items()}
        rec["cat"] = cats[rec["cat"]]
        rec["targets"] = sorted(tgts[i] for i in rec["targets"])
        out[rec["nwo"]] = rec
    return out


# The two columns a build is allowed to disagree with the published snapshot about, because both are
# derived through `taxonomy.py` on the tree the build ran on rather than copied out of the row. That is
# the point of the fixture -- it renders what this checkout thinks, not what the snapshot thought -- so
# drift here is reported and does not fail. Nothing drifts against the 2026-09-21 snapshot, because the
# taxonomy that built it is the one in this tree; against the 1,294-row 2026-09-03 snapshot three rows
# did, all of them repos with "antigravity" in the name, a pattern that arrived on 2026-09-06. Every
# other column is carried through verbatim, so a difference in one is a defect in this file and fails
# the run.
DERIVED = ("cat", "targets")


def verify(built_path: Path) -> int:
    """Diff the rendered data against the published one. Returns 0, or 1 if a copied column moved."""
    pub, got = decode(json.loads(DATA.read_text(encoding="utf-8"))), \
        decode(json.loads(built_path.read_text(encoding="utf-8")))
    if not pub or not got:
        print(f"\nverify: nothing to compare -- {len(pub):,} published rows, {len(got):,} rendered")
        return 1
    shared = sorted(set(next(iter(pub.values())).keys()) & set(next(iter(got.values())).keys()))
    only_pub, only_got = sorted(set(pub) - set(got)), sorted(set(got) - set(pub))
    print(f"\nverify: {len(got):,} rendered rows vs {len(pub):,} published, comparing "
          f"{len(shared)} shared columns by repo")
    if only_pub or only_got:
        print(f"  {len(only_pub)} published row(s) missing" +
              (f" ({', '.join(only_pub[:3])}…)" if only_pub else "") +
              f", {len(only_got)} extra" + (f" ({', '.join(only_got[:3])}…)" if only_got else ""))
    bad = 0
    for col in shared:
        diff = [n for n in pub.keys() & got.keys() if pub[n][col] != got[n][col]]
        if not diff:
            continue
        derived = col in DERIVED
        bad += 0 if derived else 1
        n = sorted(diff)[0]
        why = "derived through taxonomy.py, so this is the tree disagreeing with the snapshot" \
            if derived else "copied from the published row, so this is a fixture defect"
        print(f"  {col:11s} {len(diff):5,} differ · {why}\n"
              f"              e.g. {n}: published {pub[n][col]!r} vs rendered {got[n][col]!r}")
    if not bad and not only_pub and not only_got:
        print("  every copied column agrees on every repo")
    return bad or bool(only_pub or only_got)


def main() -> None:
    global DATA
    ap = argparse.ArgumentParser(
        description="Rebuild 19_pages.py's cache inputs from docs/data.json, under build-tmp/.")
    ap.add_argument("--out", default=str(OUT_DEFAULT),
                    help=f"fixture directory (default {OUT_DEFAULT.relative_to(ROOT)}); must be under "
                         f"build-tmp/ or outside the repository, and never cache/")
    ap.add_argument("--data", default=str(DATA), help=f"published rows to invert (default {DATA})")
    ap.add_argument("--write", action="store_true",
                    help="actually write the fixture. Without it this reports and exits.")
    ap.add_argument("--build", action="store_true",
                    help="run 19_pages.main() against the fixture afterwards. Implies --write.")
    ap.add_argument("--verify", action="store_true",
                    help="after --build, diff the rendered data.json against the published one.")
    args = ap.parse_args()

    DATA = Path(args.data).expanduser().resolve()
    out = destination(args.out)
    writing = args.write or args.build
    data = json.loads(DATA.read_text(encoding="utf-8"))

    b19 = stage()
    fx = reconstruct(data, b19)
    report(fx, data, out, writing)
    if not writing:
        print("\nnothing written. Add --write to write the fixture, or --build to render the index.")
        return
    write(fx, out)
    if not args.build:
        print(f"\nwritten. Render with: python scripts/devfixture.py --build --out {out}")
        return
    print()
    built = build(fx, out, b19)
    # `catalog/`, which is where `19_pages.main()` writes since the site grew a homepage. Printed as the real
    # path rather than the directory, because the next thing anyone does with this line is open it.
    print(f"\nrendered {out / 'docs' / 'catalog' / 'index.html'}")
    if args.verify and verify(built):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
