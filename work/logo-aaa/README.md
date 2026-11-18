# Logo round 15: five handcrafted PC-title wordmarks (all caps, letters only, transparent)

Built entirely in code. No image model, no stock textures.

Research: the Steam `logo.png` of ~40 current PC titles (Silksong, Elden Ring, God of War, Borderlands 4, Split Fiction,
Sea of Thieves, Ratchet & Clank, Deep Rock Galactic, Biomutant, Kena, ...). Common traits: capitals, no plaque, tall and
tight, one material, one or two colours, one signature letter, small wide-spaced subtitle.

| File | What it does |
|---|---|
| `craft.py` | Toolkit: font outlines → shapely geometry (exact non-zero winding), optical letter spacing, raster canvas, distance fields, bevel profiles, normals, lighting, metal reflection ramps, layered value noise. |
| `geom.py` | The five letter designs as geometry: hand edits (tall middle V, mirrored A, tin-snipped corners, speed slits, brass inlay ring), spacing, subtitles, rules. `python3 geom.py` writes flat proofs. |
| `render.py` | The five materials, per pixel: chiseled gold, oak + inlaid brass, chipped enamel tin with nails and rust, enamel-and-chrome badge, flat vector. `python3 render.py [1-5]` → `out/`. |
| `mock.py` | Each mark on the round-18 Meadow capsule, auto-placed clear of the characters → `mock/`. |

Fonts (`fonts/`, all SIL Open Font License, from Google Fonts): Cinzel (Black/Bold instances), Alfa Slab One, Anton,
Kanit Black Italic, Unbounded (Black/Bold instances).

1. **Gilt**: Cinzel. V is the 5th of 9 letters, so it becomes a tall wedge through the rule, pointing at ODYSSEY.
2. **Oak & Brass**: Alfa Slab One. One oak block per letter, brass wire inlaid along every stroke.
3. **Tin Type**: Anton. Enamelled tin letters, snipped corners, nails, rust. The letters-only heir of Tin on Wood.
4. **Jet Badge**: Kanit Black Italic. Enamel face in a chrome rim, speed slits, needle trail to ODYSSEY.
5. **Pure**: Unbounded. Flat, one colour; A = inverted V; the O of ODYSSEY is a solid orange disc. Also as SVG, cream + ink.
