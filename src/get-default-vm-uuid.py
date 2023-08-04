#!/usr/bin/env python3
# coding=utf-8
# author:Ling Leixing<lingleixing@outlook.com>

from os import environ
from re import findall
from xml.dom.minidom import parse


# path of default VM
defaultVM = environ["defaultVM"]
if defaultVM:
  configXML = f'{defaultVM}/config.pvs'
  # using minidom parse XML
  DOMTree = parse(configXML)
  defaultVMuuid = findall('^(?:.*?){(.+?)}(?:.*?)$', DOMTree.documentElement.getElementsByTagName("Identification")[0].getElementsByTagName("VmUuid")[0].firstChild.nodeValue)[0]
  print(defaultVMuuid, end="")
