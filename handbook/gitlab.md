# GitLab projects

The atlas was built from GitHub: every source list lives there, and so does almost everything they link.
This page covers the second forge it reads, gitlab.com. It describes how a GitLab project is found,
identified, fetched, judged and shown, and the limits that shaped each choice. All of it sits behind
one feature flag, `intake.gitlab` in `config/app-flags.json`. The flag shipped `0`, and with it off no
GitLab row exists anywhere.

The module docstrings hold the detail: `scripts/hosts.py`, `scripts/gitlab_api.py`,
`scripts/12b_gitlab.py` and `scripts/11b_fetch_gitlab.py`. The tests are in `tests/gitlab_test.py`.

## Identity: the host-qualified `nwo`

A GitHub row's `nwo` is `owner/repo`, as it always was. A GitLab row's `nwo` is the host followed by
the project's full path:

```
gitlab.com/gitlab-org/ai/duo-workflow
```

The two forms can never collide. A GitHub owner cannot contain a dot, and every host name has one, so
`hosts.host_of(nwo)` is a test of the first segment and needs no lookup.

Every store keyed by `nwo` takes a GitLab row without a schema change:

- `cache/meta.json`;
- `cache/readmes/gitlab.com__group__project.md`;
- `docs/data.json` and `docs/live.json`;
- `state/first-seen.json` and `state/dead-repos.json`.

A separate `host` column would have had to reach every one of those keys, and any key that forgot it
would collide silently. The cost is that an `nwo` can now have more than one slash. So code asks
`hosts.owner_of` and `hosts.name_of` rather than splitting on the first slash, and builds every URL
through `hosts`:

| Need | GitHub | GitLab |
|---|---|---|
| project page | `https://github.com/o/r` | `https://gitlab.com/g/s/p` |
| raw file | `raw.githubusercontent.com/o/r/HEAD/f` | `gitlab.com/g/s/p/-/raw/HEAD/f` |
| social card | `opengraph.githubassets.com/1/o/r` | none (see "Pictures" below) |
| detail page | `docs/repo/o/r/` | `docs/repo/gitlab.com/g/s/p/` |

Detail pages sit one directory per segment, so a GitLab page is deeper than three. `22_detail.Repo`
computes its own depth (`rel`, `up`), and `20_landing.repo_path` and the pages' `detailURL` use the
same rule: one lower-cased, slugged segment per `nwo` segment.

## How a project gets in

There are two ways in, the same two that exist for GitHub.

- **The GitLab scout, `12b_gitlab.py`.** It is a synthetic source, `gitlab` in `SOURCES`, built the way
  `12_scout.py` is. It searches gitlab.com by topic and by word, judges each result, and writes the
  survivors into `state/gitlab-repos.json`. From that file it renders `cache/sources/gitlab.md`, which
  the parser reads like any other list. The source is sticky, advisory (in `taxonomy.ADVISORY`), and
  files projects by `12_scout.section_of` into the scout's ten sections.
- **A curated list that links a gitlab.com project.** `10_parse_sources.repo_of` reads such a link as a
  repository, through `hosts.from_url`. On 2026-11-18 the 39 lists linked two gitlab.com projects
  (`elementfm/mcp`, `tldv/tldv-mcp-server`). Both were filed as websites until now.

### The rules

The rules are `12b_gitlab.verdict`, and they mirror the scout's.

| Rule | GitLab version |
|---|---|
| fork | GraphQL `isForked` |
| archived | `archived` (and the search asks for `archived=false`) |
| mirror | see below |
| no description, spam | the scout's `SPAM` and `SPAM_TOPICS` |
| list | "awesome" in the path or the display name. These are candidate *sources*, kept under the ledger's `lists` key |
| off-topic | the scout's `agentic()` on the path and the display name, never on topics alone |
| the bar | 5+ stars and activity in the last 365 days, **or** 25+ stars and created since 2023 |

The bars are GitLab's own, not the scout's. On 2026-11-18 the most-starred project tagged `ai-agents`
had 352 stars. GitHub's 300-star floor would have admitted almost nothing.

### Mirrors

Many GitLab projects are mirrors or imports of a GitHub repository, and the atlas already has the
GitHub side. An anonymous read cannot see GitLab's own `mirror` flag, so `mirror_of` judges from what
anyone can see:

