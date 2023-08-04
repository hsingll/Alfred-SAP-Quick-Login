#!/usr/bin/env python3
# coding=utf-8

import gettext
from os import environ, path
_ = gettext.gettext

try:
  loc = environ["language"]
  if not loc == "en_US":
    l10n = gettext.translation("Localizable", localedir="locale", languages=[loc])
    l10n.install()
    _ = l10n.gettext
except Exception:
  pass

SAPUILandscape = environ["SAPUILandscape"]
if SAPUILandscape:
  if path.exists(SAPUILandscape):
    if path.basename(SAPUILandscape) != "SAPUILandscape.xml":
      print(_('Filename of SAP UI Landscape XML mismatch!'))
  else:
    print(_('SAP UI Landscape XML isn\'t exit!'))
else:
  print(_('Path of SAP UI Landscape XML is empty!'))
