# CI/CD and deployment

## Where the site comes from

GitHub Pages serves the site with the **legacy** build type, from the **`/docs` folder of `latest_branch`**.
Nothing is ever deployed from `main`. There is no deploy workflow: a commit to `latest_branch` that changes
`docs/` is a deploy.

- The custom domain comes from `docs/CNAME`: `aaa.jeremyfhall.com`. `crazy54.github.io/awesome-agentic-atlas/`
  redirects to it.
- To check Pages settings, run `gh api repos/crazy54/awesome-agentic-atlas/pages`. On 2026-09-25 it reported
  `build_type: legacy`, source `latest_branch` `/docs`, and `https_enforced: false`.
- `docs/.nojekyll` is written by `19_pages.py`, so Pages serves the files exactly as committed.

Since a merge to `latest_branch` publishes immediately, **merged means deployed**. The reverse is also
true: work that is only on a feature branch is not live, however green its PR.

## The five workflows

| Workflow | Triggers | Job | Writes to the repo? |
|---|---|---|---|
| `daily.yml` | cron `12 11 * * *` (11:12 UTC), and dispatch with a `force` input | Incremental rebuild of the site and the Markdown edition from lists that moved | Yes: commits "Daily refresh YYYY-MM-DD" to `latest_branch` |
| `weekly.yml` | cron `40 12 * * 0` (Sunday 12:40 UTC), and dispatch | Full rebuild including screenshots, OG cards, collections and both workbooks | Yes: commits "Weekly rebuild", then publishes a release |
| `tests.yml` | every pull request, pushes to `latest_branch`, cron `40 7 * * 1`, dispatch | `node tests/run.mjs` on ubuntu-latest | No |
| `lighthouse.yml` | pull requests touching page generators or `docs/` (see its `paths:`), cron `40 13 * * 1`, dispatch | Lighthouse CI 0.15.1 against `/index.html` and `/catalog/index.html` | No |
| `og-preview.yml` | dispatch only | Renders the OG cards to a temp directory with `23_og.py --out` and diffs them against the committed cards | No |

`daily.yml` and `weekly.yml` share the concurrency group `atlas-build`, so they never run at once.
Scheduled start times lag: in September 2026 the 11:12 daily usually started around 15:30 UTC.

Each workflow opens with a long comment explaining its design. **Read it before editing the file.**
Several harnesses read workflow text, so these files are less safe to edit than they look. For example,
`collections_test.py` checks that the weekly runs stage 25. `latest_branch` had no branch protection and
no required checks on 2026-09-25 (`gh api repos/crazy54/awesome-agentic-atlas/branches/latest_branch/protection`
returns 404), so a red check does not block a merge by itself.

### The daily build

1. **Cache.** Restores `cache/` with `actions/cache@v4`, key `atlas-cache-${run_id}`, restore-keys
   `atlas-cache-`. That action saves only when the job succeeds, so a failed daily banks nothing.
2. **Screenshot gate.** If `cache/shots_all.done.json` is missing, the job logs a warning and **exits 0
   without rebuilding**. That file means the last weekly finished its screenshots. `force` does not bypass
   this gate. A green daily can therefore have published nothing; check the deployed
   `docs/data.json` `snapshot` to be sure.
3. **Change gate.** `watch_sources.py` asks whether any list's head commit moved. The job continues only if
   one did, or if `force` is set.
4. **Fetch.** `pull_sources`, then `01`, `02 --force`, `03`, `03b`, `04`, `10`, `11`, `13`, `14`.
5. **Build.** `17`, `check_markdown`, `19`, `25_velocity`, `19c`, `19d`, `20`, `21`, `22`, `31`, `24`, `27`.
6. **Verify.** A check that nothing outside the expected paths was rewritten, then `node tests/run.mjs`.
   The daily sets `VERIFY_GATES_DEPLOY: "false"`, so **a red suite still publishes**, and the run then
   ends red to say so.
7. **Publish.** `watch_sources.py --update` records the new SHAs. The job commits, pushes to `latest_branch`,
   and submits changed URLs to IndexNow (`26_indexnow.py`).

### The weekly build

The weekly build runs the same fetch as the daily, then adds:

