"""The skeleton every pal shares, and the step that turns a pile of tagged parts into a skinned character.

THE SKELETON. One naming scheme for the whole cast, so a clip written for one can be read against another and
the page can find the same joints on each (three.js strips '.', so the sides are `_L`/`_R`):

    root                                   on the floor between the feet; the page moves this
      hips                                 the pelvis, the centre of mass
        spine -> chest -> neck -> head
                         head: eye_L/R, lid_up_L/R, lid_lo_L/R, brow_in/mid/out_L/R, ear_L/R, + extras
                 chest: shoulder_L/R -> upper_arm -> forearm -> hand
                         hand: thumb_1..3, index_1..3, middle_1..3, ring_1..3, grip
        thigh_L/R -> shin -> foot -> toe

plus whatever a character adds (Archie's crest and core dock, Zip's horns). Every bone deforms, so every
bone exports: the page needs `grip_*` to hang props on even though no vertex follows it.

BONE AXES. Each bone is built with its local Z leaning towards a hint (its `z`), and Blender's local X is then
Y x Z. A positive rotation about local X swings the bone's tail towards that hint. Limbs take "forward" (-Y)
as the hint, fingers take the palm's side, so +X is flexion nearly everywhere: thigh forward, forearm
forward, a finger curling into the palm. The shin's +X would swing it forward too, so a knee bends with -X.

FINALIZE. Parts are separate meshes in the rest pose, each tagged `ob["bone"]` (or already carrying vertex
groups, for the few that bend: the brows). `finalize()` applies their modifiers, puts every vertex of an
untagged-group part in its bone's group at weight 1, and joins the parts by their `ob["mesh"]` tag (default
"body") into one mesh each, deformed by the armature. One mesh per tag, one draw call per material in it:
the body is a single skinned mesh however many pieces it was built from. The face (mouth and brows) is a
separate, small mesh because it carries shape keys, which glTF stores per vertex for the whole mesh.
"""
from __future__ import annotations

import bpy
from mathutils import Matrix, Vector

from .geo import apply_modifiers, link

SIDES = (("_L", 1), ("_R", -1))


class Rig:
    def __init__(self, name):
        self.name = name
        self.arm = bpy.data.armatures.new(name + "-rig")
        self.ob = bpy.data.objects.new(name, self.arm)
        link(self.ob)
        self.arm.display_type = "OCTAHEDRAL"
        self.ob.show_in_front = True
        self.specs = {}
        self.order = []

    def bone(self, name, head, tail, parent=None, z=(0, -1, 0), deform=True):
        self.specs[name] = dict(head=Vector(head), tail=Vector(tail), parent=parent, z=Vector(z),
                                deform=deform)
        self.order.append(name)
        return name

    def head(self, name):
        return self.specs[name]["head"]

    def tail(self, name):
        return self.specs[name]["tail"]

    def build(self):
        view = bpy.context.view_layer
        for o in list(bpy.context.selected_objects):
            o.select_set(False)
        view.objects.active = self.ob
        self.ob.select_set(True)
        bpy.ops.object.mode_set(mode="EDIT")
        eb = self.arm.edit_bones
        for name in self.order:
            s = self.specs[name]
            b = eb.new(name)
            b.head, b.tail = s["head"], s["tail"]
            y = (s["tail"] - s["head"]).normalized()
            z = s["z"] - y * s["z"].dot(y)
            if z.length < 1e-6:
                z = y.orthogonal()
            b.align_roll(z.normalized())
            b.use_deform = s["deform"]
            if s["parent"]:
                b.parent = eb[s["parent"]]
                b.use_connect = False
        bpy.ops.object.mode_set(mode="OBJECT")
        for pb in self.ob.pose.bones:
            pb.rotation_mode = "QUATERNION"
        view.update()
        return self

    def finalize(self, parts, keep_parts=False):
        """Skin `parts` (tagged meshes) to the armature; returns {mesh tag: joined object}."""
        groups = {}
        for ob in parts:
            if ob.type != "MESH":
                continue
            apply_modifiers(ob)
            bone = ob.get("bone")
            if not ob.vertex_groups:
                if not bone or bone not in self.specs:
                    raise ValueError(f"part {ob.name} rides on unknown bone {bone!r}")
                vg = ob.vertex_groups.new(name=bone)
                vg.add(list(range(len(ob.data.vertices))), 1.0, "REPLACE")
            groups.setdefault(ob.get("mesh", "body"), []).append(ob)
        out = {}
        view = bpy.context.view_layer
        for tag, obs in groups.items():
            for o in list(bpy.context.selected_objects):
                o.select_set(False)
            # The active object keeps its data (and its shape keys); put one with keys first.
            obs.sort(key=lambda o: 0 if o.data.shape_keys else 1)
            for o in obs:
                o.select_set(True)
            view.objects.active = obs[0]
            if len(obs) > 1:
                bpy.ops.object.join()
            j = view.objects.active
            j.name = j.data.name = f"{self.name}-{tag}"
            for k in ("bone", "mesh"):
                if k in j:
                    del j[k]
            mod = j.modifiers.new("rig", "ARMATURE")
            mod.object = self.ob
            j.parent = self.ob
            j.matrix_parent_inverse = Matrix.Identity(4)
            out[tag] = j
        view.update()
        return out

    # ---- posing helpers (the rest pose is identity) --------------------------------------------------
    def rest(self):
        for pb in self.ob.pose.bones:
            pb.matrix_basis = Matrix.Identity(4)
        for pb in self.ob.pose.bones:
            pb.location = (0, 0, 0)
        bpy.context.view_layer.update()

    def turn_world(self, name, axis, deg, about=None):
        """Rotate a bone by `deg` about a world `axis` through its head (or `about`), keeping its children."""
        import math
        bpy.context.view_layer.update()
        pb = self.ob.pose.bones[name]
        M = self.ob.matrix_world @ pb.matrix
        h = Vector(about) if about is not None else M.translation.copy()
        R = Matrix.Rotation(math.radians(deg), 4, Vector(axis).normalized())
        Mw = Matrix.Translation(h) @ R @ Matrix.Translation(-h) @ M
        pb.matrix = self.ob.matrix_world.inverted() @ Mw
        bpy.context.view_layer.update()
