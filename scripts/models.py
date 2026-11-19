"""The models index's rules: what a Hub repo is, which model it belongs to, what is kept, how big each
quantisation is, and the exact shape of `docs/models.json`.

`40_models.py` does the fetching and the file writing; everything it decides is a pure function here, so
`tests/models_test.py` can hold each rule to fixtures without a network. The published contract for the
data scientists who read the file is `team/contracts/models.md`; the handbook's summary is in
`handbook/pipeline.md#the-models-index`. When a rule here changes what a row means, both change with it.

ONE MODEL, MANY REPOS. The Hub is organised by repository, and a reader choosing what to run is choosing
a *model*: Qwen3-8B is one thing whether it arrives as the official safetensors, bartowski's twenty-four
GGUFs, unsloth's dynamic quants, or five MLX repos at 3 to 8 bits. So each repo is first classified --
`variant_format()` says whether it is a runnable re-packaging (GGUF, MLX, AWQ, GPTQ, bitsandbytes, FP8)
-- and every variant is then attached to the model its card names in `cardData.base_model`, walking
through any intermediate re-upload (`unsloth/Qwen3-8B` is a mirror of `Qwen/Qwen3-8B`, and a GGUF made
from the mirror belongs to the original). A quant repo whose card names no base gets one guess, by name
(`bartowski/Qwen_Qwen3-8B-GGUF` -> `Qwen/Qwen3-8B`), and is dropped if the guess does not land on a
model the index already has. That is the whole dedup: ten quant repos of one model are one row with ten
variants, keyed by the official repo id.

WHO IS TRUSTED. A variant is attached only if it comes from the model's own author or from one of the
quantisers in `config/models.json` (`quantisers`): bartowski, unsloth, lmstudio-community, ggml-org and
mlx-community for GGUF and MLX, and RedHatAI and hugging-quants for the vLLM formats. Those are the repos
the local-AI tools point people at; the long tail of re-uploads is where the broken files and the
mislabelled quants are.

WHAT IS KEPT. See `keep()`; in short, a model earns its row by being popular or by being runnable
locally from a trusted variant, and never by merely existing. NSFW-tagged repos, adapters, empty cards,
tiny merges and long-abandoned forks are out; uncensored fine-tunes that clear the bar are in but
flagged, so the page can decide what to show.

THE SIZES ARE EXACT. A file row's `bytes` is the sum of the LFS sizes the tree API reports for every
part of that quantisation -- a 235B model's Q4_K_M is three files and one row -- and never an estimate
from bits per weight. `bpw` is derived from it, not the other way round.
"""
from __future__ import annotations

import datetime as dt
import re

SCHEMA_VERSION = 1

# The columns, in order. Changing any of these is a schema change: bump SCHEMA_VERSION, update the
# contract, and update the frozen copy in tests/models_test.py, which fails until all three agree.
COLS = ["id", "name", "author", "family", "arch", "base_model", "relation", "pipeline", "uses",
        "params", "active", "params_src", "moe", "ctx", "ctx_src", "dims", "dtype",
        "license", "license_name", "license_url", "gated", "downloads", "downloads_all", "likes",
        "trending", "created", "modified", "tags", "flags", "ollama", "variants"]
VARIANT_COLS = ["repo", "fmt", "by", "downloads", "modified", "files", "mmproj"]
FILE_COLS = ["q", "bytes", "parts", "bpw"]
USES = ["chat", "reasoning", "code", "tools", "vision", "embed", "rerank", "asr", "tts", "base"]
FORMATS = ["gguf", "mlx", "awq", "gptq", "bnb", "fp8", "safetensors"]
FLAGS = ["uncensored", "community", "old"]
OLLAMA_MATCH = ["verified", "curated", "likely"]

# The pipelines the index covers. A repo tagged with anything else is not an agent's model.
PIPELINES = {"text-generation", "image-text-to-text", "feature-extraction", "sentence-similarity",
             "text-ranking", "automatic-speech-recognition", "text-to-speech", "text-to-audio",
             "any-to-any", "audio-text-to-text", "image-to-text", "text-classification"}
TEXT_PIPES = {"text-generation", "image-text-to-text", "any-to-any", "audio-text-to-text", "image-to-text"}
SPEECH_PIPES = {"automatic-speech-recognition", "text-to-speech", "text-to-audio"}
EMBED_PIPES = {"feature-extraction", "sentence-similarity"}

# Tags worth carrying into the row. The Hub's tag list is mostly licence, region, language and library
# noise that other columns already say better; these are the ones a reader filters on.
KEEP_TAGS = {"conversational", "code", "math", "tool-use", "function-calling", "agent", "agentic",
             "reasoning", "thinking", "multimodal", "vision", "audio", "moe", "rag", "chemistry",
             "medical", "finance", "multilingual", "long-context", "roleplay", "distillation"}

# How the keep rule measures popularity. Thirty-day downloads, as the Hub reports them.
POPULAR_DL, POPULAR_LIKES = 100_000, 300          # popular in its own right, whoever made it
LAB_DL, LAB_LIKES = 5_000, 50                     # a lab release that people use
RUNNABLE_DL, RUNNABLE_LIKES = 10_000, 50          # a community model with a trusted quant
MERGE_LIKES = 300                                 # merges need to be famous
OLD_DAYS = 730                                    # no update in two years
OLD_DL = 20_000                                   # ...and kept only if still this popular
MIN_CTX = 4096                                    # a chat model with less is not an agent's model
MIN_PARAMS = 50_000_000                           # text-generation below this is a toy
MIN_BPW = 1.0                                     # a file row below this is not the model's weights

DTYPE_BYTES = {"F64": 8, "F32": 4, "BF16": 2, "F16": 2, "F8_E4M3": 1, "F8_E5M2": 1, "F8_E8M0": 1,
               "I64": 8, "I32": 4, "U32": 4, "I16": 2, "U16": 2, "I8": 1, "U8": 1, "BOOL": 1}


def day(iso: str | None) -> str | None:
    return iso[:10] if iso else None


def listify(v) -> list:
    if v is None:
        return []
    return [v] if isinstance(v, str) else [x for x in v if isinstance(x, str)]


# ------------------------------------------------------------------ one Hub answer, reduced
def template_signals(t: str) -> dict:
    """What a chat template says about the model: whether it has one, takes `tools`, or thinks."""
    t = t or ""
    return {"has": bool(t.strip()),
            "tools": bool(re.search(r"\btools\b", t)),
            "think": "<think>" in t or "reasoning_content" in t or "enable_thinking" in t
                     or "<|channel|>analysis" in t}


def reduce_entry(x: dict) -> dict:
    """A listing or model-info answer cut down to what the index uses. The raw answer carries every chat
    template and widget on the Hub; this is what is cached and what every other function here reads."""
    card = x.get("cardData") or {}
    cfg = x.get("config") or {}
    tc = cfg.get("tokenizer_config") or {}
    tmpl = tc.get("chat_template")
    if isinstance(tmpl, list):   # named templates: [{"name": "default", "template": ...}, {"name": "tool_use", ...}]
        tmpl = "\n".join(t.get("template", "") for t in tmpl if isinstance(t, dict))
    gg = x.get("gguf") or {}
    st = x.get("safetensors") or {}
    qc = cfg.get("quantization_config") or {}
    moe = {k: cfg[k] for k in ("num_experts", "num_local_experts", "n_routed_experts",
                               "num_experts_per_tok", "experts_per_token") if isinstance(cfg.get(k), int)}
    return {
        "id": x["id"],
        "author": x.get("author") or x["id"].split("/")[0],
        "sha": x.get("sha"),
        "created": day(x.get("createdAt")),
        "modified": day(x.get("lastModified")),
        "downloads": int(x.get("downloads") or 0),
        "likes": int(x.get("likes") or 0),
        "trending": x.get("trendingScore"),
        "gated": x.get("gated") if x.get("gated") in ("auto", "manual") else False,
        "pipeline": x.get("pipeline_tag") or card.get("pipeline_tag"),
        "library": x.get("library_name") or card.get("library_name"),
        "tags": [t for t in (x.get("tags") or []) if isinstance(t, str)],
        "card": {"has": bool(card), "license": card.get("license") if isinstance(card.get("license"), str) else None,
                 "license_name": card.get("license_name"), "license_link": card.get("license_link"),
                 "base_model": listify(card.get("base_model")), "relation": card.get("base_model_relation"),
                 "tags": listify(card.get("tags"))},
        "archs": listify(cfg.get("architectures")),
        "model_type": cfg.get("model_type"),
        "qbits": qc.get("bits") if isinstance(qc, dict) else None,
        "moe": moe,
        "st": {"params": st.get("parameters") or {}, "total": st.get("total")} if st else None,
        "gguf": {"total": gg.get("total"), "arch": gg.get("architecture"), "ctx": gg.get("context_length")} if gg else None,
        "tmpl": template_signals(tmpl or gg.get("chat_template") or ""),
    }


