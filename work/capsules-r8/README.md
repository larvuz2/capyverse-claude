# Round 8 — three takes on Gus's composition (`base.jpg`)

`python3 r8.py [A|B|C]`. Characters cut from his image (BiRefNet `cut_0.png`); jet flames lost by the cut are recovered
from the original as their own layer. Logo E4 is auto-fitted (`fit_logo`): largest size whose shape doesn't touch the
dilated character mask, nearest to upper-centre. FX: popcorn burst, disco flares, trumpet confetti, crown sparkle,
eye glints, golf-ball glint, worm dust.
- A: original background untouched.  B: same gradient + low-poly desert floor (`floorkey0.png`), haze, contact shadows.
- C: sunburst from behind the logo + hazy mesas + desert floor.

## Store sizes (`r8_sizes.py [ABC] [header main small]`)
Each take rebuilt natively at 920x430 (header), 1232x706 (main) and 462x174 (small): heroes anchored left, enemies
right, logo auto-fitted per size, rendered at 2x. Vertical 748x896 needs its own layout (not shipped).
The capsule gallery artifact now opens on a "Store preview" tab (mock store page, click any capsule to cycle C → A → B).

## Round 9 (r9.py): round-12 capsule, new environments, fixed back heroes

Director's notes: the back heroes (Axie, Moody, Jim) looked like they were floating, their materials looked
odd, and the hippo/axolotl reflections looked AI. Everything inside his red circle stays identical.

- `KEEP` = cut_0 minus the back-hero components, pasted untouched on top (Cappy, enemies, Ophelia, flames).
- Backgrounds: real lobby screenshots from the env2 Drive folder (`assets_src/env2/Lobby/`, not committed, 63 MB),
  cover-cropped, defocused, warm-graded to match the sunlit characters, with optional horizon haze.
- Back heroes: original Unreal renders, Moody/Axie through `degloss.py` (kills bright low-chroma specular
  bands), color-matched to the plate, rim-lit in the scene's light color, jet trails, belt flames, soft ground shadow.
- Logo: `work/logo-tin/tin_hanging.png`, auto-fitted clear of every character.
- Run: `python3 r9.py [1_golden_path ...]` → `r9/`.

## Round 10 (r10.py): same backgrounds, only the back heroes rearranged

Same five backgrounds, red-circle content and logo position as round 9 (the logo is fitted against the round-9
hero boxes so it does not move). Five arrangements of Jim, Moody and Axie: Squadron (tight V + shared back-glow),
Portal Exit (out of a glowing portal, far-to-near), Low Skim (Jim on the ground with shadow, dust, thruster light),
Depth Stack (big soft Moody close, hazy Axie far), Contrails (glowing trails from the left edge).
Run: `python3 r10.py [1_squadron ...]` → `r10/`.
