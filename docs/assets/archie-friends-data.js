// Archie's friends: who they are, what they look like, and everything they and Archie say. This file is
// copy and data only. The runtime that draws them and plays their tricks is `archie-friends.js`, and the
// rules below are the ones it has to keep; if a trick here cannot be played inside them, it is the trick
// that goes, not the rule.
//
// THE RULES. A friend is a guest on somebody else's page, and the joke only works if the reader is never
// actually in the way of it. So:
//
//  - Rare. At most one visit a page view, on about a quarter of the views that qualify, and never in the
//    first twenty seconds, when the reader is still finding their feet.
//  - Quiet mode (`atlas-byte-quiet`) means no friends at all, the same as it means no chatter from Archie.
//    Reduced motion means no friends either; `quack`'s trick changes nothing on the page and is the one
//    exception worth making, shown still and gone in six seconds, if the runtime wants one.
//  - Nothing a reader is using. A trick picks its target from what is on screen and skips anything that
//    has focus, holds the caret, is under the pointer, or has a value typed into it. Nothing takes focus.
//    Everything the friends add takes no pointer events, so every link and button under them still works,
//    and any click or Escape sends the friend home early.
//  - Nothing the reader is reading changes. Where a trick seems to alter text (Nib's borrowed letter),
//    the text is left alone and the effect is an overlay drawn over it. The friend is hidden from
//    assistive technology, like Archie's bubble, because a moth announced mid-sentence is noise.
//  - Everything is put back within eight seconds, and put back as it was, only if it is still as the
//    friend left it, the same care `pranks()` in `archie.js` takes with the count.
//  - Nothing flashes. No brightness change faster than three a second (WCAG 2.3.1), and Lumen's wings
//    beat slower than twice a second so they never read as flicker.
//
// `?archie=friend:<id>` brings that friend first, through the same gates, so quiet mode can be checked to
// stop them, the way `?archie=prank:<name>` does for Archie's own pranks.
//
// THE SHAPE. Each line is [text] for speech or [text, 1] for a thought, exactly as in `LINES` in
// `archie.js`, so the runtime can pick from these with the same shuffled bags and show them in the same
// bubbles. Under each friend's `lines`:
//
//  - `arrive`, `leave`: the friend's own, on the way in and out;
//  - `<trick>`: the friend, doing it;
//  - `<trick>-archie`: ARCHIE's reply, in his bubble, not the friend's;
//  - `<trick>-after`: the friend's excuse, as it is put back;
//  - `poke`: if the reader pokes Archie while a friend is over, Archie answers with one of these instead;
//  - `skin`: the friend's remark when the reader is on their favourite skin (`likes`).
//
// `{n}` in a line is the friend's own name, so the same line reads right if a name ever changes. The
// looks are written for drawing as a small flat SVG: a silhouette, two or three colours, and the one
// detail that makes the character. Keep them to that; they have to read at thirty-odd pixels.
//
// `ORDER` is the friend-of-the-day rotation, for the daily greeting in `daily-lines.json`.

export const ORDER = ["nib", "posy", "lumen", "oh-four", "quack"];

