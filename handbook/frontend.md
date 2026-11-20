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
| `/local/` | `docs/local/index.html` | `32_local.py` | The local-AI page (working title "Run It Local"): pick your machine, see which models run on it and how to run them. Data from `config/local-ai/` (ds-hardware's catalogue, ds-models' picks), with `localhw.mjs` and `localfit.mjs` vendored from them, all inlined so it works offline once visited. The name and slug are `sitewide.LOCAL_PAGE` |
| `/alike/` | `docs/alike/index.html` | `33_alike.py` | Lookalikes: paste a GitHub or GitLab link, or type a project's name (or describe what it does), and see the projects that do the same thing, each with the reason it is there. Ranked in the browser from `data.json` and `docs/search/` with the shared encoder `scripts/semantic.js`; a project the atlas does not hold is looked up anonymously from the reader's browser (GitHub's REST API, 60 an hour; GitLab's v4 API) and its README read from `raw.githubusercontent.com`. `?repo=<nwo>` and `?q=<text>` are the shareable states; every detail page's **Find alternatives** links `?repo=`. Static bytes, so the daily rewrites it identically. Offline after one visit through the existing worker routes. The name and slug are `sitewide.ALIKE_PAGE`. The ranking's weights and the measurements behind them are at the top of `scripts/alike_page.js` |
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

`19d_discover.py` writes a nav too. The local-AI link is in all of these except `22_detail.py`, whose
nine thousand pages are held byte-identical week to week; it reads its label and slug from
`sitewide.LOCAL_PAGE`, so a rename is one edit. The Lookalikes link sits beside it in the same five navs,
from `sitewide.ALIKE_PAGE`; a detail page instead carries a **Find alternatives** link in its actions row
(beside "Find it in the atlas", same `.alt` class), pointing at `alike/?repo=<nwo>` for that row.

### One query encoder, two pages

The tokeniser, forward pass and staleness guard for `docs/search/` are `scripts/semantic.js`. The catalogue
(`19_pages.py`, at `__SEMJS__`) and Lookalikes (`33_alike.py`) both inline it, stripped, byte for byte;
`tests/alike_test.py` asserts both generators carry exactly one copy and that neither keeps a private
transcription. Change it there, and remember the other two copies of the algorithm are Python
(`27_semantic.py`, the reference, and `tests/semantic_test.py`), held to it by the `probe` fixtures in
`meta.json`.

Then re-run each of them and `24_pwa.py`, or `detail-churn` and the page probes go red.

## Themes

Two themes, Light and Dark, chosen in the Settings menu (on the catalogue and the homepage) or with the
light/dark button on the other pages, and worn on every page. The design language is **neumorphic glass**:
frosted, translucent panels that blur a field of the mascot's colours behind them, soft surfaces raised out
of that field by a pair of shadows (one light, one dark), pill-shaped controls, and pressed states that are
pushed *in*. The palette is Archie's: egg-shell ceramic, graphite, lime, iris light, steel and brass.

| `data-theme` | What it is | Notes |
|---|---|---|
| `dark` | A dark, dark grey with a faint lime glow; graphite glass; egg-shell (`#EBE5DA`) text; the lime for titles (`--title`), accents and lines | on `:root`, so it is the JavaScript-off floor |
| `light` | White frosted glass over a field of egg-shell with iris-light and lime pools; graphite ink; a deepened lime for text | the bright lime appears only as a fill (`--act`) |

The reader's choice is `localStorage["theme"]`: `light` or `dark`. **System**, the default, stores
nothing; then `prefers-color-scheme` picks light or dark, and the page follows the OS live. A small script in
`<head>` (`sitewide.HEAD_THEME`) settles it **before first paint**, so a returning reader never sees a flash
of the wrong theme.

**Accessibility is automatic, not a menu item.** There used to be a third theme, High contrast. What it
did is now keyed on what the reader's system says, in either theme:

- `prefers-contrast: more`: solid panels, no blur, no field, no soft shadows; text lifted to 7:1, lines to
  3:1; links underlined; a 3px focus ring; a pressed control outlined as well as filled; no art behind text.
- `prefers-reduced-transparency: reduce`, and browsers without `backdrop-filter`: solid panels, no blur.
- `forced-colors: active` (Windows High Contrast): the system palette, with focus rings, pressed states and
  button edges kept as outlines.

