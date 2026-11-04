# How Gus prompts — style guide

Built from Gus's latest 50 generations in Capyverse Odyssey (Oct 6 → Oct 21, 2026; 32 unique prompts),
his earlier video prompts, and his own rulebook (`docs/reference/prompting-rulebook.md`).

## 1. Two voices: the raw ask and the polished prompt

Gus works in two layers, and both show up in the prompts.

**The raw ask (his own typing).** Short, imperative, fast, typos left in, ends with `!`:

> Add @Axie_flying Small on the left. Keep characters as is. Add epic background for a steam game capusle. Keep center empty as is!

His hand-patches on top of polished prompts look the same:
`DO NOT move characters. Keep he middle empty!` · `Add @Logo_2 In middle big` ·
`Add huge@Logo_2 ... Make the logo extra large all letters visible!` ·
`form the second image attached planet but planet is aligned to the left half visible but faded in black`

**The polished prompt.** The raw ask gets expanded into a structured, very explicit brief (that's the
part Claude should write for him). Then Gus edits it by hand, one line at a time.

→ When Gus sends a raw ask, Claude's job is the expansion: keep every intent, add the structure and
the guard rails, don't invent new creative ideas he didn't ask for.

## 2. Register A: the edit prompt (image-to-image on an existing render)

Used Oct 21 on the gray in-engine composite. 900–4,000 characters. Template: `prompts/templates/capsule-edit.md`.

Shape:

1. **Opening line, always the same:**
   `Enhance the attached Steam game capsule while preserving the exact composition, characters, Unreal Engine meshes, textures, poses, and proportions.`
   …followed by Gus's raw add-on: `DO NOT move any existing characters. Keep the middle completely empty!`
2. **Labeled sections, one per change**, heading in caps, the important ones flagged:
   `LOGO:` · `ADDITIONAL CHARACTER:` · `BACKGROUND:` / `BACKGROUND — VERY IMPORTANT:` ·
   `LIGHTING EFFECTS:` · `JETPACK THRUSTERS — VERY IMPORTANT:` · `GOLFER — VERY IMPORTANT:` ·
   `COMIC BOOK EFFECTS — SMALL AND SUBTLE:`
3. **Precise mechanics for VFX.** He says exactly where an effect originates and where it must not:
   "short, concentrated blue-white exhaust flames shooting backward from these side-mounted nozzles …
   NOT from their backs, feet, tails, or bodies."
4. **Points at untagged things by look and position:** "the large orange capybara", "the purple flying
   character", "the small flying character at the top", "the white crowned cat, stone serpent, small
   characters, and blue barrels on the right", "the golfer on the right".
5. **Extra images are cited by order:** "inspired by the second reference image", "Use the exact planet
   from that reference".
