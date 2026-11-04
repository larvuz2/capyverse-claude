# Steam capsules v1 — 10 approaches with the new logo

Finals: `out/NN_<name>_main_capsule_1232x706.jpg` (Steam main capsule), `_full_2464x1412.jpg` (2× master),
`_thumb_test_462.jpg` (small-size readability check).

## The method (what changed vs. the Shot Forge edits)

Before, the whole capsule went through an image model, so every pass re-rendered the characters,
and players could tell they were AI. This pipeline never regenerates the in-engine characters:

1. **Cut the real render into layers.** `base_capsule_gray_composite.jpeg` (5760×3240 Unreal render)
   → BiRefNet on FAL → one layer per character group (`layers/H_*.png`, full-res pixels).
2. **Generate only what's missing.**
   - **Axie** (missing from the base): `nano-banana-pro/edit` with the base render as the *render reference* + `@Axie_flying`,
   rendered alone on gray, then cut out (`layers/L_axie.png`). Same faceted look as the game models.
   - **Clown pin minion** for the bowling concept: same trick from a crop of the base (`layers/L_pin.png`).
3. **AI paints only empty backgrounds.** Each plate prompt (`prompts/plate_*.txt`) uses **real gameplay
   screenshots from the Steam page as world references** (`refs/ss*.jpg`, `Lobby.png`, planet ref)
   and forbids characters/UI/text. Two models per plate (nano-banana-pro ×2, gpt-image-2.5 ×1), best one picked;
   gpt-image-2.5 plates were 1088px, so they were upscaled 2.5× with SeedVR.
4. **Composite by hand** (`compose.py` = the Photoshop step): colour match to the plate, light wrap,
   directional rim light, contact/flight shadows, motion trails, belt-thruster flames from the side nozzles,
   disco-ball flares from the ball, confetti from Jim's trumpet bell, the new logo as a clean cutout
   (never redrawn), final grade/bloom/vignette.

Re-render any concept: `cd work/capsules-v1 && python3 c05.py` (needs Pillow, numpy, scipy).
Positions/scales are plain numbers at the top of each `cNN.py`, so tweaks are one-line edits.

## The 10 concepts

| # | Name | Idea | Cast | Plate |
|---|---|---|---|---|
| 01 | Sunburst Showdown | The current capsule done right: brand yellow-orange, heroes vs. villains, logo centered | all | nano-banana-pro |
| 02 | Attention Kingdom | Ophelia's wall of TV screens (her kingdom runs on attention); the squad flies in | heroes + Ophelia | gpt-image-2.5 + upscale, ref: Ophelia throne screenshot |
| 03 | Capyverse Planet | Low orbit over the planet of worlds; pure adventure, no villains | heroes | gpt-image-2.5 + upscale, ref: planet |
| 04 | Desert Run | Sandworm bursts out of the canyon floor at golden hour | heroes + worm, bandits, golfer | gpt-image-2.5 + upscale, ref: desert screenshots |
| 05 | Carnival Horde | **Crowded**: night carnival, a plaza full of clown pins and bandits, giant Ophelia | everyone | nano-banana-pro, ref: carnival screenshots |
| 06 | Strike! | Cosmic bowling lane, Cappy as the bowling ball, full rack of clown pins | heroes + pins | nano-banana-pro, ref: space-lane screenshot |
| 07 | Portal Lobby | The run begins: the squad blasts out of the lobby portal | heroes | gpt-image-2.5 + upscale, ref: Lobby |
| 08 | Just Cappy | **Minimal**: one hero, flat teal, popcorn firing out of the gatling | Cappy | procedural gradient + popcorn cut from a nano-banana-pro plate |
| 09 | Comic Versus | Halftone split, lightning seam, VS badge: the store pitch in one read | all | procedural (no AI) |
| 10 | Disco Inferno | Moody gets the spotlight on the rainbow floor | heroes, Moody hero | gpt-image-2.5 + upscale, ref: disco screenshot |

## Known limits / next steps

- Characters keep their original poses (they come from one render). New poses = new Unreal renders on gray;
  drop them into `layers/` and they go through the same pipeline.
- Header capsule (920×430) and small capsule (462×174) need their own layouts (different aspect); the
  scripts make that a quick re-layout once a direction is chosen.
- Ophelia's whiskers on the upper left were lost in the cut; a fresh render with a darker background would key cleaner.

## Round 2 (picks: 01, 04, 09) — Cappy always the hero

Gus picked 01, 04 and 09. Round 2 (`c11.py`–`c20.py`) keeps those directions and makes Cappy 3–4× the size of the other heroes.
Every hero now carries its FX via helpers in `compose.py`: `cappy()` (popcorn burst + muzzle flare from the gatling),
`moody()` (disco-ball flares), `jim()` (trumpet confetti), and all of them get **subtle flames from the side-belt
jetpack cylinders, pointing backward** (anchors fixed in `THRUSTERS` after zooming into the harnesses).

| # | Name | From | Notes |
|---|---|---|---|
| 11 | Hero Burst | 01 | Crab Champions-style single hero on the sunburst |
| 12 | Showdown Stack | 01 | Roboquest-style: Cappy front, Ophelia + crew behind |
| 13 | Canyon Colossus | 04 | new plate; worm-only layer (`worm_top`) at 2.7× erupting from a crater |
| 14 | Ophelia Rising | 04 | Risk of Rain scale: colossal Ophelia on the dusk horizon |
| 15 | Comic Cover | 09 | panel layout, Cappy breaks the frame, tiny "POP!" |
| 16 | Face-Off | 09 | Cappy vs. Ophelia, one on one |
| 17 | Saturday Morning | shader | `shaders.ink_cel` (k-means cel bands + ink edges + hatching) |
| 18 | Night Run | shader | `shaders.pixel` (320px grid, 48 colours, dithered), logo pixelated finer |
| 19 | Print Run | shader | `shaders.riso` (3-ink halftone separation with misregistration) |
| 20 | Bleached Sun | shader | `shaders.painted` (edge-preserving stylisation + pale wash), RoR2-inspired |

References studied: Steam capsules of Crab Champions, Risk of Rain 2, Risk of Rain Returns, Hades, Roboquest,
Gunfire Reborn, Ravenswatch, Brotato, Dave the Diver, Vampire Survivors, Balatro. Common thread: one dominant
hero, a big logo, a strong single-hue background, the cast as a crowd behind.

## Round 3 — five variations of #12 (`c12v.py a|b|c|d|e`)

Gus picked 12. Fixes in all five: Cappy moved left so he no longer overlaps the worm; side-belt thrusters ~1.6× wider and
longer; a detailed golf shot (`golf_shot()`: shaded dimpled ball, curved speed trail, impact puff and turf chips at the tee,
since the golfer is in follow-through); small comic onomatopoeias (`sfx()`, Bangers font) placed next to the action.

| Var | Name | Change |
|---|---|---|
| 12a | Classic | the fixed #12 |
| 12b | Dusk | sunburst hue-shifted to hot pink/red |
| 12c | Horde | second worm + back row of pins, CHOMP! |
| 12d | Ink | `shaders.ink_cel`, bigger lettering |
| 12e | Clean | bigger logo + Ophelia, two tiny sound effects, for thumbnail readability |
