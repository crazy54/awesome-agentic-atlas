"""The manifest, the icons and the service worker that make the atlas installable and readable offline.

  docs/manifest.webmanifest       what a browser reads to decide the site is an app
  docs/icon-192.png               the two sizes every installer asks for
  docs/icon-512.png
  docs/icon-maskable-512.png      the same mark inside Android's safe circle, full bleed
  docs/apple-touch-icon.png       iOS ignores the manifest's icons and reads this link instead
  docs/sw.js                      the cache policy, with a version stamped from the shell it caches

  python scripts/24_pwa.py        after 19_pages.py, which writes the shell this hashes
  python scripts/24_pwa.py --kill writes a tombstone worker instead; see "Un-shipping" below

Generated rather than hand-written for one reason: the service worker's version has to be a fact about
the files it caches. A hand-maintained `const VERSION = "v3"` is bumped by whoever remembers, and the
first time someone forgets, every returning reader keeps a shell that no longer matches the data it
fetches -- with no symptom on the machine of the person who shipped it, because their browser installed
the worker before the mistake existed. Here the version is a hash of the precached bytes, so it moves
when and only when they do, and it cannot be forgotten.

WHY THE CACHING POLICY IS NOT THE ONE THE TICKET ASKED FOR

JFH-197 proposes stale-while-revalidate for `data.json`. That is the wrong policy for this dataset and
the page says so out loud: the header carries a snapshot date and turns the age amber past a fortnight,
and `data.json` is rebuilt daily with new star counts and new push dates. Serving yesterday's body
while today's downloads in the background means the page renders yesterday's numbers under today's
stamp -- not "slightly stale data", but a freshness claim that is false, which is worse than a slow
load and much worse than an honest failure. So the data is network-first: the network wins whenever it
answers, and the cache is a fallback for when it does not answer at all.

This used to lean on an ordering argument: within any visit the navigation is fetched before the page's own
`fetch("data.json")`, so a cached shell is never newer than the cached data it is paired with. The hole in
it was stated here and then filed as JFH-207 -- a visit whose navigation succeeded and whose data request
did not leaves a shell newer than the cached body, and the two caches are separately evictable besides, so
the pair a reader gets offline is not necessarily a pair that was ever deployed together. The stamp then
described the document rather than the rows underneath it, and said nothing about it.

The ordering is no longer what makes it safe. `data.json` carries its own `generated` timestamp and the
banner reads that, so the stamp travels with the rows it describes and no pairing of the two caches can
make it wrong. `data()` below also marks a response it answered out of the cache, with the header the page
renders as "offline, showing data from <date>" -- so a reader is told which day they are looking at, and
why, instead of being shown a date that came from somewhere else.

WHAT IS AND IS NOT PRECACHED

Precached at install, ~66 KB: the root shell, the manifest and `pages.css`. Everything the page needs to
paint is inside `index.html` already -- the CSS and all of the JavaScript are inline, by a decision
`19_pages.py` explains -- so the entire render path is one file. `pages.css` is not needed by the root at
all; it is the 8 KB stylesheet the 156 prerendered facet pages share, and it is precached so that a facet
page kept in the runtime cache renders as itself rather than as unstyled markup.

Not precached, deliberately:

  * The icons, 50 KB of the 116 KB this stage writes. They are read by an installer and by the OS, both
    of which keep their own copy of what they took, and the page's own favicon is an inline SVG data URI
    -- so nothing on any render path, online or offline, ever requests them. Precaching them would be
    50 KB of someone's data plan spent on a request that is not going to be made.

  * The 156 facet pages under `docs/topic/**` and `docs/target/**`, ~6 MB. Precaching them would spend
    six megabytes of someone's data plan on 155 pages they did not ask for, and they carry star counts
    and a snapshot line of their own, so a stale copy has the same freshness problem the data has. They
    are cached as they are visited instead, capped, and served from cache only when the network fails.

  * `data.json`, 552 KB. Not because it should not be available offline -- it must be, or "works
    offline" is a lie -- but because the page downloads it on the first visit anyway. Precaching it at
    install would download it a second time in the same visit for nothing. The worker stores the page's
    own response instead, so the offline copy costs zero extra bytes.

  * The 7,980 screenshots. They are Open Graph cards on `opengraph.githubassets.com`, cross-origin and
    fetched no-cors, so a response is opaque: status 0, no readable headers. A worker cannot tell a real
    card from GitHub's grey placeholder or from a 404, so it would cache failures indistinguishably from
    successes and keep them; browsers also pad opaque entries when charging them against the origin's
    storage quota, so a few hundred cards can evict the shell they were meant to sit next to. Both
    reasons point the same way: the worker does not touch cross-origin requests at all, and the HTTP
    cache handles the cards exactly as well as it does today. Offline, rows show their alt text -- which
    is empty, because the card is decorative and the row's title is the link.

  * `feed.xml`, `feed.json`, `sitemap.xml`, `robots.txt`. Machine surfaces. A feed reader and a crawler
    have their own caches and their own conditional requests, and neither runs inside this worker's
    scope in the first place.

THE PATH PREFIX, WHICH IS WHERE THIS KIND OF WORK USUALLY DIES

The atlas is a *project* Pages site: everything lives under `/awesome-agentic-atlas/`, not at the root
of `crazy54.github.io`. Every path in the manifest and in the worker is therefore relative, and nothing
below ever writes a leading slash. `start_url` and `scope` resolve against the manifest's own URL, and
the worker's `ROOT` resolves against `self.location`, so all three land on the prefix by construction --
on the published site, on a fork under a different name, and on a local `python -m http.server` serving
`docs/` at the root, which is the case that a hardcoded `/awesome-agentic-atlas/` would break. `main()`
asserts the resolution against `17_markdown.SITE` rather than trusting it, because a leading slash here
is silent: the worker would register with a scope of `/`, control nothing under the prefix, and appear
to work in every way except the one that matters.

UN-SHIPPING

A service worker outlives the deploy that shipped it: a reader who has one keeps it until it updates
itself, and deleting `sw.js` from the site does not remove it -- it leaves the last good copy installed
and its 404 is not treated as an uninstall. So the retreat is a file, not a deletion:

  python scripts/24_pwa.py --kill

writes a worker whose only behaviour is to delete this project's caches, call `registration.unregister()`
and reload its open tabs, and which registers no fetch handler at all. Commit that, and every reader
who visits is cleanly rid of it. Then, and only then, is dropping the registration from the page safe.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import struct
import sys
import zlib
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUT = ROOT / "docs"

sys.path.insert(0, str(HERE))

# 17_markdown owns the canonical site URL and every other surface asks it rather than keeping a copy, so
# this stage asks too -- here it is not decoration but the thing the prefix assertion in `main()` checks
# the relative paths against.
spec = importlib.util.spec_from_file_location("b17", HERE / "17_markdown.py")
b17 = importlib.util.module_from_spec(spec)
sys.modules["b17"] = b17
spec.loader.exec_module(b17)

SITE = b17.SITE

# And 19_pages owns the page, so the one string the worker and the page have to agree on -- the header that
# says a response came out of the cache -- is asked for here rather than spelled out again below. A copy
# would be silent when it drifted: the banner would simply stop mentioning the cache, which reads as the
# network having been up. This import is free, in that `19_pages` reads nothing at import time and its own
# `17_markdown` is the module already loaded above.
spec = importlib.util.spec_from_file_location("b19", HERE / "19_pages.py")
b19 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b19)

NAME = "Awesome Agentic Atlas"
# Twelve characters, because a home-screen label is truncated past about that and Android shows
# `short_name` under the icon. "Awesome Agentic Atlas" arrives there as "Awesome Age…".
SHORT_NAME = "Atlas"
# The list count is read off `b19.LISTS` -- i.e. off `SOURCES` -- rather than spelled out, because this
# string is shipped bytes in the installed app's manifest, and a manifest that still says "eleven" after
# the atlas has stopped being eleven lists is wrong on a reader's home screen until they reinstall.
DESCRIPTION = (f"Every agentic AI project from {b19.LISTS} awesome-lists, merged, deduplicated and "
               "filterable by topic, harness and operating system.")

# The theme's own dark surface. `background_color` is what a browser paints during the cold start of an
# installed window before the first frame, and `theme_color` tints the OS chrome around it; both are the
# dark value because dark is what the markup ships with and what a reader who has never touched the
# toggle sees. A reader who chose light gets one frame of the dark surface at launch, which is the same
# frame they already get on the web.
SURFACE = (0x10, 0x14, 0x16)
CYAN = (0x08, 0xB0, 0xCC)
GOLD = (0xFE, 0xB9, 0x32)

CACHE_PREFIX = "atlas-shell-"

# Cached pages other than the root, capped. Thirty is about a megabyte of prerendered facet pages, which
# is more than anyone browses in a sitting and small enough that no reader notices it in their storage.
PAGES_MAX = 30

# The precache list, in the order it is fetched. `./` rather than `index.html` because the request a
# navigation makes is for the directory -- a cache keyed by `index.html` is a cache that never answers
# the only request that matters.
PRECACHE = ["./", "manifest.webmanifest", "pages.css"]

ICONS = [
    # (filename, pixels, maskable, opaque)
    ("icon-192.png", 192, False, False),
    ("icon-512.png", 512, False, False),
    # Full bleed and inside the safe circle: Android crops a maskable icon to whatever shape the launcher
    # uses, and the guarantee is only that the middle 80% of the width survives. The same mark at the
    # "any" scale would lose its outer ring on a circular launcher.
    ("icon-maskable-512.png", 512, True, True),
    # iOS never reads the manifest's icons. It reads `<link rel="apple-touch-icon">`, it does not round
    # the corners of what it finds any more, and it composites onto black rather than honouring alpha --
    # so this one is opaque and square, and the plate's rounding is left to the OS.
    ("apple-touch-icon.png", 180, False, True),
]


# ------------------------------------------------------------------ icons
def _chunk(kind: bytes, body: bytes) -> bytes:
    return (struct.pack(">I", len(body)) + kind + body
            + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF))


def png(size: int, rows: list[bytearray]) -> bytes:
    """8-bit RGBA, one IDAT, filter 0 on every row.

    Written by hand because the whole pipeline is stdlib and adding Pillow for four flat-colour icons
    would be the first runtime dependency in the repo. Filter 0 rather than any of the four predictors
    costs nothing here -- the mark is large areas of three colours, which zlib flattens to a few KB
    either way -- and it keeps this to twenty lines that cannot be wrong in an interesting way.
    """
    ihdr = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    raw = b"".join(b"\x00" + bytes(r) for r in rows)
    return (b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", ihdr)
            + _chunk(b"IDAT", zlib.compress(raw, 9)) + _chunk(b"IEND", b""))


def _cover(d: float) -> float:
    """Signed distance in pixels to a 0..1 coverage, which is all the antialiasing an icon needs.

    One sample per pixel and the edge softened by its distance to it, rather than supersampling: every
    shape in the mark is a circle, an ellipse or a band, all of which have a distance function that is
    accurate to well under a pixel at these radii. Supersampling the same result would cost nine times
    the arithmetic in pure Python, on a stage that runs in every daily build.
    """
    return 0.0 if d >= 0.5 else 1.0 if d <= -0.5 else 0.5 - d


def _over(dst: list[float], rgb: tuple[int, int, int], a: float) -> None:
    if a <= 0.0:
        return
    out_a = a + dst[3] * (1.0 - a)
    for i in range(3):
        dst[i] = (rgb[i] * a + dst[i] * dst[3] * (1.0 - a)) / out_a if out_a else 0.0
    dst[3] = out_a


def icon(size: int, maskable: bool, opaque: bool) -> bytes:
    """The mark: a cyan globe inside a gold orbit, on the theme's near-black plate.

    A globe because the favicon is already one -- `19_pages.py` ships U+1F310 as an SVG data URI -- and an
    installed icon that does not match the tab is a different app as far as a reader is concerned. It is
    drawn from primitives rather than by rasterising that emoji because rendering text needs a font, and
    which font is on the build machine is not something a static-site pipeline should depend on: the same
    emoji is a flat blue disc on one platform and a shaded three-dimensional ball on another.

    Cyan and gold are the theme's two accents and the plate is its darkest surface, so the icon is
    recognisably the same object as the page. All geometry is a fraction of the icon's edge, so the four
    sizes are the same drawing rather than four drawings that drifted.
    """
    scale = 0.72 if maskable else 1.0
    r_globe = 0.30 * scale
    r_orbit = 0.385 * scale
    w_orbit = 0.032 * scale
    # Strokes as a fraction of the globe, not of the icon, so they stay the same drawing when the
    # maskable variant shrinks the globe inside the safe circle.
    w_grid = 0.115 * r_globe
    w_lat = 0.085 * r_globe
    y_lat = 0.46 * r_globe
    a_meridian = 0.50 * r_globe
    # Rounded like an app icon for the "any" purpose, square where the OS does its own cropping: Android
    # masks a maskable icon and iOS masks an apple-touch-icon, and rounding underneath either shows a
    # sliver of transparent corner inside the OS's own rounder shape.
    r_corner = 0.0 if (maskable or opaque) else 0.115

    rows: list[bytearray] = []
    for py in range(size):
        y = (py + 0.5) / size - 0.5
        row = bytearray()
        for px in range(size):
            x = (px + 0.5) / size - 0.5
            acc = [0.0, 0.0, 0.0, 0.0]

            # The plate. A rounded rectangle's distance is the distance to the inset box, which for a
            # square centred on the origin is this one expression.
            qx, qy = abs(x) - (0.5 - r_corner), abs(y) - (0.5 - r_corner)
            d_plate = (((max(qx, 0.0) ** 2 + max(qy, 0.0) ** 2) ** 0.5)
                       + min(max(qx, qy), 0.0) - r_corner)
            _over(acc, SURFACE, _cover(d_plate * size))

            r = (x * x + y * y) ** 0.5
            _over(acc, GOLD, _cover((abs(r - r_orbit) - w_orbit / 2) * size))

            globe = _cover((r - r_globe) * size)
            _over(acc, CYAN, globe)

            # The grid is painted in the plate's colour and clipped to the globe's coverage, so a
            # latitude stops at the limb instead of ruling a line across the orbit outside it.
            if globe > 0.0:
                grid = max(
                    _cover((abs(y) - w_grid / 2) * size),
                    _cover((abs(abs(y) - y_lat) - w_lat / 2) * size),
                    _cover((abs(x) - w_grid / 2) * size),
                    # The meridians are ellipse outlines. `f - 1` scaled by the semi-minor axis is the
                    # distance to within a fraction of a pixel near the equator, and thickens towards the
                    # poles -- where the globe's own edge has already clipped it.
                    _cover((abs(((x / a_meridian) ** 2 + (y / r_globe) ** 2) ** 0.5 - 1.0)
                            * a_meridian - w_grid / 2) * size),
                )
                _over(acc, SURFACE, min(grid, globe))

            a = 1.0 if opaque else acc[3]
            row += bytes((int(acc[0] + 0.5), int(acc[1] + 0.5), int(acc[2] + 0.5),
                          int(a * 255 + 0.5)))
        rows.append(row)
    return png(size, rows)


# ------------------------------------------------------------------ manifest
def manifest() -> dict:
    """The fields a browser needs to offer an install, and nothing it does not read.

    Chrome's bar is a manifest that parses, a `name` or `short_name`, a `start_url` in scope, a `display`
    that is not `browser`, an icon of at least 192px, and a service worker with a fetch handler. All six
    are here; the rest of this is what the install *looks* like rather than whether it is offered.

    `start_url` is `.` and `scope` is `./`, both relative, and that is the whole prefix story: they
    resolve against this file's own URL, which is `<prefix>/manifest.webmanifest`, so they become the
    prefix. `id` is deliberately absent -- it resolves against the *origin* rather than the manifest, so
    the relative form that is right for every other field would be wrong here, and omitting it makes the
    identity default to the resolved `start_url`, which is the same string on the site and on a fork.
    """
    return {
        "name": NAME,
        "short_name": SHORT_NAME,
        "description": DESCRIPTION,
        "start_url": ".",
        "scope": "./",
        "display": "standalone",
        # Only `standalone` is listed as a fallback chain because the page is a document, not a game or a
        # canvas: `fullscreen` would take away the reader's back button and `minimal-ui` is what a
        # browser already gives us if it declines `standalone`.
        "display_override": ["standalone", "browser"],
        "orientation": "any",
        "lang": "en",
        "dir": "ltr",
        "background_color": "#%02x%02x%02x" % SURFACE,
        "theme_color": "#%02x%02x%02x" % SURFACE,
        "categories": ["developer", "productivity", "utilities"],
        "icons": [
            {"src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png",
             "purpose": "maskable"},
        ],
    }


# ------------------------------------------------------------------ service worker
SW = r"""// Generated by scripts/24_pwa.py from the shell it caches. Editing this file by hand is how the
// version stops describing the bytes: the next build overwrites whatever was changed here, and until it
// does, readers hold a cache whose name no longer matches its contents. Change the generator.
//
// Version __VERSION__ -- a hash of the precached files, so it moves when they do and not otherwise.
const VERSION = "__VERSION__";
const SHELL = "__PREFIX__" + VERSION;
// Unversioned, and never deleted on activate, which is the difference between an offline reader and a
// broken one. A version-keyed data cache would be emptied by the very update that proves the reader is
// online, and if they closed the tab before the page's own fetch re-filled it, their next offline visit
// would have a shell and no rows.
const DATA = "atlas-data";
const PAGES = "atlas-pages";
const PAGES_MAX = __PAGES_MAX__;
// The one thing this worker tells the page in words: set on a `data.json` response that came out of DATA
// because the network did not answer. The page cannot work it out for itself -- what comes back out of that
// cache is byte-for-byte what went in -- and it is what turns "snapshot <date>" into "offline, showing data
// from <date>". The name is `CACHED_HEADER` in `19_pages.py`, which owns the page that reads it, and is
// substituted in here rather than written twice.
const CACHED = "__CACHEHDR__";

