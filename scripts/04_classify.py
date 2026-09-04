"""Derive per-repo OS support, install command, and screenshot candidates.

Precedence, strongest first:
  1. Published release assets (a .msi/.exe proves native Windows; a lone .dmg proves it does not)
  2. Explicit prose in the README ("Windows, macOS, Linux", "macOS only", "requires WSL")
  3. Install-manager inference (winget -> native Windows; brew -> macOS; curl|sh -> Unix)
  4. Runtime inference (Node/Python/Rust/Go are portable unless a Unix-only dep says otherwise)

Every verdict carries the evidence that produced it so the spreadsheet is auditable.
"""
import json
import re
from pathlib import Path
from urllib.parse import quote, urljoin

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
READMES = CACHE / "readmes"

YES, LIKELY, NO = "Yes", "Likely", "No"

# ---------------------------------------------------------------- release assets
A_WIN = re.compile(r"(windows|win32|win64|winnt|\bwin\b|-pc-windows|\.msi$|\.msix$|\.exe$|_x64\.zip$)", re.I)
A_MAC = re.compile(r"(darwin|macos|mac-os|apple|osx|\.dmg$|\.pkg$|aarch64-apple)", re.I)
A_LIN = re.compile(r"(linux|\.deb$|\.rpm$|\.appimage$|musl|unknown-linux)", re.I)

# ---------------------------------------------------------------- README prose
P_WSL = re.compile(r"\bWSL\s*2?\b|Windows Subsystem for Linux", re.I)
P_WIN = re.compile(r"\bwindows\b", re.I)
P_MAC = re.compile(r"\bmac\s?os\b|\bmacos\b|\bOS X\b|Apple Silicon|\bM[1-4]\s+Mac", re.I)
P_LIN = re.compile(r"\blinux\b|\bubuntu\b|\bdebian\b", re.I)
P_XPLAT = re.compile(r"cross[- ]platform|all (?:major )?platforms|any OS|Windows,? (?:and )?(?:macOS|Mac)|macOS,? Linux,? and Windows|Windows, macOS, (?:and )?Linux", re.I)
P_MAC_ONLY = re.compile(r"macOS[- ]only|only (?:on|for|supports) macOS|currently (?:only )?macOS|native macOS (?:app|terminal|IDE)|requires macOS|macOS \(Apple Silicon\)|Mac[- ]only", re.I)
P_WIN_NOT = re.compile(r"Windows (?:is )?not (?:yet )?supported|no Windows support|does not support Windows|Windows support is planned|Linux and macOS only|macOS and Linux only", re.I)
P_DOCKER = re.compile(r"docker (?:run|compose|build)|docker-compose|\bDockerfile\b|ghcr\.io|docker pull", re.I)
P_TMUX = re.compile(r"\btmux\b", re.I)
P_CLOUD = re.compile(r"GitHub Action|Cloudflare Workers?|AWS Lambda|\bVercel\b|Kubernetes|\bhelm install\b|self-host(?:ed|able)", re.I)
# Only an action if the README tells you to `uses:` *this* repo -- a README that
# merely shows actions/checkout is a normal project, not an Action.
def action_re(repo: str) -> re.Pattern:
    return re.compile(rf"uses:\s*[\w.-]+/{re.escape(repo)}@", re.I)

