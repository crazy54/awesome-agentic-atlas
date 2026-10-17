# The test suite

The suite lives in `tests/`. [`tests/README.md`](../tests/README.md) holds the design notes: why it is
many small harnesses, and why each one asserts what it does. This page is the working summary.

## Running it

```bash
node tests/run.mjs
```

The runner takes no arguments. It runs every harness in the `HARNESSES` list in `tests/run.mjs`: on 2026-09-25 that was
**29 harnesses, 17 Python and 12 Node**. Ten of the Node harnesses drive a headless Chromium and two do not.

**Before a PR, run the whole suite.** A full local run took about 24 minutes on the 2026-09-25 baseline.
The runner prints each harness's time in its closing table.

What the runner does:

1. It finds a Chromium in this order: `CHROME_PATH`, `CHROMIUM_PATH`, `PLAYWRIGHT_CHROMIUM`, then the
   Playwright browser caches (including `PLAYWRIGHT_BROWSERS_PATH`), then `PATH`.
2. It serves `docs/` over HTTP under the prefix **`/awesome-agentic-atlas/`**, at `http://127.0.0.1:<port>/awesome-agentic-atlas/`.
   The server is `tests/lib/serve.mjs`. It serves under a prefix, as Pages once did, so that a relative URL
   which accidentally became absolute fails.
3. It runs each harness in turn. It reads the harness's last `N passed, M failed` line, and counts as a
   failure any harness that printed no tally, asserted nothing, or made **fewer assertions than its
   `floor`**. Floors catch a harness that quietly stopped testing.

Exit codes:

| Code | Meaning |
|---|---|
| 0 | every harness green |
| 1 | at least one harness red, or below its floor |
| 2 | could not start: no Chromium, no Python 3, or `docs/index.html` or `docs/catalog/index.html` missing |
| 130 | interrupted (Ctrl-C) |

**Requirements:**

- Node 22 and Python 3.
- `openpyxl` and `pillow`, for `workbook_branding_test.py` and `media_test.py`.
- A Chromium. `npx playwright install chromium` or `python -m playwright install chromium` provides one;
  so does an installed Chrome.

### Environment variables

| Variable | Effect |
|---|---|
| `PYTHON` | The interpreter for Python harnesses. Otherwise the first Python 3 among `python`, `python3`, `py` |
| `CHROME_PATH`, `CHROMIUM_PATH`, `PLAYWRIGHT_CHROMIUM`, `PLAYWRIGHT_BROWSERS_PATH` | Where to find Chromium |
| `AAA_CHROME_FLAGS` | Extra Chromium flags. CI sets `--no-sandbox --disable-dev-shm-usage` |
| `AAA_TMP` | Scratch directory. The runner makes one per run under the OS temp directory |
| `AAA_ARTIFACTS` | Where screenshots and failure evidence go. Default: `build-tmp/` in the checkout |
| `AAA_PAGE`, `AAA_DATA`, `AAA_HOME` | Point `probe.mjs` at a different catalogue page, dataset or homepage than the committed one |

## Running one harness

A Python harness, or one of the two browserless Node harnesses, runs on its own from the repo root:

```bash
python tests/theme_test.py
node tests/probe.mjs
node tests/detail-churn.mjs
```

A browser harness needs a Chromium path and an origin. Nothing ships a standalone server, but this
one-liner starts the same one the runner uses and prints its origin:

```bash
node --input-type=module -e "import {serve} from './tests/lib/serve.mjs'; console.log((await serve('docs')).origin)"
# in another shell:
node tests/pwa-check.mjs "<path to chrome>" "http://127.0.0.1:<port>/awesome-agentic-atlas/"
```

Stop the server with Ctrl-C in its own shell. **Never** stop it with `taskkill /IM node.exe`: that kills every
Node process on the machine, including other sessions' tools and test runs.

## The harnesses

"Assertions" is the tally from the 2026-09-25 baseline run on `a77b46eb`. "Floor" is the minimum set in
`run.mjs`. Re-measure both before quoting them anywhere.

