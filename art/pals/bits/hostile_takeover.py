"""The hostile takeover: Archie opens the Atlas Core to show the atlas, and finds the miniature agents have
fortified it (the no-archies world, worlds.py). Two of them heave a NO ARCHIES sign up at the gate while the
third comes out to stand guard. He leans in, reads it, protests -- it's HIS core -- and is told to stop right
there. Then Zip strolls up, waves, and the agents cheer, part, open the gate and wave him straight through:
he hops into the projection and struts in. Archie turns to the reader.

Archie holds the Core on his left palm throughout (HOLD, bits/_corekit.py); his eyes go up to the projection,
up and to his left (screen right). Zip plays his everyday clips (walk, wave, jump: clips/zip_base.py) and has no
pieces here. The agents are the holo-agent prop on Archie's own skeleton, playing the `agent-*` pieces below
from this bit's Archie file, and their own wave, cheer and fold_arms.

    hostile-takeover/take           REST -> HOLD (the Core to his palm at _corekit.GRAB)
    hostile-takeover/hold           HOLD, looping
    hostile-takeover/present        HOLD -> HOLD: behold, the atlas
    hostile-takeover/double-take    HOLD -> HOLD: that is not the atlas
    hostile-takeover/lean-in        HOLD -> HOLD: up close, squinting at the sign
    hostile-takeover/protest        HOLD -> HOLD: MY core (two jabs at his chest, a finger up at it)
    hostile-takeover/deadpan        HOLD -> HOLD: to the reader, flat
    hostile-takeover/back           HOLD -> REST (the Core back at _corekit.DOCK)
    hostile-takeover/agent-heave    the agents: loop, heaving the sign up
    hostile-takeover/agent-stop     the agents: REST -> held, palm out: stop right there
    hostile-takeover/agent-marshal  the agents: loop, waving Zip through (across to his right, screen left,
                                    where the gate is from the guard's spot beside it)
"""
from __future__ import annotations

from . import _core_gags as G
from . import _corekit as K

NAME = "hostile-takeover"
CAST = ("archie", "zip")


def clips(bodies):
    if "archie" not in bodies:
        return {}
    body = bodies["archie"]
    n = lambda piece: f"{NAME}/{piece}"
    return {"archie": [
        K.take(body, n("take")), K.hold(body, n("hold")),
        G.present(body, n("present")), G.double_take(body, n("double-take")), G.lean_in(body, n("lean-in")),
        G.protest(body, n("protest")), G.deadpan(body, n("deadpan")), K.back(body, n("back")),
        G.agent_heave(body, n("agent-heave")), G.agent_stop(body, n("agent-stop")),
        G.agent_marshal(body, n("agent-marshal"), side=-1),
    ]}
