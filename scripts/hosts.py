"""Which forge a repository lives on, and every URL the atlas builds for it.

For its first eleven thousand rows the atlas only knew one forge, so `nwo` -- `owner/repo` -- was both
the identity of a row and, prefixed with `https://github.com/`, its address. GitLab projects break both
halves of that: a GitLab path can be any depth (`group/subgroup/project`), and the same `owner/repo`
string can name two unrelated projects on two forges. This module is the one place that decides what a
non-GitHub `nwo` looks like, so every stage that turns one into a URL, a file name or a page path asks
here rather than writing `github.com/{nwo}` itself.

**The rule.** A GitHub row's `nwo` is unchanged: `owner/repo`. Any other forge's is host-qualified:
`gitlab.com/group/subgroup/project`, the host followed by the project's full path, spelled as the forge
spells it. The two can never collide, and telling them apart needs no lookup, because a GitHub owner
cannot contain a dot (GitHub usernames and organisation names are letters, digits and single hyphens)
while every host name does. So `host_of` is a test of the first segment, and everything keyed by `nwo`
-- `cache/meta.json`, `cache/readmes/<nwo with / as __>.md`, `docs/live.json`, the first-seen and
dead-repo ledgers, `docs/repo/<nwo, lower-cased>/` -- takes a GitLab row with no change to its shape and
no chance of overwriting a GitHub one.

Why the host and not a `host` column beside an unchanged `owner/repo`: the column would have to reach
every one of those keys, and each place that forgot it would be a silent collision rather than an
error. A qualified string carries its host wherever the `nwo` goes. The cost is that `nwo` is no longer
always two segments, which is why `owner_of` and `name_of` exist: "owner" is everything before the last
slash and "name" is the last segment, which for GitHub is exactly what `split("/", 1)` gave.

`HOSTS` names the forges a row may come from. Only gitlab.com is wired up end to end; see
handbook/gitlab.md for why the self-hosted instances are not (yet) in it.

**The switch.** `enabled()` is the `intake.gitlab` feature flag in `config/app-flags.json`. Off, no
GitLab row can exist: `from_url` answers None, so the parser reads a gitlab.com link as the website it
was before, and the GitLab scout writes an empty document. Every stage after the parser therefore sees
exactly the rows it saw before GitLab existed, which is what lets all of this merge dark.
"""
from __future__ import annotations

import re
import urllib.parse

GITHUB = "github.com"
GITLAB = "gitlab.com"

# Forge -> what the atlas calls it on a page. A host absent from here is not a forge the atlas reads.
HOSTS = {GITHUB: "GitHub", GITLAB: "GitLab"}

# A gitlab.com project URL: the full path, then optionally GitLab's `/-/` separator and whatever follows
# it (`/-/tree/main/docs`, `/-/blob/...`). Paths are letters, digits, `_`, `-` and `.`, and may not
# start with `-` or end in `.git`/`.atom`. The reserved first segments are gitlab.com's own pages.
GL = re.compile(r"^https?://(?:www\.)?gitlab\.com/(?P<path>[A-Za-z0-9_.][A-Za-z0-9_.-]*"
                r"(?:/[A-Za-z0-9_.][A-Za-z0-9_.-]*)+?)(?:\.git)?(?:/-/(?P<rest>[^#?]*))?/?(?:[#?].*)?$")
GL_RESERVED = {"explore", "users", "groups", "dashboard", "help", "admin", "search", "-", "api",
               "projects", "snippets", "uploads", "assets", "s", "abuse_reports", "oauth", "jwt",
               "import", "profile", "public", "sitemap", "robots.txt"}


def host_of(nwo: str) -> str:
    """The forge an `nwo` lives on: `github.com` for `owner/repo`, the first segment otherwise."""
    head = (nwo or "").split("/", 1)[0]
    return head.lower() if "." in head else GITHUB


def is_github(nwo: str) -> bool:
    return host_of(nwo) == GITHUB


def path_of(nwo: str) -> str:
    """The project's path on its own forge: the `nwo` itself on GitHub, the part after the host on any
    other. What that forge's own API is asked about."""
    return nwo if is_github(nwo) else nwo.split("/", 1)[1]


