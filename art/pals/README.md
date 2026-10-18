# Archie and his pals, in 3D

Archie, Zip and Brick, the Atlas Core Archie carries, and every prop their bits use: built, rigged, animated
and exported from Python, headless, as the first Archie was (his script, `art/archie/archie.py`, is retired:
these replace him). A change to a pal is a reviewable diff of numbers, not a binary.

```
blender -b --factory-startup --python art/pals/archie.py -- [--views front,side,back,three,face,hand]
        [--out DIR] [--samples N] [--res WxH] [--sheet-pose] [--save PATH] [--no-render]
```

| file | what it builds |
|---|---|
| `kit/geo.py` | the solids (`superquad`, `segment`, `sweep`, `tube`, `lathe`, `disc`, `ring`) and `Surface` ray casts |
| `kit/mat.py` | glTF-safe materials (`principled`, `textured`) and generated textures (`specks`, `iris`) |
| `kit/face.py` | eyes with lids and catchlights, bendable brows, a mouth with a shape key per expression |
| `kit/rig.py` | the shared skeleton's conventions, `Rig` (declare bones, build), `finalize` (parts -> skinned meshes) |
| `kit/anim.py` | `Pose`, `Track`, `Clip`, the `Skeleton` FK/IK model, `bake` to NLA tracks |
| `kit/studio.py` | sheet-style and homepage-style lights and cameras, Cycles/Eevee settings |
| `kit/export.py` | `glb()` (Blender's exporter) and `compress()` (resample, prune, meshopt) |
| `archie.py`, `zip.py`, `brick.py` | the characters |
| `reference.md` | landmarks read off the model sheets, in sheet pixels, and the cast's relative scale |

The model sheets live outside the repository (see `reference.md`).

## Conventions every pal follows

**Space.** Metres, Z up, facing -Y, the character's own left is +X, feet on Z = 0. Build in the rest pose,
in world space, left side first and mirrored (`geo.mirror`, which swaps `_L`/`_R` in the bone tag).

**Scale.** Head tops: Archie 2.25 m (crest tip 2.40, the height the homepage banner is framed for), Zip 1.75 m,
Brick 2.75 m.

**Skeleton.** The same names on every pal, so a clip, a solver or the page can address any of them:

```
root (floor) > hips > spine > chest > neck > head
head  > eye_L/R, lid_up_L/R, lid_lo_L/R, brow_in_L/R, brow_mid_L/R, brow_out_L/R, ear_L/R  (+ extras)
chest > shoulder_L/R > upper_arm_L/R > forearm_L/R > hand_L/R
hand  > thumb_1..3, index_1..3, middle_1..3, ring_1..3 (each _L/_R), grip_L/R (where a held prop goes)
hips  > thigh_L/R > shin_L/R > foot_L/R > toe_L/R
```

Extras are per character: Archie `crest_1..3` and `core` (the Atlas Core's dock, on `spine`); Zip
`horn_1_L/R`, `horn_2_L/R`. Names use underscores, never dots (three.js strips dots from node names).

**Bone axes.** Each bone's local Z leans to a hint: forward (-Y) for the trunk and limbs, the palm's side for
fingers, up for eyes and lids. +X rotation then swings the bone's tail towards that hint, so it is flexion:
thigh forward, forearm forward, a finger into the palm. A knee bends with -X. A pose written for the left
side mirrors to the right by negating Y and Z rotations (`Pose.both`, `Pose.side`).

**Face.** Eyes on `eye_*` (they turn), lids on `lid_up_*`/`lid_lo_*` (built open; a blink turns them back),
brows skinned across `brow_in/mid/out_*`, and one `mouth` mesh with these shape keys, which every pal has:
`rest` (basis), `grin`, `smile`, `wide`, `open`, `oh`, `frown`, `flat`, `smirk_L`, `smirk_R`, `grit`, `ee`.
Each character module defines `REST_FACE`, the weights of its everyday expression (Archie: `grin` 1).

**Meshes.** `rig.finalize()` joins every part into one skinned body mesh (one draw call per material) and
the mouth and brows into one small face mesh (the only one with shape keys). Parts are rigid: weight 1 on
their bone, except the few that bend (brows, Archie's crest), which carry their own vertex groups.

**Materials.** `mat.principled` with plain inputs only, so glTF gets exactly what Blender renders; textures
go straight into Base Color (`mat.textured`) and need UVs (`geo.box_uv`). Backface culling on: every part
is a closed shell.

**Budget.** About 40-80k triangles a character. Shells are smooth-shaded superquads at a resolution chosen
per part; subdivision only where a small part needs it (the crest).

**Module shape.** A character module exposes `build() -> (rig, parts, materials)`, `REST_FACE`,
`sheet_pose(rig)` and a `main()` that understands the flags above, guarded by `if __name__ == "__main__"`
so animation scripts can import it.

## Checking a pal against its sheet

From `E:/Development Workspaces/Archie and Pals/`: `tools/cmp.sh <pal> <tag>` renders the front and side
views orthographically (2.85 m tall frame, 750x1000) and lays each next to the sheet's view at the sheet's
own scale with a 50% overlay, floors and centre lines aligned (`tools/compare.py`). `tools/viewer/` is a
three.js viewer lit the way the homepage is (`?glb=...&clip=...&view=front|three|site|face`), served by
`python -m http.server 8765` from that folder.
