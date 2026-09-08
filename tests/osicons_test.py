"""The five platform marks: that they are drawn, that they resolve, and that nothing lost its name.

`scripts/osicons.py` replaced the words Windows, WSL2, macOS, Linux and Docker with marks on four
surfaces at once -- the index's filter chips and its row of five verdicts per project, the 156 facet
pages, the 1,294 detail pages and the curated collections. Three things about that change are invisible
from the outside, and each of them is a way for the site to be quietly wrong rather than visibly broken:

  A `<use>` with no matching `<symbol>` renders NOTHING. Not a broken-image glyph, not a box -- an empty
  inline box the same size as the mark would have been. So a page that lost its sprite, or a typo in one
  id, publishes five invisible verdicts per row and looks, at a glance, like a slightly airy layout. That
  is the single most important assertion in this file: every `<use href="#...">` on every built page
  resolves to a `<symbol>` defined in that same document.

  The marks are paired with platforms BY POSITION. `data.json`'s `os` column is a five-character verdict
  string and the labels are a parallel array, so a reordered or renamed column puts the Docker mark beside
  the Windows answer -- a page that states a falsehood about the one thing a reader came here to check.
  `osicons.check()` is the guard, and every way of breaking the order is exercised here against a copy --
  but it validates the list a generator is *about to* iterate and cannot see what the generator then
  emitted. So the pairing is also checked in the built page, where the symbol id and the platform name
  beside it are the only two things that have to agree, and are next to each other.

  Replacing a word with a picture removes it from everyone who cannot see the picture. A filter chip that
  read "Windows" to a screen reader before this change must still read "Windows" after it. So every mark
  on a page of each family is walked up to its nearest naming ancestor -- a `title`, an `aria-label`, or a
  visually-hidden word, whichever that surface uses -- and the pages are checked for the words still being
  *somewhere* in the document rather than only in the picture.

Six groups:

  the module      -- that LABELS, IDS, TITLES and SHAPES are four parallel structures and not three plus
                     a stale one; that the sprite is well-formed XML with five 24x24 symbols; that no
                     shape hardcodes a colour, because these inherit the verdict's; and that every
                     coordinate is inside the box it declares.
  the guard       -- `check()` on a reorder, a rename, a truncation, an extension and the empty list, plus
                     what the refusal says. A guard nobody has watched fire is a guard nobody should
                     trust, and this one is the difference between a polish and a lie.
  the wiring      -- that all four generators import the module, call the guard, and emit the sprite; and
                     that the two stylesheets carry the rule that makes `currentColor` work.
  the resolution  -- every `<use>` on every built page under docs/, against the symbols in that page.
                     This walks the whole tree rather than a sample: the failure is per-document, so a
                     sample proves nothing about the 1,293 pages it skipped.
  the names       -- that no mark was published without a word reachable beside it, and that the word
                     reachable beside it is its own, on one page of each of the four families. The four
                     surfaces name their marks in three different shapes, so this is an ancestor walk
                     rather than a pattern: a pattern written for one shape finds nothing on the other
                     three, and finding nothing is how a group like this passes while checking nobody.
  the surfaces    -- that the words are gone from the compact places and still present in the explanatory
                     ones. The detail page's platform table keeps its row headers as text; the Markdown
                     under mega-list/ keeps its words entirely, because GitHub strips `<svg>`.

What this cannot see: whether a mark reads as the platform it means. A penguin is a penguin to a person
and a path to a test. That judgement was made by looking at all five rendered at 96px and at 13px in both
themes, which is the only instrument for it, and it is not automatable here.

Standard library only, and no network. Run: python tests/osicons_test.py
"""
from __future__ import annotations

import copy
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
DOCS = ROOT / "docs"

sys.path.insert(0, str(SCRIPTS))
import osicons  # noqa: E402

ok = bad = 0


def eq(name: str, got, want) -> None:
    global ok, bad
    if got == want:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}\n  got  {got!r}\n  want {want!r}")


def true(name: str, cond, detail: str = "") -> None:
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}" + (f"\n  {detail}" if detail else ""))


