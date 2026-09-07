# tests/

```
node tests/run.mjs
```

That is the whole thing. It finds a Chromium the machine already has, serves `docs/` on a port the OS picks,
runs ten harnesses in turn, prints what each one asserted, and exits non-zero if anything failed. About 37
seconds, of which 22 are the detail-page regeneration. No install step, no arguments, no configuration.

It asserts on `docs/` as committed, not on the generator's intentions. `docs/` is served verbatim by GitHub
Pages — `build_type: legacy`, so what is in the repository is what a reader downloads — which means the bytes
in the checkout are the deployable artefact and are the honest thing to test.

Individual harnesses can be run alone. The two that drive a browser need to be given one and told where the
site is, because `run.mjs` owns both:

```
python tests/signals_test.py
python tests/indexnow_test.py
node tests/probe.mjs
python tests/pagemin_test.py
python tests/media_test.py
python tests/refresh_test.py
python tests/live_test.py
node tests/detail-churn.mjs
node tests/cards-check.mjs <chrome-binary> <origin>
node tests/pwa-check.mjs   <chrome-binary> <origin>
```

## What each one covers, and what it deliberately does not

There are ten files rather than one because they are ten instruments, and the overlap between them is the
reason to keep them apart rather than the reason to merge them. Each file's header says at length what it
cannot see; this is the summary.

