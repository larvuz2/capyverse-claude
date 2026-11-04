import sys; sys.path.insert(0, "/home/user/capyverse-claude/work/capsules-v1")
import os; os.chdir("/home/user/capyverse-claude/work/capsules-v1")
from c12g import *
L = "/home/user/capyverse-claude/work/logo-lab/out"
which = sys.argv[1]
cfg = {
  "a": dict(logo_path=f"{L}/logo_a_trim.png", logo_w=1100, logo_xy=(620, 230)),
  "b": dict(logo_path=f"{L}/logo_b_trim.png", logo_w=1100, logo_xy=(620, 230)),
  "c": dict(logo_path=f"{L}/logo_c_stacked_trim.png", logo_w=640, logo_xy=(440, 290)),
  "c2": dict(logo_path=f"{L}/logo_c_word_trim.png", logo_w=1000, logo_xy=(600, 220)),
  "d": dict(logo_path=f"{L}/logo_d_trim.png", logo_w=900, logo_xy=(560, 250)),
  "e": dict(logo_path=f"{L}/logo_e_trim.png", logo_w=880, logo_xy=(560, 270)),
  "f": dict(logo_path=f"{L}/logo_f_trim.png", logo_w=900, logo_xy=(560, 260)),
  "d2": dict(logo_path=f"{L}/logo_d2_trim.png", logo_w=900, logo_xy=(560, 240)),
  "e2": dict(logo_path=f"{L}/logo_e2_trim.png", logo_w=920, logo_xy=(570, 250)),
  "f2": dict(logo_path=f"{L}/logo_f2_trim.png", logo_w=900, logo_xy=(560, 250)),
  "g": dict(logo_path=f"{L}/logo_g_trim.png", logo_w=900, logo_xy=(560, 240)),
  "h": dict(logo_path=f"{L}/logo_h_trim.png", logo_w=960, logo_xy=(580, 250)),
  "i": dict(logo_path=f"{L}/logo_i_trim.png", logo_w=920, logo_xy=(570, 250)),
  "gpt": dict(logo_path=f"{L}/logo_gpt_stumble_trim.png", logo_w=900, logo_xy=(560, 260)),
  "old": dict(),
}[which]
build(f"logo_mock_{which}", plate=OPTIONS["g1_vertical"][0], grade=dict(contrast=1.04, sat=1.05, vignette=0.32), **cfg)
