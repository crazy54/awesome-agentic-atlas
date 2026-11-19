"""The models index -- `scripts/models.py`, `scripts/hf_hub.py` and the committed `docs/models.json` -- against
fixtures shaped like the Hub's answers.

The index is read by people deciding what fits on their machine, so the ways it can be wrong are all
expensive: a quant whose split parts were not summed is a 50 GB file published as 25 GB, a quant repo
attached to the wrong model puts one model's sizes under another's name, and a column that moves without
a schema bump breaks the local-AI page silently. No network: the Hub's answers are fixtures, and the
client is driven offline against a scratch cache.

Seven groups:

  parsing     -- a GGUF header built here byte by byte, truncated and not; the RateLimit and Link headers.
  labels      -- GGUF quant labels from bartowski, unsloth (UD-, split directories) and ggml-org names;
                 MLX and AWQ/GPTQ labels.
  size maths  -- split parts summed into one row, mmproj kept apart, duplicates not summed, weights
                 without `original/` copies, bits per weight, MoE active parameters.
  dims        -- dense, GQA, sliding-window, MLA, hybrid and nested vision configs; the GGUF fallback;
                 the plain KV formula refusing the models it would get wrong.
  dedup       -- ten quant repos of one model are one row; mirrors are walked through; an untrusted
                 quantiser is not attached; a base named in another case still resolves.
  the rules   -- NSFW, adapters, merges, empty cards, abandoned forks and short contexts are out; flags.
  the schema  -- the frozen column lists, a row that breaks each rule raising, and the committed file
                 validating -- which is what makes a schema-breaking change fail loudly.

Run: python tests/models_test.py
"""
from __future__ import annotations

import json
import struct
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import hf_hub  # noqa: E402
import models as M  # noqa: E402

ok = bad = 0


def true(name: str, cond, detail: str = "") -> None:
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print(f"FAIL {name}" + (f"\n  {detail}" if detail else ""))


def eq(name, got, want):
    true(name, got == want, f"got {got!r}, want {want!r}")


def raises(name: str, fn, kind=Exception) -> None:
    try:
        fn()
    except kind:
        true(name, True)
        return
    except Exception as e:  # the wrong kind is as much a failure as none
        true(name, False, f"raised {type(e).__name__}: {e}")
        return
    true(name, False, "did not raise")


# ------------------------------------------------------------------ fixtures
def entry(rid, **kw):
    """A reduced Hub entry, as `M.reduce_entry` makes them, with whatever the test overrides."""
    card = {"has": True, "license": "apache-2.0", "license_name": None, "license_link": None,
            "base_model": [], "relation": None, "tags": []}
    card.update(kw.pop("card", {}))
    e = {"id": rid, "author": rid.split("/")[0], "sha": "s-" + rid, "created": "2026-01-01", "modified": "2026-10-01",
         "downloads": 0, "likes": 0, "trending": 1.0, "gated": False, "pipeline": "text-generation",
         "library": "transformers", "tags": [], "card": card, "archs": [], "model_type": None, "qbits": None,
         "moe": {}, "st": None, "gguf": None, "tmpl": {"has": True, "tools": True, "think": False}}
    e.update(kw)
    return e


def gguf_bytes(kvs: list[tuple[str, int, object]], version=3) -> bytes:
    """A GGUF header: magic, version, tensor count, kv count, then each key/value."""
    out = b"GGUF" + struct.pack("<IQQ", version, 0, len(kvs))
    for key, t, v in kvs:
        k = key.encode()
        out += struct.pack("<Q", len(k)) + k + struct.pack("<I", t)
        if t == 8:
            s = v.encode()
            out += struct.pack("<Q", len(s)) + s
        elif t == 9:
            et, items = v
            out += struct.pack("<IQ", et, len(items))
            for it in items:
                if et == 8:
                    s = it.encode()
                    out += struct.pack("<Q", len(s)) + s
                else:
                    out += struct.pack(M_SCALAR[et], it)
        else:
            out += struct.pack(M_SCALAR[t], v)
    return out


M_SCALAR = hf_hub._SCALAR

# ------------------------------------------------------------------ parsing
hdr = gguf_bytes([("general.architecture", 8, "qwen3"), ("general.basename", 8, "Qwen3"),
                  ("tokenizer.ggml.tokens", 9, (8, ["a", "bb", "ccc"])),
                  ("qwen3.block_count", 4, 36), ("qwen3.context_length", 4, 32768),
                  ("qwen3.embedding_length", 4, 4096), ("qwen3.attention.head_count", 4, 32),
                  ("qwen3.attention.head_count_kv", 4, 8), ("qwen3.attention.key_length", 4, 128),
                  ("qwen3.rope.freq_base", 6, 1e6), ("general.file_type", 4, 15)])
h = hf_hub.parse_gguf_header(hdr)
eq("gguf: architecture string", h.get("general.architecture"), "qwen3")
eq("gguf: u32 after a string array", h.get("qwen3.block_count"), 36)
eq("gguf: array length recorded, not its items", h["__arrays__"], {"tokenizer.ggml.tokens": 3})
true("gguf: f32 read", abs(h.get("qwen3.rope.freq_base", 0) - 1e6) < 1)
true("gguf: a whole header is not marked truncated", "__truncated__" not in h)
cut = hf_hub.parse_gguf_header(hdr[:120])
true("gguf: a cut header keeps what came before the cut", cut.get("general.architecture") == "qwen3"
     and cut.get("__truncated__") is True and "qwen3.block_count" not in cut, str(cut))
raises("gguf: not a GGUF raises", lambda: hf_hub.parse_gguf_header(b"PK\x03\x04" + b"\0" * 40), ValueError)
raises("gguf: an unknown version raises", lambda: hf_hub.parse_gguf_header(b"GGUF" + struct.pack("<IQQ", 9, 0, 0)), ValueError)
eq("ratelimit header", hf_hub._parse_ratelimit('"api";r=497;t=288'), ("api", 497, 288))
eq("ratelimit: absent is None", hf_hub._parse_ratelimit(None), None)
eq("link: next page", hf_hub.next_link('<https://huggingface.co/api/models?cursor=abc>; rel="next"'),
   "https://huggingface.co/api/models?cursor=abc")
