"""The pocket rave: Archie clears his throat and opens the Atlas Core to present a serious project -- and it is a
nightclub (the rave world, worlds.py): the floor flashing, lasers fanning, a disco ball, Zip on the decks, three
little agents dancing, and Brick on the door, behind the velvet rope. Archie leans in for a closer look and the
bouncer shakes his head and folds his arms: not on the list. It's HIS core. Not on the list. He folds it away;
the bass keeps thumping in his hand, and in his belly.

Archie holds the Core on his left palm (HOLD, bits/_corekit.py) from `take` to `back`; his eyes go up to the
projection, up and to his left (screen right). The DJ is the holo-zip prop playing its `dance`; the bouncer is
holo-brick (its `bouncer`, `shake-head`, `guard`, `guard-hold`); the dancers are holo-agents playing Archie's
own dances (archie-dances.glb, which the page already has).

    pocket-rave/serious      REST -> REST: ahem, a grave little nod
    pocket-rave/take         REST -> HOLD (the Core to his palm at _corekit.GRAB)
    pocket-rave/hold         HOLD, looping
    pocket-rave/present      HOLD -> HOLD: behold, the serious project
    pocket-rave/double-take  HOLD -> HOLD: that is not the serious project
    pocket-rave/lean-in      HOLD -> HOLD: up close, at the door
    pocket-rave/protest      HOLD -> HOLD: MY core
    pocket-rave/deadpan      HOLD -> HOLD: to the reader, flat
    pocket-rave/back         HOLD -> REST (the Core back at _corekit.DOCK)
"""
from __future__ import annotations

from . import _core_gags as G
from . import _corekit as K

NAME = "pocket-rave"
CAST = ("archie",)
BEAT = 0.5                      # the club's beat, seconds (120 a minute): the thump of the closed Core


def clips(bodies):
    body = bodies["archie"]
    n = lambda piece: f"{NAME}/{piece}"
    return {"archie": [
        G.serious(body, n("serious")), K.take(body, n("take")), K.hold(body, n("hold")),
        G.present(body, n("present")), G.double_take(body, n("double-take")), G.lean_in(body, n("lean-in")),
        G.protest(body, n("protest")), G.deadpan(body, n("deadpan")), K.back(body, n("back")),
    ]}
