"""Materials the glTF exporter can carry and three.js can draw, and the textures they use, generated here.

Everything is a Principled BSDF with plain inputs (base colour, metallic, roughness, clear coat, emission), so
the export maps one to one onto glTF's metallic-roughness model plus KHR_materials_clearcoat and
KHR_materials_emissive_strength. A texture, where there is one, is an Image Texture wired straight into Base
Color: the exporter follows nothing more elaborate than that.

Colours are written as sRGB hex, as read off the model sheets' material swatches, and converted to linear
here.
"""
from __future__ import annotations

import math

import bpy
import numpy as np


def srgb(hex_: str):
    h = hex_.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return (*lin, 1.0)


def _bsdf(m):
    return m.node_tree.nodes["Principled BSDF"]


def principled(name, color, metal=0.0, rough=0.35, coat=0.0, coat_rough=0.05, spec=0.5, emit=None, strength=0.0,
               alpha=1.0, aniso=0.0):
    """`color`/`emit` are sRGB hex strings or linear RGB(A) tuples."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = _bsdf(m)
    col = srgb(color) if isinstance(color, str) else (*color[:3], 1.0)
    b.inputs["Base Color"].default_value = col
    b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    b.inputs["Specular IOR Level"].default_value = spec
    b.inputs["Coat Weight"].default_value = coat
    b.inputs["Coat Roughness"].default_value = coat_rough
    if aniso:
        b.inputs["Anisotropic"].default_value = aniso
    if emit is not None:
        e = srgb(emit) if isinstance(emit, str) else (*emit[:3], 1.0)
        b.inputs["Emission Color"].default_value = e
        b.inputs["Emission Strength"].default_value = strength
    if alpha < 1.0:
        b.inputs["Alpha"].default_value = alpha
        m.surface_render_method = "BLENDED"
    m.diffuse_color = col
    m.use_backface_culling = True                # glTF doubleSided false: every pal part is a closed shell
    return m


def image(name, rgba: np.ndarray, colour=True):
    """A packed Blender image from a float array (h, w, 3|4) in 0..1, row 0 at the top."""
    h, w = rgba.shape[:2]
    if rgba.shape[2] == 3:
        rgba = np.concatenate([rgba, np.ones((h, w, 1), np.float32)], axis=2)
    img = bpy.data.images.new(name, w, h, alpha=True, float_buffer=False)
    # The colour space first: changing it afterwards makes Blender regenerate a generated image's buffer,
    # which throws the pixels away.
    img.colorspace_settings.name = "sRGB" if colour else "Non-Color"
    img.pixels.foreach_set(np.ascontiguousarray(rgba[::-1].astype(np.float32)).ravel())
    img.update()
    img.pack()
    return img


def textured(m, img, uv="UVMap"):
    """Wire `img` into the material's Base Color (the image already carries the colour)."""
    nt = m.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = "Linear"
    uvn = nt.nodes.new("ShaderNodeUVMap")
    uvn.uv_map = uv
    nt.links.new(uvn.outputs["UV"], tex.inputs["Vector"])
    nt.links.new(tex.outputs["Color"], _bsdf(m).inputs["Base Color"])
    m["textured"] = True
    return m


# ------------------------------------------------------------------------------------------ textures
def _hex01(hex_):
    h = hex_.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], np.float32)


def _tile_noise(n, cells, seed):
    """Smooth tiling value noise in 0..1, `cells` lattice cells across."""
    rng = np.random.default_rng(seed)
    g = rng.random((cells, cells)).astype(np.float32)
    x = np.arange(n) * cells / n
    i0 = np.floor(x).astype(int) % cells
    i1 = (i0 + 1) % cells
    f = x - np.floor(x)
    f = f * f * (3 - 2 * f)
    a = g[i0][:, i0] * (1 - f)[None, :] + g[i0][:, i1] * f[None, :]
    b = g[i1][:, i0] * (1 - f)[None, :] + g[i1][:, i1] * f[None, :]
    return a * (1 - f)[:, None] + b * f[:, None]


