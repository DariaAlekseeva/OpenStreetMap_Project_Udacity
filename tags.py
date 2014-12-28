#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
"""
Function uses 3 regular expressions to check for certain patterns
in the tags. Function helps to find problematic format of tags.
Function key_type takes 'k' attribute of 'tag', compares it with
regular expressions and returns a dictionary with a type of tag
as key and number these tags in file as value.
"""

TEST_FILE = "example.osm"
FILE = "map.osm"

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        if lower.search(element.attrib['k']):
            keys["lower"] +=1
        elif lower_colon.search(element.attrib['k']):
            keys["lower_colon"] +=1        
        elif problemchars.search(element.attrib['k']):
            keys["problemchars"] +=1
        else:
            keys["other"] +=1
    return keys



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

def test():
    keys = process_map(FILE)
    pprint.pprint(keys)


print test()