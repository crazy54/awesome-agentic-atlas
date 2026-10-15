# Troubleshooting

## Symptoms and usual causes

### The suite is red

1. **Is it red on `latest_branch` too?** Compare with the known-red list in
   [testing.md](testing.md#known-red-and-environment-sensitive-checks), or run the suite on a clean
   checkout of `latest_branch`. A PR is judged on adding no new failures.
2. **Re-run a flaky harness before debugging it.** `cards-check` and `dance-check` have timing-sensitive
   assertions.
3. **"made N assertions, fewer than the floor"** means the harness stopped testing something. Usually
   an early return, or a fixture that moved. It is a real failure even though every assertion it made passed.
4. **Exit code 2** means the runner could not start. Either no Chromium was found (set `CHROME_PATH`), no
   Python 3 was found (set `PYTHON`), or `docs/index.html` or `docs/catalog/index.html` is missing.
5. **Red only on CI.** Look for these:
   - font metrics (Segoe UI exists only on Windows);
   - `(hover: hover)`, which is false on CI;
   - line endings: CRLF locally, LF on CI;
   - a merge-ref difference, since CI tests your branch merged into `latest_branch`;
   - the frame rate, in the Archie harnesses. Under swiftshader a CI runner draws a frame or two a second
     once the rig is lit. Archie's clock steps at most 0.1 s a frame, so anything timed by it (a cue, a
     swell, the pods) takes five times as long on the wall or more: wait for it in the rig's seconds, as
     `untilRig` in `rig-check.mjs` does, never in wall-clock milliseconds. To reproduce it locally, pin the
     browser's whole process tree to one or two cores. On Windows `start /affinity` misses the GPU process,
     which is where swiftshader runs, so set `ProcessorAffinity` on every descendant of the harness instead.
6. **Red after a generator change, while the generator's own output looks right.** Probes read the *committed*
   `docs/`, so regenerate and commit the output alongside the generator.

### `pwa-check`: "the worker's VERSION is a hash of the bytes it precaches"

Something rewrote `docs/index.html`, `docs/pages.css` or the manifest without re-running
`python scripts/24_pwa.py`. Run it and commit `docs/sw.js`. Until then, returning readers keep the old
homepage.

### `spotlight-check`: a layout shift moves the spotlight, Archie and the nav sideways

The detail names `hero`, `mhmascot` and `NAV`. Every rect moves left (8 px; the nav 15) and none moves down,
and the widths read `"inner":1440,"client":1425`. That is a scrollbar appearing after the first paint. Loaded,
the homepage is always taller than the window. On a slow CPU, though, Chrome paints while the parser is still
between the spotlight and the first shelf, when the page still fits the window. The shelves arrive, the
scrollbar appears, and the page is laid out 15 px narrower. `html{scrollbar-gutter:stable}` in `HOME_CSS` in
`31_home.py` keeps the width the same either way. If this comes back, look for whatever removed that rule or
put an `overflow` on the root.

To reproduce, throttle the page with `Emulation.setCPUThrottlingRate` at rate 8 in the harness's session. On
2026-10-15, before the rule, that shifted 75 of 96 visits at 1440 px in 12 runs. The GitHub API made no
difference: it was as likely with `api.github.com` stubbed to answer 200 as stubbed to answer 403. With the
rule, none of 96 shifted that way.

A smaller shift names only `daily` and moves it sideways (21 px right on a friend day). It is the line of
the day: the parser painted the build day's line before the script after it swapped in today's, and a kicker
of another length ("Friend of the day" for "Did you know?") moved the text beside it. See the known issue
below.

### Archie stays a poster

- Is the window at least 900 px wide? Is reduced motion off? Does the browser have WebGL2? Add `?archie=admin`
  to see his reason on every button.