A stored `contrast` is rewritten to `dark` (the half it was) by the head script and by `atlasTheme()`.
There used to be a second axis too, eight colour "skins" (`data-skin`, `localStorage["atlas-skin"]`). The head
script deletes `atlas-skin` and `atlas-unlock` on a reader's first visit; their light or dark half is
already in `theme`.

**The glass and its contrast.** Text on glass is read against the glass composited over what is behind it,
so `theme_test.py` measures every text token against the *effective* background, worst case: a static panel
(`--panel`) over the field's darkest (light) or lightest (dark) point, and a floating one (`--panel-hi`: the
pinned bar, menus, dialogs) over pure black or pure white, because anything can scroll under it.

**Blur is rationed.** `backdrop-filter:var(--bdf)` sits on a bounded set of large surfaces (headers, footers,
the pinned bar, menus, dialogs, the homepage's spotlight and daily line), never on a rule that draws per row
or per card, and `theme_test.py` holds that list. Two traps, both measured: a backdrop filter makes its box
the containing block of every `position:fixed` descendant (a blurred `.subbar` dragged the phone filter sheet
330px up the page), and a stacking context (which would trap the local page's suggestion list under the next
step). Cards are translucent and raised, but not blurred.

**One copy.** Every token, the pre-paint script and the paint-only shared rules (the field, focus ring, the
controls, the lime button, the strengthened modes, forced colours, Archie's fog prank) are `THEME_CSS`,
`HEAD_THEME` and `THEME_JS` in `scripts/sitewide.py`. The catalogue (`19_pages.py`), `pages.css`
(`20_landing.py`) and `detail.css` (`22_detail.py`) drop them in; nothing else declares a colour token. The
token names, values and ratios for other streams are in the team's `tokens.md`, and `theme_test.py` checks
every pairing the stylesheets use. Three rules for new UI:

- Use the tokens, never a hard-coded colour, so both themes and the strengthened modes apply
  automatically. A panel is `--panel` with a `--edge` border and `--raise` (or `--raise-sm`) shadow; a
  control is `--band` with a `--ctl-edge` border and `--raise-sm`; a well (input, code) is `--press`; a
  primary filled control is `--act` with `--onact` ink and a `--act-edge` inset edge; status is
  `--good` / `--warn` with a word or a mark beside it, never colour alone.
- **Theme rules change paint, not layout.** Colours, backgrounds, border colours and radii, outlines,
  shadows, backdrop filters and text decoration; never a size, a padding, a border width, a weight or a
  position. Every glass edge and neumorphic rim is a `box-shadow` or a border *colour*. `theme_test.py`
  enforces that for the shared rules; `cards-check.mjs` measures real layout in both themes, and the theme
  work's box-for-box diff (every element on six page families, both themes, 1440 and 375) found nothing moved.
- Only blur what the list above allows; translucency alone looks the same over the soft field.

## Feature flags

`config/app-flags.json` holds 17 on/off switches. The 16 `index.*` and `detail.*` ones were all `1` on
2026-09-25; the `index.*` flags are read by `19_pages.py` for the catalogue, and the `detail.*` flags by
`22_detail.py`. The 17th, `intake.gitlab`, is a data switch rather than a page one: read by `scripts/hosts.py`,
it decides whether gitlab.com projects are indexed at all, and it shipped `0` (see
[gitlab.md](gitlab.md)). Turning it on changes what the *next build* reads,
not just how a page renders, so it takes a daily or weekly run to show. Flags are fixed at build time:

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

`24_pwa.py` writes `docs/sw.js`, `docs/manifest.webmanifest` and the icons. One of the icons is
`docs/favicon.ico`, which no page links but browsers and crawlers ask the domain root for. The worker keeps
four caches:

| Cache | Holds | Policy |
|---|---|---|
| `atlas-shell-<VERSION>` | the precache: `./` (that is `index.html`), `manifest.webmanifest`, `pages.css` | Installed up front. Replaced wholesale when `VERSION` changes |
| `atlas-data` | `data.json`, `live.json`, `discover.json` | Network first. A cached answer is marked so the page can say "offline, showing data from …" |
| `atlas-pages` | pages the reader has visited | Network first, capped at 30 entries |
| `atlas-assets` | detail-page CSS/JS and the semantic index files | Network first, created on first use |

Everything under `docs/assets/` (Archie and his pals) is deliberately **not** handled by the worker. It is
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

## Verification

- **IndexNow:** the key file `docs/<key>.txt`, written by `20_landing.py`.
- **Google Search Console:** a meta tag, emitted only when `GOOGLE_SITE_VERIFICATION` is set. It was unset on 2026-09-25.
