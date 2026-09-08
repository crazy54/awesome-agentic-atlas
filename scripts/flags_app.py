"""A local-only, dependency-free control panel for ``config/app-flags.json``.

Run ``python scripts/flags_app.py``. The server binds only to 127.0.0.1, uses an unguessable write
token, rejects cross-origin writes, checks revisions to prevent stale tabs overwriting newer edits,
and delegates validation plus atomic replacement to ``app_flags.py``.
"""
from __future__ import annotations

import argparse
import json
import secrets
import subprocess
import sys
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import app_flags  # noqa: E402

HOST = "127.0.0.1"


def catalog() -> list[dict[str, object]]:
    values = app_flags.load(app_flags.DEFAULT_PATH)
    return [{"key": spec.key, "group": spec.group, "name": spec.name,
             "description": spec.description, "off_effect": spec.off_effect,
             "value": values[spec.key]} for spec in app_flags.SPECS]


def render_site() -> str:
    result = subprocess.run([sys.executable, str(HERE / "apply_flags.py")], cwd=ROOT,
                            capture_output=True, text=True, encoding="utf-8", errors="replace")
    output = (result.stdout + result.stderr).strip()
    if result.returncode:
        raise RuntimeError(output or f"apply_flags.py exited {result.returncode}")
    return output


