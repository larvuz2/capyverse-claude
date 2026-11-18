# Logo round 16: five variants of "Gnawed" (round 9, logo 02)

Source: `src.png` = `../logo-wood/refine/gnawed_nbp_0.png` (the round-9 Gnawed artwork).

1. `p_*.txt`: edit prompts (same lettering, change only bites / colour / size). nano-banana-pro/edit, 2 takes each
   (`g_*`), `3_devoured` and `4_walnut` re-run with corrected prompts (`h_*`). Picks in `pick/`.
2. BiRefNet cutouts → `cut/`.
3. `finish.py`: trims; on `4_walnut` separates the ODYSSEY row by hand and enlarges it 1.42x (the image model
   would not resize it) → `out/`.
4. `mock.py`: each variant on the current capsule (round 18 · Meadow) at main / header / small, logo auto-placed
   clear of the characters → `mock/` (copied to the gallery as `logos/r16*` and Store preview proposals `G1`-`G5`).

Variants: 1 Nibbled (less), 2 Chewed (more), 3 Devoured (most), 4 Dark Walnut + bigger ODYSSEY, 5 Painted Cream.