// Relative to this script, so the scope is the project's Pages prefix on the published site, the fork's
// prefix on a fork, and "/" under a local `python -m http.server`. A literal "/awesome-agentic-atlas/"
// here would be correct on exactly one of those three and silently inert on the others.
const ROOT = new URL("./", self.location.href).href;
const PRECACHE = __PRECACHE__.map((p) => new URL(p, self.location.href).href);
const PRECACHED = new Set(PRECACHE);

// The cache key for a request: its URL without the query string, and without the fragment the browser
// has already dropped. Nothing on this site reads a query string -- every piece of state the page keeps
// is in the hash, by a decision `19_pages.py` explains -- so a link arriving with a campaign parameter
// on it is the same document, and keying by the full URL would file a second copy of the shell under
// every tracker that ever links here.
function key(url) {
  const u = new URL(url);
  u.search = "";
  u.hash = "";
  return u.href;
}

self.addEventListener("install", (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(SHELL);
    // Deliberately NOT `cache: "reload"`. The reader is on the page these requests are for, so the HTTP
    // cache is holding the very bytes they just loaded and Pages says `max-age=600` over them: the
    // default cache mode fills this from that copy for nothing, while "reload" would charge every first
    // visit a second 72 KB download of a shell it already has, and charge it again on every update.
    //
    // What that costs is up to ten minutes of skew, and it is the right ten minutes. The page's own
    // `data.json` request is bounded by the same `max-age` on the same HTTP cache, so a shell taken from
    // it is paired with a body of the same age rather than with one from a different deploy -- and this
    // copy is only ever read when the network is gone, where the alternative is no page at all.
    await Promise.all(PRECACHE.map(async (url) => {
      const res = await fetch(url, {credentials: "same-origin"});
      // Throwing aborts the install, and an aborted install is the point: a half-filled version is
      // worse than no version at all, because it would activate, replace the version that worked, and
      // then miss whichever file failed for as long as the reader stays offline. Failing here leaves
      // the previous worker in charge and retries on the next navigation.
      if (!res.ok) throw new Error("precache " + url + " -> " + res.status);
      await cache.put(url, res);
    }));
    // Straight past `waiting`. It is safe here for a reason that is specific to this page rather than
    // generally true: the shell inlines all of its CSS and all of its JavaScript, so there is no pair of
    // hashed assets that can be mismatched by swapping worker mid-visit. The only thing an open page
    // fetches afterwards is `data.json`, which is network-first, so it cannot be answered out of a
    // version it did not come from. Waiting instead would leave a reader who never closes the tab on an
    // old worker indefinitely, which is exactly how a bad deploy becomes permanent.
    await self.skipWaiting();
  })());
});

