// The Atlas admin panel. Imported by `atlas-site.js` when the address ends in `=admin1337` (see the header
// of that file for every form the tail can take), on any page of the site. A reader who never types it
// never fetches this file.
//
// NOT A SECURITY BOUNDARY. A static site has no server to check anything against: every switch here is a
// value in the reader's own localStorage, and the string that opens it is in plain sight in atlas-site.js.
// It keeps these controls out of the way; it does not keep anybody out.
//
// Three sections:
//   * Hidden themes. A theme in HIDDEN has a block in every stylesheet and an entry in every head script's
//     map like any other, but the head scripts refuse to wear it, and the Settings menu does not show its
//     button, until its id is in `atlas-unlock` (a comma list). Unlocking it here is the only way in.
//     Locking it again takes it back off a reader who is wearing it.
//   * Build status: the same answer the footer tags paint, with the run times and links, and a refresh
//     that skips the ten-minute cache.
//   * Archie, on the homepage only: a button that opens his own panel (`archie-admin.js`), which has a
//     control for everything he does.
//
// Non-modal, like Archie's: the page stays usable underneath. Escape closes it and focus goes back to
// wherever it was when the panel opened.

export const HIDDEN = [
  {id: "holo", name: "Holo",
   blurb: "Hairline grid, film grain and an iridescent light across the top. Clean lines, dark or light.",
   swatch: ["#07090F", "#A99BFF", "#7AD7FF"]},
];
const UNLOCK = "atlas-unlock";

let panel = null, back = null, timer = 0;

function unlocked() {
  try { return (localStorage.getItem(UNLOCK) || "").split(",").filter(Boolean); } catch (e) { return []; }
}

function setUnlocked(ids) {
  try {
    if (ids.length) localStorage.setItem(UNLOCK, ids.join(","));
    else localStorage.removeItem(UNLOCK);
  } catch (e) {}
}

function wear(skin) {
  document.documentElement.dataset.skin = skin;
  try { localStorage.setItem("atlas-skin", skin); } catch (e) {}
  // The browser chrome follows the page, as the Settings menu's own paint does.
  const plane = getComputedStyle(document.documentElement).getPropertyValue("--plane").trim();
  const tc = document.getElementById("tc");
  if (plane && tc) tc.content = plane;
  repaintSettings();
}

function repaintSettings() {
  if (typeof window.atlasPaintSettings === "function") window.atlasPaintSettings();
}

