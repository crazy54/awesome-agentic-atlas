// `scripts/22_detail.py` must write the same 1,294 bytes-for-bytes on a day when nobody re-curated
// anything. This is the harness for the one property that whole stage is designed around, and until now
// nothing enforced it.
//
// Why it matters more than it sounds: Pages here is a `build_type: legacy` deployment, so `docs/` is
// committed verbatim and every byte the generator emits is a byte git keeps for ever, in a repository whose
// `.git` is already ~110 MB. The stage's own docstring explains the design at length -- no star count, no
// push date, no snapshot date and no ordering derived from any of them, so that the output is a pure
// function of the parts of `data.json` that only move when a source list changes. The daily cron rebuilds
// and commits. If one volatile string ever leaks into a template, the cost is not a wrong page: it is
// 1,294 files rewritten and committed every single day, and by the time anybody looks at the repository
// size the history cannot be undone. A `datetime.now()` in a footer would do it, and would look completely
// harmless in review.
//
// WHAT THIS HARNESS CANNOT SEE: whether the pages are any good. It never opens one. Nothing here checks a
// link resolves, that the platform table says what the data says, or that the HTML parses -- it compares
// hashes of trees. It also cannot see churn that comes from anywhere other than this stage: `20_landing.py`
// deliberately does embed star counts and rewrites 156 facet pages on every run, which is a known and
// accepted cost and is not what this measures.
//
//   node tests/detail-churn.mjs
//
// Four generations of the whole tree, ~4s each on this machine, into scratch directories under `$AAA_TMP`
// (default the OS temp dir). Nothing is written inside the repository: `--out` exists on that stage
// precisely so its drift can be measured without touching the committed tree.
import {createHash} from "node:crypto";
import {spawnSync} from "node:child_process";
import {mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, statSync, writeFileSync} from "node:fs";
import {tmpdir} from "node:os";
import {fileURLToPath} from "node:url";
import {join, relative, sep} from "node:path";
import {findPython, pythonsTried} from "./lib/python.mjs";

const ROOT = fileURLToPath(new URL("..", import.meta.url));
const STAGE = join(ROOT, "scripts", "22_detail.py");
const DATA = join(ROOT, "docs", "data.json");

let pass = 0, fail = 0;
const ok = (n, c, extra = "") => { c ? pass++ : (fail++, console.log("FAIL " + n + (extra ? "  -- " + extra : ""))); };

// One copy of the interpreter search, in `lib/python.mjs`, because `run.mjs` needs the same answer for
// `pagemin_test.py` and two copies of a search order are two things to keep in step. The reason it is a
// search at all, and the reason a missing interpreter is a *failure* here rather than a skip, are both
// written down there.
const python = findPython();
if (!python) {
  console.log("FAIL no python 3 on PATH -- tried " + pythonsTried().join(", ") + "; set $PYTHON, or " +
              "install one. scripts/22_detail.py is the thing under test and it is a python script, so " +
              "this harness cannot be run without one and must not pretend it passed");
  console.log("\n0 passed, 1 failed");
  process.exit(1);
}

const scratch = mkdtempSync(join(process.env.AAA_TMP || tmpdir(), "aaa-churn-"));
process.on("exit", () => { try { rmSync(scratch, {recursive: true, force: true}); } catch {} });

/** Generate the whole detail tree into a scratch directory and return where it went. */
const generate = (tag, dataFile) => {
  const out = join(scratch, tag);
  mkdirSync(out, {recursive: true});
  // `PYTHONIOENCODING`, because the stage prints a `·` in its summary and the default stdout encoding on a
  // Windows pipe is cp1252, which cannot encode it. That would fail the generation for a reason that has
  // nothing to do with the pages.
  const r = spawnSync(python, [STAGE, "--out", out, "--data", dataFile],
    {encoding: "utf8", env: {...process.env, PYTHONIOENCODING: "utf-8"}});
  if (r.status !== 0)
    throw new Error(`22_detail.py exited ${r.status} generating ${tag}:\n${r.stderr || r.stdout}`);
  return out;
};

/** Every file the stage owns under `dir`, relative path -> sha256. */
const fingerprint = (dir) => {
  const seen = new Map();
  const walk = (d) => {
    for (const e of readdirSync(d, {withFileTypes: true})) {
      const full = join(d, e.name);
      if (e.isDirectory()) walk(full);
      // Forward slashes, so a tree hashed on Windows can be compared with one hashed anywhere else.
      else seen.set(relative(dir, full).split(sep).join("/"),
                    createHash("sha256").update(readFileSync(full)).digest("hex"));
    }
  };
  walk(join(dir, "repo"));
  const sitemap = join(dir, "sitemap-repos.xml");
  try {
    statSync(sitemap);
    seen.set("sitemap-repos.xml", createHash("sha256").update(readFileSync(sitemap)).digest("hex"));
  } catch { /* reported by the count assertion */ }
  return seen;
};

/** The files that differ between two fingerprints, and how. Ordered, and capped when it is reported. */
const diff = (a, b) => {
  const out = [];
  for (const [k, v] of a) {
    if (!b.has(k)) out.push(`only in the first: ${k}`);
    else if (b.get(k) !== v) out.push(`differs: ${k}`);
  }
  for (const k of b.keys()) if (!a.has(k)) out.push(`only in the second: ${k}`);
  return out.sort();
};
const say = (list, n = 4) =>
  `${list.length} file(s)` + (list.length ? ": " + list.slice(0, n).join(", ") +
   (list.length > n ? `, +${list.length - n} more` : "") : "");