def raises(name: str, kind, fn) -> str:
    global ok, bad
    try:
        fn()
    except kind as e:
        ok += 1
        return str(e)
    bad += 1
    print(f"FAIL {name} did not raise {kind.__name__}")
    return ""


def says(name: str, text: str, needle: str) -> None:
    true(name, needle in text, f"{needle!r} is not in the {len(text)} characters given")


# --------------------------------------------------------------------------- the module

print("── the module " + "─" * 83)

eq("five platforms", len(osicons.LABELS), 5)
eq("...the ones the atlas records", osicons.LABELS, ["Windows", "WSL2", "macOS", "Linux", "Docker"])
eq("one id per platform", len(osicons.IDS), len(osicons.LABELS))
eq("...all distinct", len(set(osicons.IDS)), len(osicons.IDS))
eq("one shape per id", sorted(osicons.SHAPES), sorted(osicons.IDS))
eq("one hover title per platform", sorted(osicons.TITLES), sorted(osicons.LABELS))
for i in osicons.IDS:
    true(f"{i} is usable as an HTML id and a CSS selector", re.fullmatch(r"[a-z][a-z0-9-]*", i), i)
# The one platform whose mark cannot be recognised on sight is the one whose title has to say more than
# its label already does. If this ever passes trivially, the hover has stopped being worth having.
true("WSL2's hover explains the abbreviation", len(osicons.TITLES["WSL2"]) > len("WSL2") + 8,
     osicons.TITLES["WSL2"])
says("...by naming Linux", osicons.TITLES["WSL2"], "Linux")

eq("the ids round-trip through the JavaScript literal", json.loads(osicons.JS_IDS), osicons.IDS)
says("the shared rule exists", osicons.CSS, ".oi{")
says("...and inherits the verdict's colour", osicons.CSS, "fill:currentColor")
says("...and there is a class that keeps a mark and its word on one line", osicons.CSS, ".oiw{")
says("...which is what that means", osicons.CSS, "white-space:nowrap")

# The sprite, parsed rather than pattern-matched. A malformed sprite is the one failure mode that takes
# every mark on the page down with it, and `<` counting cannot see an unclosed tag.
eq("one sprite element", osicons.SPRITE.count("<svg"), 1)
eq("...holding five symbols", osicons.SPRITE.count("<symbol"), 5)
says("...not drawn where it is defined", osicons.SPRITE, "display:none")
says("...and not announced", osicons.SPRITE, 'aria-hidden="true"')
sprite = raises_root = None
try:
    sprite = ET.fromstring(osicons.SPRITE)
    ok += 1
except ET.ParseError as e:
    bad += 1
    print(f"FAIL the sprite is well-formed XML\n  {e}")