const CSS = `
#atlasadmin{position:fixed;right:12px;bottom:12px;z-index:60;width:min(360px,calc(100vw - 24px));
  max-height:calc(100vh - 24px);overflow:auto;padding:14px 14px 12px;border-radius:12px;
  background:var(--panel,var(--plane));backdrop-filter:var(--bdf,none);-webkit-backdrop-filter:var(--bdf,none);
  border:1px solid var(--grid);color:var(--ink);font:13px/1.45 var(--ui,system-ui,sans-serif);
  box-shadow:0 2px 6px rgba(0,0,0,.3),0 24px 56px -16px rgba(0,0,0,.7)}
#atlasadmin h2{display:flex;align-items:center;justify-content:space-between;margin:0 0 10px;
  font:600 12px/1 var(--mono,ui-monospace,monospace);letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
#atlasadmin h3{margin:14px 0 6px;font:600 11px/1 var(--mono,ui-monospace,monospace);letter-spacing:.08em;
  text-transform:uppercase;color:var(--muted)}
#atlasadmin .aa-x{min-width:32px;min-height:32px;border:1px solid transparent;border-radius:8px;
  background:none;color:var(--ink2);font:inherit;font-size:16px;letter-spacing:0;cursor:pointer}
#atlasadmin .aa-x:hover{border-color:var(--grid);color:var(--ink)}
#atlasadmin .aa-skin{display:grid;grid-template-columns:auto 1fr;gap:4px 10px;align-items:center;
  padding:10px;border:1px solid var(--grid);border-radius:10px;background:var(--band)}
#atlasadmin .aa-sw{display:inline-flex;width:34px;height:16px;border-radius:999px;overflow:hidden;border:1px solid var(--grid)}
#atlasadmin .aa-sw i{flex:1}
#atlasadmin .aa-skin b{font-weight:600}
#atlasadmin .aa-skin p{grid-column:1 / -1;margin:0;color:var(--ink2);font-size:12.5px}
#atlasadmin .aa-row{grid-column:1 / -1;display:flex;gap:6px;flex-wrap:wrap;margin-top:4px}
#atlasadmin .aa-b{min-height:32px;padding:0 12px;border-radius:8px;border:1px solid var(--grid);
  background:var(--plane);color:var(--ink);font:600 12px/1 var(--ui,system-ui,sans-serif);cursor:pointer}
#atlasadmin .aa-b:hover{border-color:var(--link)}
#atlasadmin .aa-b.aa-go{background:var(--bar);border-color:var(--bar);color:var(--onbar)}
#atlasadmin .aa-b[disabled]{opacity:.5;cursor:default}
#atlasadmin .aa-st{list-style:none;margin:0;padding:0;font:12px/1.3 var(--mono,ui-monospace,monospace)}
#atlasadmin .aa-st li{display:grid;grid-template-columns:10px 72px 1fr auto;gap:8px;align-items:center;padding:5px 2px;
  border-bottom:1px solid var(--grid)}
#atlasadmin .aa-st li:last-child{border-bottom:0}
#atlasadmin .aa-st a{color:var(--link)}
#atlasadmin .aa-st .aa-t{color:var(--muted)}
#atlasadmin .aa-d{width:7px;height:7px;border-radius:50%;background:var(--off)}
#atlasadmin [data-state=ok] .aa-d{background:var(--good);box-shadow:0 0 8px var(--good)}
#atlasadmin [data-state=bad] .aa-d{background:var(--warn);box-shadow:0 0 8px var(--warn)}
#atlasadmin [data-state=run] .aa-d{background:var(--link);box-shadow:0 0 8px var(--link)}
#atlasadmin .aa-msg{min-height:1.4em;margin:8px 0 0;color:var(--muted);font-size:12px}
`;

function el(tag, attrs = {}, ...kids) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "on") for (const [ev, fn] of Object.entries(v)) n.addEventListener(ev, fn);
    else if (k === "text") n.textContent = v;
    else if (v !== false && v != null) n.setAttribute(k, v === true ? "" : v);
  }
  for (const k of kids) if (k) n.append(k);
  return n;
}

function say(msg) {
  const m = panel && panel.querySelector(".aa-msg");
  if (m) m.textContent = msg;
}

function skinCard(t) {
  const isOpen = unlocked().includes(t.id);
  const wearing = document.documentElement.dataset.skin === t.id;
  const sw = el("span", {class: "aa-sw", "aria-hidden": "true"}, ...t.swatch.map((c) => el("i", {style: `background:${c}`})));
  const row = el("div", {class: "aa-row"});
  if (!isOpen) {
    row.append(el("button", {type: "button", class: "aa-b aa-go", "data-act": "unlock", on: {click: () => {
      setUnlocked([...new Set([...unlocked(), t.id])]);
      wear(t.id);
      say(`${t.name} is unlocked and on. It is in the Settings menu now, on every page.`);
      render();
    }}, text: `Unlock ${t.name}`}));
  } else {
    row.append(el("button", {type: "button", class: "aa-b aa-go", "data-act": "wear", disabled: wearing,
      on: {click: () => { wear(t.id); say(`Wearing ${t.name}.`); render(); }}, text: wearing ? "Wearing it" : `Wear ${t.name}`}));
    row.append(el("button", {type: "button", class: "aa-b", "data-act": "lock", on: {click: () => {
      setUnlocked(unlocked().filter((id) => id !== t.id));
      if (document.documentElement.dataset.skin === t.id) wear("graphite");
      say(`${t.name} is locked again and out of the Settings menu.`);
      render();
    }}, text: "Lock it away"}));
  }
  return el("div", {class: "aa-skin", "data-skin-card": t.id}, sw, el("b", {text: t.name}),
            el("p", {text: t.blurb}), row);
}