eq("link: no next", hf_hub.next_link('<https://x>; rel="prev"'), None)

# The client's cache, offline: a hit by key, a stale key refetched (here: raises, being offline), and a
# negative answer cached like a positive one.
with tempfile.TemporaryDirectory() as tmp:
    hub = hf_hub.Hub(Path(tmp), token="", offline=True)
    hub.store("tree", "a/b", 200, [["x.gguf", 5]], key="sha1")
    eq("cache: a tree is served under its sha", hub.tree("a/b", "sha1"), [("x.gguf", 5)])
    hub2 = hf_hub.Hub(Path(tmp), token="", offline=False)
    hub2.request = lambda *a, **k: (_ for _ in ()).throw(AssertionError("asked the network"))
    eq("cache: a matching sha never touches the network", hub2.tree("a/b", "sha1"), [("x.gguf", 5)])
    raises("cache: a moved sha goes to the network", lambda: hub2.tree("a/b", "sha2"), AssertionError)
    hub.store("config", "g/gated", 401, None, key="s")
    eq("cache: a 401 is remembered", hub2.get("config", "g/gated", "https://x", key="s"), (401, None))
    raises("offline: a miss raises Offline", lambda: hub.tree("never/fetched", "s"), hf_hub.Offline)
    # The deadline: a spent budget stops the network, never the cache, so a stopped run resumes.
    import time as _time
    hub3 = hf_hub.Hub(Path(tmp), token="", offline=False)
    hub3.request = lambda *a, **k: (_ for _ in ()).throw(AssertionError("asked the network"))
    hub3.deadline = _time.monotonic() - 1
    eq("deadline: a cached tree is still served after the deadline", hub3.tree("a/b", "sha1"), [("x.gguf", 5)])
    hub4 = hf_hub.Hub(Path(tmp), token="", offline=False)
    hub4.deadline = _time.monotonic() - 1
    raises("deadline: a request past it raises DeadlineReached", lambda: hub4.request("https://huggingface.co/api/x"),
           hf_hub.DeadlineReached)
    hub5 = hf_hub.Hub(Path(tmp), token="", offline=False, log=lambda *a: None)
    hub5.deadline = _time.monotonic() + 30
    hub5._left["api"] = (3, _time.monotonic() + 600)
    raises("deadline: a rate-limit wait that would end past it is not started", lambda: hub5._wait("api"),
           hf_hub.DeadlineReached)
    true("cache: long ids make short, distinct paths",
         hub._path("tree", "a/" + "x" * 300) != hub._path("tree", "a/" + "x" * 299 + "y")
         and len(hub._path("tree", "a/" + "x" * 300).name) < 140)

# ------------------------------------------------------------------ labels
for path, want in [("Qwen_Qwen3-8B-Q4_K_M.gguf", "Q4_K_M"), ("Qwen_Qwen3-8B-IQ3_XXS.gguf", "IQ3_XXS"),
                   ("Qwen_Qwen3-8B-Q2_K_L.gguf", "Q2_K_L"), ("Qwen_Qwen3-8B-bf16.gguf", "BF16"),
                   ("Qwen3-8B-UD-Q4_K_XL.gguf", "UD-Q4_K_XL"),
                   ("Q4_K_M/Qwen3-235B-A22B-Q4_K_M-00001-of-00003.gguf", "Q4_K_M"),
                   ("UD-Q2_K_XL/Qwen3-235B-A22B-UD-Q2_K_XL-00002-of-00002.gguf", "UD-Q2_K_XL"),
                   ("gpt-oss-20b-mxfp4.gguf", "MXFP4"), ("model-f16.gguf", "F16"), ("model-fp16.gguf", "F16"),
                   ("Llama-3.1-8B-Instruct-Q8_0.gguf", "Q8_0"), ("phi-4-Q4_0_4_4.gguf", "Q4_0_4_4"),
                   ("BF16/x-00001-of-00002.gguf", "BF16"), ("weights.gguf", None)]:
    eq(f"gguf label: {path}", M.gguf_label(path), want)
eq("mlx label: 4bit", M.mlx_label(entry("mlx-community/Qwen3-30B-A3B-4bit")), "4bit")
eq("mlx label: DWQ", M.mlx_label(entry("mlx-community/Qwen3-8B-4bit-DWQ")), "4bit-DWQ")
eq("mlx label: bf16", M.mlx_label(entry("mlx-community/Qwen3-8B-bf16")), "bf16")
eq("mlx label: from config bits", M.mlx_label(entry("mlx-community/SomeModel", qbits=6)), "6bit")
eq("awq label", M.other_label(entry("Qwen/Qwen3-8B-AWQ"), "awq"), "int4")
eq("gptq label", M.other_label(entry("Qwen/Qwen2.5-7B-Instruct-GPTQ-Int8"), "gptq"), "int8")
eq("fp8 label", M.other_label(entry("Qwen/Qwen3-8B-FP8"), "fp8"), "fp8")
eq("format: gguf by tag", M.variant_format(entry("bartowski/x-GGUF", tags=["gguf"])), "gguf")
eq("format: mlx by library", M.variant_format(entry("mlx-community/x-4bit", library="mlx")), "mlx")
eq("format: an official FP8", M.variant_format(entry("Qwen/Qwen3-8B-FP8", card={"base_model": ["Qwen/Qwen3-8B"]})), "fp8")
eq("format: the model itself is none", M.variant_format(entry("Qwen/Qwen3-8B")), None)
eq("format: a lab's -FP8 with no base on its card is still a variant",
   M.variant_format(entry("Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8")), "fp8")
eq("format: a native-FP8 model is a model", M.variant_format(entry("deepseek-ai/DeepSeek-V3-0324")), None)
eq("keep: a draft head is not a model", M.keep(entry("x/Qwen3.8-27B-DFlash2", likes=9000),
   lab=True, runnable=True, downloads_all=10**7, ctx=32768, params=27e9, snapshot="2026-11-18"), (False, "draft head"))

