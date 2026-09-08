# Atlas discovery redesign — handoff log

Updated: 2026-09-08. User approved implementation. **Local review only; do not commit or push yet.**

## Scope and decisions

- Preserve all existing edits, including concurrent export/feature-flag work.
- Keep existing data and honest descriptions; do not fabricate endorsements, compatibility, activity, or popularity.
- Keep screenshots; cards prioritize name, description, category/targets, evidence and clear details/GitHub links.
- Table sizes: Compact, Normal, Expanded, remembered locally.
- Stable pseudo-random theme-matched card accents; pulsing hover/focus glow, reduced-motion and quiet-mode support.
- Atlas Byte mascot: name tag, delayed factual project commentary on hover/focus, mobile tap tip, quiet toggle and application flag.
- Use new logo/mascot across web headers, README and both workbook covers.

## Checklist

- [x] Regression test: first visible screenshots load without interaction.
- [x] Remove interaction gate; retain viewport lazy loading; add failed-image fallback.
- [x] Redesign cards and add curated accent/glow behavior.
- [x] Three persistent table densities.
- [x] Mascot name tag, truthful contextual speech, quiet mode, feature flag.
- [x] Branding in website, README, Excel builder and generated workbooks.
- [x] Regenerate site; run scoped regression tests and visual review at desktop/mobile, both themes.
- [x] Final local preview links and handoff; no commit/push.

## Evidence / starting state

- `scripts/19_pages.py:3188`: `ART=false` prevents `cardArt()` until wheel/touch/key/pointer interaction. Same defect present in generated `docs/index.html`.
- Cards/table share one DOM table; preserve row identity on view switches.
- Existing mascot: `docs/assets/atlas-byte.png`; new favicon `docs/favicon.svg`. Masthead float/reduced-motion already implemented in index generator.
- Main generators: `scripts/19_pages.py` (index), `20_landing.py` (facets), `22_detail.py` (details), `24_pwa.py` (PWA/icons), `16_build_all.py` (Excel), `17_markdown.py` (Markdown hub).
- Existing tests: `tests/cards-check.mjs`, `tests/probe.mjs`, `tests/theme_test.py`; full runner `node tests/run.mjs`.
- Prior preview URL: http://127.0.0.1:65281/ (confirm server still running).
- Current verification is recorded below. Do not interpret historical notes above as current work state.

## Session updates

- Created this log before implementation so another model can resume safely.
- Added failing browser regression checks to `tests/cards-check.mjs`; they currently fail as intended because implementation is incomplete.
- Began patching `scripts/19_pages.py`: mascot markup now contains a button wrapper, name tag, quiet-mode button and speech container; table markup has a row-size select; `cardArt()` now starts immediately and has a failed-image fallback; project rows now expect `projectAccent()` and include project action links.
- **Important:** the latest `19_pages.py` edit is deliberately incomplete after model interruption. `initDiscovery()` and `projectAccent()` are referenced but not defined, and matching CSS/behavior has not yet been added. Do not regenerate `docs/index.html` or claim a passing build until these are completed.
- Current red test command used: `node tests/cards-check.mjs <chromium> http://127.0.0.1:65281/`; it reported 59 pass / 5 expected failures against the pre-regeneration page.
- Easter egg decision: "Atlas Orbit" — five quick clicks/taps on the Atlas Byte name tag trigger a brief pixel-star burst; reduced-motion shows a still constellation. Not implemented yet.

### Workbook branding — completed generator work; release build input unavailable

- `scripts/16_build_all.py` now uses the shared web assets `docs/icon-192.png` and
  `docs/assets/atlas-byte.png` on each `Start Here` cover. The 32 × 32 globe mark is anchored at
  `L1`; the 86 × 90 Atlas Byte mascot is anchored at `M1`, with an `ATLAS BYTE` name tag at `M5:N5`.
  The placement is intentionally above the existing theme-switch control at row 6 and does not alter
  workbook sheets, formulas, tables, screenshot pooling, or source data.
- Added `tests/workbook_branding_test.py` and registered it in `tests/run.mjs`. It builds disposable
  light and dark covers, reopens them, inspects their XLSX archives, and also exercises the
  package-preserving release fallback. Latest result: `workbook branding: 22 assertions passed`.
- Attempted the canonical full command `python scripts/16_build_all.py` after the workbook-authoring
  operation marker. It stopped before creating either output because this checkout has no
  `cache/records_all.json` (the uncommitted crawler cache required for the release-sized workbooks).
  Existing `Awesome-Agentic-Atlas-DARK.xlsx` and `Awesome-Agentic-Atlas-LIGHT.xlsx` could not be
  canonically regenerated from data. A weekly build with the normal cache will generate both covers
  from the new canonical code.
- The spreadsheet artifact-tool package is unavailable in this runtime, so the project’s established
  openpyxl/media writer was used for the canonical builder and disposable cover verification.
- **Fallback applied at parent request:** `python scripts/16_build_all.py --brand-existing` updated both
  existing root release assets without loading/resaving their workbook contents. It retained all existing
  package-part payloads, added one cover drawing relationship and the two PNGs, then verified
  the drawing/media relationships. Final check for each output: ZIP integrity passed; 2,143 entries
  (four new parts), 2,045 media parts, 42 drawing parts, and exactly two `Start Here` images anchored at
  L1 and M1. This is a narrow local-release fallback, not a replacement for the normal cached build.
- Added compact, accessible README branding: the repo-local favicon/logo and Atlas Byte mascot sit above the title and both link to the live Atlas. Paths are GitHub-safe relative paths (`docs/favicon.svg` and `docs/assets/atlas-byte.png`); both files exist locally and the PNG was visually checked. No README claims or data were changed.
- Added the `index.mascot_commentary` flag (ON) and its schema entry; the index implementation honors it.

### Final index implementation and verification

- `scripts/19_pages.py` now loads visible card screenshots as soon as the page renders. Images beyond the
  viewport remain IntersectionObserver-lazy, and a failed request leaves a clear in-card fallback.
- Cards have deterministic project accents from a curated palette, a motion-safe hover/focus glow, truthful
  descriptions, evidence/context, and separate Details/GitHub paths. The table remembers Compact, Normal,
  or Expanded density in local storage.
- Atlas Byte now has a name tag, factual project tips on hover/focus, a local Quiet mode, and a five-click
  `Atlas Orbit` easter egg. Reduced-motion readers receive static effects. Both commentary and Orbit honor
  `index.mascot_commentary`.
- Regenerated `docs/index.html`. Scoped source/regression checks passed: `python -m py_compile` for edited
  generators; `node tests/probe.mjs` (364 passed); `python tests/theme_test.py` (156 passed); `python
  tests/pagemin_test.py` (47 passed); `python tests/workbook_branding_test.py` (22 passed); and, with the
  installed full Chrome, `node tests/cards-check.mjs ...` (68 passed). The cold-load browser capture visibly
  confirms the first screenshots render without an input event.
- A full `node tests/run.mjs` attempt is currently red on 35 unrelated `osicons_test.py` assertions because
  the concurrent uncommitted `scripts/osicons.py`/generated platform-icon work has not been wired into all
  surfaces. The full runner therefore cannot be used as a clean whole-suite signal until that separate work
  is finished. Do not attribute those failures to the card, mascot, screenshot, README, or workbook changes.
