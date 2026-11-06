# Round 11: Gus's reference composition rebuilt with real assets + Tin hanging logo

- `ref_composition.jpg`: the reference Gus sent (AI concept). Layout analysis is in the `r11.py` docstring.
- `plate.txt`: prompt for the EMPTY background plate (nano-banana-pro/edit ×2, gpt-image-2.5 ×1), refs: the
  reference + two lobby screenshots. Results: `plate_nb_0/1.png`, `plate_gpt_0.png`.
- Characters: Cappy = Unreal render `H_cappy` (flipped); Moody / Jim / Axie standing poses cut with BiRefNet from
  the @Moody_gp / @Jim_gp / @Axie_gp library images (`cut_*_0.png`); Ophelia = in-game head `H_ophelia_head`.
  No character went through an image model.
- Run `python3 r11.py [A_meadow B_milkyway C_vivid]` → `out/`.
