# tests/

```
node tests/run.mjs
```

That is the whole thing. It finds a Chromium the machine already has, serves `docs/` on a port the OS picks,
runs nineteen harnesses in turn, prints what each one asserted, and exits non-zero if anything failed. About
one minute, most of it in detail-page regeneration and browser layout checks. No install step, no arguments,
no configuration.

It asserts on `docs/` as committed, not on the generator's intentions. `docs/` is served verbatim by GitHub
Pages — `build_type: legacy`, so what is in the repository is what a reader downloads — which means the bytes
in the checkout are the deployable artefact and are the honest thing to test.

Individual harnesses can be run alone. The three that drive a browser need to be given one and told where the
site is, because `run.mjs` owns both:

```
python tests/theme_test.py
python tests/app_flags_test.py
python tests/signals_test.py
python tests/indexnow_test.py
python tests/newness_test.py
python tests/discover_test.py
node tests/probe.mjs
python tests/pagemin_test.py
python tests/media_test.py
python tests/workbook_branding_test.py
python tests/refresh_test.py
python tests/live_test.py
python tests/semantic_test.py
python tests/collections_test.py
python tests/osicons_test.py
node tests/detail-churn.mjs
node tests/detail-preview-check.mjs <chrome-binary> <origin>
node tests/cards-check.mjs <chrome-binary> <origin>
node tests/pwa-check.mjs   <chrome-binary> <origin>
```

## What each one covers, and what it deliberately does not

There are nineteen files rather than one because they are nineteen instruments, and the overlap between them is the
reason to keep them apart rather than the reason to merge them. Each file's header says at length what it
cannot see; this is the summary.

