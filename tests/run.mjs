// The whole verification suite, in one command:
//
//   node tests/run.mjs
//
// It finds a Chromium, serves `docs/` on a port the OS picks, runs the twenty-one harnesses in turn, and prints
// what each one asserted and what the total was. It exits non-zero if anything failed, and it cleans up the
// server, every browser any harness started and every scratch directory on the way out -- including when a
// harness threw, including when it was interrupted.
//
// WHY NINETEEN HARNESSES AND NOT ONE, which is the question anybody reading this directory will ask first:
//
//   theme_test.py     verifies both palettes' contrast and the copies used by generated surfaces, and
//                     the one channel on the page that is not colour: the five platform verdict marks,
//                     which three places in 19_pages.py describe with no generator keeping them in step.
//                     It also holds the phone's above-the-fold budget and the comparison panel's layout,
//                     both of which belong in cards-check.mjs and cannot go there yet -- see the note in
//                     each of those sections. All three are here for the same reason: a rule added to the
//                     generator today is absent from the docs/ the browser harnesses are served, so the
//                     subject of a drift check is the generator.
//   signals_test.py   the cache-staleness policy in scripts/signals.py, on fabricated entries. Pure and
//                     instant, and the only test of it that can exist offline -- the three stages it
//                     serves all shell out to `gh api graphql`, so nothing here sees a real crawl.
//   newness_test.py   the cohort model in scripts/newness.py: that `New` is the most recent import that
//                     brought anything, that the next one to bring anything takes the mark off the last,
//                     and that an import bringing nothing moves neither. Pure, and the only harness that
//                     can see it -- a cohort is correct only in relation to the one before it, so every
//                     assertion here needs two or more imports in sequence with the date supplied rather
//                     than read from the clock. Four surfaces render this one rule.
//   discover_test.py  the rule behind `docs/discover/`: fifty projects a day for seven days, every category
//                     represented in every one of them, no project twice in a day and best-effort no project
//                     twice in a week, and the rotation ledger that decides whose turn it is next. Pure and
//                     instant, and the only harness that can see any of it -- every assertion needs a corpus
//                     of a stated shape and a date supplied rather than read from the clock, and the
//                     interesting ones need several weeks dealt in sequence, because fairness is a claim
//                     about how long a category takes to come round and not about any one day. It also holds
//                     the two things that have no other witness: that a plan which has run out cycles
//                     through its seven cohorts rather than freezing on the last one, and that the stage is
//                     wired into both workflows -- weekly-only would freeze the page for six nights in seven
//                     with no error anywhere.
//   probe.mjs         runs the page's own JavaScript against a stub DOM, and reads the stylesheet and the
//                     page text. Sees every branch of the ranking, the hash and the palette. Cannot see
//                     computed layout -- there is none in Node.
//   cards-check.mjs   measures real layout in a real browser at three widths in both themes. Cannot see a
//                     prefixed property this browser has an unprefixed implementation of.
//   pwa-check.mjs     manifest, service worker, precache, offline, and a 404 that must not be cached.
//                     Needs an origin, so it cannot be done from a file:// page at all.
//   dance-check.mjs   "Dance with me": Chrome's fake microphone plays a 120 BPM WAV the harness writes, and
//                     the page's beat detector has to find the kicks, the tempo and the silence. Cannot see
//                     a shared tab's audio, which needs a picker headless Chrome does not draw.
//   detail-churn.mjs  regenerates 1,294 detail pages and compares hashes. Nothing to do with a browser.
//   detail-preview-check.mjs
//                     opens one detail page against deterministic GitHub API fixtures and verifies the
//                     rendered/source switch, file discovery, sanitising, fonts, colours and phone layout.
//   pagemin_test.py   the comment stripper against the cases the real page does not contain -- template
//                     literals, regex literals, unterminated blocks. Python, because the stripper is.
//   media_test.py     the workbook writer: one embedded part per screenshot however many rows point at it,
//                     and the 65,535-entry ZIP ceiling that dedup exists to stay under. Also that an
//                     image the pool never saw is allowed rather than a fault -- the cover branding is
//                     two of them -- which this file asserted the opposite of until a weekly died on it.
//   indexnow_test.py  which of the ~1,500 files under docs/ get submitted to a search engine, that the
//                     key-file prune deletes a rotated key and nothing else, and that a truncated HTTP
//                     response is a warning rather than a traceback. Touches no network, by a guard it
//                     asserts on rather than by convention.
//   refresh_test.py   the staleness guard in scripts/19b_refresh.py: that the only cache-free render path
//                     refuses when the checkout's source lists and the committed rows disagree about how
//                     many there are, on a disagreement this file constructs rather than waits for.
//   collections_test.py
//                     the five curated collections: that every pick is still in the atlas, that a page
//                     claiming stated Windows support still has seven stated verdicts under it, and that
//                     each refusal fires -- on a curation the file mutates, because the committed one
//                     passes, and a guard nobody has seen fire is a guard nobody should trust. Also that
//                     a workflow runs the stage at all, which for every commit from 18d373a to this one
//                     none did: the thirteen pages were published once and then frozen, and every other
//                     assertion in that file was reading a file no build could rewrite.
//   deeplinks_test.py the links into the catalogue since it moved to catalog/: the homepage's forwarder, run
//                     under node against a stub location, and every generator's filtered link resolved
//                     against the page that carries it. Also the site's host, which is read from
//                     docs/CNAME, and the feed ids that must not follow it.
//   osicons_test.py   the five platform marks that replaced the words Windows, WSL2, macOS, Linux and
//                     Docker. Mostly one assertion, walked over every built page: that every
//                     `<use href="#...">` resolves to a `<symbol>` in that same document. A `<use>` with
//                     no symbol renders nothing at all -- not a broken glyph, an empty box the size the
//                     mark would have been -- so a page that lost its sprite publishes five invisible
//                     verdicts per row and reads as a slightly airy layout. Nothing else in this suite
//                     can see that, and a sample cannot either: the failure is per-document.
//   semantic_test.py  the semantic index in docs/search/, scored using only the six files a reader downloads:
//                     no numpy, no model, no build stage imported. Reimplements the browser's half in the
//                     standard library, so what it asserts on is the code a visitor actually runs. Carries the
//                     staleness guard -- vectors are addressed by row ordinal, so an index built against a
//                     different data.json returns each project's neighbour with no error anywhere -- and the
//                     retrieval cases themselves, scored on what a reader sees: of the ten rows each query
//                     returns, how many name the topic it asked about, totalled across eight queries. Not on a
//                     similarity, and no longer on one fixture repository's rank either -- the corpus grew from
//                     1,294 rows to 8,856 and a rank turned into a measure of how crowded one project's
//                     neighbourhood is, which reddened three groups here on a build that had got better at
//                     every query. Every statistic in this file is now relative to what the corpus makes
//                     available, because a fixed one silently tightens as the corpus grows. It also asserts
//                     that a question with no topic in it --
//                     "please help me choose" -- produces no tokens and therefore no answer, and that
//                     chatter wrapped around a real topic still keeps the topic.
//                     Tokeniser parity is split across two harnesses on purpose: the algorithm exists three
//                     times, once per language, and there is nothing to import. The build stage writes its
//                     own segmentation of eight strings into meta.json, this file checks its transcription
//                     against them, and probe.mjs checks the page's -- which is the copy a reader runs.
//                     The newest group is the map: xy.bin holds two int16 per row, the coordinates the
//                     constellation is drawn from, and every check on its shape can pass over a random
//                     scatter. So it is scored against the one label the layout never saw -- of the eight
//                     rows nearest a project on screen, how many share its curated cat -- and required to
//                     close a fifth of the gap between what two rows drawn at random would share and 1.0.
//                     The share of that gap, not a multiple of chance: a multiple sounds relative and is not,
//                     because chance rises as the corpus concentrates. One import took the largest category
//                     from 21% of rows to 51%, chance from 11.7% to 29.0%, and a 5x floor from comfortable to
//                     arithmetically out of reach with nothing about the layout changed.
//                     Drift there is the one failure in this feature with no symptom at all: nothing throws,
//                     a full page comes back, and it is ranked by noise.
//   live_test.py      the star/push sidecar the 1,294 detail pages read in place of data.json: that its keys
//                     and the pages are the same set in both directions, that it resolves its three columns
//                     by name rather than by position -- a later stage appends columns -- and that its
//                     serialisation is byte-stable, which is what lets it be committed at all.
//
// A HARNESS THAT SKIPS MUST NOT BE ABLE TO PASS, which is why there is no branch anywhere below that quietly
// carries on. A missing browser or a missing interpreter exits 2 before anything runs; a harness that prints
// no tally, or a tally of zero, is counted as a failure however it exited; and each one carries a floor on
// the number of assertions it is expected to make. The floor is a floor and not a pin -- adding assertions
// costs nothing and never trips it -- but a harness that silently stops asserting half of what it used to,
// which is exactly what happened to `pagemin_test.py` when a fixture path moved out from under it, goes red
// here instead of going quiet. From outside, a suite that checked nothing and a suite that checked everything
// produce the same exit code, and the exit code is all CI reads.
//
// The overlap between the first two is the reason to keep them apart rather than the reason to merge them.
// The cards view clamps a blurb with `-webkit-line-clamp`, which needs `display:-webkit-box` beside it or it
// does nothing. This Chrome implements the standard `line-clamp` instead, so the browser harness passes a
// rule that is silently inert in Firefox; and the stub-DOM harness, which does read the rule, has no idea
// whether four lines is what a reader actually gets. Either one alone signs off a broken clamp. They are
// separate files because they are separate instruments.
//
// NO DEPENDENCIES, and that is a deliberate constraint rather than an accident of not getting round to it.
// Node's standard library has a `WebSocket` and a `fetch`, which is all CDP needs, and `node:http` is all a
// static server needs. This site has no build step and nothing from npm is ever served to a reader; a
// devDependency here would be the first `package.json` in the repository, would need a lockfile, would need
// renovating, and would make "can I run the tests" a question with a network answer. The cost is that these
// twenty-one files own their own plumbing. It is 200 lines of plumbing.
import {mkdtempSync, rmSync, existsSync, mkdirSync} from "node:fs";
import {spawn} from "node:child_process";
import {tmpdir} from "node:os";
import {fileURLToPath} from "node:url";
import {join} from "node:path";
import {find, searched, sweep} from "./lib/browser.mjs";
import {findPython, pythonsTried} from "./lib/python.mjs";
import {serve} from "./lib/serve.mjs";

