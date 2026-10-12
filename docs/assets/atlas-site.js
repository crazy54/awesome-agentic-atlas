// The site script: every page on the Atlas loads this, through `site_script()` in `scripts/sitewide.py`.
// It does two things.
//
// 1. It paints the build tags in the footer (`buildtags()` in sitewide.py) from the GitHub API: the latest
//    run of the daily, weekly and test workflows on the published branch, and when Pages last deployed.
//    The answer is kept in localStorage for ten minutes, so a reader clicking between pages costs four API
//    calls per ten minutes and not four per page -- GitHub allows sixty an hour to an anonymous address.
//    Every failure is silent: a tag nobody could fill keeps its neutral dot, and its link still goes to
//    the workflow, which is where the answer is anyway.
//
// 2. It opens the admin panel (`atlas-admin.js`) when the address ends in `=admin1337`, with or without a
//    trailing `?`, in either the query or the fragment: `/catalog/?=admin1337?`, `/repo/a/b/#=admin1337`.
//    The 404 page turns a path that ends that way (`/catalog/=admin1337?`) into the query form, so the
//    tail works on any page however it is typed. The trigger is then taken off the address, so a link
//    copied from the bar does not carry it.
//
// NOT A SECURITY BOUNDARY. This is a static site: the string above is in this file for anyone to read, and
// everything the panel does is a choice stored in the reader's own browser. It is out of the way, not locked.

const REPO = document.getElementById("btags")?.dataset.repo || "crazy54/awesome-agentic-atlas";
const BRANCH = "latest_branch";
// `atlas-gh-` like the homepage's star cache (`atlas-gh-repo`): a copy of a GitHub answer, not a choice the
// reader made, which is the line the Archie harnesses draw when they check that nothing was saved.
const KEY = "atlas-gh-builds";
const TTL = 10 * 60 * 1000;
const WORKFLOWS = ["daily.yml", "weekly.yml", "tests.yml"];
const TAIL = /=admin1337\??$/;
const VERSION = new URL(import.meta.url).searchParams.get("v") || "";

// Octicons from the Nerd Font patch of Geist Mono, by code point. See `ICONS` in scripts/subset_fonts.py
// for the full set the font file carries; a code point not in that list draws as an empty box.
export const ICON = {
  "daily.yml": "\uF52E",   // workflow
  "weekly.yml": "\uF487",  // package: the workbooks
  "tests.yml": "\uF499",   // beaker
  pages: "\uF427",         // rocket
};

async function json(url) {
  const r = await fetch(url, {headers: {Accept: "application/vnd.github+json"}});
  if (!r.ok) throw new Error(`${r.status} from ${url}`);
  return r.json();
}

// What the tags and the admin panel both show. Exported so the panel reads the same answer, from the same
// cache, rather than spending the reader's rate limit a second time.
export async function status({fresh = false} = {}) {
  if (!fresh) {
    try {
      const c = JSON.parse(localStorage.getItem(KEY) || "null");
      if (c && c.repo === REPO && Date.now() - c.at < TTL) return c.v;
    } catch (e) {}
  }
  const api = `https://api.github.com/repos/${REPO}`;
  const runs = await Promise.all(WORKFLOWS.map((wf) =>
    json(`${api}/actions/workflows/${wf}/runs?branch=${BRANCH}&per_page=1&exclude_pull_requests=true`)
      .then((j) => {
        const r = j.workflow_runs && j.workflow_runs[0];
        return r ? {wf, status: r.status, conclusion: r.conclusion, at: r.run_started_at || r.created_at,
                    url: r.html_url, event: r.event, n: r.run_number} : {wf};
      })
      .catch(() => null)));
  const deployed = await json(`${api}/deployments?environment=github-pages&per_page=1`)
    .then((j) => (j[0] ? {at: j[0].created_at, sha: (j[0].sha || "").slice(0, 7)} : null))
    .catch(() => null);
  const v = {runs, deployed};
  // Only a complete answer is kept. A rate-limited call is null here, and caching it would pin a grey tag
  // for ten minutes on an answer that a retry on the next page might have got.
  if (runs.every(Boolean) && deployed) {
    try { localStorage.setItem(KEY, JSON.stringify({repo: REPO, at: Date.now(), v})); } catch (e) {}
  }
  return v;
}