# ------------------------------------------------------------------ what a repo is
def variant_format(e: dict) -> str | None:
    """The runnable re-packaging this repo is, or None if it is a model's own weights (or not a model)."""
    tags = {t.lower() for t in e["tags"]}
    name = e["id"].split("/")[1].lower()
    lib = (e.get("library") or "").lower()
    rel0 = (e["card"].get("relation") or "").lower()
    # A `gguf` tag alone is not enough: a fine-tune that ships one GGUF beside its safetensors
    # (`huihui-ai/Huihui-gpt-oss-20b-BF16-abliterated`) is a model, and walking through it as if it were a
    # re-packaging files its quants under whatever it was trained from.
    if (lib == "gguf" or name.endswith("-gguf") or "-gguf-" in name
            or ("gguf" in tags and ("safetensors" not in tags or rel0 == "quantized"))):
        return "gguf"
    if lib == "mlx" or "mlx" in tags or re.search(r"(^|-)mlx(-|$)", name):
        return "mlx"
    if "awq" in tags or re.search(r"(^|-)awq(-|$)", name):
        return "awq"
    if "gptq" in tags or re.search(r"(^|-)gptq(-|$)", name):
        return "gptq"
    if "bitsandbytes" in tags or re.search(r"bnb-?4bit|(^|-)bnb(-|$)", name):
        return "bnb"
    rel = (e["card"].get("relation") or "").lower()
    # A name that *ends* in the format is a re-packaging even when the card names no base (the labs' own
    # `Qwen3-Coder-30B-A3B-Instruct-FP8` often does not), and `resolve()` finds the original by name. In the
    # middle of a name it needs the card's word for it: DeepSeek's native-FP8 releases are models.
    if (re.search(r"-(fp8|w8a8|w4a16|nvfp4|fp4)(-dynamic|-block)?$", name)
            or (re.search(r"(^|-)(fp8|w8a8|w4a16|nvfp4|fp4)(-|$)", name) and (rel == "quantized" or e["card"]["base_model"]))):
        return "fp8" if "fp8" in name or "w8a8" in name else "awq" if "w4a16" in name else "fp8"
    return None


def is_nsfw(e: dict) -> bool:
    return "not-for-all-audiences" in {t.lower() for t in e["tags"] + e["card"]["tags"]}


def is_adapter(e: dict) -> bool:
    return (e["card"].get("relation") == "adapter" or (e.get("library") or "") == "peft"
            or "lora" in {t.lower() for t in e["tags"]} and not e.get("st"))


def is_merge(e: dict) -> bool:
    tags = {t.lower() for t in e["tags"] + e["card"]["tags"]}
    return e["card"].get("relation") == "merge" or "merge" in tags or "mergekit" in tags


# ------------------------------------------------------------------ quant labels and file groups
# llama.cpp's quant types as they appear in GGUF filenames, longest alternatives first so `Q4_K_M`
# beats `Q4_K`. `UD-` is unsloth's "dynamic" prefix and is part of the label: UD-Q4_K_XL is not Q4_K_M.
_GGUF_Q = (r"IQ1_S|IQ1_M|IQ2_XXS|IQ2_XS|IQ2_S|IQ2_M|IQ3_XXS|IQ3_XS|IQ3_S|IQ3_M|IQ4_XS|IQ4_NL|"
           r"TQ1_0|TQ2_0|Q2_K_XL|Q2_K_L|Q2_K_S|Q2_K|Q3_K_XL|Q3_K_L|Q3_K_M|Q3_K_S|Q4_K_XL|Q4_K_L|Q4_K_M|"
           r"Q4_K_S|Q4_0_4_4|Q4_0_4_8|Q4_0_8_8|Q4_0|Q4_1|Q5_K_XL|Q5_K_L|Q5_K_M|Q5_K_S|Q5_0|Q5_1|Q6_K_XL|"
           r"Q6_K_L|Q6_K|Q8_K_XL|Q8_0|MXFP4_MOE|MXFP4|BF16|FP16|F16|F32")
GGUF_QUANT = re.compile(rf"(?<![A-Za-z0-9])(UD-)?({_GGUF_Q})(?![A-Za-z0-9])", re.I)
SPLIT = re.compile(r"-(\d{5})-of-(\d{5})(?=\.gguf$)", re.I)


def gguf_label(path: str) -> str | None:
    """`Qwen_Qwen3-8B-Q4_K_M.gguf` -> `Q4_K_M`; `Q4_K_M/x-00001-of-00003.gguf` -> `Q4_K_M`. The label in
    the file's own name wins over its directory's, and the last one in the name wins, because model names
    can contain things that look like quants and the quant is what a converter appends."""
    base = path.rsplit("/", 1)[-1]
    found = list(GGUF_QUANT.finditer(SPLIT.sub("", base[:-5] if base.lower().endswith(".gguf") else base)))
    if not found and "/" in path:
        found = list(GGUF_QUANT.finditer(path.rsplit("/", 1)[0]))
    if not found:
        return None
    m = found[-1]
    q = m.group(2).upper().replace("FP16", "F16")
    return ("UD-" + q) if m.group(1) else q


def gguf_files(tree: list[tuple[str, int]], repo: str = "") -> tuple[list[list], int | None, int]:
    """(file rows without bpw, smallest mmproj bytes, files skipped) for a GGUF repo's tree.

    One row per quant label, its split parts summed. A label met in two unrelated file sets keeps the
    largest, because summing them would publish a size no download has, and the largest is the model: what
    else shares its label in these repos is a draft head for speculative decoding (`dflash-`, `mtp-`,
    `eagle3-`, a new one every few months) or a projector, all of them a fraction of the weights. The
    named drafts are skipped outright below; this rule is what keeps the next unnamed one from being
    published as the model. The count of what was skipped is returned so the stage can say."""
    groups: dict[str, dict[tuple, list[int]]] = {}
    needle = re.sub(r"(-i1)?-gguf$", "", repo.split("/")[-1].lower()) if repo else ""
    mmproj: list[int] = []
    skipped = 0
    for path, size in tree:
        low = path.lower()
        if not low.endswith(".gguf") or size <= 0:   # 0 is a pointer the Hub has no size for
            continue
        base = low.rsplit("/", 1)[-1]
        # Speculative-decoding draft heads (unsloth's `MTP/mtp-*.gguf`, ggml-org's `eagle3-*.gguf`) and
        # imatrix data ship in the same repos and carry quant labels too; they are not the model.
        if re.search(r"(^|[-_])(mtp|eagle\d*|dflash|dspark|draft|imatrix)([-_.]|$)", base) or low.startswith("mtp/"):
            continue
        # And the drafts nobody has named yet: they are written `{prefix}-{Model}-{quant}.gguf`, so a file
        # that has the repo's model name in it, but not at the start, is something shipped beside the
        # model. A file without the name at all is kept: naming varies too much to judge it.
        if needle and needle in base and not base.startswith(needle) and not base.startswith("mmproj"):
            continue
        if "mmproj" in base:
            mmproj.append(size)
            continue
        q = gguf_label(path)
        if not q:
            skipped += 1
            continue
        # Keyed on the declared part count as well as the name, because some repos ship one quant both
        # whole and split (`x-q6_k.gguf` beside `x-q6_k-00001-of-00002.gguf`), and those are two downloads
        # of the same weights, never one file set.
        m = SPLIT.search(path)
        stem = (SPLIT.sub("", path), int(m.group(2)) if m else 1)
        groups.setdefault(q, {}).setdefault(stem, []).append(size)
    rows = []
    for q, stems in groups.items():
        # The largest set; among sets within 2% of it (the same weights, whole and split), the fewest files.
        top = max(sum(v) for v in stems.values())
        stem = min((k for k, v in stems.items() if sum(v) >= 0.98 * top), key=lambda k: (len(stems[k]), k))
        sizes = stems[stem]
        skipped += sum(len(v) for k, v in stems.items() if k != stem)
        rows.append([q, sum(sizes), len(sizes)])
    rows.sort(key=lambda r: (r[1], r[0]))
    return rows, (min(mmproj) if mmproj else None), skipped