def specks(name, base_hex, speck_hex="#6b5a48", n=512, count=260, seed=7, mottle=0.035, size=(0.6, 1.8)):
    """A tiling glaze: the base colour, a faint mottle, and small worn specks (the sheets' ceramic has them)."""
    base = _hex01(base_hex)
    sp = _hex01(speck_hex)
    m = (_tile_noise(n, 8, seed) - 0.5) * 2 * mottle + (_tile_noise(n, 32, seed + 1) - 0.5) * mottle * 0.6
    img = np.clip(base[None, None, :] * (1 + m[..., None]), 0, 1)
    rng = np.random.default_rng(seed + 2)
    yy, xx = np.mgrid[0:n, 0:n]
    for _ in range(count):
        cx, cy = rng.random(2) * n
        r = rng.uniform(*size)
        dx = (xx - cx + n / 2) % n - n / 2
        dy = (yy - cy + n / 2) % n - n / 2
        w = np.clip(1.5 - np.sqrt(dx * dx + dy * dy) / r, 0, 1) * rng.uniform(0.35, 0.8)
        img = img * (1 - w[..., None]) + sp[None, None, :] * w[..., None]
    return image(name, img)


def iris(name, inner_hex, outer_hex, n=256, iris_r=0.34, pupil_r=0.13, sclera_hex="#f3f1ec",
         limbal_hex="#151a06", streaks=48, seed=3):
    """An eye texture for a front-projected eyeball: UV (0.5, 0.5) is the centre of the gaze, and a radius of
    0.5 in UV is the eyeball's own radius. Sclera, a limbal ring, the iris graded from `outer_hex` at its rim
    to `inner_hex` near the pupil with radial streaks, and the pupil."""
    yy, xx = (np.mgrid[0:n, 0:n] + 0.5) / n - 0.5
    r = np.sqrt(xx * xx + yy * yy)
    ang = np.arctan2(yy, xx)
    scl = _hex01(sclera_hex)
    img = np.ones((n, n, 3), np.float32) * scl
    # A soft shadow in the sclera towards the edge (ambient occlusion from the lids).
    img *= (1 - 0.18 * np.clip((r - 0.3) / 0.2, 0, 1))[..., None]
    t = np.clip(r / iris_r, 0, 1)
    inner, outer = _hex01(inner_hex), _hex01(outer_hex)
    col = inner[None, None, :] * (1 - t[..., None] ** 1.4) + outer[None, None, :] * t[..., None] ** 1.4
    rng = np.random.default_rng(seed)
    phase = rng.random(streaks) * math.tau
    st = np.zeros_like(r)
    for k in range(streaks):
        st += np.cos(ang * (k % 7 + 3) + phase[k]) * 0.5 / streaks * 6
    col = col * (1 + 0.16 * np.clip(st, -1, 1)[..., None] * (t > 0.3)[..., None])
    # A lighter band round the pupil, as on the sheets.
    band = np.exp(-((t - 0.55) / 0.12) ** 2)
    col = col * (1 + 0.25 * band[..., None])
    inside = r < iris_r
    img[inside] = np.clip(col[inside], 0, 1)
    lim = np.exp(-((r - iris_r) / 0.012) ** 2)
    img = img * (1 - lim[..., None]) + _hex01(limbal_hex)[None, None, :] * lim[..., None]
    pup = np.clip((pupil_r - r) / 0.006 + 0.5, 0, 1)
    img = img * (1 - pup[..., None]) + np.array([0.01, 0.01, 0.012], np.float32)[None, None, :] * pup[..., None]
    return image(name, np.clip(img, 0, 1))


def eye_material(name, inner_hex, outer_hex, **kw):
    m = principled(name, "#ffffff", rough=0.12, coat=1.0, coat_rough=0.02, spec=0.6)
    return textured(m, iris(name + "-tex", inner_hex, outer_hex, **kw), uv="UVMap")