if sprite is not None:
    NS = "{http://www.w3.org/2000/svg}"
    syms = list(sprite)
    eq("the symbols are in the declared order", [s.get("id") for s in syms], osicons.IDS)
    for s in syms:
        i = s.get("id")
        eq(f"{i} declares the 24x24 grid its coordinates are in", s.get("viewBox"), "0 0 24 24")
        true(f"{i} draws something", len(list(s)) > 0)
        for shape in s.iter():
            if shape is s:
                continue
            tag = shape.tag.replace(NS, "")
            true(f"{i} uses a primitive this needs no library to render: {tag}",
                 tag in ("path", "circle", "ellipse", "rect", "polygon"), tag)
            # These inherit the verdict's colour -- green for a stated Yes, amber for an inference, grey
            # for no evidence, and different again in each theme. A hardcoded fill would be invisible
            # against one of those backgrounds and wrong against all of them.
            for attr in ("fill", "stroke", "style"):
                v = shape.get(attr) or ""
                true(f"{i}/{tag} hardcodes no colour in @{attr}",
                     not re.search(r"#[0-9a-f]{3}|rgb\(|currentcolor|white|black|var\(", v, re.I), v)
    # A coordinate typo -- 120 where 12 was meant -- does not fail to render. It draws the mark somewhere
    # off the side of its own viewBox, which is to say it draws nothing, on a page where the other four
    # marks are fine and nothing looks broken. Two checks, because the two kinds of shape differ:
    #
    # `circle`/`ellipse`/`rect` carry absolute coordinates, so their extent is arithmetic and the box can
    # be checked exactly. Path data is mostly *relative* -- `h20`, `v-13`, `l-3.8 4.1` -- so a negative
    # number in it is ordinary and following it would mean writing a path interpreter. The magnitude is
    # checked instead, which is the guard that actually catches the typo class: a misplaced decimal point
    # or a dropped separator turns 12 into 120, and nothing legitimate here is over 24 long.
    for s in syms:
        for shape in s.iter():
            if shape is s:
                continue
            tag, i = shape.tag.replace(NS, ""), s.get("id")
            g = lambda a: float(shape.get(a) or 0)  # noqa: E731
            if tag == "circle":
                box = (g("cx") - g("r"), g("cy") - g("r"), g("cx") + g("r"), g("cy") + g("r"))
            elif tag == "ellipse":
                box = (g("cx") - g("rx"), g("cy") - g("ry"), g("cx") + g("rx"), g("cy") + g("ry"))
            elif tag == "rect":
                box = (g("x"), g("y"), g("x") + g("width"), g("y") + g("height"))
            else:
                spans = [abs(float(n)) for n in re.findall(r"-?\d+(?:\.\d+)?", shape.get("d") or "")]
                eq(f"{i}/{tag} has no coordinate longer than the grid it is drawn on",
                   [n for n in spans if n > 24.0], [])
                continue
            eq(f"{i}/{tag} stays inside its own 24x24 viewBox",
               [round(v, 2) for v in box if not -0.5 <= v <= 24.5], [])

for k, lab in enumerate(osicons.LABELS):
    u = osicons.use(k)
    says(f"the mark for {lab} points at its symbol", u, f'href="#{osicons.IDS[k]}"')
    says(f"...and is hidden from a screen reader, which reads the word instead ({lab})",
         u, 'aria-hidden="true"')
    says(f"...and is not a tab stop in older engines ({lab})", u, 'focusable="false"')
    eq(f"...and is one element ({lab})", u.count("<svg"), 1)
    eq(f"osicons.title({k}) is {lab}'s", osicons.title(k), osicons.TITLES[lab])
eq("a caller may name its own class", osicons.use(0, "oi big").split('"')[1], "oi big")

# --------------------------------------------------------------------------- the guard

print("\n── the guard " + "─" * 84)

# The committed order passes, which is the acceptance criterion: a guard that fails on the real data is
# not a guard, it is an outage.
true("the real order is accepted", osicons.check(osicons.LABELS) is None)
true("...as a tuple too, because data.json's column arrives as whatever json gave",
     osicons.check(tuple(osicons.LABELS)) is None)

swapped = copy.copy(osicons.LABELS)
swapped[0], swapped[4] = swapped[4], swapped[0]
msg = raises("a reordered column is refused", SystemExit, lambda: osicons.check(swapped))
says("...and the message shows the order the marks were drawn for", msg, "Windows")
says("...and the order the caller had", msg, str(swapped))
says("...and says why a wrong pairing is not survivable", msg, "position")
says("...and names every list that has to move together", msg, "SHAPES")

renamed = copy.copy(osicons.LABELS)
renamed[2] = "Mac OS"
raises("a renamed platform is refused", SystemExit, lambda: osicons.check(renamed))
raises("a dropped platform is refused", SystemExit, lambda: osicons.check(osicons.LABELS[:4]))
raises("a sixth platform is refused", SystemExit,
       lambda: osicons.check(osicons.LABELS + ["Android"]))
raises("an empty column is refused", SystemExit, lambda: osicons.check([]))
# Case is not a detail here: `.lower()` somewhere upstream would pair every mark correctly and print
# every word wrong, and this file would rather that failed loudly at build time.
raises("a case change is refused", SystemExit,
       lambda: osicons.check([s.lower() for s in osicons.LABELS]))

