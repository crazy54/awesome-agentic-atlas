"""Will this model run on this machine, and how fast? The Python half of the maths behind `docs/local/`.

`scripts/localfit.js` is the same arithmetic for the browser, and the page runs that one; this one exists so
the generator can write a cheat sheet that a reader with no script, or a crawler, still gets an answer from.
Two copies of a formula drift unless something compares them, so `tests/local_test.py` runs both over a grid
of machines, models and contexts and fails on the first number that differs. The docstring in the JS file
explains the model; it is not repeated here, and every constant below has the same name there.

PLACEHOLDER MATHS. ds-app's first cut, written to the interface agreed with ds-models
(`team/contracts/fit.md`) so the page could be built before the real method landed. ds-models' method
replaces the bodies; the function names and the dict shapes they return are the contract.

Plain dicts, not dataclasses, for one reason: the JS returns objects with these exact keys, and the parity
test compares the two by key. A dataclass here would be a third shape to keep in step.
"""
from __future__ import annotations

import math

EFF_GPU, EFF_CPU = 0.6, 0.5
OVERHEAD_GB = 0.6
SPREAD = (0.7, 1.3)
GREAT_TPS, GREAT_HEADROOM = 6, 0.15

BANDS = ((2, "crawl", "very slow: a word every second or so"),
         (6, "type", "slow: like someone typing"),
         (15, "read", "about as fast as you read"),
         (40, "fast", "faster than you can read"),
         (math.inf, "instant", "near-instant"))


def budget(m: dict, r: dict) -> dict:
    ram = m["ram_gb"]
    sys_gb = max(ram * r["system_min_frac"], ram - r["system_reserve_gb"])
    if m.get("unified") and m.get("backend") == "metal":
        return {"gpu": ram * (r["apple_big_frac"] if ram >= r["apple_big_from_gb"] else r["apple_small_frac"]),
                "cpu": 0}
    if m.get("unified"):
        return {"gpu": max(0, min(ram * r["unified_max_frac"], ram - r["unified_reserve_gb"])), "cpu": 0}
    if m.get("vram_gb", 0) > 0:
        return {"gpu": max(0, m["vram_gb"] - r["vram_reserve_gb"]), "cpu": sys_gb}
    return {"gpu": 0, "cpu": sys_gb}


def kv_gb(model: dict, ctx: int) -> float:
    return 2 * model["layers"] * model["kv_heads"] * model["head_dim"] * ctx * 2 / 1e9


def need(model: dict, quant: dict, ctx: int) -> dict:
    kv = kv_gb(model, ctx)
    return {"weights": quant["gb"], "kv": kv, "overhead": OVERHEAD_GB, "total": quant["gb"] + kv + OVERHEAD_GB}


def speed(m: dict, model: dict, quant: dict, place: str, gpu_frac: float) -> list[float]:
    nbytes = quant["gb"] * (model["active_b"] / model["params_b"])
    gpu_bw, cpu_bw = (m.get("gpu_bw_gbs") or 0) * EFF_GPU, (m.get("cpu_bw_gbs") or 0) * EFF_CPU
    if place == "gpu":
        secs = nbytes / gpu_bw
    elif place == "cpu":
        secs = nbytes / cpu_bw
    else:
        secs = gpu_frac * nbytes / gpu_bw + (1 - gpu_frac) * nbytes / cpu_bw
    mid = 1 / secs
    return [mid * SPREAD[0], mid, mid * SPREAD[1]]


def fit_quant(m: dict, model: dict, quant: dict, ctx: int, rules: dict) -> dict:
    b, n = budget(m, rules), need(model, quant, ctx)
    place, space, gpu_frac = None, 0, 0
    if b["gpu"] > 0 and n["total"] <= b["gpu"]:
        place, space, gpu_frac = "gpu", b["gpu"], 1
    elif b["gpu"] == 0 and n["total"] <= b["cpu"]:
        place, space = "cpu", b["cpu"]
    elif b["gpu"] > 0 and b["cpu"] > 0 and n["total"] <= b["gpu"] + b["cpu"]:
        place, space, gpu_frac = "split", b["gpu"] + b["cpu"], b["gpu"] / n["total"]
    have = space if place else b["gpu"] + b["cpu"]
    if not place:
        return {"verdict": "no", "quant": quant["q"], "ctx": ctx, "need": n, "have": have, "place": None,
                "gpu_frac": 0, "tps": None, "headroom": 1 - n["total"] / max(have, 1e-9), "catches": []}
    tps = speed(m, model, quant, place, gpu_frac)
    headroom = 1 - n["total"] / space
    catches = []
    if tps[1] < GREAT_TPS:
        catches.append("slow")
    if headroom < GREAT_HEADROOM:
        catches.append("snug")
    if place == "split":
        catches.append("split")
    verdict = "great" if tps[1] >= GREAT_TPS and headroom >= GREAT_HEADROOM else "ok"
    return {"verdict": verdict, "quant": quant["q"], "ctx": ctx, "need": n, "have": have, "place": place,
            "gpu_frac": gpu_frac, "tps": tps, "headroom": headroom, "catches": catches}


def fit(m: dict, model: dict, opts: dict | None, rules: dict) -> dict:
    opts = opts or {}
    ctx = opts.get("ctx") or 8192
    qs = sorted(model["quants"], key=lambda x: x["bits"])
    if opts.get("quant"):
        q = next((x for x in qs if x["q"] == opts["quant"]), None)
        if q:
            return {**fit_quant(m, model, q, ctx, rules), "smaller": False}
    default = next((x for x in qs if x["q"] == model.get("default_q")), qs[-1])
    first = fit_quant(m, model, default, ctx, rules)
    if first["verdict"] != "no":
        return {**first, "smaller": False}
    for q in reversed([x for x in qs if 3 <= x["bits"] < default["bits"]]):
        r = fit_quant(m, model, q, ctx, rules)
        if r["verdict"] != "no":
            return {**r, "smaller": True}
    return {**first, "smaller": False}


def speed_words(tps: float) -> dict | None:
    for top, key, words in BANDS:
        if tps < top:
            return {"key": key, "words": words, "wps": tps * 0.75}
    return None