def weights_bytes(tree: list[tuple[str, int]]) -> tuple[int, int]:
    """(bytes, files) of a safetensors repo's weights. Only `.safetensors` at any depth except the
    `original/` and `consolidated` copies some labs ship beside the HF-format weights, which would double
    the count."""
    total = n = 0
    for path, size in tree:
        low = path.lower()
        if not low.endswith(".safetensors") or size <= 0:
            continue
        if low.startswith("original/") or "consolidated" in low.rsplit("/", 1)[-1]:
            continue
        total += size
        n += 1
    return total, n


MLX_Q = re.compile(r"(?:^|-)((?:\d+(?:\.\d+)?)bit(?:-(?:dwq|awq|dq|mixed[\w.-]*))?|bf16|fp16|f16|mxfp4|nvfp4|"
                   r"dwq|q[2-8]|mixed[_-]?\d[\w.-]*)(?:-v\d+)?$", re.I)


def mlx_label(e: dict) -> str:
    """`mlx-community/Qwen3-30B-A3B-4bit` -> `4bit`; falls back to the config's quantisation bits."""
    name = e["id"].split("/")[1]
    m = MLX_Q.search(name)
    if m:
        lab = m.group(1).lower()
        return lab.replace("-dwq", "-DWQ").replace("fp16", "f16")
    if e.get("qbits"):
        return f"{e['qbits']}bit"
    return "bf16"


def other_label(e: dict, fmt: str) -> str:
    """The one quant an AWQ/GPTQ/bnb/FP8 repo is. These rarely put more than the bit width in the name."""
    name = e["id"].split("/")[1].lower()
    if fmt == "fp8":
        return "nvfp4" if "nvfp4" in name else "fp4" if "fp4" in name else "fp8"
    if fmt == "bnb":
        return "nf4" if "4bit" in name or "nf4" in name else "int8"
    m = re.search(r"int(4|8)|w(4|8)a16|(\d)bit", name)
    bits = next((g for g in m.groups() if g), None) if m else (str(e["qbits"]) if e.get("qbits") else "4")
    return f"int{bits}"


def bpw(nbytes: int, params: int | None) -> float | None:
    """Bits per weight. The number a reader compares quants by, derived from the exact size."""
    if not params or not nbytes:
        return None
    return round(nbytes * 8 / params, 2)


def params_bytes(st: dict | None) -> tuple[int, str] | None:
    """(bytes, dominant dtype) of the official weights from the safetensors parameter counts. Used only
    to name the dtype; the size published is the tree's."""
    if not st or not st.get("params"):
        return None
    p = st["params"]
    dom = max(p, key=lambda k: p[k])
    return sum(DTYPE_BYTES.get(k, 2) * v for k, v in p.items()), dom


# ------------------------------------------------------------------ naming
SIZE_TOKEN = re.compile(r"^(?:\d+(?:\.\d+)?[bmkt]|\d+x\d+(?:\.\d+)?[bm]|a\d+(?:\.\d+)?b|e\d+(?:\.\d+)?b)$", re.I)
SUFFIXES = {"instruct", "it", "chat", "hf", "base", "preview", "gguf", "mlx", "awq", "gptq", "fp8",
            "bf16", "pt", "sft", "dpo", "rl", "final", "release"}


def family_of(name: str) -> str:
    """`Qwen3-30B-A3B-Instruct-2507` -> `Qwen3`, `Llama-3.1-8B-Instruct` -> `Llama-3.1`,
    `Qwen3-Coder-30B-A3B-Instruct` -> `Qwen3-Coder`, `bge-m3` -> `bge-m3`. Everything before the first
    size token; with no size token, the name less its generic suffixes and dates. A browsing aid: two
    unrelated models can share a family name and the page does not claim more than that."""
    name = re.sub(r"^Meta-(?=Llama)", "", name)
    toks = re.split(r"[-_ ]+", name)
    out = []
    for t in toks:
        if SIZE_TOKEN.match(t):
            break
        out.append(t)
    if not out or len(out) == len(toks):
        out = [t for t in toks if t.lower() not in SUFFIXES and not re.fullmatch(r"\d{4}", t)] or toks
    return "-".join(out)


def params_from_name(name: str) -> tuple[int | None, int | None]:
    """(total, active) from a name like `Qwen3-30B-A3B` (30e9, 3e9) or `gemma-3-12b` (12e9, None).
    Only used when neither safetensors nor GGUF said; `8x7B` is left alone because 56B is wrong."""
    total = active = None
    for t in re.split(r"[-_ ]+", name):
        m = re.fullmatch(r"(\d+(?:\.\d+)?)([bm])", t, re.I)
        if m and total is None:
            total = int(float(m.group(1)) * (1e9 if m.group(2).lower() == "b" else 1e6))
        m = re.fullmatch(r"a(\d+(?:\.\d+)?)b", t, re.I)
        if m:
            active = int(float(m.group(1)) * 1e9)
    return total, active


def guess_base(repo: str) -> str | None:
    """One guess at the model a quant repo with no `base_model` came from. bartowski writes the original
    org into the name as `Org_Model-GGUF`; the others drop the org, and that guess is `?/Model`."""
    name = repo.split("/")[1]
    # Repeated until nothing changes, because suffixes stack: `-4bit-mlx`, `-Q8_0-GGUF`, `-qat-mxfp8`.
    pat = re.compile(r"(-i1)?-GGUF$|-mlx$|-MLX-.*$|-(\d+(\.\d+)?-?bits?|bf16|fp16|f16|mxfp[48]|nvfp4|dwq)(-(dwq|mlx|v\d+|\d{6,8}|q\d+|gs\d+|mixed[\w.]*|optiq|ct|dynamic))*$|"
                     r"-(Q\d_K(_[SML])?|Q\d_\d|IQ\d_\w+)$|-qat$|-AWQ.*$|-GPTQ.*$|-quantized\..*$|-FP8.*$|"
                     r"-unsloth-bnb-4bit$|-bnb-4bit$|-MTP$|-unquantized$", re.I)
    while True:
        shorter = pat.sub("", name)
        if shorter == name:
            break
        name = shorter
    if "_" in name and repo.split("/")[0] in ("bartowski", "lmstudio-community"):
        org, _, rest = name.partition("_")
        return f"{org}/{rest}"
    return f"?/{name}"


def stem(repo: str) -> str:
    """A variant repo's model name with the org and every format suffix removed, lower-cased."""
    return guess_base(repo).split("/", 1)[1].lower()


def same_weights(vid: str, target: str, entries: dict[str, dict], lower: dict[str, str] | None = None) -> bool:
    """Whether a variant repo is plausibly a re-packaging of `target` itself, and not of something made
    from it. Cards do not always say: `bartowski/bagel-8b-v1.0-GGUF` names `meta-llama/Meta-Llama-3-8B` as
    its base, because bagel was trained from it, and attaching it would publish a fine-tune's file sizes
    as Llama's. So the variant's own name, stripped of its format suffixes, must be the model's name or a
    name its card gives for its base (which is how a renamed repo still matches). Strict on purpose: a
    variant left off a row costs a download option, a wrong one costs a reader the wrong model."""
    want = {target.split("/")[1].lower(), stem(target)}
    lower = lower or {}
    for b in entries[vid]["card"]["base_model"]:
        if b.count("/") != 1:
            continue
        hop = entries.get(lower.get(b.lower(), b))
        # A card's base counts as another name for the target only when it *is* the target under an old
        # name, or a plain re-upload with the target's own stem (`unsloth/Qwen3-8B`). A base that is a
        # fine-tune in between -- which the walk passed through -- does not lend the variant its name.
        if hop is None or hop["id"] == target or stem(hop["id"]) == stem(target):
            want |= {b.split("/")[1].lower(), stem(b)}
    return stem(vid) in want