const data = JSON.parse(readFileSync(DATA, "utf8"));
const col = (name) => {
  const i = data.cols.indexOf(name);
  if (i < 0) throw new Error(`data.json has no ${name} column -- cols are ${data.cols.join(", ")}`);
  return i;
};

// ---- run A: the committed data, exactly as it stands
const A = generate("a", DATA);
const fpA = fingerprint(A);
const pages = [...fpA.keys()].filter(k => k.endsWith("index.html")).length;
// One page per repository plus the directory that makes them reachable. Asserted so that none of the
// comparisons below can pass by comparing two empty trees, which is the way a check like this rots.
ok("the stage wrote one page per repository, plus the directory",
   pages === data.rows.length + 1, `${pages} pages for ${data.rows.length} rows`);
ok("...and the shared shell and the sitemap beside them",
   ["repo/detail.css", "repo/detail.js", "sitemap-repos.xml"].every(f => fpA.has(f)),
   [...fpA.keys()].filter(k => !k.endsWith("index.html")).join(", "));

// ---- run B: the same data again. Determinism, full stop.
//
// This is the one that catches a timestamp, a `set` iteration order, a `dict` whose keys arrive in hash
// order, or an `id()` leaking into an anchor. Deliberately run with whatever `PYTHONHASHSEED` the
// environment has rather than pinning it: a pinned seed would make an ordering bug reproducible and
// invisible, which is the wrong half of the trade.
const fpB = fingerprint(generate("b", DATA));
const ab = diff(fpA, fpB);
ok("two runs over identical data write identical bytes", ab.length === 0, say(ab));

// ---- run C: the data as the daily cron changes it, which is the property that matters
//
// Exactly the fields that move on a day when nobody touched a source list: every star count, every push
// date, and the two snapshot stamps in the header. Not `first_seen`, which only changes when a repository
// is genuinely new, and not `listed_by`, `cat`, `targets`, `os`, `blurb` or `install`, which are the
// curation -- those SHOULD move the pages, and run D below is what proves they still do.
const stars = col("stars"), pushed = col("pushed");
const churned = structuredClone(data);
churned.snapshot = "2099-12-31";
churned.baseline = "2099-12-31";
for (const row of churned.rows) {
  row[stars] = (row[stars] || 0) + 91_337;
  if (row[pushed]) row[pushed] = "2099-12-30";
}
const churnedFile = join(scratch, "data-churned.json");
writeFileSync(churnedFile, JSON.stringify(churned), "utf8");
const ac = diff(fpA, fingerprint(generate("c", churnedFile)));
ok("a day on which only stars, push dates and the snapshot moved rewrites nothing at all",
   ac.length === 0, say(ac));

// ---- run D: and the comparison is not comparing nothing
//
// A blurb is curation: it is this project's own writing about somebody else's repository, it changes only
// when a human changes it, and it is rendered into the page. So changing one MUST move that page's bytes.
// Without this, every assertion above would still pass if `render()` started returning a constant.
const blurb = col("blurb");
const victim = data.rows[0];
const edited = structuredClone(data);
edited.rows[0][blurb] = "A blurb nobody wrote, inserted by tests/detail-churn.mjs.";
const editedFile = join(scratch, "data-edited.json");
writeFileSync(editedFile, JSON.stringify(edited), "utf8");
const ad = diff(fpA, fingerprint(generate("d", editedFile)));
// The page for the repository whose blurb moved, by the path the stage's own `segment()` builds: lowercased,
// a leading dot rewritten. Only the lowercasing matters for `rows[0]`, but both are here so the assertion
// does not become wrong the day row 0 is a dot-repository.
const victimPage = "repo/" + victim[col("nwo")].toLowerCase().split("/")
  .map(s => (s.startsWith(".") ? "dot-" + s.slice(1) : s)).join("/") + "/index.html";
ok("editing one curated blurb moves the page it belongs to", ad.includes(`differs: ${victimPage}`),
   `${victimPage} not among ${say(ad, 6)}`);
// It moves more than that one, and that is correct rather than a bug: a blurb is printed again in the
// "related projects" section of every page that lists this repository as kin. What would be a bug is all
// 1,295, which is what a template that had gone volatile would look like -- so the bound is asserted, and
// generously, because how many pages call a given repository kin is a property of the curation.
ok("...and not the whole tree, which is what a volatile template would look like",
   ad.length < fpA.size / 4, `${ad.length} of ${fpA.size}`);

// ---- and the committed tree is what this generator produces from the committed data
//
// A different property from the three above, and worth having for the same reason they are: `docs/` is
// served verbatim, so a tree that no longer matches its generator is a site serving pages nobody can
// reproduce -- and the next rebuild commits all 1,294 of them at once. Green means the checkout is
// consistent. Red has three honest causes, in order of likelihood: `22_detail.py` changed and `docs/` was
// not rebuilt; `19_pages.py` changed, which this stage imports for `SITE` and `REPO` and which therefore
// reaches into every canonical URL on every page; or `docs/data.json` was regenerated without this stage
// being re-run after it. In all three the fix is `python scripts/22_detail.py`.
const committed = fingerprint(join(ROOT, "docs"));
const ac2 = diff(fpA, committed);
ok("the committed docs/repo is byte-identical to a fresh regeneration", ac2.length === 0,
   say(ac2) + " -- run: python scripts/22_detail.py");

const bytes = [...fpA.keys()].length;
console.log(`\n${bytes.toLocaleString()} generated files compared across 4 runs of 22_detail.py`);
console.log(`${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
