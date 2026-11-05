import sys; sys.path.insert(0, "/home/user/capyverse-claude/work/capsules-r8")
import r8_sizes as R
R.LOGO = "/home/user/capyverse-claude/work/logo-tin/tin_hanging.png"
_fit = R.fit_logo
R.fit_logo = lambda mask, cw, ch, prefer=(0.52, 0.30), max_frac=0.9: _fit(mask, cw, ch, prefer=(0.52, 0.28), max_frac=0.9)
_cm = R.char_mask
R.char_mask = lambda lay, pad: _cm(lay, max(4, pad // 3))   # let the logo come closer to the characters
for size in ("main", "header", "small"):
    print(size, "%.2f" % R.build("C", size, out_dir="/home/user/capyverse-claude/work/logo-tin/mock"))