const ROOT = fileURLToPath(new URL("..", import.meta.url));
const HERE = fileURLToPath(new URL(".", import.meta.url));
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Order is cheapest first, so a typo in the page fails in two seconds rather than after a minute of browser
// work. `needs: "browser"` gets the binary and the origin as arguments; `python: true` is run by the
// interpreter instead of by node. `floor` is the number of assertions below which the harness is presumed
// broken rather than passing -- see the note at the top, and set generously below the real count so that
// only a harness that has lost assertions trips it.
const HARNESSES = [
  {file: "app_flags_test.py", label: "the 0/1 schema, atomic editor writes, and every kill switch", python: true, floor: 28},
  {file: "theme_test.py", label: "eight token sets in four copies, the theme menu, the verdict marks, the phone's fold, the compare panel", python: true, floor: 500},
  {file: "signals_test.py", label: "when a cached release/action signal needs re-querying", python: true, floor: 170},
  {file: "indexnow_test.py", label: "which URLs are submitted, the key prune, a truncated response", python: true, floor: 100},
  {file: "newness_test.py", label: "what `New` means: one cohort, superseded by the next import that brings anything", python: true, floor: 45},
  {file: "discover_test.py", label: "fifty a day for seven days, every category in each, and the queue that rotates them", python: true, floor: 75},
  {file: "probe.mjs", label: "the page script under a stub DOM, and the page as text", floor: 140},
  {file: "pagemin_test.py", label: "the comment stripper, on the cases the page lacks", python: true, floor: 40},
  {file: "media_test.py", label: "one embedded part per screenshot, the entry ceiling, and the unpooled cover", python: true, floor: 45},
  {file: "workbook_branding_test.py", label: "the Atlas mark and mascot on both workbook covers, saved as a weekly saves them", python: true, floor: 24},
  {file: "refresh_test.py", label: "the cache-free render, refused when the source count moved", python: true, floor: 60},
  {file: "live_test.py", label: "the star/push sidecar the 1,294 detail pages read", python: true, floor: 90},
  {file: "semantic_test.py", label: "the semantic index, scored from the bytes a reader downloads", python: true, floor: 30},
  {file: "collections_test.py", label: "the curated picks, and every refusal that keeps them honest", python: true, floor: 500},
  {file: "deeplinks_test.py", label: "the homepage forwarder, every filtered link resolving into catalog/, and the host in docs/CNAME", python: true, floor: 34},
  {file: "osicons_test.py", label: "the five platform marks, and that every one of them resolves", python: true, floor: 200},
  {file: "detail-churn.mjs", label: "1,294 detail pages, regenerated and hashed", floor: 7},
  {file: "detail-preview-check.mjs", label: "rendered repository reader, source and phone layout", needs: "browser", floor: 12},
  {file: "cards-check.mjs", label: "real layout at 1440/900/375 in both themes", needs: "browser", floor: 86},
  {file: "pwa-check.mjs", label: "manifest, worker, precache, offline, freshness, 404", needs: "browser", floor: 25},
  {file: "dance-check.mjs", label: "Dance with me: the beat detector against a known tempo", needs: "browser", floor: 30},
];