# ------------------------------------------------------------------ config.json and the GGUF header
def _first(c: dict, *keys):
    for k in keys:
        v = c.get(k)
        if v is not None:
            return v
    return None


def text_config(cfg: dict) -> tuple[dict, bool]:
    """The language model's half of a config. Vision-language and audio models nest it."""
    for k in ("text_config", "llm_config", "language_config", "thinker_config"):
        sub = cfg.get(k)
        if isinstance(sub, dict):
            if k == "thinker_config" and isinstance(sub.get("text_config"), dict):
                sub = sub["text_config"]
            return {**{a: b for a, b in cfg.items() if not isinstance(b, dict)}, **sub}, True
    return cfg, False


def dims_from_config(cfg: dict) -> tuple[dict, int | None, str | None, dict | None]:
    """(dims, ctx, ctx_src, moe) from a config.json. See the contract for what each key means."""
    c, nested = text_config(cfg)
    layers = _first(c, "num_hidden_layers", "n_layer", "num_layers", "n_layers")
    hidden = _first(c, "hidden_size", "n_embd", "d_model", "dim")
    heads = _first(c, "num_attention_heads", "n_head", "n_heads", "num_heads")
    kv = _first(c, "num_key_value_heads", "n_kv_heads", "num_kv_heads")
    if kv is None and c.get("multi_query"):
        kv = 1
    if kv is None:
        kv = heads
    head_dim = c.get("head_dim")
    # Derived as transformers derives it when the config is silent -- except for MLA (DeepSeek, Kimi), where
    # hidden / heads is no dimension the model has: its cache is `kv_lora_rank + rope_dim` wide per layer.
    if (head_dim is None and isinstance(hidden, int) and isinstance(heads, int) and heads
            and not isinstance(c.get("kv_lora_rank"), int)):
        head_dim = hidden // heads
    d: dict = {}
    for k, v in (("layers", layers), ("hidden", hidden), ("heads", heads), ("kv_heads", kv),
                 ("head_dim", head_dim), ("vocab", c.get("vocab_size"))):
        if isinstance(v, int) and not isinstance(v, bool):
            d[k] = v
    hybrid = False
    lt = c.get("layer_types")
    if isinstance(lt, list) and lt:
        kinds = {str(x) for x in lt}
        if kinds - {"full_attention", "sliding_attention", "attention"}:
            hybrid = True
            d["attn_layers"] = sum(1 for x in lt if x in ("full_attention", "attention"))
        if "sliding_attention" in kinds:
            d["swa_layers"] = sum(1 for x in lt if x == "sliding_attention")
    if any(k in c for k in ("hybrid_override_pattern", "layers_block_type", "attn_layer_indices",
                            "full_attn_idxs")) or "mamba" in str(c.get("model_type", "")):
        hybrid = True
    swa = c.get("sliding_window")
    if isinstance(swa, int) and swa > 0 and c.get("use_sliding_window", True) is not False:
        d["swa"] = swa
        pat = c.get("sliding_window_pattern")
        if "swa_layers" not in d and isinstance(pat, int) and pat > 1 and layers:
            d["swa_layers"] = layers - layers // pat
    if isinstance(c.get("kv_lora_rank"), int):
        d["kv_lora_rank"] = c["kv_lora_rank"]
        if isinstance(c.get("qk_rope_head_dim"), int):
            d["rope_dim"] = c["qk_rope_head_dim"]
    if hybrid:
        d["hybrid"] = True
    # The layers that keep no KV cache: linear attention, Mamba/SSM, short convolutions. From `layer_types`
    # (Qwen3-Next), `layers_block_type` (Jamba, Granite 4) or `hybrid_override_pattern` (Nemotron-H, where
    # `M` is a Mamba layer and `*` attention). Raw counts; null when the config does not say.
    lin = None
    if isinstance(lt, list) and lt and hybrid:
        lin = sum(1 for x in lt if x not in ("full_attention", "sliding_attention", "attention"))
    elif isinstance(c.get("layers_block_type"), list):
        lin = sum(1 for x in c["layers_block_type"] if str(x).lower() not in ("attention", "full_attention"))
    elif isinstance(c.get("hybrid_override_pattern"), str):
        lin = c["hybrid_override_pattern"].count("M")
    if lin is not None:
        d["linear_layers"] = lin
    # For the fit maths' split of expert and shared weights (ds-models, team/contracts/fit.md): the expert
    # FFN width, the leading dense layers before the MoE ones, and whether the embedding table is tied.
    E0 = _first(c, "num_experts", "num_local_experts", "n_routed_experts", "moe_num_experts")
    ffn = c.get("moe_intermediate_size")
    if ffn is None and isinstance(E0, int) and E0 > 1:
        ffn = c.get("intermediate_size")   # Mixtral and gpt-oss size their experts with the plain key
    if isinstance(ffn, int) and not isinstance(ffn, bool):
        d["moe_ffn"] = ffn
    if isinstance(c.get("first_k_dense_replace"), int):
        d["dense_layers"] = c["first_k_dense_replace"]
    tied = cfg.get("tie_word_embeddings", c.get("tie_word_embeddings"))
    if isinstance(tied, bool):
        d["tied"] = tied
    if isinstance(cfg.get("vision_config"), dict) or isinstance(cfg.get("vision_tower"), (dict, str)):
        d["vision"] = True
    d["kv_f16_per_token"] = kv_f16(d)
    ctx = _first(c, "max_position_embeddings", "max_sequence_length", "seq_length", "n_positions",
                 "n_ctx", "max_seq_len")
    if not isinstance(ctx, int) or isinstance(ctx, bool) or ctx <= 0:
        ctx = None
    moe = None
    E = _first(c, "num_experts", "num_local_experts", "n_routed_experts", "moe_num_experts")
    k = _first(c, "num_experts_per_tok", "experts_per_token", "num_experts_per_token", "moe_topk")
    if isinstance(E, int) and E > 1 and isinstance(k, int):
        moe = {"experts": E, "per_tok": k,
               "shared": int(_first(c, "n_shared_experts", "num_shared_experts", "shared_expert_count") or 0)
               if not isinstance(_first(c, "n_shared_experts", "num_shared_experts"), list) else 0}
    return d, ctx, ("text_config" if nested else "config") if ctx else None, moe


def kv_f16(d: dict) -> int | None:
    """Bytes of f16 KV cache per token for a plain full-attention model: K and V, every layer, every KV
    head, two bytes. None where sliding windows, MLA or hybrid layers make that formula wrong; `fit.md`
    owns the formula that handles those."""
    if d.get("swa") or d.get("kv_lora_rank") or d.get("hybrid"):
        return None
    if not all(isinstance(d.get(k), int) for k in ("layers", "kv_heads", "head_dim")):
        return None
    return 2 * d["layers"] * d["kv_heads"] * d["head_dim"] * 2


def dims_from_gguf(h: dict) -> tuple[dict, int | None, dict | None, int | None]:
    """(dims, ctx, moe, params) from a parsed GGUF header -- the fallback for gated repos."""
    a = h.get("general.architecture")
    if not a:
        return {}, None, None, None
    g = lambda k: h.get(f"{a}.{k}")  # noqa: E731
    d: dict = {}
    for k, key in (("layers", "block_count"), ("hidden", "embedding_length"),
                   ("heads", "attention.head_count"), ("kv_heads", "attention.head_count_kv"),
                   ("head_dim", "attention.key_length"), ("vocab", "vocab_size")):
        v = g(key)
        if isinstance(v, int):
            d[k] = v
    if "kv_heads" not in d and f"{a}.attention.head_count_kv" in h.get("__arrays__", {}):
        d["hybrid"] = True   # a per-layer KV head count: some layers have none
    elif "kv_heads" not in d and "heads" in d:
        d["kv_heads"] = d["heads"]
    if "head_dim" not in d and d.get("hidden") and d.get("heads"):
        d["head_dim"] = d["hidden"] // d["heads"]
    if isinstance(g("attention.sliding_window"), int) and g("attention.sliding_window") > 0:
        d["swa"] = g("attention.sliding_window")
    if isinstance(g("attention.kv_lora_rank"), int):
        d["kv_lora_rank"] = g("attention.kv_lora_rank")
        if isinstance(g("rope.dimension_count"), int):
            d["rope_dim"] = g("rope.dimension_count")
    if any(isinstance(g(k), int) for k in ("ssm.state_size", "ssm.conv_kernel", "shortconv.l_cache")):
        d["hybrid"] = True
    if isinstance(g("expert_feed_forward_length"), int):
        d["moe_ffn"] = g("expert_feed_forward_length")
    if isinstance(g("leading_dense_block_count"), int):
        d["dense_layers"] = g("leading_dense_block_count")
    d["kv_f16_per_token"] = kv_f16(d)
    moe = None
    if isinstance(g("expert_count"), int) and g("expert_count") > 1:
        moe = {"experts": g("expert_count"), "per_tok": g("expert_used_count") or 0,
               "shared": g("expert_shared_count") or 0}
    ctx = g("context_length") if isinstance(g("context_length"), int) else None
    return d, ctx, moe, None


