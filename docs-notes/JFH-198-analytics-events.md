# JFH-198 — filter, search and outbound-click events

Investigation note, 2026-09-06. Not a published surface: `docs-notes/` sits outside `docs/`, so GitHub
Pages never sees it.

The ticket asks for an event layer over the analytics shipped in JFH-177. Before designing one it has to
be settled whether Cloudflare Web Analytics can carry custom events at all, and whether it already sees
the URL hash — because this site puts every filter in the hash, and if the beacon reported it, most of
this ticket would already be done. Both questions are now answered, from Cloudflare's own current
documentation and from the shipped `beacon.min.js` itself.

---

## The short answer

1. **No custom events.** Cloudflare Web Analytics has no custom-event or custom-metric API, at any plan
   level. Documented as "not yet", and confirmed by reading the beacon: its event-type enum has exactly
   three members and it exposes no callable global.
2. **The hash is stripped, on purpose.** The beacon runs every URL it reports through a `cleanLocation()`
   helper that blanks `hash`, `search`, `username` and `password`. So `#topic=x&target=y&sort=stars` is
   invisible to it, and always will be while that function exists. Cloudflare says the same thing about
   query strings in the FAQ, and gives the reason: avoiding sensitive data.
3. **The ticket's premise is inverted, and this matters.** The ticket says `history.replaceState` makes
   "every filtered view collapse into a single pageview of `/`". On Chromium the opposite happens: every
   `replaceState` fires an *extra* page-load beacon for `/`. Filtered views are indistinguishable not
   because they are collapsed but because the hash is removed from each one.
4. **Most of what the ticket wants is already being collected — by paths, not events.** `20_landing.py`
   and `22_detail.py` prerender 1,451 real pages besides the index. Every one is a distinct `Path` in
   Cloudflare's existing reports. That covers "which topic/target combinations get crossed" (for arrivals)
   and "which projects get clicked through to" (completely, since the index's row titles now link inward
   to `/repo/<owner>/<name>/`).
5. **Exactly one thing in this ticket is unobtainable and worth having: zero-result search terms.** It is
   also the thing the ticket itself calls "probably the single most actionable dataset this site could
   collect", and it is the only item that needs new machinery.

**Recommendation:** split the ticket. Close the filter-combination and outbound-click halves as already
satisfied, and reduce the remainder to zero-result search terms. For that one dataset, ship an opt-in
prefilled-issue link on the empty result set — no script, no request, no cookie, no service, no vendor —
and hold the Worker + Analytics Engine design in reserve if 60 days of that produces too little. Snippets
for the link are at the end of this note.

---

## Method: what I verified, and how

| Claim | How established |
| --- | --- |
| No custom-event API | Cloudflare FAQ, **and** read of the shipped `beacon.min.js` (enum + no exported global) |
| Hash and query string stripped | Read of `cleanLocation()` in `beacon.min.js`, **and** captured live payloads |
| SPA navigations counted, and by which mechanism | Cloudflare SPA doc, **and** captured payloads on three engine configurations |
| `replaceState` inflates `/` page views on Chromium | Captured payloads only — see the caveat below |
| `"spa": false` collapses 10 beacon POSTs to 2 | Captured payloads, against the real `docs/index.html` |
| Payload byte sizes | Measured (`Content-Length` at the collector) |
| Analytics Engine / Workers / Zaraz limits and prices | Documentation only; not exercised |
| GraphQL dataset name for RUM page loads | **Not verified** — see "Weaknesses" |

The beacon under test was fetched from `https://static.cloudflareinsights.com/beacon.min.js` on
2026-09-06: 30,294 bytes, `ETag: W/"2026.9.1"`, `Last-Modified: Wed, 02 Sep 2026 15:29:47 GMT`. That
matches the newest changelog entry (2026-09-02) and the `versions.js` field in its own payload, so the
version I read is the version in production.

Payloads were captured without sending anything to Cloudflare. The beacon honours
`data-cf-beacon='{"send":{"to":"<url>"}}'`, so pointing that at a same-origin local endpoint yields the
real payload with no CORS in the way and nothing landing in the project's real Web Analytics account. The
token used in the probes was 32 zeroes, not the project's. Scripts and captures are in
`%TEMP%/jfh198/` (`probe.py`, `probe_real.py`, `probe_nonav.py`, `captured*.jsonl`); they are outside the
repository on purpose and can be deleted.

---

## Finding 1 — there is no custom-event API

> **Does Web Analytics support custom events?**
> Not yet, but we may add support for this in the future.
> — <https://developers.cloudflare.com/web-analytics/faq/> (page last updated 2026-07-14)