// One reading of a run, shared with the panel: [state, words]. `state` is the attribute the stylesheet keys
// on; `words` is what the tag says, so the colour is never the only carrier of the answer.
export function verdict(run) {
  if (!run || !run.status) return ["", "unknown"];
  if (run.status !== "completed") return ["run", run.status === "queued" ? "queued" : "running"];
  if (run.conclusion === "success") return ["ok", "passing"];
  if (run.conclusion === "failure" || run.conclusion === "timed_out" || run.conclusion === "startup_failure")
    return ["bad", "failing"];
  return ["off", (run.conclusion || "unknown").replace(/_/g, " ")];
}

export function ago(iso) {
  const t = Date.parse(iso);
  if (!Number.isFinite(t)) return "";
  const s = Math.max(0, (Date.now() - t) / 1000);
  if (s < 90) return "just now";
  if (s < 5400) return `${Math.round(s / 60)}m ago`;
  if (s < 129600) return `${Math.round(s / 3600)}h ago`;
  return `${Math.round(s / 86400)}d ago`;
}

function paint(root, v) {
  for (const el of root.querySelectorAll(".btag[data-wf]")) {
    const run = v.runs[WORKFLOWS.indexOf(el.dataset.wf)];
    if (run === null) continue;  // that call failed; leave the neutral tag as it was
    const [state, words] = verdict(run);
    el.dataset.state = state;
    el.querySelector(".bv").textContent = words;
    if (run.url) el.href = run.url;
    const label = el.querySelector("b").textContent;
    el.title = `${label}: ${words}` + (run.at ? `, run #${run.n} started ${new Date(run.at).toLocaleString()}` : "");
    el.setAttribute("aria-label", `${label} build ${words}`);
  }
  const dep = root.querySelector(".btag[data-pages]");
  if (dep && v.deployed) {
    dep.dataset.state = "ok";
    dep.querySelector(".bv").textContent = ago(v.deployed.at);
    dep.title = `Published ${new Date(v.deployed.at).toLocaleString()}` + (v.deployed.sha ? ` from ${v.deployed.sha}` : "");
    dep.setAttribute("aria-label", `deployed ${ago(v.deployed.at)}`);
  }
  const sr = root.querySelector("#btagsr");
  if (sr) sr.textContent = "";
}

// The icons go in only once "Atlas Icons" -- the mono file's private-use range, under `swap`; see the note in
// scripts/sitewide.py -- has loaded. `load()` resolving with no face means the family is not declared here.
async function icons(root) {
  try {
    const faces = await document.fonts.load('400 12px "Atlas Icons"', ICON.pages);
    if (!faces.length) return;
    for (const el of root.querySelectorAll(".btag")) {
      const glyph = ICON[el.dataset.wf || "pages"];
      if (glyph) el.querySelector(".bico").textContent = glyph;
    }
  } catch (e) {}
}

function adminAsked() {
  const read = (s) => { try { return decodeURIComponent(s); } catch (e) { return s; } };
  return TAIL.test(read(location.search)) || TAIL.test(read(location.hash));
}

function dropTrigger() {
  try {
    const u = new URL(location.href);
    const strip = (s) => s.replace(/[?#&]?[^?#&=]*=admin1337\??$/, "");
    u.search = strip(decodeURIComponent(u.search));
    u.hash = strip(decodeURIComponent(u.hash));
    history.replaceState(history.state, "", u.pathname + u.search + u.hash);
  } catch (e) {}
}

export async function openAdmin(trigger) {
  // The panel is handed this module's own functions rather than importing them: an `import` of
  // "./atlas-site.js" without this file's exact `?v=` would be a second instance of it, which would paint
  // the tags again and see the trigger in the address again.
  const m = await import(`./atlas-admin.js?v=${VERSION}`);
  return m.open({trigger, api: {status, verdict, ago}});
}

const root = document.getElementById("btags");
if (root) {
  icons(root);
  // After load, so four API calls never compete with the page's own data for the first paint.
  const go = () => status().then((v) => paint(root, v)).catch(() => {});
  if (document.readyState === "complete") go(); else addEventListener("load", go, {once: true});
}

if (adminAsked()) {
  dropTrigger();
  openAdmin().catch((e) => console.warn("The admin panel did not load:", e));
}

// A theme unlocked in another tab shows up in this one's Settings menu without a reload.
addEventListener("storage", (ev) => {
  if (ev.key === "atlas-unlock" && typeof window.atlasPaintSettings === "function") window.atlasPaintSettings();
});