PAGE = r'''<!doctype html>
<html lang="en" data-theme="dark"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Atlas application flags</title>
<style>
:root{color-scheme:dark;--bg:#090b12;--panel:#111522;--panel2:#171c2c;--line:#2b3450;
  --text:#eef2ff;--muted:#a7b1ca;--on:#5ee6a8;--off:#ff829c;--violet:#a78bfa;
  --blue:#62c7ff;--shadow:0 22px 70px #0008;font-family:Inter,Aptos,"Segoe UI",sans-serif}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 15% -10%,#282052 0,transparent 35%),
  radial-gradient(circle at 90% 5%,#083a4b 0,transparent 30%),var(--bg);color:var(--text);min-height:100vh}
.wrap{width:min(1040px,calc(100% - 32px));margin:auto}.hero{padding:54px 0 26px}.eyebrow{margin:0 0 9px;
  color:var(--blue);font:700 11px/1.2 "Cascadia Code",Consolas,monospace;letter-spacing:.14em;text-transform:uppercase}
h1{font-size:clamp(31px,6vw,54px);line-height:1.02;letter-spacing:-.04em;margin:0;max-width:760px}h1 span{color:var(--violet)}
.intro{max-width:760px;color:var(--muted);font-size:17px;line-height:1.55;margin:18px 0 0}.summary{display:flex;gap:9px;
  flex-wrap:wrap;margin:22px 0 0}.pill{border:1px solid var(--line);background:#0b0e18aa;border-radius:999px;padding:7px 11px;
  color:var(--muted);font:700 11px/1 "Cascadia Code",Consolas,monospace}.pill b{color:var(--text)}
.group{margin:26px 0 38px}.group h2{font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);
  margin:0 0 11px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.flag{display:grid;
  grid-template-columns:1fr auto;gap:14px;border:1px solid var(--line);background:linear-gradient(145deg,var(--panel2),var(--panel));
  border-radius:14px;padding:18px;box-shadow:0 1px 0 #ffffff08 inset;transition:border-color .15s,transform .15s}.flag:hover{border-color:#465477}
.flag.changed{border-color:var(--violet);transform:translateY(-1px)}.flag h3{margin:0 0 7px;font-size:17px;letter-spacing:-.015em}
.flag p{margin:0;color:var(--muted);font-size:13px;line-height:1.48}.flag .off-note{margin-top:8px;color:#8490ac;font-size:12px}
.key{display:block;color:#707d9c;font:600 10px/1.2 "Cascadia Code",Consolas,monospace;margin-top:12px;overflow-wrap:anywhere}
.switch{appearance:none;align-self:start;width:92px;border:1px solid currentColor;border-radius:10px;padding:10px 8px;background:#15101a;
  color:var(--off);font:800 11px/1.1 "Cascadia Code",Consolas,monospace;cursor:pointer;text-align:center;box-shadow:none}
.switch[aria-checked="true"]{color:var(--on);background:#0d1d1a}.switch .num{display:block;font-size:21px;margin-bottom:3px}
.switch:focus-visible,button:focus-visible{outline:3px solid var(--blue);outline-offset:3px}.dock{position:sticky;bottom:0;z-index:4;
  border-top:1px solid var(--line);background:#090b12e8;backdrop-filter:blur(16px);padding:13px 0}.dockin{display:flex;align-items:center;gap:10px}
.status{color:var(--muted);font-size:13px;margin-right:auto}.status.good{color:var(--on)}.status.bad{color:var(--off)}
.action{border:1px solid var(--line);border-radius:9px;background:var(--panel2);color:var(--text);font-weight:750;padding:10px 14px;cursor:pointer}
.action.primary{background:var(--violet);border-color:var(--violet);color:#100b1e}.action:disabled{opacity:.42;cursor:not-allowed}
.log{display:none;white-space:pre-wrap;max-height:170px;overflow:auto;background:#060810;border:1px solid var(--line);border-radius:10px;
  color:#b7c3df;padding:12px;font:11px/1.45 "Cascadia Code",Consolas,monospace;margin:0 0 18px}.log.on{display:block}
@media(max-width:720px){.hero{padding-top:34px}.grid{grid-template-columns:1fr}.flag{padding:15px}.dockin{flex-wrap:wrap}.status{width:100%}
  .action{flex:1;padding-inline:8px}.switch{width:82px}}
</style></head><body><div class="wrap hero">
<p class="eyebrow">Local control panel · build-time kill switches</p><h1>Atlas application <span>flags</span></h1>
<p class="intro">Every value is one bit and every effect is explicit. <b>1 means ON.</b> <b>0 means OFF / DISABLED.</b>
Save atomically, then render the exact configuration readers will receive.</p>
<div class="summary"><span class="pill"><b id="on-count">—</b> ON</span><span class="pill"><b id="off-count">—</b> OFF</span>
<span class="pill"><b id="change-count">0</b> unsaved changes</span></div></div>
<main class="wrap" id="flags" aria-live="polite"></main><div class="wrap"><pre class="log" id="log"></pre></div>
<div class="dock"><div class="wrap dockin"><span class="status" id="status">Loading flags…</span>
<button class="action" id="reload" type="button">Discard &amp; reload</button>
<button class="action" id="save" type="button" disabled>Save values only</button>
<button class="action primary" id="render" type="button" disabled>Save &amp; render site</button></div></div>
<script>
const TOKEN="__TOKEN__";let revision="",initial={},values={},busy=false;
const el=id=>document.getElementById(id), esc=s=>String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
function changed(){return Object.keys(values).filter(k=>values[k]!==initial[k])}
function counts(){const n=Object.values(values).filter(Boolean).length,c=changed();el("on-count").textContent=n;el("off-count").textContent=Object.keys(values).length-n;
 el("change-count").textContent=c.length;el("save").disabled=el("render").disabled=busy||!c.length;
 document.querySelectorAll(".flag").forEach(card=>card.classList.toggle("changed",c.includes(card.dataset.key)))}
function switchMarkup(f){return `<button class="switch" type="button" role="switch" data-key="${esc(f.key)}" aria-checked="${f.value===1}">
 <span class="num">${f.value}</span><span>${f.value===1?"ON":"OFF"}</span></button>`}
async function load(){busy=true;buttons();setStatus("Loading flags…","");try{const r=await fetch("/api/flags",{cache:"no-store"}),d=await r.json();if(!r.ok)throw Error(d.error||r.statusText);
 revision=d.revision;initial={};values={};const groups=new Map;for(const f of d.flags){initial[f.key]=values[f.key]=f.value;if(!groups.has(f.group))groups.set(f.group,[]);groups.get(f.group).push(f)}
 el("flags").innerHTML=[...groups].map(([name,flags])=>`<section class="group"><h2>${esc(name)}</h2><div class="grid">${flags.map(f=>`<article class="flag" data-key="${esc(f.key)}"><div><h3>${esc(f.name)}</h3><p>${esc(f.description)}</p><p class="off-note"><b>When OFF:</b> ${esc(f.off_effect)}</p><code class="key">${esc(f.key)}</code></div>${switchMarkup(f)}</article>`).join("")}</div></section>`).join("");
 document.querySelectorAll(".switch").forEach(b=>b.onclick=()=>toggle(b));setStatus("Saved configuration loaded.","good");}catch(e){setStatus(e.message,"bad")}finally{busy=false;buttons();counts()}}
function toggle(b){const k=b.dataset.key;values[k]=values[k]?0:1;b.setAttribute("aria-checked",values[k]===1);b.querySelector(".num").textContent=values[k];b.lastElementChild.textContent=values[k]?"ON":"OFF";counts();setStatus(changed().length?"Changes are local until you save.":"No unsaved changes.","")}
function buttons(){el("reload").disabled=busy;counts()}
function setStatus(t,c){el("status").textContent=t;el("status").className="status "+c}
async function save(render){busy=true;buttons();el("log").classList.remove("on");setStatus(render?"Saving and rendering all pages…":"Saving values…","");try{const r=await fetch("/api/flags",{method:"POST",headers:{"Content-Type":"application/json","X-Atlas-Token":TOKEN},body:JSON.stringify({revision,values,render})}),d=await r.json();if(!r.ok)throw Error(d.error||r.statusText);
 revision=d.revision;initial={...values};counts();if(d.output){el("log").textContent=d.output;el("log").classList.add("on")}setStatus(render?"Saved and rendered into docs/. Review the git diff before deploying.":"Values saved. Render locally or let the build workflow apply them.","good");}catch(e){setStatus(e.message,"bad")}finally{busy=false;buttons()}}
el("reload").onclick=load;el("save").onclick=()=>save(false);el("render").onclick=()=>save(true);load();
</script></body></html>'''


