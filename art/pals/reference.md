# Landmarks read off the model sheets

The sheets themselves are kept outside the repository, in `E:/Development Workspaces/Archie and Pals/`:
`Archie robot model reference sheet.png`, `Zip robot model reference sheet.png`, `Brick, the friendly orange
robot.png` and `Archie’s unfolding Atlas Core.png`. Grid crops for reading them are made with that folder’s
`tools/grid_crop.py`.

All numbers are sheet pixels (1536x1024 PNGs), read from the grid crops in this folder
(`python tools/grid_crop.py <sheet> <out> x0,y0,x1,y1 [scale] [step]`). y grows downwards; the floor line is
the sole bottom. "Char right" is screen left in the front view.

## Archie (`Archie robot model reference sheet.png`) — front view centre x≈300, floor y≈632

| part | front view | side view (face points +x, screen right) |
|---|---|---|
| crest tip | (358, 62) — about (343, 56) with the head's tilt taken out | (801, 57) — the pompadour sweeps from the back of the skull up and *forward*; its top edge a near-straight rise from (681, 133) through (731, 99) and (781, 75), curling up at the tip; its front face bulges to x≈813 at y 80–105 |
| crest, across | a swoosh: a long hollow slope from char-right's temple (x≈255 at y≈125) to the tip, the char-left side near upright (x≈366, y 90–115); graphite with a lime front face on the tip and a lime streak rising along each flank | from behind, its foot nearly the skull's width, the tip a little to char-left |
| head shell | x 250–368 at its widest (y 175–190), skull top y≈114 under the crest, chin y≈228 (w≈118, h≈114); round outline, full cheeks, the jaw narrowing to a soft chin. The head is tilted ≈8° towards char-left in this view | x 668 (back) – 800 (face), depth ≈132: the face upright from forehead to mouth, the back a ball; a face-plate seam just in front of the ear cups, the back panelled like a football (a hexagon in the middle) |
| ear cups | centres ≈(238,182) and (366,184); ceramic housing r≈28 with a lime band round its front, graphite face r≈21, thin lime ring r≈15, dark lens, brass pin | centre ≈(708,175), behind the head's middle |
| eyes | centres (288,178), (340,185) (tilted); openings ≈41 x 43 px, round, set into the face; lime iris ≈26 px across, high in the opening with white below it; big pupil (≈18 px); heavy dark upper lid line with a wing at the outer corner | the eye's front a little behind the cheek's |
| brows | thick graphite arcs (≈12 px): char-right's long and arched high (peak ≈47 px above its eye), char-left's lower and flatter, its inner end thick and turned up — the smirk's eyebrow | |
| mouth | the smirk: a wide thin line from (281,191) to (341,205), char-right's corner higher with a dimple, open only on char-left's half: a dark lip line, top teeth, dark inside (≈7 px at most) | |
| neck | graphite segmented, x 282–318, y 222–248 | |
| chest | ceramic, x 240–360, y 245–320; lime chevron piping at y≈290 dipping to 297 at centre; lime collar trim | depth ≈105 (x 685–790) |
| abdomen | graphite segmented plates x 270–330, y 315–365 — the Atlas Core dock (octagonal recess, lime clasp) | |
| pelvis | ceramic brief x 250–350, y 365–420, lime-trimmed centre plate | depth ≈80 |
| hip joints | graphite discs (260,400), (340,400), r≈18 | |
| shoulder pads | caps centred (210,275), (390,275), r≈25, lime edge trim; graphite joint disc with lime ring | |
| upper arm | (215,280) → elbow (150,330), length ≈78 | |
| elbow | graphite, lime ring, r≈15 | |
| forearm | → wrist (90,388), length ≈65, lime cuff at wrist | |
| hand | ceramic palm, 4 graphite digits (thumb + 3), brass joint rings, rounded tips | |
| A-pose | arms ≈40° below horizontal | arms hang straight in side view |
| thighs | ceramic, y 390–470, centres x 250 / 350, w≈50 | |
| knees | graphite joint + ceramic kneecap with lime trim, centre y≈495, cap ≈40x50 | joint disc (735,485) |
| shins | ceramic, y 520–580, w≈42, slight calf | |
| shoes | sneakers: ceramic upper, lime side panels, graphite laces/tongue, lime + graphite chunky sole; y 575–632; front width ≈75 | length ≈150 (x 690–840), ankle disc (705,580) |
| heights | head top 532 above floor; crest tip 567 | |