def active_from_config(cfg: dict, total: int | None) -> int | None:
    """Active parameters of a MoE from its config: the total less the experts not routed to. Counts a
    SwiGLU expert as three matrices of hidden x expert-width; attention, embeddings, shared experts and
    dense layers are all active. Within about 5% of the labs' own figures on the models checked
    (Qwen3-30B-A3B: 3.35B against "3.3B"), which is why `params_src` says `config` and not `name`."""
    c, _ = text_config(cfg)
    E = _first(c, "num_experts", "num_local_experts", "n_routed_experts", "moe_num_experts")
    k = _first(c, "num_experts_per_tok", "experts_per_token", "num_experts_per_token", "moe_topk")
    hidden = _first(c, "hidden_size", "d_model")
    layers = _first(c, "num_hidden_layers", "num_layers")
    inter = _first(c, "moe_intermediate_size", "expert_intermediate_size", "intermediate_size")
    if not all(isinstance(v, int) and v > 0 for v in (E, k, hidden, layers, inter)) or not total or E <= k:
        return None
    dense = c.get("first_k_dense_replace") or 0
    step = c.get("decoder_sparse_step") or 1
    only = c.get("mlp_only_layers") or []
    moe_layers = max(0, (layers - dense) // step - (len(only) if isinstance(only, list) else 0))
    inactive = moe_layers * (E - k) * 3 * hidden * inter
    active = total - inactive
    return active if 0 < active < total else None


# ------------------------------------------------------------------ uses and licences
def uses_of(e: dict, has_mmproj: bool) -> list[str]:
    """The use tags. Derived from the pipeline, the chat template and the name; see the contract."""
    name = e["id"].split("/")[1].lower()
    tags = {t.lower() for t in e["tags"] + e["card"]["tags"]}
    pipe = e.get("pipeline") or ""
    u = set()
    if pipe in EMBED_PIPES or (e.get("library") or "") == "sentence-transformers" or "embed" in name:
        u.add("embed")
    if pipe == "text-ranking" or "rerank" in name:
        u = {"rerank"}
    if pipe == "automatic-speech-recognition":
        u.add("asr")
    if pipe in ("text-to-speech", "text-to-audio") or re.search(r"(^|-)tts(-|$)", name):
        u.add("tts")
    if u:
        return [x for x in USES if x in u]
    if pipe in ("image-text-to-text", "image-to-text") or has_mmproj or "vision" in tags or re.search(r"(^|-)vl(-|$)", name):
        u.add("vision")
    t = e.get("tmpl") or {}
    if t.get("tools") or tags & {"tool-use", "function-calling", "tool-calling", "agent", "agentic"}:
        u.add("tools")
    if t.get("think") or tags & {"reasoning", "thinking"} or re.search(r"thinking|reason|(^|-)r1(-|$)|qwq", name):
        u.add("reasoning")
    if "code" in tags or re.search(r"cod(er|e|estral|ing)|devstral", name):
        u.add("code")
    if t.get("has") or "conversational" in tags or re.search(r"instruct|chat|(^|-)it(-|$)", name):
        u.add("chat")
    elif pipe in TEXT_PIPES and not u:
        u.add("base")
    if not u:
        # No pipeline tag and nothing else to go on: a model reached through its quants is a text model,
        # and without a chat template it is a base one. Every row has at least one use.
        u.add("base")
    return [x for x in USES if x in u]


LICENSE_NAMES = {
    "apache-2.0": "Apache 2.0", "mit": "MIT", "bsd-3-clause": "BSD 3-Clause", "bsd-2-clause": "BSD 2-Clause",
    "cc-by-4.0": "CC BY 4.0", "cc-by-sa-4.0": "CC BY-SA 4.0", "cc0-1.0": "CC0", "unlicense": "Unlicense",
    "cc-by-nc-4.0": "CC BY-NC 4.0", "cc-by-nc-sa-4.0": "CC BY-NC-SA 4.0", "cc-by-nc-nd-4.0": "CC BY-NC-ND 4.0",
    "gpl-3.0": "GPL 3.0", "agpl-3.0": "AGPL 3.0", "lgpl-3.0": "LGPL 3.0", "mpl-2.0": "MPL 2.0",
    "llama2": "Llama 2 Community", "llama3": "Llama 3 Community", "llama3.1": "Llama 3.1 Community",
    "llama3.2": "Llama 3.2 Community", "llama3.3": "Llama 3.3 Community", "llama4": "Llama 4 Community",
    "gemma": "Gemma Terms of Use", "openrail": "OpenRAIL", "openrail++": "OpenRAIL++",
    "bigcode-openrail-m": "BigCode OpenRAIL-M", "creativeml-openrail-m": "CreativeML OpenRAIL-M",
    "other": "Other (see the card)", "unknown": "Unknown",
}
PERMISSIVE = {"apache-2.0", "mit", "bsd-3-clause", "bsd-2-clause", "cc-by-4.0", "cc0-1.0", "unlicense",
              "isc", "zlib", "bsl-1.0", "odc-by", "cc-by-3.0", "cc-by-2.0", "afl-3.0", "ecl-2.0", "pddl"}
COPYLEFT = {"cc-by-sa-4.0", "cc-by-sa-3.0", "gpl-3.0", "gpl-2.0", "agpl-3.0", "lgpl-3.0", "lgpl-2.1",
            "mpl-2.0", "epl-2.0", "eupl-1.1", "odbl"}


def license_kind(lic: str | None) -> str:
    """`permissive`, `copyleft`, `non-commercial` or `custom`. `custom` is every licence with its own terms
    -- Llama's community licences, Gemma's terms, the OpenRAILs, and `other` -- and means "read it before
    you ship it", not "closed"."""
    if not lic:
        return "custom"
    if lic in PERMISSIVE:
        return "permissive"
    if lic in COPYLEFT:
        return "copyleft"
    if "-nc" in lic or "noncommercial" in lic or "non-commercial" in lic or "research" in lic:
        return "non-commercial"
    return "custom"


def license_url(e: dict) -> str | None:
    link = e["card"].get("license_link")
    if not isinstance(link, str) or not link.strip():
        return None
    link = link.strip()
    if link.startswith(("http://", "https://")):
        return link
    return f"https://huggingface.co/{e['id']}/blob/main/{link.lstrip('./')}"


# ------------------------------------------------------------------ the keep rule
def keep(e: dict, *, lab: bool, runnable: bool, downloads_all: int, ctx: int | None, params: int | None,
         snapshot: str) -> tuple[bool, str]:
    """(keep?, why) for a would-be model row. The order is the order of the reasons a row is refused."""
    if is_nsfw(e):
        return False, "nsfw"
    if re.search(r"(^|[-_])(dflash\d*|eagle\d*|dspark|draft)([-_]|$)", e["id"].split("/")[1], re.I):
        return False, "draft head"
    if is_adapter(e):
        return False, "adapter"
    pipe = e.get("pipeline")
    if pipe and pipe not in PIPELINES:
        return False, f"pipeline {pipe}"
    if pipe == "text-classification" and "rerank" not in e["id"].lower():
        return False, "pipeline text-classification"
    if not e["card"]["has"] and not e["card"].get("license"):
        return False, "empty card"
    popular = downloads_all >= POPULAR_DL or e["likes"] >= POPULAR_LIKES
    if is_merge(e) and e["likes"] < MERGE_LIKES:
        return False, "merge"
    text = (pipe in TEXT_PIPES) or (pipe is None and runnable)
    if text and params is not None and params < MIN_PARAMS:
        return False, "too small"
    if text and ctx is not None and ctx < MIN_CTX:
        return False, f"context {ctx}"
    if e.get("modified"):
        age = (dt.date.fromisoformat(snapshot) - dt.date.fromisoformat(e["modified"])).days
        if age > OLD_DAYS and downloads_all < OLD_DL:
            return False, "abandoned"
    if popular:
        return True, "popular"
    if lab and (e["downloads"] >= LAB_DL or e["likes"] >= LAB_LIKES or (runnable and downloads_all >= LAB_DL)):
        return True, "lab"
    if runnable and (downloads_all >= RUNNABLE_DL or e["likes"] >= RUNNABLE_LIKES):
        return True, "runnable"
    return False, "unpopular"


def flags_of(e: dict, lab: bool, snapshot: str) -> list[str]:
    out = []
    if re.search(r"abliterat|uncensor|heretic|unfiltered", e["id"], re.I):
        out.append("uncensored")
    if not lab:
        out.append("community")
    if e.get("modified") and (dt.date.fromisoformat(snapshot) - dt.date.fromisoformat(e["modified"])).days > OLD_DAYS:
        out.append("old")
    return out


# ------------------------------------------------------------------ Ollama
def ollama_candidates(name: str) -> tuple[str, str | None, bool]:
    """(library key, size tag, has extra tokens) for an HF model name. `Llama-3.1-8B-Instruct` ->
    (`llama3.1`, `8b`, False); `Qwen3-30B-A3B-Instruct-2507` -> (`qwen3`, `30b`, True). The key is the
    family with every separator removed, which is how both sides are compared."""
    toks = re.split(r"[-_ ]+", re.sub(r"^Meta-(?=Llama)", "", name))
    fam, size, extra = [], None, False
    for t in toks:
        tl = t.lower()
        if size is None and re.fullmatch(r"\d+(?:\.\d+)?[bm]|e\d+b", tl):
            size = tl
            continue
        if re.fullmatch(r"a\d+(?:\.\d+)?b", tl) or tl in SUFFIXES:
            continue
        if size is None:
            fam.append(tl)
        else:
            extra = True
    return re.sub(r"[^a-z0-9.]", "", "".join(fam)), size, extra


def match_ollama(models: list[dict], library: dict[str, dict], overrides: dict[str, str]) -> dict[str, tuple]:
    """{model id: (name, tag, how)} -- `how` is `curated` (from `config/models.json`) or `likely` (by name
    and size). Each library tag goes to at most one model: an exact family-and-size match beats one with
    extra tokens (a dated re-release, a thinking variant), and among equals the most downloaded wins."""
    keyed = {re.sub(r"[^a-z0-9.]", "", n): n for n in library}
    out: dict[str, tuple] = {}
    claimed: dict[tuple, tuple] = {}
    for m in models:
        if m["id"] in overrides:
            name, _, tag = overrides[m["id"]].partition(":")
            out[m["id"]] = (name, tag or "latest", "curated")
            claimed[(name, tag or "latest")] = (-1, 0, m["id"])
    for m in models:
        if m["id"] in out or "base" in m["uses"]:
            continue
        key, size, extra = ollama_candidates(m["name"])
        lib = keyed.get(key)
        if not lib or not size or size not in library[lib].get("sizes", []):
            continue
        rank = (1 if extra else 0, -m["downloads_all"], m["id"])
        prev = claimed.get((lib, size))
        if prev is None or rank < prev:
            if prev is not None and prev[0] >= 0:
                out.pop(prev[2], None)
            claimed[(lib, size)] = rank
            out[m["id"]] = (lib, size, "likely")
    return out


def verify_ollama(model_files: list[list], q: str | None, nbytes: int) -> bool:
    """True when an Ollama tag's model layer is, to within 3%, a GGUF of this model at the same quant.
    Ollama does not say what it converted from; a size match at the stated quant is the evidence."""
    for f in model_files:
        if (q is None or f[0].upper() == q.upper()) and f[1] and abs(f[1] - nbytes) <= 0.03 * f[1]:
            return True
    return False


def parse_ollama_library(html: str) -> dict[str, dict]:
    """{name: {"sizes": [...], "caps": [...]}} from ollama.com/library. The page is HTML, so this is the
    least stable input the index has; a parse that finds fewer than 50 models is treated as a failure by
    the stage rather than as an Ollama with no models."""
    out: dict[str, dict] = {}
    for block in re.split(r'<li\b', html):
        m = re.search(r'href="/library/([a-z0-9._-]+)"', block)
        if not m:
            continue
        spans = re.findall(r"<span[^>]*>\s*([a-z0-9.:+-]+)\s*</span>", block)
        sizes = [s for s in spans if re.fullmatch(r"(e)?\d+(\.\d+)?[bmk]|\d+x\d+b", s)]
        caps = [s for s in spans if s in ("tools", "thinking", "vision", "embedding", "audio", "cloud")]
        out[m.group(1)] = {"sizes": sizes, "caps": caps}
    return out


# ------------------------------------------------------------------ the schema
class SchemaError(Exception):
    """`docs/models.json` would not be what the contract says it is. Raised before anything is written."""


_INT = (int,)
_NUM = (int, float)


def _t(v, types, null=True):
    if v is None:
        return null
    return isinstance(v, types) and not isinstance(v, bool)


def validate(doc: dict) -> None:
    """Raise SchemaError unless `doc` is exactly the published shape. Called by the stage before it writes
    and by the test on the committed file, so a change that breaks a consumer breaks the build first."""
    def fail(msg):
        raise SchemaError(msg)

    if doc.get("schema_version") != SCHEMA_VERSION:
        fail(f"schema_version {doc.get('schema_version')!r}, expected {SCHEMA_VERSION}")
    for k, want in (("cols", COLS), ("variant_cols", VARIANT_COLS), ("file_cols", FILE_COLS), ("uses", USES)):
        if doc.get(k) != want:
            fail(f"{k} is {doc.get(k)!r}; the schema says {want!r}")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(doc.get("snapshot", ""))):
        fail("snapshot is not a date")
    lics = doc.get("licenses")
    if not isinstance(lics, dict):
        fail("licenses is not an object")
    ix = {c: i for i, c in enumerate(COLS)}
    seen = set()
    nv = nf = 0
    for r in doc.get("models", []):
        if not isinstance(r, list) or len(r) != len(COLS):
            fail(f"model row of length {len(r) if isinstance(r, list) else '?'}: {str(r)[:80]}")
        mid = r[ix["id"]]
        if not isinstance(mid, str) or mid.count("/") != 1:
            fail(f"bad id {mid!r}")
        if mid in seen:
            fail(f"duplicate model {mid}")
        seen.add(mid)
        for c in ("name", "author", "family"):
            if not isinstance(r[ix[c]], str) or not r[ix[c]]:
                fail(f"{mid}: {c} is {r[ix[c]]!r}")
        for c in ("params", "active", "ctx"):
            if not _t(r[ix[c]], _INT) or (r[ix[c]] is not None and r[ix[c]] <= 0):
                fail(f"{mid}: {c} is {r[ix[c]]!r}")
        for c in ("downloads", "downloads_all", "likes"):
            if not _t(r[ix[c]], _INT, null=False) or r[ix[c]] < 0:
                fail(f"{mid}: {c} is {r[ix[c]]!r}")
        if r[ix["downloads_all"]] < r[ix["downloads"]]:
            fail(f"{mid}: downloads_all is less than downloads")
        if not _t(r[ix["trending"]], _NUM):
            fail(f"{mid}: trending is {r[ix['trending']]!r}")
        if not set(r[ix["uses"]]) <= set(USES) or not r[ix["uses"]]:
            fail(f"{mid}: uses {r[ix['uses']]!r}")
        if not set(r[ix["flags"]]) <= set(FLAGS):
            fail(f"{mid}: flags {r[ix['flags']]!r}")
        if r[ix["gated"]] not in (False, "auto", "manual"):
            fail(f"{mid}: gated {r[ix['gated']]!r}")
        if r[ix["license"]] is not None and r[ix["license"]] not in lics:
            fail(f"{mid}: licence {r[ix['license']]!r} is not in the licenses table")
        for c in ("created", "modified"):
            if r[ix[c]] is not None and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", r[ix[c]]):
                fail(f"{mid}: {c} {r[ix[c]]!r}")
        if r[ix["active"]] is not None and r[ix["params"]] is not None and r[ix["active"]] > r[ix["params"]]:
            fail(f"{mid}: active > params")
        dims = r[ix["dims"]]
        # Every dims value is a count (int), a flag (bool: `hybrid`, `vision`, `tied`), or null.
        if dims is not None and (not isinstance(dims, dict) or not all(
                v is None or isinstance(v, bool) or (isinstance(v, int) and v >= 0) for v in dims.values())):
            fail(f"{mid}: dims {dims!r}")
        ol = r[ix["ollama"]]
        if ol is not None and (set(ol) != {"name", "tag", "bytes", "q", "match"} or ol["match"] not in OLLAMA_MATCH):
            fail(f"{mid}: ollama {ol!r}")
        vs = r[ix["variants"]]
        if not isinstance(vs, list):
            fail(f"{mid}: variants is not a list")
        for v in vs:
            if not isinstance(v, list) or len(v) != len(VARIANT_COLS):
                fail(f"{mid}: variant row {str(v)[:80]}")
            if v[1] not in FORMATS:
                fail(f"{mid}: variant format {v[1]!r}")
            if not v[5]:
                fail(f"{mid}: variant {v[0]} has no files")
            for f in v[5]:
                if (not isinstance(f, list) or len(f) != len(FILE_COLS) or not isinstance(f[0], str)
                        or not _t(f[1], _INT, null=False) or f[1] <= 0 or not _t(f[2], _INT, null=False)
                        or f[2] < 1 or not _t(f[3], _NUM)):
                    fail(f"{mid}: file row {f!r} in {v[0]}")
                nf += 1
            nv += 1
    cnt = doc.get("counts", {})
    if cnt.get("models") != len(seen) or cnt.get("variants") != nv or cnt.get("files") != nf:
        fail(f"counts {cnt} disagree with the rows ({len(seen)} models, {nv} variants, {nf} files)")