# --------------------------------------------------------------------------- the wiring

print("\n── the wiring " + "─" * 83)

GENERATORS = {
    "19_pages.py": "the index",
    "20_landing.py": "the 156 facet pages",
    "22_detail.py": "the 1,294 detail pages",
    "25_collections.py": "the curated collections",
}
for f, what in GENERATORS.items():
    src = (SCRIPTS / f).read_text(encoding="utf-8")
    says(f"{what} imports the marks rather than redrawing them", src, "import osicons")
    says(f"{what} refuses to publish a mark beside the wrong platform", src, "osicons.check(")
    says(f"{what} emits the sprite the marks resolve against", src, "osicons.SPRITE")

for f, css in (("20_landing.py", "docs/pages.css"), ("22_detail.py", "docs/repo/detail.css")):
    src = (SCRIPTS / f).read_text(encoding="utf-8")
    says(f"{f} puts the shared rule in {css}", src, "osicons.CSS")
index_src = (SCRIPTS / "19_pages.py").read_text(encoding="utf-8")
says("the index carries the shared rule in its inline stylesheet", index_src, "osicons.CSS")
says("...and takes the symbol ids into its client script from the module", index_src, "osicons.JS_IDS")
# The words are what a reader types to find a platform in the command palette, and what an exported
# Markdown table has instead of a stylesheet. Both must stay textual; see osicons.py's docstring.
says("the index's Markdown export still writes the words", index_src, "function osText")
true("...and no mark reaches it",
     "osIcon" not in index_src.split("function osText")[1].split("\n}")[0],
     "osText() is exported to a document that has no sprite in it")

# `detail.css` sits under `docs/repo/` beside the pages it serves rather than beside `pages.css` at the
# root -- see 22_detail.py's docstring on two stages writing one filename.
for css, where in (("pages.css", "the facet pages and the collections"),
                   ("repo/detail.css", "the detail pages")):
    text = (DOCS / css).read_text(encoding="utf-8")
    says(f"{css} carries the mark rule for {where}", text, ".oi{")
    says(f"{css} lets the verdict's colour through", text, "fill:currentColor")

# --------------------------------------------------------------------------- the resolution

print("\n── the resolution, over every built page " + "─" * 56)

USE = re.compile(r'<use[^>]+href="#(oi-[a-z0-9-]+)"')
SYM = re.compile(r'<symbol id="(oi-[a-z0-9-]+)"')
pages = sorted(DOCS.rglob("index.html"))
true("there are pages to check", len(pages) > 1400, f"{len(pages)} index.html under docs/")

dangling, spriteless, marked, doubled, unused = [], [], 0, [], []
for p in pages:
    text = p.read_text(encoding="utf-8", errors="replace")
    uses, syms = set(USE.findall(text)), SYM.findall(text)
    if len(syms) != len(set(syms)):
        doubled.append(p.relative_to(ROOT).as_posix())
    if uses:
        marked += 1
        missing = uses - set(syms)
        if missing:
            dangling.append((p.relative_to(ROOT).as_posix(), sorted(missing)))
        if not syms:
            spriteless.append(p.relative_to(ROOT).as_posix())
    elif syms:
        unused.append(p.relative_to(ROOT).as_posix())

true("marks were published at all", marked > 1400, f"{marked} of {len(pages)} pages draw a mark")
# The assertion this file exists for.
eq("every mark on every page resolves to a symbol in that same page", dangling[:6], [])
eq("...so no page draws a mark it has no sprite for", spriteless[:6], [])
eq("no page defines the same symbol twice", doubled[:6], [])
# And the other direction, which is 1.4 KB of dead weight per page rather than a wrong answer -- but named
# exactly rather than tolerated as a count, because the one legitimate case is a specific page for a
# specific reason. `docs/index.html` builds its rows and chips in the browser, so its sprite is referenced
# only after the script runs. Every other page either draws a mark or must not carry the sprite: the
# collections hub does not (it lists collections, not projects) and a detail page with the platform table
# switched off does not, which is 1.8 MB of path data the flag is there to avoid committing.
eq("the only page carrying a sprite it does not statically draw from is the client-rendered index",
   unused, ["docs/index.html"])

