"""Unit tests for `scripts/pagemin.py`, concentrating on what the real page cannot test.

The template exercises the easy 90%: 296 whole-line `//` comments, 46 CSS blocks, 16 HTML blocks, and two
`//` inside string literals. It exercises **none** of the interesting cases, because the page's JavaScript
contains no template literals at all -- all 258 backticks in it turned out to be inline code in prose
comments -- and no block comments. So the paths most likely to be wrong are the ones with no coverage from
the thing the module was written for. Hence this file.

Run: python build-tmp/pagemin_test.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import pagemin  # noqa: E402

ok = bad = 0


def eq(name: str, got: str, want: str) -> None:
    global ok, bad
    if got == want:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}\n  got  {got!r}\n  want {want!r}")


def js(name: str, src: str, want: str) -> None:
    eq(name, pagemin.strip_js(src), want)


# ---- template literals: every byte is data, including whitespace and comment-shaped text
js("a `//` inside a template survives",
   "x = `see https://a.example/b`;", "x = `see https://a.example/b`;")
js("so does a `/*` inside a template",
   "x = `a /* not a comment */ b`;", "x = `a /* not a comment */ b`;")
js("a template's own indentation is data, not indentation",
   "x = `a\n    b\n`;", "x = `a\n    b\n`;")
js("a blank line inside a template is data",
   "x = `a\n\nb`;", "x = `a\n\nb`;")
# The space after `v` goes with the comment, as it would anywhere else in the expression -- a `${ }`
# substitution is ordinary JavaScript and its whitespace is not data. See `_Out.rtrim` for why that trim
# can never reach backwards into the template's text.
js("a comment inside ${} is still a comment",
   "x = `a${ v // note\n }b`;", "x = `a${ v\n }b`;")
js("a string inside ${} keeps its slashes",
   'x = `a${ "//" }b`;', 'x = `a${ "//" }b`;')
js("a nested template inside ${} keeps its slashes",
   "x = `a${ `//${w}//` }b`;", "x = `a${ `//${w}//` }b`;")
js("braces inside ${} do not end the substitution early",
   "x = `a${ f({k: 1}) }b`; // gone", "x = `a${ f({k: 1}) }b`;")
js("an escaped backtick does not end the template",
   "x = `a\\`b`; // gone", "x = `a\\`b`;")

# ---- regex literals
js("a regex containing an escaped slash",
   "r = /https?:\\/\\//; // gone", "r = /https?:\\/\\//;")
js("a regex containing a star",
   "r = /a\\/*b/g; // gone", "r = /a\\/*b/g;")
js("a slash inside a character class is not the terminator",
   "r = /[/*]/; // gone", "r = /[/*]/;")
js("a regex as a call argument", "f(/a\\/b/, 1); // gone", "f(/a\\/b/, 1);")
js("a regex after return", "return /a\\/b/.test(s); // gone", "return /a\\/b/.test(s);")
js("a regex after a comma in an array", "[1, /a\\/b/]; // gone", "[1, /a\\/b/];")
js("division is not a regex", "q = a / b / c; // gone", "q = a / b / c;")
js("division by a number then a comment", "q = n / 2; // gone", "q = n / 2;")

# ---- strings
js("a URL in a double-quoted string", 'u = "https://a.example/"; // gone', 'u = "https://a.example/";')
js("a URL in a single-quoted string", "u = 'https://a.example/'; // gone", "u = 'https://a.example/';")
js("a block-comment opener in a string", 'u = "a /* b"; // gone', 'u = "a /* b";')
js("an escaped quote does not end the string", 'u = "a\\"//b"; // gone', 'u = "a\\"//b";')

# ---- line comments and the lines they live on
js("a comment that owns its line takes the line", "a;\n  // note\nb;", "a;\nb;")
js("a comment at column zero takes its line", "a;\n// note\nb;", "a;\nb;")
js("consecutive comment lines all go", "a;\n// one\n// two\n// three\nb;", "a;\nb;")
js("a trailing comment leaves no trailing space", "a; // note\nb;", "a;\nb;")
js("a comment with no newline after it", "a; // note", "a;")
js("code keeps its indentation", "if (x) {\n    a;  // note\n}", "if (x) {\n    a;\n}")

# ---- block comments: what is left behind matters
js("a block comment between two tokens leaves a space", "a/*x*/b", "a b")
js("a block comment spanning lines leaves a newline, so ASI is unchanged",
   "return/*x\ny*/5", "return\n5")
js("a block comment owning whole lines takes them", "a;\n  /* x\n     y */\nb;", "a;\nb;")
js("an unterminated block comment eats the rest", "a;\n/* x", "a;\n")

# ---- CSS
eq("a CSS comment owning its line takes the line",
   pagemin.strip_css("a{b:c}\n  /* note */\nd{e:f}"), "a{b:c}\nd{e:f}")
eq("a CSS comment between declarations leaves a separator",
   pagemin.strip_css("a{b:c/*x*/d:e}"), "a{b:c d:e}")
eq("content:\"/*\" is a string, not a comment",
   pagemin.strip_css('a::before{content:"/*"}/* gone */'), 'a::before{content:"/*"}')
eq("a URL with slashes is untouched",
   pagemin.strip_css("a{background:url(https://x.example/y.png)}/* gone */"),
   "a{background:url(https://x.example/y.png)}")

# ---- HTML
eq("an HTML comment owning its line takes the line",
   pagemin.strip_html("<p>a</p>\n  <!-- note -->\n<p>b</p>"), "<p>a</p>\n<p>b</p>")
eq("an inline HTML comment leaves the text adjacent, as it rendered before",
   pagemin.strip_html("<b>a</b><!-- x --><i>b</i>"), "<b>a</b><i>b</i>")
eq("a multi-line HTML comment goes entirely",
   pagemin.strip_html("<p>a</p>\n<!-- one\n     two -->\n<p>b</p>"), "<p>a</p>\n<p>b</p>")

# ---- whole documents
DOC = """<!doctype html>
<!-- a note -->
<style>
/* a rule */
a{b:c}
</style>
<script>
// a line
x = "https://a.example/";
</script>
<script type="application/ld+json">
{"a": "b // not a comment"}
</script>
<p>__COUNT__</p>
"""
eq("a whole document, one language at a time", pagemin.strip_page(DOC),
   '<!doctype html>\n<style>\na{b:c}\n</style>\n<script>\nx = "https://a.example/";\n</script>\n'
   '<script type="application/ld+json">\n{"a": "b // not a comment"}\n</script>\n<p>__COUNT__</p>\n')

eq("stripping is idempotent", pagemin.strip_page(pagemin.strip_page(DOC)), pagemin.strip_page(DOC))

# A `<script>` whose type is not JavaScript is copied byte for byte -- asserted above inside the document
# case, and separately here because it is the one region the scanner must refuse to touch.
eq("JSON-LD is not scanned at all",
   pagemin.strip_page('<script type="application/ld+json">{"u":"//x"}\n// literal\n</script>'),
   '<script type="application/ld+json">{"u":"//x"}\n// literal\n</script>')
eq("type=module is scanned",
   pagemin.strip_page('<script type="module">a; // gone\n</script>'),
   '<script type="module">a;\n</script>')

# ---- the invariants strip_page asserts, checked from outside as well
PAGE = (Path(__file__).resolve().parent / "page-raw.html")
if PAGE.exists():
    page = PAGE.read_text(encoding="utf-8")
    out = pagemin.strip_page(page)
    eq("the real template is idempotent under stripping", pagemin.strip_page(out), out)
    ok += 1 if len(out) < len(page) else 0
    if len(out) >= len(page):
        bad += 1
        print("FAIL the real template did not get smaller")
    # The nine URLs are the whole point: these are the `//` the stripper must not mistake for a comment.
    for u in ('https://opengraph.githubassets.com', "http://www.w3.org/2000/svg",
              '"https://opengraph.githubassets.com/1/"', "file://"):
        if u in out:
            ok += 1
        else:
            bad += 1
            print(f"FAIL the URL {u!r} was eaten")
    n = out.count("//")
    if n == 9:
        ok += 1
    else:
        bad += 1
        print(f"FAIL expected 9 surviving '//' in the template, found {n}")
else:
    print("note: build-tmp/page-raw.html absent, skipped the checks against the real template")

print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