1. The description says "mirror of" or "mirror from" (the scout's `MIRROR`).
2. The first 1,500 characters of the README say "mirror", "read-only copy" or "moved to" next to a
   github.com link.
3. The project's own last two path segments are a GitHub repository the atlas already indexes.
4. The README's opening links a GitHub repository with the same name, and the atlas already indexes it.

Rules 3 and 4 are about the atlas rather than about mirroring. A GitLab twin of an indexed repository
would be the same project twice, whichever side is the copy.

## The rate limit, and why the scout rotates

Anonymous gitlab.com is capped per IP. Three limits are documented: 500 requests a minute, 400 a
minute for `/projects`, and the one that binds, **about 60 an hour**. On 2026-11-18, about fifty
requests into the first local scan, every endpoint started answering 429 under
`ratelimit-name: unauthenticated_traffic_per_ip`, with `Retry-After` set to the top of the hour.

A CI runner shares that cap with every other job on the same egress IP. So the stages are built to
work without a token and to stay frugal:

- **`gitlab_api.Client` fails fast.** A `Retry-After` longer than two minutes raises at once, instead
  of holding the daily job for an hour.
- **Anonymous runs rotate.** An anonymous run takes one slice of the query rotation, starting at an
  offset set by the day and stopping after `ANON_BUDGET` (40) requests. Over a few days the sticky
  ledger accumulates the whole sweep. Merging is monotone except where a returned result proves a
  drop, so a partial run is as safe to keep as a whole one.
- **Enrichment is filtered.** GraphQL is asked about forks and READMEs only for the projects
  `prejudge` says could qualify.
- **The fetch falls back to the last good answer.** `11b_fetch_gitlab.py` uses the last good answer
  for any project it could not read this run. A project that has never been read is left out of the
  build by `14_classify_all.py`; it is not published as broken.
- **A token makes it immediate.** With `GITLAB_TOKEN` set, as a `read_api` personal access token from
  any free account, the limit is 2,000 a minute and every run asks every query. The workflows pass
  `secrets.GITLAB_TOKEN` when it exists. Adding the secret is the owner's decision.

## Metadata: GitLab's answers in GitHub's names

`11b_fetch_gitlab.py` writes each project into `cache/meta.json` under the field names GitHub's
GraphQL uses, so every later stage reads a GitLab row unchanged. Two of the fields are worth knowing:

- **`pushedAt` is GitLab's `lastActivityAt`.** GitLab counts issues and merge requests as activity,
  not only pushes. So "pushed" on a GitLab row means "last active".
- **`licenseInfo` is recognised from the LICENSE file's text** (`license_of`). GitLab's GraphQL has no
  licence field, and REST's `?license=true` costs one request per project. Text it cannot place is
  `NOASSERTION`, which is what GitHub says in the same case.

Releases and Actions are GitHub-only, so `13_signals_all.py` skips GitLab rows. A GitLab row's platform
verdict comes from its README alone.

## How a GitLab row looks

All of this uses existing theme tokens only (`--band`, `--grid`, `--ink2`):

- **The marker.** Wherever a row shows its path, it shows the project path without the host, followed
  by a neutral `.forge` pill reading "GitLab". This applies to catalogue rows, facet pages, Discover
  cards and the detail page header. Outward links say "GitLab" where a GitHub row's say "GitHub".
- **Pictures.** GitLab has no social card. A project's `og:image` is its avatar, or GitLab's logo when
  it has none. So a GitLab row shows its own README picture if it has one. With none, it shows the
  no-preview fallback on the catalogue, an empty cell on facet pages, and no Screenshot section on its
  detail page. It never shows a GitHub card for a repository
  GitHub has never heard of. The catalogue renders a GitLab row's own picture even though GitHub rows
  use the bounded social card (JFH-218). There are few GitLab rows, so the cost stays bounded by their
  number.
- **The repository reader.** The reader on a GitHub detail page is driven by GitHub's Contents API.
  GitLab's Markdown renderer needs a signed-in user on gitlab.com, so a GitLab page shows a link to the
  README on GitLab instead.

## Dead projects

`dead_repos.py` asks gitlab.com about every GitLab row, by GraphQL full path and then by REST: 404 means
gone, and 200 means alive, because GitLab redirects a moved project's old path. A GitLab read that fails
keeps every GitLab entry in the ledger as it was, and the GitHub half of the scan is written as usual.

## Self-hosted GitLab instances: out, for now

These instances were probed on 2026-11-18 with the same word searches: framagit.org, salsa.debian.org,
gitlab.freedesktop.org, invent.kde.org, gitlab.gnome.org and gitlab.torproject.org. Nothing agentic
cleared even the 5-star bar except `salsa.debian.org/deeplearning-team/debgpt` (11 stars). Salsa's
hits were mostly Debian packaging of GitHub projects, and the `agent` hits on the others were system
agents (SPICE, polkit, Akonadi). The identity scheme already supports another host
(`hosts.HOSTS`, `from_url`), so adding one later is a matter of a URL pattern and a client base URL.

## Turning it on

1. Set `"intake.gitlab": 1` in `config/app-flags.json`.
2. Optionally, ask the owner for a `GITLAB_TOKEN` repo secret. Without it, the first full sweep takes
   a few days of daily runs to accumulate.
3. The next daily run scouts, fetches and publishes. The GitLab scout's document is a new synthetic
   source, so its first digest counts as a move and the run builds.
