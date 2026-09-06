"""Strip the comments out of a generated page, keeping every one of them in the source.

`docs/index.html` was 37,569 B gzipped and 22,381 of those bytes were commentary -- 46 CSS blocks, 299
JavaScript lines and 18 HTML blocks, about 55 KB of prose uncompressed. The Lighthouse budget for the
document is 40,960 B and was down to 8% of headroom, so the next feature would have turned that check red.

Raising the budget was the wrong answer. Nothing a reader interacts with has to shrink: the comments are
written for whoever is editing `scripts/19_pages.py`, and that is where they can be read, in order, with
`git blame` attached. They do not need to be downloaded 1,294 times by people looking at a table. So the
stage strips its own output on the way out and the template keeps everything.

WHAT IT WILL AND WILL NOT DO, WHICH IS THE ONE PROPERTY THIS MODULE IS BUILT AROUND

It only ever *deletes* bytes it has positively identified as a comment. Every other byte is copied
verbatim, and `strip_page` asserts that the result is a subsequence of its input, so nothing can be
reordered, rewritten or invented even if the scanner below is wrong about where a comment starts. That
turns the worst case from "the page is subtly broken" into "a comment survived and we paid for it" -- a
missed saving rather than a defect. Everything else here is in service of that.

It is a scanner, not a parser, and it is not a minifier. It does not rename anything, reorder anything,
collapse whitespace inside a line, or touch the markup's structure. A line that held nothing but a
comment goes away entirely; a line that held code keeps its indentation, because gzip charges almost
nothing for a repeated run of spaces and the diffs stay readable.

THE THREE LANGUAGES

A page is HTML with a `<style>` and some `<script>` in it, and the comment syntax is different in each --
so a single regex over the whole document is not merely fragile, it is wrong. `strip_page` walks the
markup and hands each embedded region to the scanner for its own language. A `<script>` whose `type` is
not JavaScript is left completely alone: JSON-LD has no comments to remove and a `/` heuristic has no
business anywhere near it.

WHY IT RUNS BEFORE SUBSTITUTION, NOT AFTER

`substitute()` calls this on the template, so the input is a constant and the output is a pure function of
the source file. Run afterwards, the input would change every day -- counts, dates, the analytics snippet
-- and a scanner bug could be triggered by data, which is the hardest kind of bug to reproduce. It also
means the beacon's own `<!-- Cloudflare Web Analytics -->` markers survive into the page, which is
deliberate: they are that vendor's snippet as given, and a marker naming the one third-party request on
the page is a courtesy to anyone reading view-source to find out what is phoning home.

THE REGEX-OR-DIVISION PROBLEM

In JavaScript `/` is either division or the start of a regex literal, and telling them apart needs the
previous token. The heuristic here is the usual one: a regex may follow an operator, an opening bracket,
a comma, a semicolon or one of the keywords in `_REGEX_OK_AFTER`, and a `/` after an identifier, a number
or a closing bracket is division. It is not exhaustive -- `if (x) /re/.test(s)` reads as division after
`)`, and an object literal's closing `}` is indistinguishable from a block's. Both of those mis-readings
are harmless *here* because of the subsequence property: a mis-identified regex is still copied out byte
for byte, and the only consequence is that a comment further along the same line may be kept. Nothing is
lost. That is why this is a heuristic in 40 lines instead of a JavaScript parser in 4,000.

`//` is never a regex, because an empty regex is spelled `/(?:)/` precisely so that `//` can be a comment,
and `/*` is never a regex either, because a pattern cannot open with a quantifier. So the comment checks
can safely come first.

ASI, WHICH IS THE ONE PLACE DELETING A COMMENT CAN CHANGE MEANING

A line terminator inside a block comment triggers automatic semicolon insertion just as a bare newline
would, so `return /* \n */ 5` returns undefined and `return 5` does not. A block comment that is removed
from the middle of a line therefore leaves a newline behind if it contained one, and a space if it did
not -- the space because `a/*x*/b` is two tokens and `ab` is one, in CSS as much as in JavaScript. A
comment that occupied whole lines can take its newline with it, because the newline that ended the
previous line is still there.
"""
from __future__ import annotations

import re

# A `/` here may open a regex. Anything else that can end an expression -- an identifier, a number, `)`,
# `]`, `}` -- means division. `of` and `in` are included for `for (const x of /re/.exec(s))`, which is
# contrived, but the cost of listing them is nothing and the cost of a missing one is a kept comment.
_REGEX_OK_AFTER = frozenset("""
return typeof instanceof in of new delete void throw case do else yield await
""".split())

