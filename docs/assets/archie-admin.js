// Archie's admin panel: a button for everything he does, for trying one without waiting for the director to
// get round to it. Loaded only when the footer's hidden trigger (`#archieadmin`, a faint "·" after the
// footer's last sentence) is used, or when the address has `?archie=admin`; see ADMIN_JS in
// `scripts/31_home.py`. A reader who does neither never fetches this file.
//
// NOT A SECURITY BOUNDARY. This is a static site with no server: the "hidden" in hidden panel means out of
// the way, not locked. Anybody can open it, and every button is something Archie already does by himself.
//
// Every button is one command of `window.archie` (see "Commands" at the top of `archie.js`), the same path the
// `?archie=` flags take, and nothing here reaches into the model. A button whose command cannot run now --
// the model is a poster under reduced motion or on a narrow screen, the rig is not up, a friend is already
// over -- is disabled, and says why in its title and in the panel's status line. The states are asked
// again twice a second while the panel is open, because most of them change as he moves.
//
// The friends are `friend:<id>` for each id in `archie-friends-data.js`'s ORDER, read here rather than by
// `archie.js`, so that their data loads with the panel and not for every reader.
//
// Escape closes it and focus goes back to the trigger. It is a non-modal dialog: the page stays usable
// under it, so that the reader can watch what a button does.
const V = new URL(import.meta.url).search;

const NAMES = {
  idle: "Idle", watch: "Watch", sit: "Sit", sleep: "Sleep", press: "Press", shrug: "Shrug",
  "walk-off": "Walk off / moonwalk", show: "Light show", chatter: "Chatter", poke: "Poke", quiet: "Stop everything",
};
const label = cmd => NAMES[cmd] || cmd.split(":")[1].replace(/-/g, " ");

const CSS = `
#archiepanel{position:fixed;right:16px;bottom:16px;z-index:60;width:min(560px,calc(100vw - 32px));
  max-height:min(78vh,720px);overflow:auto;box-sizing:border-box;padding:14px 16px 12px;
  background:var(--panel,var(--surface));color:var(--ink,#eef);border:1px solid var(--panel-b,var(--hair,#333));
  border-radius:var(--radius,10px);box-shadow:0 12px 40px rgba(0,0,0,.35);font:13px/1.35 system-ui,sans-serif}
#archiepanel h2{margin:0 0 2px;font-size:14px}
#archiepanel .why{margin:0 0 8px;color:var(--muted,#999);font-size:12px}
#archiepanel fieldset{border:0;border-top:1px solid var(--hair,#333);margin:8px 0 0;padding:6px 0 0}
#archiepanel legend{padding:0;color:var(--ink2,#ccd);font-size:11px;letter-spacing:.06em;text-transform:uppercase}
#archiepanel .row{display:flex;flex-wrap:wrap;gap:6px}
#archiepanel button{font:inherit;min-height:32px;padding:4px 10px;border-radius:999px;cursor:pointer;
  color:var(--ink,#eef);background:transparent;border:1px solid var(--panel-b,var(--hair,#444))}
#archiepanel button:hover:not(:disabled){border-color:var(--ac,var(--link,#8af))}
#archiepanel button:focus-visible{outline:2px solid var(--link,var(--ac,#8af));outline-offset:2px}
#archiepanel button:disabled{opacity:.45;cursor:not-allowed;text-decoration:line-through}
#archiepanel button[data-cmd=quiet]{border-color:var(--accent-coral,#e77)}
#archiepanel .top{display:flex;justify-content:space-between;align-items:start;gap:8px}
#archiepanel [data-close]{min-height:28px;padding:2px 9px}
#archiepanel output{display:block;margin-top:8px;color:var(--muted,#999);font:12px/1.3 var(--mono,monospace)}
`;

let panel = null, opener = null, poll = 0;