# Every id the pages reference is one this module actually declares -- the reverse direction, which
# catches a hand-typed `#oi-mac` where `#oi-macos` was meant on a page that happens to define both.
referenced = set()
for p in pages:
    referenced |= set(USE.findall(p.read_text(encoding="utf-8", errors="replace")))
eq("the pages reference no id this module does not draw", sorted(referenced - set(osicons.IDS)), [])
eq("...and draw every one it does", sorted(set(osicons.IDS) - referenced), [])

# --------------------------------------------------------------------------- the names

print("\n── the names " + "─" * 84)

INDEX = DOCS / "index.html"
# The three PRERENDERED families. The index is the fourth surface and is deliberately not in this dict:
# it builds its table and its five filter chips in the browser, so `osIcon()` assembles `href="#" + OSI[k]`
# at runtime and the committed document contains the sprite and no `<use>` at all. A static walk over it
# would find nothing and, worse, would report that as everything being fine. Its marks are checked below
# by reading the script that makes them, and `tests/probe.mjs` -- which runs that script against a stub DOM
# -- is the instrument that sees the chips a reader gets.
FAMILY = {
    "a facet page": DOCS / "topic" / "agent-skills" / "index.html",
    "a detail page": DOCS / "repo" / "ollama" / "ollama" / "index.html",
    "a collection": DOCS / "collections" / "first-setup" / "index.html",
}

# An ancestor walk rather than a pattern, because the three surfaces do not agree on the markup and should
# not have to. The detail table names each mark in a `title` on the span beside the word; the collections
# name it in a `title` and again in a visually-hidden span; the facet rows name all five once on the row's
# container, with `role="img"`, because 500 marks a page cannot each afford their own name. A regex written
# for one of those shapes matches nothing on the other two -- and matching nothing is how this group
# passes while asserting anything, which is the failure `tests/run.mjs`'s floor exists to catch.
#
# So: for every mark, find the nearest ancestor that names *a* platform -- in a `title`, in an `aria-label`,
# or in its own text, which is what a visually-hidden word contributes -- and require that it names *this*
# one. That last clause is the part no other test in the suite can make: `osicons.check()` validates the
# label list a generator is about to iterate, and cannot see what the generator then emitted, so a loop
# that paired mark `k` with verdict `k+1` would pass it and publish a Docker whale over the Windows answer.
# Here the name and the symbol id are compared in the built page, which is the only place they meet.
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source",
        "track", "wbr"}
# Four is past every wrapper any of these generators puts between a mark and its name (two is the most any
# of them uses) and stops short of the page, whose text contains all five words in the legend -- a walk
# that reached `<body>` would report every document as fully named, including one that named nothing.
REACH = 4


