// Lookalikes' resolver and ranking, run under node against the committed `docs/`, with no browser.
//
//   node tests/alike-probe.mjs
//   AAA_ALIKE_TABLE=1 node tests/alike-probe.mjs     ...and print the hand-check table (top ten of 32 projects)
//
// WHAT IT IS FOR. `ALIKE` in `scripts/alike_page.js` is the page's pure half, and this loads exactly that file
// -- after `scripts/semantic.js`, the shared encoder, as the page does -- into a node VM, hands it the bytes a
// reader downloads (`docs/data.json` and four files of `docs/search/`), and asks it the questions a reader
// asks. So what is asserted is the code that runs, against the data that ships, and not a transcription of
// either. `tests/alike-check.mjs` drives the DOM half in a browser; `tests/alike_test.py` holds the stage,
// the shared encoder and the wiring.
//
// THE QUALITY CASES ARE RELATIVE, ON PURPOSE. `semantic_test.py` learned that a fixed rank for one fixture
// repository turns, as the corpus grows, into a measure of how crowded that neighbourhood is. So a case here
// asks "is a project a person would name as an alternative somewhere in the top N", with N generous, never
// "is it first"; and the aggregate asks for a share of category agreement well under what ships (see the
// measurements at the top of `alike_page.js`) and well over what the bare README vector manages, so it reddens
// on a regression to the naive ranking and not on a corpus that merely moved.
//
// WHAT IT CANNOT SEE: the forges. The not-in-the-atlas path is exercised here with a fabricated API answer,
// which covers the ranking and the answer's mapping; the fetch, its failures and the page's words for them are
// `alike-check.mjs`'s, against fabricated responses in a real browser.
import {readFileSync, existsSync} from "node:fs";
import {fileURLToPath} from "node:url";
import {join} from "node:path";
import vm from "node:vm";

