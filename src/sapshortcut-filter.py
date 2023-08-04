#!/usr/bin/env python3
# coding=utf-8
# author:Ling Leixing<lingleixing@outlook.com>

import gettext
from json import dumps, loads
from os import environ
from re import findall, search, I
from sys import argv
from xml.dom.minidom import parse
_ = gettext.gettext

try:
  loc = environ["language"]
  if not loc == "en_US":
    l10n = gettext.translation("Localizable", localedir="locale", languages=[loc])
    l10n.install()
    _ = l10n.gettext
except Exception:
  pass

# enable/disable fuzzy matching
enableFuzzywuzzy = environ["enableFuzzywuzzy"]
if enableFuzzywuzzy == "1":
  try:
    from fuzzywuzzy import process, fuzz
  except ImportError:
    fuzzysearch = False
  else:
    fuzzysearch = True
else:
  fuzzysearch = False


# Traversing SAPUILandscape.xml, return shortcuts
def list_shortcuts():
  shortcuts = []
  # using minidom parse XML
  DOMTree = parse(SAPUILandscape)
  Landscape = DOMTree.documentElement
  Services = Landscape.getElementsByTagName("Services")[0].getElementsByTagName("Service")

  for Service in Services:
    if Service.getAttribute("type") != "Reference":  # continue if not shortcut
      continue
    name = Service.getAttribute("name")          # name
    desc = Service.getAttribute("description")   # descrption
    sid = Service.getAttribute("systemid")       # system id
    clt = Service.getAttribute("client")         # client
    user = Service.getAttribute("user")          # user
    lang = Service.getAttribute("language")      # login language
    Memo = Service.getElementsByTagName("Memo")  # remarks
    wd = Service.getAttribute("work_dir")        # work dir
    winmax = Service.getAttribute("winmax")      # window size
    if Memo:
      RegExrPWEnc = environ["RegExrPWEnc"]
      pwenc = "".join(findall(RegExrPWEnc, Memo[0].childNodes[0].data))  # password(ciphertext)
    tmp = ({"name": name, "desc": desc, "sid": sid, "clt": clt, "user": user, "lang": lang, "wd": wd, "winmax": winmax, "pwenc": pwenc})
    shortcut = dumps(tmp, ensure_ascii=False)
    shortcuts.append(shortcut)
  else:
    shortcuts.sort(key=lambda x: x.lower())
    return shortcuts


# fuzzy matching
def search_shortcuts_fuzzy(shortcuts):
  match = filter(lambda x: x[1] >= scorer, process.extract(query, shortcuts, scorer=fuzz.UWRatio, limit=30))
  list = [entry[0] for entry in match]
  return list


# re.search matching(case-insensitive)
def search_shortcuts_filter(shortcuts):
  list = []
  for shortcut in shortcuts:
    match = search(query, shortcut, I)
    if match:
      list.append(shortcut)
  return list


# return matching result
def search_shortcuts():
  shortcuts = list_shortcuts()
  if query:
    # fuzzy matching first
    if fuzzysearch:
      list = search_shortcuts_fuzzy(shortcuts)
    else:
      list = search_shortcuts_filter(shortcuts)
  else:
    list = []
  return list


def serialize_json():
  list = []
  if not items:
    if query:
      list.append({"title": _("No matching shortcut found"), "subtitle": _("Please check keyword and SAPUILandscape.xml"), "arg": False})
    else:
      list.append({"title": _("Please enter keyword to search shortcuts"), "arg": False})
  else:
    for item in items:
      jsonobj = loads(item)
      winmax = jsonobj["winmax"]  # window size

      title = '{name}'.format(**jsonobj)  # shortcut name
      subtitle = _('Login on {desc} client {clt} with user {user} in language {lang}').format(**jsonobj)
      argument = ('sapshcut.exe -sid={sid} -clt={clt} -u={user} -l={lang} -pwenc={pwenc}').format(**jsonobj)
      if winmax == "1":  # window maximum
        argument = f'{argument} -wsz=Maximized'

      list.append({"title": title, "subtitle": subtitle, "arg": argument})
  json = dumps({"items": list}, ensure_ascii=False)
  return json


query = argv[1]
if fuzzysearch:
  if query.strip():
    scorer = int(environ["scorer"])
  else:
    scorer = 0
SAPUILandscape = environ["SAPUILandscape"]
# get shortcuts
items = search_shortcuts()
# serialize
output = serialize_json()
print(output)
