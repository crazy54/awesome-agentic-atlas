// The whole verification suite, in one command:
//
//   node tests/run.mjs
//
// It finds a Chromium, serves `docs/` on a port the OS picks, runs the seven harnesses in turn, and prints
// what each one asserted and what the total was. It exits non-zero if anything failed, and it cleans up the
// server, every browser any harness started and every scratch directory on the way out -- including when a
// harness threw, including when it was interrupted.
//
// WHY SEVEN HARNESSES AND NOT ONE, which is the question anybody reading this directory will ask first:
//
//   signals_test.py   the cache-staleness policy in scripts/signals.py, on fabricated entries. Pure and
//                     instant, and the only test of it that can exist offline -- the three stages it
//                     serves all shell out to `gh api graphql`, so nothing here sees a real crawl.
//   probe.mjs         runs the page's own JavaScript against a stub DOM, and reads the stylesheet and the
//                     page text. Sees every branch of the ranking, the hash and the palette. Cannot see
//                     computed layout -- there is none in Node.
//   cards-check.mjs   measures real layout in a real browser at three widths in both themes. Cannot see a
//                     prefixed property this browser has an unprefixed implementation of.
//   pwa-check.mjs     manifest, service worker, precache, offline, and a 404 that must not be cached.
//                     Needs an origin, so it cannot be done from a file:// page at all.
//   detail-churn.mjs  regenerates 1,294 detail pages and compares hashes. Nothing to do with a browser.
//   pagemin_test.py   the comment stripper against the cases the real page does not contain -- template
//                     literals, regex literals, unterminated blocks. Python, because the stripper is.
//   media_test.py     the workbook writer: one embedded part per screenshot however many rows point at it,
//                     and the 65,535-entry ZIP ceiling that dedup exists to stay under.
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
// seven files own their own plumbing. It is 200 lines of plumbing.
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
  {file: "signals_test.py", label: "when a cached release/action signal needs re-querying", python: true, floor: 170},
  {file: "probe.mjs", label: "the page script under a stub DOM, and the page as text", floor: 140},
  {file: "pagemin_test.py", label: "the comment stripper, on the cases the page lacks", python: true, floor: 40},
  {file: "media_test.py", label: "one embedded part per screenshot, and the entry ceiling", python: true, floor: 40},
  {file: "detail-churn.mjs", label: "1,294 detail pages, regenerated and hashed", floor: 7},
  {file: "cards-check.mjs", label: "real layout at 1440/900/375 in both themes", needs: "browser", floor: 40},
  {file: "pwa-check.mjs", label: "manifest, worker, precache, offline, freshness, 404", needs: "browser", floor: 25},
];

if (!existsSync(join(ROOT, "docs", "index.html"))) {
  console.error("docs/index.html is not here. This suite asserts on the built site, and the built site is " +
                "committed -- so this is either the wrong directory or a checkout with docs/ removed.");
  process.exit(2);
}

const bin = find();
if (!bin) {
  console.error(
    "No Chromium found, and two of the seven harnesses drive one over CDP.\n\n" +
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
// prerequisite that goes missing must stop the run, not reduce it. Four of the seven need it -- one runs
// `22_detail.py` 1,294 pages at a time, one tests `pagemin.py`, one builds a workbook and counts the ZIP
// entries it holds, one decides which repos a crawl would ask about -- and between them they are 309 of the
// assertions below, which is nearly half.
const python = findPython();
if (!python) {
  console.error(
    "No Python 3 found, and four of the seven harnesses are Python or drive it.\n\n" +
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
