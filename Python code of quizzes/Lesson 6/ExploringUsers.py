"""
Finds out how many unique users have contributed to the map in this particular area!
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re

#Gets the user who contributed to a particular tag.
def get_user(element):
    if element.tag == "node" or  element.tag == "way" or  element.tag == "relation":
           return element.attrib["uid"]
           


#The function process_map returns a set of unique user IDs ("uid").
def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        temp = get_user(element)
        if temp != None and temp not in users:
            users.add(temp)

    return users

$Tests if we got the expected output.
def test():

    users = process_map('example.osm')
    pprint.pprint(users)
    assert len(users) == 6



if __name__ == "__main__":
    test()