# Punctuation after which a `/` opens a regex.
_REGEX_OK_PUNCT = frozenset("(,=:[!&|?{};+-*%~^<>")

# `<script>` bodies are only scanned when the type says JavaScript, or says nothing. `module` covers
# `type="module"`; the rest are the spellings the HTML spec still treats as a classic script.
_JS_TYPES = frozenset(["", "module", "text/javascript", "application/javascript",
                       "text/ecmascript", "application/ecmascript", "module/javascript"])

_TAG = re.compile(r"<(script|style)\b([^>]*)>", re.I)
_TYPE = re.compile(r"""\btype\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""", re.I)


class _Out:
    """An output buffer that holds a line's indentation back until it knows the line has content.

    That is the whole mechanism behind "a comment that owned a line takes the line with it". Ordinary
    characters go through `ch`, which can therefore drop the indentation retroactively; string, template
    and regex literals go through `raw`, which never touches whitespace, because whitespace inside a
    literal is data.
    """
    __slots__ = ("parts", "pend", "fresh")

    def __init__(self) -> None:
        self.parts: list[str] = []
        self.pend = ""      # horizontal whitespace seen since the last newline, not yet committed
        self.fresh = True   # nothing but whitespace on this line so far

    def ch(self, c: str) -> None:
        if c in " \t":
            if self.fresh:
                self.pend += c
            else:
                self.parts.append(c)
        elif c == "\n":
            if self.fresh:
                self.pend = ""
            self.parts.append("\n")
            self.fresh = True
        else:
            self._flush()
            self.parts.append(c)

    def raw(self, s: str) -> None:
        if s:
            self._flush()
            self.parts.append(s)

    def _flush(self) -> None:
        if self.pend:
            self.parts.append(self.pend)
            self.pend = ""
        self.fresh = False

    def rtrim(self) -> None:
        """Drop trailing spaces and tabs, for the run left behind by `code(); // note`.

        It cannot reach back into a template literal's whitespace, which would be data. Only `_drop` calls
        this, `_drop` is only reached from a comment, and a comment is only recognised in normal state --
        and the only way from a template's text into normal state is through a `${`, which is not
        whitespace and stops the walk. The same holds for a nested template, whose closing backtick shields
        its own trailing spaces.
        """
        if self.fresh:
            self.pend = self.pend.rstrip(" \t")
            return
        while self.parts and self.parts[-1] and self.parts[-1][-1] in " \t":
            self.parts[-1] = self.parts[-1].rstrip(" \t")
            if not self.parts[-1]:
                self.parts.pop()

    def text(self) -> str:
        return "".join(self.parts) + self.pend


def _drop(out: _Out, src: str, start: int, end: int, sep: str) -> int:
    """Delete `src[start:end]`, and the line around it when the comment was the only thing on it.

    Returns the index to continue from. `sep` is what a mid-line deletion leaves behind so that the
    tokens either side of the comment stay two tokens -- a newline when the comment spanned lines, a
    space otherwise.
    """
    owned_start = out.fresh
    rest = end
    while rest < len(src) and src[rest] in " \t":
        rest += 1
    owned_end = rest >= len(src) or src[rest] == "\n"

    if owned_start and owned_end:
        out.pend = ""
        return rest + 1 if rest < len(src) else rest
    if owned_end:                     # `code(); // note` -- the trailing run goes with it
        out.rtrim()
        return rest
    out.raw(sep)
    return end


