# Capsules from a real 3D scene (round 6)

Assets: Drive "Models&Animations/November2026" (downloaded with gdown into `assets_src/`): BowlingPins, Worm, Golfer,
WastelandWarboy — FBX meshes, rigs, animations, textures, separate ST_CatHead meshes.
Not in the folders: heroes (Cappy, Moody, Jim), Ophelia, environments, screenshots.

Pipeline:
- `scene.py` (Blender 5.2 as Python module `bpy`): imports FBX, assigns textures, attaches cat heads to the `head`
  bone (rot -90,0,0), sets animation frames, poses Warboy bones by hand (its animations are for another skeleton),
  models a golf club on the golfer's right hand, Axie from fal Trellis image-to-3D (`axie3d/axie_trellis.glb`),
  shadow-catcher ground, Cycles CPU render with transparent film.
- `layouts.py L1..L5`: five scenes/cameras -> `renders/L*_3d.png` (2464x1412, RGBA with shadows).
- `compose_3d.py`: plate -> Ophelia (Unreal render, anchored right because the source crop is cut there) -> 3D layer ->
  real hero renders (Cappy biggest, popcorn/disco flares/confetti/belt thrusters) -> onomatopoeias -> logo E4.
