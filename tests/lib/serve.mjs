// A static file server over `docs/`, on a port the OS chooses.
//
// Two of the four harnesses assert on the bytes in `docs/` as a browser sees them, which means those bytes
// have to come over HTTP: `file://` has no origin, so there is no service worker, no manifest scope and no
// `caches` API, and three quarters of pwa-check would have nothing to assert against.
//
// It serves under a path prefix rather than at the origin root, and that is the whole reason this is 90
// lines rather than one call to `python -m http.server`. Every URL in this site is relative -- the manifest
// is `manifest.webmanifest`, its scope is `./`, the worker is `sw.js`, `data.json` is `data.json` -- because
// the published site lives at `/<repo>/` on `<owner>.github.io` and an absolute path would be correct there
// and broken everywhere else. Served at the origin root, "the manifest scope carries the Pages path prefix"
// and "the worker's scope is the prefixed site, not the origin root" are both true by accident and would
// stay true if every relative URL in the page became absolute tomorrow. Served under a prefix they mean
// what they say.
//
// A directory URL without its trailing slash gets a 301, which is what GitHub Pages does and what `sw.js`
// has a branch for: a redirected navigation response must not be cached, and there is no way to exercise
// that branch against a server that does not redirect.
//
// WHAT IT DELIBERATELY DOES NOT MODEL: compression, and caching headers. Pages gzips and sends
// `max-age=600`; this sends the bytes as they sit on disk with `no-store`. The Lighthouse budget in
// `.github/workflows/lighthouse.yml` is where transfer size is measured and it says so at length -- byte
// budgets belong to the tool that compresses the same way the CDN does. `no-store` is chosen over a made-up
// `max-age` so that nothing here can pass because of a stale HTTP cache; the service worker's own caches are
// unaffected by it, which is what pwa-check is reading.
import {createServer} from "node:http";
import {createReadStream, statSync} from "node:fs";
import {join, normalize, extname} from "node:path";

// Long enough to cover what `docs/` holds, and no `application/octet-stream` default that would let a
// mistyped extension pass: an unknown type is served as `text/plain`, which a browser will refuse to run as
// script or parse as a manifest, so the harness fails loudly rather than subtly.
const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  // Not `application/json`. Chrome accepts either, but only this one is the registered type, and the
  // manifest is the one file here whose MIME is part of what pwa-check asserts.
  ".webmanifest": "application/manifest+json; charset=utf-8",
  ".xml": "application/xml; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
  ".woff2": "font/woff2",
  ".pdf": "application/pdf",
};

/**
 * Serve `root` under `prefix` on 127.0.0.1, on whatever port the OS hands out.
 *
 * `listen(0)` rather than a number, because a number is a guess about a machine this code has never seen.
 * The three harnesses this replaces hardcoded 9333 and 9334, which works until something else on the
 * machine has one -- and the failure mode of a port collision is a harness that connects to somebody
 * else's process and reports nonsense, or a previous session killing a PID that was not its own.
 *
 * @returns {Promise<{origin: string, port: number, close: () => Promise<void>}>} `origin` ends in a slash,
 *   so a harness can concatenate a relative path onto it.
 */
export async function serve(root, prefix = "/awesome-agentic-atlas/") {
  const sockets = new Set();
  const server = createServer((req, res) => {
    const send = (code, body, type = "text/plain; charset=utf-8", extra = {}) => {
      res.writeHead(code, {"content-type": type, "cache-control": "no-store", ...extra});
      res.end(body);
    };
    let path;
    try { path = decodeURIComponent(new URL(req.url, "http://127.0.0.1").pathname); }
    catch { return send(400, "bad escape sequence in path\n"); }

    if (!path.startsWith(prefix))
      return send(404, `nothing is served outside ${prefix} -- this server models the Pages ` +
                       `path prefix, so every URL needs it\n`);

    const rel = normalize(path.slice(prefix.length)).replace(/^([\\/]|\.\.[\\/])+/, "");
    let file = join(root, rel);
    let st;
    try { st = statSync(file); } catch { st = null; }

    // A directory reached without its trailing slash is a redirect, not a page. Pages does this and `sw.js`
    // reads the redirect off the response, so serving the index directly here would hide that branch.
    if (st?.isDirectory() && !path.endsWith("/"))
      return send(301, "", "text/plain; charset=utf-8", {location: path + "/"});
    if (st?.isDirectory()) { file = join(file, "index.html"); try { st = statSync(file); } catch { st = null; } }

    if (!st?.isFile())
      return send(404, `404 ${path}\n`, "text/html; charset=utf-8");

    res.writeHead(200, {
      "content-type": TYPES[extname(file).toLowerCase()] || "text/plain; charset=utf-8",
      "content-length": st.size,
      "cache-control": "no-store",
    });
    if (req.method === "HEAD") return res.end();
    createReadStream(file).pipe(res);
  });

  // Tracked so `close()` is a close and not a wait. `server.close()` stops accepting and then blocks on
  // every live connection, and a browser keeps its keep-alive sockets open -- so without this the suite
  // hangs at the end for as long as the browser's idle timeout, having already passed.
  server.on("connection", (s) => { sockets.add(s); s.on("close", () => sockets.delete(s)); });

  await new Promise((res, rej) => {
    server.once("error", rej);
    server.listen(0, "127.0.0.1", res);
  });
  const {port} = server.address();
  return {
    port,
    origin: `http://127.0.0.1:${port}${prefix}`,
    close: () => new Promise((r) => {
      for (const s of sockets) s.destroy();
      server.close(() => r());
    }),
  };
}
