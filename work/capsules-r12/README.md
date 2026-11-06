# Round 12: real 3D hero models in the round-11 layout, bigger logo

Hero models from Drive (`assets_src/heroes3d/Heroes/`, not committed): SM_Capy, SM_Moody, SM_Bulldog_Jim, the
animations (CapyWalk, MoodyWalk, JimSprint, each with the in-game mesh) and BaseColor textures. No gear in the files.

1. `render_heroes.py`: Blender/Cycles renders of the in-game meshes from the animation FBXs, posed on an anim frame
   (Capy walk f9 tilted into flight, Moody walk f9, Jim sprint f24), lit like the meadow plate (orange fire key from
   the right, purple sky fill, front fill), shadow catcher for ground heroes. Capy's eye texture is missing, so the
   eyes are painted procedurally (vertex colours). → `renders/<name>.png`
2. Gear: `gear/p_*.txt` prompts, nano-banana-pro/edit with the render + our old render (@Cappy/@Moody/@Jim) as gear ref.
   `gear_merge.py` keeps ONLY the pixels the model added (difference mask touching the body); the body stays the 3D
   render. → `renders/<name>_gear.png`
3. `r12.py`: composite on the round-11 plates, logo ~60% of the width, Axie stays 2D. → `out/`

## Round 13 (r13.py): big 2D Cappy in the corner

Same logo + plate as round 12. Cappy = the round-11 Unreal render (H_cappy, flipped), big in the lower-right corner.
Jim = 3D render. Moody (3D) and Axie (2D) small and hazed into the background. Three arrangements → `out13/`.