> Currently, Cloudflare Web Analytics do not log query strings to avoid collecting potentially sensitive
> data, but we may add support for this in the future.
> — same page, on UTM parameters

> We do not support custom integrations directly with the endpoint: all requests should originate from our
> beacon JavaScript.
> — same page, on `/cdn-cgi/rum`

That last quote closes the obvious workaround of POSTing to `/cdn-cgi/rum` directly.

The beacon agrees. Its whole event vocabulary is three values:

```js
t[t.Load=1]="Load", t[t.Additional=2]="Additional", t[t.WebVitalsV2=3]="WebVitalsV2"
```

Its configuration surface — everything it reads out of `data-cf-beacon` or `window.__cfBeacon` — is
`token`, `version`, `load`, `spa`, `send.to`, `serverTiming` and `icTag`. Nothing else. `window.__cfBeacon`
is input config that the beacon reads and writes back; it is not an API object, and the beacon installs no
callable global. There is no `track()` to call, no plan that unlocks one, and no field in the payload that
would carry an arbitrary name or value.

**Verified.** Documentation and code agree.

## Finding 2 — the hash is stripped before anything is reported

Every URL the beacon reports goes through one helper, which is worth quoting in full because it settles
the central question of this ticket on its own:

```js
e.cleanLocation = function(t) {
  if (!t) return t;
  try {
    const e = new URL(t);
    return e.username = "", e.password = "", e.hash = "", e.search = "", e.toString()
  } catch (e) {
    let n = t.split("?")[0].split("#")[0];
    /* ...strips userinfo from the fallback path too... */
    return n
  }
}
```

and the payload builder calls it on both fields that could have carried the hash:

```js
location: (0, a.cleanLocation)(i || n()) || "",
referrer: (0, a.cleanLocation)(W(u)),
```

Confirmed empirically. Loading a probe page at
`http://127.0.0.1:8731/#q=observability&topic=agents&target=claude-code&sort=stars&os=linux` produced a
page-load payload whose `location` was `http://127.0.0.1:8731/` — the entire fragment absent. Same on the
real `docs/index.html` loaded at `#topic=harnesses-and-runtime-infra&os=linux`.

So the "already collected" outcome is **false for the hash**. There is no report, dashboard filter or
GraphQL dimension that can recover `#topic=x&target=y`, because those bytes never leave the browser.

Two consequences worth noting in the site's favour, though:

- The strip is a privacy feature, not an oversight. Cloudflare removes the fragment and the query for the
  same reason it removes `username:password@`. Any design that routes reader input around it is
  deliberately defeating a vendor safeguard — see "Considered and rejected" below.
- `search` is stripped too, so there is no cheaper trick of moving filters into a query string.

**Verified.** Code read plus captured payloads.

## Finding 3 — `replaceState` is counted on Chromium; the ticket has the mechanism backwards

Cloudflare tracks SPA navigation by three routes, in order of preference:

> 1. Using the Soft Navigations API
> 2. Listening on `navigate` events via the Navigation API
> 3. By patching the History API's `pushState` function and listening to the `onpopstate` event
>
> — <https://developers.cloudflare.com/web-analytics/get-started/web-analytics-spa/> (last updated 2026-08-20)

Route 3 does not cover `replaceState`, which is what `writeHash()` uses — and that is presumably where the
ticket's premise came from. But route 2 does: the Navigation API's `navigate` event fires for
`replaceState` as well. So the behaviour splits by engine, and I measured both.

**Chromium 148 (Navigation API present).** Real `docs/index.html`, four filter changes driven through the
page's own `set()`:

| # | bytes | eventType | nt | location |
| --- | --- | --- | --- | --- |
| 1 | 785 | 1 Load | navigate | `/` |
| 2 | 349 | 1 Load | routing-apis | `/` |
| 3 | 786 | 3 WebVitals | navigate | `/` |
| 4 | 337 | 3 WebVitals | routing-apis | `/` |
| 5 | 349 | 1 Load | routing-apis | `/` |
| 6 | 349 | 1 Load | routing-apis | `/` |
| 7 | 337 | 3 WebVitals | routing-apis | `/` |
| 8 | 349 | 1 Load | routing-apis | `/` |
| 9 | 337 | 3 WebVitals | routing-apis | `/` |
| 10 | 337 | 3 WebVitals | routing-apis | `/` |

Ten POSTs, of which **five are page-load events for `/`**. Note beacon #2: it arrives before any
interaction, because `readHash()`/`writeHash()` call `replaceState` during initialisation. So even a
reader who follows a filter link and then does nothing at all reports two page loads of `/`.

