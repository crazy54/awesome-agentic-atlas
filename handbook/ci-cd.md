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

## The workflows

| Workflow | Triggers | Job | Writes to the repo? |
|---|---|---|---|
| `daily.yml` | cron `12 11 * * *` (11:12 UTC), and dispatch with a `force` input | Incremental rebuild of the site and the Markdown edition from lists that moved | Yes: commits "Daily refresh YYYY-MM-DD" to `latest_branch` |
| `weekly.yml` | cron `40 12 * * 0,3` (Sunday and Wednesday 12:40 UTC), and dispatch | Full rebuild including screenshots, OG cards and collections | Yes: commits "Weekly rebuild" |
| `tests.yml` | every pull request, pushes to `latest_branch`, cron `40 7 * * 1`, dispatch | `node tests/run.mjs` on ubuntu-latest | No |
| `lighthouse.yml` | pull requests touching page generators or `docs/` (see its `paths:`), cron `40 13 * * 1`, dispatch | Lighthouse CI 0.15.1 against `/index.html` and `/catalog/index.html` | No |
| `dead-repos.yml` | cron `30 9 * * 6` (Saturday 09:30 UTC), and dispatch | Asks GitHub which listed repos are gone and records them in `state/dead-repos.json`; dispatches `daily.yml` with `force` when that changed | Yes: commits "Dead-repo scan YYYY-MM-DD" to `latest_branch` |
| `og-preview.yml` | dispatch only | Renders the OG cards to a temp directory with `23_og.py --out` and diffs them against the committed cards | No |
| `canary.yml` | cron `23 1-23/4 * * *` (every 4 hours), dispatch | Pulls every source list and parses it; regenerates the pages that are pure functions of committed files. Proposes a fix on a `bot/` branch | Only `bot/drift-<fingerprint>` and `bot/regenerate` |
| `alert.yml` | when the daily, weekly, tests or canary finish on `latest_branch`; cron `47 */2 * * *`; dispatch (dry run by default) | Keeps one `build-red` issue in step with those four | No (issues only) |

`daily.yml` and `weekly.yml` share the concurrency group `atlas-build`, so they never run at once. **Nothing else
may join it.** A concurrency group holds one running and one *pending* run, and a newly queued run cancels the
pending one. So a short job queued in `atlas-build` behind a running weekly cancels the daily waiting there.
`dead-repos.yml` left the group on 2026-11-18 for that reason. The builds never write its ledger, so its push
rebases cleanly, and it retries. The canary and the alert have groups of their own.

Scheduled start times lag. In September 2026 the 11:12 daily usually started around 15:30 UTC, and in November
between 15:00 and 21:00 UTC.

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
   one did, or if `force` is set. Just before it (and before the screenshot check, as its own step),
   `12_scout.py` searches GitHub for rising agentic repos and writes `cache/sources/scout.md`; for that
   synthetic source "moved" means the document's SHA-256 differs from the one last recorded. A search that
   fails keeps the committed `state/scout-repos.json` and re-renders the same document, so it never fails
   the job and never moves the gate.
4. **Fetch.** `pull_sources`, then `01`, `02 --force`, `03`, `03b`, `04`, `10`, `11`, `13`, `14`.
5. **Build.** `17`, `check_markdown`, `19`, `25_velocity`, `19c`, `19d`, `20`, `21`, `22`, `31`, `24`, `27`.
6. **Verify.** A check that nothing outside the expected paths was rewritten, then `node tests/run.mjs`.
   The daily sets `VERIFY_GATES_DEPLOY: "false"`, so **a red suite still publishes**, and the run then
   ends red to say so.
7. **Publish.** `watch_sources.py --update` records the new SHAs. The job commits, pushes to `latest_branch`,
   and submits changed URLs to IndexNow (`26_indexnow.py`).

### The weekly build

The weekly build runs the same fetch as the daily, then adds:

- **Screenshots:** `05`, `06` and `15`. The job installs `pillow`, `playwright` and `numpy`, and runs
  `playwright install chromium`.
