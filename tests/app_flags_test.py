"""Application-flag schema, editor writes, and both generators' kill-switch paths."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
import app_flags  # noqa: E402
import flags_app  # noqa: E402

passed = failed = 0


def ok(label: str, condition: bool, detail: object = "") -> None:
    global passed, failed
    if condition:
        passed += 1
    else:
        failed += 1
        print(f"FAIL {label}: {detail}")


def rejects(label: str, value: object, contains: str) -> None:
    try:
        app_flags.validate(value)
    except app_flags.FlagError as exc:
        ok(label, contains in str(exc), exc)
    else:
        ok(label, False, "accepted invalid configuration")


values = app_flags.load()
keys = [spec.key for spec in app_flags.SPECS]
ok("the schema exposes every value key once", list(values) == keys, (list(values), keys))
ok("the shipped control panel has more than a token pair of switches", len(keys) >= 10, len(keys))
ok("every shipped value is visibly 1 or 0", all(type(v) is int and v in (0, 1) for v in values.values()))
ok("every flag has a human name", all(spec.name.strip() for spec in app_flags.SPECS))
ok("every flag explains what it controls", all(len(spec.description.split()) >= 6 for spec in app_flags.SPECS))
ok("every flag explains the disabled result", all(spec.off_effect.strip() for spec in app_flags.SPECS))
ok("the schema identifies the controlled application",
   json.loads(app_flags.SCHEMA_PATH.read_text(encoding="utf-8"))["application"]["id"] == "awesome-agentic-atlas")
ok("the editor catalog includes all flags", [row["key"] for row in flags_app.catalog()] == keys)
ok("the editor catalog reports live values",
   all(row["value"] == values[row["key"]] for row in flags_app.catalog()))

missing = dict(values)
missing.pop(keys[0])
rejects("a missing switch stops the build", missing, "missing flag")
unknown = dict(values, **{"detail.typo": 1})
rejects("an unknown switch stops the build", unknown, "unknown flag")
bad_bool = dict(values)
bad_bool[keys[0]] = True
rejects("JSON true is rejected so the file keeps one vocabulary", bad_bool, "integer 1")
bad_string = dict(values)
bad_string[keys[0]] = "1"
rejects("a quoted one is rejected", bad_string, "integer 1")
bad_number = dict(values)
bad_number[keys[0]] = 2
rejects("a number other than zero or one is rejected", bad_number, "integer 1")

with tempfile.TemporaryDirectory(prefix="aaa-flags-") as raw_tmp:
    tmp = Path(raw_tmp)
    target = tmp / "flags.json"
    target.write_text(app_flags.serialise(values), encoding="utf-8")
    first_revision = app_flags.revision(target)
    changed = dict(values)
    changed[keys[0]] = 0 if changed[keys[0]] else 1
    second_revision = app_flags.write(changed, first_revision, target)
    ok("an editor save writes the new values", app_flags.load(target) == changed)
    ok("an editor save changes the revision", first_revision != second_revision)
    ok("the file remains easy-to-review pretty JSON", "\n  \"" in target.read_text(encoding="utf-8"))
    ok("the replacement leaves no temporary sibling", not list(tmp.glob("*.tmp")), list(tmp.iterdir()))
    try:
        app_flags.write(values, first_revision, target)
    except app_flags.FlagError as exc:
        ok("a stale editor cannot overwrite a newer save", "changed after" in str(exc), exc)
    else:
        ok("a stale editor cannot overwrite a newer save", False)

    # Render with every optional surface disabled. The candidate file is outside the repository and the
    # detail stage writes to scratch, so this exercises the real generator without touching committed docs/.
    off = {key: 0 for key in keys}
    off_file = tmp / "all-off.json"
    off_file.write_text(app_flags.serialise(off), encoding="utf-8")
    out = tmp / "site"
    env = dict(os.environ, AAA_APP_FLAGS=str(off_file), PYTHONIOENCODING="utf-8")
    result = subprocess.run([sys.executable, str(SCRIPTS / "22_detail.py"), "--out", str(out),
                             "--data", str(ROOT / "docs" / "data.json")],
                            cwd=ROOT, env=env, capture_output=True, text=True)
    ok("the detail generator accepts an all-OFF candidate", result.returncode == 0, result.stdout + result.stderr)
    sample_path = out / "repo" / "0-ai-ug" / "cate" / "index.html"
    sample = sample_path.read_text(encoding="utf-8") if sample_path.exists() else ""
    for label, fragment in (
        ("Install", "<h2>Install</h2>"),
        ("repository reader", "id=\"source-preview\""),
        ("screenshot", "<h2>Screenshot</h2>"),
        ("platform support", "<h2>Platform support</h2>"),
        ("provenance", "<h2>Where it came from</h2>"),
        ("classification", "<h2>How it is classified</h2>"),
        ("related projects", "<section class=\"kin\">"),
    ):
        ok(f"the {label} kill switch omits its detail-page markup", fragment not in sample)

# Root rendering can be exercised without writing docs: this is the exact function both root build stages use.
spec = importlib.util.spec_from_file_location("flags_b19", SCRIPTS / "19_pages.py")
b19 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b19)
data = json.loads((ROOT / "docs" / "data.json").read_text(encoding="utf-8"))
off = {key: 0 for key in keys}
b19.APP_FLAGS = off
root_page = b19.substitute(b19.PAGE, data, b19.REPO, b19.b17.SITE)
ok("card-view OFF makes table the first paint", 'data-view="table"' in root_page)
ok("screenshot OFF marks the layout before JavaScript", 'data-index-screenshots="off"' in root_page)
ok("deployment-badge OFF removes the badge", 'id="deployed"' not in root_page)
ok("the generated page carries its exact flag values", 'const FLAGS = {"index.card_view":0' in root_page)
ok("root screenshot rendering has a runtime kill-switch branch", 'FLAGS["index.project_screenshots"]' in root_page)
ok("root install rendering has a runtime kill-switch branch", 'FLAGS["index.install_commands"]' in root_page)
# The export switches at runtime rather than at build time, like the two above it and unlike the deployment
# badge: the chip and its dialog still ship, hidden by `.takechip{display:none}` with nothing wired to them,
# and `readHash` ignores a `#list=` fragment. Asserted on the branch and on the value, because the markup
# being present is exactly why the branch is the only thing keeping the feature off.
ok("root export rendering has a runtime kill-switch branch", 'FLAGS["index.export"]' in root_page)
ok("export OFF reaches the page as a zero", '"index.export":0' in root_page)
ok("export OFF leaves the chip in the markup but hidden and unwired",
   'id="take"' in root_page and ".takechip{display:none}" in root_page)

print(f"\n{passed} passed, {failed} failed")
raise SystemExit(1 if failed else 0)
