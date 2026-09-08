// The repository reader is asynchronous UI around third-party data, so neither the deterministic tree
// test nor a static text scan can prove it becomes readable. This opens a real detail page in Chromium
// and fulfils its GitHub API requests at the browser boundary. The fixture is stable, exercises GitHub's
// rendered and raw media types, and never spends the anonymous API quota the production reader uses.
//
//   node tests/detail-preview-check.mjs <chrome-binary> <origin>
import {mkdirSync, writeFileSync} from "node:fs";
import {tmpdir} from "node:os";
import {fileURLToPath} from "node:url";
import {join} from "node:path";
import {launch} from "./lib/browser.mjs";

const ROOT = fileURLToPath(new URL("..", import.meta.url));
const BIN = process.argv[2], ORIGIN = process.argv[3];
if (!BIN || !ORIGIN) {
  console.log("usage: node tests/detail-preview-check.mjs <chrome-binary> <origin>");
  process.exit(2);
}
const SHOTS = process.env.AAA_ARTIFACTS || join(ROOT, "build-tmp");
mkdirSync(SHOTS, {recursive: true});

const browser = await launch(BIN, process.env.AAA_TMP || tmpdir(), "detail-preview");
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
let ws, id = 0, sessionId;
const waiters = new Map();
const exceptions = [];
const send = (method, params = {}, session) => new Promise((resolve, reject) => {
  const call = ++id;
  waiters.set(call, {resolve, reject});
  ws.send(JSON.stringify({id: call, method, params, ...(session ? {sessionId: session} : {})}));
});

ws = new WebSocket(browser.wsUrl);
await new Promise((resolve) => ws.addEventListener("open", resolve, {once: true}));
ws.addEventListener("message", (event) => {
  const message = JSON.parse(event.data);
  if (message.id && waiters.has(message.id)) {
    const waiter = waiters.get(message.id);
    waiters.delete(message.id);
    message.error ? waiter.reject(new Error(message.error.message)) : waiter.resolve(message.result);
    return;
  }
  if (message.sessionId !== sessionId) return;
  if (message.method === "Runtime.exceptionThrown")
    exceptions.push(message.params.exceptionDetails.exception?.description ||
                    message.params.exceptionDetails.text);
  if (message.method === "Fetch.requestPaused") void fulfilGitHub(message.params);
});

const {targetId} = await send("Target.createTarget", {url: "about:blank"});
({sessionId} = await send("Target.attachToTarget", {targetId, flatten: true}));
const S = (method, params = {}) => send(method, params, sessionId);
await S("Page.enable");
await S("Runtime.enable");
await S("Fetch.enable", {patterns: [{urlPattern: "https://api.github.com/repos/*"}]});

const renderedReadme = `<div class="markdown-heading"><h1 id="user-content-reader-demo">Reader demo</h1></div>
<p>Rendered <strong>Markdown</strong> arrives before source. Read the <a href="docs/guide.md">guide</a>.</p>
<blockquote><p>A short decision-making note.</p></blockquote>
<pre><code><span class="pl-k">const</span> answer = <span class="pl-c1">42</span>;</code></pre>
<table><thead><tr><th>Feature</th><th>Ready</th></tr></thead><tbody><tr><td>Skills</td><td>Yes</td></tr></tbody></table>
<img src="docs/diagram.png" alt="Diagram" style="position:fixed" onerror="window.fixtureUnsafe=true">
<script>window.fixtureUnsafe=true</script>`;
const renderedSkill = `<div class="markdown-heading"><h1 id="user-content-review-skill">Review skill</h1></div>
<p>Use this skill to <strong>review a change</strong> before release.</p>
<h2 id="user-content-steps">Steps</h2><ol><li>Inspect</li><li>Verify</li></ol>`;
const rawReadme = "# Reader demo\n\nRendered **Markdown** arrives before source.\n";
const rawSkill = "# Review skill\n\nUse this skill to **review a change** before release.\n";
const tree = {truncated: false, tree: [
  {path: "README.md", type: "blob", size: rawReadme.length},
  {path: "skills/review/SKILL.md", type: "blob", size: rawSkill.length},
  {path: "AGENTS.md", type: "blob", size: 120},
  {path: "docs/guide.md", type: "blob", size: 240},
  {path: "notes.md", type: "blob", size: 180},
  {path: "archive/too-large.md", type: "blob", size: 1000001},
  {path: "src/index.js", type: "blob", size: 90},
]};

