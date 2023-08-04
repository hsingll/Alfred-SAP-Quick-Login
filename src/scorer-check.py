#!/usr/bin/env python3
# coding=utf-8

import gettext
from os import environ
from sys import exit
_ = gettext.gettext

try:
  loc = environ["language"]
  if not loc == "en_US":
    l10n = gettext.translation("Localizable", localedir="locale", languages=[loc])
    l10n.install()
    _ = l10n.gettext
except Exception:
  pass

enableFuzzywuzzy = environ["enableFuzzywuzzy"]
if enableFuzzywuzzy == "0":
  exit()
try:
  scorer = int(environ["scorer"])
except ValueError:
  scoreTypeError = True
else:
  scoreTypeError = False

if scoreTypeError is True or scorer < 1 or scorer > 100:
  print(_('score must be an integer of [1, 100]!'))