| Harness | Kind | Guards | Assertions | Floor |
|---|---|---|---|---|
| `app_flags_test.py` | Python | Feature-flag schema, the editor's atomic writes, every kill switch | 39 | 28 |
| `theme_test.py` | Python | The eight skins' token sets, which must stay identical across their four copies; the theme menu; verdict marks; the phone layout | 1053 | 500 |
| `signals_test.py` | Python | When a cached release or action answer must be re-queried | 210 | 170 |
| `fetch_test.py` | Python | A batch GitHub keeps timing out on is split and retried; nothing else is | 27 | 20 |
| `indexnow_test.py` | Python | Which URLs are submitted, the key prune, truncated responses. Network is stubbed | 140 | 100 |
| `newness_test.py` | Python | What "New" means: one cohort, replaced by the next import that adds anything | 54 | 45 |
| `discover_test.py` | Python | Discover's fifty-a-day selection, category fairness, rotation | 148 | 75 |
| `probe.mjs` | Node | The catalogue's page script under a stub DOM; the page and root README as text | 456 | 140 |
| `pagemin_test.py` | Python | The comment stripper | 47 | 40 |
| `media_test.py` | Python | Workbook image dedup and the entry ceiling | 49 | 45 |
| `workbook_branding_test.py` | Python | The mark and mascot on both workbook covers | 26 | 24 |
| `refresh_test.py` | Python | `19b_refresh.py`'s cache-free render, and its refusal when the source count moved | 74 | 60 |
| `live_test.py` | Python | `live.json`, the sidecar detail pages read | 106 | 90 |
| `semantic_test.py` | Python | The semantic index, scored from the published bytes | 48 | 30 |
| `collections_test.py` | Python | Curated picks and every refusal that keeps them honest | 652 | 500 |
| `deeplinks_test.py` | Python | The homepage forwarding old `/#…` links into `catalog/`, and the host in `docs/CNAME`. Needs `node` on PATH | 66 | 34 |
| `spotlight_test.py` | Python | The daily spotlight rule, which is written in both Python and JS and must agree. Needs `node` on PATH | 326 | 300 |
| `osicons_test.py` | Python | The five platform icons, resolved over every built page. Slow: about 3 min | 251 | 200 |
| `detail-churn.mjs` | Node | Re-runs `22_detail.py` four times and hashes every output file, so unchanged data must mean unchanged bytes. Slow: about 7 min | 13 | 7 |
| `detail-preview-check.mjs` | browser | The in-page README/source reader on detail pages. The GitHub API is stubbed | 16 | 12 |
| `cards-check.mjs` | browser | Real layout at 1440, 900 and 375 px in both themes; the pinned filter bar | 202 | 86 |
| `pwa-check.mjs` | browser | Manifest, service worker, precache, offline, freshness, 404; **the `VERSION` hash** | 62 | 25 |
| `dance-check.mjs` | browser | "Dance with me": the beat detector against a known tempo. WebGL2 is stubbed out | 37 | 30 |
| `spotlight-check.mjs` | browser | The spotlight on a pinned clock: per day, all day, local time, no layout shift, no-JS | 117 | 100 |
| `prank-check.mjs` | browser | Archie's pranks: each undone, nothing saved, the flicker rate | 33 | 28 |
| `friends-check.mjs` | browser | Archie's friends: each arrives, leaves, restores the page and keeps off the controls | 109 | 80 |
| `rig-check.mjs` | browser | The light show: the flash rate of every fixture, the blinders' swell, the cues | 43 | 40 |
| `admin-check.mjs` | browser | Archie's admin panel: hidden, one button per command, each dispatching its own, why a button is greyed | 69 | 60 |
| `stage-check.mjs` | browser | The stage by its pixels: the LED wall moving; pyro, CO2, haze and blinders visible | 51 | 45 |
| `bits-check.mjs` | browser | Every one of the pals' bits, played where it can play: the page put back exactly, nothing saved, no focus taken, no more than three flashes a second, nothing outside the stage's layer, and Escape and a click stopping it. Slow: about 30 min (`AAA_BITS=name,…` for one) | 696 | 450 |

The Assertions column counts passed plus failed. The six Archie browser harnesses (`prank`, `friends`, `rig`, `admin`,
`stage` and `bits`) render the real model through swiftshader's software WebGL. They add the needed flags
themselves.

## Known-red and environment-sensitive checks

**The 2026-09-25 baseline on `latest_branch` (`a77b46eb`) was red:** 4,368 passed and 9 failed, in 7 harnesses.
A PR is judged on adding no new failures. For each of the nine:

