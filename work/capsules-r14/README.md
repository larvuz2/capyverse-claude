# Round 14: flying heroes re-posed from their real images, no 3D models

- Cappy: Unreal render `H_cappy` (flipped), big in the lower-right corner. Muzzle flash anchored on the measured
  barrel tip (H_cappy px 2055,95; the old PROPS anchor was mid-barrel).
- Moody / Jim / Axie: `p_*.txt` prompts, gpt-image-2.5/flare/edit with the real render + library view as refs,
  re-posed flying toward the left, matte skin. Picks: gpt_axie_1, gpt_jim_0, gpt_moody_0 → BiRefNet `cut_*_0.png`.
- `r14.py`: same plate + logo as rounds 12-13; belt flames at hand-measured thruster points; three arrangements → `out/`.