**Chromium with `window.navigation` removed** (which is how the beacon behaves on any engine that lacks
the Navigation API — I forced the fallback rather than trust it):

- `replaceState('#topic=…')` → **no beacon at all**
- `pushState('#topic=…')` → one beacon, `location` = `http://127.0.0.1:8735/` (bare origin: the beacon's
  URL builder tries `new URL("#…")`, which throws, and falls back to origin-only)
- `pushState('/probe/control-path')` → one beacon, `location` = `…/probe/control-path` — the control, which
  proves a real path *is* reported

So the site's `/` page-view count is currently **1 + (number of filter interactions) per Chromium visit,
and 1 per visit on engines without the Navigation API.** That is an engine-dependent bias in the site's
headline number, and nobody has been told about it.

Three mitigations already exist, and they are why this is a nuisance rather than a crisis:

- The **Navigation type** dimension separates them. Filtering to navigation types other than
  *Routing APIs* and *Soft Navigation* gives the true count of loads of `/`.
- **Visits** are unaffected. Cloudflare defines a visit as a page view whose HTTP referer does not match
  the hostname; the route-change payloads carry a same-origin `referrer`, so they cannot become visits.
- The *Routing APIs* count is itself **a free aggregate filter-engagement metric** — not which filters,
  but how many interactions per session. That is a real if crude answer to "do people use the filters".

**Verified for Chromium 148 and for the forced fallback.** *Not* verified: that Cloudflare's dashboard
counts these as "Page views". The payloads are indistinguishable from a real load (eventType 1, fresh
`pageloadId`, incrementing `n`) and the docs describe SPA route changes as measurements to be reported, so
the inference is solid — but it is an inference. One dashboard check settles it: compare `/` page views
with and without the *Routing APIs* navigation type.

## Finding 4 — most of the ticket is already answerable, from paths

This is the part the ticket does not account for, and it changes the scope substantially. The site does not
consist of one page. `20_landing.py` and `22_detail.py` prerender real, separately-addressable pages, and
`Path` is one of Cloudflare's existing dimensions.

| Path shape | Count | What a page view there means |
| --- | --- | --- |
| `/` | 1 | the filterable index |
| `/topic/<topic>/` | 14 | arrived at one topic |
| `/topic/<topic>/target/<target>/` | 130 | **arrived at a topic × harness crossing** |
| `/target/<target>/` | 12 | arrived at one harness |
| `/repo/` + `/repo/<owner>/<name>/` | 1 + 1,294 | **opened one project's detail page** |

1,452 distinct paths, all already reported today. Against the ticket's acceptance criteria:

- *"Filter combinations rankable by use"* — **partly already true.** The 130 crossing paths are exactly the
  topic × target combinations, and they are cross-linked to each other by `related()`, so moving between
  cells of the grid is a real navigation and a real page view. What is missing is in-page chip filtering,
  the OS axis, `confirmed`, `new` and `sort`. So: the two-axis crossing question is answerable for
  arrivals and for grid navigation; it is not answerable for a reader who lands on `/` and clicks chips.
- *"Which projects get clicked through to"* — **effectively already true, and better than the ticket
  asks.** The index's row title and screenshot now link inward to `detailURL(r.nwo)`, not to GitHub; only
  the small `owner/name` line goes outward. So the click the ticket wants to count *is* a page view of
  `/repo/<owner>/<name>/`, for all 1,294 projects, with no instrumentation. The final hop from the detail
  page to `github.com` is not counted, but it is downstream of the interesting decision and the detail
  page view is a superset of it.
- *"Zero-result searches are queryable"* — **impossible.** No configuration of this beacon can carry the
  term.
- *"No PII, no cookies, no consent banner"* — true today and must stay true.
- *"Page weight impact stated and kept small"* — currently 30,294 bytes of third-party script plus roughly
  780 bytes + 350 × N of POST body. Documented here for the first time.

One caveat on ranking 1,294 paths: the dashboard shows a top-paths list, and Cloudflare applies
adaptive-bit-rate sampling (between 0.0001% and 100%, chosen per query) to both the dashboard and the
GraphQL API. Low-traffic sites are sampled at higher rates, so at this site's volume the numbers should be
close to exact, but a long tail of one-view repos will be noisy. Retention is six months.

## What is actually missing

After Finding 4, the honest remaining list is:

1. **Zero-result search terms.** Unobtainable, and the highest-value item in the ticket. A term that
   returns nothing names either a tool the atlas lacks or a word its taxonomy does not use — and thanks to
   `near()`, the empty branch of `render()` is only reached when the trigram fallback *also* found nothing,
   so a term that gets there is not a typo of anything in the atlas. That is a remarkably clean signal.