# ---------------------------------------------------------------- install commands
# (priority, label, os hint, regex)
# Every pattern is line-bounded ([ \t] rather than \s): plain \s+ crosses newlines,
# which glued two neighbouring snippets into one bogus command.
INSTALLERS = [
    (10, "winget",  "win",    re.compile(r"^[ \t]*winget install[ \t]+[^\n|&;]+", re.I | re.M)),
    (10, "scoop",   "win",    re.compile(r"^[ \t]*scoop (?:bucket add[^\n]+\n[ \t]*scoop )?install[ \t]+[^\n|&;]+", re.I | re.M)),
    (10, "choco",   "win",    re.compile(r"^[ \t]*choco install[ \t]+[^\n|&;]+", re.I | re.M)),
    (9,  "psh",     "win",    re.compile(r"^[ \t]*(?:irm|iwr)[ \t]+\S+[ \t]*\|[ \t]*iex[^\n]*", re.I | re.M)),
    (8,  "gh-ext",  "go",     re.compile(r"^[ \t]*gh extension install[ \t]+[^\n|&;]+", re.I | re.M)),
    (8,  "npm",     "node",   re.compile(r"^[ \t]*(?:npm|pnpm|yarn)[ \t]+(?:i|install|add)[ \t]+(?:-g|--global)[ \t]+[^\n|&;]+", re.I | re.M)),
    (7,  "deno",    "node",   re.compile(r"^[ \t]*deno install[ \t]+[^\n|&;]+", re.I | re.M)),
    (3,  "helm",    "docker", re.compile(r"^[ \t]*helm install[ \t]+[^\n|&;]+", re.I | re.M)),
    (8,  "npx",     "node",   re.compile(r"^[ \t]*(?:npx|pnpm dlx|bunx)[ \t]+[^\n|&;]+", re.I | re.M)),
    (8,  "bun",     "node",   re.compile(r"^[ \t]*bun (?:add|install)[ \t]+(?:-g|--global)[ \t]+[^\n|&;]+", re.I | re.M)),
    (7,  "cargo",   "rust",   re.compile(r"^[ \t]*cargo (?:install|binstall)[ \t]+[^\n|&;]+", re.I | re.M)),
    (7,  "go",      "go",     re.compile(r"^[ \t]*go install[ \t]+[^\n|&;]+", re.I | re.M)),
    (7,  "uv",      "python", re.compile(r"^[ \t]*(?:uvx|uv tool install)[ \t]+[^\n|&;]+", re.I | re.M)),
    (7,  "pipx",    "python", re.compile(r"^[ \t]*pipx install[ \t]+[^\n|&;]+", re.I | re.M)),
    (6,  "pip",     "python", re.compile(r"^[ \t]*pip3? install[ \t]+(?!-r\b)[^\n|&;]+", re.I | re.M)),
    (5,  "brew",    "mac",    re.compile(r"^[ \t]*brew (?:install|tap)[ \t]+[^\n|&;]+", re.I | re.M)),
    (4,  "script",  "unix",   re.compile(r"^[ \t]*(?:curl|wget)[ \t]+[^\n]*?\|[ \t]*(?:sudo[ \t]+)?(?:ba)?sh[^\n]*", re.I | re.M)),
    (3,  "docker",  "docker", re.compile(r"^[ \t]*docker (?:run|compose up)[ \t]+[^\n]+", re.I | re.M)),
    (1,  "clone",   "src",    re.compile(r"^[ \t]*git clone[ \t]+\S+", re.I | re.M)),
]

DEV_HEADING = re.compile(r"^#{1,4}\s*(?:contributing|development|develop|building from source|build from source|for developers|local development)", re.I | re.M)

# ---------------------------------------------------------------- images
MD_IMG = re.compile(r"!\[(?P<alt>[^\]]*)\]\(\s*(?P<url>[^)\s]+)(?:\s+\"[^\"]*\")?\s*\)")
HTML_IMG = re.compile(r"<img[^>]+src=[\"'](?P<url>[^\"']+)[\"'][^>]*>", re.I)
BADGE_HOST = re.compile(r"(shields\.io|badgen\.net|badge\.fury|awesome\.re|forthebadge|img\.badgesize|codecov\.io|coveralls|travis-ci|circleci|app\.netlify|vercel\.com/button|deploy\.workers|herokucdn|visitor-badge|hits\.dwyl|star-history|contrib\.rocks|skillicons|opencollective|patreon|buymeacoffee|ko-fi|gitads|repobeats)", re.I)
BADGE_PATH = re.compile(r"(badge|shield|button|logo|icon|favicon|sponsor|license|discord\.svg|slack\.svg|twitter|npm-version)", re.I)
SHOT_HINT = re.compile(r"(screenshot|screen-shot|screen_shot|demo|preview|hero|banner|cover|showcase|ui[-_.]|app[-_.]|main[-_.]|dashboard|example|usage|overview|light|dark)", re.I)
RASTER = re.compile(r"\.(png|jpe?g|gif|webp|avif)(\?|$)", re.I)


def norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def code_regions(md: str) -> str:
    """Fenced blocks plus inline code -- where install commands actually live."""
    fences = re.findall(r"```[^\n]*\n(.*?)```", md, re.S)
    inline = re.findall(r"`([^`\n]{3,200})`", md)
    return "\n".join(fences) + "\n" + "\n".join(inline)


