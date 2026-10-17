"""glTF export for the pals, and the post-pass that makes the files small enough to fetch on a page view.

`glb()` writes one character (its armature, the meshes skinned to it, and every NLA track on the armature or
on its face mesh's shape keys as a named animation) with Blender's exporter. Modifiers other than the
armature are applied by `rig.finalize()` already, so the exporter applies nothing; the rest pose is exported
as the bind pose; only deforming bones (all of the pals' are) become joints.

`compress()` then runs glTF-Transform over the file: it resamples the baked clips (dropping keys that a
straight line through their neighbours reproduces), prunes attributes no material reads (texture
coordinates on untextured primitives), and applies EXT_meshopt_compression with quantisation, which
three.js reads through MeshoptDecoder. The CLI lives in the scratch tools folder, not in this repository,
which has no package.json; `GLTF_TRANSFORM` names its entry point.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

import bpy


def select_only(objs):
    for o in list(bpy.context.selected_objects):
        o.select_set(False)
    for o in objs:
        o.hide_set(False)
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]


def glb(path, objs, animations=True, frame_step=1, image_quality=86, fps=30):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    bpy.context.scene.render.fps = fps          # the exporter turns frames into seconds at the scene's rate
    bpy.context.scene.render.fps_base = 1.0
    select_only(objs)
    bpy.ops.export_scene.gltf(
        filepath=str(path), export_format="GLB", use_selection=True, export_apply=False, export_yup=True,
        export_texcoords=True, export_normals=True, export_tangents=False, export_materials="EXPORT",
        export_image_format="WEBP", export_image_quality=image_quality, export_cameras=False, export_lights=False,
        export_extras=False, export_skins=True, export_def_bones=True, export_rest_position_armature=True,
        export_leaf_bone=False, export_morph=True, export_morph_normal=False, export_morph_tangent=False,
        export_animations=animations, export_animation_mode="NLA_TRACKS", export_force_sampling=True,
        export_frame_step=frame_step, export_optimize_animation_size=True, export_anim_single_armature=True,
        export_reset_pose_bones=True, export_merge_animation="NLA_TRACK", export_nla_strips=True,
        export_anim_slide_to_zero=True)
    return path


def compress(src, dst=None, tolerance=0.0004):
    """Slim `src` into `dst` (default: in place) with tools/slim.mjs: drop channels held at rest, resample,
    prune, quantise and meshopt-compress. `PALS_TOOLS` names the folder holding slim.mjs and its
    node_modules."""
    tools = Path(os.environ.get("PALS_TOOLS", r"E:/Development Workspaces/Archie and Pals/tools"))
    src = Path(src)
    dst = Path(dst or src)
    r = subprocess.run(["node", str(tools / "slim.mjs"), str(src), str(dst), "--tolerance", str(tolerance)],
                       capture_output=True, text=True, cwd=str(tools))
    if r.returncode:
        raise RuntimeError(f"slim.mjs failed:\n{r.stdout}\n{r.stderr}")
    print(r.stdout.strip())
    return dst