2. **In-page filter combinations**, including the OS axis, `confirmed`, `new` and `sort`. Obtainable only
   with new machinery. Value: moderate — it would rank chip usage, but the crossing question it was mainly
   meant to answer is already partly covered by the 130 prerendered paths.
3. **Theme toggles.** Obtainable, near-worthless. Not worth a byte.
4. **The github.com hop from a detail page.** Obtainable, largely redundant given item 2 of Finding 4.

Only item 1 justifies new machinery. Items 2–4 do not, on their own.

---

## Options for zero-result search terms

The binding constraints: no build step, no runtime npm dependency, no third-party script beyond the one
beacon, no cookies, no personal data, no new paid or administered service if avoidable. And the structural
one: **GitHub Pages serves static files and cannot run server-side code**, which rules out a same-origin
`/collect` endpoint, server-side log analysis, and edge middleware. Anything that receives an event must
live somewhere else.

### A. Ask, do not measure — a prefilled issue link on the empty result set  *(recommended)*

When a search returns nothing and the trigram fallback also finds nothing, offer a quiet link that opens a
GitHub issue prefilled with the term, the active filters and the snapshot date.

- **Cost to the reader:** zero bytes of new script, zero requests, zero cookies, zero collection from
  anyone who does not press it. About 25 lines of page source, mostly comment.
- **Cost to the owner:** nothing to deploy, nothing to administer, nothing to pay for, no new origin, no
  secret, no CI change. Reports arrive already written up, in the tracker where taxonomy work happens.
- **What you get:** a small number of high-quality, self-explaining reports.
- **What you do not get:** a rate. No denominator, no ranking, heavily biased toward motivated readers.
  If ten people a week search for a missing tool and none of them press the link, you learn nothing.
- **Privacy:** this is the only option that does not erode the current position at all in the passive
  sense — nothing is collected from a reader who does not act. It must still be said plainly that a reader
  who *does* press it files a public issue under their own GitHub account, so the act is self-identifying
  by construction. That is their choice to make, which is precisely why this is an `<a href>` and not a
  `fetch()`.

### B. Cloudflare Worker + Workers Analytics Engine

A ~30-line Worker on `*.workers.dev` with an Analytics Engine binding; the page `fetch()`es it (no script
loaded, so the "no third-party script" constraint holds in letter and mostly in spirit) with
`{term, filters, hits: 0}`.

- **Cost:** Workers Free allows 100,000 requests/day; Analytics Engine on the free plan allows 100,000
  data points written and 10,000 read queries per day, and Cloudflare currently bills nothing at all for
  Analytics Engine ("Currently, you will not be billed for your use of Workers Analytics Engine"). Limits:
  20 blobs / 20 doubles / 1 index per data point, index ≤ 96 bytes, 3 months retention. All comfortably
  within reach at this site's volume. Page weight: ~600 bytes of script, one `sendBeacon` per zero-result
  search, debounced.
- **Cost to the owner:** a Worker to deploy and keep deployed, `wrangler` in the toolchain or a manual
  deploy, a CORS allowlist, a rate limit, and a bot-filtering decision. This is the "new service to
  administer" the constraints ask to avoid — but it is on the Cloudflare account that already exists for
  Web Analytics, and it costs nothing.
- **Privacy:** this is where the line moves, and it must be said out loud. **It would be the first thing
  this site ever collects that is free-typed reader input.** Search boxes receive pasted email addresses,
  internal hostnames and worse. Mitigations exist and should be mandatory rather than optional: truncate
  hard (64 chars), reject anything matching `@` or a URL shape, drop control characters, store no IP and
  set no cookie, and state the whole thing in the README. Even then the honest description changes from
  "collects nothing identifying" to "collects the words readers type into the search box, filtered".
- Preferred over the ticket's "Worker + KV": KV is a key-value store being asked to be a time series.
  Analytics Engine is the right primitive, has unlimited cardinality by design, and is queryable with SQL.

### C. Vendor with a custom-event API — rejected on constraints

Plausible (`plausible('EventName', {props})`) and Umami and GoatCounter
(`window.goatcounter.count({path, event: true})`) all have exactly the API this ticket wants, are cookieless
and need no consent banner. Every one of them ships a second third-party script, which the constraints
exclude; Plausible's hosted tier is paid, and self-hosting any of them is a service to administer. If the
"no third-party script" constraint were ever relaxed, GoatCounter is the cheapest of these to adopt and
the closest in spirit to this project. It is not relaxed, so: no.