self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    // Only this project's shell caches, and only the ones that are not the current version. The origin
    // is `<user>.github.io`, which every other Pages project of the same owner shares -- so a blanket
    // `caches.keys()` sweep here would delete a neighbouring site's storage.
    const names = await caches.keys();
    await Promise.all(names
      .filter((n) => n.startsWith("__PREFIX__") && n !== SHELL)
      .map((n) => caches.delete(n)));

    // Navigation preload lets the browser start the document request while this worker is still booting.
    // Without it, network-first navigations pay worker start-up before the request even leaves -- around
    // a hundred milliseconds on a cold mobile process, spent to arrive at the same response.
    if (self.registration.navigationPreload) {
      await self.registration.navigationPreload.enable();
    }
    // So the first visit is controlled by the worker it just installed rather than the one after it.
    await self.clients.claim();
  })());
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  // A worker that declines to call respondWith is a worker that is not in the way: the browser makes the
  // request exactly as it would with no worker registered. Everything this does not have a real policy
  // for takes that path, rather than a "pass through" branch that re-implements the browser badly.
  if (req.method !== "GET") return;
  // Range requests cannot be satisfied from a whole cached body, and a 206 cannot be cached.
  if (req.headers.has("range")) return;

  const url = new URL(req.url);
  // The Open Graph cards, the analytics beacon, every outbound link. Cross-origin and mostly opaque:
  // nothing here can inspect them, so nothing here should hold them.
  if (url.origin !== self.location.origin) return;
  // A project Pages site shares its origin with every other project of the same owner. The scope
  // already limits which pages this worker controls, but a controlled page can request a URL outside it.
  if (!key(url.href).startsWith(ROOT)) return;
  // The browser updates this file by fetching it; answering that request from here is how a worker
  // makes itself immortal.
  if (url.pathname.endsWith("/sw.js")) return;

  if (req.mode === "navigate") {
    event.respondWith(navigation(event));
  } else if (url.pathname.endsWith("/data.json")) {
    event.respondWith(data(req));
  } else if (PRECACHED.has(key(url.href))) {
    event.respondWith(asset(req));
  }
});