def qualify(host: str, path: str) -> str:
    """The `nwo` for `path` on `host`."""
    path = path.strip("/")
    return path if host.lower() == GITHUB else f"{host.lower()}/{path}"


def owner_of(nwo: str) -> str:
    """Everything before the project's own name: the GitHub owner, or a GitLab host and namespace."""
    return nwo.rsplit("/", 1)[0]


def name_of(nwo: str) -> str:
    return nwo.rsplit("/", 1)[-1]


def label(nwo: str) -> str:
    """The forge's display name, for a marker on a page: "GitHub" or "GitLab"."""
    return HOSTS.get(host_of(nwo), host_of(nwo))


def web_url(nwo: str) -> str:
    """The project's own page."""
    return f"https://{host_of(nwo)}/{path_of(nwo)}"


def clone_url(nwo: str) -> str:
    return f"{web_url(nwo)}.git"


def raw_base(nwo: str, branch: str = "HEAD") -> str:
    """Prefix for a file's raw bytes at `branch`, with a trailing slash. GitLab serves `HEAD` as the
    default branch exactly as raw.githubusercontent.com does."""
    branch = branch or "HEAD"
    if is_github(nwo):
        return f"https://raw.githubusercontent.com/{nwo}/{branch}/"
    return f"{web_url(nwo)}/-/raw/{branch}/"


def blob_base(nwo: str, branch: str = "HEAD") -> str:
    """Prefix for a file's rendered page at `branch`, with a trailing slash."""
    branch = branch or "HEAD"
    sep = "/" if is_github(nwo) else "/-/"
    return f"{web_url(nwo)}{sep}blob/{branch}/"


def tree_url(nwo: str, branch: str, path: str) -> str:
    sep = "/" if is_github(nwo) else "/-/"
    return f"{web_url(nwo)}{sep}tree/{branch or 'HEAD'}/{path.strip('/')}"


def social_card(nwo: str) -> str:
    """The forge's generated preview image for a repository, or "" where the forge has none.

    GitHub renders one for every repository at a predictable URL, which is why the atlas falls back to
    it everywhere a row has no screenshot. GitLab has no equivalent -- a project's `og:image` is its
    avatar, or GitLab's own logo when it has none -- so a GitLab row with no picture of its own gets ""
    and each surface shows what it shows for a row with no image at all, rather than a GitHub card for
    a repository GitHub has never heard of (that URL answers with a picture of nothing).
    """
    return f"https://opengraph.githubassets.com/1/{nwo}" if is_github(nwo) else ""


_ENABLED: bool | None = None


def enabled() -> bool:
    """Whether GitLab projects are indexed at all: the `intake.gitlab` flag, read once per process.
    `AAA_APP_FLAGS` points `app_flags` at another file, which is how a test or a trial turns it on."""
    global _ENABLED
    if _ENABLED is None:
        import app_flags
        _ENABLED = bool(app_flags.load().get("intake.gitlab"))
    return _ENABLED


def from_url(url: str, force: bool = False) -> tuple[str, str] | None:
    """(nwo, rest) for a project URL on a non-GitHub forge the atlas reads, else None. `rest` is what
    follows GitLab's `/-/` separator: `tree/main/docs` for a folder, "" for the project itself.
    None for every URL while the flag is off, unless `force`."""
    if not (force or enabled()):
        return None
    m = GL.match((url or "").strip())
    if not m:
        return None
    # `.git` is stripped here rather than in the pattern: a segment may contain dots, so the greedy
    # segment would otherwise swallow it into the name.
    path = re.sub(r"\.git$", "", m.group("path"))
    if path.split("/", 1)[0].lower() in GL_RESERVED:
        return None
    return qualify(GITLAB, path), (m.group("rest") or "").strip("/")


def readme_file(nwo: str) -> str:
    """The cache file a repository's README is kept in, under `cache/readmes/`. Every slash becomes
    `__`, so a GitLab path of any depth is still one flat file name, and the host's dot keeps it apart
    from every GitHub one."""
    return f"{nwo.replace('/', '__')}.md"


def quote_path(nwo: str) -> str:
    """The project's path URL-encoded as one segment, which is how GitLab's REST API takes an id."""
    return urllib.parse.quote(path_of(nwo), safe="")
