// Which `python` on this machine is a Python 3, answered by asking rather than by assuming.
//
// Two of the five harnesses need one: `detail-churn.mjs` runs `scripts/22_detail.py` four times, and
// `pagemin_test.py` *is* Python. Neither can be skipped when no interpreter is found -- a suite that goes
// quiet when a tool is missing reports the same green as a suite that checked everything, and the only signal
// CI reads is the exit code. So this returns null and the caller fails loudly; nothing here has a fallback.
//
// The spellings, and why all four: `$PYTHON` first so a machine with several can name one. `python` is what
// a venv puts on PATH and what Windows Store installs provide. `python3` is the only one present on some
// Linux images, where bare `python` is either Python 2 or absent. `py` is the Windows launcher, which is the
// only entry point a stock python.org install adds to PATH. Each candidate is *run*, not stat'd, because on
// Windows a bare `python` is frequently an App Execution Alias that exists, is on PATH, exits 9009 and
// installs nothing -- it passes every test except being run.
import {spawnSync} from "node:child_process";

/** The first command on this machine that is a working Python 3, or null. */
export function findPython() {
  for (const cmd of [process.env.PYTHON, "python", "python3", "py"].filter(Boolean)) {
    const r = spawnSync(cmd, ["-c", "import sys; print(sys.version_info[0])"], {encoding: "utf8"});
    if (r.status === 0 && r.stdout.trim() === "3") return cmd;
  }
  return null;
}

/** What was tried, for an error message that says something more useful than ENOENT. */
export const pythonsTried = () =>
  [process.env.PYTHON && `$PYTHON (${process.env.PYTHON})`, "python", "python3", "py"].filter(Boolean);