# Word-pieces too generic to prove a command belongs to this project: a README
# for `claude-squad` showing `npm i -g @anthropic-ai/claude-code` must not match.
GENERIC_PIECE = {
    "claude", "agent", "agents", "agentic", "code", "coding", "openai", "anthropic",
    "gemini", "codex", "opencode", "tools", "tool", "server", "client", "cloud",
    "swarm", "runner", "orchestrator", "assistant", "python", "node", "rust",
}


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def name_tokens(entry: dict) -> tuple[set[str], set[str]]:
    """(strong, weak) tokens whose presence marks a command as this project's.

    Strong = the tool's own name; weak = the owner or its website, which can also
    front sibling packages (`plasma-ai/fractal` documents `plasma-wiki` too), so a
    weak-only match loses to a strong one.
    """
    strong: set[str] = set()
    weak: set[str] = set()
    for whole, bucket in ((entry["repo"], strong), (entry["name"], strong), (entry["owner"], weak)):
        s = slug(whole)
        if len(s) >= 2:
            bucket.add(s)
        # Hyphen/underscore pieces, but only distinctive ones.
        for piece in re.split(r"[-_.\s]+", (whole or "").lower()):
            p = slug(piece)
            if len(p) >= 5 and p not in GENERIC_PIECE:
                bucket.add(p)
    home = (entry.get("homepage") or "").lower()
    host = re.sub(r"^https?://(www\.)?", "", home).split("/")[0]
    label = slug(host.split(".")[0])
    if len(label) >= 4:
        weak.add(label)
    return {t for t in strong if t}, {t for t in weak if t} - strong


def pick_install(md: str, entry: dict) -> tuple[str, str, str]:
    """Return (command, method, os_hint). Prefers pre-'Contributing' commands.

    Only a command that names *this* project is trusted. A generic one is usually
    a prerequisite (`winget install --id GitHub.cli`, `pip install setuptools`),
    and shipping that as the install line is worse than shipping nothing -- the
    caller falls back to `git clone`, which always works.
    """
    dev = DEV_HEADING.search(md)
    head = md[: dev.start()] if dev else md
    strong, weak = name_tokens(entry)

    cands: list[tuple[int, str, str, str]] = []
    for scope, penalty in ((head, 0), (md, 1)):
        code = code_regions(scope)
        if not code.strip():
            continue
        for prio, method, os_hint, rx in INSTALLERS:
            for m in rx.finditer(code):
                cmd = norm_ws(m.group(0))
                if len(cmd) > 160 or len(cmd) < 5:
                    continue
                # A bare `pip install .` / `npx .` is not a usable install line.
                if cmd.rstrip().endswith((" .", " ./", " -r")):
                    continue
                s = slug(cmd)
                if any(t in s for t in strong):
                    bonus = 30
                elif any(t in s for t in weak):
                    bonus = 0
                else:
                    continue
                cands.append((prio * 10 - penalty * 5 + bonus, cmd, method, os_hint))

    if not cands:
        return "", "", ""
    cands.sort(key=lambda c: -c[0])
    return cands[0][1], cands[0][2], cands[0][3]


def shot_candidates(md: str, entry: dict, branch: str) -> list[str]:
    raw_base = f"https://raw.githubusercontent.com/{entry['nwo']}/{branch or 'HEAD'}/"
    found, seen = [], set()

    for m in list(MD_IMG.finditer(md)) + list(HTML_IMG.finditer(md)):
        url = (m.group("url") or "").strip()
        alt = (m.groupdict().get("alt") or "")
        if not url or url.startswith("data:"):
            continue
        if BADGE_HOST.search(url) or BADGE_PATH.search(url.rsplit("/", 1)[-1]):
            continue

        if url.startswith("//"):
            url = "https:" + url
        elif not url.startswith("http"):
            url = urljoin(raw_base, quote(url.lstrip("./"), safe="/._-~%"))
        # Point blob/raw URLs at the raw host.
        url = re.sub(r"https://github\.com/([^/]+/[^/]+)/(?:blob|raw)/", r"https://raw.githubusercontent.com/\1/", url)

        is_attachment = "user-attachments/assets" in url or "githubusercontent.com" in url
        if not RASTER.search(url) and not is_attachment:
            continue  # skip SVG/unknown: badges mostly, and not embeddable
        if url in seen:
            continue
        seen.add(url)

        score = 0
        if SHOT_HINT.search(url) or SHOT_HINT.search(alt):
            score += 3
        if "user-attachments/assets" in url:
            score += 2  # drag-and-dropped screenshots
        if re.search(r"\.gif(\?|$)", url, re.I):
            score += 1  # demo recordings
        found.append((score, len(found), url))

    found.sort(key=lambda t: (-t[0], t[1]))
    return [u for _, _, u in found[:4]]