| harness | what it covers | what it cannot see |
| --- | --- | --- |
| `theme_test.py` | The palette, which is now two axes: four themes — graphite, glass, terminal, prism — times light and dark, so eight token sets rather than two. WCAG contrast on every one of them, run through the same role map and the same floors, so a new theme cannot be cheaper to add than the default was to keep; that all eight declare the same thirteen tokens and no others, and that no two share a `--surface`, which is what stops a theme being the default repainted under a new selector. Consistency across the generated surfaces: the region is compared byte for byte between `19_pages.py`, `20_landing.py` and `22_detail.py`, and the colours used by social cards and app icons are pinned to graphite-dark, which is what holds that theme at `:root`. Then the structural half — `--ui`, `--wash`, `--panel`, `--bdf` — including that graphite's four defaults are the page exactly as it shipped, and that the one translucent token, `--panel`, carries its own block's `--plane` channels, so a composite still lies between two backdrops that were measured. Then the enumeration, in both directions: the pre-paint script's theme map names exactly the themes that have blocks, each literal in it matches that block's `--plane`, the Settings menu offers exactly those names, each swatch shows its own theme's surface, action and link in that order, exactly one is pressed in the markup, and the panel is hidden by the attribute rather than by CSS — and that an *open* one outranks the pinned bar, which is not the same claim as being displayed, and is the one the first version of this got wrong: the panel was `display:block` with `aria-expanded="true"` and two thirds of it behind the search field. Asserted as the relationship between three z-indexes rather than as the number 30, and with the base `header` rule required to stay *below* the bar, because `probe.mjs` reads the pinned-over-scrolling order off that rule and is right to. 623 assertions. | Whether the result looks good, and whether a theme reads as the thing it is named after. Contrast is a ratio and a skin is a judgement: glass keeps a frosted panel and a coloured wash, but its hairline border is `--grid` rather than the prototype's translucent white, which flattened to 1.146 on `--band` and would have failed the floor. Browser layout checks cover the rendered page, and `probe.mjs` reads the last *published* `index.html` rather than this source, so it lags a build. |
| `app_flags_test.py` | The standard application-flag schema, its strict integer `1`/`0` vocabulary, human descriptions, atomic conflict-safe writes from the control panel, and real all-OFF renders through both site generators. | A deployed build workflow or another application's schema. The controller's multi-app registry is deliberately independent of Atlas. |
| `probe.mjs` | Runs the page's own script from `docs/index.html` under a stub DOM against the real `docs/data.json`, then asserts on the HTML it renders: ranking, the search fallback, the hash round-trip, the palette, the theme colour, the cards stylesheet, the saved set and the link that carries it, the map chip declining a browser whose canvas has no 2D context while the export chip beside it still switches on, the detail links the rows point at — lowercased, and rewritten wherever a repository name would otherwise ask Windows for a directory it cannot create — and the page as shipped text. Then `docs/discover/`, where one card is rendered by two renderers in two languages: the page's `DISCOVER CORE` block is evaluated on its own — no DOM, no fetch, no clock — and held to the fixtures `docs/discover.json` carries for exactly that purpose, that it reads the same UTC instants as the same Chicago dates `zoneinfo` does, that its `forDay()` lands on the same cohort as `discover.for_day()` for three weeks of dates straddling the plan, and that its `cardHTML()` is byte-identical to the stage's `card_html()` on all fifty cards of a built day and on three hand-written rows covering the arms those fifty never reach. 437 assertions. | Computed layout. There is none in Node, so it can tell you a clamp rule is spelled correctly and not that anything clamps. |
| `cards-check.mjs` | Real layout in a real browser over HTTP at 1440, 900 and 375 px in both themes: how many cards are across, the screenshot's aspect ratio, horizontal overflow, scroll and focus survival across a view switch, the DOM work a switch does counted against the re-render it avoids, and the clamp's behaviour. Also Archie's commentary: that a hovered project's fact renders in at most two lines, that no string the generator can produce for any committed row makes the box exceed two lines -- the box, not the line boxes a `line-clamp` still reports for text it is clipping, which is a count of the runner's fonts rather than a defect -- that walking the rendered rows until every one of Archie's five data-driven wordings has actually been heard finds all five and finds nothing the restated templates cannot produce, that the sixth -- a name clipped to fit -- is asked of the longest name in the whole atlas, fetched through the reader's own search box rather than left to whichever rows the corpus happens to put on page one, that the bubble clears both the navigation and the filter bar at 1440 and again at 900 where the masthead reflows, that his name tag is two lines at 1440 and one unwrappable word at 375 and at the 640px boundary itself, with the full name still on `aria-label` and nothing overflowing the 44px tap target the pill's box is pinned to, that setting the bubble's `hidden` attribute still removes its box rather than merely satisfying the seven assertions that read the attribute, that it is absent at 640px and below where there is no band to put it in, that a reader who enlarges the navigation past what any stylesheet here chooses keeps every link rather than the bubble, and that it leaves with the pointer, with focus, and with Escape rather than staying pinned over the masthead. Then the page once it has scrolled, which every measurement above deliberately avoided: that nothing covers the search box, that the pinned band leaves the results most of the screen, and that a click where the box is drawn lands in it (JFH-354). And where keyboard focus lands when the browser, not the reader, chooses the scroll position: `--pin` at least as tall as the measured bar at five widths in both views, eighteen dispatched Shift+Tabs at each of two widths in both views with `elementFromPoint` at each focused control's own centre, the skip link driven for real, and the pinned bar's own controls asserted to have no scroll margin at all (JFH-356). Then Discover's carousel, which is a scrolling rail and not a transformed track: fifty cards on one line at 1440 and one card at 390 with no document-level horizontal scroll at either, geometry expressed in card widths and snap points rather than in exact offsets — a mandatory snap keeps nudging the rail after a smooth scroll ends, 31px on the run that taught this, so an equality on `scrollLeft` is the wrong assertion and a restarted roll is a screenful — Next, Back and the arrow keys, the roll advancing on its own and not restarting under a keypress, the `New` pulse read off computed style rather than off a CSSOM walk, `prefers-reduced-motion` stopping both the roll and the pulse while leaving the rail scrollable, the deep link the homepage strip sends landing on its own card, a link to a day that has since rolled over saying so instead of silently showing today's, and the grid view surviving a reload. Writes screenshots to `build-tmp/`. 189 assertions. | Any prefixed spelling this browser has an unprefixed implementation of. `-webkit-line-clamp` is the case that bit: this Chrome does the standard `line-clamp`, so a rule missing `display:-webkit-box` clamps perfectly here and is inert in Firefox. That half lives in `probe.mjs`. |
| `pwa-check.mjs` | Manifest, service worker registration and scope, the precached shell, the worker's `VERSION` recomputed from the bytes actually being served, the caching of every file in `DATA_FILES` — `data.json` and `live.json` both, by the route rather than by an exact filename — offline rendering with *both* the page and the worker taken offline, the freshness stamp reading the cached data's own date rather than the document's, and a 404 navigation that must not be cached. Then a real detail page, offline: that it renders the same star count and last push it rendered online, which is the claim JFH-282 made true and the one this file used to carry a paragraph explaining it could not make — the page under test is chosen for a repository whose `live.json` row has both figures, because 24 of the 1,294 rows have an empty push date and a missing figure would otherwise pass. That both sub-resources are in `atlas-assets` and that nothing else is, so the cache is bounded by `PAGE_ASSETS` rather than by a cap. And that a reader who has opened no detail page has no such cache at all. 43 assertions. | The paths this browser does not take: it supports navigation preload, so the worker's fallback for browsers that do not is never exercised. Nor the 156 prerendered facet pages, whose own snapshot lines have no data fetch to read a date out of. Nor `PAGES_MAX` eviction: the cap is asserted nowhere, and a detail page is cached by the same navigation route as a facet page, so the two share it. |
| `detail-churn.mjs` | Regenerates all 1,294 detail pages four times into scratch directories and compares SHA-256 trees: determinism, that a day of moving star counts and push dates rewrites nothing, that editing one curated blurb does move its page, and that committed `docs/repo` matches a fresh regeneration. 13 assertions over 1,298 files. | Whether the pages are any good. It never opens one. It also cannot see churn from any other stage — `20_landing.py` rewrites 156 facet pages on every run by design, and that is not what this measures. |
| `detail-preview-check.mjs` | Opens a real detail page in Chromium while fulfilling the GitHub API at the browser boundary with a deterministic README, SKILL.md and repository tree. Verifies rendered Markdown is the default, raw source is secondary, nested Markdown discovery and prioritisation, active-markup stripping, repository-relative URLs, typography, dark/light colour tokens and phone layout. | GitHub's live availability and anonymous rate limit. The fixture uses the same media types and response shapes, but deliberately spends no network quota and cannot prove an upstream repository still exists. |
| `pagemin_test.py` | `scripts/pagemin.py` against the cases the real page does not contain: template literals, `${}` substitutions, regex literals, unterminated blocks, strings that look like comments, and the whole template loaded live out of `19_pages.py`. 47 assertions. Written and owned by the JFH-204 author. | Everything about the page that is not comment stripping. |
| `indexnow_test.py` | `scripts/26_indexnow.py` and `20_landing.py`'s key-file prune. That `url_for`'s mapped set is exactly the `<loc>` set of the two sitemaps — 1,458 URLs, asserted both directions and by content rather than by count, so a page that stops being submitted and a page submitted without ever reaching a sitemap are both red. That the prune deletes a rotated `INDEXNOW_KEY` file and leaves `robots.txt`, `security.txt` and anything else whose name and content disagree. And that `IncompleteRead`/`BadStatusLine` out of the opener is a workflow warning and exit 0 rather than a traceback, including the class hierarchy that turns on. 140 assertions. | Anything on the wire. `socket.connect` is replaced with a counter that raises and the count is asserted to be zero, so the endpoint is always a stub — no key is ever validated and no real submission is ever made. Nor whether Bing does anything with what it is sent. |
| `media_test.py` | `scripts/media.py` against a synthetic workbook of the real one's shape: that a plain `wb.save` writes one media part per *placement*, that the pool collapses those to one part per distinct picture, that nothing else in the package changes, and that every drawing relationship still resolves to a part that is present — asserted against the archive itself rather than against a reading of openpyxl. Then the entry-count projection against the 65,535-entry ZIP ceiling, written down as arithmetic that can be re-run instead of re-argued. 49 assertions. | Whether Excel draws the shared part in every cell it is anchored to: it reads the package with `zipfile` and `openpyxl`, and no spreadsheet application opens it. Nor the real workbook — stages 14+ need a crawl that is not committed, so the shape is a miniature. |
| `workbook_branding_test.py` | A disposable pair of light/dark covers from `scripts/16_build_all.py`: both shared source assets exist, both covers embed exactly the compact logo and Archie artwork, their displayed bounds and upper-right anchors stay fixed, the mascot keeps its name tag, the theme-switch cell survives, and each archive contains one drawing part with two media parts. It also checks the package-preserving fallback used when the crawler cache is absent. 26 assertions. | The release-sized workbooks: their full data and screenshot cache are not committed, so this harness proves the cover builder and fallback without requiring a crawl to test two small cover images. |
| `signals_test.py` | `scripts/signals.py`, the rule deciding when a cached release-asset or `action.yml` answer needs re-querying: every term of it at its boundaries, every timestamp spelling that reaches those files, every earlier schema still loading and reading as stale, and a textual tripwire that the three fetch stages still consult it and still stamp what they write. 210 assertions, no I/O, instant. | Whether GitHub answers the queries. The three stages shell out to `gh api graphql`, so the crawl itself is untested here and untestable offline — this harness only asserts which repos would be asked about. |
| `newness_test.py` | `scripts/newness.py`, the rule that decides what `New` means on four surfaces: that it is the most recent import which brought anything rather than the last fortnight, that the next import to bring anything takes the mark off the previous cohort while leaving its dates alone, that an import bringing nothing moves neither, that a source list read for the first time is a real cohort rather than back-dated founding stock, and the stale bound on both sides of its boundary. Run against a ledger in a scratch directory several imports deep, with the date supplied rather than read from the clock. 54 assertions, instant. | Whether the surfaces render what it computes. It imports no stage: the chip, the outline and the two feeds read `COHORT` and `SEEN`, and that reading is `probe.mjs`'s and `refresh_test.py`'s half. |
| `discover_test.py` | `scripts/discover.py`, the daily-fifty rule: fifty projects a day, seven days a deploy, rolled over at 00:00 in one named zone. Run over eight consecutive weeks against synthetic corpora shaped to break it — a category with fewer rows than its allocation, more categories than slots, a corpus smaller than one day — with the date supplied rather than read from the clock and the ledger repointed into a temp directory. Nine groups: the day (both 2026 DST switches and the hour UTC has turned over and Chicago has not, with the expected dates written out by hand, because taking them from the module would only prove it agrees with itself); the shape; the split (`allocate()` sums to the day's slots and never starves a live category); fairness (every category in every day, no row twice in a week, no overlap between consecutive weeks); rotation (this week's picks at the back of next week's queue, asserted as a trajectory over eight weeks rather than one comparison); blindness (three shuffles and a star permutation each produce a byte-identical plan, because a Discover that consulted stars would be the front page with a different heading); the fallback (`covers()`, `for_day()`, and the ledger's format on disk); the copies (the four clock functions that exist twice, in `19d_discover.py` and in the homepage strip in `19_pages.py`, compared character for character off the two files as text, plus the accents, the flag, the deep link's two halves, and the stage being in both workflows); and the payload (the real `docs/discover.json` — columns against `CARD_COLS`, every pick backed by a row, no row carried that no day names, the ledger's week matching the plan's). 143 assertions, instant. | Whether the page renders what it computes, or whether the fifty are any good. The carousel, the deep link into it and the rollover in a browser are `probe.mjs`'s and `cards-check.mjs`'s half. The homepage strip is asserted here as *source* rather than as built output, because `19_pages.py` needs CI's crawl cache: the committed `docs/index.html` in any checkout predates whatever was last changed about the strip. |
| `refresh_test.py` | The staleness guard in `scripts/19b_refresh.py` — the only render path that works without the crawl cache, and the one that renders a live template over committed rows. Constructs the disagreement the guard exists for: the `listed_by` reader on every shape it comes in, a fabricated `SOURCES` one list too long and one too short, what the refusal says, `main()` three times against a scratch `docs/` with `reversion()` stubbed so a broken guard cannot reach the deployable tree, and the hazard itself — drop a row from the committed data and the rendered count and star total both move while `__LISTS__` beside them, filled from the live `SOURCES` rather than from the rows, does not. 74 assertions, ~1 s. | Whether a real crawl would produce the labels it counts. Stages 14+ need a crawl that is not committed, so the source count is inferred from the committed rows — it measures "lists that produced at least one row", not "lists configured". |
| `live_test.py` | `scripts/19c_live.py`, the star/push sidecar the 1,294 detail pages fetch in place of `data.json` — 21,791 B gzipped against 162,473, which is the largest measured saving in the site. That its key set and the set of detail pages are identical in *both* directions, so a page with no stars and a key with no page are both red rather than silent. That it resolves its three columns by name and hard-stops on a missing one, because `25_velocity.py` appends columns after `19_pages.py` writes the file and a positional read would quietly shift. That the serialisation is byte-stable — sorted keys, no line endings — since a file that reshuffles itself would show up as churn in a commit rather than as a failure here. And the three hard stops: a missing `snapshot`, a duplicate `nwo`, an absent column. Then the page set itself, on the platform most of this repository is edited on: that no row in the dataset and no directory committed under `docs/repo/` slugs to a path Windows cannot check out. A component ending in a dot, or named for a DOS device, is not a file NTFS refuses to create quietly — `git worktree add` aborts on the whole tree, so two rows out of 8,856 made the repository unclonable here until the slug rule started rewriting them. 105 assertions, ~2 s. | Whether the numbers are true. They are copied from `docs/data.json`, so a stale crawl is faithfully reproduced — this asserts the sidecar and the index agree, not that either is current. Nor the fetch itself: `detail.js` reading it is `pwa-check.mjs`'s and `probe.mjs`'s half. |
| `semantic_test.py` | `docs/search/` — six files — scored using only what a reader downloads: no numpy, no model, no build stage imported. Nine groups: the shape (every file's length agrees with `meta.json`'s declared row and token counts, including the int8 matrices that carry no dimension headers — a wrong `dims` reinterprets the whole matrix at an offset); the guard (SHA-256 of the 1,294 `nwo` values compared to `meta.json`'s fingerprint, because an index built against a different `data.json` returns each project's *neighbour* confidently with no error anywhere); the arithmetic (documents dequantise to unit length, and the two int8 scales are separate — a shared scale crushed all 1,294 document vectors onto a handful of distinct values in the first build, with unrelated projects tying to three decimal places); the vocabulary (every ASCII word is segmentable, and the shipped stoplist holds no topical word while holding the ones that matter); the tokeniser (the stage writes its own segmentation of eight strings into `meta.json` as `probe`, and this file's transcription must reproduce every one of them slot ordinal for slot ordinal — `tests/probe.mjs` does the same against the page's copy); the map (`xy.bin`, the coordinates the constellation is drawn from, has to be a picture rather than a scatter — of the eight rows nearest a project on screen, the share sharing its curated `cat` must close a fifth of the gap between what two random rows would share and 1.0, and the rows `near.bin` calls neighbours must land measurably closer than strangers; the *share of the gap* rather than a multiple of chance, because chance moves with the category distribution and a multiple of it silently demands more purity every time the corpus concentrates — the largest category went from 21% of rows to 51% in a single import, which took chance from 11.7% to 29.0% and failed a floor nothing had regressed under); the retrieval (8 natural-language queries scored on what a reader sees — of the ten rows each query returns, how many name the topic it asked about, totalled across all eight — never on a similarity, and no longer on one fixture repository's rank either, because at 8,856 rows a rank measures how crowded that project's neighbourhood is); the chatter (twelve topicless questions — "please help me choose", "is this any good" — must produce no tokens and therefore no answer, and four queries that wrap chatter around a real topic must keep the topic); and the regression (five of the eight queries return nothing at all under the page's current substring filter, which is what makes the retrieval group measure the *index* rather than the filter; the ones that have stopped being zero-result are printed, because a growing corpus eventually answers a two-word query by accident). 47 assertions. | Whether the vectors are *good*. Ranking quality is bounded by how much text each row carries; a cold `cache/readmes/` build is honestly weaker than a warm one, so the retrieval group asserts a total across eight queries rather than demanding every one of them land, and prints each fixture repository's own rank as context rather than asserting on it. |
| `collections_test.py` | `scripts/25_collections.py` and `config/collections.json` — the one editorial surface on the site, where a wrong number is a recommendation that is not true printed under a heading that says trust us. So mostly it tests the machinery that refuses to publish one: the committed curation resolving against the committed `docs/data.json` (every `nwo` exists, every `requires` holds, no slot filled twice), each refusal fired separately against a mutated copy, "N of M lists" counting the lists that actually contributed rows rather than `len(SOURCES)` — 11 and 39 on this checkout, and the second makes a false sentence of every pick's evidence line — the rendered pages and their share links, the `mega-list/` twins carrying the same picks in the same order, and the wiring: the URLs reaching `docs/sitemap.xml`, every page linked from somewhere a reader can get to, and a workflow actually running the stage, which none did from 18d373a until it was asserted. 651 assertions. | Whether the picks are *good*. Nothing here can see that; it can only check that every claim printed beside them is one the dataset supports. It writes nothing under `docs/` or `mega-list/` — the renderers are pure functions of two loaded dicts, and `main()` and `prune()` are never called. |
| `osicons_test.py` | The five platform marks — Windows, WSL2, macOS, Linux, Docker — after `scripts/osicons.py` replaced the words with pictures on four surfaces at once. Three failures here are invisible rather than broken, and each has a group: a `<use>` with no matching `<symbol>` renders *nothing*, so every `<use href="#…">` on every built page under `docs/` is resolved against the symbols in that same document, walking the whole tree because the failure is per-document and a sample proves nothing about the 1,293 pages it skips; the marks pair with platforms *by position*, so `check()` is fired on a reorder, a rename, a truncation, an extension and the empty list, and the pairing is re-checked in the built page where the symbol id and the platform name sit next to each other; and a picture is nothing to a reader who cannot see it, so every mark on a page of each family is walked up to its nearest naming ancestor — `title`, `aria-label` or a visually-hidden word, whichever that surface uses — and the words are asserted gone from the compact places and still present in the explanatory ones. 251 assertions. | Whether a mark reads as the platform it means. A penguin is a penguin to a person and a path to a test; that judgement was made by looking at all five rendered at 96px and at 13px in both themes, and is not automatable here. |

Between them, 3,157 assertions, from a real run rather than by adding up the figures above. The number only
matters in one direction — see the floors below. Twelve are red on the tree this sentence was written on, and
they are worth naming rather than leaving a total to imply otherwise, because a reader who finds a red suite
and no account of it cannot tell which failures are expected: eleven in `cards-check.mjs` are the instrument
rather than the page — CDP's synthetic pointer does not land on a row, which reproduces under
`chrome-headless-shell` on a workstation as well as on a runner, so it is not runner flakiness; and one is
`semantic_test.py`'s map extent. Neither is a claim about the palette or the shelves, and neither was
introduced here. This paragraph said seventeen until the Discover top-up merged: five of them were one day
publishing forty-nine picks under a heading promising fifty, and they went green on a merge rather than on
anything done here, which is the argument for re-running the suite to write this number instead of adjusting
it by hand. The two that were red here for months were
`probe.mjs`'s, and they were red because it reads a `docs/index.html` that `19_pages.py` alone
can rebuild, and that stage needs the crawl cache CI has and a checkout does not. The blind spot is still
there — a change to the index's source is green here and unmeasured by `probe.mjs` until a build lands, and
the whole of `theme_test.py` exists on the other side of that line, reading `scripts/19_pages.py` as text
precisely so it does not have to wait for one. So a green run on a checkout means every harness agrees with
the tree; it does not mean the published page has caught up with it. See `probe.mjs`'s own header,
`scripts/devfixture.py` for the local render that closes most of the gap, and `19b_refresh.py` for why the
other local render path refuses when the committed rows and the configured source lists disagree.

Every one of them compares bytes, counts, geometry or text. None of them measures a duration, and that is
deliberate: `cards-check.mjs` asserted the view switch was cheaper than the re-render it avoids by racing two
wall clocks, and failed on one run in three on an unchanged tree at a 2.5% margin (JFH-223). It now counts the
work instead — rows constructed, rows kept, mutation records under `#out` — which is the same claim stated so
that it cannot depend on how busy the machine is. If you are ever tempted to assert on elapsed time here, the
question to answer first is what you would be counting instead.

## No dependencies, and why that is a constraint rather than an oversight

There is no `package.json` here, no lockfile, and nothing to install. The harnesses use Node's standard
library and a Chromium the machine already has:

- Node has a global `WebSocket` and a global `fetch`, which between them are all the Chrome DevTools Protocol
  needs. `lib/browser.mjs` speaks CDP directly.
- `node:http` is all a static server needs. `lib/serve.mjs` is 90 lines including its comments.
- The browser is found, never installed. `lib/browser.mjs` is a port of `scripts/chrome.py`'s search order, so
  a machine that can build this site can run these tests.

The reason: this site has no build step and nothing from npm is ever served to a reader. A devDependency here
would be the first `package.json` in the repository, would need a lockfile, would need renovating, and would
turn "can I run the tests" into a question with a network answer. The cost is that these files own their own
plumbing — about 200 lines of it, in `lib/`. That is the trade, and it is deliberate.

The fourteen Python harnesses are Python because the things they test are. `python` here means whatever
`lib/python.mjs` finds. Node's side needs no packages, and neither do `app_flags_test.py`, `theme_test.py`,
`pagemin_test.py`, `signals_test.py`, `indexnow_test.py`, `newness_test.py`, `discover_test.py`,
`refresh_test.py`, `live_test.py`, `collections_test.py`, `osicons_test.py` and `semantic_test.py` — standard
library only, except that `indexnow_test.py` also needs `git` on `PATH`, because it asserts against the
*tracked* paths under `docs/` rather than a walk of the working tree, so that a local build's leftovers cannot
change what it thinks the site contains. `media_test.py` and `workbook_branding_test.py` — the two that
build a real `.xlsx` — need `openpyxl` and `pillow`, which are the
generator's dependencies rather than the suite's — every workflow that needs them installs them, `tests.yml`
included, so a checkout that can build the workbook can already test it. Missing them is an `ImportError` with no tally,
which `run.mjs` counts as a failure and not as a skip.

## A harness that skips must not be able to pass

This is the rule the suite is built around, because it has already been broken once: `pagemin_test.py` located
a fixture with a path that stopped resolving when the file moved, took its `if exists` else-branch, stopped
running seven assertions, printed a note naming a directory it was not looking in — and exited 0. Nothing was
red. From outside, a suite that checked everything and a suite that checked nothing produce the same exit code,
and the exit code is all CI reads.

So `run.mjs`:

- exits 2 before running anything if no Chromium or no Python 3 is found, with the list of places it looked and
  the two cheapest fixes. A missing prerequisite stops the run; it never reduces it.
- counts a harness that printed no tally, or a tally of zero assertions, as a failure whatever it exited.
- carries a per-harness floor on the number of assertions expected. It is a floor and not a pin: adding
  assertions costs nothing and never trips it, and only a harness that has *lost* assertions goes red. If you
  delete assertions on purpose, lower the floor in the same commit — that is the point at which somebody should
  have to think.

The same shape is worth watching for inside the harnesses. `[].every(...)` is `true`, so any assertion of the
form "every result satisfies X" passes when there are no results, which is usually the exact failure it was
written to catch. Four in `probe.mjs` had that shape and now carry an explicit non-emptiness conjunct; if you
add another, add the conjunct.

## Where this runs

`.github/workflows/tests.yml` runs `node tests/run.mjs` on pull requests, on pushes to `latest_branch`, on
Mondays at 07:40 UTC, and on demand. Until that file existed the suite was only ever run by hand, so every
harness here was a test of the moment it was written rather than a test of the repository. Its own header
comment carries the long version of what follows.

Three things about it are worth knowing before you read a green tick as a fact about the site:

- **The daily build's commits do not trigger it.** `daily.yml` pushes with `secrets.GITHUB_TOKEN`, and GitHub
  starts no workflow runs for pushes made with that token. So the thirty commits a month that rewrite
  `data.json`, `index.html`, `sw.js` and 156 facet pages — all four of which this suite asserts on — are
  unverified when they land, and since Pages serves `latest_branch` verbatim, landing is publishing. The
  Monday run closes that within seven days rather than within one. Running the suite inside `daily.yml`
  before its commit step would close it properly, at the cost of letting a failed assertion block the deploy;
  that is a decision about the site rather than about a test runner, so it is not made here.
- **Exit 2 means the suite never ran.** The workflow annotates 1 and 2 differently on purpose. 1 is this
  suite doing its job — an assertion failed, or a harness went quiet. 2 is `run.mjs` refusing to start
  because it found no Chromium or no Python 3, which is a fact about the runner and not about the code, and
  sending somebody to read a diff over it wastes the trip.
- **There is no `paths` filter.** `lighthouse.yml` next door can name the files that change the page it
  measures; this suite asserts on `docs/`, on `scripts/` and on the relationship between them, so a filter
  would be a hand-maintained list of nearly the whole repository. Getting one wrong produces the single
  outcome this suite exists to prevent: a check that quietly did not run, which from outside is
  indistinguishable from a check that passed.

No browser is installed there. `ubuntu-latest` carries two on `PATH` — `/usr/bin/chromium` and
`/usr/bin/google-chrome` — and `launch()` passes `--headless=new` unconditionally, so either needs no flag
from the workflow; installing one would be a ~130 MB download on every run. The browser is found, never
installed, which is the policy `lighthouse.yml` already states. `ON_PATH` order means the one actually used
is **chromium**, which on that image is a snap shim rather than Chrome, and `CHROME_PATH` is deliberately not
set to pin it: the value of running this anywhere is that it is not the laptop the suite went green on, and
choosing the closest available browser to that laptop would buy agreement by construction. The one setting CI
does need is `AAA_CHROME_FLAGS: --no-sandbox --disable-dev-shm-usage`, for the reason in the table below.

### What the first CI run found, which is the argument for having one

This suite was green on every machine that had ever run it, and red on `ubuntu-latest` the first time a
runner tried. Two defects, both in `tests/` rather than in the site, and neither findable from one platform:

- `lib/browser.mjs` waited 15 seconds for Chrome to write `DevToolsActivePort`. The first browser launch of
  a CI run took 15.6, so the first browser harness died having asserted nothing. The budget is 60 now, and
  the reason is variance rather than a floor: the same launch on the same image took 15.6 s, then 48.2 s,
  then 16.8 s. There is no number to sit just above, and a timeout is not a sleep — a browser ready in
  300 ms is not charged for the ceiling.
- `pwa-check.mjs`'s offline helper called `Target.attachToTarget` on every invocation, and that opens a
  *new* session rather than returning the existing one. Seven calls left seven sessions on the service
  worker with conflicting network conditions, so whether the worker came back online depended on how a
  particular Chrome merges them. `chrome-headless-shell` 1223 takes the last write and passed; Chromium 152
  does not, and six assertions failed — the first genuinely, the other five as consequences of a worker that
  was never let back online. One session per target now, and the harness went from 18.5 s red to 2.9 s green.

Both are the shape this suite already warns about, one level up: not an assertion that stopped biting, but an
assertion that could not run. Three green local runs proved nothing about either, because the thing that was
wrong was the same on all three machines. If you add a harness, the question this section exists to prompt is
which of its numbers are properties of the code and which are properties of the laptop you wrote it on.

## Environment

Nothing is required. All of these are escape hatches.

| variable | effect |
| --- | --- |
| `CHROME_PATH`, `CHROMIUM_PATH`, `PLAYWRIGHT_CHROMIUM` | Name the browser binary instead of searching. First one set wins. |
| `PYTHON` | Name the interpreter instead of probing `python`, `python3`, `py`. |
| `AAA_CHROME_FLAGS` | Extra flags for every browser launch, space separated. `--no-sandbox --disable-dev-shm-usage` on a CI container. |
| `AAA_TMP` | Where scratch profiles and generated trees go. `run.mjs` sets this for its children. |
| `AAA_ARTIFACTS` | Where screenshots go. Defaults to `build-tmp/`, which is gitignored. |
| `AAA_PAGE` | Point `probe.mjs`'s text scans at a different HTML file. A development hatch for working on `pagemin.py`; the page script cannot boot from an unsubstituted template. |

Ports are never hardcoded. The static server binds `127.0.0.1:0` and Chrome gets
`--remote-debugging-port=0`, with the real port read back out of `DevToolsActivePort` in its profile
directory. Two runs can overlap, and a run will not fight another session for a port or kill a process it does
not own. Every browser gets a fresh profile under one scratch root, which is what makes the cold-visit
assertions in `pwa-check.mjs` mean the same thing on the second run as on the first.

Cleanup is three-layered, because a browser process left running is worse than a failed test: each launch
registers a `process.on("exit")` hook that kills its child and removes its profile, each harness closes its
browser on the way out, and `run.mjs`'s `finally` sweeps any pid a hard-killed harness left behind and removes
the scratch root — retried, because Windows holds a profile open for a moment after the process dies.

## One thing that will make a green suite go red for no reason

Do not run a build while the suite is running. `pwa-check.mjs` caches the shell and `data.json` in a real
service worker and then asks for them with the network emulated off; if `docs/data.json` is rewritten between
those two moments, the offline navigation renders zero rows and the run goes red with `the atlas still renders
with the network off -- 0`. That happened once during development, on a working tree where another session was
regenerating `docs/` at the same time, and it was not a page defect — the same commit was green immediately
before and twice immediately after.

It fails in the safe direction, and it is not worth serving a snapshot to avoid: the fix is to let the build
finish. Worth knowing so that the message is recognised rather than investigated.

## Watching it fail

A test suite nobody has watched fail is not known to work. Five cheap ways to check this one still bites:

- Give a template a timestamp. Add `datetime.now()` to anything `scripts/22_detail.py` renders and
  `detail-churn.mjs` reports `two runs over identical data write identical bytes -- 1,295 file(s)`, then
  restore it.
- Break a scoping rule. Copy `docs/index.html`, delete an `html[data-view=cards]` prefix from one selector in
  the copy, and run `AAA_PAGE=/path/to/copy node tests/probe.mjs`. The scope assertion names the offending
  selector.
- Widen a staleness term. Change `MAX_AGE_DAYS = 30` to `= 45` in `scripts/signals.py`, or drop the
  `_raced_ci` call out of `reason()`, and `signals_test.py` names the boundary that moved. Delete
  `scripts/__pycache__/` first: `= 30` and `= 45` are the same number of bytes, so an edit inside one mtime
  tick reuses the old bytecode and the suite reports the result of code you have already changed.
- Neuter the guard. Change `if implied == live:` to `if True:` in `scripts/19b_refresh.py` and
  `refresh_test.py` reports 21 failures naming the refusal that never came, then restore it. Delete
  `scripts/__pycache__/` first, for the reason above.
- Unsort the sidecar. Change `dict(sorted(repos.items()))` to `dict(repos.items())` in
  `scripts/19c_live.py` and `live_test.py` reports 4 failures — the key order, the row order reaching the
  bytes, and byte-identity with the committed file in both of the places it is asserted — then restore it.
  Same `__pycache__` note.
- Make the view switch rebuild the list. Add a `render()` call to the `#view` button's `onclick` in
  `docs/index.html` — the regression the toggle exists to avoid — and `cards-check.mjs` prints
  `a switch built 120 row(s) and kept 0 of 120 on screen` and reports four failures: the three counting
  assertions and the focus-survival one beside them. Then restore it. This is the assertion that used to be
  a wall-clock comparison, so it is the one most worth re-watching.

None needs the repository dirtied for long, and the second needs nothing tracked touched at all.