async function navigation(event) {
  const k = key(event.request.url);
  const cache = await caches.open(k === ROOT ? SHELL : PAGES);
  try {
    // `preloadResponse` is the request the browser already started for us where navigation preload is
    // supported, and `undefined` where it is not; either way exactly one request goes out.
    const pre = await event.preloadResponse;
    const res = pre || await fetch(event.request);
    // 200 and no redirect. An opaque redirect -- Pages sends one for a directory URL without its
    // trailing slash -- has status 0 and must be returned untouched rather than cached, and a 404 page
    // cached under the URL that 404ed would be served in place of the real page once it exists.
    if (res.status === 200 && !res.redirected) {
      await cache.put(k, res.clone());
      if (k !== ROOT) await trim(cache);
    }
    return res;
  } catch (err) {
    // Only a network failure lands here -- an HTTP error is a response and was returned above. An exact
    // URL match or nothing: substituting the root shell for an unvisited facet page would put the
    // whole atlas under a topic URL and let the address bar describe a page the reader is not looking
    // at. The browser's own offline page is a worse experience and a true statement.
    const hit = await caches.match(k);
    if (hit) return hit;
    throw err;
  }
}

async function data(req) {
  const k = key(req.url);
  try {
    const res = await fetch(req);
    if (res.status === 200) {
      const cache = await caches.open(DATA);
      await cache.put(k, res.clone());
      return res;
    }
    // A 4xx or 5xx is returned as it stands, and the cached body is deliberately not used to paper over
    // it. An HTTP error is a fact about the site rather than about the reader's network, and the page has
    // a visible failure path for a data request that does not arrive. A 404 here also means the file
    // moved, and the last thing that should happen then is a reader being kept on the old one for as
    // long as their cache survives.
    return res;
  } catch (err) {
    // The network is gone, so the shell above was almost certainly answered from cache too, and this is
    // the pair the reader is meant to have offline. Marked, so the page can say which day these rows are
    // from rather than repeating a date its own bytes were stamped with -- see `cached` below.
    const hit = await caches.match(k);
    if (hit) return cached(hit);
    throw err;
  }
}