### D. Cloudflare Zaraz — not available here

Zaraz does have `zaraz.track()`. But on a domain not proxied through Cloudflare it requires loading the
script from *your own* Cloudflare-proxied subdomain. This site is `crazy54.github.io`, and `github.io`
cannot be added to anyone's Cloudflare account. Zaraz therefore requires buying and administering a
domain first, which is a bigger change than the thing it enables. (Web Analytics works without a domain
only because its JS-beacon mode is explicitly designed to — which is exactly what the `beacon()` comment
in `19_pages.py` already says.)

### Considered and rejected: smuggling the term into the path

The one way to get the real dataset with no new service. Finding 3's control proves the beacon reports the
`pushState` path verbatim, so on a zero-result search the page could `pushState('/search-miss/<term>/')`,
let the beacon fire, then `replaceState` the correct hash URL back. Cloudflare's `Path` dimension would
then hold the zero-result terms, for free, with no server, no vendor and no new origin.

Reject it, for four reasons in descending order of seriousness:

1. **It is a privacy regression by stealth.** `cleanLocation()` strips the fragment and the query
   *specifically* so that reader input does not reach Cloudflare; the FAQ says so. Encoding that input into
   the path to get around it puts free-typed reader text into a third party's six-month store, with no
   truncation, no filtering and no control by the owner. It is strictly worse on privacy than option B,
   which collects the same data into a store the owner controls and can sanitise.
2. **It breaks URL integrity.** There is a window in which the address bar shows a path that 404s, and the
   `pushState`/`replaceState` pair leaves an extra history entry, so the back button starts behaving
   differently after a failed search than after a successful one. `writeHash()` uses `replaceState` for
   exactly this reason.
3. **It pollutes the page-view total** with synthetic paths that look like real pages.
4. It is against the letter of "all requests should originate from our beacon JavaScript" — the requests
   would, but the content would not be what the beacon is for.

Worth writing down because it is the only zero-service route to the real data, and because someone will
think of it later.

---

## Recommendation

1. **Re-scope JFH-198.** Close the filter-combination and outbound-click halves, citing Finding 4: the 130
   crossing paths and the 1,294 detail paths already answer them, and the queries are recorded below. Keep
   one narrow issue open for zero-result search terms.
2. **Ship option A** — the prefilled-issue link. Snippets below. It is small, reversible, costs the reader
   nothing, and asks nothing of the owner.
3. **Do not change the beacon's `spa` setting yet; check the dashboard first.** If `/` page views turn out
   to be inflated as Finding 3 predicts, decide between (a) leaving it on and always filtering the
   *Routing APIs* navigation type when reading reports, keeping it as a free filter-engagement counter, or
   (b) setting `"spa": false`, which I measured as taking a four-filter session from ten beacon POSTs to
   two. My preference is (a): the dimension already separates them, the extra bytes are trivial against a
   30 KB page and a 380 KB `data.json`, and the aggregate interaction count is genuinely useful. The
   one-token diff for (b) is below in case you disagree.
4. **Revisit option B in 60 days,** with a decision rule set in advance: if fewer than five prefilled
   issues arrive, the interest is not there and the Worker is not worth building; if more than about
   twenty, option A has proven the demand and the Worker is worth the privacy paragraph it will cost.

### Queries that answer the closed halves

All in the Web Analytics dashboard for the site, with **Exclude Bots = Yes** (the beacon is JS-only, so bot
noise is already low, but crawlers that execute JS exist):

- **Topic × harness crossings, ranked:** filter `Path` starts with `/awesome-agentic-atlas/topic/` and
  contains `/target/`, group by `Path`. 130 rows, ranked by page views.
- **Single-axis interest:** the same with `Path` starting `/topic/` or `/target/` and *not* containing the
  other segment.
- **Projects clicked through to, ranked:** filter `Path` starts with `/awesome-agentic-atlas/repo/`, group
  by `Path`. Up to 1,294 rows. This is the click-through ranking the ticket asks for.
- **How the reader got there:** `Referer path` on those same rows, available from the GraphQL API but not
  the dashboard, distinguishes "arrived from a search engine" from "arrived from the index".
- **Aggregate filter interactions:** `Path` = `/awesome-agentic-atlas/` and `Navigation type` =
  *Routing APIs*. Chromium-only, so read it as a lower bound.
- **True loads of the index:** the same path with `Navigation type` ≠ *Routing APIs* and ≠ *Soft
  Navigation*.