def strip_js(src: str) -> str:
    """Remove `//` and `/* */` comments from JavaScript, leaving strings, templates and regexes alone."""
    out = _Out()
    i, n = 0, len(src)
    stack: list = []    # "tmpl" inside a template literal's text; ["sub", depth] inside its `${ }`
    prev = ""           # last significant character emitted, for the regex test
    word = ""           # the identifier run ending at `prev`

    while i < n:
        # Inside a template literal every byte is data until the closing backtick or a `${`.
        if stack and stack[-1] == "tmpl":
            c = src[i]
            if c == "\\":
                out.raw(src[i:i + 2]); i += 2; continue
            if c == "`":
                stack.pop(); out.raw(c); i += 1; prev, word = "`", ""; continue
            if src.startswith("${", i):
                stack.append(["sub", 0]); out.raw("${"); i += 2; prev, word = "{", ""; continue
            out.raw(c); i += 1; continue

        c, two = src[i], src[i:i + 2]

        if two == "//":
            j = src.find("\n", i)
            i = _drop(out, src, i, n if j < 0 else j, " ")
            continue
        if two == "/*":
            j = src.find("*/", i + 2)
            j = n if j < 0 else j + 2
            i = _drop(out, src, i, j, "\n" if "\n" in src[i:j] else " ")
            continue
        if c in "\"'":
            j = i + 1
            while j < n:
                if src[j] == "\\":
                    j += 2
                elif src[j] == c:
                    j += 1
                    break
                elif src[j] == "\n":    # unterminated: a syntax error already, so stop rather than run on
                    break
                else:
                    j += 1
            out.raw(src[i:j]); i = j; prev, word = c, ""
            continue
        if c == "`":
            stack.append("tmpl"); out.raw(c); i += 1; prev, word = "`", ""
            continue
        if c == "/" and (not prev or prev in _REGEX_OK_PUNCT or word in _REGEX_OK_AFTER):
            j, klass = i + 1, False
            while j < n:
                d = src[j]
                if d == "\\":
                    j += 2; continue
                if d == "[":
                    klass = True
                elif d == "]":
                    klass = False
                elif d == "/" and not klass:
                    j += 1
                    break
                elif d == "\n":         # not a regex after all; the copy below is still exact
                    break
                j += 1
            while j < n and (src[j].isalpha() or src[j] == "_"):
                j += 1
            out.raw(src[i:j]); i = j; prev, word = "/", ""
            continue

        # A `}` at depth zero inside `${ }` returns to the template's text.
        if stack and isinstance(stack[-1], list):
            if c == "{":
                stack[-1][1] += 1
            elif c == "}":
                if stack[-1][1] == 0:
                    stack.pop(); out.ch(c); i += 1; prev, word = "}", ""
                    continue
                stack[-1][1] -= 1

        out.ch(c)
        i += 1
        if not c.isspace():
            prev = c
            word = word + c if (c.isalnum() or c in "_$") else ""
    return out.text()


def strip_css(src: str) -> str:
    """Remove `/* */` from CSS. Strings are respected so that `content:"/*"` survives."""
    out = _Out()
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        if src.startswith("/*", i):
            j = src.find("*/", i + 2)
            j = n if j < 0 else j + 2
            i = _drop(out, src, i, j, "\n" if "\n" in src[i:j] else " ")
            continue
        if c in "\"'":
            j = i + 1
            while j < n:
                if src[j] == "\\":
                    j += 2
                elif src[j] == c:
                    j += 1
                    break
                elif src[j] == "\n":
                    break
                else:
                    j += 1
            out.raw(src[i:j]); i = j
            continue
        out.ch(c)
        i += 1
    return out.text()


def strip_html(src: str) -> str:
    """Remove `<!-- -->` from markup. Only called on the regions outside `<script>` and `<style>`."""
    out = _Out()
    i, n = 0, len(src)
    while i < n:
        if src.startswith("<!--", i):
            j = src.find("-->", i + 4)
            j = n if j < 0 else j + 3
            i = _drop(out, src, i, j, "")
            continue
        out.ch(src[i])
        i += 1
    return out.text()


def _subsequence(small: str, big: str) -> bool:
    it = iter(big)
    return all(c in it for c in small)


def strip_page(page: str) -> str:
    """Strip comments from a whole HTML document, one language at a time.

    Asserts on the way out that it only deleted -- see the module docstring. The check is a linear walk
    over 100 KB and it runs once per build, so its cost is not worth an argument.
    """
    out, i, n = [], 0, len(page)
    while i < n:
        m = _TAG.search(page, i)
        if not m:
            out.append(strip_html(page[i:]))
            break
        out.append(strip_html(page[i:m.start()]))
        out.append(m.group(0))

        kind = m.group(1).lower()
        close = f"</{kind}>"
        end = page.lower().find(close, m.end())
        if end < 0:                          # unclosed: copy the remainder and stop guessing
            out.append(page[m.end():])
            break
        body = page[m.end():end]
        if kind == "style":
            out.append(strip_css(body))
        else:
            t = _TYPE.search(m.group(2) or "")
            declared = (next((g for g in t.groups() if g is not None), "") if t else "").strip().lower()
            out.append(strip_js(body) if declared in _JS_TYPES else body)
        out.append(page[end:end + len(close)])
        i = end + len(close)

    stripped = "".join(out)
    assert _subsequence(stripped, page), "pagemin rewrote bytes instead of only deleting them"
    before, after = set(re.findall(r"__[A-Z_]+__", page)), set(re.findall(r"__[A-Z_]+__", stripped))
    assert before == after, f"pagemin lost placeholders: {sorted(before - after)}"
    return stripped