Materials: ceramic (warm white, glossy, faint specks), graphite (near-black, satin), lime (#9BCB1A-ish, glossy),
brushed steel, brass joint rings; eyes lime iris, black pupil, white catchlight.

## Zip (`Zip robot model reference sheet.png`) — front view centre x≈290, floor y≈625

| part | front view | side view |
|---|---|---|
| horns | graphite base, mint faceted tip; from (207,137) to (200,80) and (354,146) to (410,102): up and outward | sweep up and *back* |
| head | very wide: dome x≈190–390, with ear cups x≈165–415; y 140–270 (h≈130); purple dome, cream faceplate on the lower front | long front-to-back (x 668–845, ≈177 deep), helmet-like back |
| ear cups | centres ≈(180,215), (400,215), r≈30; mint ring, graphite, dark lens, brass centre | centre (725,200), r≈40 |
| eyes | huge: centres (260,209), (338,212), r≈28; magenta/violet iris, large pupil | |
| brow visors | mint ridges over the eyes on the purple shell, plus dark brows | |
| mouth | wide grin, y≈250 | |
| neck | graphite, thin, y 270–295 | |
| chest | small purple chest x 255–330, y 290–345, mint triangle emblem | depth ≈70 |
| waist | graphite y 345–375 | |
| pelvis | purple y 375–420, graphite hip joints | |
| shoulders | graphite balls with mint caps (238,305), (330,305) | |
| arms | long, thin, ≈50° below horizontal; elbow (195,360); wrist (135,420); hand to y≈470 | |
| hand | purple palm, mint cuff, graphite digits (thumb + 3) | |
| legs | purple thighs, mint knee pads, knees y≈490, purple shins, graphite ankles | |
| shoes | chunky sneakers: mint sole, purple upper, graphite tread; y 565–625; front width ≈85 | length ≈160 |
| heights | head top 485 above floor; horn tips ≈545 | |

Materials: violet (glossy), mint (glossy), graphite, metal, eyes violet/magenta iris.

## Brick (`Brick, the friendly orange robot.png`) — front view centre x≈300, floor y≈600

| part | front view | side view |
|---|---|---|
| head | small: x 210–367 incl. ear cups, y 100–180 (h≈80); cream face, orange crown band, brown eyes half-lidded, dark thick brows (one raised), small smile | head sits forward of the chest, low |
| ear cups | orange/graphite, centres ≈(215,140), (355,140) | |
| chest | huge barrel: x 147–417, y 167–333; orange plates with panel lines + rivets, cream side panels; graphite lower-chest plate y 290–370; cream waist band y 345–420 | chest front x≈855, back x≈690: deep, hunched |
| chest discs | graphite/orange round ports at (180,315) and (385,315) | |
| pauldrons | big orange domes x 60–163 and 417–517, y 160–253 | |
| upper arm | cream segment, y 253–290 | |
| elbow | graphite with orange ring | |
| forearms | massive orange gauntlets, x 20–123, y 290–400 | |
| hands | cream palm with orange trim, graphite 4 digits with orange segments; hang to y≈500 | |
| thighs | thick orange x 127–243 / 323–443, y 400–480 | |
| knees | graphite y 480–510, cream shin plates | |
| shins | orange y 510–560 | |
| feet | big blocky boots, graphite soles, y 555–600, front width ≈145 | long (x 665–870) |
| heights | head top 500 above floor | |

Materials: orange (glossy, worn), cream, graphite, metal, eyes amber/brown.

## Relative scale (not given by the sheets — each sheet fills its frame)

Chosen so the bits read: Brick covers a switch with one finger and lifts a README with one finger; Zip is the
small one. Head tops: Archie 2.25 m (crest tip 2.40, the height the homepage banner is framed for), Zip 1.75 m
(0.78; horn tips about 1.96), Brick 2.75 m (1.22, and twice as broad).
