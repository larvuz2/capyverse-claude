import sys; sys.path.insert(0, "/home/user/capyverse-claude/work/capsules-v1")
import os; os.chdir("/home/user/capyverse-claude/work/capsules-v1")
from c12g import *
L = "/home/user/capyverse-claude/work/logo-lab/out"
which = sys.argv[1]
cfg = {
  "a": dict(logo_path=f"{L}/logo_a_trim.png", logo_w=1100, logo_xy=(620, 230)),
  "b": dict(logo_path=f"{L}/logo_b_trim.png", logo_w=1100, logo_xy=(620, 230)),
  "c": dict(logo_path=f"{L}/logo_c_stacked_trim.png", logo_w=640, logo_xy=(440, 290)),
  "old": dict(),
}[which]
build(f"logo_mock_{which}", plate=OPTIONS["g1_vertical"][0], grade=dict(contrast=1.04, sat=1.05, vignette=0.32), **cfg)