const groups = async () => {
  // `?archie=admin` can open the panel before archie.js, a module script and so deferred, has run; every
  // module has by `load`.
  if (!window.archie && document.readyState !== "complete")
    await new Promise(r => addEventListener("load", r, {once: true}));
  const all = window.archie ? window.archie.list() : [];
  let friends = [];
  try { friends = (await import(`./archie-friends-data.js${V}`)).ORDER.map(id => "friend:" + id); } catch {}
  const pick = f => all.filter(f);
  return [
    ["Dances", pick(c => c.startsWith("dance:"))],
    ["Acts", pick(c => !c.includes(":") && !["chatter", "poke", "quiet"].includes(c))],
    ["Pranks", pick(c => c.startsWith("prank:"))],
    ["Friends", friends],
    ["Talk", pick(c => c === "chatter" || c === "poke")],
    ["Rig", pick(c => c.startsWith("cue:"))],
    ["Stop", pick(c => c === "quiet")],
  ].filter(([, cmds]) => cmds.length);
};

// Every button's state, from `can()`; the status line says why the first disabled one is, for readers who
// cannot see a title.
const refresh = () => {
  if (!panel) return;
  const why = new Set();
  for (const b of panel.querySelectorAll("button[data-cmd]")) {
    const no = window.archie ? window.archie.can(b.dataset.cmd) : "Archie's script has not run";
    b.disabled = !!no;
    b.title = no || "";
    if (no) why.add(no);
  }
  panel.querySelector(".why").textContent = why.size ? "Greyed out: " + [...why].join("; ") + "." :
    "Everything can run now.";
};

const fire = async b => {
  const out = panel.querySelector("output"), cmd = b.dataset.cmd;
  let ok = false;
  try { ok = await window.archie.run(cmd); } catch (e) { console.warn("Archie admin:", e); }
  out.textContent = `${cmd}: ${ok ? "sent" : "not taken"}`;
  document.dispatchEvent(new CustomEvent("archie:admin", {detail: {cmd, ok: !!ok}}));
  refresh();
};

export function close() {
  if (!panel) return;
  clearInterval(poll);
  panel.remove(); panel = null;
  removeEventListener("keydown", onKey, true);
  if (opener) { opener.setAttribute("aria-expanded", "false"); opener.focus(); }
}

const onKey = e => { if (e.key === "Escape" && panel) { e.stopPropagation(); close(); } };

export async function open(trigger) {
  opener = trigger || null;
  if (panel) { panel.querySelector("button").focus(); return panel; }
  if (!document.getElementById("archieadmincss")) {
    const st = document.createElement("style");
    st.id = "archieadmincss"; st.textContent = CSS;
    document.head.append(st);
  }
  panel = document.createElement("div");
  panel.id = "archiepanel";
  panel.setAttribute("role", "dialog");
  panel.setAttribute("aria-labelledby", "archiepaneltitle");
  panel.innerHTML = `<div class="top"><div><h2 id="archiepaneltitle">Archie, by hand</h2>
    <p class="why" aria-live="polite"></p></div><button type="button" data-close aria-label="Close">&times;</button></div>`;
  const built = panel;
  for (const [title, cmds] of await groups()) {
    if (built !== panel) return null;              // closed while the friends' names loaded
    const fs = document.createElement("fieldset"), lg = document.createElement("legend"), row = document.createElement("div");
    lg.textContent = title; row.className = "row";
    for (const cmd of cmds) {
      const b = document.createElement("button");
      b.type = "button"; b.dataset.cmd = cmd; b.textContent = label(cmd);
      row.append(b);
    }
    fs.append(lg, row); panel.append(fs);
  }
  panel.append(document.createElement("output"));
  panel.addEventListener("click", e => {
    const b = e.target.closest("button");
    if (!b || b.disabled) return;
    if (b.hasAttribute("data-close")) close(); else fire(b);
  });
  document.body.append(panel);
  addEventListener("keydown", onKey, true);
  if (opener) opener.setAttribute("aria-expanded", "true");
  refresh();
  poll = setInterval(refresh, 500);
  panel.querySelector("[data-close]").focus();
  return panel;
}
