"""The homepage's two daily slots -- the spotlight and the line of the day -- off the generator.

Both are picked in the reader's browser, by the reader's calendar date, out of a pool `31_home.py` inlines
into the page; the note above `SPOT_POOL_N` there says why. `tests/spotlight-check.mjs` watches that happen
in a real browser against the committed page. This file holds the other half, the half no browser can see:

  the rule       -- `spot_day()` is days since 1970-01-01, and `spot_index()` that modulo the pool. Two
                    consecutive dates never give the same index; no index repeats inside any window of
                    pool-length days; one date always gives one index. Checked over two years of dates.
  one rule, two  -- the *rendered* page's pickers, run under node against a stub document, with the
    languages       process's zone set to Chicago and the clock pinned, choose exactly the card and the
                    line `spot_index()` does -- at noon, at 00:01 and 23:59, across a month end, a year
                    end and a leap day. Read out of the rendered page rather than the Python constants, so
                    it is the comment-stripped bytes a reader runs that are exercised. Also that a picker
                    whose pool does not parse still draws the `<noscript>` card rather than nothing.
  the pool       -- thirty-one distinct projects, every one of them eligible by the rule `spot_eligible()`
                    states, which is itself re-derived here from the row fields rather than by calling it,
                    and none of them showing a GIF. The build day's card is the one in the `<noscript>`.
  the page       -- the order the pickers depend on: the day, then the pool, then the picker, then the
                    fallback; the line's slot, then its pool, then its picker. That the pool's markup cannot
                    end its own `<script>` element, and that nothing outside the `<noscript>` reads as a
                    spotlight card or a picture to anything that scans the page by pattern.
  the lines      -- `daily_lines()` accepts the committed file and refuses each defect it claims to: a
                    duplicate id, an unknown kind, text over the limit, markup in the text, a friend line
                    with no friend, a `javascript:` or protocol-relative href. On a copy it mutates, since
                    the committed file passes. And that with no file there is no slot, rather than an empty
                    one or a failed build.

Nothing here writes to `docs/`. It reads the committed `docs/data.json` and `docs/assets/daily-lines.json`.

Run: python tests/spotlight_test.py
"""
from __future__ import annotations

import datetime
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

ok = bad = 0


def true(name: str, cond, detail: str = "") -> None:
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}" + (f"\n  {detail}" if detail else ""))


def eq(name: str, got, want) -> None:
    true(name, got == want, f"got {got!r}, want {want!r}")


def load(name: str, file: str):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / file)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


b31 = load("b31", "31_home.py")
b30 = b31.b30
N = b31.SPOT_POOL_N
TODAY = b30.discover.today()


# =====================================================================  1. the rule
start = datetime.date(2026, 1, 1)
dates = [(start + datetime.timedelta(days=i)).isoformat() for i in range(731)]
idx = [b31.spot_index(d, N) for d in dates]
true("two consecutive dates never share a spotlight, over two years",
     all(a != b for a, b in zip(idx, idx[1:])))
true(f"no pick repeats inside any {N} consecutive days",
     all(len(set(idx[i:i + N])) == N for i in range(len(idx) - N + 1)))
eq("the same date always gives the same pick", [b31.spot_index(d, N) for d in dates[:40]], idx[:40])
eq("day 0 is 1970-01-01", b31.spot_day("1970-01-01"), 0)
eq("...and the day number is a plain day count across a leap day", b31.spot_day("2028-03-01") -
   b31.spot_day("2028-02-28"), 2)


# =====================================================================  2. the pool
pool, eligible_n = b31.spot_pool()
nwos = [b30.g(r, "nwo") for r in pool]
eq(f"the pool is {N} projects", len(pool), N)
eq("...no project twice", len(set(nwos)), N)
# The eligibility rule, restated from the row fields, so a `spot_eligible()` that drifted from its own
# docstring is red here rather than agreed with.
for r in pool:
    f = b30.face(r)
    n = f["nwo"]
    true(f"{n}: outside the top 200", n not in b30.TOP200)
    true(f"{n}: has an install command", bool(b30.g(r, "install")))
    true(f"{n}: named by two or more lists", (b30.g(r, "lists") or 1) >= 2)
    true(f"{n}: pushed recently (hot or warm)", f["fresh"] in ("hot", "warm"), f["fresh"])
    true(f"{n}: has a blurb", bool(f["blurb"].strip()))
cards = [b31.hero_card(r, eligible_n) for r in pool]
for c, n in zip(cards, nwos):
    img = re.findall(r"<img\b[^>]*>", c)
    true(f"{n}: its card has exactly one picture, and it is not a GIF",
         len(img) == 1 and not re.search(r'src="[^"]*\.gif(?:[?#"])', img[0], re.I), str(img))
true("the eligible set is larger than the pool, so the next snapshot can deal a different one",
     eligible_n > N, str(eligible_n))


