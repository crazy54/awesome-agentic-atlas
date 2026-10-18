"""Bootleg Archie: Archie stands, dignified, and Zip sneaks up beside him with a remote and clicks it at the
Atlas Core in Archie's belly. It opens by itself and projects -- not the page's world's usual show, but a
tiny, big-headed, hologram Archie on it (the holo-archie prop), lecturing, finger raised, in pompous
bubbles. Real Archie folds his arms. Tiny Archie folds his arms. Real Archie wags a finger at it ("Stop
that."); so does Tiny Archie. Zip cracks up, and whips the remote behind his back, whistling, as Archie
presses the Core shut and goes. Zip, alone, clicks once more at
where he went: from off the edge of the window, "Ahem! I am ARCH--", "ZIP!", and Zip runs.

FORMATION (metres across the page from Archie's root, both on the window's floor, facing the reader):

    archie   (0, 0)
    zip      (ZIP_X, 0), on Archie's left (screen right); the projection floats up between them

Archie's pieces (clips/archie_base.py). WATCH is REST with his head up and to his left, on the projection;
FOLDED his arms folded, chin up, the same way. Tiny Archie, on Archie's skeleton, plays the ones marked *
a beat after him.

    bootleg-archie/startle   REST -> WATCH: the Core opens by itself: a jolt, a look down at his belly, up
    bootleg-archie/watch     WATCH, looping: watching it, unamused
    bootleg-archie/fold *    WATCH -> FOLDED: the arms folded, the lids heavy
    bootleg-archie/folded *  FOLDED, looping: a toe tapping
    bootleg-archie/wag *     FOLDED -> FOLDED: the left hand out of the fold, a finger wagged up at it
    bootleg-archie/shut      FOLDED -> REST: the arms unfolded, the right palm pressed on the Core (PRESS s:
                             the page folds it), and a sniff

Zip's (clips/zip_base.py); the remote is the remote-zip prop in grip_R, from REMOTE s in `remote`:

    bootleg-archie/remote    REST -> AIM: the right hand behind his back and out with the remote, aimed at
                             Archie's belly (on his right), a click (CLICK s)
    bootleg-archie/aim       AIM, looping: thumb on the button, a hand over his mouth, snickering
    bootleg-archie/hide      REST -> HIDE: both hands whipped behind his back, eyes to the ceiling
    bootleg-archie/innocent  HIDE, looping: rocking heel to toe, whistling
    bootleg-archie/again     HIDE -> REST: the remote out again, aimed off to his right (where Archie went),
                             a click (AGAIN s), a snicker, and the hand down
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import blink_layer, breathe, brows, look
from kit.anim import Clip, Pose, pulse, smooth
from . import _corekit as K

NAME = "bootleg-archie"
CAST = ("archie", "zip")
ZIP_X = 3.4
PRESS = 0.95                          # shut: his palm on the Core
REMOTE, CLICK = 0.7, 1.35             # remote: the remote in his hand; the click
AGAIN = 1.0                           # again: the click
PROJ = (14, 30)                       # Archie's eyes on the projection: up, to his left (degrees)


def V(*a):
    return Vector(a)


def clips(bodies):
    out = {}
    if "archie" in bodies:
        out["archie"] = archie_clips(bodies["archie"])
    if "zip" in bodies:
        out["zip"] = zip_clips(bodies["zip"])
    return out


# ============================================================================================== Archie
def archie_clips(body):
    L = body.lib
    n = lambda piece: f"{NAME}/{piece}"           # noqa: E731
    RW = {sg: K.rest_wrist(body, sg) for sg in (1, -1)}
    out = []

    def lids(p, k):
        p.both("lid_up", x=-46 * k, add=True)
        p.both("lid_lo", x=40 * k, add=True)

    watch = L.REST.copy()
    watch.set("head", -8, 16, 6)
    watch.face = {"grin": 0.3}
    folded = L.REST.copy()
    folded.set("head", -14, 14, 4)
    folded.set("chest", -4, 6, 0)
    folded.face = {"flat": 1.0, "grin": 0.0}
    FOLD = {1: V(-0.12, -0.37, 1.41), -1: V(0.13, -0.39, 1.35)}      # the wrists, folded (left over right)
    FOLD_ROT = {1: L.hand_world((-1, 0.1, 0.1), (0, 1, -0.2)), -1: L.hand_world((1, 0.1, -0.1), (0, 1, 0.2))}

    def arms(p, k=1.0, skip=0):
        """The arms folded, k of the way from hanging (`skip` a side to leave to the caller)."""
        for sg in (1, -1):
            if sg == skip:
                continue
            body.hand_to(p, sg, RW[sg].lerp(FOLD[sg], k), elbow=(0.5, -0.4, -0.4),
                         hand_rot=FOLD_ROT[sg] if k > 0.5 else None)
            p.fingers(sg, 20 + 30 * k, spread=2, thumb=15)

    def stand(p, tap=0.0):
        body.plant(p, 1)
        body.plant(p, -1, roll=-14 * tap)

    def on_it(k=1.0):
        return look((PROJ[0] * k, PROJ[1] * k))

    # ---- startle -------------------------------------------------------------------------------------
    T = 2.0
    c = Clip(n("startle"), T)
    c.key(0.0, L.REST)
    down = L.REST.copy()
    down.set("head", 26, 0, 0)
    down.set("chest", 8, 0, 0)
    down.face = {"wide": 0.8, "oh": 0.5}
    c.key(0.25, down, "snap")
    c.key(0.9, down, "linear")
    c.key(1.5, watch, "inout")
    c.key(T, watch, "linear")

    def startle_solve(t, p, skel, T=T):
        jump = pulse(t, 0.0, 0.06, 0.1, 0.3)
        k = pulse(t, 0.05, 0.12, 0.7, 0.45)
        L.hips(body, p, dz=0.05 * jump)
        for sg in (1, -1):
            if k > 0.01:
                body.hand_to(p, sg, RW[sg].lerp(V(sg * 0.5, -0.36, 1.55), k), elbow=(0.6, 0.2, -0.5),
                             hand_rot=L.hand_world((sg * 0.3, -0.1, 1), (0, -1, 0)) if k > 0.5 else None)
                L.open_hand(p, sg, 12 * k)                     # whoa
        body.plant(p, 1, lift=0.05 * jump)
        body.plant(p, -1, lift=0.04 * jump)
        return p

    c.solve(startle_solve)

    def startle_face(t, T=T):
        p = Pose()
        d = pulse(t, 0.1, 0.12, 0.8, 0.3)
        u = smooth(1.0, 1.5, t)
        brows(p, 2.0 * d, 2.2 * d, 1.4 * d)
        p.add("crest_2", 10 * pulse(t, 0.0, 0.05, 0.1, 0.3), 0, 0)
        p.add("crest_3", 16 * pulse(t, 0.0, 0.05, 0.1, 0.3), 0, 0)
        return p + look((-30 * d, 0)) + on_it(u)

    c.layer(startle_face)
    out.append(c)

    # ---- watch (loop) --------------------------------------------------------------------------------
    T = 4.0
    c = K.loop_clip(n("watch"), T)
    c.key(0.0, watch)
    c.solve(lambda t, p, skel: (stand(p), p)[1])

    def watch_face(t, T=T):
        p = on_it()
        brows(p, -0.4, 0.0, 0.3)
        return p

    c.layer(watch_face)
    c.layer(breathe(T / 2, 0.8))
    c.layer(blink_layer([1.3]))
    out.append(c)

    # ---- fold ----------------------------------------------------------------------------------------
    T = 1.4
    c = Clip(n("fold"), T)
    c.key(0.0, watch)
    c.key(0.9, folded, "inout")
    c.key(T, folded, "linear")

    def fold_solve(t, p, skel, T=T):
        arms(p, smooth(0.05, 0.85, t))
        L.hips(body, p, dx=0.02 * smooth(0.3, 0.9, t), roll=-2 * smooth(0.3, 0.9, t))
        stand(p)
        return p

    c.solve(fold_solve)

    def fold_face(t, T=T):
        p = on_it()
        k = smooth(0.4, 0.9, t)
        lids(p, 0.3 * k)
        brows(p, -0.6 * k, -0.2 * k, 0.4 * k)
        return p

    c.layer(fold_face)
    out.append(c)

    # ---- folded (loop) -------------------------------------------------------------------------------
    T = 2.0
    c = K.loop_clip(n("folded"), T)
    c.key(0.0, folded)

    def folded_solve(t, p, skel, T=T):
        u = t / T
        arms(p)
        L.hips(body, p, dx=0.02, roll=-2)
        stand(p, max(0.0, math.sin(math.tau * 2 * u)) ** 2)
        return p

    c.solve(folded_solve)

    def folded_face(t, T=T):
        p = on_it()
        lids(p, 0.3)
        brows(p, -0.6, -0.2, 0.4)
        return p

    c.layer(folded_face)
    c.layer(blink_layer([1.1]))
    out.append(c)

    # ---- wag -----------------------------------------------------------------------------------------
    T = 2.4
    c = Clip(n("wag"), T)
    c.key(0.0, folded)
    c.key(T, folded)
    WAG = V(0.5, -0.5, 1.78)

    def wag_solve(t, p, skel, T=T):
        k = pulse(t, 0.15, 0.3, 1.45, 0.4)
        arms(p, skip=1)
        sw = math.sin(math.tau * 3 * (t - 0.45)) * smooth(0.4, 0.55, t) * (1 - smooth(1.7, 1.9, t))
        body.hand_to(p, 1, FOLD[1].lerp(WAG, k), elbow=(0.6, 0.0, -0.5),
                     hand_rot=L.hand_world((0.25 + 0.4 * sw, -0.2, 1), (0.7, -0.6, 0.2)) if k > 0.5 else None)
        if k > 0.5:
            L.point(p, 1)
        else:
            p.fingers(1, 50, spread=2, thumb=15)
        L.hips(body, p, dx=0.02, roll=-2)
        stand(p)
        return p

    c.solve(wag_solve)

    def wag_face(t, T=T):
        p = on_it()
        k = pulse(t, 0.2, 0.3, 1.4, 0.4)
        lids(p, 0.3 + 0.15 * k)
        brows(p, -0.6 - 0.6 * k, -0.2, 0.4 + 0.4 * k)
        p.face.update({"grit": 0.4 * k})
        return p

    c.layer(wag_face)
    out.append(c)

    # ---- shut ----------------------------------------------------------------------------------------
    T = 2.0
    c = Clip(n("shut"), T)
    c.key(0.0, folded)
    look_down = L.REST.copy()
    look_down.set("head", 20, 0, 0)
    look_down.face = {"flat": 0.8, "grin": 0.0}
    smug = L.REST.copy()
    smug.set("head", -8, -4, 0)
    smug.face = {"grin": 0.6, "smirk_R": 0.5}
    c.key(0.55, look_down, "inout")
    c.key(1.15, look_down, "linear")
    c.key(1.6, smug, "inout")
    c.key(T, L.REST, "inout")
    CORE_W = V(-0.1, -0.36, 1.2)                # his right wrist, the palm flat on the Core in his belly

    def shut_solve(t, p, skel, T=T):
        un = 1 - smooth(0.0, 0.45, t)
        arms(p, un, skip=-1)
        k = pulse(t, 0.25, 0.45, 0.45, 0.5)
        press = 0.03 * pulse(t, PRESS - 0.05, 0.05, 0.1, 0.15)
        tgt = FOLD[-1].lerp(RW[-1], smooth(0.0, 0.3, t)).lerp(CORE_W + V(0, press, 0), k)
        body.hand_to(p, -1, tgt if t > 0.25 else FOLD[-1].lerp(RW[-1], smooth(0.0, 0.3, t)), elbow=(0.5, 0.3, -0.6),
                     hand_rot=L.hand_world((1, 0, -0.1), (0, 1, 0)) if k > 0.5 else None)
        L.open_hand(p, -1, 4)
        stand(p)
        return p

    c.solve(shut_solve)

    def shut_face(t, T=T):
        p = Pose()
        d = pulse(t, 0.4, 0.2, 0.7, 0.3)
        p = p + look((-26 * d, 0))
        lids(p, 0.3 * (1 - smooth(1.2, 1.6, t)))
        sniff = pulse(t, 1.4, 0.1, 0.3, 0.2)
        p.add("head", -6 * sniff, 0, 0)
        return p

    c.layer(shut_face)
    c.layer(blink_layer([1.7]))
    out.append(c)
    return out


# ================================================================================================= Zip
def zip_clips(body):
    L = body.lib
    RW = L.rest_wrists(body)
    out = []
    behind = L.hand_world((0, 0.3, -1), (0, 1, 0))
    hide_w = {1: V(0.1, 0.26, 0.86), -1: V(-0.1, 0.26, 0.88)}
    AIM_W = V(-0.42, -0.36, 1.0)                                    # the remote out at Archie, on his right
    aim_rot = L.hand_world((-0.85, -0.45, 0.25), (0, 0, -1))        # fingers (and the remote) at him, palm down
    OFF_W = V(-0.46, -0.24, 1.06)                                   # ... and off to his right, along the floor
    off_rot = L.hand_world((-0.95, -0.15, 0.25), (0, 0, -1))
    MOUTH = V(0.06, -0.44, 1.18)                                    # the left hand over his mouth
    mouth_rot = L.hand_world((-0.3, -0.1, 1), (0, 1, 0))

    def hidden(p, k=1.0, wob=0.0):
        for sg in (1, -1):
            body.hand_to(p, sg, RW[sg].lerp(hide_w[sg] + V(0, 0, 0.02 * wob * sg), k), elbow=(0.5, 0.6, -0.4),
                         hand_rot=behind if k > 0.6 else None)
            L.fist(p, sg, 0.5 * k)

    def thumb(p, click=0.0):
        p.set("thumb_2_R", 20 + 40 * click, 0, 0)
        p.set("thumb_3_R", 20 + 40 * click, 0, 0)

    aim = L.REST.copy()
    aim.set("chest", 4, -10, 0)
    aim.set("head", 2, -12, 0)
    aim.face = {"grin": 0.8, "smirk_R": 0.6}
    hide = L.REST.copy()
    hide.face = {"grin": 0.6, "smile": 0.4}

    # ---- remote --------------------------------------------------------------------------------------
    T = 2.0
    c = Clip(f"{NAME}/remote", T)
    c.key(0.0, L.REST)
    c.key(T, aim)

    def remote_solve(t, p, skel, T=T):
        back = pulse(t, 0.1, 0.35, 0.2, 0.25)
        if back > 0.01 and t < REMOTE:
            body.hand_to(p, -1, RW[-1].lerp(hide_w[-1], back), elbow=(0.5, 0.6, -0.4))
        k = smooth(REMOTE, REMOTE + 0.45, t)
        if k > 0.01:
            cur = hide_w[-1].lerp(RW[-1], 1 - back) if back > 0.01 else RW[-1]
            body.hand_to(p, -1, cur.lerp(AIM_W, k), elbow=(0.5, 0.2, -0.5), hand_rot=aim_rot if k > 0.5 else None)
        L.fist(p, -1, smooth(0.45, REMOTE, t) * 0.7)
        thumb(p, pulse(t, CLICK - 0.05, 0.05, 0.05, 0.12))
        L.hips(body, p, roll=3 * k, yaw=-6 * k)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(remote_solve)

    def remote_face(t, T=T):
        sly = pulse(t, 0.3, 0.15, 0.6, 0.2)
        at = smooth(REMOTE + 0.2, CLICK, t)
        p = look((-4 * sly - 8 * at, -20 * sly - 24 * at), head=(0, 0, -10 * sly))
        brows(p, 0.0, 1.6 * sly, 1.2 * sly, side=1)
        brows(p, -0.8 * at, -0.3 * at, 0.4 * at)
        p.face.update({"grin": 1 - 0.4 * sly, "smirk_L": 0.8 * sly, "smirk_R": 0.6 * at})
        L.squint(p, 0.4 * sly + 0.3 * at)
        L.horns(p, x=6 * L.ring(t, CLICK, 18, 6))
        return p

    c.layer(remote_face)
    out.append(c)

    # ---- aim (loop) ----------------------------------------------------------------------------------
    T = 1.6
    c = L.looped(f"{NAME}/aim", T)
    c.key(0.0, aim)

    def aim_solve(t, p, skel, T=T):
        u = t / T
        sh = math.sin(math.tau * 4 * u)
        L.hips(body, p, dz=0.008 * sh, roll=3, yaw=-6)
        p.both("shoulder", z=4 * sh, add=True)
        body.hand_to(p, -1, AIM_W + V(0, 0, 0.01 * sh), elbow=(0.5, 0.2, -0.5), hand_rot=aim_rot)
        L.fist(p, -1, 0.7)
        thumb(p, max(0.0, math.sin(math.tau * 2 * u)) ** 4)
        body.hand_to(p, 1, MOUTH + V(0, 0, 0.01 * sh), elbow=(0.5, 0.3, -0.6), hand_rot=mouth_rot)
        L.open_hand(p, 1, 4)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(aim_solve)

    def aim_face(t, T=T):
        u = t / T
        p = look((22, -22 + 3 * math.sin(math.tau * u)))           # up at the projection, on his right
        L.squint(p, 0.6 + 0.2 * math.sin(math.tau * 4 * u))
        brows(p, 0.4, 1.0, 0.8)
        p.face.update({"grin": 1.0})
        L.horns(p, x=3 * math.sin(math.tau * 4 * u))
        return p

    c.layer(aim_face)
    out.append(c)

    # ---- hide ----------------------------------------------------------------------------------------
    T = 1.2
    c = Clip(f"{NAME}/hide", T)
    c.key(0.0, L.REST)
    c.key(0.3, hide)
    c.key(T, hide, "linear")

    def hide_solve(t, p, skel, T=T):
        hidden(p, smooth(0.0, 0.3, t))
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(hide_solve)

    def hide_face(t, T=T):
        up = smooth(0.3, 0.6, t)
        p = look((26 * up, -4), head=(-8 * up, 0, 0))
        brows(p, 1.4 * up + 1.6 * pulse(t, 0.0, 0.06, 0.2, 0.2), 1.6, 1.0)
        p.face.update({"grin": 0.0, "wide": pulse(t, 0.0, 0.06, 0.25, 0.2), "oh": 0.6 * up})
        L.horns(p, x=10 * L.ring(t, 0.05, 20, 5))
        return p

    c.layer(hide_face)
    out.append(c)

    # ---- innocent (loop) -----------------------------------------------------------------------------
    T = 2.4
    c = L.looped(f"{NAME}/innocent", T)
    c.key(0.0, hide)

    def innocent_solve(t, p, skel, T=T):
        rock = math.sin(math.tau * t / T)
        L.hips(body, p, dy=0.015 * rock, dz=0.01 * abs(rock), pitch=-2 * rock)
        hidden(p, 1.0, rock)
        body.plant(p, 1, roll=-16 * max(0.0, -rock) + 12 * max(0.0, rock))
        body.plant(p, -1, roll=-16 * max(0.0, -rock) + 12 * max(0.0, rock))
        return p

    c.solve(innocent_solve)

    def innocent_face(t, T=T):
        u = t / T
        p = look((26, 14 * math.sin(math.tau * u)), head=(-8, 6 * math.sin(math.tau * u), 4 * math.sin(math.tau * u)))
        brows(p, 1.4, 1.6, 1.0)
        w = 0.5 + 0.5 * math.sin(math.tau * 4 * u)
        p.face.update({"grin": 0.0, "oh": 0.5 + 0.3 * w, "smile": 0.2})
        return p

    c.layer(innocent_face)
    out.append(c)

    # ---- again ---------------------------------------------------------------------------------------
    T = 2.2
    c = Clip(f"{NAME}/again", T)
    c.key(0.0, hide)
    c.key(T, L.REST)

    def again_solve(t, p, skel, T=T):
        k = pulse(t, 0.2, 0.45, 1.0, 0.5)
        hidden(p, 1 - smooth(0.1, 0.4, t))
        if k > 0.01:
            body.hand_to(p, -1, hide_w[-1].lerp(OFF_W, k) if t < 1.0 else RW[-1].lerp(OFF_W, k),
                         elbow=(0.5, 0.2, -0.5), hand_rot=off_rot if k > 0.5 else None)
            L.fist(p, -1, 0.7)
        thumb(p, pulse(t, AGAIN - 0.05, 0.05, 0.05, 0.12))
        sh = math.sin(math.tau * 8 * t) * pulse(t, AGAIN + 0.1, 0.1, 0.6, 0.3)
        p.both("shoulder", z=4 * sh, add=True)
        L.hips(body, p, dz=0.008 * sh, yaw=-8 * k)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(again_solve)

    def again_face(t, T=T):
        k = pulse(t, 0.1, 0.4, 1.2, 0.4)
        p = look((-4 * k, -30 * k), head=(0, 0, -20 * k))
        p.face.update({"grin": 0.4 + 0.6 * k, "smirk_R": 0.8 * k, "oh": 0.0})
        L.squint(p, 0.5 * k)
        brows(p, -0.8 * k, 0.4 * k, 1.2 * k)
        L.horns(p, x=6 * L.ring(t, AGAIN, 18, 6))
        return p

    c.layer(again_face)
    out.append(c)
    return out
