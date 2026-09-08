This directory holds the two things about the site that are decisions rather than data:
[`app-flags.json`](#application-flags), which says what ships, and
[`collections.json`](#curated-collections), which says what we recommend.

# Application flags

`app-flags.json` is the site's build-time control panel. Every value is deliberately either `1` or
`0`:

- `1` — ON
- `0` — OFF / DISABLED

The friendly editor is the easiest way to change them:

```powershell
python scripts/flags_app.py
```

It opens a local-only page with every flag, its effect, and a large ON/OFF switch. **Save & render
site** writes the JSON atomically, rebuilds the index and all project detail pages, and updates the
service-worker version. **Save values only** is useful when a workflow will perform the build later.

The file is also intentionally easy to edit by hand or by an agent. After a manual edit, apply it with:

```powershell
python scripts/apply_flags.py
```

The generators reject missing flags, unknown flags, booleans, strings and numbers other than `0` or
`1` before writing a page. The shipped configuration keeps every feature enabled. For an emergency
kill switch, change only the relevant line from `1` to `0`, render, review the diff, and deploy.

An alternate file can be previewed without changing the committed control panel:

```powershell
$env:AAA_APP_FLAGS = 'C:\path\to\candidate-flags.json'
python scripts/apply_flags.py
```

Unset `AAA_APP_FLAGS` before making a production build. The Flags app always edits the committed
`config/app-flags.json`; it never follows that environment override.

# Curated collections

`collections.json` is the source for the pages under `docs/collections/`. Everything else on this site
is generated from what 11 source lists agreed on; these pages are the one place where we say *pick this
one*, so the opinions live in a reviewable file rather than in a template.

Each collection has a `slug`, a `title`, a short `kicker`, an `intro` paragraph explaining the criteria,
and 5–8 `picks`. A pick is a repository already in the atlas plus two pieces of prose:

- `role` — the slot it fills, and the reason these read as a *set*. One agent, one memory layer, one
  sandbox. Two picks with the same role in one collection is a curation bug, and the build says so.
- `why` — why this one for that slot. Ground it in something the page can show: how many of the source
  lists agreed, the licence, a stated platform verdict, the language.

A collection may also carry `requires`, which is the part that keeps the prose honest:

```json
"requires": {"os": "Windows"}
"requires": {"target": "claude-code"}
```

The generator checks every pick against `docs/data.json` and **fails the build** rather than publish a
page whose claim has gone stale — a repository that left the atlas, a "runs on Windows" page listing a
project whose Windows verdict has dropped to inferred, or a Claude Code kit containing something that no
longer targets Claude Code. Adding a collection is a JSON edit plus:

```powershell
python scripts/25_collections.py
python scripts/24_pwa.py
```

The first writes `docs/collections/`, its entry in `docs/sitemap.xml` and the Markdown twins under
`mega-list/collections/`; the second re-versions the service worker so returning readers see the change.
