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
