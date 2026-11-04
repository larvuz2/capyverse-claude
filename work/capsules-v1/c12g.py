from c12v import *
# #12 on plain gradients (no sunburst, no scenery). Characters, FX and layout identical to 12a.

def grad(stops, kind="linear", angle=90, center=(0.5, 0.35), grain=0.012):
    """stops: [(pos 0..1, (r,g,b)), ...]. linear angle in degrees (90 = top->bottom)."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    if kind == "linear":
        a = math.radians(angle); dx, dy = math.cos(a), math.sin(a)
        t = (xx / W - 0.5) * dx * (W / H) + (yy / H - 0.5) * dy
        t = (t - t.min()) / (t.max() - t.min())
    else:
        t = np.hypot((xx / W - center[0]) * W / H, yy / H - center[1]); t = np.clip(t / 1.05, 0, 1)
    pos = np.array([p for p, _ in stops]); cols = np.array([c_ for _, c_ in stops], np.float32)
    rgb = np.stack([np.interp(t, pos, cols[:, i]) for i in range(3)], -1)
    rgb += np.random.default_rng(0).normal(0, grain * 255, rgb.shape[:2])[..., None]  # tiny grain, no banding
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert("RGBA")

Y, O = (255, 212, 38), (255, 120, 20)
OPTIONS = {
    "g1_vertical":   (grad([(0, Y), (1, O)], angle=90), "Vertical: golden yellow on top to vibrant orange at the bottom (the original gradient)."),
    "g2_diagonal":   (grad([(0, (255, 226, 60)), (1, (255, 104, 18))], angle=35), "Diagonal: bright yellow top-left to deep orange bottom-right."),
    "g3_radial":     (grad([(0, (255, 236, 120)), (0.45, Y), (1, O)], kind="radial", center=(0.5, 0.3)), "Radial: a soft yellow glow behind the logo and heroes, orange at the edges."),
    "g4_sunset":     (grad([(0, (255, 214, 50)), (0.55, (255, 128, 24)), (1, (232, 52, 40))], angle=90), "Three stops: yellow to orange to red, warmer and heavier at the bottom."),
    "g5_flat":       (grad([(0, (255, 160, 28)), (1, (255, 140, 22))], angle=90, grain=0.006), "Almost flat orange: the plainest option, everything rides on the characters."),
    "g6_sky":        (grad([(0, (80, 190, 255)), (1, (20, 110, 230))], angle=90), "Off-brand test: Crab Champions sky blue, the warm characters pop against it."),
    "g7_teal":       (grad([(0, (60, 210, 200)), (1, (10, 120, 130))], angle=90), "Off-brand test: teal, cool contrast for the orange capybara."),
    "g8_purple":     (grad([(0, (230, 70, 170)), (1, (90, 30, 150))], angle=90), "Off-brand test: magenta to purple, Ophelia's colors."),
}
RIMS = {"g6_sky": (230, 245, 255), "g7_teal": (220, 255, 250), "g8_purple": (255, 210, 245)}

if __name__ == "__main__":
    import sys, json
    which = sys.argv[1:] or list(OPTIONS)
    for k in which:
        build(f"12{k}", plate=OPTIONS[k][0], rim=RIMS.get(k), grade=dict(contrast=1.04, sat=1.05, vignette=0.32))
    json.dump({k: v[1] for k, v in OPTIONS.items()}, open("out/12g_notes.json", "w"), indent=1)