// Both entry points, because the site has two and either one missing is a different broken build:
// `index.html` is the shelves homepage from `31_home.py`, `catalog/index.html` the catalogue from
// `19_pages.py`. Two checks rather than one, so the message can name the stage that did not run.
for (const [rel, stage] of [[["docs", "index.html"], "scripts/31_home.py"],
                            [["docs", "catalog", "index.html"], "scripts/19_pages.py"]]) {
  if (existsSync(join(ROOT, ...rel))) continue;
  console.error(`${rel.join("/")} is not here. This suite asserts on the built site, and the built site is ` +
                "committed -- so this is either the wrong directory, a checkout with docs/ removed, or a " +
                `tree where ${stage} has not run.`);
  process.exit(2);
}

const bin = find();
if (!bin) {
  console.error(
    "No Chromium found, and five of the twenty-one harnesses drive one over CDP.\n\n" +
    "Looked in, in this order:\n" +
    "  $CHROME_PATH, $CHROMIUM_PATH, $PLAYWRIGHT_CHROMIUM\n" +
    searched().map((p) => "  " + p).join("\n") + "\n\n" +
    "Fixes, cheapest first:\n" +
    "  CHROME_PATH=/path/to/chrome node tests/run.mjs\n" +
    "  python -m playwright install chromium --with-deps\n\n" +
    "This search order is scripts/chrome.py's, which the screenshot stages already use -- so a machine " +
    "that can build this site can run these tests. Nothing here installs a browser.");
  process.exit(2);
}

