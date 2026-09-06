/* Written by scripts/22_detail.py. Shared by every page under docs/repo/.

   Three jobs, none of which the page needs in order to be complete: the theme toggle, the copy button,
   and the two figures that are deliberately not in the HTML. */
"use strict";

/* Not a data fetch and not a framework: the light half of the theme is in detail.css and without a
   switch nothing on these pages can ever reach it.

   Three pieces, ported from `wire()` in 19_pages.py, because the toggle used to change nothing beyond
   this tab's current document: the write on click, so the choice survives the next link; the agreement
   with the head script on load; and the listener, so a reader who has expressed no choice follows their
   OS the way the index does. The *read* is not here -- it is inline in every page's <head>, because by
   the time this file has been fetched and run the wrong theme has already been painted.

   label() is folded into every path that changes the theme, which is the index's arrangement and for its
   reasons: the button's markup says "Light theme" and aria-pressed="false", which is wrong for every
   reader the head script just resolved to light, and --plane is read off the stylesheet rather than
   restated here so the browser chrome cannot drift from the page. There is a computed value to read by
   now -- detail.css is a render-blocking link in the head, so it is parsed before this runs. The meta is
   looked up defensively: this file is one shared request, and a page that ever ships without the head
   block should lose the chrome colour, not the copy button and the two figures below. */
var toggle = document.getElementById("theme");
if (toggle) {
  var label = function () {
    var light = document.documentElement.dataset.theme === "light";
    toggle.textContent = light ? "Dark theme" : "Light theme";
    toggle.setAttribute("aria-pressed", light ? "true" : "false");
    var tc = document.getElementById("tc");
    var plane = getComputedStyle(document.documentElement).getPropertyValue("--plane").trim();
    if (tc && plane) tc.content = plane;
  };
  toggle.onclick = function () {
    var light = document.documentElement.dataset.theme !== "light";
    document.documentElement.dataset.theme = light ? "light" : "dark";
    /* The choice is the point: it used to last until the next navigation, so a reader who needs light
       re-picked it on every one of these 1,295 pages and again on every trip back to the atlas. */
    try { localStorage.setItem("theme", light ? "light" : "dark"); } catch (e) {}
    label();
  };
  label();
  /* Follow the OS live, but only for a reader who has not overridden it -- flipping someone out of a
     theme they explicitly chose because the sun went down is worse than not following at all. */
  try {
    matchMedia("(prefers-color-scheme: light)").addEventListener("change", function (ev) {
      if (localStorage.getItem("theme")) return;
      document.documentElement.dataset.theme = ev.matches ? "light" : "dark";
      label();
    });
  } catch (e) {}
}

/* Feature-detected rather than assumed, and the button stays hidden when the answer is no -- a button
   that fails on click is worse than no button. isSecureContext is part of the test because the API
   exists but always rejects on plain http, which is how anyone serving docs/ locally sees it. */
var copy = document.querySelector(".copy");
if (copy && navigator.clipboard && navigator.clipboard.writeText && window.isSecureContext) {
  copy.hidden = false;
  copy.onclick = function () {
    var cmd = document.getElementById(copy.dataset.for);
    navigator.clipboard.writeText(cmd.textContent).then(function () {
      copy.textContent = "Copied";
      setTimeout(function () { copy.textContent = "Copy"; }, 1400);
    });
  };
}

/* The star count and the last push.

   These are the only two facts on the page that change daily, and they are read from docs/data.json
   here instead of being written into the HTML by the generator. docs/ is committed verbatim on this
   deployment, so a star count in the markup means all 1,294 pages are rewritten in git every time the
   cron runs; reading them from a file that already changes every run costs the repository nothing.

   Failure is silent by design. The two spans are hidden until this succeeds, so a 404, an offline
   reader or a parse error leaves a page that is missing two figures rather than a page with a broken
   promise on it -- and every other fact on it was in the initial response. */
var root = document.documentElement.dataset.root || "";
var nwo = document.documentElement.dataset.nwo;
if (nwo && window.fetch) {
  fetch(root + "data.json").then(function (r) {
    return r.ok ? r.json() : Promise.reject(r.status);
  }).then(function (d) {
    var i = d.cols.indexOf("nwo"), s = d.cols.indexOf("stars"), p = d.cols.indexOf("pushed");
    var row = d.rows.find(function (x) { return x[i] === nwo; });
    if (!row) return;
    show("stars", row[s] ? "<b>" + row[s].toLocaleString() + "</b> stars" : "No stars recorded");
    if (row[p]) show("pushed", "last push <b>" + row[p] + "</b>");
    /* The snapshot the two figures above belong to. It is the single most volatile string in the
       dataset -- it changes on every run without exception -- so one copy of it per page would be
       1,294 rewritten files for one date, and it is also the qualifier without which the two numbers
       beside it are being presented as live when they are not. */
    if (d.snapshot) show("snap", "snapshot " + d.snapshot);
  }).catch(function () {});
}

function show(id, html) {
  var el = document.getElementById(id);
  if (!el) return;
  el.innerHTML = html;
  el.className = "live on";
}
