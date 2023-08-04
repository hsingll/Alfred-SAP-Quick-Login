#!/usr/bin/env python3
# coding=utf-8

import gettext
from os import environ
from re import compile, error
_ = gettext.gettext

try:
  loc = environ["language"]
  if not loc == "en_US":
    l10n = gettext.translation("Localizable", localedir="locale", languages=[loc])
    l10n.install()
    _ = l10n.gettext
except Exception:
  pass

RegExrPWEnc = environ["RegExrPWEnc"]
if RegExrPWEnc:
  try:
    compile(RegExrPWEnc)
  except error:
    print(_('Regular expression password(ciphertext) is invalid!'))
else:
  print(_('Regular expression password(ciphertext) is empty!'))
