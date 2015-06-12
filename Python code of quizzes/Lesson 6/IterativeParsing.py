#Iteratively parses an XML document and records the type of tags it contains and the number of each tag occurs.
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint

"""
Counts the tags and writes the tags (and their number) to a dictionary.Returns the dictionary.
"""
def count_tags(filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        tags = dict()
        with open(filename, "r") as read:
                for child in root.iter():
                    print child.tag
                    addTagToDict(child.tag,tags)
                  
        return tags

#Helper method that helps in adding the tag to a dictionary.
def addTagToDict(tag, tags):
    #print tag
    #print tags
    if tag in tags:
        tags[tag] = tags[tag]+1
    else:
        tags[tag] = 1
    return tags

#Tests if we got the expected output.
def test():
    tags = count_tags('example.osm')
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                     'member': 3,
                     'nd': 4,
                     'node': 20,
                     'osm': 1,
                     'relation': 1,
                     'tag': 7,
                     'way': 1}

    

if __name__ == "__main__":
    test()