Ranking the full 1,294-row tail needs the GraphQL Analytics API rather than the dashboard. Authenticate
with an Analytics-scoped API token and group the RUM page-load dataset by request path; check the exact
dataset and field names by introspection in the GraphiQL explorer, and read the `sampleInterval` field on
every result — see "Weaknesses".

---

## The privacy line

Where the site stands today, and it is worth stating precisely because it is unusually good: no cookies,
no `localStorage` beyond a single `theme` key that is the reader's own explicit choice, no identifiers, no
consent banner, and one third-party script that Cloudflare designed to strip fragments, query strings and
userinfo before reporting. Nothing the site collects can be tied to a person.

- **Option A does not move that line passively at all.** It collects nothing. A reader who presses the link
  chooses to file a public issue under their own GitHub identity, which is self-identifying — but it is an
  act they take, on a surface they can read first, and they can edit or abandon the prefilled issue.
- **Option B moves it.** Search-box text is free-typed reader input, and free-typed input is where personal
  data arrives by accident. The truncation, the `@`/URL rejection and the no-IP/no-cookie rules are not
  polish; they are the reason the option is acceptable at all. If option B ships, the README has to say
  what is collected, in plain words, before anyone asks.
- **The path-smuggling trick moves the line furthest** while looking like it moves nothing, because the
  data lands somewhere the owner cannot sanitise or delete. That is why it is rejected above.
- **Options C and D move it** by adding a second third-party script — a second party with its own
  retention policy, and one more origin that sees every reader's IP.

---

## Weaknesses in this analysis

- **The page-view inflation in Finding 3 is an inference about Cloudflare's aggregation, not a measurement
  of it.** I captured the payloads; I could not query the dashboard or the GraphQL API, because that needs
  an account token I do not have. If Cloudflare filters `nt: routing-apis` out of the page-view metric,
  Finding 3's practical consequence disappears (the ticket's premise would then be right by accident, and
  the "free filter-engagement counter" evaporates). Everything else in this note stands either way.
- **The GraphQL dataset name is unverified.** Cloudflare's docs describe how to explore the schema but do
  not publish the RUM dataset name on any page I could find. Confirm by introspection before writing a
  query; do not trust a name from memory.
- **Core Web Vitals may be distorted by the route-change beacons, and I could not settle it.** In the
  synthetic probe the vitals split across `pageloadId`s: the real navigate load reported only TTFB, and
  LCP/CLS/FCP landed on a synthetic routing-apis pseudo-load. On the real `docs/index.html` that did *not*
  happen — the navigate load kept all four. So the failure mode is real but timing-dependent, and I do not
  know how often it fires in the wild. Worth a look at whether the CWV panel's numbers look sane. (If they
  do not, that is a second argument for `"spa": false`.)
- **`19_pages.py` is being edited concurrently, and drifted while this note was being written** — it went
  from 1,886 lines to 1,901, and four of the five anchors below moved. The numbers were refreshed against
  md5 `8f3633a6121b2c5619a7a9d7f6c2df7c` and will be wrong again shortly. Match on the quoted text, not the
  number.
- **Engine coverage of the empirical work is one engine.** Chromium 148 (`chrome-headless-shell`), plus a
  forced no-Navigation-API variant standing in for Safari and Firefox. I did not run a real Safari or
  Firefox. The forced variant exercises the same code branch, but "same branch" is not "same browser".
- **Option A's yield is unknowable in advance.** It could be zero. The 60-day decision rule exists because
  I cannot honestly predict it, and shipping the Worker first would be building the expensive thing on a
  guess.
- **I did not measure the site's actual traffic**, so every "comfortably within the free tier" claim about
  option B is an assumption about volume rather than a calculation from it. Check the current page-view
  figure before relying on it.
- **The snippets were exercised in isolation, not in a build.** `scripts/19_pages.py` cannot be run without
  the 64 MB `cache/`, so nothing below has been through `substitute()` and out onto a page. `missLink()` was
  run in Chromium against stubbed `state`/`esc`/`SNAPSHOT`/`REPO` — a term containing a tab, `<script>`, `&`
  and `"` encodes cleanly, an empty term returns `""`, and a 300-character term truncates as intended — and
  the `"spa": false` f-string was checked to emit JSON that `json.loads` accepts. That covers syntax and
  escaping. It does not cover how the link looks on the page, or how it reads to someone who has just failed
  to find something; look at both before shipping.

---

## Snippets for `scripts/19_pages.py`

Not applied — that file is owned and being edited elsewhere. Line numbers are as of the reading above and
will have drifted; the quoted anchors will not have.

### 1. A `REPO` constant for the page's script