def classify(entry: dict, meta: dict, rel: dict, md: str, has_action_yml: bool = False) -> dict:
    assets = rel.get("assets") or []
    lang = ((meta.get("primaryLanguage") or {}).get("name")) or ""
    topics = [n["topic"]["name"] for n in ((meta.get("repositoryTopics") or {}).get("nodes") or [])]
    hay = md + "\n" + (meta.get("description") or "") + "\n" + entry["description"] + "\n" + " ".join(topics)

    win = mac = lin = doc = NO
    wsl = NO
    ev: list[str] = []
    conf = "Low"
    win_blocked = False   # a hard Unix-only dep or explicit "no Windows"
    mac_only = False      # a native macOS app: never claim Linux/WSL2 for it

    cmd, method, os_hint = pick_install(
        md, {**entry, "homepage": (meta.get("homepageUrl") or "")}
    )

    # --- 1. release assets (strongest) -------------------------------------
    a_win = [a for a in assets if A_WIN.search(a)]
    a_mac = [a for a in assets if A_MAC.search(a)]
    a_lin = [a for a in assets if A_LIN.search(a)]
    if a_win:
        win, conf = YES, "High"
        ev.append(f"ships Windows build ({a_win[0]})")
    if a_mac:
        mac, conf = YES, "High"
        ev.append(f"ships macOS build ({a_mac[0]})")
    if a_lin:
        lin, conf = YES, "High"
        ev.append(f"ships Linux build ({a_lin[0]})")

    # --- 2. explicit prose -------------------------------------------------
    # A repo can ship an action.yml *and* be a normal CLI (bernstein, skillfold).
    # Only call it CI-only when there is no local install path at all.
    is_action = has_action_yml or bool(action_re(entry["repo"]).search(md))
    action_only = is_action and not assets and os_hint not in ("win", "mac", "unix", "node", "python", "rust", "go")

    if P_MAC_ONLY.search(hay) and not a_win:
        m = P_MAC_ONLY.search(hay)
        ev.append(f'README says macOS-only ("{norm_ws(m.group(0))[:40]}")')
        mac, conf = YES, "High"
        win, win_blocked, mac_only = NO, True, True
        if not a_lin:
            lin = NO
    if P_WIN_NOT.search(hay) and not a_win:
        ev.append("README says Windows unsupported")
        win, win_blocked, conf = NO, True, "High"

    if P_XPLAT.search(hay) and not mac_only:
        ev.append("README states cross-platform")
        conf = "High"
        if not win_blocked:
            win = YES if win == NO else win
        mac = YES if mac == NO else mac
        lin = YES if lin == NO else lin

    # A hard tmux dependency rules out *native* Windows but is fine under WSL2.
    if P_TMUX.search(hay) and not a_win and os_hint != "win":
        ev.append("requires tmux (Unix-only)")
        win, win_blocked = NO, True
        conf = "High" if conf == "Low" else conf
        if not mac_only:
            lin = YES if lin == NO else lin
            wsl = YES

    if P_WSL.search(hay) and not mac_only:
        wsl = YES
        ev.append("README documents WSL")
        if conf == "Low":
            conf = "Medium"

    # --- 3/4. installer + runtime inference --------------------------------
    if method:
        ev.append(f"install via {method}")
    if os_hint == "win" and not win_blocked:
        win, conf = YES, "High"
    if os_hint == "mac" and mac == NO:
        mac = YES
    if os_hint == "unix":
        mac = YES if mac == NO else mac
        if not mac_only:
            lin = YES if lin == NO else lin
            if win == NO:
                wsl = YES
    if os_hint in ("node", "python", "rust", "go"):
        if not win_blocked:
            win = LIKELY if win == NO else win
            if conf == "Low":
                conf = "Medium"
        mac = LIKELY if mac == NO else mac
        if not mac_only:
            lin = LIKELY if lin == NO else lin
        ev.append(f"portable runtime ({os_hint})")

    if P_DOCKER.search(hay) and not mac_only:
        doc = YES
        ev.append("Docker supported")
        lin = YES if lin == NO else lin
        if win == NO:
            wsl = YES  # Docker Desktop on Windows is WSL2-backed

    # Fallbacks from language when nothing else fired.
    if win == mac == lin == NO and doc == NO:
        if lang in ("Rust", "Go", "TypeScript", "JavaScript", "Python", "C#", "Zig"):
            if not win_blocked:
                win = LIKELY
            mac = LIKELY
            if not mac_only:
                lin = LIKELY
            ev.append(f"inferred from language ({lang})")
        elif lang == "Swift":
            mac, conf, mac_only = YES, "Medium", True
            ev.append("Swift -> macOS")

    if P_MAC.search(hay) and mac == NO:
        mac = LIKELY
    if P_LIN.search(hay) and lin == NO and not mac_only:
        lin = LIKELY
    if P_WIN.search(hay) and win == NO and not win_blocked:
        win = LIKELY
        ev.append("README mentions Windows")

    # WSL2 is available whenever some Unix target works.
    if wsl == NO and not mac_only and (lin in (YES, LIKELY)):
        wsl = LIKELY

    cloud = YES if P_CLOUD.search(hay) else NO

    # A pure GitHub Action never gets installed on your box -- it runs on a runner.
    if action_only:
        ev.insert(0, "GitHub Action: runs on a CI runner, not installed locally")
        win = wsl = mac = lin = doc = "n/a"
        cloud, conf = YES, "High"
        summary = "Hosted CI - drive from any OS"
        cmd, method = f"uses: {entry['nwo']}@main   # in .github/workflows/*.yml", "gh-action"
    else:
        # Confirmed platforms first, then unconfirmed ones marked with "?".
        pairs = (("Win", win), ("WSL2", wsl), ("macOS", mac), ("Linux", lin), ("Docker", doc))
        parts = [lbl for lbl, val in pairs if val == YES] + [f"{lbl}?" for lbl, val in pairs if val == LIKELY]
        summary = " · ".join(parts) or "Unknown"

    # Always leave the user something runnable to copy.
    if not cmd:
        cmd, method = f"git clone {entry['url']}.git", method or "source"

    return {
        "win_native": win,
        "win_wsl2": wsl,
        "macos": mac,
        "linux": lin,
        "docker": doc,
        "cloud": cloud,
        "gh_action": YES if is_action else NO,
        "os_summary": summary,
        "os_confidence": conf,
        "os_evidence": "; ".join(dict.fromkeys(ev))[:300] or "no platform signal found",
        "install_cmd": cmd,
        "install_method": method or ("release" if assets else "source"),
        "language": lang,
        "topics": topics[:8],
    }


