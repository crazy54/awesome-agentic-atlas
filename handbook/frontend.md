# The website front end

The site is static HTML with CSS and JavaScript written by Python generators. There is no front-end
framework and no build step. Two consequences:

- **To change a page, change its generator and re-run it.** Hand edits to `docs/` are overwritten on the
  next build.
- **The generator owns the whole file.** Each page family below has exactly one owning script.

## Page families

Counts were measured on 2026-09-25 with `find docs/<dir> -name index.html | wc -l`.

| URL | File(s) | Owner | Notes |
|---|---|---|---|
| `/` | `docs/index.html` | `31_home.py` | The homepage: shelves, the daily spotlight, the Discover strip, Archie. It also forwards old `/#filter` links to `catalog/`; `deeplinks_test.py` guards that |
| `/catalog/` | `docs/catalog/index.html` | `19_pages.py` | The filterable catalogue: every row of `data.json`, card and table views, compare, export, the constellation, semantic search |
| `/topic/<slug>/`, `/topic/<slug>/target/<slug>/` | 166 pages | `20_landing.py` | The 14 topics and the topic × target crossings that clear a minimum size |
| `/target/<slug>/` | 12 pages | `20_landing.py` | One per target harness |
| `/repo/<owner>/<name>/` | 8,858 pages, plus `/repo/` | `22_detail.py` | One per project, with the in-page README reader. Names are slugged so every path is legal on Windows |
| `/collections/…` | 6 pages | `25_collections.py` | Curated picks from `config/collections.json`. Rebuilt weekly only |
| `/discover/` | `docs/discover/index.html`, `discover/cards/*.json` | `19d_discover.py`; `31_home.py` writes the cards | Fifty a day |
| `/v2/…` | prototype pages | `30_v2.py` | The redesign lab. On demand only, and not linked from the nav |
| feeds, sitemaps | `feed.xml`, `feed.json`, `sitemap*.xml`, `robots.txt` | `21_feeds.py`, `20_landing.py`, `22_detail.py` | |
| data | `data.json`, `live.json`, `discover.json`, `search/*`, `build.json` | `19`/`25_velocity`, `19c`, `19d`, `27`, `31` | `data.json` is a public API; its schema is in the root README |

`docs/pages.css` is the stylesheet shared by the homepage and the facet, collection and discover pages. `20_landing.py` writes it.
The catalogue and the detail pages do not link it: the catalogue inlines its CSS, and detail pages use `repo/detail.css`.

### Shared chrome

The masthead, navigation, theme menu and footer are generated separately by several scripts, and are
kept consistent by tests rather than by a shared template. Adding a nav link therefore means editing
five generators:

- `19_pages.py`
- `20_landing.py`
- `22_detail.py`
- `25_collections.py`
- `31_home.py`

Then re-run each of them and `24_pwa.py`, or `detail-churn` and the page probes go red.

## Themes and skins

Two independent attributes on `<html>` control appearance:

| Attribute | Values | Stored in | Default |
|---|---|---|---|
| `data-theme` | `light`, `dark` | `localStorage["theme"]` | follows `prefers-color-scheme` until the reader picks one |
| `data-skin` | `graphite`, `glass`, `terminal`, `prism`, `sherbet`, `riso`, `blueprint`, `aurora` | `localStorage["atlas-skin"]` | `graphite` |

A small script in `<head>` sets both **before first paint**, so a returning reader never sees a flash of the
wrong theme.

The skins' colour tokens are defined in `scripts/19_pages.py` and copied **byte for byte** into the page
families that do not import it: `pages.css` from `20_landing.py`, and `22_detail.py`. `theme_test.py`
fails if the copies drift, so change the source in `19_pages.py`, then regenerate every copy.

## Feature flags

`config/app-flags.json` holds 16 on/off switches, every one `1` on 2026-09-25. The `index.*` flags are read
by `19_pages.py` for the catalogue, and the `detail.*` flags by `22_detail.py`. Flags are fixed at build time:

- `22_detail.py` omits a disabled section from the HTML.
- `19_pages.py` bakes some flags into the markup and embeds all of them as JSON, which the catalogue's
  script checks.

Either way, editing the file changes nothing until the page is regenerated. The full reference is
[`config/README.md`](../config/README.md).

- **Validate:** `scripts/app_flags.py` checks the file against `config/app-flags.schema.json` on every
  load, so a typo fails the build instead of silently enabling something.
- **Edit locally:** `python scripts/flags_app.py [--port N] [--no-open]` serves a small editor. Its writes
  are atomic.
- **Override the path:** set `AAA_APP_FLAGS=/path/to/flags.json`, for experiments.
- **Re-render:** `scripts/apply_flags.py`, or the flags app's **Save & render** button, which calls it.
  It writes the catalogue, `docs/catalog/index.html` (`19_pages.CATALOG`), and leaves the homepage alone.
  Until that is fixed, restore the homepage afterwards with `python scripts/31_home.py` followed by
  `python scripts/24_pwa.py`. Also check that `docs/catalog/index.html` really changed: `apply_flags.py`
  does not write the catalogue at all. Its detail-page and service-worker steps (`22_detail.py`, `24_pwa.py`) are correct.

## The PWA and the service worker

`24_pwa.py` writes `docs/sw.js`, `docs/manifest.webmanifest` and the icons. The worker keeps four caches:

| Cache | Holds | Policy |
|---|---|---|
| `atlas-shell-<VERSION>` | the precache: `./` (that is `index.html`), `manifest.webmanifest`, `pages.css` | Installed up front. Replaced wholesale when `VERSION` changes |
| `atlas-data` | `data.json`, `live.json`, `discover.json` | Network first. A cached answer is marked so the page can say "offline, showing data from …" |
| `atlas-pages` | pages the reader has visited | Network first, capped at 30 entries |
| `atlas-assets` | detail-page CSS/JS and the semantic index files | Network first, created on first use |

Everything under `docs/assets/` (Archie and the rig) is deliberately **not** handled by the worker. It is
versioned by a `?v=` query string instead; see [archie.md](archie.md#after-editing-archie).

### The versioning rule

`VERSION` is the first 12 hex characters of a SHA-256 over the precached files. Line endings are
normalised from CRLF to LF first, so Windows and Linux compute the same hash. When the version changes,
returning readers get the new shell; while it is unchanged, they keep the old one.

> **Any change to `docs/index.html`, `docs/pages.css` or `docs/manifest.webmanifest` must be followed by
> `python scripts/24_pwa.py`, and the new `docs/sw.js` must be committed in the same change.**

If you skip it, returning readers keep the old homepage. `pwa-check.mjs` fails with "the worker's
VERSION is a hash of the bytes it precaches", and its message names the command to run. The CI builds
always run `24_pwa.py` after `31_home.py`, so only hand-made changes can miss it.

## Analytics and verification

- **Cloudflare Web Analytics:** a beacon on every page family, with the token committed in `19_pages.py`.
  See [ci-cd.md](ci-cd.md#configuration-variables-and-secrets) for overrides.
- **IndexNow:** the key file `docs/<key>.txt`, written by `20_landing.py`.
- **Google Search Console:** a meta tag, emitted only when `GOOGLE_SITE_VERIFICATION` is set. It was unset on 2026-09-25.

`docs-notes/JFH-198-analytics-events.md` is an investigation note from 2026-09-06 on whether custom analytics events are possible.