# =====================================================================  3. the page
page = b31.render()
spot_at = page.find('<script type="application/json" id="spotpool">')
day_at = page.find("const ATLASDAY")
ns_open = page.find("<noscript>", spot_at)
ns_close = page.find("</noscript>", ns_open)
pool_json = page[page.index(">", spot_at) + 1:page.index("</script>", spot_at)]
true("the page carries the spotlight's pool", spot_at > 0)
true("...after the script that decides the day", 0 < day_at < spot_at)
picker = re.search(r"<script>\s*(\(\(\) => \{\n  const me = document\.currentScript.*?)</script>", page, re.S)
true("...then the picker", picker and spot_at < picker.start() < ns_open)
true("...then the fallback, in a <noscript>", 0 < ns_open < ns_close)
page_cards = json.loads(pool_json)
eq("the page's pool is the generator's, card for card", page_cards, cards)
true("the pool's markup cannot end its <script> element", "</" not in pool_json and "<!--" not in pool_json)
fallback = page[ns_open + len("<noscript>"):ns_close]
eq("the <noscript> card is the build day's pick", fallback, cards[b31.spot_index(TODAY, N)])
outside = page[:ns_open] + page[ns_close:]
eq("no spotlight card is markup outside the <noscript>", len(re.findall(r'<article class="hero"', outside)), 0)
true("no picture in the pool reads as a picture to a pattern scan",
     not re.search(r'<img\b[^>]*\bsrc="', pool_json))

lines = b31.daily_lines()
true("the committed line file loads and validates", len(lines) > 0, str(len(lines)))
slot = page.find('<aside class="daily"')
lines_at = page.find('<script type="application/json" id="dailylines">')
dpick = page.find('const box = document.querySelector("[data-daily]")')
true("the line of the day: slot, then its pool, then its picker", 0 < slot < lines_at < dpick)
true("...and all three after the spotlight", slot > ns_close)
m = re.search(r'<aside class="daily"[^>]*data-line="([^"]+)"', page)
eq("the slot is drawn with the build day's line", m and m.group(1), lines[b31.spot_index(TODAY, len(lines))]["id"])


# =====================================================================  4. one rule, two languages
node = shutil.which("node")
true("node is on PATH (the pickers are JavaScript and are run, not read)", node)
scripts = re.findall(r"<script>(.*?)</script>", page, re.S)
daypick = next((s for s in scripts if "const ATLASDAY" in s), None)
spotpick = next((s for s in scripts if "document.currentScript" in s and "spotpool" in s), None)
dailypick = next((s for s in scripts if "[data-daily]" in s and "dailylines" in s), None)
true("the three pickers are in the rendered page", daypick and spotpick and dailypick)
lines_json = page[page.index(">", lines_at) + 1:page.index("</script>", lines_at)]

HARNESS = r"""
const vm = require("vm");
const {daypick, spotpick, dailypick, pool, lines, fallback, cases} = JSON.parse(require("fs").readFileSync(0, "utf8"));
const out = cases.map(([y, mo, d, h, mi, broken]) => {
  const R = Date, T = new R(y, mo - 1, d, h, mi).getTime();
  class D extends R { constructor(...a) { a.length ? super(...a) : super(T); } static now() { return T; } }
  let inserted = null;
  const ds = {};
  const box = {dataset: ds, querySelector: (sel) => sel === "[data-k]" ? kick : text};
  const kick = {textContent: ""}, text = {textContent: "", kids: [], appendChild(k) { this.kids.push(k); }};
  const me = {nextElementSibling: {textContent: fallback},
              insertAdjacentHTML: (where, html) => { inserted = [where, html]; }};
  const document = {
    currentScript: me,
    getElementById: (id) => ({textContent: id === "spotpool" ? (broken ? "{not json" : pool) : lines}),
    querySelector: () => box,
    createElement: (tag) => ({tag, textContent: "", href: ""}),
  };
  const ctx = vm.createContext({Date: D, document, String, Math, JSON});
  vm.runInContext(daypick + "\n" + spotpick + "\n" + dailypick, ctx);
  const k = text.kids[0] || {};
  return {where: inserted && inserted[0], html: inserted && inserted[1], iso: vm.runInContext("ATLASDAY.iso", ctx),
          line: ds.line, friend: ds.friend || null, kick: kick.textContent, text: k.textContent,
          tag: k.tag, href: k.href || null};
});
process.stdout.write(JSON.stringify(out));
"""
# Noon on dates across a month end, a year end and a leap day; the first and last minute of one date; and
# half past nine at night, which is already the next day in UTC. The last case has a pool that does not
# parse.
CASES = [(2026, 9, 30, 12, 0), (2026, 10, 1, 12, 0), (2026, 12, 31, 12, 0), (2027, 1, 1, 12, 0),
         (2028, 2, 28, 12, 0), (2028, 2, 29, 12, 0), (2028, 3, 1, 12, 0),
         (2026, 10, 2, 0, 1), (2026, 10, 2, 23, 59), (2026, 10, 2, 21, 30)]
