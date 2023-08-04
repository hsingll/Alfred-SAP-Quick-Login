#!/usr/bin/env python3
# coding=utf-8

import gettext
from os import environ, system
from sys import argv, exit
_ = gettext.gettext

try:
  loc = environ["language"]
  if not loc == "en_US":
    l10n = gettext.translation("Localizable", localedir="locale", languages=[loc])
    l10n.install()
    _ = l10n.gettext
except Exception:
  pass

uuid = argv[1]
shortcut = argv[2]
# uuid = "45b9d"
# shortcut = "sapshcut.exe -sid=022 -clt=200 -u=hd_llx -l=ZH -pwenc=pw_3bef7741a0e5310cf77d38319c -wsz=Maximized"

# check if argv empty
if not uuid:
  print(_('No VM selected, exit!'))
if not shortcut:
  print(_('No shortcut selected, exit!'))

# run login command
if not (uuid and shortcut):
  exit()
else:
  system(f'prlctl exec {uuid} --current-user {shortcut} 2>&1')
  print(_('Link Start!'))  # :)