// A cached body, saying so. Two things make this a rewrap rather than a header set: a Response handed back
// by the Cache API has immutable headers, and there is nothing else about it for the page to notice --
// what comes out of that cache is exactly what went in, down to `Last-Modified`. The body is passed
// through as a stream rather than read, so this costs no copy of 552 KB and nothing before the page can
// begin parsing.
//
// Only the data path uses it. A navigation answered from the shell cache is equally a cached response, but
// a document cannot read the headers of its own navigation, so there would be nobody to tell.
function cached(hit) {
  const headers = new Headers(hit.headers);
  headers.set(CACHED, "1");
  return new Response(hit.body, {status: hit.status, statusText: hit.statusText, headers});
}

async function asset(req) {
  // Cache-first, and a miss is not written back. The only way anything enters the shell cache is an
  // install, which fills it completely or not at all, so a version's cache always holds exactly that
  // version's bytes -- and an asset whose content changes gets a new hash, a new worker and a new cache
  // rather than a revalidation that has to be got right.
  const hit = await caches.match(key(req.url));
  return hit || fetch(req);
}

async function trim(cache) {
  // `keys()` is in insertion order, so this drops the oldest additions. It is not true LRU -- the Cache
  // API does not record reads -- but re-putting a page moves it to the end, so a page that is revisited
  // while online does keep its place.
  const keys = await cache.keys();
  for (const k of keys.slice(0, keys.length - PAGES_MAX)) await cache.delete(k);
}
"""

KILL = r"""// A tombstone, written by `python scripts/24_pwa.py --kill`.
//
// Deleting `sw.js` from the site does not uninstall anything: a reader who already has the worker keeps
// it, and the 404 its update check gets is treated as a failed check rather than as an uninstall. The
// only thing that removes a worker is a worker. This one takes itself out, takes this project's caches
// with it, and reloads whatever tabs it controls so they come back over the network. It registers no
// fetch handler, so it is not in the way of anything while it does so.
//
// Ship this, wait for it to reach the readers who visit, and only then drop the registration from the
// page -- in that order, because a page that no longer registers cannot deliver this file either.
self.addEventListener("install", () => self.skipWaiting());