if node and daypick and spotpick and dailypick:
    payload = json.dumps({"daypick": daypick, "spotpick": spotpick, "dailypick": dailypick, "pool": pool_json,
                          "lines": lines_json, "fallback": fallback,
                          "cases": [[*c, False] for c in CASES] + [[2026, 10, 1, 12, 0, True]]})
    res = subprocess.run([node, "-e", HARNESS], input=payload, capture_output=True, text=True, encoding="utf-8",
                         env={**os.environ, "TZ": "America/Chicago"})
    true("the pickers ran under node", res.returncode == 0, res.stderr[-800:])
    got = json.loads(res.stdout) if res.returncode == 0 else []
    for c, g in zip(CASES, got):
        day = f"{c[0]:04d}-{c[1]:02d}-{c[2]:02d}"
        at = f"{day} {c[3]:02d}:{c[4]:02d}"
        eq(f"{at}: the page's day is the reader's local date", g["iso"], day)
        eq(f"{at}: the card is inserted in front of the picker", g["where"], "beforebegin")
        eq(f"{at}: ...and it is spot_index()'s card", g["html"], cards[b31.spot_index(day, N)])
        want = lines[b31.spot_index(day, len(lines))]
        eq(f"{at}: the line is spot_index()'s line", g["line"], want["id"])
        eq(f"{at}: ...its text, as text", g["text"], want["text"])
        eq(f"{at}: ...a link exactly when the line has one", (g["tag"], g["href"]),
           ("a", want["href"]) if want.get("href") else ("span", None))
        eq(f"{at}: ...the kicker names its kind", g["kick"], b31.DAILY_KINDS[want["kind"]])
        eq(f"{at}: ...and data-friend is set exactly on a friend line", g["friend"],
           want.get("friend") if want["kind"] == "friend" else None)
    true("a friend line came up in the sample, so the data-friend arm was exercised",
         any(g["friend"] for g in got[:len(CASES)]))
    true("a linked line and an unlinked one both came up in the sample",
         {g["tag"] for g in got[:len(CASES)]} == {"a", "span"})
    if len(got) > len(CASES):
        eq("a pool that does not parse still inserts the <noscript> card", got[-1]["html"], fallback)
    seen = [g["html"] for g in got[:7]]
    true("consecutive sample dates show different cards",
         all(seen[i] != seen[i + 1] for i in (0, 2, 4, 5)))


# =====================================================================  5. the lines
committed = json.loads((ROOT / "docs" / "assets" / b31.DAILY_FILE).read_text(encoding="utf-8"))
tmp = Path(tempfile.mkdtemp(prefix="aaa-daily-"))
try:
    def refused(name: str, mutate) -> None:
        doc = json.loads(json.dumps(committed))
        mutate(doc["lines"])
        p = tmp / "lines.json"
        p.write_text(json.dumps(doc), encoding="utf-8")
        try:
            b31.daily_lines(p)
        except AssertionError:
            true(f"refused: {name}", True)
        else:
            true(f"refused: {name}", False, "daily_lines() accepted it")

    def first(kind):
        return lambda ls: next(ln for ln in ls if ln["kind"] == kind)

    refused("a duplicate id", lambda ls: ls[1].update(id=ls[0]["id"]))
    refused("an unknown kind", lambda ls: ls[0].update(kind="joke"))
    refused("text over the limit", lambda ls: ls[0].update(text="x" * (b31.DAILY_MAX + 1)))
    refused("empty text", lambda ls: ls[0].update(text="   "))
    refused("markup in the text", lambda ls: ls[0].update(text="see <b>this</b>"))
    refused("a friend line with no friend", lambda ls: first("friend")(ls).pop("friend"))
    refused("a javascript: href", lambda ls: ls[0].update(href="javascript:alert(1)"))
    refused("a protocol-relative href", lambda ls: ls[0].update(href="//evil.example/"))
    refused("a plain-http href", lambda ls: ls[0].update(href="http://example.com/"))
    refused("a root-absolute href, which breaks under a project-path host", lambda ls: ls[0].update(href="/catalog/"))
    eq("text at exactly the limit is accepted", len(b31.daily_lines(
        (lambda p: (p.write_text(json.dumps({"version": 1, "lines": [
            {"id": "a", "kind": "tip", "text": "x" * b31.DAILY_MAX}]}), encoding="utf-8"), p)[1])(tmp / "edge.json"))), 1)
    eq("no file, no lines", b31.daily_lines(tmp / "absent.json"), [])
    eq("...and no slot, rather than an empty one", b31.daily_line(lines=[]), "")
    for ln in lines:
        h = ln.get("href")
        if h and not h.startswith("https://"):
            target = ROOT / "docs" / h.split("#")[0].split("?")[0]
            true(f"{ln['id']}: its link {h!r} is a file or directory the site has",
                 target.is_file() or (target / "index.html").is_file(), str(target))
finally:
    shutil.rmtree(tmp, ignore_errors=True)


print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
