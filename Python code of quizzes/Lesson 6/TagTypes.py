#Determines the problematic tag types that exist in a dataset and their numbers.
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

#Uses regular expressions to check each element and find if it contains a problematic tag.
def key_type(element, keys):
    if element.tag == "tag":
        temp =  element.attrib['k']
        print temp
        a = re.search(lower,temp)
        b = re.search(lower_colon,temp)
        c = re.search(problemchars,temp)
        if a!=None:
              keys["lower"] =  keys["lower"] + 1     
       
        elif b!=None:
              keys["lower_colon"] =  keys["lower_colon"] + 1     
        
        elif c!=None:
              keys["problemchars"] =  keys["problemchars"] + 1     
        else:
            keys["other"] =  keys["other"] + 1
    return keys


#Processes the maps and finds probelematic tags.
def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys


#Uses other methods to find tag types and tests the output.
def test():
    keys = process_map('example.osm')
    pprint.pprint(keys)
    assert keys == {'lower': 5, 'lower_colon': 0, 'other': 1, 'problemchars': 1}


if __name__ == "__main__":
    test()