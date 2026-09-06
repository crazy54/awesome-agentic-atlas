// Finding a Chromium, and starting one on a port the OS chooses.
//
// `find()` is a port of `scripts/chrome.py` and deliberately not a second opinion: the search order there
// is the one the two screenshot stages already use, so a machine where the build can take screenshots is a
// machine where these tests can run, and there is exactly one place to fix when that stops being true. Its
// docstring is the explanation; the short version is env var, then Playwright's browser cache newest-build
// first, then anything Chromium-shaped on PATH.
//
// It differs from `chrome.py` in one way, and on purpose. `find()` there returns None and the build
// degrades to Open Graph cards, because a missing browser costs the build its screenshots and not the
// build. A missing browser costs this suite two of its four harnesses, which is not a degraded pass, so
// `find()` here returns null and `tests/run.mjs` turns that into a message naming the three places it
// looked and the env var that overrides them.
//
// `launch()` asks for `--remote-debugging-port=0` and reads the port back out of `DevToolsActivePort` in the
// profile directory, whose first line is the port and whose second is the browser's websocket path. Verified
// on this machine against chrome-headless-shell 148.0.7778.96, which wrote "59331\n/devtools/browser/<uuid>".
// Every process started here also drops its pid in `<tmp>/pids/`, so `run.mjs` can sweep for survivors after
// a harness has crashed hard enough not to clean up after itself -- see the note there.
import {spawn} from "node:child_process";
import {existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, statSync,
        unlinkSync, writeFileSync} from "node:fs";
import {homedir, tmpdir} from "node:os";
import {delimiter, join} from "node:path";

const ENV_VARS = ["CHROME_PATH", "CHROMIUM_PATH", "PLAYWRIGHT_CHROMIUM"];

// The headless shell first, for `chrome.py`'s reasons: it is a third of the size of full Chrome, it is what
// Playwright installs by default, and it is the only one of these that cannot try to open a window.
const BINARIES = ["chrome-headless-shell.exe", "chrome-headless-shell", "headless_shell",
                  "chrome.exe", "chrome", "chromium"];

const ON_PATH = ["chrome-headless-shell", "chromium", "chromium-browser",
                 "google-chrome", "google-chrome-stable", "chrome"];

function* caches() {
  if (process.env.PLAYWRIGHT_BROWSERS_PATH) yield process.env.PLAYWRIGHT_BROWSERS_PATH;
  const home = homedir();
  yield join(home, "AppData", "Local", "ms-playwright");   // Windows
  yield join(home, ".cache", "ms-playwright");             // Linux, and GitHub's ubuntu runners
  yield join(home, "Library", "Caches", "ms-playwright");  // macOS
}

// `chromium_headless_shell-1223` style names, by build number and descending. By name would be wrong the
// first time a build number changes width: "999" sorts above "1223".
const newestFirst = (names) => names.slice().sort((a, b) => {
  const n = (s) => { const m = /(\d+)\s*$/.exec(s); return m ? Number(m[1]) : -1; };
  return n(b) - n(a) || (a < b ? 1 : a > b ? -1 : 0);
});

// Bounded, because this walks a directory chosen by an env var and a runaway symlink loop in one would hang
// the suite before it printed anything. Playwright's installs are four levels deep at most.
function walk(dir, want, depth = 0, hits = []) {
  if (depth > 6) return hits;
  let entries;
  try { entries = readdirSync(dir, {withFileTypes: true}); } catch { return hits; }
  for (const e of entries) {
    const full = join(dir, e.name);
    if (e.isDirectory()) walk(full, want, depth + 1, hits);
    else if (e.name === want) hits.push(full);
  }
  return hits;
}

const onPath = (name) => {
  const exts = process.platform === "win32" ? [".exe", ".cmd", ".bat", ""] : [""];
  for (const dir of (process.env.PATH || "").split(delimiter).filter(Boolean))
    for (const ext of exts) {
      const full = join(dir, name + ext);
      try { if (statSync(full).isFile()) return full; } catch { /* next */ }
    }
  return null;
};

/** The first Chromium this machine can offer, or null. Mirrors `scripts/chrome.py`'s order exactly. */
export function find() {
  for (const v of ENV_VARS) {
    const value = process.env[v];
    if (value && existsSync(value)) return value;
  }
  for (const cache of caches()) {
    let installs;
    try { installs = readdirSync(cache).filter((n) => n.startsWith("chromium")); } catch { continue; }
    // `chromium_headless_shell-*` sorts above `chromium-*` for the same build, which is the preference we
    // want: underscore is above hyphen, and the comparison keeps build number first.
    for (const install of newestFirst(installs))
      for (const name of BINARIES) {
        const hits = walk(join(cache, install), name).sort();
        if (hits.length) return hits[0];
      }
  }
  for (const name of ON_PATH) {
    const hit = onPath(name);
    if (hit) return hit;
  }
  return null;
}

