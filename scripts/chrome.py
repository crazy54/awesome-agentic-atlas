"""Find a headless Chromium, wherever this happens to be running.

Both screenshot stages shell out to `chrome-headless-shell` rather than driving Playwright's Python
binding, which is the right call -- it is one subprocess per shot, no event loop, and it survives a
browser that hangs. The cost is that they need the binary's path, and that path used to be a string
literal pointing into one developer's home directory. On any other machine, and on every CI runner, it
did not exist; and because both stages treat a missing browser as "no screenshot available" rather than
an error, the failure was silent -- the build simply produced an Open Graph card for every row in the
atlas and said nothing.

So the path is resolved instead of assumed, in the order a person would look:

  1. $CHROME_PATH, $CHROMIUM_PATH or $PLAYWRIGHT_CHROMIUM -- an explicit answer always wins
  2. the Playwright browser cache for this platform, newest build first
  3. anything Chromium-shaped on $PATH

Nothing here installs a browser. If the answer is None the caller degrades to Open Graph cards, which
is why `find()` returns None rather than raising: a missing browser costs the build its screenshots,
not the build.
"""
from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

ENV_VARS = ("CHROME_PATH", "CHROMIUM_PATH", "PLAYWRIGHT_CHROMIUM")

# The headless shell first: it is a third of the size of full Chrome, it is what Playwright installs by
# default, and it is the only one of these that cannot try to open a window.
BINARIES = ("chrome-headless-shell.exe", "chrome-headless-shell", "headless_shell",
            "chrome.exe", "chrome", "chromium")

ON_PATH = ("chrome-headless-shell", "chromium", "chromium-browser",
           "google-chrome", "google-chrome-stable", "chrome")

BUILD = re.compile(r"(\d+)\s*$")


def _caches():
    """Where Playwright keeps browsers, per platform. Non-existent entries are filtered by the caller."""
    if env := os.environ.get("PLAYWRIGHT_BROWSERS_PATH"):
        yield Path(env)
    home = Path.home()
    yield home / "AppData" / "Local" / "ms-playwright"      # Windows
    yield home / ".cache" / "ms-playwright"                 # Linux, and GitHub's ubuntu runners
    yield home / "Library" / "Caches" / "ms-playwright"      # macOS


def _newest_first(dirs):
    """Sort `chromium_headless_shell-1223` style names by build number, descending.

    By name would be wrong the first time a build number changes width: "999" sorts above "1223".
    """
    def key(p: Path):
        m = BUILD.search(p.name)
        return (int(m.group(1)) if m else -1, p.name)
    return sorted(dirs, key=key, reverse=True)


def find() -> Path | None:
    for var in ENV_VARS:
        value = os.environ.get(var)
        if value and Path(value).exists():
            return Path(value)

    for cache in _caches():
        if not cache.is_dir():
            continue
        # `chromium_headless_shell-*` sorts above `chromium-*` for the same build, which is the
        # preference we want: underscore is above hyphen, and the tuple key keeps build number first.
        for install in _newest_first(cache.glob("chromium*")):
            for name in BINARIES:
                for hit in sorted(install.rglob(name)):
                    if hit.is_file():
                        return hit

    for name in ON_PATH:
        if found := shutil.which(name):
            return Path(found)
    return None


PATH = find()


def describe() -> str:
    return str(PATH) if PATH else "not found -- screenshots will fall back to Open Graph cards"


if __name__ == "__main__":
    print(describe())
