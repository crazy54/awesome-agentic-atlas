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
light/dark button on the other pages, and worn on every page. The design language is **neumorphism (soft
UI)**: every surface is the page's own colour, and light is the only thing that makes it an object. A raised
surface casts a dark shadow down and to the right and catches a highlight up and to the left; a pressed one
has the same pair inside it. Nothing has a visible border and nothing is translucent.

| What | Treatment | Tokens |
|---|---|---|
| Cards, panels, menus, dialogs, the pinned search bar | raised | `--raise` |
| Chips, buttons, the build tags, the logo's disc | raised; lifted on hover; pressed while held | `--raise-sm`, `--raise-hi`, `--press` |
| Search boxes, inputs, selects, code wells, tracks | pressed in | `--press` (`--press-sm` for small badges in dense rows) |
| The active chip, tab or nav item | pressed in, with the accent as its ink | `--press`, `--bar` |
| The one primary button | Archie's lime, raised, with its glow | `--act`, `--onact`, `--act-edge`, `--glow` |

| `data-theme` | What it is | Notes |
|---|---|---|
| `dark` | A cool charcoal base (`#24272D`), near-white ink, the lime for the active state, glows, progress and key numbers | on `:root`, so it is the JavaScript-off floor |
| `light` | A cool grey-white base (`#E3E7ED`), navy-graphite ink, the lime deepened to an olive wherever it is text | the bright lime appears only as a fill (`--act`) |

**The top nav is a segmented control.** Every page family writes its own header nav as runs of plain links,
and `sitewide.segnav()` turns each run into a raised track (`.seg`) on the way out, with the page the reader
is on pressed into it (`aria-current="page"`, and put back as the first item when the page leaves itself
out). Icon-only controls -- the Settings gear, the shelves' arrows, the catalogue's platform filters -- are
round 44px buttons (`.iconbtn`), with their word kept as visually hidden text. Both are `NAV_CSS`.

**Type.** Geist, on a larger and heavier scale: display titles 34px at 750 (38px on a project page), section
titles 20px, star counts 18px at 750, project names 16px at 650, and small caps for labels tracked wide.

**Archie never covers the page.** When he follows a reader off the homepage he docks at the bottom right, and
`html.archie-docked` reserves his slot as a right gutter (900px and up), so nothing scrolls under him.

**The v2 beta** wears the same soft UI by default: `30_v2.py` builds its `soft` and `soft-light` skins from
`sitewide.PALETTE` and `GLASS`, and keeps its three older skins in the picker.

The accent is rationed, the way the reference designs ration theirs: titles and body text are the neutral
inks. The masthead behind Archie is light, not a picture: the base's own highlight and a faint lime glow
where he stands.

The reader's choice is `localStorage["theme"]`: `light` or `dark`. **System**, the default, stores
nothing; then `prefers-color-scheme` picks light or dark, and the page follows the OS live. A small script in
`<head>` (`sitewide.HEAD_THEME`) settles it **before first paint**, so a returning reader never sees a flash
of the wrong theme.

**Accessibility is automatic, not a menu item.** Soft shadows carry no contrast, so a reader whose system
asks for more gets something else in their place, in either theme:

- `prefers-contrast: more`: no soft shadows and no field; real 1px edges on controls; text lifted to 7:1,
  lines to 3:1; links underlined; a 3px focus ring; a pressed control outlined as well as pressed in.
- `prefers-reduced-transparency: reduce`: no field.
- `forced-colors: active` (Windows High Contrast): the system palette, with focus rings, pressed states and
  button edges kept as outlines.

A stored `contrast` (the old third theme) is rewritten to `dark` by the head script and by `atlasTheme()`.
The old skin keys (`atlas-skin`, `atlas-unlock`) are deleted on a reader's first visit.

**Contrast.** Every surface is the base, so `theme_test.py` measures every text token against the base and
against the field's worst point (in dark, the top-left highlight, which lifts the base towards the ink).
Every pair clears WCAG AA; the strengthened modes clear AAA.

**One copy.** Every token, the pre-paint script and the paint-only shared rules (the field, the focus ring,
the controls, the lime button, the wells, the strengthened modes, forced colours, Archie's fog prank) are
`THEME_CSS`, `HEAD_THEME` and `THEME_JS` in `scripts/sitewide.py`. The catalogue (`19_pages.py`), `pages.css`
(`20_landing.py`) and `detail.css` (`22_detail.py`) drop them in; nothing else declares a colour token.
Three rules for new UI:

- Use the tokens, never a hard-coded colour, so both themes and the strengthened modes apply
  automatically. A panel or card is `--surface` with `--raise`; a control is `--surface` with `--raise-sm`,
  `--raise-hi` on hover and `--press` while pressed or on; a well is `--surface` with `--press`; the primary
  action is `--act` with `--onact` ink. Borders the layout already has stay, in `transparent`. Status is
  `--good` / `--warn` with a word or a mark beside it, never colour alone.
- **Theme rules change paint, not layout.** Colours, backgrounds, border colours and radii, outlines,
  shadows and text decoration; never a size, a padding, a border width, a weight, a transform or a
  position. `theme_test.py` enforces that for the shared rules; `cards-check.mjs` measures real layout in
  both themes.
- Nothing is blurred: soft UI is opaque, and `theme_test.py` holds that no rule asks for `backdrop-filter`.

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

`24_pwa.py` writes `docs/sw.js` and `docs/manifest.webmanifest`, and copies the icons in from `art/brand/`
(cut from Archie's tile by `art/brand/build.py`, which needs Pillow and is run by hand). One of the icons is
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