- Check the console for a 404 or a module error. After an asset edit, the usual cause is a stale `?v=`: a new
  `archie.js` has met an old sibling from the HTTP cache. Run `python scripts/31_home.py` and then
  `python scripts/24_pwa.py`. See [archie.md](archie.md#after-editing-archie).
- In headless Chromium you need the swiftshader flags for WebGL. The Archie harnesses add them.

### The daily run is green but the site did not change

The daily **exits 0 without building** in two cases:

- `cache/shots_all.done.json` is missing, because the last weekly did not finish its screenshots;
- no source list moved.

Read the run log for "Skipped the rebuild". To check what is live, fetch the deployed data and read its snapshot:

```bash
curl -s https://aaa.jeremyfhall.com/data.json | head -c 300
```

Re-running the weekly (`gh workflow run weekly.yml --ref latest_branch`) resumes from its banked cache.

### A build failed with "Generator missing from the build"

The "Every tracked page was rewritten" step lists every tracked file under `docs/` and `mega-list/` that the
build did not write. A file on that list is either:

- a genuinely missing stage, which is the check's purpose; or
- a hand-written file that is not in its short `static` allowlist.

See issue G below.

### "No commits between A and B", or a PR shows zero checks

- **Zero checks** almost always means the PR has conflicts, so GitHub built no merge ref.
- If `gh pr create` fails with "No commits between" on refs that do differ, create the PR through the REST
  API instead:

  ```bash
  gh api repos/crazy54/awesome-agentic-atlas/pulls --input pr.json
  ```

### Git problems on Windows

- **`git show ref:path` says the path does not exist:** prefix the command with `MSYS_NO_PATHCONV=1`.
- **`git status` is dirty right after a checkout:** this is `autocrlf` interacting with a file somebody forced
  to LF. Don't "fix" it by re-forcing.
- **A Python-written file breaks a `while read` loop:** the file has CRLF endings. See
  [contributing.md](contributing.md#windows-and-git-bash).

## Known issues

Seven issues, found on `latest_branch` at `a77b46eb` on 2026-09-25 while this handbook was being written,
are now all fixed: a stale `sw.js` `VERSION`, mismatched `?v=` values, two gaps in the Archie asset hash,
the catalogue overwriting the homepage, `admin-check.mjs` left out of the suite, and the daily's
allowlist missing `docs/assets/`. Add new issues here as a table: issue, effect, fix. Delete each entry
when its fix merges.

| Issue | Effect | Fix |
|---|---|---|
| The line of the day is drawn with the build day's line, and `DAILYPICK_JS` swaps in today's after the `#dailylines` pool that follows it. `31_home.py` says the swap "lands before the first paint", but on a slow CPU the parser can paint in between (found 2026-10-15) | A layout shift naming `daily`. Under 8x CPU throttling it failed `spotlight-check` once in 12 runs; it has not been seen on CI | Draw the slot the way the spotlight is drawn: insert it from the script, with the build day's line in a `<noscript>` |

Also found, and lower priority:

- `18_slicers.py` runs in no workflow, so released workbooks have no slicers. `18_slicers.py --probe` writes
  `slicer-probe.xlsx` at the repo root, and that file is not gitignored.
- `08_verify.py`'s docstring says the merged workbook "has twenty sheets". `16_build_all.py`'s sheet plan has 21, counted from the source, not from a built workbook.
- The `25_collections.py` docstring says "Five sets, seven picks each", but `keep-it-honest` has six in `config/collections.json`.
- The committed `mega-list/` still links `crazy54.github.io/awesome-agentic-atlas/` and the pre-`/catalog/`
  URLs. It is generated, so it corrects itself on the next successful `17_markdown.py` run.
- Workflow comments with stale figures. These were left unedited because harnesses read workflow text:
  - `tests.yml`'s `name:` says "eighteen-harness", and its comments say "twenty harnesses, 3,157". The runner has 26.
  - `daily.yml` says "nineteen harnesses", and says its cache is saved on failure. `actions/cache` saves only on
    success; the weekly's split restore/save is the one that saves on failure.
  - `lighthouse.yml` comments quote 40,960, 25,600 and 307,200 byte budgets. The enforced limit has been
    16,777,216 B since `81ba01d8`.