# ------------------------------------------------------------------ size maths
tree = [("Q4_K_M/M-Q4_K_M-00001-of-00003.gguf", 49_944_699_648),
        ("Q4_K_M/M-Q4_K_M-00002-of-00003.gguf", 49_930_349_824),
        ("Q4_K_M/M-Q4_K_M-00003-of-00003.gguf", 42_279_026_016),
        ("M-Q8_0.gguf", 8_709_518_880), ("mmproj-M-f16.gguf", 900), ("mmproj-M-Q8_0.gguf", 500),
        ("M.imatrix", 5_316_782), ("README.md", 12_847), ("old/M-Q8_0.gguf", 7)]
rows, mm, skipped = M.gguf_files(tree)
eq("split parts are one row with their bytes summed",
   [r for r in rows if r[0] == "Q4_K_M"], [["Q4_K_M", 49_944_699_648 + 49_930_349_824 + 42_279_026_016, 3]])
eq("a second file set for the same quant is not summed in; the larger is kept",
   [r for r in rows if r[0] == "Q8_0"], [["Q8_0", 8_709_518_880, 1]])
eq("a draft named {prefix}-{Model}-{quant} is not the model, even under a label the model lacks",
   M.gguf_files([("dspark-DeepSeek-V4-Flash-Q8_0.gguf", 10_896_057_440), ("UD-Q2_K_XL/DeepSeek-V4-Flash-UD-Q2_K_XL-00001-of-00002.gguf", 5),
                 ("UD-Q2_K_XL/DeepSeek-V4-Flash-UD-Q2_K_XL-00002-of-00002.gguf", 90_000_000_000),
                 ("ggml-model-Q4_K_M.gguf", 4_000_000_000)], "unsloth/DeepSeek-V4-Flash-GGUF")[0],
   [["Q4_K_M", 4_000_000_000, 1], ["UD-Q2_K_XL", 90_000_000_005, 2]])
eq("a quant shipped both whole and split is one download, not their sum",
   M.gguf_files([("q-q6_k.gguf", 6_250_000_000), ("q-q6_k-00001-of-00002.gguf", 4_000_000_000),
                 ("q-q6_k-00002-of-00002.gguf", 2_260_000_000)])[0], [["Q6_K", 6_250_000_000, 1]])
eq("an unknown draft prefix loses to the model it shares a label with",
   M.gguf_files([("newdraft-M-Q8_0.gguf", 400_000_000), ("M-Q8_0.gguf", 8_000_000_000)])[0], [["Q8_0", 8_000_000_000, 1]])
eq("...and is counted as skipped", skipped, 1)
eq("mmproj is kept apart, smallest", mm, 500)
true("imatrix and README are not weights", all(r[0] in ("Q4_K_M", "Q8_0") for r in rows), str(rows))
eq("rows run smallest first", [r[0] for r in rows], ["Q8_0", "Q4_K_M"])
_rows, _, _ = M.gguf_files([("gemma-4-12b-it-Q4_K_M.gguf", 7_381_382_944), ("MTP/mtp-gemma-4-12b-it-Q8_0.gguf", 465_109_248),
                            ("mtp-gemma-4-12b-it.gguf", 465_109_248), ("eagle3-gpt-oss-20b-Q8_0.gguf", 921_488_000),
                            ("imatrix_unsloth.gguf", 13_642_656), ("x-Q6_K.gguf", 0)])
eq("speculative-decoding drafts, imatrix data and zero-byte pointers are not quantisations",
   _rows, [["Q4_K_M", 7_381_382_944, 1]])
eq("the stem keeps a fine-tune marker after a bit width", M.stem("mlx-community/Qwen3-8B-4bit-abliterated"),
   "qwen3-8b-4bit-abliterated")
eq("...and drops format tokens after one", M.stem("mlx-community/Qwen3-30B-A3B-4bit-DWQ-05082025"), "qwen3-30b-a3b")
eq("a fine-tune that ships a GGUF beside its safetensors is a model, not a variant",
   M.variant_format(entry("huihui-ai/Huihui-gpt-oss-20b-BF16-abliterated", tags=["safetensors", "gguf"],
                          card={"base_model": ["unsloth/gpt-oss-20b-BF16"]})), None)
eq("weights: original/ and consolidated copies are not counted",
   M.weights_bytes([("model-00001-of-00002.safetensors", 10), ("model-00002-of-00002.safetensors", 5),
                    ("original/consolidated.00.safetensors", 99), ("consolidated.safetensors", 99), ("x.bin", 3)]),
   (15, 2))
eq("bits per weight", M.bpw(5_027_784_224, 8_190_735_360), 4.91)
eq("bits per weight: unknown params", M.bpw(10, None), None)
eq("a file under one bit per weight is left off the variant",
   M.variant_row(entry("x/M-GGUF", tags=["gguf"]), "gguf", [("M-IQ2_M.gguf", 600_000_000), ("M-Q4_K_M.gguf", 4_900_000_000)],
                 "x", 8_000_000_000)[5], [["Q4_K_M", 4_900_000_000, 1, 4.9]])
eq("...and a variant left with none is no variant", M.variant_row(entry("x/M-GGUF", tags=["gguf"]), "gguf",
   [("M-Q4_K_M.gguf", 900_000_000)], "x", 27_000_000_000), None)
qmoe = {"architectures": ["Qwen3MoeForCausalLM"], "hidden_size": 2048, "moe_intermediate_size": 768,
        "num_hidden_layers": 48, "num_experts": 128, "num_experts_per_tok": 8, "num_attention_heads": 32,
        "num_key_value_heads": 4, "head_dim": 128, "max_position_embeddings": 40960, "decoder_sparse_step": 1,
        "mlp_only_layers": [], "model_type": "qwen3_moe", "sliding_window": None, "use_sliding_window": False}
act = M.active_from_config(qmoe, 30_532_122_624)
true("MoE active from config: Qwen3-30B-A3B lands within 5% of 3.3B", act and abs(act - 3.3e9) / 3.3e9 < 0.05, str(act))
eq("MoE active: a dense config is None", M.active_from_config({"hidden_size": 4096, "num_hidden_layers": 32}, 8e9), None)
eq("params from a name", M.params_from_name("Qwen3-30B-A3B-Instruct-2507"), (30_000_000_000, 3_000_000_000))
eq("params from a name: 0.6B", M.params_from_name("Qwen3-0.6B")[0], 600_000_000)
eq("params from a name: 8x7B is not guessed", M.params_from_name("Mixtral-8x7B-Instruct"), (None, None))

