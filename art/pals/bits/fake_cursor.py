"""The fake cursor: Zip, with a remote, flies an oversized, obviously theatrical pointer at Archie -- a prop;
the reader's own cursor is never touched -- and pokes him with it. Archie jumps, looks round; the pointer
pokes again and he swats at it; it hovers in front of his face, wobbling, taunting. He snatches it out of the
air, looks from it to Zip (who has hidden the remote and is whistling), and twists it, squeaking, into a
balloon dog, which he hands to Zip. Zip hugs it.

FORMATION (metres across the page from Archie's root, both standing on the same floor, facing the reader):

    archie   (0, 0)
    zip      (ZIP_X, 0), on Archie's left (screen right); for the hand-over the page walks Zip in to
             (GIVE_X, 0)

Archie's pieces (clips/archie_base.py):

    fake-cursor/poked    jumps (the pointer has poked his left shoulder), a hand to it, a look round
    fake-cursor/swat     poked on the head: swats the air over it with his right hand, and misses
    fake-cursor/grab     eyes narrowed on the pointer hovering by his face, a snatch with the left hand at
                         ARCHIE_GRAB (his frame) at GRAB s, the pointer brought in to his chest: ends HOLDING
    fake-cursor/twist    HOLDING -> PRESENT: a long look at Zip, then both hands at it, twisting like a
                         balloon artist (the page plays
                         the pointer's `bend`); at POP s the page swaps it for the balloon dog, held up
    fake-cursor/give     PRESENT -> REST: stoops to his left and holds it out to Zip; at HANDOFF s it goes
                         from his grip_L to Zip's grip_R

Zip's pieces (clips/zip_base.py):

    fake-cursor/deploy   the right hand behind his back and out with the remote (grip_R from REMOTE s), a
                         thumb on the button (the pointer pops into being at CLICK s), a sly look
    fake-cursor/drive    looping: both hands on the remote, leaning into the steering, eyes on the pointer
    fake-cursor/caught   drive -> HIDE: freezes, whips the remote behind his back, eyes to the ceiling
    fake-cursor/innocent HIDE, looping: rocking heel to toe, whistling
    fake-cursor/take     HIDE -> HUG: reaches up for the dog (HANDOFF s, into grip_R), hugs it
    fake-cursor/hug      HUG, looping: swaying with it, eyes squeezed shut with joy
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import blink_layer, brows, look
from kit.anim import Clip, Pose, pulse, smooth

NAME = "fake-cursor"
CAST = ("archie", "zip")
ZIP_X, GIVE_X = 3.4, 1.3
ARCHIE_GRAB = (0.55, -0.42, 1.95)      # his left wrist at the snatch
GRAB = 0.62                            # grab: the pointer is in his hand
POP = 2.85                             # twist: the pointer becomes a balloon dog
HANDOFF = 0.95                         # give / take: the dog changes hands
REMOTE, CLICK = 0.7, 1.35              # deploy: the remote in his hand; the pointer appears


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
    RW = {sg: L.wrist_of(body, planted(body, L), sg) for sg in (1, -1)}
    out = []

    def lids(p, k):
        p.both("lid_up", x=-46 * k, add=True)
        p.both("lid_lo", x=40 * k, add=True)

    # ---- poked ---------------------------------------------------------------------------------------
    T = 2.0
    c = Clip(f"{NAME}/poked", T)
    c.key(0.0, L.REST)

    def poked_solve(t, p, skel, T=T):
        jump = pulse(t, 0.0, 0.05, 0.08, 0.35)
        rub = pulse(t, 0.2, 0.25, 0.8, 0.4)
        L.hips(body, p, dz=0.05 * jump, dx=-0.05 * jump, roll=4 * jump)
        p.add("chest", -6 * jump, 0, 4 * jump)
        if rub > 0.01:
            body.hand_to(p, -1, RW[-1].lerp(V(0.26, -0.24, 1.58), rub), elbow=(0.5, 0.2, -0.6),
                         hand_rot=L.hand_world((1, 0, 0.2), (0, 1, 0)) if rub > 0.5 else None)
            L.open_hand(p, -1, 4)
        body.plant(p, 1, lift=0.06 * jump)
        body.plant(p, -1, lift=0.04 * jump)
        return p

    c.solve(poked_solve)

    def poked_face(t, T=T):
        p = Pose()
        jump = pulse(t, 0.0, 0.04, 0.2, 0.3)
        round_ = math.sin(math.tau * (t - 0.4) / 1.2) * pulse(t, 0.4, 0.15, 0.9, 0.3)
        p = p + look((0, 24 * round_ + 20 * pulse(t, 0.05, 0.1, 0.3, 0.2)), head=(0, 0, 30 * round_ + 22 * pulse(t, 0.05, 0.1, 0.3, 0.2)))
        p.face.update({"grin": 1 - jump - 0.6 * abs(round_), "wide": jump, "flat": 0.6 * abs(round_)})
        brows(p, 2.0 * jump, 2.0 * jump, 1.4 * jump)
        brows(p, -0.8 * abs(round_), -0.3 * abs(round_), 0.4 * abs(round_))
        p.add("crest_2", 10 * jump, 0, 0)
        p.add("crest_3", 14 * jump, 0, 0)
        return p

    c.layer(poked_face)
    c.layer(blink_layer([1.6]))
    out.append(c)

    # ---- swat ----------------------------------------------------------------------------------------
    T = 1.6
    c = Clip(f"{NAME}/swat", T)
    c.key(0.0, L.REST)

    def swat_solve(t, p, skel, T=T):
        duck = pulse(t, 0.0, 0.06, 0.15, 0.3)
        sw = pulse(t, 0.2, 0.18, 0.15, 0.4)
        arc = smooth(0.25, 0.55, t)
        L.hips(body, p, dz=-0.06 * duck, pitch=6 * duck)
        p.add("head", 12 * duck, 0, 0)
        if sw > 0.01:
            tgt = V(-0.3, -0.25, 2.35).lerp(V(0.35, -0.3, 2.3), arc)
            body.hand_to(p, -1, RW[-1].lerp(tgt, sw), elbow=(0.5, 0.2, -0.3),
                         hand_rot=L.hand_world((0.6, -0.2, 0.5), (0, -0.3, 1)) if sw > 0.5 else None)
            L.open_hand(p, -1, 10 * sw)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(swat_solve)

    def swat_face(t, T=T):
        p = Pose()
        g = pulse(t, 0.0, 0.08, 1.0, 0.3)
        p = p + look((20 * g, 8 * smooth(0.25, 0.55, t) * g))
        p.face.update({"grin": 1 - g, "grit": g})
        brows(p, -1.2 * g, -0.6 * g, 0.4 * g)
        p.add("crest_3", -8 * pulse(t, 0.0, 0.06, 0.15, 0.3), 0, 0)
        return p

    c.layer(swat_face)
    out.append(c)

    # ---- grab ----------------------------------------------------------------------------------------
    holding = L.REST.copy()
    holding.set("head", 10, 4, 0)
    holding.face = {"flat": 0.7, "smirk_R": 0.4}
    HOLD_W = V(0.1, -0.42, 1.4)                # his left wrist holding it in front of his chest
    hold_rot = L.hand_world((-0.2, -0.5, 1), (-1, 0, 0))

    T = 1.8
    c = Clip(f"{NAME}/grab", T)
    c.key(0.0, L.REST)
    c.key(T, holding)

    def grab_solve(t, p, skel, T=T):
        snatch = smooth(GRAB - 0.14, GRAB, t)
        down = smooth(GRAB + 0.3, T, t)
        tgt = V(*ARCHIE_GRAB).lerp(HOLD_W, down)
        k = snatch
        body.hand_to(p, 1, RW[1].lerp(tgt, k), elbow=(0.55, 0.3, -0.5), hand_rot=hold_rot if k > 0.5 else None)
        if snatch > 0.5:
            L.fist(p, 1, 0.75)
        L.hips(body, p, dz=-0.03 * pulse(t, GRAB, 0.05, 0.05, 0.25))
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(grab_solve)

    def grab_face(t, T=T):
        p = Pose()
        narrow = pulse(t, 0.0, 0.25, 0.25, 0.1)
        got = smooth(GRAB, GRAB + 0.3, t)
        p = p + look((14 * (1 - got) - 10 * got, 16 * (1 - got)))
        lids(p, 0.4 * narrow)
        brows(p, -1.2 * narrow, -0.6 * narrow, 0.2 * narrow)
        p.face.update({"grin": 0.3 * narrow})
        return p

    c.layer(grab_face)
    out.append(c)

    # ---- twist ---------------------------------------------------------------------------------------
    present = L.REST.copy()
    present.set("head", -2, 6, 6)
    present.set("chest", -4, 4, 0)
    present.face = {"grin": 1.0}
    PRES_W = V(0.6, -0.36, 1.7)                # held up out to his left, clear of his white front
    pres_rot = L.hand_world((-0.3, -0.4, 1), (-1, 0, 0))
    T = 3.6
    c = Clip(f"{NAME}/twist", T)
    c.key(0.0, holding)
    c.key(T, present)

    def twist_solve(t, p, skel, T=T):
        work = pulse(t, 1.0, 0.25, POP - 1.35, 0.1)
        tw = math.sin(math.tau * 2.2 * t)
        show = smooth(POP, POP + 0.4, t)
        lw = HOLD_W.lerp(PRES_W, show)
        body.hand_to(p, 1, lw + V(0.02 * tw * work, 0, 0.02 * tw * work), elbow=(0.55, 0.3, -0.5),
                     hand_rot=hold_rot if show < 0.5 else pres_rot)
        L.fist(p, 1, 0.7)
        if work > 0.01:
            rt = HOLD_W + V(-0.16 + 0.03 * tw, -0.02, 0.06 * tw)
            body.hand_to(p, -1, RW[-1].lerp(rt, work), elbow=(0.5, 0.3, -0.6),
                         hand_rot=L.hand_world((1, -0.3, 0.3 * tw), (0, 0.2, 1)) if work > 0.5 else None)
            L.fist(p, -1, 0.6 * work)
        p.add("chest", 0, 4 * tw * work, 0)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(twist_solve)

    def twist_face(t, T=T):
        p = Pose()
        work = pulse(t, 1.0, 0.25, POP - 1.35, 0.1)
        pop = pulse(t, POP, 0.04, 0.1, 0.3)
        at_zip = pulse(t, 0.0, 0.25, 0.45, 0.25)               # a long look at Zip, on his left
        p = p + look((-22 * work, 4 * math.sin(math.tau * 2.2 * t) * work + 28 * at_zip),
                     head=(0, 0, 26 * at_zip))
        lids(p, 0.35 * at_zip)
        brows(p, -1.0 * at_zip, -0.4 * at_zip, 0.3 * at_zip)
        p.face.update({"grin": 1 - work * 0.5, "smirk_L": 0.6 * work, "wide": pop})
        brows(p, 1.6 * pop, 1.8 * pop, 1.2 * pop)
        lids(p, -0.0)
        return p

    c.layer(twist_face)
    c.layer(blink_layer([1.4, POP + 0.6]))
    out.append(c)

    # ---- give ----------------------------------------------------------------------------------------
    T = 1.8
    c = Clip(f"{NAME}/give", T)
    c.key(0.0, present)
    c.key(0.8, present)
    c.key(T, L.REST)

    def give_solve(t, p, skel, T=T):
        reach = pulse(t, 0.0, 0.7, 0.3, 0.6)
        L.hips(body, p, dx=0.06 * reach, roll=-6 * reach, pitch=8 * reach)
        p.add("chest", 8 * reach, 0, -6 * reach)
        tgt = PRES_W.lerp(V(0.78, -0.3, 1.02), reach)
        k = 1 - smooth(HANDOFF + 0.3, T, t)
        body.hand_to(p, 1, RW[1].lerp(tgt, k), elbow=(0.6, 0.2, -0.4), hand_rot=pres_rot if k > 0.5 else None)
        L.fist(p, 1, 0.7 * (1 - smooth(HANDOFF, HANDOFF + 0.15, t)))
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(give_solve)
    c.layer(lambda t, T=T: look((-14 * pulse(t, 0.2, 0.3, 0.8, 0.3), 20 * pulse(t, 0.2, 0.3, 0.8, 0.3))))
    out.append(c)
    return out


def planted(body, L):
    q = L.REST.copy()
    body.plant(q, 1)
    body.plant(q, -1)
    return q


# ================================================================================================= Zip
def zip_clips(body):
    L = body.lib
    RW = L.rest_wrists(body)
    out = []
    behind = L.hand_world((0, 0.3, -1), (0, 1, 0))
    hide_w = {1: V(0.1, 0.26, 0.86), -1: V(-0.1, 0.26, 0.88)}

    def hidden(p, k=1.0, wob=0.0):
        for sg in (1, -1):
            body.hand_to(p, sg, RW[sg].lerp(hide_w[sg] + V(0, 0, 0.02 * wob * sg), k), elbow=(0.5, 0.6, -0.4),
                         hand_rot=behind if k > 0.6 else None)
            L.fist(p, sg, 0.5 * k)

    # remote at the chest: right hand on it, thumb working, left cupped under
    RM = V(-0.06, -0.36, 0.98)
    rm_rot = L.hand_world((0.25, -0.3, 1), (0.3, 1, 0.2))

    def driving(p, k=1.0, thumb=0.0):
        body.hand_to(p, -1, RW[-1].lerp(RM, k), elbow=(0.5, 0.3, -0.5), hand_rot=rm_rot if k > 0.5 else None)
        L.fist(p, -1, 0.7 * k)
        p.set("thumb_2_R", 20 * k + 30 * thumb, 0, 0)
        p.set("thumb_3_R", 20 * k + 30 * thumb, 0, 0)
        if k > 0.01:
            body.hand_to(p, 1, RW[1].lerp(RM + V(0.12, 0.02, -0.04), k), elbow=(0.5, 0.3, -0.5),
                         hand_rot=L.hand_world((-0.6, -0.3, 0.6), (0, 0, 1)) if k > 0.5 else None)
            p.fingers(1, 40 * k, thumb=20)

    hide = L.REST.copy()
    hide.face = {"grin": 0.6, "smile": 0.4}
    drive = L.REST.copy()
    drive.set("chest", 8, -6, 0)
    drive.set("head", 4, -14, 0)
    drive.face = {"grin": 0.8, "smirk_R": 0.6}

    # ---- deploy --------------------------------------------------------------------------------------
    T = 2.2
    c = Clip(f"{NAME}/deploy", T)
    c.key(0.0, L.REST)
    c.key(T, drive)

    def deploy_solve(t, p, skel, T=T):
        back = pulse(t, 0.1, 0.35, 0.2, 0.25)
        if back > 0.01:
            body.hand_to(p, -1, RW[-1].lerp(hide_w[-1], back), elbow=(0.5, 0.6, -0.4))
        k = smooth(REMOTE, REMOTE + 0.45, t)
        if k > 0.01:
            cur = L.wrist_of(body, p, -1)
            body.hand_to(p, -1, cur.lerp(RM + V(0, -0.04, 0.12 * (1 - smooth(CLICK, T, t))), k), elbow=(0.5, 0.3, -0.5),
                         hand_rot=rm_rot if k > 0.5 else None)
        L.fist(p, -1, smooth(0.45, REMOTE, t) * 0.7)
        click = pulse(t, CLICK - 0.05, 0.05, 0.05, 0.12)
        p.set("thumb_2_R", 20 + 40 * click, 0, 0)
        p.set("thumb_3_R", 20 + 40 * click, 0, 0)
        left = smooth(CLICK + 0.2, T, t)
        if left > 0.01:
            body.hand_to(p, 1, RW[1].lerp(RM + V(0.12, 0.02, -0.04), left), elbow=(0.5, 0.3, -0.5),
                         hand_rot=L.hand_world((-0.6, -0.3, 0.6), (0, 0, 1)) if left > 0.5 else None)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(deploy_solve)

    def deploy_face(t, T=T):
        p = Pose()
        sly = pulse(t, 0.4, 0.15, 0.6, 0.2)
        p = p + look((-6 * sly, -20 * sly), head=(0, 0, -10 * sly))
        brows(p, 0.0, 1.6 * sly, 1.2 * sly, side=1)
        p.face.update({"grin": 1 - 0.4 * sly, "smirk_L": 0.8 * sly})
        L.squint(p, 0.4 * sly)
        L.horns(p, x=6 * L.ring(t, CLICK, 18, 6))
        return p

    c.layer(deploy_face)
    out.append(c)

    # ---- drive (loop) --------------------------------------------------------------------------------
    T = 1.6
    c = L.looped(f"{NAME}/drive", T)
    c.key(0.0, drive)

    def drive_solve(t, p, skel, T=T):
        u = t / T
        steer = math.sin(math.tau * u)
        L.hips(body, p, dz=-0.03, roll=5 * steer, yaw=-6 * steer, pitch=6)
        driving(p, 1.0, thumb=max(0.0, math.sin(math.tau * 4 * u)))
        body.plant(p, 1, roll=6 * max(0.0, steer))
        body.plant(p, -1, roll=6 * max(0.0, -steer))
        return p

    c.solve(drive_solve)

    def drive_face(t, T=T):
        u = t / T
        p = Pose()
        p = p + look((10, -26 + 6 * math.sin(math.tau * u)), head=(0, 0, 8 * math.sin(math.tau * u)))
        brows(p, -0.6, 0.2, 0.8)
        p.face.update({"grin": 0.3, "smirk_R": 0.6, "grit": 0.3})
        L.horns(p, x=3 * math.sin(math.tau * 2 * u), z=3 * math.sin(math.tau * u))
        return p

    c.layer(drive_face)
    out.append(c)

    # ---- caught --------------------------------------------------------------------------------------
    T = 1.4
    c = Clip(f"{NAME}/caught", T)
    c.key(0.0, drive)
    c.key(0.35, hide)
    c.key(T, hide, "linear")

    def caught_solve(t, p, skel, T=T):
        froze = 1 - smooth(0.12, 0.45, t)
        driving(p, froze)
        hidden(p, smooth(0.15, 0.45, t))
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(caught_solve)

    def caught_face(t, T=T):
        p = Pose()
        up = smooth(0.4, 0.7, t)
        p = p + look((26 * up, -4), head=(-8 * up, 0, 0))
        brows(p, 1.4 * up + 1.6 * pulse(t, 0.0, 0.06, 0.2, 0.2), 1.6, 1.0)
        p.face.update({"grin": 0.0, "wide": pulse(t, 0.0, 0.06, 0.25, 0.2), "oh": 0.6 * up})
        L.horns(p, x=10 * L.ring(t, 0.05, 20, 5))
        return p

    c.layer(caught_face)
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
        p = Pose()
        p = p + look((26, 14 * math.sin(math.tau * u)), head=(-8, 6 * math.sin(math.tau * u), 4 * math.sin(math.tau * u)))
        brows(p, 1.4, 1.6, 1.0)
        w = 0.5 + 0.5 * math.sin(math.tau * 4 * u)
        p.face.update({"grin": 0.0, "oh": 0.5 + 0.3 * w, "smile": 0.2})
        return p

    c.layer(innocent_face)
    out.append(c)

    # ---- take ----------------------------------------------------------------------------------------
    hug = L.REST.copy()
    hug.set("head", 10, 0, -8)
    hug.face = {"grin": 0.6, "smile": 0.6}
    HUG = V(0.0, -0.34, 1.02)
    T = 1.8
    c = Clip(f"{NAME}/take", T)
    c.key(0.0, hide)
    c.key(T, hug)

    def take_solve(t, p, skel, T=T):
        out_ = 1 - smooth(0.0, 0.3, t)
        if out_ > 0.01:
            hidden(p, out_)
        reach = pulse(t, 0.15, 0.55, 0.3, 0.5)
        up = V(-0.36, -0.28, 1.2)
        home = smooth(HANDOFF + 0.2, T, t)
        tgt = up.lerp(HUG + V(-0.08, 0, 0), home)
        k = max(reach, home)
        body.hand_to(p, -1, RW[-1].lerp(tgt, k), elbow=(0.5, 0.3, -0.5),
                     hand_rot=L.hand_world((0.4, -0.3, 0.8), (1, 0, 0)) if k > 0.5 else None)
        L.fist(p, -1, 0.6 * smooth(HANDOFF - 0.05, HANDOFF + 0.1, t))
        if home > 0.01:
            body.hand_to(p, 1, RW[1].lerp(HUG + V(0.1, 0.02, -0.06), home), elbow=(0.5, 0.3, -0.5),
                         hand_rot=L.hand_world((-1, -0.2, 0.3), (0, 1, 0)) if home > 0.5 else None)
        L.hips(body, p, dz=0.02 * reach, roll=4 * reach)
        body.plant(p, 1, roll=10 * reach)
        body.plant(p, -1, roll=10 * reach)
        return p

    c.solve(take_solve)

    def take_face(t, T=T):
        p = Pose()
        up = pulse(t, 0.1, 0.3, 0.6, 0.4)
        joy = smooth(HANDOFF, HANDOFF + 0.4, t)
        p = p + look((16 * up, -18 * up))
        p.face.update({"grin": 1 - 0.4 * joy, "wide": 0.6 * up * (1 - joy), "smile": 0.6 * joy})
        brows(p, 1.6 * up, 1.8 * up, 1.0 * up)
        L.squint(p, 0.8 * joy)
        return p

    c.layer(take_face)
    out.append(c)

    # ---- hug (loop) ----------------------------------------------------------------------------------
    T = 2.0
    c = L.looped(f"{NAME}/hug", T)
    c.key(0.0, hug)

    def hug_solve(t, p, skel, T=T):
        sway = math.sin(math.tau * t / T)
        L.hips(body, p, dx=0.02 * sway, roll=-5 * sway)
        p.add("chest", 0, 0, -6 * sway)
        body.hand_to(p, -1, HUG + V(-0.08, 0, 0), elbow=(0.5, 0.3, -0.5),
                     hand_rot=L.hand_world((0.4, -0.3, 0.8), (1, 0, 0)))
        L.fist(p, -1, 0.6)
        body.hand_to(p, 1, HUG + V(0.1, 0.02, -0.06), elbow=(0.5, 0.3, -0.5),
                     hand_rot=L.hand_world((-1, -0.2, 0.3), (0, 1, 0)))
        body.plant(p, 1, roll=8 * max(0.0, sway))
        body.plant(p, -1, roll=8 * max(0.0, -sway))
        return p

    c.solve(hug_solve)

    def hug_face(t, T=T):
        p = Pose()
        sway = math.sin(math.tau * t / T)
        p = p + look((0, 0), head=(0, 0, -10 * sway))
        L.squint(p, 0.9)
        L.horns(p, x=3 * math.sin(math.tau * 2 * t / T), z=3 * sway)
        return p

    c.layer(hug_face)
    out.append(c)
    return out