// Checked here rather than inside the two harnesses that need it, for the same reason the browser is: a
// prerequisite that goes missing must stop the run, not reduce it. Sixteen of the twenty-one need it -- one runs
// `22_detail.py` 1,294 pages at a time, one tests `pagemin.py`, one builds a workbook and counts the ZIP
// entries it holds, one decides which repos a crawl would ask about, one drives the IndexNow client and
// `20_landing.py`'s key-file prune, one guards the cache-free render path, one builds the star/push sidecar,
// one reads every built page looking for a platform mark that resolves to nothing, one re-derives the
// semantic index's arithmetic from the committed bytes -- and between them they are most of the assertions
// below, comfortably over half.
const python = findPython();
if (!python) {
  console.error(
    "No Python 3 found, and sixteen of the twenty-one harnesses are Python or drive it.\n\n" +
    "Tried: " + pythonsTried().join(", ") + "\n\n" +
    "Fixes:\n" +
    "  PYTHON=/path/to/python node tests/run.mjs\n" +
    "  install Python 3 -- this repository's whole generator is Python, so a checkout that cannot run it\n" +
    "  cannot rebuild the site either.\n\n" +
    "Nothing here is skipped when it is missing: a suite that goes quiet reports the same exit code as a " +
    "suite that checked everything.");
  process.exit(2);
}

// One scratch root for the whole run, with every browser profile and every generated tree underneath it.
// That is what makes cleanup a single removal instead of four harnesses each remembering to tidy up: see
// the `finally` at the bottom, which runs on a thrown exception and on Ctrl-C as well as on success.
const scratch = mkdtempSync(join(tmpdir(), "aaa-tests-"));
// Screenshots and other keepable output. `build-tmp/` because it is already gitignored and is already where
// this project's throwaway build output goes; `tests/` is tracked, and 1.5 MB of PNG per run is not a thing
// to commit.
const artifacts = join(ROOT, "build-tmp");
mkdirSync(artifacts, {recursive: true});

let server, current = null, interrupted = false;
const results = [];

const cleanup = async () => {
  if (server) { await server.close(); server = null; }
  // The backstop. A harness that died on an uncaught exception still runs its own `process.on("exit")`
  // hook and kills its browser; one that was killed outright does not, so anything still holding a pid
  // file under the scratch root is killed here before the root is removed.
  const killed = sweep(scratch);
  if (killed.length) console.log(`swept ${killed.length} browser process(es) a harness left behind`);
  // Retried, because a browser that has just been killed can hold its own profile open for a moment and a
  // single removal loses that race about half the time on Windows.
  for (let i = 0; i < 15; i++) {
    try { rmSync(scratch, {recursive: true, force: true}); return; } catch { await sleep(200); }
  }
  console.log(`could not remove ${scratch} -- it is in the OS temp directory and is safe to delete`);
};

for (const sig of ["SIGINT", "SIGTERM"]) process.on(sig, async () => {
  interrupted = true;
  if (current) current.kill();
  await cleanup();
  process.exit(130);
});

