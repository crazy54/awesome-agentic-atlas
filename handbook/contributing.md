# Contributor guide

## Branches and pull requests

- **`latest_branch` is the default branch and the deployed one.** There is no `main`. Pages serves
  `latest_branch` `/docs` (see [ci-cd.md](ci-cd.md)).
- **Branch off `origin/latest_branch`, and open every PR against it.** Branch names so far look like
  `jfh-<topic>`.
- **A merge is a deploy.** Anything that changes `docs/` is live as soon as it merges, so merge only work
  that is ready to ship.
- **Branches are unprotected.** No check is required, so reading the checks is your job. Before merging,
  confirm that `tests.yml` ran and that any red is also red on `latest_branch`.
  - A PR that shows **zero** checks almost always has merge conflicts: GitHub builds no merge ref, so CI
    never starts.
  - CI tests the merge ref, not your head. If CI fails and your branch doesn't, merge `latest_branch` in
    and re-run.
- **Keep the build bots in mind.** The daily and weekly builds commit straight to `latest_branch`, often
  once a day. Expect to merge `latest_branch` into a long-lived branch more than once.
- **Merging.** `latest_branch` has been merged with merge commits so far. If you resolve conflicts in
  GitHub's web editor, review the result locally afterwards: web merges on this repository have dropped one
  side of a conflict before.

### What goes in a PR

A PR should contain:

1. The change to the **generator or source**, in `scripts/`, `config/`, `art/` or `docs/assets/`.
2. The **regenerated output** that change produces in `docs/` or `mega-list/`. Regenerate only what can
   run on a checkout; see [pipeline.md](pipeline.md#working-without-the-cache). Anything cache-dependent is
   rebuilt by the next CI run.
3. `docs/sw.js` from `python scripts/24_pwa.py`, if `docs/index.html`, `docs/pages.css` or the manifest
   changed.
4. Doc updates; see [keeping-docs-current.md](keeping-docs-current.md).

Run `node tests/run.mjs` before opening it. Say in the description which failures were already red on
`latest_branch` (see [testing.md](testing.md#known-red-and-environment-sensitive-checks)).

## Generated vs hand-written

| Hand-written, edit freely | Generated, edit the generator instead |
|---|---|
| `scripts/`, `tests/`, `config/`, `art/`, `.github/`, `handbook/`, READMEs | `docs/**/*.html`, `docs/*.json`, `docs/*.xml`, `docs/pages.css`, `docs/sw.js`, `docs/manifest.webmanifest`, `docs/search/`, `docs/og/`, `docs/repo/` |
| `docs/assets/archie*.js`, `docs/assets/rig-show.js`, `docs/CNAME`, `docs/favicon.svg`, `docs/assets/atlas-byte.png` | `mega-list/**` |
| `docs/assets/three-archie.js` and the `.glb`/`.webm`/`.webp` art: not edited by hand, but rebuilt from `art/` (see [archie.md](archie.md)) | `state/*.json`: ledgers written by the pipeline. Never hand-edit them; on a merge conflict, keep both sides |

Every generated HTML file carries its generator's name in the pipeline table in [pipeline.md](pipeline.md).
When in doubt, search `scripts/` for the output path.

## Windows and Git Bash

Most of this repository has been built on Windows with Git Bash, and CI runs on Linux. The same few
things go wrong repeatedly.

### Line endings (CRLF and `core.autocrlf`)

- The Windows checkout has `core.autocrlf=true`, so the working tree is **CRLF** while the committed and
  served files are **LF**.
- **Never hash files straight from disk** and compare the result with CI, because the answer differs by
  platform. Every hash in the pipeline normalises CRLF to LF first: the service worker's `VERSION` and
  Archie's `?v=`. Any new one must too.
- `.gitattributes` pins two exceptions:
  - `docs/search/*.bin` is **binary**, because autocrlf would corrupt those int8 matrices without any visible sign.
  - `docs/search/*.json` is `eol=lf`.

  Add a rule there for any new binary format.
- Python writing with a default `open(..., "w")` on Windows emits CRLF. A Bash `while read` loop over that
  output then sees a trailing `\r` on every line. Write with `newline="\n"`, or strip `\r`.
- Don't try to force LF in the working tree to "fix" diffs. With autocrlf on, `git status` then stays dirty
  forever.

### MSYS path conversion

Git Bash rewrites arguments that look like POSIX paths. Two common victims:

```bash
# fails with a misleading "bad revision" or "path does not exist" error:
git show origin/latest_branch:docs/data.json
# works:
MSYS_NO_PATHCONV=1 git show origin/latest_branch:docs/data.json
```

Any `git show <ref>:<path>`, and any argument starting with `/` that is meant for a native Windows
program, needs `MSYS_NO_PATHCONV=1`.

### Temporary files

Git Bash's `/tmp` and Python's `/tmp` are **different directories** on Windows: Python resolves `/tmp` against
the current drive. To pass a file between the two, use a path both agree on, such as a directory in the
checkout's parent, or `%TEMP%` spelled as a Windows path.

### Long paths and reserved names

Detail pages are written to `docs/repo/<owner>/<name>/`. `22_detail.py` turns names into slugs so that no path
contains a character or reserved name Windows cannot check out. If a checkout fails on Windows with
"invalid path", look for a generator that writes an un-slugged name.

### Processes

- Never stop a stray server or browser with `taskkill /IM node.exe` or `taskkill /IM chrome.exe`. That kills
  every Node or Chrome process on the machine, including other people's editors, MCP servers and test runs.
  Stop your own process by PID, or with Ctrl-C.
- `run.mjs` cleans up its own server and browsers, even on Ctrl-C.

### Shell heredocs

Long quoted heredocs full of apostrophes can fail in Git Bash and write nothing, so write multi-line files with an
editor rather than `cat <<'EOF'`.

## Tools you will need

| Task | Needs |
|---|---|
| Run the suite | Node 22, Python 3, `pip install openpyxl pillow`, a Chromium |
| Run the data-only stages (19c to 31) | Python 3 |
| Run `27_semantic.py` | numpy, and network access for the model |
| Anything that fetches | `gh`, authenticated |
| Rebuild Archie or the rig | Blender (5.2 is the default path `wall.py` assumes); numpy and Pillow for `wall.py` |
| Rebuild `three-archie.js` | Node, `npm i three@0.186.0 esbuild` in a scratch directory |
| `08_verify.py`, `09_pdf.py` | Windows with Microsoft Excel |