- **Screenshots and workbooks:** `05`, `06`, `15`, `15b`, and `16`. The job installs `playwright` and
  `numpy`, and runs `playwright install chromium`.
- **Weekly-only site stages:** `25_collections` and `23_og`, on top of the daily build.
- **A cache split into `restore` and `save`.** The save step is `if: always()`, so a failed or timed-out
  weekly still banks its progress, and a re-run resumes. The timeout is 350 minutes.
- **`VERIFY_GATES_DEPLOY: "true"`.** A red suite blocks the commit, the IndexNow submission and the release.
  The cache is still saved.
- **A release.** It is tagged `vYYYY.MM.DD` and carries `Awesome-Agentic-Atlas-DARK.xlsx` and
  `Awesome-Agentic-Atlas-LIGHT.xlsx`. If the tag already exists, the files are re-uploaded with `--clobber`.
  The latest release on 2026-09-25 was `v2026.09.21`.

**`18_slicers.py` runs in neither workflow**, so released workbooks have no slicers. Nothing in CI builds
the legacy orchestrators workbook (`07`, `08`, `09`) either.

### Pushes by a workflow do not run the tests

The daily and weekly builds push with `secrets.GITHUB_TOKEN`. GitHub starts no workflow runs for pushes
made with that token. That is why both builds run the suite themselves before committing, and why a
build commit on `latest_branch` shows no `tests.yml` check.

### tests.yml

This workflow runs on ubuntu-latest with Node 22 and Python 3.12.

- It installs `openpyxl` and `pillow`.
- It sets `AAA_CHROME_FLAGS="--no-sandbox --disable-dev-shm-usage"`, because a container has no user
  namespace to sandbox into.
- On failure it uploads `build-tmp/` as the `test-screenshots` artifact.
- It has no `paths` filter, on purpose: a change anywhere can break a generated page.
- A PR with merge conflicts has no merge ref, so `pull_request` CI is **never created**. "Zero checks" on a
  PR usually means it conflicts, not that CI is queued.
- CI tests the **merge ref** (`refs/pull/N/merge`), not your branch head. A failure you cannot reproduce on
  your branch may come from `latest_branch` moving underneath it.

## Configuration: variables and secrets

The workflows read four optional settings. Each can be set either as a repository variable or as a
secret, read as `vars.X || secrets.X`. Every one has a committed default or a safe "off":

| Setting | Read by | If unset |
|---|---|---|
| `CF_BEACON_TOKEN` | `19_pages.py`, and through it `19d`, `20`, `22`, `25_collections` and `31` (Cloudflare Web Analytics) | Uses the token committed in `scripts/19_pages.py`. Setting it to `""` or `off` removes the beacon |
| `GOOGLE_SITE_VERIFICATION` | `19_pages.py` | No Search Console meta tag. **It was unset on 2026-09-25**, so the property is unverified |
| `INDEXNOW_KEY` | `19_pages.py`, `20_landing.py` (key file), `26_indexnow.py` | Uses the committed default key |
| `GITHUB_TOKEN` | every `gh` call, as `GH_TOKEN` | Supplied by Actions |

The workflows write these to `$GITHUB_ENV` only when a value exists. Declaring them in `env:` would set
them to `""` whenever they are unset, and for two of the four `""` means something different from unset.

## Caches and state

- **`cache/`** lives only in the GitHub Actions cache. If it is evicted (7 days unused, or the 10 GB cap),
  the next weekly starts cold, and every daily skips until that weekly finishes its screenshots.
- **`state/*.json`** is committed. It holds the first-seen ledger, star history and Discover rotation, and
  must survive any cache loss. See [overview.md](overview.md#committed-state).

## Running a build by hand

Dispatch a workflow from the Actions tab, or run:

```bash
gh workflow run daily.yml --ref latest_branch -f force=true
gh workflow run weekly.yml --ref latest_branch
```

Dispatching against a feature branch (`--ref your-branch`) rebuilds from that branch's scripts and pushes to
**that branch** (the builds push to `HEAD:${GITHUB_REF_NAME}`). This is the only way to see a
cache-dependent stage's real output before merging.

To check a finished run, use `gh run view <id>`. Do not rely on `gh run watch --exit-status`: it returns 0
when you attach to a run that has already failed.
