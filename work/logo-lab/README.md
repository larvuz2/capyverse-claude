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