# ------------------------------------------------------------------ phase one: which repos are which
def classify(entries: dict[str, dict], quantisers: set[str]) -> tuple[dict[str, str], set[str]]:
    """({variant id: format}, mirror ids). A mirror is a quantiser's plain re-upload of a model --
    `unsloth/Qwen3-8B` -- which is neither a model of its own nor a format; anything made from it
    belongs to the original."""
    variants: dict[str, str] = {}
    mirrors: set[str] = set()
    for rid, e in entries.items():
        f = variant_format(e)
        if f:
            variants[rid] = f
        elif e["author"] in quantisers and e["card"]["base_model"]:
            mirrors.add(rid)
    return variants, mirrors


def resolve(rid: str, entries: dict[str, dict], variants: dict, mirrors: set, lower: dict[str, str]):
    """("ok", model id) | ("missing", repo id to fetch) | ("none", reason) for the model a repo belongs to.

    Walks `base_model` through variants and mirrors until it reaches a repo that is neither. `lower` maps
    lower-cased ids to the spelling the Hub uses, because cards write `qwen/qwen3-8b` too."""
    cur, seen = rid, set()
    while True:
        e = entries.get(cur)
        if e is None:
            return "missing", cur
        if cur not in variants and cur not in mirrors:
            # `e["id"]`, not `cur`: a card that names a renamed repo (`meta-llama/Meta-Llama-3.1-8B-Instruct`)
            # is answered by the Hub under the new name, and the stage files that answer under both.
            return "ok", e["id"]
        seen.add(cur)
        bases = [b for b in e["card"]["base_model"] if b.count("/") == 1]
        if not bases:
            if cur != rid:
                return "none", f"{cur} names no base"
            g = guess_base(rid)
            if g.startswith("?/"):
                want = g[2:].lower()
                hits = [i for i in entries if i.split("/")[1].lower() == want
                        and i not in variants and i not in mirrors]
                # Same-named repos are usually one original and its re-uploads (`openai/whisper-tiny` and
                # five copies). The original is the one with ten times the downloads of the next; failing
                # that, no guess.
                hits.sort(key=lambda i: -entries[i]["downloads"])
                if len(hits) > 1 and entries[hits[0]]["downloads"] >= 10 * max(1, entries[hits[1]]["downloads"]):
                    hits = hits[:1]
                if len(hits) != 1:
                    return "none", f"{rid}: no base_model, and {len(hits)} repos are called {g[2:]}"
                return "ok", hits[0]
            nxt = lower.get(g.lower(), g)
        else:
            nxt = lower.get(bases[0].lower(), bases[0])
        if nxt in seen:
            return "none", f"{rid}: base_model loops"
        cur = nxt