# ------------------------------------------------------------------ dims
d, ctx, src, moe = M.dims_from_config(qmoe)
eq("dims: MoE layers, kv heads, head dim", (d["layers"], d["kv_heads"], d["head_dim"]), (48, 4, 128))
eq("dims: context from max_position_embeddings", (ctx, src), (40960, "config"))
eq("dims: moe", moe, {"experts": 128, "per_tok": 8, "shared": 0})
eq("dims: the plain KV formula", d["kv_f16_per_token"], 2 * 48 * 4 * 128 * 2)
d, _, _, _ = M.dims_from_config({"num_hidden_layers": 32, "hidden_size": 4096, "num_attention_heads": 32,
                                 "max_position_embeddings": 4096})
eq("dims: no num_key_value_heads means no GQA", d["kv_heads"], 32)
eq("dims: head_dim derived from hidden/heads", d["head_dim"], 128)
gemma = {"model_type": "gemma3", "text_config": {"num_hidden_layers": 48, "hidden_size": 3840, "num_attention_heads": 16,
         "num_key_value_heads": 8, "head_dim": 256, "sliding_window": 1024, "sliding_window_pattern": 6,
         "max_position_embeddings": 131072}, "vision_config": {"hidden_size": 1152}}
d, ctx, src, _ = M.dims_from_config(gemma)
true("dims: a vision tower is recorded", d.get("vision") is True)
eq("dims: a vision model's text_config is read", (d["layers"], ctx, src), (48, 131072, "text_config"))
eq("dims: sliding window and its share of layers", (d["swa"], d["swa_layers"]), (1024, 40))
eq("dims: the plain KV formula refuses SWA", d["kv_f16_per_token"], None)
d, _, _, _ = M.dims_from_config({"num_hidden_layers": 61, "hidden_size": 7168, "num_attention_heads": 128,
                                 "num_key_value_heads": 128, "kv_lora_rank": 512, "qk_rope_head_dim": 64,
                                 "max_position_embeddings": 163840, "n_routed_experts": 256, "num_experts_per_tok": 8,
                                 "moe_intermediate_size": 2048, "first_k_dense_replace": 3, "tie_word_embeddings": False})
eq("dims: MLA rank and rope dim", (d["kv_lora_rank"], d["rope_dim"], d["kv_f16_per_token"]), (512, 64, None))
eq("dims: no head_dim is invented for MLA", "head_dim" in d, False)
eq("dims: expert width, leading dense layers, untied embeddings", (d["moe_ffn"], d["dense_layers"], d["tied"]), (2048, 3, False))
d, _, _, _ = M.dims_from_config({"num_hidden_layers": 24, "hidden_size": 2880, "num_attention_heads": 64,
                                 "num_key_value_heads": 8, "head_dim": 64, "num_local_experts": 32,
                                 "experts_per_token": 4, "intermediate_size": 2880})
eq("dims: gpt-oss sizes its experts with the plain intermediate_size", d["moe_ffn"], 2880)
d, _, _, _ = M.dims_from_config({"num_hidden_layers": 4, "hidden_size": 1024, "num_attention_heads": 8,
                                 "hybrid_override_pattern": "M-M*", "max_position_embeddings": 8192})
eq("dims: Nemotron-H's pattern counts its Mamba layers", (d.get("hybrid"), d.get("linear_layers")), (True, 2))
eq("dims: a dense config has no expert width", "moe_ffn" in M.dims_from_config({"num_hidden_layers": 32, "hidden_size": 4096, "num_attention_heads": 32, "intermediate_size": 14336})[0], False)
d, _, _, _ = M.dims_from_config({"num_hidden_layers": 4, "hidden_size": 2048, "num_attention_heads": 16,
                                 "num_key_value_heads": 2, "head_dim": 256, "max_position_embeddings": 262144,
                                 "layer_types": ["linear_attention"] * 3 + ["full_attention"]})
eq("dims: hybrid linear attention counts both kinds of layer and refuses the formula",
   (d.get("hybrid"), d.get("attn_layers"), d.get("linear_layers"), d["kv_f16_per_token"]), (True, 1, 3, None))
d, ctx, moe, _ = M.dims_from_gguf(h)
eq("dims from a GGUF header", (d["layers"], d["kv_heads"], d["head_dim"], ctx), (36, 8, 128, 32768))
eq("dims from a GGUF header: KV formula", d["kv_f16_per_token"], 2 * 36 * 8 * 128 * 2)

# ------------------------------------------------------------------ naming
for name, want in [("Qwen3-30B-A3B-Instruct-2507", "Qwen3"), ("Llama-3.1-8B-Instruct", "Llama-3.1"),
                   ("Meta-Llama-3.1-8B-Instruct", "Llama-3.1"), ("Qwen3-Coder-30B-A3B-Instruct", "Qwen3-Coder"),
                   ("gemma-3-12b-it", "gemma-3"), ("gpt-oss-20b", "gpt-oss"), ("bge-m3", "bge-m3"),
                   ("Phi-4-mini-instruct", "Phi-4-mini"), ("gemma-3n-E4B-it", "gemma-3n")]:
    eq(f"family: {name}", M.family_of(name), want)
eq("guess base: bartowski writes the org in", M.guess_base("bartowski/Qwen_Qwen3-8B-GGUF"), "Qwen/Qwen3-8B")
eq("guess base: others do not", M.guess_base("unsloth/Qwen3-8B-GGUF"), "?/Qwen3-8B")
eq("guess base: an MLX repo", M.guess_base("mlx-community/Qwen3-8B-4bit"), "?/Qwen3-8B")
eq("guess base: stacked suffixes", M.guess_base("mlx-community/whisper-small.en-mlx-4bit"), "?/whisper-small.en")
eq("guess base: ggml-org's quant-in-the-name", M.guess_base("ggml-org/gemma-1.1-2b-it-Q8_0-GGUF"), "?/gemma-1.1-2b-it")
eq("guess base: RedHatAI's spelling", M.guess_base("RedHatAI/Mistral-7B-Instruct-v0.3-quantized.w4a16"), "?/Mistral-7B-Instruct-v0.3")
_e = {e["id"]: e for e in [entry("openai/whisper-tiny", downloads=900_000), entry("someone/whisper-tiny", downloads=300),
                           entry("mlx-community/whisper-tiny-mlx", library="mlx")]}