const run = (h, args, env) => new Promise((resolve) => {
  const started = Date.now();
  // `PYTHONIOENCODING` for the same reason `detail-churn.mjs` sets it: the stages print a `·` and the
  // default encoding on a Windows pipe is cp1252, which cannot encode it. A test that dies on its own
  // summary line is a confusing way to learn about a code page.
  const child = spawn(h.python ? python : process.execPath, [join(HERE, h.file), ...args],
    {cwd: ROOT, env: {...process.env, PYTHONIOENCODING: "utf-8", ...env}, stdio: ["ignore", "pipe", "pipe"]});
  current = child;
  // Streamed and buffered at once: streamed so a harness that hangs still shows what it got through, and
  // buffered so the tally can be read back off the end of it.
  let out = "";
  const tap = (from, to) => from.on("data", (b) => { out += b; to.write(b); });
  tap(child.stdout, process.stdout);
  tap(child.stderr, process.stderr);
  child.on("error", (e) => { out += "\nfailed to start: " + e.message; });
  child.on("close", (code) => {
    current = null;
    resolve({code, out, ms: Date.now() - started});
  });
});

let exit = 0;
try {
  server = await serve(join(ROOT, "docs"));
  console.log(`browser   ${bin}`);
  console.log(`serving   docs/ at ${server.origin}`);
  console.log(`scratch   ${scratch}`);
  console.log(`artifacts ${artifacts}`);

  for (const h of HARNESSES) {
    if (interrupted) break;
    console.log(`\n── ${h.file}  ·  ${h.label} ` + "─".repeat(
      Math.max(3, 96 - h.file.length - h.label.length)));
    const args = h.needs === "browser" ? [bin, server.origin] : [];
    const {code, out, ms} = await run(h, args, {AAA_TMP: scratch, AAA_ARTIFACTS: artifacts});
    // The tally is the last one printed, because a harness may print others in passing. A harness that
    // crashed before printing one counts as failed with no assertions, which is louder than reporting it as
    // zero of zero.
    const tallies = [...out.matchAll(/(\d[\d,]*) passed, (\d[\d,]*) failed/g)];
    const last = tallies[tallies.length - 1];
    const n = (s) => Number(String(s).replace(/,/g, ""));
    const passed = last ? n(last[1]) : 0, failed = last ? n(last[2]) : null;
    // The exit code is not the only authority, and this is the whole reason the three tests below exist. A
    // harness whose assertions stopped running -- a fixture that moved, a guard that took its else branch,
    // an early `return` -- exits 0 and prints a tally that is merely smaller than it was. Nothing about that
    // is visible from outside, so it is caught here: no tally, an empty tally, or fewer assertions than the
    // file is known to contain are each a failure of the run regardless of what the child thought.
    let quiet = null;
    if (last === undefined) quiet = `printed no tally at all, and exited ${code}`;
    else if (passed + failed === 0) quiet = "ran and asserted nothing";
    else if (h.floor && passed + failed < h.floor)
      quiet = `made ${passed + failed} assertions, fewer than the ${h.floor} this file is known to ` +
              "contain -- something stopped asserting rather than started failing";
    if (quiet) console.log(`\n${h.file} ${quiet}`);
    results.push({file: h.file, ms, code, passed, failed, quiet});
    if (code !== 0 || quiet) exit = 1;
  }
} catch (err) {
  console.error("\nthe run itself failed, before any harness could report:\n" + (err.stack || err));
  exit = 1;
} finally {
  await cleanup();
}

const width = Math.max(...HARNESSES.map((h) => h.file.length));
console.log("\n── total " + "─".repeat(60));
let passed = 0, failed = 0;
for (const r of results) {
  passed += r.passed;
  failed += r.failed ?? 0;
  const tally = r.failed === null
    ? `no tally printed -- exited ${r.code}`
    : `${String(r.passed).padStart(4)} passed, ${r.failed} failed`;
  console.log(`  ${r.file.padEnd(width)}  ${tally}  ${(r.ms / 1000).toFixed(1)}s` +
              (r.quiet ? `  (${r.quiet})` : "") +
              (r.code !== 0 && r.failed === 0 && !r.quiet
                 ? `  (exited ${r.code} with nothing failing -- read its output)` : ""));
}
if (results.length < HARNESSES.length)
  console.log(`  ${HARNESSES.length - results.length} harness(es) never ran`);
console.log(`  ${results.length} of ${HARNESSES.length} harnesses · ${passed} passed, ${failed} failed`);
if (results.length < HARNESSES.length) exit = exit || 1;
console.log(exit === 0 && failed === 0 ? "\ngreen" : "\nRED");
process.exit(exit || (failed ? 1 : 0));
