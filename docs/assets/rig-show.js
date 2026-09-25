// The light show's look book: the colours the rig plays in, the gobos its moving heads project, and the
// graphics its lasers draw. Data and a few pure helpers only -- no DOM, no three.js -- so the rig in
// `archie.js`/`archie-fx.js` and the admin panel can both import it, and so can a test under node.
//
// LOOKS. One palette for the whole rig: four colours for the moving-head beams, two for the LED wash, two
// for the lasers, one for the blinders, and the gobo and laser graphics that suit it. One family and one
// accent per look, nothing at full saturation on every channel: pure RGB beams read as a toy and fight
// where they cross. On the dark theme the rig adds light, so the tones may be bright; on the light theme
// it lays haze over white, where pale tones vanish, so each look has a deeper `light` set. In show order:
// a cool opener, a warm drop, a complementary finale, a quiet breakdown. `cue` is the admin panel's line.
//
// NOTHING HERE STROBES. The blinder is only a colour; how often anything fires is the rig's to keep under
// three flashes a second (WCAG 2.3.1).
//
// GOBOS: one SVG each under `rig-gobos/`, 256 x 256, white where light passes, all inside a circle of
// radius 120, no line under 6 px so it survives a soft beam. Load with `new URL(src, import.meta.url)`.
//
// LASERS: a scanned beam is one dot moving fast, so a graphic is a few `strokes`, each a polyline traced
// without lifting (at most 64 points), the beam blanked between them. Points in [-1, 1], y up. `d(id)` is
// an SVG path for a preview in viewBox "-1 -1 2 2". PATTERNS take the beat's phase in [0, 1) and a point
// count and return one polyline, so the shape moves with the music.

export const LOOKS = [
  {
    id: "blue-hour", name: "Blue Hour",
    cue: "The opener: ice-blue beams in cold haze, lavender lasers, the room waking up.",
    beams: ["#6FD3FF", "#4E7BFF", "#9C8CFF", "#3FE0C5"],
    wash: ["#1B3A8A", "#2A7F9E"],
    laser: ["#7FE9FF", "#B7A6FF"],
    blinder: "#EAF4FF",
    gobo: "dots", lasers: ["wave", "globe", "sheet"],
    light: {beams: ["#0B7FC1", "#2F4FD9", "#6A4FE0", "#0E9E86"], wash: ["#1E4FA8", "#1D7D95"],
            laser: ["#0A8FB8", "#6B4FD8"], blinder: "#9CC4FF"},
  },
  {
    id: "ember", name: "Ember",
    cue: "The drop: amber beams, tungsten blinders, gold lasers fanning on the beat.",
    beams: ["#FFB347", "#FF7A45", "#FF5E7E", "#FFD27A"],
    wash: ["#8A2B1F", "#B8491C"],
    laser: ["#FF6A3D", "#FFC15E"],
    blinder: "#FFE7C2",
    gobo: "breakup", lasers: ["bolt", "heart", "fan"],
    light: {beams: ["#D9751A", "#D24A1F", "#C92E5A", "#B8860B"], wash: ["#9E3A1E", "#B35A12"],
            laser: ["#D2451F", "#C98A12"], blinder: "#FFC56B"},
  },
  {
    id: "afterglow", name: "Afterglow",
    cue: "The finale: teal against rose, violet wash, Archie's face in the lasers.",
    beams: ["#2EC4B6", "#FF4FA3", "#FFB000", "#7A5CFF"],
    wash: ["#5B1E7A", "#0F6E6A"],
    laser: ["#3CF2D8", "#FF5CB8"],
    blinder: "#FFF4E0",
    gobo: "star", lasers: ["face", "star", "ai", "tunnel"],
    light: {beams: ["#0E8A80", "#C8207A", "#C27C00", "#5634D6"], wash: ["#6A2A8C", "#0E6E68"],
            laser: ["#0E9E8C", "#C8207A"], blinder: "#FFD68A"},
  },
  {
    id: "low-tide", name: "Low Tide",
    cue: "The breakdown: slow periwinkle beams, indigo wash, a cone breathing with the bass.",
    beams: ["#5F7DFF", "#8A6BFF", "#5CC8FF", "#A0B4FF"],
    wash: ["#121A4A", "#24185A"],
    laser: ["#6E8BFF", "#9D7CFF"],
    blinder: "#DDE4FF",
    gobo: "spiral", lasers: ["cone", "chevrons"],
    light: {beams: ["#3350D9", "#6441D6", "#1C82C9", "#4C5FC2"], wash: ["#26307A", "#3A2A86"],
            laser: ["#3A55D6", "#6A45D0"], blinder: "#B8C4FF"},
  },
];

export const GOBOS = [
  {id: "breakup", name: "Breakup"},
  {id: "dots", name: "Dots"},
  {id: "star", name: "Star"},
  {id: "spiral", name: "Spiral"},
  {id: "archie", name: "Archie"},
  {id: "braces", name: "Braces"},
  {id: "iris", name: "Iris rings"},
  {id: "prism", name: "Prism"},
].map(g => ({...g, src: `rig-gobos/${g.id}.svg`}));

