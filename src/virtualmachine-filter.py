#!/usr/bin/env python3
# coding=utf-8
# author:Ling Leixing<lingleixing@outlook.com>

import gettext
from json import dumps, loads
from os import environ, popen
from re import search, I
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


def serialize_json():
  list = []

  if vmList == []:
    list.append({"title": _("No running VM found"), "subtitle": _("Please check VM is running"), "arg": False})
  else:
    for item in vmList:

      title = '{name}'.format(**item)  # VM name
      subtitle = _('Status: {status}').format(**item)
      argument = '{uuid}'.format(**item)  # VM uuid

      # filter if keyword isn't empty
      match = search(query, title, I)
      if query and match:
        list.append({"title": title, "subtitle": subtitle, "arg": argument})
      elif not query:
        list.append({"title": title, "subtitle": subtitle, "arg": argument})

  # no matching VM
  if list == []:
      list.append({"title": _("No matching VM found"), "subtitle": _("Please check keyword"), "arg": False})

  return dumps({"skipknowledge": True, "items": list}, ensure_ascii=False)


# keyword
query = argv[1]
# get running VMs
vmList = loads(popen("prlctl list -j").read())
# serialize json
output = serialize_json()
print(output)
