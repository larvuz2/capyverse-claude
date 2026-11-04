from compose import *
# OPHELIA RISING — Risk of Rain scale: a colossal Ophelia rises over the dunes at dusk. Cappy flies to meet her.
c = Comp("plates_used/v2_dusk_dunes_nbp_0.jpg", focus=(0.5, 0.5))
S = 1.55
ox, oy = W - 613 * S + 10, 880 - 930 * S
c.place("ophelia_head", ox, oy, scale=S, bright=0.82, sat=0.75, match=0.45, opacity=0.95,
        rim=dict(color=(255, 170, 140), dir=(1, 0), width=12, strength=0.8))
# haze band over her base so she sits behind the horizon
haze = Image.new("RGBA", (W, H), (0, 0, 0, 0)); hd = ImageDraw.Draw(haze)
for i in range(420):
    hd.line([(0, 520 + i), (W, 520 + i)], fill=(255, 150, 110, int(200 * min(1, i / 300) * math.sin(math.pi * min(i, 400) / 800))))
c.canvas.alpha_composite(haze.filter(ImageFilter.GaussianBlur(20)))
for ex, ey in ((165, 520), (453, 496)): c.glow(ox + ex * S, oy + ey * S, 130, (255, 30, 40), 0.85)
DR = dict(color=(255, 180, 140), dir=(1, -1), width=8, strength=0.85)
T = dict(length=320, color=(255, 210, 180), opacity=0.25, angle=195)
fs = dict(dx=60, dy=420, blur=45, opacity=0.25, squash=0.18)
moody(c, 1330, 760, 0.6, rim=DR, trail=dict(T, length=170))
jim(c, 1560, 1080, 0.8, rim=DR, trail=dict(T, length=150))
axie(c, 1720, 900, 0.12, rim=DR, trail=dict(T, length=170))
cappy(c, 0, 560, 1.38, rim=DR, trail=T, shadow=fs)
c.logo(600, 270, 900, glow=(255, 200, 170))
c.grade(contrast=1.06, sat=1.06, vignette=0.42, bloom=0.2)
c.save("14_ophelia_rising", "out")