// Laser graphics
const TAU = Math.PI * 2;
const r3 = v => Math.round(v * 1000) / 1000;
// An arc about (cx, cy), from angle a to b (radians, anticlockwise with y up), in n segments.
const arc = (cx, cy, rx, ry, a, b, n) => Array.from({length: n + 1}, (_, i) => {
  const t = a + (b - a) * i / n;
  return [r3(cx + rx * Math.cos(t)), r3(cy + ry * Math.sin(t))];
});
// A rounded rectangle, starting and ending at the middle of its bottom edge, so it closes on itself.
const rrect = (cx, cy, w, h, r) => {
  const x0 = cx - w / 2, x1 = cx + w / 2, y0 = cy - h / 2, y1 = cy + h / 2, q = 6;
  return [[r3(cx), r3(y0)],
    ...arc(x1 - r, y0 + r, r, r, -TAU / 4, 0, q), ...arc(x1 - r, y1 - r, r, r, 0, TAU / 4, q),
    ...arc(x0 + r, y1 - r, r, r, TAU / 4, TAU / 2, q), ...arc(x0 + r, y0 + r, r, r, TAU / 2, TAU * 3 / 4, q),
    [r3(cx), r3(y0)]];
};
const star = (R, r, k = 5, rot = TAU / 4) => {
  const p = Array.from({length: 2 * k}, (_, i) => {
    const a = rot + i * TAU / (2 * k), m = i % 2 ? r : R;
    return [r3(m * Math.cos(a)), r3(m * Math.sin(a))];
  });
  return [...p, p[0]];
};

export const LASERS = {
  // Archie: head, visor, smile, antenna.
  face: {name: "Archie", strokes: [
    rrect(0, -0.12, 1.3, 1.1, 0.28),
    rrect(0, 0.02, 0.96, 0.42, 0.18),
    arc(0, -0.34, 0.26, 0.12, TAU * 0.58, TAU * 0.92, 10),
    [[0, 0.43], [0, 0.66], ...arc(0, 0.76, 0.1, 0.1, -TAU / 4, TAU * 3 / 4, 12)],
  ]},
  heart: {name: "Heart", strokes: [Array.from({length: 49}, (_, i) => {
    const t = i / 48 * TAU;
    const x = 16 * Math.sin(t) ** 3, y = 13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t);
    return [r3(x / 17), r3(y / 17 + 0.1)];
  })]},
  star: {name: "Star", strokes: [star(0.95, 0.4)]},
  bolt: {name: "Lightning", strokes: [[[0.15, 0.95], [-0.45, -0.05], [-0.02, -0.05], [-0.2, -0.95],
                                       [0.5, 0.15], [0.06, 0.15], [0.32, 0.95], [0.15, 0.95]]]},
  // The atlas: a globe.
  globe: {name: "Globe", strokes: [
    arc(0, 0, 0.9, 0.9, -TAU / 4, TAU * 3 / 4, 40),
    arc(0, 0, 0.45, 0.9, -TAU / 4, TAU * 3 / 4, 30),
    [[-0.9, 0], [0.9, 0]],
    arc(0, 0, 0.9, 0.3, 0, TAU, 30),
  ]},
  // A still waveform, swelling and dying away.
  wave: {name: "Waveform", strokes: [Array.from({length: 61}, (_, i) => {
    const x = -1 + i / 30;
    return [r3(x * 0.95), r3(0.7 * Math.sin(x * TAU * 2.5) * Math.cos(x * Math.PI / 2))];
  })]},
  ai: {name: "AI", strokes: [
    [[-0.95, -0.7], [-0.45, 0.7], [0.05, -0.7]],
    [[-0.72, -0.1], [-0.18, -0.1]],
    [[0.45, 0.7], [0.85, 0.7], [0.65, 0.7], [0.65, -0.7], [0.45, -0.7], [0.85, -0.7]],
  ]},
  chevrons: {name: "Chevrons", strokes: [0.3, 0.6, 0.9].map(s => [[-s, s * 0.8], [0, -s * 0.8 + 0.1 * s], [s, s * 0.8]])},
};

// The graphic as an SVG path, y flipped for SVG's y-down, in a viewBox of "-1 -1 2 2".
export const d = id => LASERS[id].strokes.map(s => "M" + s.map(([x, y]) => `${x} ${r3(-y)}`).join("L")).join("");

// Beat-synced patterns
export const PATTERNS = {
  // A sheet of light: a line across that ripples, the wave travelling one cycle a beat.
  sheet: (phase, n = 48) => Array.from({length: n}, (_, i) => {
    const x = -1 + 2 * i / (n - 1);
    return [x, 0.18 * Math.sin(TAU * (1.5 * x - phase))];
  }),
  // A cone: a circle that breathes, widest on the beat, for projecting down a tunnel of haze.
  cone: (phase, n = 48) => {
    const r = 0.55 + 0.15 * Math.exp(-4 * phase);
    return Array.from({length: n}, (_, i) => [r * Math.cos(TAU * i / (n - 1)), r * Math.sin(TAU * i / (n - 1))]);
  },
  // A fan: n beam tips spread on a line, swinging a little either way over two beats' worth of phase.
  fan: (phase, n = 9) => Array.from({length: n}, (_, i) => {
    const a = 1.1 * (i / (n - 1) - 0.5) + 0.35 * Math.sin(TAU * phase);
    return [Math.sin(a) * 0.95, -0.2];
  }),
  // A chevron tunnel: one chevron growing from the centre to the edge each beat.
  tunnel: (phase, n = 3) => {
    const s = 0.1 + 0.9 * phase;
    return [[-s, s * 0.8], [0, -s * 0.7], [s, s * 0.8]].slice(0, Math.max(3, n));
  },
};
