# Round 15: three new capsules + round-14 Cappy Solo at every Steam store size

`python3 r15.py [S D Q U] [header main small]` → `out/<tag>_<size>_<WxH>.jpg` (copied to
`capsules-v1/store/caps/R15<tag>_*` for the Store preview tab; S is the default proposal there).

- S: round-14 Cappy Solo re-flowed per size. D: Duel (Cappy vs giant Ophelia on lobby screenshot 2).
  Q: Squad Burst (four heroes on the brand sunburst). U: Close-Up (Cappy on teal).
- All characters are real renders (Axie = the matte-passed solo render). Backgrounds are procedural or a real
  game screenshot, except S's meadow plate. Layouts are in fractions of the canvas, one dict entry per size.

## Round 16 (r16.py): heroes vs. enemies face-off

Heroes left (Cappy lower-left corner, trio behind), enemy crew right (H_worm_bandits, H_golfer, L_pin), giant Ophelia
behind, ground + sky plates (night meadow / desert canyon / carnival). The logo is auto-placed with r15's reserve
system so nothing touches it. Main size only → `out16/`.