| harness | what it covers | what it cannot see |
| --- | --- | --- |
| `probe.mjs` | Runs the page's own script from `docs/index.html` under a stub DOM against the real `docs/data.json`, then asserts on the HTML it renders: ranking, the search fallback, the hash round-trip, the palette, the theme colour, the cards stylesheet, the saved set and the link that carries it, and the page as shipped text. ~276 assertions. | Computed layout. There is none in Node, so it can tell you a clamp rule is spelled correctly and not that anything clamps. |
| `cards-check.mjs` | Real layout in a real browser over HTTP at 1440, 900 and 375 px in both themes: how many cards are across, the screenshot's aspect ratio, horizontal overflow, scroll and focus survival across a view switch, the toggle's cost against the re-render it avoids, and the clamp's behaviour. Writes screenshots to `build-tmp/`. ~47 assertions. | Any prefixed spelling this browser has an unprefixed implementation of. `-webkit-line-clamp` is the case that bit: this Chrome does the standard `line-clamp`, so a rule missing `display:-webkit-box` clamps perfectly here and is inert in Firefox. That half lives in `probe.mjs`. |
| `pwa-check.mjs` | Manifest, service worker registration and scope, the precached shell, the worker's `VERSION` recomputed from the bytes actually being served, the caching of every file in `DATA_FILES` — `data.json` and `live.json` both, by the route rather than by an exact filename — offline rendering with *both* the page and the worker taken offline, the freshness stamp reading the cached data's own date rather than the document's, and a 404 navigation that must not be cached. 37 assertions. | The paths this browser does not take: it supports navigation preload, so the worker's fallback for browsers that do not is never exercised. Nor the 156 prerendered facet pages, whose own snapshot lines have no data fetch to read a date out of. |
| `detail-churn.mjs` | Regenerates all 1,294 detail pages four times into scratch directories and compares SHA-256 trees: determinism, that a day of moving star counts and push dates rewrites nothing, that editing one curated blurb does move its page, and that committed `docs/repo` matches a fresh regeneration. 7 assertions over 1,298 files. | Whether the pages are any good. It never opens one. It also cannot see churn from any other stage — `20_landing.py` rewrites 156 facet pages on every run by design, and that is not what this measures. |
| `pagemin_test.py` | `scripts/pagemin.py` against the cases the real page does not contain: template literals, `${}` substitutions, regex literals, unterminated blocks, strings that look like comments, and the whole template loaded live out of `19_pages.py`. 48 assertions. Written and owned by the JFH-204 author. | Everything about the page that is not comment stripping. |
| `indexnow_test.py` | `scripts/26_indexnow.py` and `20_landing.py`'s key-file prune. That `url_for`'s mapped set is exactly the `<loc>` set of the two sitemaps — 1,452 URLs, asserted both directions and by content rather than by count, so a page that stops being submitted and a page submitted without ever reaching a sitemap are both red. That the prune deletes a rotated `INDEXNOW_KEY` file and leaves `robots.txt`, `security.txt` and anything else whose name and content disagree. And that `IncompleteRead`/`BadStatusLine` out of the opener is a workflow warning and exit 0 rather than a traceback, including the class hierarchy that turns on. 140 assertions. | Anything on the wire. `socket.connect` is replaced with a counter that raises and the count is asserted to be zero, so the endpoint is always a stub — no key is ever validated and no real submission is ever made. Nor whether Bing does anything with what it is sent. |
| `media_test.py` | `scripts/media.py` against a synthetic workbook of the real one's shape: that a plain `wb.save` writes one media part per *placement*, that the pool collapses those to one part per distinct picture, that nothing else in the package changes, and that every drawing relationship still resolves to a part that is present — asserted against the archive itself rather than against a reading of openpyxl. Then the entry-count projection against the 65,535-entry ZIP ceiling, written down as arithmetic that can be re-run instead of re-argued. 44 assertions. | Whether Excel draws the shared part in every cell it is anchored to: it reads the package with `zipfile` and `openpyxl`, and no spreadsheet application opens it. Nor the real workbook — stages 14+ need a crawl that is not committed, so the shape is a miniature. |
| `signals_test.py` | `scripts/signals.py`, the rule deciding when a cached release-asset or `action.yml` answer needs re-querying: every term of it at its boundaries, every timestamp spelling that reaches those files, every earlier schema still loading and reading as stale, and a textual tripwire that the three fetch stages still consult it and still stamp what they write. 210 assertions, no I/O, instant. | Whether GitHub answers the queries. The three stages shell out to `gh api graphql`, so the crawl itself is untested here and untestable offline — this harness only asserts which repos would be asked about. |
| `refresh_test.py` | The staleness guard in `scripts/19b_refresh.py` — the only render path that works without the crawl cache, and the one that renders a live template over committed rows. Constructs the disagreement the guard exists for: the `listed_by` reader on every shape it comes in, a fabricated `SOURCES` one list too long and one too short, what the refusal says, `main()` three times against a scratch `docs/` with `reversion()` stubbed so a broken guard cannot reach the deployable tree, and the hazard itself — drop a row from the committed data and the rendered count and star total both move while `__LISTS__` beside them, filled from the live `SOURCES` rather than from the rows, does not. 74 assertions, ~1 s. | Whether a real crawl would produce the labels it counts. Stages 14+ need a crawl that is not committed, so the source count is inferred from the committed rows — it measures "lists that produced at least one row", not "lists configured". |
| `live_test.py` | `scripts/19c_live.py`, the star/push sidecar the 1,294 detail pages fetch in place of `data.json` — 21,791 B gzipped against 162,473, which is the largest measured saving in the site. That its key set and the set of detail pages are identical in *both* directions, so a page with no stars and a key with no page are both red rather than silent. That it resolves its three columns by name and hard-stops on a missing one, because `25_velocity.py` appends columns after `19_pages.py` writes the file and a positional read would quietly shift. That the serialisation is byte-stable — sorted keys, no line endings — since a file that reshuffles itself would show up as churn in a commit rather than as a failure here. And the three hard stops: a missing `snapshot`, a duplicate `nwo`, an absent column. 100 assertions, ~2 s. | Whether the numbers are true. They are copied from `docs/data.json`, so a stale crawl is faithfully reproduced — this asserts the sidecar and the index agree, not that either is current. Nor the fetch itself: `detail.js` reading it is `pwa-check.mjs`'s and `probe.mjs`'s half. |

Between them, roughly 983 assertions. The number only matters in one direction — see the floors below.

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

The six Python harnesses are Python because the things they test are. `python` here means whatever
`lib/python.mjs` finds. Node's side needs no packages, and neither do `pagemin_test.py`, `signals_test.py`,
`indexnow_test.py`, `refresh_test.py` and `live_test.py` — standard library only, except that `indexnow_test.py` also needs
`git` on `PATH`, because it asserts against the *tracked* paths under `docs/` rather than a walk of the working
tree, so that a local build's leftovers cannot change what it thinks the site contains. `media_test.py` needs `openpyxl`
and `pillow`, which are the generator's dependencies rather than the suite's — both workflows install them,
so a checkout that can build the workbook can already test it. Missing them is an `ImportError` with no
tally, which `run.mjs` counts as a failure and not as a skip.

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

None needs the repository dirtied for long, and the second needs nothing tracked touched at all.
