# tests/

```
node tests/run.mjs
```

That is the whole thing. It finds a Chromium the machine already has, serves `docs/` on a port the OS picks,
runs five harnesses in turn, prints what each one asserted, and exits non-zero if anything failed. About 35
seconds, of which 22 are the detail-page regeneration. No install step, no arguments, no configuration.

It asserts on `docs/` as committed, not on the generator's intentions. `docs/` is served verbatim by GitHub
Pages — `build_type: legacy`, so what is in the repository is what a reader downloads — which means the bytes
in the checkout are the deployable artefact and are the honest thing to test.

Individual harnesses can be run alone. The two that drive a browser need to be given one and told where the
site is, because `run.mjs` owns both:

```
node tests/probe.mjs
python tests/pagemin_test.py
node tests/detail-churn.mjs
node tests/cards-check.mjs <chrome-binary> <origin>
node tests/pwa-check.mjs   <chrome-binary> <origin>
```

## What each one covers, and what it deliberately does not

There are five files rather than one because they are five instruments, and the overlap between them is the
reason to keep them apart rather than the reason to merge them. Each file's header says at length what it
cannot see; this is the summary.

| harness | what it covers | what it cannot see |
| --- | --- | --- |
| `probe.mjs` | Runs the page's own script from `docs/index.html` under a stub DOM against the real `docs/data.json`, then asserts on the HTML it renders: ranking, the search fallback, the hash round-trip, the palette, the theme colour, the cards stylesheet, and the page as shipped text. ~157 assertions. | Computed layout. There is none in Node, so it can tell you a clamp rule is spelled correctly and not that anything clamps. |
| `cards-check.mjs` | Real layout in a real browser over HTTP at 1440, 900 and 375 px in both themes: how many cards are across, the screenshot's aspect ratio, horizontal overflow, scroll and focus survival across a view switch, the toggle's cost against the re-render it avoids, and the clamp's behaviour. Writes screenshots to `build-tmp/`. ~47 assertions. | Any prefixed spelling this browser has an unprefixed implementation of. `-webkit-line-clamp` is the case that bit: this Chrome does the standard `line-clamp`, so a rule missing `display:-webkit-box` clamps perfectly here and is inert in Firefox. That half lives in `probe.mjs`. |
| `pwa-check.mjs` | Manifest, service worker registration and scope, the precached shell, `data.json` caching, offline rendering with the network emulated off, and a 404 navigation that must not be cached. 17 assertions. | Anything not observable from a page: it cannot tell you the worker's version hash is derived from the files it precaches rather than hardcoded. It also cannot see paths this browser does not take — it supports navigation preload, so the fallback never runs. |
| `detail-churn.mjs` | Regenerates all 1,294 detail pages four times into scratch directories and compares SHA-256 trees: determinism, that a day of moving star counts and push dates rewrites nothing, that editing one curated blurb does move its page, and that committed `docs/repo` matches a fresh regeneration. 7 assertions over 1,298 files. | Whether the pages are any good. It never opens one. It also cannot see churn from any other stage — `20_landing.py` rewrites 156 facet pages on every run by design, and that is not what this measures. |
| `pagemin_test.py` | `scripts/pagemin.py` against the cases the real page does not contain: template literals, `${}` substitutions, regex literals, unterminated blocks, strings that look like comments, and the whole template loaded live out of `19_pages.py`. 48 assertions. Written and owned by the JFH-204 author. | Everything about the page that is not comment stripping. |

Between them, roughly 276 assertions. The number only matters in one direction — see the floors below.

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

The Python harness is Python because the thing it tests is. `python` here means whatever `lib/python.mjs`
finds; there are no packages, only the standard library.

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

A test suite nobody has watched fail is not known to work. Two cheap ways to check this one still bites:

- Give a template a timestamp. Add `datetime.now()` to anything `scripts/22_detail.py` renders and
  `detail-churn.mjs` reports `two runs over identical data write identical bytes -- 1,295 file(s)`, then
  restore it.
- Break a scoping rule. Copy `docs/index.html`, delete an `html[data-view=cards]` prefix from one selector in
  the copy, and run `AAA_PAGE=/path/to/copy node tests/probe.mjs`. The scope assertion names the offending
  selector.

Neither needs the repository dirtied for long, and the second needs nothing tracked touched at all.