self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    const names = await caches.keys();
    await Promise.all(names
      .filter((n) => n.startsWith("__PREFIX__") || n === "atlas-data" || n === "atlas-pages")
      .map((n) => caches.delete(n)));
    await self.registration.unregister();
    for (const client of await self.clients.matchAll({type: "window"})) client.navigate(client.url);
  })());
});
"""


def version(paths: list[Path]) -> str:
    """The precached bytes, as twelve hex characters.

    Every file's path goes in alongside its contents, so adding a file to the precache list changes the
    version even if that file happens to be a copy of one already there. Twelve characters of SHA-256 is
    about 2^48 of room -- this is a cache name, not a signature, and the only thing it has to do is
    differ whenever the contents do.

    Newlines are normalised because the version has to describe the bytes Pages *serves*, not the bytes
    this checkout happens to hold. `core.autocrlf` is true and there is no `.gitattributes`, so on Windows
    the working copy is CRLF while the committed and served file is LF -- and hashing the working copy made
    the version a function of the operating system. A hand regeneration on Windows and the next Linux cron
    run then disagree about identical content and flip the version back and forth forever, and every flip
    discards every returning reader's cache. Production shipped the CRLF hash this way in `ad237c4`.
    """
    h = hashlib.sha256()
    for p in sorted(paths):
        h.update(p.name.encode("utf-8"))
        h.update(b"\0")
        h.update(p.read_bytes().replace(b"\r\n", b"\n"))
        h.update(b"\0")
    return h.hexdigest()[:12]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--kill", action="store_true",
                    help="write the tombstone worker that uninstalls itself, instead of the real one")
    args = ap.parse_args()

    OUT.mkdir(exist_ok=True)

    if args.kill:
        (OUT / "sw.js").write_text(KILL.replace("__PREFIX__", CACHE_PREFIX), encoding="utf-8")
        print("docs/sw.js is now a tombstone: it unregisters itself and deletes atlas-* caches.")
        print("Commit it, leave the registration in the page until it has had time to reach readers,")
        print("and re-run without --kill to bring the real worker back.")
        return

    # This stage hashes the shell, so it cannot run before the stage that writes it. The failure without
    # this check is not a crash but a version computed from last week's `index.html`, which is a cache
    # that never invalidates -- so it is worth one explicit sentence.
    shell = OUT / "index.html"
    if not shell.exists():
        sys.exit("docs/index.html is missing. Run scripts/19_pages.py first: this stage stamps the "
                 "worker with a hash of the shell it precaches.")
    if not (OUT / "pages.css").exists():
        sys.exit("docs/pages.css is missing. Run scripts/20_landing.py first: the facet pages' "
                 "stylesheet is precached so a cached facet page renders offline.")

    # Written before the hash is taken, because they are part of what is hashed. Unconditionally, like
    # every other generator here: both workflows assert that each tracked file under `docs/` was
    # rewritten by the build, and a write-if-different path would report this stage as missing.
    for name, size, maskable, opaque in ICONS:
        (OUT / name).write_bytes(icon(size, maskable, opaque))

    man = manifest()
    (OUT / "manifest.webmanifest").write_text(
        json.dumps(man, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # The prefix assertion. `start_url` and `scope` are relative and resolve against the manifest's URL,
    # which is the one thing this stage cannot see from disk -- so it is reconstructed from the canonical
    # site URL and checked. A leading slash on either field, or a manifest that ends up somewhere other
    # than the root of `docs/`, breaks this here rather than shipping a worker whose scope is the origin
    # root and which therefore controls none of the pages it was written for.
    man_url = urljoin(SITE, "manifest.webmanifest")
    start = urljoin(man_url, man["start_url"])
    scope = urljoin(man_url, man["scope"])
    prefix = urlsplit(SITE).path
    if start != SITE or scope != SITE:
        sys.exit(f"start_url resolves to {start} and scope to {scope}, but the site is {SITE}. "
                 "Both must be relative to the manifest.")

    files = [OUT / p for p in PRECACHE if p != "./"] + [shell]
    sw = (SW
          .replace("__VERSION__", version(files))
          .replace("__PREFIX__", CACHE_PREFIX)
          .replace("__PAGES_MAX__", str(PAGES_MAX))
          .replace("__CACHEHDR__", b19.CACHED_HEADER)
          .replace("__PRECACHE__", json.dumps(PRECACHE)))
    (OUT / "sw.js").write_text(sw, encoding="utf-8")

    total = sum((OUT / p if p != "./" else shell).stat().st_size for p in PRECACHE)
    for f in ("manifest.webmanifest", "sw.js", *(n for n, *_ in ICONS)):
        print(f"{f:24s} {(OUT / f).stat().st_size / 1024:7.1f} KB")
    print(f"precache {len(PRECACHE)} files · {total / 1024:.0f} KB · version "
          f"{version(files)} · scope {prefix}")
    print(f"data.json ({(OUT / 'data.json').stat().st_size / 1024:.0f} KB) is cached from the page's "
          "own fetch, not precached; the 156 facet pages are cached as they are visited, "
          f"{PAGES_MAX} at a time.")


if __name__ == "__main__":
    main()
