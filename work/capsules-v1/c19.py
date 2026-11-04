from compose import *
import shaders
# PRINT RUN (shader) — three-ink risograph poster: fluorescent pink, yellow, blue on cream paper.
plate = Image.new("RGBA", (W, H), (250, 235, 200, 255))
c = Comp(plate)
c.glow(1800, 520, 1400, (255, 120, 170), 0.55)
c.glow(500, 1100, 1200, (120, 200, 255), 0.45)
S = 1.6
c.place("ophelia_head", W - 613 * S + 80, H - 930 * S + 160, scale=S, match=0.0, wrap=0)
T = dict(length=240, color=(255, 255, 255), opacity=0.2, angle=195)
moody(c, 1150, 300, 0.55, trail=T, match=0, wrap=0)
jim(c, 1300, 120, 0.72, trail=T, match=0, wrap=0)
axie(c, 1240, 520, 0.11, trail=T, match=0, wrap=0)
cappy(c, 40, 520, 1.42, trail=dict(T, length=320), match=0, wrap=0)
c.canvas = ImageEnhance.Contrast(ImageEnhance.Color(c.canvas.convert("RGB")).enhance(1.5)).enhance(1.25).convert("RGBA")
c.canvas = shaders.riso(c.canvas, cell=11, shift=5)
c.logo(600, 260, 880, shadow=0.35)
c.save("19_print_run_riso", "out")
