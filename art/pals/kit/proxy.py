"""A stand-in for a pal's face in the clip-only files (the dances, the bits).

The face's shape keys are animated by name: a glTF animation's `weights` channel has to target a node whose
mesh has those morph targets, so a clip file that animates the face has to carry a face. It need not be the
real one. `standin(face)` makes a three-vertex mesh with the same shape keys in the same order and gives it
the face's object name (the real face is renamed out of the way until `restore()`), so the clips bake onto
it and export against it; on the page the same track names bind to the real face by name, which is the only
thing three.js looks at. It saves the whole face mesh -- most of a clip file -- in every pack.
"""
from __future__ import annotations

import bpy


class StandIn:
    def __init__(self, face):
        self.face = face
        self.name = face.name
        face.name = self.name + "~real"
        me = bpy.data.meshes.new(self.name)
        me.from_pydata([(0, 0, 0), (0.001, 0, 0), (0, 0.001, 0)], [], [(0, 1, 2)])
        ob = bpy.data.objects.new(self.name, me)
        bpy.context.scene.collection.objects.link(ob)
        keys = face.data.shape_keys.key_blocks
        ob.shape_key_add(name=keys[0].name, from_mix=False)
        for kb in keys[1:]:
            k = ob.shape_key_add(name=kb.name, from_mix=False)
            k.value = 0.0
            k.data[0].co = (0, 0, 0.0001)           # not empty, or the exporter drops it as a no-op
        ob.parent = face.parent
        self.ob = ob

    def restore(self):
        bpy.data.objects.remove(self.ob)
        self.face.name = self.name