eq("guess base: of same-named repos, the one with ten times the downloads",
   M.resolve("mlx-community/whisper-tiny-mlx", _e, {"mlx-community/whisper-tiny-mlx": "mlx"}, set(), {i.lower(): i for i in _e}),
   ("ok", "openai/whisper-tiny"))
_e["someone/whisper-tiny"]["downloads"] = 200_000
eq("guess base: ...and no guess when it is close",
   M.resolve("mlx-community/whisper-tiny-mlx", _e, {"mlx-community/whisper-tiny-mlx": "mlx"}, set(), {i.lower(): i for i in _e})[0],
   "none")

# ------------------------------------------------------------------ dedup
conf = {"quantisers": ["bartowski", "unsloth", "mlx-community", "lmstudio-community"], "labs": ["Qwen"]}
Q = "Qwen/Qwen3-8B"
ents = {e["id"]: e for e in [
    entry(Q, downloads=900_000, likes=800, st={"params": {"BF16": 8_190_735_360}, "total": 8_190_735_360}),
    entry("Qwen/Qwen3-8B-Base", downloads=50_000, tmpl={"has": False, "tools": False, "think": False}),
    entry("bartowski/Qwen_Qwen3-8B-GGUF", tags=["gguf"], library="gguf", downloads=50_000,
          card={"base_model": [Q], "relation": "quantized"}),
    entry("unsloth/Qwen3-8B", downloads=30_000, card={"base_model": [Q]}),                       # a mirror
    entry("unsloth/Qwen3-8B-GGUF", tags=["gguf"], downloads=200_000,
          card={"base_model": ["unsloth/Qwen3-8B"], "relation": "quantized"}),                  # via the mirror
    entry("mlx-community/Qwen3-8B-4bit", library="mlx", downloads=5_000,
          card={"base_model": ["qwen/qwen3-8b"]}),                                              # another case
    entry("mlx-community/Qwen3-8B-8bit", library="mlx", downloads=2_000, card={"base_model": []}),  # by name
    entry("lmstudio-community/Qwen3-8B-GGUF", tags=["gguf"], downloads=40_000, card={"base_model": [Q]}),
    entry("Qwen/Qwen3-8B-GGUF", tags=["gguf"], downloads=60_000, card={"base_model": [Q]}),        # official
    entry("Qwen/Qwen3-8B-AWQ", tags=["awq"], downloads=20_000, card={"base_model": [Q]}),
    entry("randomuser/Qwen3-8B-GGUF", tags=["gguf"], downloads=90_000, card={"base_model": [Q]}),  # untrusted
    entry("bartowski/Missing_Model-GGUF", tags=["gguf"], downloads=1_000, card={"base_model": ["Missing/Model"]}),
]}
sel = M.select(ents, conf, "2026-11-18")
eq("dedup: one model, every trusted variant attached",
   sorted(sel["models"].get(Q, [])),
   sorted(["bartowski/Qwen_Qwen3-8B-GGUF", "unsloth/Qwen3-8B-GGUF", "mlx-community/Qwen3-8B-4bit",
           "mlx-community/Qwen3-8B-8bit", "lmstudio-community/Qwen3-8B-GGUF", "Qwen/Qwen3-8B-GGUF", "Qwen/Qwen3-8B-AWQ"]))
true("dedup: a mirror is not a model", "unsloth/Qwen3-8B" not in sel["models"])
true("dedup: an untrusted quantiser is not attached", "randomuser/Qwen3-8B-GGUF" not in sel["models"].get(Q, []))
true("dedup: no variant is a model of its own", not any("GGUF" in m or "-4bit" in m for m in sel["models"]))
eq("dedup: an unknown base is asked for, not guessed, with its quants' downloads", sel["missing"], {"Missing/Model": 1_000})
true("dedup: the pretrained base is its own row", "Qwen/Qwen3-8B-Base" in sel["models"])
# A renamed repo: a card names the old id, the Hub answered under the new one, and the stage files the answer
# under both. One row, under the new name, with the old name's variants on it. The first full build found this
# one (`Meta-Llama-3.1-8B-Instruct`) when validate() refused the duplicate.
_new = entry("meta-llama/Llama-3.1-8B-Instruct", downloads=5_000_000)
_ren = {"meta-llama/Llama-3.1-8B-Instruct": _new, "meta-llama/Meta-Llama-3.1-8B-Instruct": _new,
        "bartowski/Meta-Llama-3.1-8B-Instruct-GGUF": entry("bartowski/Meta-Llama-3.1-8B-Instruct-GGUF", tags=["gguf"],
                                                          card={"base_model": ["meta-llama/Meta-Llama-3.1-8B-Instruct"]})}
_s = M.select(_ren, conf, "2026-11-18")
_ft = {e["id"]: e for e in [
    entry("meta-llama/Meta-Llama-3-8B", downloads=900_000), entry("jondurbin/bagel-8b-v1.0", downloads=200),
    entry("bartowski/bagel-8b-v1.0-GGUF", tags=["gguf"], card={"base_model": ["meta-llama/Meta-Llama-3-8B"]}),
    entry("Qwen/Qwen2.5-Coder-7B", downloads=100_000), entry("Qwen/Qwen2.5-Coder-7B-Instruct", downloads=900_000),
    entry("mlx-community/Qwen2.5-Coder-7B-Instruct-4bit", library="mlx", card={"base_model": ["Qwen/Qwen2.5-Coder-7B"]}),
    entry("unsloth/Qwen3.6-35B-A3B-MTP-GGUF", tags=["gguf"], card={"base_model": ["Qwen/Qwen3.6-35B-A3B"]}),
    entry("Qwen/Qwen3.6-35B-A3B", downloads=900_000)]}
_f = M.select(_ft, conf, "2026-11-18")
true("dedup: a fine-tune's quant whose card names the root model is not filed under the root",
     "bartowski/bagel-8b-v1.0-GGUF" not in _f["models"].get("meta-llama/Meta-Llama-3-8B", []), str(_f["models"]))