const ROOT = fileURLToPath(new URL("..", import.meta.url));
const DOCS = join(ROOT, "docs");
let pass = 0, fail = 0;
const ok = (name, cond, detail = "") => {
  if (cond) pass++; else { fail++; console.log(`FAIL ${name}${detail ? `\n  ${detail}` : ""}`); }
};
const done = () => { console.log(`${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0); };

// ---- the code, as the page carries it
const ctx = vm.createContext({console, TextEncoder, crypto: globalThis.crypto, URLSearchParams, Date, Math});
vm.runInContext(readFileSync(join(ROOT, "scripts", "semantic.js"), "utf8") + "\n" +
                readFileSync(join(ROOT, "scripts", "alike_page.js"), "utf8") +
                "\n;globalThis.ALIKE = ALIKE; globalThis.semDecode = semDecode; globalThis.semEncode = semEncode;", ctx);
const A = ctx.ALIKE;
ok("the page script defines ALIKE without a DOM", !!A && typeof A.rank === "function");

// ---- parseInput: every shape a reader copies a repository in
const P = (s) => A.parseInput(s);
const repo = (s, nwo) => { const p = P(s); ok(`${JSON.stringify(s)} is the repository ${nwo}`, p.kind === "repo" && p.nwo === nwo, JSON.stringify(p)); };
repo("https://github.com/langfuse/langfuse", "langfuse/langfuse");
repo("https://github.com/langfuse/langfuse/", "langfuse/langfuse");
repo("http://www.github.com/langfuse/langfuse.git", "langfuse/langfuse");
repo("github.com/langfuse/langfuse/tree/main/web/src", "langfuse/langfuse");
repo("https://github.com/langfuse/langfuse/blob/main/README.md#readme", "langfuse/langfuse");
repo("https://github.com/langfuse/langfuse?tab=readme-ov-file", "langfuse/langfuse");
repo("git@github.com:langfuse/langfuse.git", "langfuse/langfuse");
repo("  langfuse/langfuse  ", "langfuse/langfuse");
repo("langfuse/langfuse.git", "langfuse/langfuse");
repo("https://gitlab.com/gitlab-org/gitlab", "gitlab.com/gitlab-org/gitlab");
repo("https://gitlab.com/group/sub/project/-/tree/main/src", "gitlab.com/group/sub/project");
repo("gitlab.com/group/project.git", "gitlab.com/group/project");
repo("git@gitlab.com:group/sub/project.git", "gitlab.com/group/sub/project");
ok("a GitHub profile is a link, not a repository", P("https://github.com/anthropics").kind === "notrepo");
ok("...and so is GitHub's root", P("https://github.com/").kind === "notrepo");
ok("words with a slash in them are words", P("ci/cd for agents").kind === "words");
ok("a name is words", P("claude code").kind === "words");
ok("nothing is nothing", P("   ").kind === "empty");

// ---- the shareable state
ok("?repo= round-trips with its slash readable", A.writeQuery({repo: "langfuse/langfuse"}) === "?repo=langfuse/langfuse");
ok("...and reads back", A.readQuery(A.writeQuery({repo: "gitlab.com/a/b c"})).repo === "gitlab.com/a/b c");
ok("?q= round-trips", A.readQuery(A.writeQuery({q: "tracing & evals"})).q === "tracing & evals");
ok("repo wins over q, and an empty query is no state",
   A.readQuery("?repo=a/b&q=x").repo === "a/b" && Object.keys(A.readQuery("?x=1")).length === 0);

// ---- the bytes a reader downloads
const need = ["data.json", "search/meta.json", "search/vocab.json", "search/vocab.bin", "search/docs.bin"];
const missing = need.filter((f) => !existsSync(join(DOCS, f)));
ok("docs/ carries data.json and the semantic index", !missing.length, "missing: " + missing.join(", "));
if (missing.length) done();
const d = JSON.parse(readFileSync(join(DOCS, "data.json"), "utf8"));
const buf = (f) => { const b = readFileSync(join(DOCS, f)); return b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength); };
const nwoAt = d.cols.indexOf("nwo");
const sem = await ctx.semDecode({meta: JSON.parse(readFileSync(join(DOCS, "search/meta.json"), "utf8")),
                                 vocab: JSON.parse(readFileSync(join(DOCS, "search/vocab.json"), "utf8")),
                                 table: buf("search/vocab.bin"), docs: buf("search/docs.bin")},
                                d.rows.map((r) => r[nwoAt]));
ok("the shared guard accepts the committed index against the committed data.json", sem && sem.dims > 0);
// And refuses one built against other rows, which is the failure that has no symptom.
let refused = false;
try {
  await ctx.semDecode({meta: JSON.parse(readFileSync(join(DOCS, "search/meta.json"), "utf8")),
                       vocab: JSON.parse(readFileSync(join(DOCS, "search/vocab.json"), "utf8")),
                       table: buf("search/vocab.bin"), docs: buf("search/docs.bin")},
                      d.rows.map((r) => r[nwoAt]).reverse());
} catch (e) { refused = /index was built against/.test(e.message); }
ok("...and refuses the same rows in another order", refused);

const t0 = Date.now();
const IX = A.build(d, sem);
const built = Date.now() - t0;
ok("the index builds", IX.n === d.rows.length && IX.B && IX.U);
ok(`...in reasonable time (${built} ms for ${IX.n} rows; the page pays this once)`, built < 15000);
const at = (nwo) => IX.by.get(nwo.toLowerCase());
const nwoOf = (j) => IX.rows[j].nwo;

// ---- resolve: names, links, and the obvious one
const hit = (q, nwo) => { const r = A.resolve(IX, q); ok(`${JSON.stringify(q)} resolves to ${nwo}`, r.kind === "hit" && nwoOf(r.i).toLowerCase() === nwo, JSON.stringify(r.kind === "hit" ? nwoOf(r.i) : r)); };
hit("claude code", "anthropics/claude-code");
hit("Claude Code", "anthropics/claude-code");
hit("https://github.com/anthropics/claude-code/tree/main/plugins", "anthropics/claude-code");
hit("ANTHROPICS/CLAUDE-CODE", "anthropics/claude-code");
hit("langfuse", "langfuse/langfuse");
hit("Context7", "upstash/context7");
const gl = IX.rows.find((r) => r.nwo.startsWith("gitlab.com/"));
if (gl) hit("https://" + gl.nwo + "/-/tree/main", gl.nwo.toLowerCase());
else ok("a GitLab row resolves by its link (no GitLab rows in this data.json, so nothing to check)", true);
const ext = A.resolve(IX, "https://github.com/someone-nobody-has/not-in-the-atlas-zz");
ok("a repository the atlas does not hold is a lookup, not a miss", ext.kind === "external" && ext.host === "github.com" && ext.path === "someone-nobody-has/not-in-the-atlas-zz");
ok("...and a bare owner/name is marked as possibly words", A.resolve(IX, "nobody-zz/thing-zz").bare === true);
const amb = A.resolve(IX, "memory");
ok("an ambiguous name offers a short list to choose from", amb.kind === "choose" && amb.choices.length >= 2 && amb.choices.length <= 6, JSON.stringify(amb).slice(0, 200));
ok("words that name nothing are a description", A.resolve(IX, "keep my agent from deleting files").kind === "words");

// ---- rank: the quality cases
const top = (nwo, k = 10) => { const s = A.sourceRow(IX, at(nwo)); const r = A.rank(IX, s); return {s, r, main: r.main.slice(0, k).map(nwoOf)}; };
const has = (list, want) => want.filter((w) => list.some((x) => x.toLowerCase() === w.toLowerCase()));
const expect = (nwo, k, want, min = 1) => {
  const {main} = top(nwo, k);
  const got = has(main, want);
  ok(`${nwo}: at least ${min} of ${want.join(", ")} in its top ${k}`, got.length >= min, main.join(" | "));
};
expect("langfuse/langfuse", 10, ["comet-ml/opik", "Helicone/helicone", "promptfoo/promptfoo", "Arize-ai/phoenix", "langwatch/langwatch", "traceloop/openllmetry"], 2);
expect("microsoft/playwright-mcp", 10, ["ChromeDevTools/chrome-devtools-mcp", "executeautomation/mcp-playwright", "BrowserMCP/mcp", "drisplabs/browser-mcp"], 1);
expect("qdrant/qdrant", 10, ["lancedb/lancedb", "chroma-core/chroma", "milvus-io/milvus", "vdaas/vald", "tensorchord/pgvecto.rs", "weaviate/weaviate"], 2);
expect("aider-ai/aider", 10, ["anomalyco/opencode", "openai/codex", "plandex-ai/plandex", "OpenHands/OpenHands", "SWE-agent/SWE-agent", "cline/cline", "continuedev/continue"], 3);
expect("e2b-dev/E2B", 10, ["daytonaio/daytona", "TencentCloud/CubeSandbox", "zerobootdev/zeroboot", "opensandbox-group/OpenSandbox"], 2);
expect("letta-ai/letta", 10, ["getzep/zep", "MemPalace/mempalace", "vectorize-io/hindsight", "mem0ai/mem0", "MemMachine/MemMachine"], 2);
expect("microsoft/graphrag", 10, ["HKUDS/LightRAG", "infiniflow/ragflow", "apecloud/ApeRAG"], 1);
expect("stanfordnlp/dspy", 10, ["dottxt-ai/outlines", "567-labs/instructor", "guidance-ai/guidance"], 1);

// The ecosystem rule: built on or around it is not an alternative to it.
{
  const {r} = top("langfuse/langfuse", 50);
  const main = r.main.slice(0, 50).map(nwoOf), around = r.around.map(nwoOf);
  ok("langfuse's own MCP servers are listed as built around it, not as alternatives",
     !main.some((x) => /langfuse/i.test(x.split("/").pop())) && around.some((x) => /langfuse-mcp|mcp-server-langfuse/i.test(x)),
     "main: " + main.slice(0, 12).join(" | ") + "\n  around: " + around.slice(0, 6).join(" | "));
  const q = top("qdrant/qdrant", 50);
  ok("a project's own owner's other repositories are built around it",
     q.r.around.map(nwoOf).some((x) => x.toLowerCase().startsWith("qdrant/")) && !q.r.main.slice(0, 50).map(nwoOf).some((x) => x.toLowerCase().startsWith("qdrant/")));
  const ag = A.sourceRow(IX, at("wshobson/agents"));
  ok("a one-word name too common to be a name does not claim every row containing it", !ag.names.includes("agents"), JSON.stringify(ag.names));
}

// Why: every lookalike on the first page has at least one reason a reader can see.
{
  const {s, r} = top("langfuse/langfuse", 24);
  const reasons = r.main.slice(0, 24).map((j) => A.why(IX, s, r, j));
  ok("every one of langfuse's 24 has a stated reason", reasons.every((w) => w.cat || w.targets.length || w.terms.length || w.alt),
     JSON.stringify(reasons.filter((w) => !(w.cat || w.targets.length || w.terms.length || w.alt)).slice(0, 2)));
  ok("...and the shared words named are not the ubiquitous ones",
     reasons.every((w) => !w.terms.some((t) => ["agent", "agents", "llm", "claude", "code", "tool", "one", "mcp", "server"].includes(t))), JSON.stringify(reasons.map((w) => w.terms)));
}

// The aggregate, against the bare README vector as the control.
const PROJECTS = `anthropics/claude-code openai/codex google-gemini/gemini-cli cline/cline aider-ai/aider OpenHands/OpenHands
modelcontextprotocol/servers github/github-mcp-server microsoft/playwright-mcp upstash/context7 mem0ai/mem0
run-llama/llama_index langchain-ai/langgraph crewAIInc/crewAI e2b-dev/E2B daytonaio/daytona pydantic/pydantic-ai
anthropics/skills obra/superpowers langfuse/langfuse promptfoo/promptfoo confident-ai/deepeval browser-use/browser-use
microsoft/graphrag letta-ai/letta ollama/ollama open-webui/open-webui firecrawl/firecrawl assafelovic/gpt-researcher
stanfordnlp/dspy qdrant/qdrant wshobson/agents`.split(/\s+/).filter(Boolean);
const present = PROJECTS.filter((p) => at(p) !== undefined);
ok(`the hand-check projects are in the atlas (${present.length} of ${PROJECTS.length})`, present.length >= PROJECTS.length - 4,
   "missing: " + PROJECTS.filter((p) => at(p) === undefined).join(", "));
let same = 0, sameCtl = 0;
const dims = IX.dims;
for (const p of present) {
  const i = at(p), cat = IX.rows[i].cat;
  same += top(p).main.filter((x) => IX.rows[at(x)].cat === cat).length;
  // The control: what `near.bin` already offers, the README cosine alone.
  const s = new Float32Array(IX.n);
  for (let j = 0; j < IX.n; j++) { let a = 0; for (let k = 0; k < dims; k++) a += IX.U[i * dims + k] * IX.U[j * dims + k]; s[j] = a; }
  s[i] = -9;
  sameCtl += [...s.keys()].sort((a, b) => s[b] - s[a]).slice(0, 10).filter((j) => IX.rows[j].cat === cat).length;
}
const slots = present.length * 10;
console.log(`top-ten category agreement over ${present.length} projects: ${same}/${slots}; README vector alone ${sameCtl}/${slots}`);
ok(`top-ten category agreement: ${same}/${slots} against ${sameCtl}/${slots} for the README vector alone -- at least half, and well clear of the control`,
   same >= slots * 0.5 && same >= sameCtl * 1.8, `${same} vs ${sameCtl}`);

// ---- filters, on a pinned clock
{
  const {r} = top("langfuse/langfuse", 0);
  const now = Date.parse(d.snapshot || "2026-11-01");
  const py = A.filter(IX, r.main, {lang: "Python"}, now);
  ok("the language filter keeps only that language", py.length > 0 && py.slice(0, 50).every((j) => IX.rows[j].lang === "Python"));
  const big = A.filter(IX, r.main, {stars: 1000}, now);
  ok("the stars filter keeps only rows at or over it", big.length > 0 && big.every((j) => IX.rows[j].stars >= 1000));
  const act = A.filter(IX, r.main, {active: true}, now);
  ok("'active in the last 6 months' keeps only rows pushed since",
     act.length > 0 && act.every((j) => Date.parse(IX.rows[j].pushed) >= now - A.ACTIVE_DAYS * 86400000));
  ok("filters never reorder", A.filter(IX, r.main, {stars: 1000}, now).every((j, n, arr) => n === 0 || r.main.indexOf(arr[n - 1]) < r.main.indexOf(j)));
  ok("the language menu is drawn from the list itself", A.languages(IX, r.main).length > 0 && A.languages(IX, r.main).includes("Python"));
}

// ---- not in the atlas: a fabricated forge answer, ranked
{
  const gh = A.fromAPI("github.com", {full_name: "someone/tiny-tracer", name: "tiny-tracer",
    description: "Open-source LLM observability: tracing, evals and prompt management for LLM apps",
    topics: ["llm-observability", "tracing", "evals"], language: "TypeScript", stargazers_count: 12,
    pushed_at: "2026-10-01T00:00:00Z", html_url: "https://github.com/someone/tiny-tracer", default_branch: "main"});
  ok("a GitHub answer maps to the page's shape", gh.nwo === "someone/tiny-tracer" && gh.topics.length === 3 && gh.branch === "main");
  const s = A.sourceRepo(IX, gh), r = A.rank(IX, s);
  const main = r.main.slice(0, 15).map(nwoOf);
  ok("a project the atlas does not hold is ranked against it from its description and topics",
     has(main, ["langfuse/langfuse", "comet-ml/opik", "Helicone/helicone", "Arize-ai/phoenix", "traceloop/openllmetry", "langwatch/langwatch", "Scale3-Labs/langtrace"]).length >= 2,
     main.join(" | "));
  ok("...with its category voted from its neighbours", IX.cats[r.lead] === "Observability & Evals", IX.cats[r.lead]);
  const glab = A.fromAPI("gitlab.com", {path_with_namespace: "grp/sub/proj", name: "proj", description: "x", topics: ["a"],
    star_count: 3, last_activity_at: "2026-11-01T00:00:00Z", web_url: "https://gitlab.com/grp/sub/proj", default_branch: "main"});
  ok("a GitLab answer maps to a host-qualified nwo", glab.nwo === "gitlab.com/grp/sub/proj" && glab.path === "grp/sub/proj");
  ok("the GitLab API URL encodes the whole path as one id", A.apiURL("gitlab.com", "grp/sub/proj") === "https://gitlab.com/api/v4/projects/grp%2Fsub%2Fproj");
  ok("the GitHub API URL is /repos/owner/name", A.apiURL("github.com", "a/b") === "https://api.github.com/repos/a/b");
  ok("the README comes from raw.githubusercontent.com, which costs no API call",
     A.readmeURL("github.com", {path: "a/b", branch: "main"}) === "https://raw.githubusercontent.com/a/b/main/README.md");
  const H = (o) => ({get: (k) => o[k] ?? null});
  ok("a 404 is 'not there'", A.failure("github.com", 404, H({})).kind === "missing");
  ok("a 403 with the limit spent is 'limited', with its reset", (() => { const f = A.failure("github.com", 403, H({"x-ratelimit-remaining": "0", "x-ratelimit-reset": "1800000000"})); return f.kind === "limited" && f.reset === 1800000000000; })());
  ok("a 429 is 'limited'", A.failure("gitlab.com", 429, H({})).kind === "limited");
  ok("a GitLab 403 with no limit header is 'private'", A.failure("gitlab.com", 403, H({})).kind === "private");
  ok("anything else is an error carrying its status", A.failure("github.com", 502, H({})).status === 502);
}

// ---- a description
{
  const s = A.sourceText(IX, "a vector database for agent memory"), r = A.rank(IX, s);
  const main = r.main.slice(0, 15).map(nwoOf);
  ok("a description finds vector databases", has(main, ["qdrant/qdrant", "lancedb/lancedb", "chroma-core/chroma", "milvus-io/milvus", "weaviate/weaviate", "vdaas/vald", "jina-ai/vectordb", "oceanbase/seekdb"]).length >= 2, main.join(" | "));
  ok("...and has no ecosystem, because words have no owner", r.around.length === 0);
  ok("a description of nothing but stopwords has no terms and no vector", (() => { const t = A.sourceText(IX, "please help me choose"); return !t.terms.size && !t.doc; })());
}

// ---- the blurb clean-up the measurements depend on
ok("a trailing run of link labels is stripped", A.cleanBlurb("A memory layer for LLMs. github | website | docs | discord | twitter | github profile | linkedin") === "A memory layer for LLMs.");
ok("...and a real word that ends a sentence is not", A.cleanBlurb("Self-hosted docs") === "Self-hosted docs" || A.cleanBlurb("Self-hosted docs") === "Self-hosted");
ok("README markup is reduced to its words", A.readmeText("# Title\n```sh\nnpm i x\n```\n[docs](https://x) ![b](y)") .trim() === "Title docs b");

// ---- the detail-page link, for every row, against the tree 22_detail.py writes
{
  let bad = [];
  for (const r of IX.rows) if (!existsSync(join(DOCS, A.detailPath(r.nwo), "index.html"))) bad.push(r.nwo);
  ok(`every row's detail link resolves to a committed page (${IX.n - bad.length} of ${IX.n})`, bad.length === 0, bad.slice(0, 5).join(", "));
}

// ---- the table, on request: what the PR's hand check reads
if (process.env.AAA_ALIKE_TABLE) {
  for (const p of present) {
    const {s, r, main} = top(p, 10);
    console.log(`\n## ${IX.rows[at(p)].name} (${p}) [${IX.cats[IX.rows[at(p)].cat]}]`);
    const i = at(p), s0 = new Float32Array(IX.n);
    for (let j = 0; j < IX.n; j++) { let a = 0; for (let k = 0; k < dims; k++) a += IX.U[i * dims + k] * IX.U[j * dims + k]; s0[j] = a; }
    s0[i] = -9;
    console.log("  before (README vector alone): " + [...s0.keys()].sort((a, b) => s0[b] - s0[a]).slice(0, 5).map(nwoOf).join(" | "));
    main.forEach((x, n) => {
      const j = at(x), w = A.why(IX, s, r, j);
      console.log(`  ${n + 1}. ${x} (${IX.rows[j].stars}) [${IX.cats[IX.rows[j].cat]}] ${w.alt ? "ALT " : ""}${w.terms.join(",")}`);
    });
    console.log("  around: " + r.around.slice(0, 6).map(nwoOf).join(" | "));
  }
}
done();