class Handler(BaseHTTPRequestHandler):
    token = ""
    origin = ""

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"flags app: {fmt % args}")

    def reply(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(body)

    def json_reply(self, status: int, value: object) -> None:
        self.reply(status, json.dumps(value, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        if self.path == "/":
            self.reply(HTTPStatus.OK, PAGE.replace("__TOKEN__", self.token).encode("utf-8"), "text/html; charset=utf-8")
        elif self.path == "/api/flags":
            try:
                self.json_reply(HTTPStatus.OK, {"revision": app_flags.revision(), "flags": catalog()})
            except app_flags.FlagError as exc:
                self.json_reply(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
        else:
            self.json_reply(HTTPStatus.NOT_FOUND, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        if self.path != "/api/flags":
            self.json_reply(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return
        if self.headers.get("X-Atlas-Token") != self.token or self.headers.get("Origin") not in (None, self.origin):
            self.json_reply(HTTPStatus.FORBIDDEN, {"error": "write rejected; reload the local Flags app"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 64 * 1024:
                raise app_flags.FlagError("invalid request size")
            request = json.loads(self.rfile.read(length).decode("utf-8"))
            if type(request) is not dict or set(request) != {"revision", "values", "render"}:
                raise app_flags.FlagError("the save request has an unexpected shape")
            if type(request["render"]) is not bool:
                raise app_flags.FlagError("render must be true or false")
            new_revision = app_flags.write(request["values"], request["revision"])
            output = render_site() if request["render"] else ""
            self.json_reply(HTTPStatus.OK, {"revision": new_revision, "output": output})
        except json.JSONDecodeError:
            self.json_reply(HTTPStatus.BAD_REQUEST, {"error": "request body is not valid JSON"})
        except app_flags.FlagError as exc:
            status = HTTPStatus.CONFLICT if "changed after" in str(exc) else HTTPStatus.BAD_REQUEST
            self.json_reply(status, {"error": str(exc)})
        except RuntimeError as exc:
            self.json_reply(HTTPStatus.INTERNAL_SERVER_ERROR,
                            {"error": "Flags were saved, but rendering failed:\n" + str(exc)})


def main() -> None:
    parser = argparse.ArgumentParser(description="Edit Awesome Agentic Atlas application flags")
    parser.add_argument("--port", type=int, default=0, help="local port (default: choose a free port)")
    parser.add_argument("--no-open", action="store_true", help="do not open the browser automatically")
    args = parser.parse_args()
    token = secrets.token_urlsafe(32)
    server = ThreadingHTTPServer((HOST, args.port), Handler)
    url = f"http://{HOST}:{server.server_port}"
    Handler.token = token
    Handler.origin = url
    print(f"Atlas Flags app: {url}")
    print("Bound to this computer only. Press Ctrl+C to stop.")
    if not args.no_open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nFlags app stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