true("dedup: ...and goes to the fine-tune, which has its name", "bartowski/bagel-8b-v1.0-GGUF" in _f["attach"].get("jondurbin/bagel-8b-v1.0", []))
eq("dedup: a card naming the wrong base is re-homed by name", _f["attach"].get("Qwen/Qwen2.5-Coder-7B-Instruct"),
   ["mlx-community/Qwen2.5-Coder-7B-Instruct-4bit"])
# The chain that put an abliterated quant on gpt-oss: the quant's card names a fine-tune, the fine-tune is
# (wrongly) walked through, and the fine-tune's name then vouched for the quant. A hop that is not the
# target's own weights must not lend its name.
_hop = {e["id"]: e for e in [
    entry("openai/gpt-oss-20b", downloads=5_000_000),
    entry("someone/Tuned-gpt-oss-20b-GGUF", tags=["gguf"], card={"base_model": ["openai/gpt-oss-20b"], "relation": "quantized"}),
    entry("bartowski/someone_Tuned-gpt-oss-20b-GGUF", tags=["gguf"], card={"base_model": ["someone/Tuned-gpt-oss-20b-GGUF"]})]}
_h = M.select(_hop, conf, "2026-11-18")
true("dedup: a fine-tune met on the walk does not vouch for its quant", not _h["attach"].get("openai/gpt-oss-20b"),
     str(_h["attach"]))
eq("dedup: an -MTP GGUF is the same weights", _f["models"].get("Qwen/Qwen3.6-35B-A3B"), ["unsloth/Qwen3.6-35B-A3B-MTP-GGUF"])
eq("dedup: a renamed repo is one model under its new name, with the old name's quants",
   _s["models"], {"meta-llama/Llama-3.1-8B-Instruct": ["bartowski/Meta-Llama-3.1-8B-Instruct-GGUF"]})

# A whole row, with trees.
trees = {Q: [("model-00001-of-00002.safetensors", 10_000_000_000), ("model-00002-of-00002.safetensors", 6_400_000_000),
             ("config.json", 700)],
         "bartowski/Qwen_Qwen3-8B-GGUF": [("Qwen_Qwen3-8B-Q4_K_M.gguf", 5_027_784_224), ("Qwen_Qwen3-8B-Q8_0.gguf", 8_709_518_880)],
         "unsloth/Qwen3-8B-GGUF": [("Qwen3-8B-UD-Q4_K_XL.gguf", 5_100_000_000)],
         "mlx-community/Qwen3-8B-4bit": [("model.safetensors", 4_600_000_000), ("tokenizer.json", 11_000_000)],
         "mlx-community/Qwen3-8B-8bit": [("model.safetensors", 8_700_000_000)],
         "lmstudio-community/Qwen3-8B-GGUF": [("Qwen3-8B-Q4_K_M.gguf", 5_027_784_224)],
         "Qwen/Qwen3-8B-GGUF": [("Qwen3-8B-Q4_K_M.gguf", 5_027_784_224)],
         "Qwen/Qwen3-8B-AWQ": [("model.safetensors", 6_000_000_000)]}
cfg = {"model_type": "qwen3", "num_hidden_layers": 36, "hidden_size": 4096, "num_attention_heads": 32,
       "num_key_value_heads": 8, "head_dim": 128, "max_position_embeddings": 40960, "torch_dtype": "bfloat16"}
vs = [(ents[v], sel["variants"][v]) for v in sel["models"][Q]]
row = M.model_row(ents[Q], vs, trees, cfg, None, None, sel["labs"], "2026-11-18")
r = dict(zip(M.COLS, row))
eq("row: the official weights are the first variant", r["variants"][0][:3], [Q, "safetensors", "official"])
eq("row: the official GGUF says official", next(v[2] for v in r["variants"] if v[0] == "Qwen/Qwen3-8B-GGUF"), "official")
eq("row: an MLX repo is one file row, tokenizer not counted",
   next(v[5] for v in r["variants"] if v[0] == "mlx-community/Qwen3-8B-4bit"), [["4bit", 4_600_000_000, 1, 4.49]])
eq("row: downloads_all is the model plus every attached variant",
   r["downloads_all"], 900_000 + sum(ents[v]["downloads"] for v in sel["models"][Q]))
eq("row: params, ctx, family", (r["params"], r["ctx"], r["family"]), (8_190_735_360, 40960, "Qwen3"))
eq("row: dense model has no active count", r["active"], None)
eq("row: uses", r["uses"], ["chat", "tools"])
true("row: validates as a document", M.document([row], "2026-11-18", "2026-11-18T00:00:00Z")["counts"]["models"] == 1)

# ------------------------------------------------------------------ the rules
snap = "2026-11-18"
base = dict(lab=False, runnable=True, downloads_all=50_000, ctx=32768, params=8_000_000_000, snapshot=snap)
eq("keep: a popular community model with a quant", M.keep(entry("x/y", likes=10), **base)[0], True)
eq("keep: NSFW is out whatever its numbers",
   M.keep(entry("x/y", tags=["not-for-all-audiences"], likes=9000), **{**base, "downloads_all": 10**7}), (False, "nsfw"))
eq("keep: an adapter is out", M.keep(entry("x/y", card={"relation": "adapter"}), **base)[1], "adapter")
eq("keep: a merge needs fame", M.keep(entry("x/y", tags=["merge"], likes=40), **base), (False, "merge"))
eq("keep: an empty card is out", M.keep(entry("x/y", card={"has": False, "license": None}), **base)[1], "empty card")
eq("keep: two years idle and unpopular is abandoned",
   M.keep(entry("x/y", modified="2023-01-01"), **{**base, "downloads_all": 12_000}), (False, "abandoned"))
eq("keep: a 2,048-token chat model is out", M.keep(entry("x/y"), **{**base, "ctx": 2048})[1], "context 2048")
eq("keep: ...but an embedding model's 512 is fine",
   M.keep(entry("x/e", pipeline="sentence-similarity", downloads=200_000), **{**base, "ctx": 512, "downloads_all": 200_000})[0], True)