6. **Closes with `CRITICAL COMPOSITION RULES:`** as `* ` bullets that restate every requirement in one
   line each (preserve center, don't move anyone, add X without replacing anyone, exact count of
   effects, avoid excessive flares/glow, authentic Unreal meshes, "premium Steam capsule … without
   looking like AI-generated concept art").

## 3. Register B: the art-direction manifesto (new composition from scratch)

Used Oct 6–7 for Steam capsules with the logo. 9,000–12,000 characters. Template: `prompts/templates/capsule-keyart.md`.

Signature moves:

- **Opens with the medium in caps:** `RAW UNREAL ENGINE GAMEPLAY SCREENSHOT / IN-ENGINE CAPTURE.` then the deliverable in one sentence, with tags.
- **`ABSOLUTE VISUAL DIRECTION:`** says what it is *not*: "NOT KEY ART, NOT CONCEPT ART, NOT ILLUSTRATION, NOT A POLISHED CGI ADVERTISEMENT, NOT AI ART."
- **Layout as fractions of the frame:** "LEFT 45–50%: MASSIVE @Logo. RIGHT 50–55%: …"
- **Numbers for hierarchy:** "Cappy should occupy approximately 55–65% of the entire visible character cluster", "secondary characters … 40–60% of Cappy's apparent scale", "Cappy may obscure approximately 30–50%".
- **Equations:** `CAPPY = LARGE FOREGROUND HERO.` · `SMALLER = FARTHER BACK. SMALLER DOES NOT = FARTHER AWAY SIDEWAYS.`
- **Mental images:** "Think: Cappy has already flown almost directly past the gameplay camera while the rest of the squad is still catching up behind him."
- **The thumbnail read test:** "At thumbnail size, the viewer should first perceive: ONE HUGE CAPPY. Then, after looking closer: 'Wait — there are three other characters packed behind him.'"
- **Tie-breakers:** "If there is any ambiguity, MAKE CAPPY BIGGER and MOVE THE OTHERS FARTHER BACK."
- **Long one-per-line DO NOT lists** naming the failure modes he expects: no V formation, no lineup, no
  "separate character islands", no "four evenly spaced heads", "Avoid the common AI-art tendency to present every character equally."
- **Imperfection is a feature:** "RAW GAMEPLAY IMPERFECTIONS ARE DESIRABLE: slightly rigid poses, subtle asymmetry … DO NOT polish these imperfections away." Lighting: "No cinematic rim lights. No studio lighting. … No movie-style color grading."
- **Character lock block:** "@capy_gp … are LOCKED EXISTING GAME ASSETS. Preserve their EXACT meshes … DO NOT REDESIGN THEM. DO NOT BEAUTIFY THEM. DO NOT ADD DETAIL."
- **VFX tied to the prop that emits it:** disco-ball flares "originate PHYSICALLY from the disco ball and disco ball barrel — NOT randomly from the background"; confetti "must clearly originate inside the trumpet bell" and stays localized.
- **`THE CURRENT PROBLEM TO FIX:`** when iterating: "THE IMAGE FEELS TOO CROWDED. TOO MANY CHARACTERS ARE TOO LARGE. CAPPY DOES NOT FEEL IMPORTANT ENOUGH. @Logo IS NOT LARGE ENOUGH."
- **Negative wall at the end:** NO UI. NO HUD. NO CHARACTER NAMES. NO EXTRA TEXT. NO STEAM BRANDING. NO BORDER. NO SPLASH ART. NO ARTSTATION RENDER. NO AI-ART AESTHETIC.
- **Closes with an `ABSOLUTE PRIORITY:` chain** joined by `→`, most important first.

## 4. How he iterates

- **One change per round.** Everything else stays word-for-word (diffs between runs are often a
  single word: "epic outer-space" → "outer-space" → "game outer-space").
- **Re-rolls:** the same prompt run 2–3 times before editing.
- **A/B models:** the same prompt sent to `nano-banana-pro` and `gpt-image-2-5` minutes apart.
- **Escalation when ignored:** plain sentence → section heading → `— VERY IMPORTANT` → caps → repeated
  in the rules list → hard numbers. Example (onomatopoeias over 4 rounds): "a few … such as ZAP, BOOM,
  WHOOSH" → "three … WHOOSH / BOOM / POW, each with a location" → "only three" → "exactly three small,
  understated … approximately 2–3% of the image width each … tiny graphic accents that viewers notice
  only after looking closely".
- **Over-correction gets walked back:** after asking for a huge centered logo he went back to "Leave
  the empty space in center!" and dropped the logo section; the logo goes in later.
- **Explores backgrounds as a set:** gray → purple-to-black → yellow-to-orange → space with planet →
  black hole/portal ring → back to yellow-to-orange with comic accents.

## 5. Vocabulary he reaches for

- Deliverable words: *Steam game capsule*, *Steam store capsule*, *premium*, *high-converting*, *thumbnail size*, *future logo placement*, *negative space*.
- Look words: *authentic Unreal Engine in-game look/aesthetic*, *real 3D game asset*, *in-engine*, *clean silhouettes*, *slightly imperfect*.
- Background presets he likes:
  - "epic, vibrant yellow-to-orange gradient. Use bright golden yellow transitioning smoothly into rich, saturated orange, creating a bold, energetic, playful atmosphere with subtle cinematic lighting and depth. Keep the gradient clean and smooth, without additional scenery or distracting elements." (the brand look; it keeps coming back)
  - "epic, smooth purple-to-black gradient, featuring subtle cinematic lighting and atmospheric depth."
  - Space: "dark, cinematic outer-space environment … Use the exact planet from that reference … toward the left side … only approximately half of its spherical surface visible … subtle, dark, and partially faded into black."
- Restraint words for effects: *subtle, small, few, restrained, minimal, localized, controlled, secondary*. Effects never compete with the hero.
- Image prompts use "epic" freely. His **video** rulebook bans generic adjectives ("epic, stunning, 8K") — follow the rulebook for video.

## 6. Video prompts

Two modes appear in his history:
- **Quick tests:** "animate", "animate poster...capybara makes backflip", "slow push in, subtle head turn".
- **Production loops/shots:** precise and technical — "Walk continuously in place, staying perfectly
  centered. Use a seamless loop with natural body bounce and subtle accessory movement. Static camera,
  constant scale, no drifting or reframing." Logo stings get a timed macro breakdown (`0.0–0.7s — Macro descent …`)
  and "the final frame must remain exactly identical to the reference".
- For story sequences, use the fixed block order from his rulebook: HEADER → REFERENCE ROLE MAP →
  CHARACTER PROFILES → SCENE PROMISE → STAGING + PERFORMANCE → SPACE + LIGHTING → TIMELINE → AUDIO →
  CONTINUITY LOCKS → NEGATIVE. Template: `prompts/templates/video-shot.md`.

## 7. Models (what he's using now)

| Model | Use it for | Notes from the latest 50 |
|---|---|---|
| `nano-banana-pro` | **Edits that must preserve the source** (backgrounds, adding a character, VFX, logo drop-in) | Best composition lock on Oct 21; tends to add *more* effect than asked, so state counts and sizes. |
| `gpt-image-2-5` | **New compositions** (capsules from tagged assets), A/B against nano-banana-pro | Strong layouts and logo fidelity; re-renders/shrinks characters on edits; tends to polish characters toward glossy CGI despite "raw in-engine" asks. 4 failures on the 5760×3240 source (Oct 21). |
| `nano-banana-2`, `nano-banana-lite` | Cheap drafts, layout tests | Lite ignored the 16:9 brief once (1:1 output). |
| Video: `seedance-2.0` / `2.5`, `veo-3.1(-fast)`, `kling-3.0`, `gemini-omni-flash` | See Shot Forge model list | Seedance 2.5 / H3 take multiple references cited as Image 1, Video 1, Audio 1. |

Defaults: aspect **16:9**; Steam capsule outputs; one source image + 1–2 tagged references.
