/* Written by scripts/22_detail.py. Shared by every page under docs/repo/.

   Three jobs, none of which the page needs in order to be complete: the theme toggle, the copy button,
   and the two figures that are deliberately not in the HTML. */
"use strict";

/* Not a data fetch and not a framework: the light half of the theme is in detail.css and without a
   switch nothing on these pages can ever reach it. Same default as the site (dark) and the same
   unpersisted, one-tab scope, so the two surfaces behave alike. */
var toggle = document.getElementById("theme");
if (toggle) {
  toggle.onclick = function (e) {
    var light = document.documentElement.dataset.theme !== "light";
    document.documentElement.dataset.theme = light ? "light" : "dark";
    e.target.textContent = light ? "Dark theme" : "Light theme";
    e.target.setAttribute("aria-pressed", light ? "true" : "false");
  };
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