export const FRIENDS = {
  nib: {
    name: "Nib",
    likes: "sherbet",
    look: "The arrow cursor from Archie's prank, escaped and grown legs. A standard pointer-arrow " +
      "silhouette about 28 px tall, filled #FFFFFF with a 2 px #FF2BD6 outline (Archie's cursor " +
      "magenta). Two black dot eyes near the tip, a tiny curved smile, two 2 px #FF2BD6 stick legs with " +
      "round feet out of the bottom edge. Leans about ten degrees forward when it walks.",
    personality: "Cheeky and light-fingered. Collects letters for a font it is designing, and is always " +
      "sure this one will be the last.",
    enter: "Skitters in from the left edge of the page along the top of a section heading.",
    exit: "Hops off the right edge.",
    tricks: {
      borrow: "Picks a section heading on screen and lifts one letter: a copy of the glyph rises 12 px in " +
        "Nib's hands while a chip in the page's own background colour covers the original. The heading's " +
        "text is never touched. After Archie's reply, Nib sets the letter back, the copy settles into " +
        "place and the chip goes, all within five seconds.",
    },
    lines: {
      arrive: [["Don't mind me. Just browsing."], ["Is this where the good letters are?"],
               ["Hi Archie! Remember me? I was your cursor."], ["Ooh, headings. Lovely headings.", 1]],
      borrow: [["I'll just borrow this one."], ["Nobody reads the vowels anyway."],
               ["Mine now. For my font."], ["Five-finger discount. Well. One-pixel discount."]],
      "borrow-archie": [["Nib! Put that back. People are reading that."], ["That's not yours. That's a heading's."],
                        ["Nib, we've talked about the letters."], ["Drop it. Now. Gently."]],
      "borrow-after": [["Fine. It was the wrong kerning anyway."], ["Borrowed! I said borrowed!"],
                       ["It was a loan. With zero interest.", 1], ["Nobody saw that. Right?"]],
      leave: [["Bye! Your font is safe. For now."], ["Gotta click."], ["See you around. Literally."]],
      poke: [["Not now, I'm keeping an eye on Nib."], ["Hang on, Nib's got that look again."]],
      skin: [["Sherbet! Everything tastes like strawberry."], ["This skin matches my outline. Coincidence?", 1]],
    },
  },

  posy: {
    name: "Posy",
    likes: "riso",
    look: "A sentient sticky note. A 44 px square, #FFD84D, the bottom-right corner curled up as a " +
      "triangle of #E8B92E, and a soft drop shadow. Two short vertical-oval eyes and a small round " +
      "mouth in #2B2140. A tiny pencil tucked behind the top edge: #FF8C42 body, pink eraser.",
    personality: "Earnest and helpful to a fault. Leaves notes for everyone, mostly compliments, " +
      "occasionally reminders nobody asked for.",
    enter: "Drifts down from the top of the window like a falling leaf, two or three gentle sways.",
    exit: "Peels off, a quarter-turn and a fade, and floats away.",
    tricks: {
      note: "Sticks a small yellow note, rotated three degrees, on the corner of a project card (`.cx`) on screen, " +
        "or of the spotlight (`.hero`) if no card is, " +
        "with one of `notes` written on it in a handwriting face (\"Segoe Print\", \"Bradley Hand\", " +
        "\"Comic Sans MS\", cursive). It covers only the card's corner, never its name or description, " +
        "and curls and drops off after six seconds, or at the first click.",
    },
    // What is written on the note itself: 22 characters at most, so it fits two lines of a 64 px note.
    notes: [["This one's good! -P"], ["Star the original!"], ["Read the README :)"], ["Ooh, fancy."],
            ["Future you says thanks"], ["Hidden gem? Yes."], ["10/10 would clone"], ["Posy was here <3"],
            ["Don't forget water!"], ["Bookmark me!"], ["Try this one first"], ["A+ README"]],
    lines: {
      arrive: [["Hi! I brought notes."], ["Hello, hello! Sorry, just passing through."],
               ["Archie! I made you something."], ["Who wants a note? Everybody gets a note."]],
      note: [["There. Now it's official."], ["A little reminder, just for you."],
             ["I'll leave this here."], ["Everyone deserves a note."]],
      "note-archie": [["Posy, that's a catalogue, not a fridge."], ["Very kind. Very sticky."],
                      ["Posy, the adhesive. We talked about the adhesive."],
                      ["Aww. Okay, but it comes off in a minute."]],
      "note-after": [["Oh! It's not very sticky, is it."], ["It fell off. That means it was read.", 1],
                     ["I'll bring stronger glue next time."], ["Reusable! Very eco."]],
      leave: [["Bye! Have a noteworthy day."], ["Off to the next page. So many pages."],
              ["Remember what I wrote!"]],
      poke: [["Shh, Posy's writing."], ["Careful, you'll get a note too."]],
      skin: [["Riso! It's like being printed in a zine."], ["I've never felt so fluorescent.", 1]],
    },
  },

  lumen: {
    name: "Lumen",
    likes: "aurora",
    look: "A small moth with a 36 px wingspan. A round, fuzzy body in #C9B8FF; four rounded wings in " +
      "#EDE6FF, a #22E1FF eye-spot on each fore-wing; feathery antennae in #8A5BFF; big black eyes with " +
      "a white glint. The wings beat slowly, under two beats a second, and nothing about her flashes.",
    personality: "Dreamy, easily dazzled, speaks in half-poems. Believes every bright thing is the moon.",
    enter: "Flutters in along a lazy wave from off the edge of the window.",
    exit: "Spirals slowly up and out of the top.",
    tricks: {
      photobomb: "Flutters to the corner of the homepage's spotlight project, lands, spreads her wings " +
        "wide in a pose for three seconds, then flutters off after Archie's reply. She sits on the corner, " +
        "never over the project's name, picture or link. With no spotlight on screen, she tries the glow " +
        "behind Archie in the masthead instead.",
    },
    lines: {
      arrive: [["Oh... what a lovely light."], ["Is that the moon? It's always the moon.", 1],
               ["Hello, Archie. Your visor is glowing."], ["I followed the brightest thing on the page."]],
      photobomb: [["Take my picture! Quick!"], ["Me and the spotlight. Best friends."],
                  ["This is my good side."], ["Spotlight... so warm... so featured.", 1]],
      "photobomb-archie": [["Lumen, that's the spotlight, not a lamp."], ["Lumen! You're in the shot!"],
                           ["That project worked hard for that spotlight."],
                           ["Every day. Every single day, the spotlight."]],
      "photobomb-after": [["Fine. But I was very photogenic."], ["It's a different light every day. I'll be back.", 1],
                          ["I just wanted to be featured too."], ["Oh! Another light! Over there!"]],
      leave: [["Goodnight, bright things."], ["Off to find the moon. Again."], ["Stay luminous, Archie."]],
      poke: [["Sorry, Lumen's using my visor as a nightlight."], ["Mind the moth."]],
      skin: [["Aurora! The whole sky came indoors."], ["So many lights. I can't choose.", 1]],
    },
  },

  "oh-four": {
    name: "Oh-Four",
    likes: "blueprint",
    look: "A shy little sheet ghost, 32 px tall. Filled #F4F7FF with a 1.5 px outline in #9AA3B8, a hem " +
      "of three scallops, two oval eyes in #1A1A2E, and \"404\" in tiny faint #B8C0D0 across the " +
      "forehead. Bobs up and down by two pixels.",
    personality: "Shy and apologetic. Is always lost, and was never quite sure it was found in the first " +
      "place. Thinks it is a page nobody could find.",
    // The homepage has no search box of its own, so Oh-Four hides behind the masthead's "Search and filter"
    // button (`a.cta`), the nearest thing to one.
    enter: "Rises from behind the masthead's search button until its eyes and the top of its head peek " +
      "over the button's top edge.",
    exit: "Sinks back down behind it.",
    tricks: {
      peek: "Peeks over the top edge of the search button, sitting above its border, never over its " +
        "label. If the pointer comes within about 120 px, it ducks at once; it never follows the pointer. " +
        "Skipped altogether while the button has focus.",
    },
    lines: {
      arrive: [["Oh! Sorry. Wrong page."], ["Is this... found? Am I found?", 1], ["Um. Hi. Don't look."],
               ["I'm not lost. I'm... exploring."]],
      peek: [["Boo? ...sorry, was that too much?"], ["I'm not hiding. I'm searching. From behind."],
             ["Don't mind me. I live here. Sort of.", 1], ["Peekaboo. Please don't search for me."], ["I'm not in the index. Don't look it up."]],
      "peek-archie": [["Oh-Four, come out, nobody's cross."], ["There's nothing behind that button, I promise."],
                      ["Oh-Four! Were you there the whole time?"], ["It's fine. Everybody gets a bit lost here."]],
      "peek-after": [["Too many eyes. Back I go."], ["Found! Oh no. Hiding again."],
                     ["Maybe next time.", 1], ["Eep."]],
      leave: [["I'll just... not be found now."], ["Page not found. That's me. Bye."],
              ["Going back behind the button. It's cosy."]],
      poke: [["Shh, you'll scare Oh-Four."], ["Gently. We have a guest."]],
      skin: [["Blueprint! Finally, a map. Now I know where I am.", 1], ["I'm on the plans! Look, there I am!"]],
    },
  },

  quack: {
    name: "Quack",
    likes: "graphite",
    look: "A classic rubber duck, 34 px. Body #FFD23F, beak #FF8C42, one black dot eye with a white " +
      "glint and a small wing line. A tiny lanyard with a badge reading DEBUG in #22E1FF.",
    personality: "Says almost nothing. Asks one-word questions, which makes Archie explain himself out " +
      "loud until he finds his own bug. The wisest one here, and the only one who never touches anything.",
    enter: "Bobs in, a gentle float as if on water, and sits at the bottom edge of the masthead next to " +
      "Archie.",
    exit: "Bobs away.",
    tricks: {
      debug: "Quack asks a question; Archie explains, then realises what was wrong all along. Nothing on " +
        "the page changes, so this is the one trick that may play still, for a reader who has asked for " +
        "reduced motion, if the runtime wants one there.",
    },
    lines: {
      arrive: [["Quack."], ["...quack?"], ["*squeak*"]],
      debug: [["Why?"], ["How?"], ["And then?"], ["Sure?"], ["Tests?"]],
      // Archie's side of it, in two beats paired by index: `debug-archie[i]` explains, and
      // `debug-archie-2[i]` is the moment he hears himself and finds it. Keep the two the same length, and
      // each line under 45 characters: the runtime gives each beat under three seconds.
      "debug-archie": [["The loop runs from 0 up to length, so..."],
                       ["The config says 'recieve', which is..."],
                       ["I only changed one tiny thing, and..."],
                       ["The tests pass. The tests do run..."],
                       ["Can't be the cache. I cleared it last..."],
                       ["It works on my machine, because..."],
                       ["The script runs, then looks for the page..."],
                       ["There's data, and data2, and data3..."]],
      "debug-archie-2": [["...oh. Off by one. Thanks, Quack."], ["...a typo. It was a typo.", 1],
                         ["...that was the whole bug. Right."], ["...don't they? Oh no."],
                         ["...month. It's the cache."], ["...nobody else has my machine. Oh."],
                         ["...before the page exists. Of course."],
                         ["...and I used the wrong one. Thanks, Quack."]],
      "debug-after": [["Quack."], ["*satisfied squeak*"], ["...quack."]],
      leave: [["Quack."], ["*squeak* (goodbye)"]],
      poke: [["Busy. Explaining things to a duck."], ["Shh. Quack's thinking."]],
      skin: [["Quack. (Graphite. Classic. Approved.)"]],
    },
  },
};

// Archie on the friends, for his own idle chatter on a day a friend is expected, and his remarks about
// the new skins. Same shape as `LINES` in `archie.js`; the runtime can merge these in under the same keys.
export const ARCHIE = {
  // An idle thought on the day `{n}` is friend of the day
  expecting: [["{n} said they might drop by today.", 1], ["If you see {n}, act natural."],
              ["I told {n} to behave. We'll see.", 1], ["Today's guest: {n}. Hide the headings."]],
  // After a visit, the next idle line
  missed: [["You just missed {n}. Well, you didn't. You saw everything."],
           ["{n} says hi. {n} always says hi.", 1], ["Nothing happened. {n} was never here."]],
  // The new skins, one reaction each, in the shape of `glass`, `terminal`, `prism` in `LINES`
  sherbet: [["Sherbet! My visor feels fizzy."]],
  riso: [["Riso! Everything's slightly misaligned. On purpose."]],
  blueprint: [["Blueprint. Finally, I can see how I was built."]],
  aurora: [["Aurora! Okay, this one's pretty."]],
};