/** Where `find()` looked, for the error message when it found nothing. */
export const searched = () => [...caches(), "$PATH"];

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/**
 * Start `bin` headless on an OS-chosen debugging port, with a profile of its own under `tmp`.
 *
 * A profile per launch rather than a shared one, and it is not tidiness: pwa-check's first four assertions
 * are about a *cold* visit -- no worker registered, no caches, no localStorage -- and cards-check writes a
 * theme into localStorage and reloads to read it back. A reused profile would make the second run of the
 * suite assert something different from the first, which is the sort of test that passes until the day it
 * matters.
 *
 * @returns {Promise<{wsUrl: string, port: number, profile: string, close: () => Promise<void>}>}
 */
export async function launch(bin, tmp = tmpdir(), tag = "chrome") {
  mkdirSync(tmp, {recursive: true});
  const profile = mkdtempSync(join(tmp, `aaa-${tag}-`));
  const flags = (process.env.AAA_CHROME_FLAGS || "").split(/\s+/).filter(Boolean);
  const child = spawn(bin, [
    "--remote-debugging-port=0", `--user-data-dir=${profile}`,
    "--headless=new", "--no-first-run", "--disable-gpu",
    ...flags,
  ], {stdio: ["ignore", "ignore", "pipe"]});

  let err = "";
  child.stderr.on("data", (b) => { err += b; });
  child.on("error", (e) => { err += e.message; });

  // Registered here rather than left to the caller's `finally`, because the caller is a harness whose whole
  // job is to fail: an assertion that throws, a CDP call that rejects, a `process.exit(1)` on a failure
  // count. Only `exit` fires for all of those, and only synchronous work is allowed in it -- which `kill()`
  // and `rmSync()` both are. The graceful path is `close()` below; this is the one that runs when there
  // wasn't one. Chrome killed here can leave its profile locked for a moment, so the removal is
  // best-effort and `run.mjs` sweeps the whole scratch directory afterwards.
  const onExit = () => {
    try { child.kill(); } catch { /* already gone */ }
    try { rmSync(profile, {recursive: true, force: true}); } catch { /* run.mjs will */ }
  };
  process.on("exit", onExit);

  const pids = join(tmp, "pids");
  mkdirSync(pids, {recursive: true});
  const pidFile = join(pids, String(child.pid));
  writeFileSync(pidFile, profile, "utf8");

  // First line is the port, second is the browser's websocket path. Read after a non-empty read, because
  // the file exists before it is written and an empty read gives NaN.
  const portFile = join(profile, "DevToolsActivePort");
  let raw = "";
  for (let i = 0; i < 120 && !raw.includes("\n"); i++) {
    if (child.exitCode !== null)
      throw new Error(`${bin} exited with ${child.exitCode} before it opened a debugging port` +
                      (err ? `:\n${err.trim()}` : ""));
    try { raw = readFileSync(portFile, "utf8"); } catch { /* not yet */ }
    if (!raw.includes("\n")) await sleep(125);
  }
  if (!raw.includes("\n"))
    throw new Error(`${bin} never wrote ${portFile} -- no debugging port to connect to` +
                    (err ? `:\n${err.trim()}` : ""));
  const [portLine, wsPath] = raw.split("\n");
  const port = Number(portLine.trim());
  // Asked for anyway, rather than trusting the file: it is also the readiness probe. The port is open the
  // moment the file is written, but the browser target list is not necessarily answering yet.
  let info;
  for (let i = 0; i < 60 && !info; i++) {
    try { info = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json(); }
    catch { await sleep(250); }
  }
  if (!info) throw new Error(`chrome wrote port ${port} but never answered /json/version`);

  return {
    port, profile,
    wsUrl: info.webSocketDebuggerUrl || `ws://127.0.0.1:${port}${wsPath.trim()}`,
    version: info.Browser,
    close: async () => {
      process.off("exit", onExit);
      child.kill();
      for (let i = 0; i < 40 && child.exitCode === null; i++) await sleep(100);
      try { unlinkSync(pidFile); } catch { /* swept by run.mjs */ }
      // Retried, because on Windows the profile's own files stay locked for a moment after the process
      // has gone and a single rmSync loses the race about half the time.
      for (let i = 0; i < 12; i++) {
        try { rmSync(profile, {recursive: true, force: true}); return; } catch { await sleep(200); }
      }
    },
  };
}

/**
 * Kill anything started by `launch()` under `tmp` that is still running, and say how many there were.
 *
 * The backstop for a harness that died before its own cleanup ran. A pid file whose process has already
 * gone is the normal case and is not reported.
 */
export function sweep(tmp) {
  const pids = join(tmp, "pids");
  let names;
  try { names = readdirSync(pids); } catch { return []; }
  const killed = [];
  for (const name of names) {
    const pid = Number(name);
    try { process.kill(pid, 0); } catch { try { unlinkSync(join(pids, name)); } catch {} continue; }
    try { process.kill(pid, "SIGKILL"); killed.push(pid); } catch { /* raced us */ }
    try { unlinkSync(join(pids, name)); } catch {}
  }
  return killed;
}
