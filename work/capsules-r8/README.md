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