| Harness | Failing assertion | Cause, as far as it is known |
|---|---|---|
| `pwa-check` (2) | the worker's `VERSION` is a hash of what it precaches | **Real defect.** `docs/sw.js` is stale; fix with `python scripts/24_pwa.py`. See [troubleshooting.md](troubleshooting.md#known-issues) |
| `probe` (1) | Discover has cards with and without a language | Data-dependent: that day's 48 picks all had a language |
| `semantic` (1) | the body of the corpus fills the map | Data-dependent: the 1st to 99th percentile spread of the map projection |
| `detail-preview-check` (1) | README, skill, agent and docs Markdown are discoverable in the picker | Not investigated |
| `dance-check` (2) | beats timed by the audio clock; the poster hops on the beat | Timing-sensitive: intervals ranged from 396 to 3,498 ms against a 500 ms beat on a loaded machine |
| `friends-check` (1) | "and so does Escape" | Load. In-page, Escape takes 0.42-0.46 s against the 1 s budget (2026-10-14), and every CI run with a tally from 2026-09-26 to 2026-10-14 passed it. With another suite running on the same machine, Tab missed once; pinned to one core, Tab and the poke did |
| `rig-check` (1) | the blinder cue plays | **Fixed 2026-10-14.** The waits were in wall-clock seconds, and a cue is timed in the rig's, which CI's software WebGL, at under two frames a second, runs at a fifth of real time or less. They are bounded in the rig's seconds now |

Other known sensitivities:

- **`cards-check` screenshot-deferral** has failed once in 189 on runner timing, on a page that passed
  4 minutes earlier. Re-run before debugging it.
- **`cards-check` name-tag line count** depends on whether Segoe UI is installed. There is 2.4 px of
  slack in an 82 px pill, so it can pass on Windows and fail on Linux CI.
- **Archie's frame rate.** The Archie harnesses render through swiftshader, which on CI draws a frame or two
  a second once the rig is lit. Wait for anything Archie times in his frames by the rig's clock, as
  `rig-check`'s `untilRig` does. The friends' dismissals are a 350 ms fade, held to a wall-clock second
  (three for a poke); a run on one core shared with other work can miss them. See
  [troubleshooting.md](troubleshooting.md#the-suite-is-red).
- **Hover styles:** CI's headless Chromium reports `(hover: hover)` as false, while a desktop run reports
  true. The harnesses assert hover CSS from the stylesheet (CSSOM), not by hovering.
- **Checks on committed output:** `probe`, `cards-check` and others read the *committed* `docs/`. A new
  rule in a generator therefore turns CI red until someone regenerates and commits the output.
- **Don't mutate `docs/` in place to test drift.** Peer sessions sharing the checkout run the suite against
  the same files. Copy the file somewhere and point `probe.mjs` at the copy with `AAA_PAGE`, `AAA_DATA` or `AAA_HOME`.
- **CI's browser is not the one a local run finds.** CI runs full Chromium (`/usr/bin/chromium`); locally,
  `run.mjs` finds Playwright's headless shell first. Only full Chromium asks the origin root for
  `/favicon.ico` when it shows `robots.txt`, a feed, JSON or an image, so a 404 there is red in CI and
  invisible locally. To see what CI sees, set `CHROME_PATH` to a full Chromium, such as Playwright's
  `chromium-<build>/chrome-win64/chrome.exe`.
- **The GitHub API's anonymous limit.** The homepage's star count and every footer's build tags call
  `api.github.com` without a token: 60 calls an hour per address, shared by every run on the machine. Once
  that is used up, each refused call is a 403 that the page ignores and Chrome logs as a console error.
  `prank-check` and `dance-check` excuse a 403 or 429 from `api.github.com`. The other harnesses that count
  console errors don't yet.
- **Wait for state; don't sleep for it.** With the CPU throttled four times, a matchMedia `change` event took
  a second to arrive, and a poll read Archie's quiet cut 300 to 600 ms after the page made it. Wait with
  `until()`, or stamp the moment in the page, and keep the bound on the thing being measured.

## When you add or change a harness

- Add it to `HARNESSES` in `tests/run.mjs` with a `label` and a `floor`. A harness file in `tests/` that is not in that
  list reddens the run, so it cannot be forgotten silently.
- Set the floor a little under the real count, so a harness that silently stops asserting fails the run.
- Check that a deliberately broken input makes it fail. A check that has never been red has not been
  shown to work.
- Update the table above and the one in `tests/README.md`.