eq("keep: an off-topic pipeline is out", M.keep(entry("x/y", pipeline="text-to-image"), **base)[1], "pipeline text-to-image")
eq("keep: a lab's quiet release is in", M.keep(entry("Qwen/x", downloads=6_000), **{**base, "lab": True, "runnable": False})[0], True)
eq("keep: a stranger's quiet model is out", M.keep(entry("x/y", downloads=600), **{**base, "downloads_all": 900})[1], "unpopular")
eq("flags", M.flags_of(entry("x/Qwen3-8B-abliterated", modified="2024-01-01"), False, snap), ["uncensored", "community", "old"])
eq("licence kinds", [M.license_kind(x) for x in ("apache-2.0", "llama3.1", "cc-by-nc-4.0", "gpl-3.0", None)],
   ["permissive", "custom", "non-commercial", "copyleft", "custom"])
eq("licence link made absolute", M.license_url(entry("Qwen/Qwen3-8B", card={"license_link": "LICENSE"})),
   "https://huggingface.co/Qwen/Qwen3-8B/blob/main/LICENSE")
eq("uses: an embedding model is only that", M.uses_of(entry("BAAI/bge-m3", pipeline="sentence-similarity"), False), ["embed"])
eq("uses: thinking template", "reasoning" in M.uses_of(entry("x/y", tmpl={"has": True, "tools": False, "think": True}), False), True)
eq("uses: a coder with an mmproj", M.uses_of(entry("x/Some-Coder-7B", tmpl={"has": True, "tools": False, "think": False}), True),
   ["chat", "code", "vision"])
eq("uses: no template is a base model",
   M.uses_of(entry("x/y-Base", tmpl={"has": False, "tools": False, "think": False}), False), ["base"])

# ------------------------------------------------------------------ Ollama
eq("ollama key", M.ollama_candidates("Llama-3.1-8B-Instruct"), ("llama3.1", "8b", False))
eq("ollama key: extra tokens noticed", M.ollama_candidates("Qwen3-30B-A3B-Instruct-2507"), ("qwen3", "30b", True))
lib = {"qwen3": {"sizes": ["8b", "30b"]}, "llama3.1": {"sizes": ["8b"]}, "deepseek-r1": {"sizes": ["7b"]}}
ms = [{"id": "Qwen/Qwen3-30B-A3B-Instruct-2507", "name": "Qwen3-30B-A3B-Instruct-2507", "uses": ["chat"], "downloads_all": 10**7},
      {"id": "Qwen/Qwen3-30B-A3B", "name": "Qwen3-30B-A3B", "uses": ["chat"], "downloads_all": 10**5},
      {"id": "meta-llama/Llama-3.1-8B-Instruct", "name": "Llama-3.1-8B-Instruct", "uses": ["chat"], "downloads_all": 1},
      {"id": "meta-llama/Llama-3.1-8B", "name": "Llama-3.1-8B", "uses": ["base"], "downloads_all": 1},
      {"id": "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B", "name": "DeepSeek-R1-Distill-Qwen-7B", "uses": ["chat"], "downloads_all": 1}]
got = M.match_ollama(ms, lib, {"deepseek-ai/DeepSeek-R1-Distill-Qwen-7B": "deepseek-r1:7b"})
eq("ollama: the exact name beats the dated re-release", got.get("Qwen/Qwen3-30B-A3B"), ("qwen3", "30b", "likely"))
true("ollama: ...which gets nothing", "Qwen/Qwen3-30B-A3B-Instruct-2507" not in got)
eq("ollama: Llama", got.get("meta-llama/Llama-3.1-8B-Instruct"), ("llama3.1", "8b", "likely"))
true("ollama: a base model is never matched", "meta-llama/Llama-3.1-8B" not in got)
eq("ollama: an override is curated", got.get("deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"), ("deepseek-r1", "7b", "curated"))
true("ollama: a size within 3% at the same quant verifies", M.verify_ollama([["Q4_K_M", 5_027_784_224, 1, 4.9]], "Q4_K_M", 5_100_000_000))
true("ollama: the wrong quant does not", not M.verify_ollama([["Q8_0", 5_027_784_224, 1, 4.9]], "Q4_K_M", 5_027_784_224))
html = ('<li x><a href="/library/qwen3"><span>qwen3</span><span class="a">tools</span><span>8b</span><span>30b</span></a></li>'
        '<li><a href="/library/bge-m3"><span>embedding</span><span>567m</span></a></li>')
eq("ollama library page parse", M.parse_ollama_library(html),
   {"qwen3": {"sizes": ["8b", "30b"], "caps": ["tools"]}, "bge-m3": {"sizes": ["567m"], "caps": ["embedding"]}})

# ------------------------------------------------------------------ the schema
# The frozen copy. If this fails, the columns moved: bump SCHEMA_VERSION, update team/contracts/models.md and
# handbook/pipeline.md, tell ds-models and ds-app, then update these lists. In that order.
FROZEN = {1: (["id", "name", "author", "family", "arch", "base_model", "relation", "pipeline", "uses", "params",
               "active", "params_src", "moe", "ctx", "ctx_src", "dims", "dtype", "license", "license_name",
               "license_url", "gated", "downloads", "downloads_all", "likes", "trending", "created", "modified",
               "tags", "flags", "ollama", "variants"],
              ["repo", "fmt", "by", "downloads", "modified", "files", "mmproj"],
              ["q", "bytes", "parts", "bpw"])}
eq("schema: the columns are the frozen ones for this version",
   (M.COLS, M.VARIANT_COLS, M.FILE_COLS), FROZEN.get(M.SCHEMA_VERSION))
good = M.document([row], snap, "2026-11-18T00:00:00Z")


def broken(fn):
    d = json.loads(json.dumps(good))
    fn(d)
    return lambda: M.validate(d)