function statusList(site, v) {
  const ul = el("ul", {class: "aa-st"});
  const names = {"daily.yml": "daily", "weekly.yml": "weekly", "tests.yml": "tests"};
  for (const run of v.runs) {
    if (!run) { ul.append(el("li", {}, el("i", {class: "aa-d"}), el("span", {text: "?"}), el("span", {class: "aa-t", text: "could not ask GitHub"}), el("span"))); continue; }
    const [state, words] = site.verdict(run);
    const link = run.url ? el("a", {href: run.url, text: words}) : el("span", {text: words});
    ul.append(el("li", {"data-state": state}, el("i", {class: "aa-d"}), el("span", {text: names[run.wf] || run.wf}),
                 link, el("span", {class: "aa-t", text: run.at ? site.ago(run.at) : ""})));
  }
  const d = v.deployed;
  ul.append(el("li", {"data-state": d ? "ok" : ""}, el("i", {class: "aa-d"}), el("span", {text: "deployed"}),
               el("span", {text: d && d.sha ? d.sha : "unknown"}), el("span", {class: "aa-t", text: d ? site.ago(d.at) : ""})));
  return ul;
}

let site = null;

async function render() {
  if (!panel) return;
  const body = panel.querySelector(".aa-body");
  const keep = document.activeElement && panel.contains(document.activeElement) ? document.activeElement.dataset.act : null;
  body.replaceChildren(
    el("h3", {text: "Hidden themes"}),
    ...HIDDEN.map(skinCard),
    el("h3", {text: "Build status"}),
    el("div", {class: "aa-stw"}, el("p", {class: "aa-t", text: "Asking GitHub…"})),
    el("div", {class: "aa-row"}, el("button", {type: "button", class: "aa-b", "data-act": "refresh", on: {click: async () => {
      say("Refreshing…");
      await paintStatus(true);
      say("Up to date.");
    }}, text: "Refresh"}),
      el("a", {class: "aa-b", href: `https://github.com/${document.getElementById("btags")?.dataset.repo || "crazy54/awesome-agentic-atlas"}/actions`,
               style: "display:inline-flex;align-items:center;text-decoration:none", text: "All runs"})),
    ...(document.getElementById("archieadmin") ? [
      el("h3", {text: "Archie"}),
      el("div", {class: "aa-row"}, el("button", {type: "button", class: "aa-b", "data-act": "archie", on: {click: () => {
        close();
        document.getElementById("archieadmin").click();
      }}, text: "Open Archie's controls"}))] : []),
  );
  if (keep) body.querySelector(`[data-act="${keep}"]`)?.focus();
  paintStatus(false);
}

async function paintStatus(fresh) {
  const box = panel && panel.querySelector(".aa-stw");
  if (!box || !site) return;
  try { box.replaceChildren(statusList(site, await site.status({fresh}))); }
  catch (e) { box.replaceChildren(el("p", {class: "aa-t", text: "GitHub did not answer. The footer tags link to each workflow."})); }
}

function onKey(ev) {
  if (ev.key === "Escape") { ev.stopPropagation(); close(); }
}

export function open({trigger = null, api = null} = {}) {
  if (api) site = api;
  if (panel) { panel.querySelector(".aa-x").focus(); return; }
  if (!document.getElementById("atlasadmincss")) document.head.append(el("style", {id: "atlasadmincss", text: CSS}));
  back = trigger || document.activeElement;
  panel = el("section", {id: "atlasadmin", role: "dialog", "aria-modal": "false", "aria-labelledby": "atlasadminh"},
    el("h2", {id: "atlasadminh"}, el("span", {text: "Admin"}),
       el("button", {type: "button", class: "aa-x", "aria-label": "Close the admin panel", on: {click: close}, text: "×"})),
    el("div", {class: "aa-body"}),
    el("p", {class: "aa-msg", role: "status"}));
  panel.addEventListener("keydown", onKey);
  document.body.append(panel);
  render();
  panel.querySelector(".aa-x").focus();
  // The run times say "3m ago"; keep them true while the panel stays open.
  timer = setInterval(() => paintStatus(false), 60000);
}

export function close() {
  if (!panel) return;
  clearInterval(timer);
  panel.remove();
  panel = null;
  if (back && back.isConnected && typeof back.focus === "function") back.focus();
  back = null;
}

export function isOpen() { return !!panel; }
