/* Written by scripts/22_detail.py. Shared by every page under docs/repo/.

   Four jobs, none of which the page needs in order to be complete: the theme toggle, the copy button,
   the repository reader, and the two figures that are deliberately not in the HTML. */
"use strict";

var root = document.documentElement.dataset.root || "";
var nwo = document.documentElement.dataset.nwo;

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

/* The repository reader.

   Nothing fetched here is committed to the atlas. GitHub's Contents endpoint renders the preferred
   README and any selected Markdown file with the same markup engine GitHub uses on a repository page;
   its Trees endpoint supplies one file list so SKILL.md and nested documentation are discoverable. Two
   requests open the reader, subsequent requests happen only when the reader picks another file, and
   both rendered and source bodies are cached for the rest of this page visit.

   The returned HTML is already sanitised by GitHub. `safeFragment` still strips active document
   elements and event attributes before it enters this page, because a boundary is worth enforcing at
   the boundary. It also resolves repository-relative links and images, which otherwise point back into
   the atlas's /repo/ tree when this page is served from GitHub Pages. */
var reader = document.querySelector(".reader");
if (reader && nwo && window.fetch) {
  var fileSelect = document.getElementById("source-file");
  var renderedTab = document.getElementById("rendered-tab");
  var sourceTab = document.getElementById("source-tab");
  var renderedView = document.getElementById("rendered-view");
  var sourceView = document.getElementById("source-view");
  var readerStatus = document.getElementById("reader-status");
  var readerNote = document.getElementById("reader-note");
  var openSource = document.getElementById("open-source");
  var apiBase = "https://api.github.com/repos/" + nwo;
  var repoBase = "https://github.com/" + nwo;
  var renderedCache = Object.create(null);
  var sourceCache = Object.create(null);
  var currentPath = "__readme";
  var currentMode = "rendered";
  var requestNumber = 0;
  var markdownLimit = 200;
  var maxMarkdownBytes = 1000000;

  renderedTab.onclick = function () { setReaderMode("rendered"); };
  sourceTab.onclick = function () { setReaderMode("source"); };
  fileSelect.onchange = function () {
    currentPath = fileSelect.value;
    currentMode = "rendered";
    paintTabs();
    updateSourceLink();
    loadRendered(currentPath);
  };

  loadPreferredReadme();
  loadMarkdownFiles();

  function github(path, accept) {
    return fetch(apiBase + path, {headers: {Accept: accept}}).then(function (response) {
      if (response.ok) return response;
      var error = new Error("GitHub returned " + response.status);
      error.status = response.status;
      throw error;
    });
  }

  function encodedPath(path) {
    return path.split("/").map(encodeURIComponent).join("/");
  }

  function contentEndpoint(path) {
    return path === "__readme" ? "/readme" : "/contents/" + encodedPath(path);
  }

  function loadPreferredReadme() {
    var ticket = ++requestNumber;
    setReaderStatus("Loading the project’s README…");
    github("/readme", "application/vnd.github.html+json")
      .then(function (response) { return response.text(); })
      .then(function (markup) {
        renderedCache.__readme = markup;
        if (currentPath !== "__readme") renderedCache[currentPath] = markup;
        if (ticket !== requestNumber || currentMode !== "rendered") return;
        showRendered(markup, currentPath);
      })
      .catch(function (error) {
        if (ticket === requestNumber) showReaderError(error);
      });
  }

  function loadMarkdownFiles() {
    github("/git/trees/HEAD?recursive=1", "application/vnd.github+json")
      .then(function (response) { return response.json(); })
      .then(function (data) {
        var all = (data.tree || []).filter(function (entry) {
          return entry.type === "blob" && /\.md$/i.test(entry.path) &&
            (!entry.size || entry.size <= maxMarkdownBytes);
        }).map(function (entry) { return entry.path; });
        all.sort(function (a, b) {
          return fileRank(a) - fileRank(b) || pathDepth(a) - pathDepth(b) ||
            a.localeCompare(b, undefined, {sensitivity: "base"});
        });

        var readme = all.find(function (path) { return /^readme(?:\.[^.]+)?\.md$/i.test(path); }) ||
          all.find(function (path) { return /(^|\/)readme(?:\.[^.]+)?\.md$/i.test(path); });
        if (readme && currentPath === "__readme") {
          currentPath = readme;
          if (renderedCache.__readme) renderedCache[readme] = renderedCache.__readme;
        }

        var shown = all.slice(0, markdownLimit);
        fileSelect.replaceChildren();
        if (!shown.length) {
          addFileOption(fileSelect, "__readme", "README (preferred)");
          currentPath = "__readme";
        } else {
          var groups = ["Start here", "Skills & agent instructions", "Documentation", "Other Markdown"];
          groups.forEach(function (label) {
            var paths = shown.filter(function (path) { return fileGroup(path) === label; });
            if (label === "Start here" && !readme) paths.unshift("__readme");
            if (!paths.length) return;
            var group = document.createElement("optgroup");
            group.label = label;
            paths.forEach(function (path) {
              addFileOption(group, path, path === "__readme" ? "README (preferred)" : path);
            });
            fileSelect.appendChild(group);
          });
        }
        fileSelect.value = currentPath;
        fileSelect.disabled = false;
        updateSourceLink();
        var note = all.length + " Markdown file" + (all.length === 1 ? "" : "s") + " found";
        if (all.length > shown.length) note += "; showing the first " + shown.length;
        if (data.truncated) note += ". GitHub truncated this unusually large repository tree";
        readerNote.textContent = note + ". Files are loaded on demand and are not copied into the atlas.";
      })
      .catch(function () {
        fileSelect.replaceChildren();
        addFileOption(fileSelect, "__readme", "README (preferred)");
        fileSelect.disabled = true;
        readerNote.textContent = "The README can still be read here, but GitHub did not provide this " +
          "repository’s Markdown file list.";
      });
  }

  function addFileOption(parent, value, label) {
    var option = document.createElement("option");
    option.value = value;
    option.textContent = label;
    parent.appendChild(option);
  }

  function pathDepth(path) {
    return (path.match(/\//g) || []).length;
  }

  function fileRank(path) {
    var base = path.split("/").pop();
    if (/^readme(?:\.[^.]+)?\.md$/i.test(base)) return 0;
    if (/^skill\.md$/i.test(base)) return 1;
    if (/^(agents?|claude)\.md$/i.test(base)) return 2;
    if (/(^|\/)(skills?|agents?)(\/|$)/i.test(path)) return 3;
    if (/(^|\/)(docs?|documentation)(\/|$)/i.test(path)) return 4;
    return 5;
  }

  function fileGroup(path) {
    var rank = fileRank(path);
    if (rank === 0) return "Start here";
    if (rank <= 3) return "Skills & agent instructions";
    if (rank === 4) return "Documentation";
    return "Other Markdown";
  }

  function loadRendered(path) {
    if (renderedCache[path]) return showRendered(renderedCache[path], path);
    var ticket = ++requestNumber;
    setReaderStatus("Rendering " + displayPath(path) + "…");
    github(contentEndpoint(path), "application/vnd.github.html+json")
      .then(function (response) { return response.text(); })
      .then(function (markup) {
        renderedCache[path] = markup;
        if (ticket === requestNumber && currentMode === "rendered" && currentPath === path)
          showRendered(markup, path);
      })
      .catch(function (error) {
        if (ticket === requestNumber) showReaderError(error);
      });
  }

  function loadSource(path) {
    if (sourceCache[path] !== undefined) return showSource(sourceCache[path]);
    var ticket = ++requestNumber;
    setReaderStatus("Loading the source for " + displayPath(path) + "…");
    github(contentEndpoint(path), "application/vnd.github.raw+json")
      .then(function (response) { return response.text(); })
      .then(function (source) {
        sourceCache[path] = source;
        if (ticket === requestNumber && currentMode === "source" && currentPath === path)
          showSource(source);
      })
      .catch(function (error) {
        if (ticket === requestNumber) showReaderError(error);
      });
  }

  function setReaderMode(mode) {
    if (mode === currentMode && !readerStatus.hidden) return;
    currentMode = mode;
    paintTabs();
    if (mode === "source") loadSource(currentPath);
    else loadRendered(currentPath);
  }

  function paintTabs() {
    var rendered = currentMode === "rendered";
    renderedTab.classList.toggle("on", rendered);
    sourceTab.classList.toggle("on", !rendered);
    renderedTab.setAttribute("aria-pressed", rendered ? "true" : "false");
    sourceTab.setAttribute("aria-pressed", rendered ? "false" : "true");
  }

  function setReaderStatus(message) {
    reader.dataset.state = "loading";
    renderedView.hidden = true;
    sourceView.hidden = true;
    readerStatus.hidden = false;
    readerStatus.replaceChildren();
    var spinner = document.createElement("span");
    spinner.className = "loader";
    spinner.setAttribute("aria-hidden", "true");
    var text = document.createElement("span");
    text.textContent = message;
    readerStatus.append(spinner, text);
  }

  function showRendered(markup, path) {
    reader.dataset.state = "ready";
    readerStatus.hidden = true;
    sourceView.hidden = true;
    renderedView.replaceChildren(safeFragment(markup, path));
    renderedView.hidden = false;
    renderedView.scrollTop = 0;
  }

  function showSource(source) {
    reader.dataset.state = "ready";
    readerStatus.hidden = true;
    renderedView.hidden = true;
    sourceView.querySelector("code").textContent = source;
    sourceView.hidden = false;
    sourceView.scrollTop = 0;
    sourceView.scrollLeft = 0;
  }

  function showReaderError(error) {
    reader.dataset.state = "error";
    renderedView.hidden = true;
    sourceView.hidden = true;
    readerStatus.hidden = false;
    readerStatus.replaceChildren();
    var title = document.createElement("strong");
    title.textContent = error && error.status === 403 ? "GitHub’s preview limit was reached" :
      "This file could not be previewed";
    var explanation = document.createElement("span");
    explanation.textContent = error && error.status === 403 ?
      "GitHub limits anonymous file requests. The repository itself is still available." :
      "It may have moved, be too large, or no longer be public.";
    var link = document.createElement("a");
    link.href = openSource.href;
    link.target = "_blank";
    link.rel = "noopener";
    link.textContent = "Open it on GitHub →";
    readerStatus.append(title, explanation, link);
  }

  function displayPath(path) {
    return path === "__readme" ? "README" : path;
  }

  function updateSourceLink() {
    openSource.href = currentPath === "__readme" ? repoBase :
      repoBase + "/blob/HEAD/" + encodedPath(currentPath);
  }

  function safeFragment(markup, path) {
    var template = document.createElement("template");
    template.innerHTML = markup;
    var content = template.content;

    content.querySelectorAll("script,style,link,meta,base,iframe,object,embed,form,button,textarea,select," +
      "svg,math,video,audio")
      .forEach(function (element) { element.remove(); });
    content.querySelectorAll("*").forEach(function (element) {
      Array.from(element.attributes).forEach(function (attribute) {
        if (/^on/i.test(attribute.name) ||
            /^(style|srcdoc|srcset|poster|action|formaction|form|autofocus|name|xlink:href)$/i.test(attribute.name))
          element.removeAttribute(attribute.name);
      });
    });
    content.querySelectorAll("input").forEach(function (input) {
      if ((input.getAttribute("type") || "").toLowerCase() !== "checkbox") return input.remove();
      input.disabled = true;
    });

    var ids = Object.create(null);
    content.querySelectorAll("[id]").forEach(function (element, index) {
      var old = element.id;
      var clean = old.toLowerCase().replace(/[^a-z0-9_-]+/g, "-").replace(/^-|-$/g, "") || "part";
      var next = "source-" + clean + "-" + index;
      ids[old] = next;
      element.id = next;
    });

    content.querySelectorAll("a[href]").forEach(function (link) {
      var href = link.getAttribute("href") || "";
      if (href.charAt(0) === "#") {
        var target = href.slice(1);
        try { target = decodeURIComponent(target); } catch (_) {}
        link.setAttribute("href", ids[target] ? "#" + ids[target] : "#source-preview");
      } else {
        href = resolveRepositoryUrl(href, path, false);
        if (!href) return link.removeAttribute("href");
        link.href = href;
        link.target = "_blank";
        link.rel = "nofollow noopener noreferrer";
      }
    });

    content.querySelectorAll("img[src]").forEach(function (image) {
      var src = resolveRepositoryUrl(image.getAttribute("src") || "", path, true);
      if (!src) return image.remove();
      image.src = src;
      image.loading = "lazy";
      image.decoding = "async";
    });
    return content;
  }

  function resolveRepositoryUrl(value, path, media) {
    value = value.trim();
    if (!value || /^(javascript|vbscript|data):/i.test(value)) return "";
    if (/^(https?:|mailto:)/i.test(value)) return value;
    if (value.charAt(0) === "#") return value;

    var hash = "";
    var query = "";
    var hashAt = value.indexOf("#");
    if (hashAt >= 0) { hash = value.slice(hashAt); value = value.slice(0, hashAt); }
    var queryAt = value.indexOf("?");
    if (queryAt >= 0) { query = value.slice(queryAt); value = value.slice(0, queryAt); }
    var parts = value.charAt(0) === "/" || path === "__readme" ? [] : path.split("/").slice(0, -1);
    value.split("/").forEach(function (part) {
      if (!part || part === ".") return;
      if (part === "..") parts.pop();
      else parts.push(part);
    });
    var resolved = parts.map(encodeURIComponent).join("/");
    var base = media ? "https://raw.githubusercontent.com/" + nwo + "/HEAD/" :
      repoBase + "/blob/HEAD/";
    return base + resolved + query + hash;
  }
}

/* The star count and the last push.

   These are the only two facts on the page that change daily, and they are read from a file here
   instead of being written into the HTML by the generator. docs/ is committed verbatim on this
   deployment, so a star count in the markup means all 1,294 pages are rewritten in git every time the
   cron runs.

   The file is docs/live.json, written by scripts/19c_live.py:

     {"snapshot": "<date>", "repos": {"<owner>/<name>": [stars, "<pushed>"]}}

   which is these three values for every repository and nothing else -- 21.8 KB gzipped. Until JFH-222
   this fetched docs/data.json, all eighteen columns of all 1,294 rows at 162.5 KB gzipped, and then
   scanned it for one row. Same two numbers, 7.5x fewer bytes, and an object lookup instead of a linear
   search through 1,294 arrays.

   Failure is silent by design. The three spans are hidden until this succeeds, so a 404, an offline
   reader or a parse error leaves a page that is missing two figures rather than a page with a broken
   promise on it -- and every other fact on it was in the initial response. */
if (nwo && window.fetch) {
  fetch(root + "live.json").then(function (r) {
    return r.ok ? r.json() : Promise.reject(r.status);
  }).then(function (d) {
    /* Array.isArray rather than a truth test. Every nwo contains a slash, so none of them can name an
       inherited property of Object.prototype and a plain lookup is in fact safe -- but a check that is
       exact rather than merely sufficient costs nothing, and this one also declines a sidecar whose
       shape has changed underneath the page instead of rendering "undefined stars". */
    var row = d.repos && d.repos[nwo];
    if (!Array.isArray(row)) return;
    show("stars", row[0] ? "<b>" + row[0].toLocaleString() + "</b> stars" : "No stars recorded");
    if (row[1]) show("pushed", "last push <b>" + row[1] + "</b>");
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