async function fulfilGitHub(params) {
  const url = new URL(params.request.url);
  const headers = params.request.headers || {};
  const accept = headers.Accept || headers.accept || "";
  let code = 200, type = "text/html; charset=utf-8", body = "";
  if (params.request.method === "OPTIONS") code = 204;
  else if (url.pathname.endsWith("/git/trees/HEAD")) {
    type = "application/json; charset=utf-8";
    body = JSON.stringify(tree);
  } else if (url.pathname.endsWith("/readme")) {
    body = accept.includes("raw") ? rawReadme : renderedReadme;
    type = accept.includes("raw") ? "text/plain; charset=utf-8" : type;
  } else if (url.pathname.endsWith("/contents/skills/review/SKILL.md")) {
    body = accept.includes("raw") ? rawSkill : renderedSkill;
    type = accept.includes("raw") ? "text/plain; charset=utf-8" : type;
  } else {
    code = 404;
    type = "application/json; charset=utf-8";
    body = JSON.stringify({message: "fixture has no " + url.pathname});
  }
  await S("Fetch.fulfillRequest", {
    requestId: params.requestId,
    responseCode: code,
    responseHeaders: [
      {name: "content-type", value: type},
      {name: "access-control-allow-origin", value: "*"},
      {name: "access-control-allow-headers", value: "accept"},
    ],
    body: Buffer.from(body).toString("base64"),
  });
}

const evalIn = async (expression) => {
  const result = await S("Runtime.evaluate", {expression, awaitPromise: true, returnByValue: true});
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.exception?.description ||
                                                result.exceptionDetails.text);
  return result.result.value;
};
const waitFor = async (expression, label) => {
  for (let i = 0; i < 100; i++) {
    if (await evalIn(expression)) return;
    await sleep(100);
  }
  throw new Error("timed out waiting for " + label);
};
const resize = (width, height) => S("Emulation.setDeviceMetricsOverride",
  {width, height, deviceScaleFactor: 1, mobile: width < 500});
const shot = async (name) => {
  // The DOM state changes inside a fetch continuation; two frames make the screenshot describe the
  // state the assertions just read rather than the previous compositor frame on a busy CI runner.
  await evalIn("new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))");
  const {data} = await S("Page.captureScreenshot", {format: "png"});
  writeFileSync(join(SHOTS, name + ".png"), Buffer.from(data, "base64"));
};

let pass = 0, fail = 0;
const ok = (name, condition, extra = "") => {
  condition ? pass++ : (fail++, console.log("FAIL " + name + (extra ? "  -- " + extra : "")));
};

await resize(1100, 900);
await S("Page.navigate", {url: ORIGIN + "repo/anthropics/skills/"});
await waitFor("document.querySelector('.reader')?.dataset.state === 'ready' && " +
              "document.querySelector('#rendered-view h1')?.textContent === 'Reader demo'", "rendered README");

const initial = await evalIn(`(() => {
  const reader = document.querySelector('.reader');
  const rendered = document.getElementById('rendered-view');
  const source = document.getElementById('source-view');
  const options = [...document.getElementById('source-file').options].map(o => o.value);
  const install = [...document.querySelectorAll('section h2')].find(h => h.textContent === 'Install').parentElement;
  const preview = document.getElementById('source-preview');
  const screenshot = [...document.querySelectorAll('section h2')].find(h => h.textContent === 'Screenshot').parentElement;
  const image = rendered.querySelector('img');
  return {
    renderedShown: !rendered.hidden, sourceHidden: source.hidden,
    statusHidden: getComputedStyle(document.getElementById('reader-status')).display === 'none',
    renderedPressed: document.getElementById('rendered-tab').getAttribute('aria-pressed'),
    options, order: !!(install.compareDocumentPosition(preview) & Node.DOCUMENT_POSITION_FOLLOWING) &&
                    !!(preview.compareDocumentPosition(screenshot) & Node.DOCUMENT_POSITION_FOLLOWING),
    unsafe: !!window.fixtureUnsafe || !!rendered.querySelector('script') || image?.hasAttribute('onerror') ||
            image?.hasAttribute('style'),
    image: image?.src || '', guide: rendered.querySelector('a')?.href || '',
    bodyFont: getComputedStyle(rendered).fontFamily,
    codeFont: getComputedStyle(rendered.querySelector('code')).fontFamily,
    colour: getComputedStyle(reader).getPropertyValue('--read-violet').trim(),
    content: rendered.innerText,
    hscroll: document.documentElement.scrollWidth - document.documentElement.clientWidth,
  };
})()`);
ok("the repository reader sits between install and screenshot", initial.order);
ok("rendered Markdown is visible by default and source is hidden",
   initial.renderedShown && initial.sourceHidden && initial.statusHidden && initial.renderedPressed === "true",
   JSON.stringify(initial));