def labs_of(entries: dict[str, dict], variants: dict, mirrors: set, configured: set[str]) -> set[str]:
    """The configured labs plus any author with a root model (no base, not a re-packaging) that the Hub
    counts at 200,000 downloads a month. The second half is what keeps the list current without an edit
    every time a new lab ships."""
    out = set(configured)
    for rid, e in entries.items():
        if rid not in variants and rid not in mirrors and not e["card"]["base_model"] and e["downloads"] >= 200_000:
            out.add(e["author"])
    return out


def _vg(vs, key):
    """The first of `vs`' listing-time GGUF facts (`total`, `ctx`, `arch`) that is known."""
    return next(((v.get("gguf") or {}).get(key) for v in vs if (v.get("gguf") or {}).get(key)), None)


def select(entries: dict[str, dict], conf: dict, snapshot: str) -> dict:
    """Phase one, from listings alone: which repos are models, which variants attach to which, and which
    base models still need fetching. Returns {"models": {id: [variant ids]}, "missing": {id: downloads of
    the trusted variants that name it}, "dropped":
    {reason: count}, "variants": {id: fmt}, "mirrors": set, "labs": set, "why": {id: reason}}."""
    quantisers = set(conf.get("quantisers", []))
    excluded = set(conf.get("exclude", []))
    variants, mirrors = classify(entries, quantisers)
    lower = {i.lower(): i for i in entries}
    labs = labs_of(entries, variants, mirrors, set(conf.get("labs", [])))
    attach: dict[str, list[str]] = {}
    missing: dict[str, int] = {}
    dropped: dict[str, int] = {}

    def drop(reason):
        dropped[reason] = dropped.get(reason, 0) + 1

    by_name: dict[str, list[str]] = {}
    for i in entries:
        if i not in variants and i not in mirrors:
            by_name.setdefault(i.split("/")[1].lower(), []).append(i)

    for vid in sorted(variants):
        state, target = resolve(vid, entries, variants, mirrors, lower)
        if state == "missing":
            # Counted by the downloads of the trusted variants asking for it, so the stage can leave
            # unfetched a base nobody downloads a quant of: it could not pass `keep()` on that evidence.
            if entries[vid]["author"] in quantisers or entries[vid]["author"] == target.split("/")[0]:
                missing[target] = missing.get(target, 0) + entries[vid]["downloads"]
            continue
        if state == "none":
            drop("variant: no resolvable base")
            continue
        if not same_weights(vid, target, entries, lower):
            # A card that names the wrong base (`mlx-community/Qwen2.5-Coder-7B-Instruct-4bit` says
            # `Qwen2.5-Coder-7B`) is re-homed by its own name when exactly one model has that name, with
            # the same ten-times rule as `resolve()` for same-named repos. Otherwise it is a re-packaging of
            # something made from the base, and it is left out.
            hits = sorted({entries[i]["id"] for i in by_name.get(stem(vid), ())}, key=lambda i: -entries[i]["downloads"])
            if len(hits) > 1 and entries[hits[0]]["downloads"] >= 10 * max(1, entries[hits[1]]["downloads"]):
                hits = hits[:1]
            if len(hits) != 1:
                drop("variant: name is not its base's")
                continue
            target = hits[0]
        attach.setdefault(target, []).append(vid)

    # Only canonical keys: an entry filed under an old name (see `resolve`) is the same repo as the entry
    # under its new one, and listing both is the duplicate `validate()` refuses.
    candidates = {i for i, e in entries.items() if i == e["id"] and i not in variants and i not in mirrors
                  and (e.get("pipeline") in PIPELINES or i in attach)}
    models: dict[str, list[str]] = {}
    why: dict[str, str] = {}
    for mid in sorted(candidates):
        e = entries[mid]
        if mid in excluded:
            drop("excluded by config")
            continue
        vs = [v for v in attach.get(mid, [])
              if entries[v]["author"] in quantisers or entries[v]["author"] == e["author"]]
        if not vs and attach.get(mid):
            drop("variants: untrusted quantiser only")
        ve = [entries[v] for v in vs]
        runnable = any(variants[v] in ("gguf", "mlx", "awq", "gptq") for v in vs)
        total = (e.get("st") or {}).get("total") or _vg(ve, "total") or params_from_name(mid.split("/")[1])[0]
        dl_all = e["downloads"] + sum(x["downloads"] for x in ve)
        pipe = e.get("pipeline") or next((x.get("pipeline") for x in ve if x.get("pipeline")), None)
        ok, reason = keep({**e, "pipeline": pipe}, lab=e["author"] in labs, runnable=runnable,
                          downloads_all=dl_all, ctx=_vg(ve, "ctx"), params=total, snapshot=snapshot)
        if not ok:
            drop(reason)
            continue
        models[mid] = sorted(vs, key=lambda v: -entries[v]["downloads"])
        why[mid] = reason
    return {"models": models, "missing": missing, "dropped": dropped, "variants": variants,
            "mirrors": mirrors, "labs": labs, "why": why, "attach": attach}