- **Weekly-only site stages:** `25_collections` and `23_og`, on top of the daily build.
- **A cache split into `restore` and `save`.** The save step is `if: always()`, so a failed or timed-out
  weekly still banks its progress, and a re-run resumes. The timeout is 350 minutes.
- **`VERIFY_GATES_DEPLOY: "true"`.** A red suite blocks the commit and the IndexNow submission.
  The cache is still saved.

**No release.** Until November 2026 the weekly also ran `16_build_all.py` to build two Excel workbooks and
published them as a release tagged `vYYYY.MM.DD`. Spreadsheet edition: retired. The last copy, built 2026-10-22, stays available but is no longer updated. The website is the maintained edition. That copy is release `v2026.10.22`; every
link to it (the README, `mega-list/`, the catalogue's nav) is pinned to that tag rather than
`releases/latest`, so nothing published later can move it. `16_build_all.py` is now a library of row
functions that `17_markdown.py` and `19_pages.py` import, not a stage. The weekly step it ran took 4 to 7
minutes. `15b_shots_sources.py`, which drew repo cards for the workbook's Sources sheet, went with it.

### The dead-repo scan

A repo that is deleted, made private, taken down or disabled stays in its source list, and the build used
to keep publishing it: a card with no picture (its Open Graph image 404s) and a detail page whose README
never loads. `dead-repos.yml` runs `scripts/dead_repos.py` every Saturday, a day before the weekly build:

1. **Scan.** Every repo in `docs/data.json`, plus every repo already in the ledger, is asked about through
   `graphql_batch`, fifty to a query. Only the repos GraphQL cannot find are asked about again over REST,
   which follows renames. Dead means REST 404, 451 or a 403 with a `block` object, or `isDisabled`.
   Renamed and archived repos are alive.
2. **Guards.** Any request that fails for a reason that is not about the repo (a rate limit, a 5xx, a bad
   token) fails the step, and nothing is written. A scan that would newly mark more than 10% of the atlas
   dead, or more than 25 repos on a small atlas, also fails without writing.
3. **Commit.** If `state/dead-repos.json` changed, the job commits it to the branch it ran on. The run's
   summary page lists the repos newly gone and the ones that came back.
4. **Rebuild.** Only when the ledger changed, it dispatches `daily.yml` with `force=true`. `14_classify_all.py`
   leaves every ledger repo out, so that run drops them from the site and the Markdown edition. The daily's
   screenshot gate still applies.

A repo stays in the ledger while it is still gone, including after its list drops it. One that answers
again is removed by the next scan and is listed again by the build after it. To look at the ledger without
a network, run `python scripts/dead_repos.py --status`. A curated pick in `config/collections.json` that
goes dead fails the weekly at `25_collections`, by design; remove or replace the pick.

### Time limits, retries and the budget line

- **Every job has a `timeout-minutes`, and every long step has its own.** Each step limit is two to three times
  that step's longest green run in the 45 days to 2026-11-18. A hang fails the step it is in, and the step is
  named in the build-red issue. Before this, a hang ran to the job limit, and the log stopped mid-line.
  `ci_tools_test.py` fails a job that has no `timeout-minutes`.
- **The weekly's screenshots have no fixed limit.** They get whatever the job has left, minus 90 minutes kept
  back for the steps after them and for the cache bank. A cold run stops, banks its screenshots, and the next
  weekly resumes.
- **`tests.yml`'s suite step stops a few minutes before its job does.** The screenshots artifact is then still
  uploaded. `run.mjs` also has a watchdog for each harness: 20 minutes by default, 100 for `bits-check.mjs`, or
  `AAA_HARNESS_MINUTES`. A hung harness is killed and reported as `hung`, and the run carries on.
- **Retries.** `tools/retry.sh N cmd` wraps `pip install` and the builds' `git pull --rebase && git push`. It
  makes three tries, 15 s and then 45 s apart, and each retry is a warning in the log. The fetch stages are not
  wrapped, because `scripts/02_fetch.py` already retries GitHub's 502s and 504s and splits batches; in the audit
  it absorbed every one.
- **The budget line.** The last step of the daily, the weekly and each tests job prints
  `This job used N of its M minutes`, and from 75% it is also a warning. Raise the limit, or split the job,
  when that warning starts appearing, not after the first timeout. Headroom on 2026-11-18: daily 68 to 96 of
  180, weekly 86 to 126 of 350, suite 17 to 28 of 45, bits 40 to 70 of 120.

## When a build goes red

**One issue, labelled `build-red`, is the place to look.** `alert.yml` keeps it in step with the newest relevant
run of the daily, the weekly, the tests and the canary on `latest_branch`. Pull-request runs and cancelled runs
don't count, except a cancellation by timeout, which does. For each red workflow, the issue gives:

- the failing step;
- the first error lines (every `FAIL` line, the parser's drift block, or what led up to the error);
- a link to the run;
- the suggested fix, when the failure is one the 2026-11-18 audit found;
- the canary's proposal, when one exists.

The issue is commented on only when a *new* failure arrives, which is what sends a notification. A failure
counts as new when its job, its kind or its quoted lines change, ignoring numbers. Every sweep rewrites the
body. When all four are green, the issue gets a comment and closes. The logic is `tools/ci_alert.py`. Run
`python tools/ci_alert.py --dry-run` to see what it would do now; it only reads. Add `--run <id>` to see how one
run would be reported.

The suggested fixes, by kind:

| Kind | What it printed | What to do |
|---|---|---|
| drift | `drift: placed ...` (the canary), or `N sections no category is named for` (a strict run) | Merge the canary's `bot/drift-<fingerprint>` PR, or add the lines to `taxonomy.SECTIONS` by hand. Until then the daily files them provisionally and still publishes |
| degraded | `drift: degraded ...` | A list could not be read properly: a failed pull, a shrink, a collapsed parse, a rename. No mapping fixes it; look at the list upstream |
| regenerate | a `FAIL` ending `-- run: python scripts/<stage>.py` | Merge the canary's `bot/regenerate` PR, or run that command and commit |
| conflict | `CONFLICT` | Re-run: the builds check out the branch head |
| timeout | `exceeded the maximum execution time` | See the budget line; raise the limit or split the job |
| quiet | `no tally printed` | A harness crashed before reporting, usually a page lost mid-call. Re-run once; harden it if it repeats |
| assertion | any other `FAIL` | Read it. A browser check that passed last time may be runner timing ([testing.md](testing.md)) |

### The canary

`canary.yml` runs every four hours, so drift is usually found before the 11:12 daily trips on it. It has two jobs.

- **drift** pulls every list fresh, with no cache: about 40 REST calls, plus the lists from
  raw.githubusercontent.com. It renders the scout's document offline and runs `10_parse_sources.py` with
  `AAA_PROVISIONAL=1`, as the daily does (see [pipeline.md](pipeline.md) for the provisional mode).
  - The parse writes `cache/drift-proposal.json` and `.md` (`drift.PROPOSAL`), and the job uploads them as the
    `drift-proposal` artifact.
  - `tools/drift_report.py` reads the proposal and prints one `drift:` line per placement and per degraded
    list; those are the lines the build-red issue quotes.
  - Placements are written in with `scripts/apply_drift_proposal.py` and pushed to `bot/drift-<fingerprint[:8]>`.
  - The job is red while there are placements or degraded lists.
- **regenerate** runs the stages listed in its `STAGES` (today only `22_detail`). They are the stages whose
  output depends only on committed files. If the output differs from what is committed, it pushes the result
  to `bot/regenerate`. This catches a generator change that was merged without its pages, as PR #104 was.

Each run rebuilds its proposal from `latest_branch`. It pushes only when the proposed files changed, and it
deletes the branch (closing its PR) once nothing is left to propose. A drift branch is named for `drift.py`'s
fingerprint, which stays the same for the same drift, so six runs a day over one unmerged drift make one branch
and one PR. A different drift opens a new branch and withdraws the old one. A job goes red while it has something
for a human to merge, which is what puts it in the build-red issue. `tools/bot_branch.py` does all the pushing
and refuses any branch that is not `bot/...`.

Opening the pull request needs the repository setting **"Allow GitHub Actions to create and approve pull
requests"**. When it is off, the branch is still pushed, and the job summary and the build-red issue carry a
one-click compare link instead. A PR opened by the Actions token runs no checks on itself. To see them before
merging, either run `gh workflow run tests.yml --ref bot/drift-<fingerprint>` (the run shows under Actions on that
branch, not as a check on the PR), or have a person close and reopen the PR, which does attach the checks to it.
Merging runs them on `latest_branch` regardless.

The canary stays out of `atlas-build` and never restores or saves the build cache. That cache holds every
screenshot and is gigabytes; one more entry would also count against the repository's 10 GB allowance.

### Why PR #104 merged unverified, and what stops it now

PR #104 came from a fork, from a first-time contributor. Its `tests.yml` run waited for approval and was closed
with **no jobs** when the PR merged. With no required checks, nothing stopped the merge. Three things now stand
in the way:

1. The push run after a merge is in the build-red issue within two hours.
2. The canary's regenerate job proposes the missing pages within four.
3. Two settings only the owner can change: a branch ruleset that requires the `suite` check on pull requests
   (the daily and weekly push directly, so GitHub Actions has to be allowed to bypass it), and a habit of not
   merging a PR that shows "workflows awaiting approval".

## Reproducing a build on a laptop

`tools/local_daily.py` runs the daily's stages, or the weekly's with `--workflow weekly`, in the workflow's
order, against the `cache/` in your worktree:

```bash
python tools/local_daily.py --list                    # the stages, by step
python tools/local_daily.py --from 10_parse_sources   # that stage and everything after it
python tools/local_daily.py --only 22_detail          # one stage (repeatable, or comma-separated)
python tools/local_daily.py --from 17_markdown --to 22_detail
python tools/local_daily.py --dry-run --from 19_pages # print the commands only
python tools/local_daily.py --cache ../aaa-cache      # keep cache/ outside the worktree (symlink or junction)
```

- **The stage list is read out of `daily.yml` itself.** Every `python scripts/...` line in a `run:` block is a
  stage, named for its script and flags (`02_fetch--force`, `12_scout--follow-renames`). A list kept anywhere
  else would drift from the workflow the first time someone added a stage.
- **It never runs** `26_indexnow.py` (that would tell search engines about live URLs) or
  `watch_sources.py --update` (that would record the build as done). It also leaves out the workflow's own
  shell: the gates, staging, committing and pushing.
- **The suite runs only with `--with-suite`**, and then with `AAA_SKIP=bits-check.mjs`. On a shared machine, set
  `AAA_ONLY` to the harnesses you need. The weekly's screenshot stages run only with `--with-shots`.
- **A cold cache means a full crawl**: about 1,200 GraphQL points and 800 REST calls through your own `gh` login.
  GitHub offers no API to download the runner's cache.
- **On a failure it stops** and prints the `--from` that resumes at the failed stage.
- **The stages write `docs/`, `mega-list/` and `state/` in your worktree.** At the end it says how many paths
  changed. `git restore docs mega-list state` (and `git clean -fd docs mega-list`) puts them back.

A typical drift reproduction is `--only pull_sources,10_parse_sources`. A page bug needs only the generators
over the committed data, for example `--from 17_markdown --to 27_semantic`.

## Adding a stage to the daily or the weekly

The workflows are owned by `eng-ci`. Other streams add stages to them like this:

1. **Add one line, `python scripts/NN_name.py`, to the step it belongs in.** Put fetches in "Fetch and classify";
   anything that writes `docs/` or `mega-list/` goes in "Build the Markdown edition and the site", before
   `24_pwa.py`, which has to come after every generator it hashes. Keep it a bare line, not inside an `if` or a
   heredoc, so `tools/local_daily.py` picks it up. Use the same line in `weekly.yml` if the weekly should run
   it too.
2. **Give it one fixed-path output.** The "Every tracked page was rewritten" step fails on a fixed path that no
   generator wrote, and only warns about a facet page.
3. **If it calls a network,** give it its own retries (look at `graphql_batch` in `02_fetch.py`) or wrap it in
   `bash tools/retry.sh 3`, but only if it can safely run twice. Raise the step's `timeout-minutes` if it adds
   more than a few minutes, and watch the budget line on the next runs.
4. **If its output depends only on committed files,** add it to `canary.yml`'s `STAGES`, and give it a churn
   assertion like `detail-churn.mjs`.
5. **Say in your PR** that it changes a workflow, and tell `eng-ci`. `ci_tools_test.py` asserts the daily's
   stage order, so add the stage's name to its `order` list.

### Pushes by a workflow do not run the tests

The daily and weekly builds push with `secrets.GITHUB_TOKEN`. GitHub starts no workflow runs for pushes
made with that token. That is why both builds run the suite themselves before committing, and why a
build commit on `latest_branch` shows no `tests.yml` check.

### tests.yml

This workflow runs on ubuntu-latest with Node 22 and Python 3.12.

- It installs no Python packages. The suite's Python harnesses are standard library only.
- It sets `AAA_CHROME_FLAGS="--no-sandbox --disable-dev-shm-usage"`, because a container has no user
  namespace to sandbox into.
- It runs as two parallel jobs: `suite`, every harness but `bits-check.mjs` (`AAA_SKIP`, 45-minute limit), and
  `bits`, that one alone (`AAA_ONLY`, 120 minutes). `bits-check` plays all 44 of the pals' bits and is over an
  hour on a runner on its own. The daily and weekly builds' own suites leave it out (`AAA_SKIP`): the bits
  are code, which this workflow checks on every push and pull request, not the data those builds change.
- On failure each job uploads `build-tmp/` as `test-screenshots-<job>`.
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
| `CF_BEACON_TOKEN` | `19_pages.py`, and through it `19d`, `20`, `22`, `25_collections` and `31` | Uses the token committed in `scripts/19_pages.py`. Setting it to `""` or `off` removes the beacon |
| `GOOGLE_SITE_VERIFICATION` | `19_pages.py` | No Search Console meta tag. **It was unset on 2026-09-25**, so the property is unverified |
| `INDEXNOW_KEY` | `19_pages.py`, `20_landing.py` (key file), `26_indexnow.py` | Uses the committed default key |
| `GITHUB_TOKEN` | every `gh` call, as `GH_TOKEN` | Supplied by Actions |

The workflows write these to `$GITHUB_ENV` only when a value exists. Declaring them in `env:` would set
them to `""` whenever they are unset, and for two of the four `""` means something different from unset.

## Caches and state

- **`cache/`** lives only in the GitHub Actions cache. Locally it is the gitignored `cache/` in your worktree (see
  [Reproducing a build on a laptop](#reproducing-a-build-on-a-laptop)). If it is evicted (7 days unused, or the 10 GB cap),
  the next weekly starts cold, and every daily skips until that weekly finishes its screenshots.
- **`state/*.json`** is committed. It holds the first-seen ledger, star history, Discover rotation and the dead-repo ledger, and
  must survive any cache loss. See [overview.md](overview.md#committed-state).

## Running a build by hand

On this team only the lead dispatches workflows, because a dispatch shares the `atlas-build` queue with the real
daily. Reproduce locally first (see above). Dispatch a workflow from the Actions tab, or run:

```bash
gh workflow run daily.yml --ref latest_branch -f force=true
gh workflow run weekly.yml --ref latest_branch
gh workflow run dead-repos.yml --ref latest_branch
```

Dispatching against a feature branch (`--ref your-branch`) rebuilds from that branch's scripts and pushes to
**that branch** (the builds push to `HEAD:${GITHUB_REF_NAME}`). This is the only way to see a
cache-dependent stage's real output before merging.

To check a finished run, use `gh run view <id>`. Do not rely on `gh run watch --exit-status`: it returns 0
when you attach to a run that has already failed.
