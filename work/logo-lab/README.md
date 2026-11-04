# Logo lab — 3 directions (Nov 2026)

Live page: https://claude.ai/artifact/95iDZxS99Uzs7tz4cNzqF5

Built by hand as vector art: `svglogo.py` turns real font outlines (fontTools) into SVG paths that are re-set
letter by letter; the capybara, popcorn, verified badge, play button and planet are hand-written SVG paths.
`render.js` rasterises with the preinstalled Chromium. Final SVGs contain only paths (no font dependency).

| Dir | File | Idea |
|---|---|---|
| A Popcorn Pop | `logo_a.py` → `out/logo_a.svg` | Titan One, bouncing letters, Cappy-head C, popcorn O on a popcorn-bucket band, jetpack streaks |
| B Going Viral | `logo_b.py` → `out/logo_b.svg` | Rubik Black sheared, verified badge, play-button O in a notification pill, heart reaction |
| C Capy Planet | `logo_c.py` → `out/logo_c*.svg` | capybara-head planet emblem + Chango wordmark; horizontal, stacked, icon |

Recommendation: B as the logo, C's planet as the app icon. Re-render: `python3 logo_b.py` (needs fonttools, node + playwright).
Research: 21 Steam library logos (`page/steam_logos.jpg`), type audition (`specimen.png`), size tests (`out/sizes/`),
capsule mocks via `mock.py` (uses `work/capsules-v1/c12g.py`, `build(logo_path=...)`).

## Round 2 — C without emblem + D, E, F (Luckiest Guy, two rows)

- C → `logo_c.py` `wordmark_only()` → `out/logo_c_word.svg`
- `logo_def.py`: D Toybox (bouncy two rows, cream/orange, sticker outline), E Stumble (Stumble Guys structure:
  small white tilted CAPYVERSE over huge gold ODYSSEY on a navy 3D block), F Marquee (arched CAPYVERSE + ODYSSEY tag)
- `page/steam_logos_with_ours.jpg`: research grid with B inserted. Recommendation: B, runner-up E.

## Round 3 — unified lockups, collision-free, + GPT 2.5 Stumble style

- `lockup.py`: letters placed with explicit matrices; `Row.check()` tests real glyph outlines (shapely) for touching
  neighbours; `draw()` renders all rows as one object (shared silhouette, outline, 3D block, sticker).
- `logo_v3.py`: D2 Toybox, E2 Stumble (CAPYVERSE big), F2 Marquee, G Popcorn Band, H Viral Stumble (winner), I Jetpack.
  Auto-kerning fixed the old Toybox collisions (Y/V 585 px², A/P, E/R, S/E).
- `gpt/`: Stumble Guys logo -> GPT Image 2.5 edit (`gpt/prompt.txt`, 3 takes) + nano-banana-pro (2 takes);
  take `gpt25_2` upscaled 3x (SeedVR) and cleaned by `clean_gpt.py` (even navy outline, black blobs removed, transparent)
  -> `out/logo_gpt_stumble.png`.
- `page/steam_logos_with_winner.jpg`: the 21 research logos + H at the end.

## Round 4 — designed overlaps (D3, E3, H3)

`logo_v4.py` + `lockup.overlap_kern()` / `draw_layered()`: instead of pushing letters apart, every neighbour pair is tuned
to a target overlap (1.2–3.5% of the smaller glyph), and each letter is drawn as its own outlined object in z-order, so
overlaps get a clean outline seam (Stumble Guys style). Rows overlap by 12–14 px. H3 adds jetpack thruster streaks.

## Round 5
- `logo_v5.py` E4: `selective_kern` — only CAPYVERSE Y/V overlap (1.5–3.5%); all other pairs 3–9 px apart (shapely distance).
- `out/logo_gpt_stumble_backed.png`: GPT Stumble version with a solid navy backing (morphological close r≈45px, holes filled, smoothed).
