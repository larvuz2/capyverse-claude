# Study: Gus's latest 50 generations (Capyverse Odyssey)

Source: Shot Forge DB, `scenes_v2` + `generation_events`, authors gus@phattyacid.studio and
gus@metazooie.com, project Capyverse Odyssey, newest 50 non-deleted rows (Oct 6 → Oct 21, 2026).
50 runs · 32 unique prompts · 46 completed, 4 failed · all 16:9 except one 1:1.
Outputs: `media/latest50/NN_*.jpg` (NN = 01 newest … 50 oldest; gaps are failed runs).
Prompts: `prompts/archive/` (numbered oldest → newest).

## Context: where Gus is in the project

Across his 2,072 generations in this project: Jan–Feb heavy `nano-banana-pro` + video tests
(Seedance, Veo, Kling); Mar music/SFX/dialogue (Suno, ElevenLabs); Apr big `nano-banana-2` push
(381 runs, most favorites); Aug character turnarounds + `gpt-image-2` (218 runs); Sep–Oct
**Steam store marketing art** with `gpt-image-2-5` and `nano-banana-pro`. The latest 50 are all Steam capsule work.

## Session 1 — Oct 6–7: Steam capsule from tagged heroes (outputs 38–50, prompts 01–07)

**Goal:** a wide capsule: big logo on the left, the four heroes on the right, Cappy as protagonist.
**Inputs:** `@capy_gp` sheet as the source + `@Logo`, `@moody_gp`, `@axie_gp`, `@jim_gp` via tags.
**Model:** `gpt-image-2-5` (one `nano-banana-lite` test).

How it evolved:
1. *Huge Cappy + 3 smaller heroes receding behind him*, yellow-orange gradient, disco flares + trumpet confetti (prompt 01, 12k chars, 3 runs).
2. *"DIRECTLY. BEHIND. CAPPY."* — tighter single character mass after the squad spread out (02–04).
3. *Grounded ensemble on a dark ridge*, purple bg, thin inset frame, pyramid silhouette (05 → outputs 40–43).
4. *Back to flying*, side-belt jetpacks must be visible (06 → 39).
5. *"THE CURRENT PROBLEM TO FIX: too crowded, Cappy not important enough, logo not large enough"* (07 → 38).

What came out: strong logo fidelity and clean layouts; the yellow-orange versions (44–50) read best at
thumbnail size. But the characters drifted toward **polished, glossy CGI** (bigger cute faces, fur
detail) despite the 12k-char "raw in-engine" direction, and the squad kept spreading into a lineup.

## Session 2 — Oct 21: edit the real in-engine composite (outputs 01–33, prompts 08–32)

**Goal:** turn a gray-background Unreal render (`base_capsule_gray_composite.jpeg`) into the capsule
without touching the characters, keeping the center empty for the logo.
**Inputs:** the composite as source + `@Axie_flying`, later `@Logo_2`, the planet reference.

1. Raw ask → expanded prompt; **4 failures on `gpt-image-2-5`** (03:53–03:58), then a shorter
   890-char prompt succeeded (output 32).
2. Purple-to-black gradient + Axie added + disco flares + barrel glow (30–28). Long
   "JETPACK THRUSTERS — VERY IMPORTANT" section added to force side-belt flames.
3. Switched to `nano-banana-pro` (26) — much better preservation of the source.
4. Logo tests: `@Logo_2` dropped in center (25), then yellow-orange gradient (24, 23).
5. Space backgrounds with the planet reference (22–16): ring portal / black hole (`gpt-image-2-5`
   reinterpreted the planet as a gate), then "planet on the left, half visible, faded in black" (16–08).
   Logo forced "huge, all letters visible" (12).
6. Back to **yellow-orange + comic onomatopoeias + golf ball** for the golfer (07–01). Onomatopoeias
   were shrunk over four rounds to "exactly three … 2–3% of image width".

**Latest state (output 01, prompt 32):** yellow-orange gradient, Axie added far left, small
WHOOSH!/BOOM!/POW!, golf ball at club impact, blue-white belt-thruster flames, center empty.

## Lessons for the next request

- For edits on the real render, use `nano-banana-pro` and the Register A shape; it keeps the
  meshes. Use `gpt-image-2-5` when the brief is a new layout.
- Any effect without a number grows. Give counts, sizes (% of width), and origin points.
- Asking for empty center *and* a logo in the same prompt confuses models; Gus separates those passes.
- The 5760×3240 source may be behind the `gpt-image-2-5` failures; downscale to 2560 wide if it fails again.
- Jetpack flames must be pinned to the **side belt nozzles** every time, or models put them on backs/feet.
- `@Cappy_flying`'s sheet shows a disco-ball cannon; the game's Cappy carries the popcorn gatling.
  When the popcorn gatling matters, use `@capy_gp` or the source render, not `@Cappy_flying`.
- Gus hasn't marked any of the latest 50 as favorites; ask which outputs he's keeping.