The prefilled-issue href has to be composed in script, and `substitute()` replaces `__REPO__` across the
whole page string, so the same placeholder trick `SNAPSHOT` and `BUILT` already use works here.

**Immediately after line 884, which currently reads `const BUILT = "__BUILT__";`** — insert:

```js

// The repository, in script rather than in markup, for the one link on this page whose href has to be
// composed: the "tell us what's missing" line on an empty result set carries the search term in a query
// string. Substituted the same way SNAPSHOT and BUILT are, because `substitute()` replaces __REPO__ over
// the whole page and does not care that this occurrence is inside a <script>.
const REPO = "__REPO__";
```

### 2. The link itself

**Immediately after line 1545, which is the closing `}` of `function rescue()`** (the line after
`.slice(0, 4);`) — insert:

```js

// The one thing about this page that analytics cannot learn, and the one worth learning.
//
// Cloudflare's beacon runs every URL it reports through a helper that blanks the hash and the query before
// sending -- verified against beacon.min.js 2026.9.1 -- so `#q=kubernetes` never leaves the browser, and no
// dashboard filter or plan upgrade can recover it. A page view of `/topic/x/target/y/` is a real fact and a
// search for a tool that is not here is not, and the second one is the more useful.
//
// So the reader is asked instead of measured. A prefilled issue link costs no script, no request and no
// cookie; it collects nothing from anyone who does not press it; and what arrives lands in the tracker
// where taxonomy work already happens, already written up by someone who knows what they wanted. The trade
// is worth stating plainly: this yields a handful of good reports rather than a rate, and the reader who
// sends one identifies themselves through their own GitHub account -- which is their decision to make, and
// exactly why this is an anchor and not a fetch().
//
// Only rendered from the empty branch of render(), which is the gate that makes it worth having: `near()`
// has already offered every trigram-near correction as real rows before that branch can be reached, so a
// term that gets this far is not a misspelling of anything in the atlas. It is a word the atlas does not
// know.
function missLink() {
  // The reader's own free text, on its way into a URL. Control characters go because a pasted newline
  // would split the issue title, and 80 characters because a pasted paragraph makes an issue nobody triages
  // -- the useful terms are two or three words.
  const q = state.q.replace(/[\u0000-\u001f]+/g, " ").trim().slice(0, 80);
  if (!q) return "";
  // The filters travel with the term, because "kubernetes, confirmed-only, Windows" and "kubernetes" are
  // different findings and only one of them is a coverage gap. The hash is already the canonical
  // description of the view, so it is what gets quoted.
  const body = "Searched for: " + q + "\n\nFilters: " + (location.hash.slice(1) || "none") +
    "\nSnapshot: " + SNAPSHOT + "\n\nWhat were you hoping to find? A repository URL is ideal.\n";
  const href = "https://github.com/" + REPO + "/issues/new?labels=coverage&title=" +
    encodeURIComponent("Nothing found for “" + q + "”") + "&body=" + encodeURIComponent(body);
  // esc() on the href like every other URL this file writes into an attribute: the two query separators are
  // bare ampersands, which a validator rejects and a strict parser may mangle. target=_blank because the
  // whole point of keeping state in the hash is that the view survives, and a same-tab navigation to GitHub
  // would throw away the filters the reader spent six clicks building.
  return '<p><a class="miss" href="' + esc(href) + '" target="_blank" rel="noopener">' +
    "Searched for something that isn’t here? Tell us what’s missing</a></p>";
}
```

### 3. Render it in the empty branch

**Line 1702 currently reads:**

```js
      '<p style="margin-top:16px"><button class="fix" data-all="1">Clear all filters</button></p>' +
```

**Replace that single line with:**

```js
      '<p style="margin-top:16px"><button class="fix" data-all="1">Clear all filters</button></p>' +
      // Last, and after Clear all, because loosening a filter is what most empty result sets need and
      // reporting a gap is the rarer thing. Returns "" unless there is a search term, so a reader who has
      // only over-filtered is not invited to file an issue about it.
      missLink() +
```

No change is needed in `wire()`. The delegated `#out` listener tests `closest(".fix")` and
`closest(".copy")`, so a click on this anchor matches neither and falls through to the browser's own
handling of the href — which is the whole reason this is an anchor.

### 4. Style

**Immediately after line 514, which currently reads `.fix:hover .n{color:var(--ink2)}`** — insert:

```css
/* Quieter than the rescue buttons above it, deliberately. Loosening a filter fixes most empty result sets,
   and a link that shouted would be pressed by readers who only mistyped -- who are already served by the
   near-match rows that ran before this branch. The underline is explicit because the global rule sets
   text-decoration:none on every anchor, and a link that looks like text is not an affordance. */
.empty .miss{color:var(--muted);font-size:13px;text-decoration:underline}
.empty .miss:hover{color:var(--ink)}
```