ix = {c: i for i, c in enumerate(M.COLS)}
raises("schema: a renamed column fails", broken(lambda d: d["cols"].__setitem__(1, "title")), M.SchemaError)
raises("schema: a short row fails", broken(lambda d: d["models"][0].pop()), M.SchemaError)
raises("schema: a version bump without new columns fails", broken(lambda d: d.__setitem__("schema_version", 2)), M.SchemaError)
raises("schema: a string where bytes go fails", broken(lambda d: d["models"][0][ix["variants"]][1][5][0].__setitem__(1, "5GB")), M.SchemaError)
raises("schema: zero bytes fails", broken(lambda d: d["models"][0][ix["variants"]][1][5][0].__setitem__(1, 0)), M.SchemaError)
raises("schema: an unknown use fails", broken(lambda d: d["models"][0][ix["uses"]].append("vibes")), M.SchemaError)
raises("schema: an unknown format fails", broken(lambda d: d["models"][0][ix["variants"]][0].__setitem__(1, "onnx")), M.SchemaError)
raises("schema: a duplicate model fails", broken(lambda d: d["models"].append(d["models"][0])), M.SchemaError)
raises("schema: a licence missing from the table fails", broken(lambda d: d["licenses"].clear()), M.SchemaError)
raises("schema: counts that disagree fail", broken(lambda d: d["counts"].__setitem__("files", 1)), M.SchemaError)
_ok = json.loads(json.dumps(good))
_ok["models"][0][ix["dims"]].update({"tied": False, "vision": True})
true("schema: false and true flags in dims are valid", (M.validate(_ok) is None))
raises("schema: a string in dims fails", broken(lambda d: d["models"][0][ix["dims"]].__setitem__("layers", "36")), M.SchemaError)
raises("schema: active above total fails",
       broken(lambda d: d["models"][0].__setitem__(ix["active"], 10**12)), M.SchemaError)

# The committed file, if there is one: valid, and its sizes are what they claim.
pub = ROOT / "docs" / "models.json"
if pub.exists():
    doc = json.loads(pub.read_text(encoding="utf-8"))
    try:
        M.validate(doc)
        true("docs/models.json validates against the schema", True)
    except M.SchemaError as e:
        true("docs/models.json validates against the schema", False, str(e))
    rows = doc["models"]
    true("docs/models.json: a real index, not a stub", len(rows) >= 300, f"{len(rows)} models")
    pi, vi = ix["params"], ix["variants"]
    off = [(r[0], v[0], f) for r in rows for v in r[vi] for f in v[5]
           if f[3] is not None and r[pi] and abs(f[3] - round(f[1] * 8 / r[pi], 2)) > 0.011]
    true("docs/models.json: every bpw is bytes x 8 / params", not off, str(off[:3]))
    # For text models (a music or speech model's safetensors count can leave out parts its GGUF holds, so its
    # bpw is evidence of nothing). Under 1 bit per weight is not a quantisation, it is a draft head or a
    # projector filed as the model -- the mistake this caught on the first real build, three ways (`MTP/`,
    # `dflash-`, `dspark-`). Over 40 is a file set summed twice. In between, real files range widely: gpt-oss
    # keeps MXFP4 experts inside its "BF16" GGUF (5.3), unsloth's Q8_K_XL keeps some tensors at 16 bits
    # (10.5), and a 270M model's embeddings dominate whatever the label says (14).
    pl = ix["pipeline"]
    nonsense = [(r[0], v[0], f) for r in rows if r[pl] in M.TEXT_PIPES for v in r[vi] if v[1] == "gguf" for f in v[5]
                if f[3] is not None and not (1.0 <= f[3] <= 40.0)]
    true("docs/models.json: no text model's GGUF is under 1 or over 40 bits per weight", not nonsense,
         f"{len(nonsense)}: {nonsense[:5]}")
    repos = [v[0] for r in rows for v in r[vi] if v[1] != "safetensors"]
    true("docs/models.json: no variant repo is attached to two models", len(repos) == len(set(repos)),
         str(sorted({x for x in repos if repos.count(x) > 1})[:5]))
    ids = {r[0] for r in rows}
    true("docs/models.json: no variant repo is also a model row", not (set(repos) & ids), str(sorted(set(repos) & ids)[:5]))
    true("docs/models.json: compact (one line, no indentation)", "\n" not in pub.read_text(encoding="utf-8").strip())

# ------------------------------------------------------------------ the page's two card renderers
# 41_models_page.py writes a card in Python for the first paint and again in the page script after the data
# loads. The script's CARD CORE block is run here under Node over real rows (or the fixture row) and must
# print byte for byte what the Python prints, quotes and odd licences included.
import importlib.util  # noqa: E402
import re  # noqa: E402
import shutil  # noqa: E402
import subprocess  # noqa: E402

node = shutil.which("node")
spec = importlib.util.spec_from_file_location("p41", ROOT / "scripts" / "41_models_page.py")
p41 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p41)
core = re.search(r"/\* CARD CORE.*?\*/(.*?)/\* END CARD CORE \*/", p41.SCRIPT, re.S)
true("page: the script has a CARD CORE block", core is not None)
sample = json.loads(pub.read_text(encoding="utf-8")) if pub.exists() else good
odd = json.loads(json.dumps(sample["models"][0]))
odd[ix["id"]], odd[ix["name"]] = 'o/It\'s "<odd>" & co', 'It\'s "<odd>" & co'
odd[ix["license"]], odd[ix["license_name"]], odd[ix["license_url"]], odd[ix["gated"]] = "other", "x-'lic'", None, "manual"
odd[ix["flags"]] = ["uncensored", "community"]
probe = dict(sample, models=sample["models"][:80] + [odd],
             licenses=dict(sample["licenses"], other={"name": "Other", "kind": "custom"}))
objs = p41.rows(probe)
py = [p41.card(m, probe["licenses"]) for m in objs]
if node and core:
    js_src = core.group(1) + "\nlic = DATA.licenses;\nprocess.stdout.write(JSON.stringify(DATA.objs.map(card)));\n"
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "core.js"
        f.write_text("const DATA = " + json.dumps({"licenses": probe["licenses"], "objs": objs}) + ";\n(function(){"
                     + js_src + "})();", encoding="utf-8")
        out = subprocess.run([node, str(f)], capture_output=True, text=True, encoding="utf-8")
    js = json.loads(out.stdout) if out.returncode == 0 else []
    true("page: the script's card core runs under Node", out.returncode == 0, out.stderr[:400])
    diff = [(a, b) for a, b in zip(py, js) if a != b]
    true(f"page: Python and script cards are identical over {len(py)} rows", js and not diff and len(js) == len(py),
         (diff[0][0][:300] + "\n  vs\n  " + diff[0][1][:300]) if diff else f"{len(js)} js cards")
else:
    true("page: Node is available to compare the two card renderers", False, "no node on PATH")

print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
