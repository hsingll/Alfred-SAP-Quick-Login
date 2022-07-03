#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import re
import sys

fuzzysearch = True # True尝试使用fuzzywuzzy.process.extract匹配
try:
    from fuzzywuzzy import process, fuzz
except:
    fuzzysearch = False

QUERY = sys.argv[1].decode("utf-8")
SHORTCUT_DIR = os.environ['shortcut_dir']


# TODO: list_shortcuts creates cache of shortcuts for first time
def list_shortcuts():
    ret = []
    SHORTCUT_FILE = io.open(SHORTCUT_DIR,encoding="gbk")
    line = SHORTCUT_FILE.readline()
    shortcut = False
    while line:
        if shortcut == False:
            if line == "[Command]\n":
                shortcut = True
        elif shortcut == True:
            ret.append("".join(re.findall(r"Key(?:.*?)=(.*)\n",line)))
        line = SHORTCUT_FILE.readline()
    SHORTCUT_FILE.close()

    return sorted(ret, key=lambda s: s.lower())


def search_shortcuts(query):
    ''' Search shortcuts using the Fuzzy search method if fuzzywuzzy is available,
    or default to the filter-based search otherwise'''
    if fuzzysearch:
        return search_shortcuts_fuzzy(query)
    return search_shortcuts_filter(query)


def search_shortcuts_fuzzy(query):
    ''' Search shortcuts using the Fuzzy search method using fuzzywuzzy'''
    shortcuts = list_shortcuts()
    #搜索关键词是非ascii字符时注意,https://segmentfault.com/q/1010000009868699
    return [entry[0] for entry in process.extract(query, shortcuts, scorer=fuzz.UWRatio, limit=10)]


def search_shortcuts_filter(query):
    ''' Search shortcuts using the filter-based search, which doesn't require fuzzywuzzy'''
    ret = []

    terms = filter(lambda x: x, query.lower().split())
    shortcuts = list_shortcuts()

    for shortcut in shortcuts:
        for t in terms:
            if t not in shortcut.lower():
                break
        else:
            ret.append(shortcut)

    return ret


def xmlize_items(items, query):
    items_a = []

    for item in items:
        desc = "".join(re.findall(r'(?:.*?)-desc="(.+?)"',item)) # 连接名称
        sid = "".join(re.findall(r'(?:.*?)-sid="(.+?)"',item)) # 系统标识
        clt = "".join(re.findall(r'(?:.*?)-clt="(.+?)"',item)) # 客户端
        user = "".join(re.findall(r'(?:.*?)-u="(.+?)"',item)) # 用户
        lang = "".join(re.findall(r'(?:.*?)-l="(.+?)"',item)) # 登录语言

        title = "".join(re.findall(r'(?:.*?)-tit="(.+?)"',item)) # 快捷方式标题
        subtitle = u"继续登录"+desc+u"(系统标识"+sid+u")客户端"+clt+u"账户"+user+u"登录语言"+lang
        items_a.append("""
    <item arg='%(item)s' autocomplete='%(item)s'>
        <title>%(title)s</title>
        <subtitle>%(subtitle)s</subtitle>
    </item>
        """ % {'item':item, 'title':title, 'subtitle':subtitle})

    return """
<?xml version="1.0"?>
<items>
    %s
</items>
    """ % '\n'.join(items_a)


items = search_shortcuts(QUERY)
print xmlize_items(items, QUERY)

