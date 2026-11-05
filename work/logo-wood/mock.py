import sys; sys.path.insert(0, "/home/user/capyverse-claude/work/capsules-r8")
import r8_sizes as R
k = sys.argv[1]
R.LOGO = f"/home/user/capyverse-claude/work/logo-wood/final/{k}.png"
R.build("C", "main", out_dir=f"/home/user/capyverse-claude/work/logo-wood/mock/{k}")
