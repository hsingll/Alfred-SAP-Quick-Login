#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import re
import sys

fuzzysearch = False # True尝试使用fuzzywuzzy.process.extract匹配。但是尝试下来中文关键字的准确性不好，暂不启用。
try:
    from fuzzywuzzy import process
except:
    fuzzysearch = False

QUERY = sys.argv[1].decode("utf-8")
# SHORTCUT_DIR = sys.argv[2]
SHORTCUT_DIR = os.environ['shortcut_dir']
# SHORTCUT_DIR = '/Users/Simon/Library/Mobile Documents/com~apple~CloudDocs/应用/SAP/Config/sapshortcut.ini'


# TODO: list_passwords creates cache of passwords for first time
def list_passwords():
    ret = []
    SHORTCUT_FILE = io.open(SHORTCUT_DIR,encoding="gbk")
    line = SHORTCUT_FILE.readline()
    start = False
    while line:
        if start == False:
            if line == "[Command]\n":
                start = True
        elif start == True:
            ret.append("".join(re.findall(r"Key(?:.*?)=(.*)\n",line)))
        line = SHORTCUT_FILE.readline()
    SHORTCUT_FILE.close()

    return sorted(ret, key=lambda s: s.lower())


def search_passwords(query):
    ''' Search passwords using the Fuzzy search method if fuzzywuzzy is available,
    or default to the filter-based search otherwise'''
    if fuzzysearch:
        return search_passwords_fuzzy(query)
    return search_passwords_filter(query)


def search_passwords_fuzzy(query):
    ''' Search passwords using the Fuzzy search method using fuzzywuzzy'''
    passwords = list_passwords()
    return [entry[0] for entry in process.extract(query, passwords, limit=10)]


def search_passwords_filter(query):
    ''' Search passwords using the filter-based search, which doesn't require fuzzywuzzy'''
    ret = []

    terms = filter(lambda x: x, query.lower().split())
    passwords = list_passwords()

    for password in passwords:
        for t in terms:
            if t not in password.lower():
                break
        else:
            ret.append(password)

    return ret


def xmlize_items(items, query):
    items_a = []

    for item in items:
        name = "".join(re.findall(r'(?:.*?)-tit="(.+?)"',item))

        items_a.append("""
    <item arg='%(item)s' autocomplete='%(item)s'>
        <title>%(name)s</title>
        <subtitle>%(item)s</subtitle>
    </item>
        """ % {'item': item, 'name': name, 'complete': name})

    return """
<?xml version="1.0"?>
<items>
    %s
</items>
    """ % '\n'.join(items_a)


items = search_passwords(QUERY)
print xmlize_items(items, QUERY)