### 5. Optional — clean page-view counts, if you decide the inflation matters

**Line 156 currently reads:**

```python
            f"data-cf-beacon='{{\"token\": \"{token}\"}}'></script>"
```

**Replace with:**

```python
            f"data-cf-beacon='{{\"token\": \"{token}\", \"spa\": false}}'></script>"
```

and add this to the comment block above `CF_TOKEN`:

```python
# `spa` is off, against Cloudflare's default, because this page is not a single-page app and the default
# measures it as one. Every filter change calls `history.replaceState` in `writeHash()`, and on any engine
# with the Navigation API the beacon treats that as a route change and reports another page load of `/` --
# so four filter clicks became ten POSTs and five page-load events where there had been one visit. The hash
# that distinguishes those views is stripped from every one of them before sending, so the extra events
# carry no information: they are the same `/` five times. Off, they collapse back to one load and one
# web-vitals report. The cost is Cloudflare's SPA route tracking, which measures nothing here, because every
# real navigation on this site is a real document load of a real prerendered path.
```

Note what this gives up, since it is not nothing: the *Routing APIs* navigation type is currently a free
count of filter interactions per session. If that number is interesting, leave `spa` alone and filter the
navigation type when reading reports instead.

---

## Sources

All fetched 2026-09-06. Cloudflare docs carry their own last-updated dates, quoted here.

| Source | Date | Used for |
| --- | --- | --- |
| <https://developers.cloudflare.com/web-analytics/faq/> | 2026-07-14 | no custom events; no query-string logging; no custom endpoint integrations; ABR sampling 0.0001–100%; `sampleInterval`; six-month retention |
| <https://developers.cloudflare.com/web-analytics/get-started/web-analytics-spa/> | 2026-08-20 | the three SPA detection routes; `"spa": false` |
| <https://developers.cloudflare.com/web-analytics/data-metrics/dimensions/> | 2026-08-21 | Country, Host, Path, Referer, Device type, Browser, OS, Site, Exclude Bots, Navigation type; *Routing APIs* and *Soft Navigation* definitions; referer path via GraphQL only |
| <https://developers.cloudflare.com/web-analytics/data-metrics/high-level-metrics/> | 2026-04-16 | Visits vs Page views definitions |
| <https://developers.cloudflare.com/web-analytics/data-metrics/data-origin-and-collection/> | 2026-04-17 | `/cdn-cgi/rum` endpoints; CWV reported on first `visibilityState` hidden |
| <https://developers.cloudflare.com/web-analytics/about/> | 2026-04-17 | free; privacy-first; no DNS change; "does not collect or use your visitors' personal data" |
| <https://developers.cloudflare.com/web-analytics/limits/> | 2026-08-12 | 10 non-proxied sites; Rules limit 0 on Free |
| <https://developers.cloudflare.com/web-analytics/changelog/> | 2026-04-16 (entries to 2026-09-02) | beacon version history; corroborates the fetched build |
| <https://static.cloudflareinsights.com/beacon.min.js> | `Last-Modified` 2026-09-02, ETag `W/"2026.9.1"` | `cleanLocation()`; the three-member `EventType` enum; the config surface; the `pushState`-only History fallback; no exported API |
| <https://developers.cloudflare.com/analytics/analytics-engine/> and `/limits/`, `/pricing/` | 2026-04-23 | option B: free-plan quotas, 20 blobs / 96-byte index / 16 KB, 3-month retention, currently unbilled |
| <https://developers.cloudflare.com/workers/platform/pricing/> | — | Workers Free: 100,000 requests/day, 10 ms CPU |
| <https://developers.cloudflare.com/zaraz/get-started/> and `/advanced/domains-not-proxied/` | 2026-04-16 | `zaraz.track()` exists; non-proxied use needs your own Cloudflare-proxied subdomain |
| <https://plausible.io/docs/custom-event-goals> | — | `plausible('EventName', {props})` |
| <https://www.goatcounter.com/help/events> | — | `window.goatcounter.count({path, event: true})` |

Repository evidence, read directly: `scripts/19_pages.py` (`beacon()`, `writeHash()`, `readHash()`,
`set()`, `wire()`, `render()`, `detailURL`), `scripts/20_landing.py` (14 + 12 + 130 prerendered paths,
`related()`, `live`), and the on-disk counts under `docs/topic/`, `docs/target/` and `docs/repo/`.