ok("README, skill, agent and docs Markdown are discoverable in the picker",
   ["README.md", "skills/review/SKILL.md", "AGENTS.md", "docs/guide.md"].every(p => initial.options.includes(p)),
   initial.options.join(", "));
ok("non-Markdown and over-limit files stay out of the picker",
   !initial.options.includes("src/index.js") && !initial.options.includes("archive/too-large.md"));
ok("the rendered document carries readable body and monospace code fonts",
   /Charter|Sitka Text|Cambria/.test(initial.bodyFont) && /Cascadia Code|Consolas/.test(initial.codeFont),
   initial.bodyFont + " / " + initial.codeFont);
ok("the dark reader has its own violet accent", initial.colour === "#c4a7ff", initial.colour);
ok("repository-relative document links and images point back to source",
   initial.guide.includes("github.com/anthropics/skills/blob/HEAD/docs/guide.md") &&
   initial.image.includes("raw.githubusercontent.com/anthropics/skills/HEAD/docs/diagram.png"),
   initial.guide + " / " + initial.image);
ok("active markup and inline styling are removed before the preview is mounted", !initial.unsafe);
ok("the desktop detail page has no horizontal overflow", initial.hscroll <= 0, String(initial.hscroll));
await evalIn("document.getElementById('source-preview').scrollIntoView({block: 'start'})");
await shot("detail-reader-dark");

await evalIn(`(() => {
  const select = document.getElementById('source-file');
  select.value = 'skills/review/SKILL.md';
  select.dispatchEvent(new Event('change', {bubbles: true}));
})()`);
await waitFor("document.querySelector('#rendered-view h1')?.textContent === 'Review skill'", "rendered skill");
ok("choosing SKILL.md replaces the rendered document",
   (await evalIn("document.getElementById('rendered-view').innerText")).includes("review a change"));
ok("the file action follows the selected document",
   (await evalIn("document.getElementById('open-source').href")) ===
   "https://github.com/anthropics/skills/blob/HEAD/skills/review/SKILL.md");

await evalIn("document.getElementById('source-tab').click()");
await waitFor("!document.getElementById('source-view').hidden", "raw Markdown source");
const sourceState = await evalIn(`({
  raw: document.querySelector('#source-view code').textContent,
  sourcePressed: document.getElementById('source-tab').getAttribute('aria-pressed'),
  renderedHidden: document.getElementById('rendered-view').hidden
})`);
ok("source mode shows the exact Markdown for the selected skill",
   sourceState.raw === rawSkill && sourceState.sourcePressed === "true" && sourceState.renderedHidden,
   JSON.stringify(sourceState));

await evalIn("document.getElementById('theme').click(); document.getElementById('rendered-tab').click()");
await waitFor("!document.getElementById('rendered-view').hidden", "light rendered view");
const light = await evalIn(`({
  theme: document.documentElement.dataset.theme,
  colour: getComputedStyle(document.querySelector('.reader')).getPropertyValue('--read-violet').trim(),
  bg: getComputedStyle(document.querySelector('.reader')).backgroundColor
})`);
ok("the light theme gives the reader a distinct accessible palette",
   light.theme === "light" && light.colour === "#6d28d9" && light.bg !== "rgb(17, 24, 39)",
   JSON.stringify(light));
await evalIn("document.getElementById('source-preview').scrollIntoView({block: 'start'})");
await shot("detail-reader-light");

await resize(375, 812);
const mobile = await evalIn(`(() => {
  const reader = document.querySelector('.reader').getBoundingClientRect();
  const picker = document.querySelector('.file-picker').getBoundingClientRect();
  const chrome = document.querySelector('.reader-chrome').getBoundingClientRect();
  return {readerWidth: Math.round(reader.width), pickerWidth: Math.round(picker.width),
          chromeHeight: Math.round(chrome.height),
          hscroll: document.documentElement.scrollWidth - document.documentElement.clientWidth};
})()`);
ok("the phone toolbar wraps its file picker onto a useful full row",
   mobile.chromeHeight >= 90 && mobile.pickerWidth >= mobile.readerWidth - 24, JSON.stringify(mobile));
ok("the reader does not create sideways page scroll on a phone", mobile.hscroll <= 0, JSON.stringify(mobile));
await evalIn("document.getElementById('source-preview').scrollIntoView({block: 'start'})");
await shot("detail-reader-mobile");

ok("the page raised no browser exceptions", exceptions.length === 0, exceptions.join(" | "));
console.log(`\n${pass} passed, ${fail} failed`);
ws.close();
await browser.close();
process.exit(fail ? 1 : 0);
