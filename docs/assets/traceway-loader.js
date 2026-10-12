// Starts Traceway telemetry on the live site, and does nothing anywhere else. Hand-maintained, like the rest of
// docs/assets: no generator writes it. Every page loads it with `defer`, last of three, after the vendored
// traceway-1.2.1.js (@tracewayapp/frontend, unmodified) and web-vitals-6.2.3.js (web-vitals, unmodified), whose
// globals it reads; `telemetry()` in scripts/19_pages.py writes the three tags, and its comment says why.
//
// Nothing secret is committed. The connection string is fetched at run time from blog.jeremyfhall.com, and the
// data goes to the owner's self-hosted Traceway. The hostname check comes first, so a fork, a `file://` clone,
// a `python -m http.server` and every harness in tests/ (served from 127.0.0.1) send nothing at all. Every
// failure is silent: telemetry being down must never be something a reader can see.
//
// `mask()` marks every form field, including fields added later, so the replay ignores keystrokes in them.
// That is narrower than it sounds. The SDK starts rrweb with its defaults, which mask only password values,
// so a field's text still appears in the full-page snapshots the replay takes at the start and every 30 s.
// Navigation capture also records the whole URL, hash included. The root README says all of this in plain
// words, under "What the site records".
//
// A classic script in ES5, like repo/detail.js, so a browser too old for the SDK fails nowhere it can be seen.
(function () {
  'use strict';
  var HOST = 'aaa.jeremyfhall.com';
  var SITE = 'aaa';
  if (window.location.hostname !== HOST || window.__jfhTelemetryStarted || !window.Traceway || !window.fetch) return;
  window.__jfhTelemetryStarted = true;
  function mask() {
    var fields = document.querySelectorAll('input, textarea, [contenteditable="true"]');
    for (var i = 0; i < fields.length; i++) fields[i].classList.add('rr-mask', 'rr-ignore');
  }
  mask();
  if (window.MutationObserver) new MutationObserver(mask).observe(document.documentElement, { childList: true, subtree: true });
  window.fetch('https://blog.jeremyfhall.com/api/telemetry-config?site=' + SITE)
    .then(function (response) { return response.ok ? response.json() : null; })
    .then(function (config) {
      if (!config || !config.connectionString) return;
      var Traceway = window.Traceway;
      Traceway.init(config.connectionString, {
        recordAllSessions: true, sessionRecording: true, captureNavigation: true,
        captureNetwork: true, captureLogs: false, captureHttpServerErrors: true,
        version: 'atlas-site-2026-10-11'
      });
      Traceway.setAttribute('site', HOST);
      var report = function (metric) { Traceway.recordAction('performance', metric.name, { value: metric.value, rating: metric.rating }); };
      if (window.webVitals) ['onCLS', 'onINP', 'onLCP', 'onFCP', 'onTTFB'].forEach(function (name) { window.webVitals[name](report); });
      document.addEventListener('click', function (event) {
        var link = event.target && event.target.closest ? event.target.closest('a[href]') : null;
        if (link) Traceway.recordAction('navigation', 'link-click', { path: new URL(link.href, window.location.href).pathname });
      });
    })
    ['catch'](function () {});
}());
