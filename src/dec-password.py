#!/usr/bin/env python3
# coding=utf-8
# author:Ling Leixing<lingleixing@outlook.com>

import gettext
from re import findall, I
from json import dumps
from os import environ
from sys import argv
_ = gettext.gettext

try:
  loc = environ["language"]
  if not loc == "en_US":
    l10n = gettext.translation("Localizable", localedir="locale", languages=[loc])
    l10n.install()
    _ = l10n.gettext
except Exception:
  pass


# xor
def sxor(s1, s2):
  return bytearray(a ^ b for a, b in zip(*map(bytearray, [s1, s2])))


def serialize_json():
  list = []

  if not enc_pass_hex:
    list.append({"title": _("Please enter ciphertext, then press the Enter key"), "arg": False})
  elif dec_pass:
    list.append({"title": _("Ciphertext has been converted to plaintext"), "subtitle": _("Press the Enter key to copy to clipboard"), "arg": dec_pass})
  json = dumps({"items": list}, ensure_ascii=False)
  return json


# The XOR key in hexadecimal is 78811328e0c7003ec4490d07ab090781966b63490a7ed8655ca285f354e7749f12cce8c053ba9874
key = bytes.fromhex(environ["key"])

enc_pass_hex = "".join(findall('^(?:.*?)pw_(.+?)$', argv[1], I))
enc_pass = bytes.fromhex(enc_pass_hex)
dec_pass = sxor(key, enc_pass).decode("utf-8")
# serialize
output = serialize_json()
print(output)
