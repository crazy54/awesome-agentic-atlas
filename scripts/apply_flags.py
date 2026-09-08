"""Apply the committed application flags to every page readers can see."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent

# Import first so a bad flag stops before either generator writes anything.
sys.path.insert(0, str(HERE))
import app_flags  # noqa: E402


def run(script: str) -> None:
    result = subprocess.run([sys.executable, str(HERE / script)], cwd=ROOT)
    if result.returncode:
        raise SystemExit(f"{script} failed with exit code {result.returncode}")


def render_index() -> None:
    """Render the shell against the committed dataset without pretending a new crawl happened.

    This intentionally does not call 19b_refresh.py: that stage also mutates first-seen data and refuses
    a checkout whose configured sources are ahead of its last crawl. A flag change is presentation-only.
    The source count printed in the shell is therefore derived from the same committed rows as its project
    and star counts, keeping the page internally consistent while a larger ingest is in flight.
    """
    spec = importlib.util.spec_from_file_location("flags_b19", HERE / "19_pages.py")
    b19 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(b19)
    data_path = ROOT / "docs" / "data.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))
    listed_by = data["cols"].index("listed_by")
    labels = {name.strip() for row in data["rows"] for name in row[listed_by].split(",") if name.strip()}
    b19.LISTS = len(labels)
    page = b19.substitute(b19.PAGE, data, b19.REPO, b19.b17.SITE)
    (ROOT / "docs" / "index.html").write_text(page, encoding="utf-8")
    print(f"index.html rendered from {len(data['rows']):,} committed rows and {len(labels)} source labels")


def main() -> None:
    on = sum(app_flags.FLAGS.values())
    print(f"Validated {len(app_flags.FLAGS)} application flags · {on} ON · "
          f"{len(app_flags.FLAGS) - on} OFF")
    render_index()
    run("22_detail.py")
    run("24_pwa.py")
    print("Application flags applied to docs/.")


if __name__ == "__main__":
    main()