def main() -> None:
    entries = json.loads((CACHE / "entries.json").read_text(encoding="utf-8"))
    meta = json.loads((CACHE / "meta.json").read_text(encoding="utf-8"))
    rel = json.loads((CACHE / "releases.json").read_text(encoding="utf-8"))
    acts = json.loads((CACHE / "actions.json").read_text(encoding="utf-8"))

    records = []
    for e in entries:
        m = meta.get(e["nwo"], {})
        safe = e["nwo"].replace("/", "__")
        p = READMES / f"{safe}.md"
        md = p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""
        branch = ((m.get("defaultBranchRef") or {}).get("name")) or "HEAD"

        rec = dict(e)
        if "error" in m:
            rec.update(
                stars=0, forks=0, archived=False, language="", license="", homepage="",
                pushed_at="", created_at="", gh_description="",
                win_native="No", win_wsl2="No", macos="No", linux="No", docker="No", cloud="No",
                os_summary="Repo unavailable", os_confidence="n/a",
                os_evidence="GitHub returned 404 - repo deleted, renamed, or made private",
                install_cmd="", install_method="unavailable", topics=[], shots=[],
                gh_action="No", unavailable=True,
            )
            records.append(rec)
            continue

        c = classify(e, m, rel.get(e["nwo"], {}), md, acts.get(e["nwo"], False))
        rec.update(c)
        rec.update(
            stars=m.get("stargazerCount") or 0,
            forks=m.get("forkCount") or 0,
            archived=bool(m.get("isArchived")),
            license=((m.get("licenseInfo") or {}).get("spdxId")) or "",
            homepage=(m.get("homepageUrl") or "").strip(),
            pushed_at=(m.get("pushedAt") or "")[:10],
            created_at=(m.get("createdAt") or "")[:10],
            gh_description=m.get("description") or "",
            branch=branch,
            shots=shot_candidates(md, e, branch),
            readme_bytes=m.get("readme_bytes", 0),
            unavailable=False,
        )
        records.append(rec)

    out = CACHE / "records.json"
    out.write_text(json.dumps(records, indent=1, ensure_ascii=False), encoding="utf-8")

    def cnt(field, val=YES):
        return sum(1 for r in records if r.get(field) == val)

    print(f"classified {len(records)} records -> {out}\n")
    print(f"{'':22} {'Yes':>5} {'Likely':>7}")
    for f, lbl in (("win_native", "Windows native"), ("win_wsl2", "WSL2"), ("macos", "macOS"),
                   ("linux", "Linux"), ("docker", "Docker"), ("cloud", "Cloud/CI")):
        print(f"  {lbl:20} {cnt(f):5d} {cnt(f, LIKELY):7d}")
    print(f"\n  install command found : {sum(1 for r in records if r['install_cmd'])}/{len(records)}")
    print(f"  screenshot candidates : {sum(1 for r in records if r['shots'])}/{len(records)}")
    print(f"  confidence High/Med/Low: {cnt('os_confidence','High')}/{cnt('os_confidence','Medium')}/{cnt('os_confidence','Low')}")


if __name__ == "__main__":
    main()
