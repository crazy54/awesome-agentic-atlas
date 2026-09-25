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
5. **Red only on CI.** Look for three things:
   - font metrics (Segoe UI exists only on Windows);
   - `(hover: hover)`, which is false on CI;
   - line endings: CRLF locally, LF on CI;
   - a merge-ref difference, since CI tests your branch merged into `latest_branch`.
6. **Red after a generator change, while the generator's own output looks right.** Probes read the *committed*
   `docs/`, so regenerate and commit the output alongside the generator.

### `pwa-check`: "the worker's VERSION is a hash of the bytes it precaches"

Something rewrote `docs/index.html`, `docs/pages.css` or the manifest without re-running
`python scripts/24_pwa.py`. Run it and commit `docs/sw.js`. Until then, returning readers keep the old
homepage.

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