# ------------------------------------------------------------------ phase two: the rows
def variant_row(v: dict, fmt: str, tree: list[tuple[str, int]] | None, model_author: str,
                params: int | None) -> list | None:
    """One variant row, or None when its tree has no weights this index can size."""
    if tree is None:
        return None
    mmproj = None
    if fmt == "gguf":
        files, mmproj, _ = gguf_files(tree, v["id"])
    else:
        nbytes, n = weights_bytes(tree)
        if not nbytes:
            return None
        q = mlx_label(v) if fmt == "mlx" else other_label(v, fmt)
        files = [[q, nbytes, n]]
    if not files:
        return None
    by = "official" if v["author"] == model_author else v["author"]
    # Under one bit per weight is not a quantisation of this model, whichever side is wrong: a broken
    # upload, a draft head no rule above recognised, or a parameter count read off a name that is not the
    # file's. Left out rather than published, because a reader sizing a download trusts this number.
    rows = [[q, b, n, bpw(b, params)] for q, b, n in files]
    rows = [r for r in rows if r[3] is None or r[3] >= MIN_BPW]
    if not rows:
        return None
    return [v["id"], fmt, by, v["downloads"], v["modified"], rows, mmproj]


def model_row(e: dict, variants: list[tuple[dict, str]], trees: dict, config: dict | None,
              header: dict | None, ollama: dict | None, labs: set[str], snapshot: str) -> list | None:
    """One model row in COLS order, or None if what the config revealed makes it fail `keep()` after all
    (a 2,048-token context, say, which the listing could not show)."""
    mid = e["id"]
    name = mid.split("/")[1]
    ve = [v for v, _ in variants]
    st = e.get("st") or {}
    params, src = st.get("total"), "safetensors" if st.get("total") else None
    if not params:
        params = _vg(ve, "total")
        src = "gguf" if params else None
    if not params:
        params = params_from_name(name)[0]
        src = "name" if params else None

    dims, ctx, ctx_src, moe = {}, None, None, None
    if config:
        dims, ctx, ctx_src, moe = dims_from_config(config)
    if header and (not dims or ctx is None):
        hd, hctx, hmoe, _ = dims_from_gguf(header)
        if not dims:
            dims = hd
        if ctx is None and hctx:
            ctx, ctx_src = hctx, "gguf"
        moe = moe or hmoe
    if ctx is None and _vg(ve, "ctx"):
        ctx, ctx_src = _vg(ve, "ctx"), "gguf"
    if moe is None and e.get("moe"):
        m = e["moe"]
        E = m.get("num_experts") or m.get("num_local_experts") or m.get("n_routed_experts")
        k = m.get("num_experts_per_tok") or m.get("experts_per_token")
        if E and E > 1 and k:
            moe = {"experts": E, "per_tok": k, "shared": 0}

    active = None
    if moe:
        _, named = params_from_name(name)
        if named:
            active = named
        elif config:
            active = active_from_config(config, params)
    if active is not None and params is not None and active >= params:
        active = None

    rows = []
    tree = trees.get(mid)
    if tree:
        nbytes, n = weights_bytes(tree)
        pb = params_bytes(e.get("st"))
        if nbytes:
            q = (pb[1] if pb else (config or {}).get("torch_dtype") or "bf16").lower()
            q = {"bfloat16": "bf16", "float16": "f16", "float32": "f32", "f8_e4m3": "fp8"}.get(q, q)
            rows.append([mid, "safetensors", "official", e["downloads"], e["modified"],
                         [[q, nbytes, n, bpw(nbytes, params)]], None])
    for v, fmt in variants:
        r = variant_row(v, fmt, trees.get(v["id"]), e["author"], params)
        if r:
            rows.append(r)
    has_mmproj = any(r[6] for r in rows)
    lab = e["author"] in labs
    pipe = e.get("pipeline") or next((v.get("pipeline") for v in ve if v.get("pipeline")), None)
    runnable = any(r[1] in ("gguf", "mlx", "awq", "gptq") for r in rows)
    dl_all = e["downloads"] + sum(r[3] for r in rows if r[0] != mid)
    ok, _ = keep({**e, "pipeline": pipe}, lab=lab, runnable=runnable, downloads_all=dl_all, ctx=ctx,
                 params=params, snapshot=snapshot)
    if not ok:
        return None
    rows.sort(key=lambda r: (r[0] != mid, -r[3], r[0]))

    lic = e["card"].get("license") or next((v["card"].get("license") for v in ve if v["card"].get("license")), None)
    e2 = {**e, "pipeline": pipe}
    tags = sorted({t.lower() for t in e["tags"] + e["card"]["tags"]} & KEEP_TAGS)
    arch = e.get("model_type") or (config or {}).get("model_type") or (header or {}).get("general.architecture") \
        or _vg(ve, "arch")
    dtype = (config or {}).get("torch_dtype") or (config or {}).get("dtype")
    return [mid, name, e["author"], family_of(name), arch,
            e["card"]["base_model"][0] if e["card"]["base_model"] else None,
            e["card"].get("relation"), pipe, uses_of(e2, has_mmproj),
            params, active, src, moe, ctx, ctx_src, dims or None, dtype if isinstance(dtype, str) else None,
            lic, e["card"].get("license_name") if lic == "other" else None, license_url(e),
            e["gated"], e["downloads"], dl_all, e["likes"],
            round(e["trending"], 2) if isinstance(e.get("trending"), (int, float)) else None,
            e["created"], e["modified"], tags, flags_of(e, lab, snapshot), ollama, rows]


def document(rows: list[list], snapshot: str, generated: str) -> dict:
    """The whole of `docs/models.json`, counted and validated."""
    rows = sorted(rows, key=lambda r: (-r[COLS.index("downloads_all")], r[0]))
    li = COLS.index("license")
    lics = sorted({r[li] for r in rows if r[li]})
    nv = sum(len(r[-1]) for r in rows)
    nf = sum(len(v[5]) for r in rows for v in r[-1])
    fmts: dict[str, int] = {}
    for r in rows:
        for v in r[-1]:
            fmts[v[1]] = fmts.get(v[1], 0) + 1
    doc = {
        "schema_version": SCHEMA_VERSION,
        "snapshot": snapshot,
        "generated": generated,
        "source": "https://huggingface.co",
        "cols": COLS, "variant_cols": VARIANT_COLS, "file_cols": FILE_COLS, "uses": USES,
        "licenses": {k: {"name": LICENSE_NAMES.get(k, k), "kind": license_kind(k)} for k in lics},
        "counts": {"models": len(rows), "variants": nv, "files": nf,
                   "families": len({r[COLS.index("family")].lower() for r in rows}), "formats": fmts},
        "models": rows,
    }
    validate(doc)
    return doc
