"""Lights, cameras and renders: a model-sheet studio for checking a pal against its reference, and the
homepage's own camera and lights, for the poster and for previews that look like the page will.
"""
from __future__ import annotations

import math

import bpy
from mathutils import Vector

from .geo import link


def gpu():
    """Cycles on the GPU when there is one: OptiX, else CUDA, else the CPU."""
    prefs = bpy.context.preferences.addons["cycles"].preferences
    for kind in ("OPTIX", "CUDA"):
        try:
            prefs.compute_device_type = kind
            prefs.refresh_devices()
        except TypeError:
            continue
        ok = False
        for d in prefs.devices:
            d.use = d.type == kind
            ok = ok or d.use
        if ok:
            return kind
    return "CPU"


def aim(ob, target):
    d = Vector(target) - ob.location
    ob.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def area(name, energy, loc, target, size, color=(1, 1, 1), shape="DISK"):
    li = bpy.data.lights.new(name, "AREA")
    li.energy, li.color, li.shape, li.size = energy, color, shape, size
    ob = bpy.data.objects.new(name, li)
    link(ob)
    ob.location = loc
    aim(ob, target)
    return ob


def world(color=(0.9, 0.9, 0.9), strength=1.0):
    w = bpy.data.worlds.new("world")
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (*color, 1)
    bg.inputs["Strength"].default_value = strength
    bpy.context.scene.world = w
    return w


def sheet_lights(focus, scale=1.0):
    """Soft, bright and frontal, as the model sheets are lit: a big key high on the left, a fill on the
    right, a rim behind and a bounce from below."""
    f = Vector(focus)
    s = scale
    area("key", 1500 * s * s, f + Vector((-3.0, -4.5, 3.6)) * s, f, 3.0 * s, (1.0, 0.97, 0.93))
    area("fill", 330 * s * s, f + Vector((4.2, -3.6, 1.4)) * s, f, 4.5 * s, (0.93, 0.96, 1.0))
    area("rim", 1100 * s * s, f + Vector((1.2, 4.6, 3.4)) * s, f, 2.5 * s, (1.0, 1.0, 1.0))
    area("bounce", 140 * s * s, f + Vector((0.0, -3.0, -2.6)) * s, f, 5.0 * s, (1.0, 0.98, 0.95))
    world((0.94, 0.94, 0.95), 0.22)


def floor(z=0.0, size=30.0, color=(0.92, 0.92, 0.93)):
    """A shadow-catching floor, so a render sits on the ground like the sheet's figures do."""
    me = bpy.data.meshes.new("floor")
    h = size / 2
    me.from_pydata([(-h, -h, z), (h, -h, z), (h, h, z), (-h, h, z)], [], [(0, 1, 2, 3)])
    ob = bpy.data.objects.new("floor", me)
    link(ob)
    ob.is_shadow_catcher = True
    return ob


def camera(name, focus, angle_deg, distance, height=0.0, lens=85, ortho=None, shift_y=0.0):
    """A camera `distance` from `focus`, round from the front by `angle_deg` (positive towards the
    character's left), raised by `height`."""
    cam = bpy.data.cameras.new(name)
    if ortho:
        cam.type = "ORTHO"
        cam.ortho_scale = ortho
    else:
        cam.lens = lens
    cam.shift_y = shift_y
    ob = bpy.data.objects.new(name, cam)
    link(ob)
    a = math.radians(angle_deg)
    f = Vector(focus)
    ob.location = f + Vector((math.sin(a) * distance, -math.cos(a) * distance, height))
    aim(ob, f + Vector((0, 0, height * 0.0)))
    bpy.context.scene.camera = ob
    return ob


def site_camera():
    """The homepage banner's camera (archie.js `start()`): Blender's
    (0.9, -6.2, 1.55) aimed at z 1.08, a 70 mm lens on a 36 mm sensor."""
    cam = bpy.data.cameras.new("site")
    cam.lens = 70
    ob = bpy.data.objects.new("site", cam)
    link(ob)
    ob.location = (0.9, -6.2, 1.55)
    aim(ob, (0, 0, 1.08))
    bpy.context.scene.camera = ob
    return ob


def site_lights():
    """The homepage's lights: archie.js puts three directional lights where the poster's three areas
    were, plus a dim room environment."""
    area("key", 900, (-2.2, -3.0, 3.0), (0, 0, 1.1), 2.5, (1.0, 0.95, 0.88))
    area("fill", 260, (2.8, -2.2, 1.4), (0, 0, 1.1), 3.0, (0.75, 0.82, 1.0))
    area("rim", 700, (0.6, 3.0, 2.8), (0, 0, 1.1), 1.5, (1.0, 0.75, 0.4))
    world((0.02, 0.022, 0.03), 0.6)


def settings(res=(1200, 1600), samples=96, engine="CYCLES", transparent=False, view="Standard", exposure=0.0):
    sc = bpy.context.scene
    if engine == "CYCLES":
        sc.render.engine = "CYCLES"
        sc.cycles.device = "GPU" if gpu() != "CPU" else "CPU"
        sc.cycles.samples = samples
        sc.cycles.use_denoising = True
        sc.cycles.max_bounces = 6
    else:
        for e in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
            try:
                sc.render.engine = e
                break
            except TypeError:
                continue
        try:
            sc.eevee.taa_render_samples = samples
        except AttributeError:
            pass
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = transparent
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA" if transparent else "RGB"
    sc.view_settings.view_transform = view
    sc.view_settings.look = "None"
    sc.view_settings.exposure = exposure


def render(path):
    sc = bpy.context.scene
    sc.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)
    return path