class Marks(HTMLParser):
    """Every `<use href="#oi-...">` in a document, with the elements enclosing it."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[list] = []   # open elements, outermost first: [tag, attrs, text pieces]
        self.found: list[tuple[str, list[list]]] = []

    def handle_starttag(self, tag, attrs) -> None:
        a = {k: (v or "") for k, v in attrs}
        if tag == "use":
            href = a.get("href") or a.get("xlink:href") or ""
            if href.startswith("#oi-"):
                # The frames themselves, not copies: their text is still being collected, and a
                # visually-hidden word arrives after the mark it belongs to.
                self.found.append((href[1:], list(reversed(self.stack))[:REACH]))
            return
        if tag not in VOID:
            self.stack.append([tag, a, []])

    def handle_endtag(self, tag) -> None:
        # Generated markup is well formed, so the guard is for the tags this parser and the generator
        # disagree about -- a self-closing `<use/>` arrives here having never been pushed.
        if self.stack and self.stack[-1][0] == tag:
            frame = self.stack.pop()
            if self.stack:
                self.stack[-1][2].append("".join(frame[2]))

    def handle_startendtag(self, tag, attrs) -> None:
        self.handle_starttag(tag, attrs)

    def handle_data(self, data) -> None:
        if self.stack:
            self.stack[-1][2].append(data)


def names_in(frame: list) -> list[str]:
    """Which platforms this one element names, in a hover, in a label, or in its own text."""
    where = " ".join([frame[1].get("title", ""), frame[1].get("aria-label", ""), "".join(frame[2])])
    return [lab for lab in osicons.LABELS if lab in where]


for what, p in FAMILY.items():
    if not p.exists():
        bad += 1
        print(f"FAIL {what} is not built: {p.relative_to(ROOT)}")
        continue
    text = p.read_text(encoding="utf-8", errors="replace")
    eq(f"{what} carries exactly one sprite", len(SYM.findall(text)), 5 if USE.search(text) else 0)
    # Somewhere in the document, in text, for a search engine and for a reader who turns off images.
    for lab in osicons.LABELS:
        says(f"{what} still contains the word {lab} as text", text, lab)

    parser = Marks()
    parser.feed(text)
    # Counted, and required to be all five, so this cannot report success over an empty list. A page in
    # one of these families that stopped drawing marks is a finding, not a reason to skip the group.
    drawn = {i for i, _ in parser.found}
    eq(f"{what} draws all five marks", sorted(drawn), sorted(osicons.IDS))
    unnamed, mispaired = [], []
    for sym, ancestors in parser.found:
        lab = osicons.LABELS[osicons.IDS.index(sym)]
        near = next((f for f in ancestors if names_in(f)), None)
        if near is None:
            unnamed.append(sym)
        # WSL2's hover text says "Windows Subsystem for Linux 2", so an element that names one platform
        # may legitimately mention two others. Membership is therefore the strongest form of this that
        # does not fail on the correct page: the name found beside a mark must include the mark's own.
        elif lab not in names_in(near):
            mispaired.append((sym, near[0], sorted(names_in(near))))
    eq(f"{what}: every mark has a platform name within {REACH} elements of it", unnamed[:6], [])
    eq(f"{what}: no mark sits inside a name for a different platform", mispaired[:6], [])

# The index, on its own terms. It ships the sprite and a function that references it, and the marks
# themselves do not exist until the script runs -- so what can be asserted here is that the pieces are
# present and that the words came with them. `tests/probe.mjs` runs the script and reads the chips it
# built; this only has to be sure the script cannot have been left half-wired.
index = INDEX.read_text(encoding="utf-8", errors="replace")
eq("the index carries the sprite its script will reference", len(SYM.findall(index)), 5)
eq("...and draws no mark in the document itself, because it has no rows until it fetches them",
   USE.findall(index), [])
# `OSI` is `osicons.JS_IDS` and the ids are lowercase and hyphenated, so nothing about the marks puts the
# platform words into this document. `OST` is the only thing that does -- which is the whole reason the
# module exports it, and is why losing it would be a silent, total loss of the five names on the one page
# most readers see. The words are also what a reader types into the command palette to find a platform.
for k, lab in enumerate(osicons.LABELS):
    says(f"the index carries the word {lab} for its script to label a chip with", index, lab)
says("the index's five chips are built from the shared ids", index, osicons.JS_IDS)
says("...and named from the shared titles", index, osicons.JS_TITLES)
# The `href` is assembled at runtime, so the ids in the sprite and the ids the script asks for are the
# same thing only while the script reads them from `OSI` instead of spelling them a second time.
true("the marks are built from that array rather than a second copy of the ids",
     re.search(r'href="#\'\s*\+\s*OSI\[', index),
     "osIcon() spells an id itself, so the sprite and the reference can drift inside one document")
# Two things on this page are drawn as a mark, and each needs its word for a different reason. A filter
# chip's whole label is the picture, so without the word it is not a worse label -- it is an unlabelled
# button. A verdict in the table has a glyph beside it, so the word is what says which platform the glyph
# is answering for. Both are checked by locating the statement that builds the markup and requiring the
# hidden word inside it, rather than by matching the expression: the property is that the two are
# assembled together, and an assertion pinned to `a + b + c` goes red the day someone writes a template
# literal that does exactly the same thing. This one already did, which is why it reads this way now.
CHIP = re.search(r"if \(icon\)[^;]*;", index)
ROW = re.search(r"'<span class=\"sr\">'[^;]*;", index)
for what, m in (("a filter chip", CHIP), ("a verdict in the table", ROW)):
    if not m:
        bad += 1
        print(f"FAIL the index still builds {what} from a mark -- the statement that did is gone")
        continue
    says(f"{what} is a mark plus a visually-hidden word, not a mark alone", m.group(0), 'class="sr"')
    says(f"...and that word is the platform's own, escaped ({what})", m.group(0), "esc(")

# --------------------------------------------------------------------------- the surfaces

print("\n── the surfaces " + "─" * 81)

# The compact places: the three-letter words are what the marks replaced, and a page that still prints
# them is a page one of the four generators did not get to.
for what, p in (("a facet page", FAMILY["a facet page"]), ("a collection", FAMILY["a collection"])):
    if not p.exists():
        continue
    text = p.read_text(encoding="utf-8", errors="replace")
    for short in ("Win", "WSL", "mac", "Lin", "Doc"):
        eq(f"{what} no longer prints the truncated {short!r} as a verdict",
           re.findall(r'<span class="v[YLNa-]"[^>]*>\s*' + short + r'\b', text), [])

# The explanatory place. The detail page's platform table is the only surface whose job is to finish the
# sentence, and its row header is the accessible name for the whole row -- so there the mark goes beside
# the word and the word stays real text. A mark instead of it would be a loss dressed as a tidy-up.
detail = FAMILY["a detail page"]
if detail.exists():
    text = detail.read_text(encoding="utf-8", errors="replace")
    for lab in osicons.LABELS:
        true(f"the platform table still names {lab} in its row header",
             re.search(r'<th scope="row"[^>]*>(?:(?!</th>).)*?' + re.escape(lab), text, re.S),
             f"{lab} is not in any row header of docs/repo/ollama/ollama/index.html")

# Markdown keeps its words. GitHub strips `<svg>` from rendered Markdown, so a mark there is not a
# degraded label -- it is nothing at all.
md = sorted((ROOT / "mega-list").rglob("*.md"))
true("there is Markdown to check", len(md) > 10, f"{len(md)} files")
# The reference shapes, not the substring `oi-`: two of these files print an install command containing
# `coi-linux-amd64`, and a test that calls a project's own binary name a bug is a test that gets edited
# out. What GitHub actually strips is the element and the fragment reference, so those are what is looked
# for -- an inline sprite, a use of one, or a symbol id in a link.
STRIPPED = re.compile(r"<svg\b|<use\b|<symbol\b|#oi-")
offenders = [p.relative_to(ROOT).as_posix() for p in md
             if STRIPPED.search(p.read_text(encoding="utf-8", errors="replace"))]
eq("no Markdown file references a symbol GitHub will strip", offenders, [])

# --------------------------------------------------------------------------- the source

print("\n── the source " + "─" * 83)

SRC = (SCRIPTS / "osicons.py").read_text(encoding="utf-8")
doc = osicons.__doc__ or ""
says("the docstring says why the accessible name survives", doc, "accessible name")
says("...and that the pairing is positional", doc, "position")
says("...and why the sprite is inline rather than per-use", doc, "sprite")
says("...and that Markdown keeps the words", doc, "Markdown")
THIRD_PARTY = ("requests", "httpx", "openpyxl", "PIL", "yaml", "dateutil", "numpy")
eq("the module imports nothing at all beyond __future__",
   [m for m in THIRD_PARTY if f"import {m}" in SRC], [])
true("...and reads no file and takes no argument",
     "open(" not in SRC and "Path(" not in SRC,
     "geometry with an input is geometry that can differ between two callers")

print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
