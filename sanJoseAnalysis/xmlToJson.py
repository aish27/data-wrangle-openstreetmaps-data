#Prepares a XML file for the database by converting it to a JSON file.
__author__ = 'Aishwarya'

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import string
import os

#Converts the xml file into json format.
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


#Defines the shape of a particular element in JSON format.
def shape_element(element):
    if element.tag == "node" or element.tag == "way" :
        val =  element.attrib
        lat1 = None
        lon1 = None
        if element.tag == "node":
            lat1 = float(val['lat'])
            lon1 = float(val['lon'])
        visible1 = None
        if "visible" in val:
            visible1 = val["visible"]
        node = {
        "id": val["id"],
        "visible": visible1,
        "type": element.tag,
        "pos": [lat1,lon1],
        "created": {
            "changeset": val["changeset"],
            "user": val["user"],
            "version": val["version"],
            "uid": val["uid"],
            "timestamp": val["timestamp"]
        }
        }
        # get second level tags
        for child in element:
                if 'ref' in child.attrib:
                    temp = child.attrib['ref']
                    if "node_refs" not in node:
                        node["node_refs"] = list()
                    node["node_refs"].append(temp)
                elif 'k' in child.attrib:
                    kVal = clean(child.attrib['k'])
                    vVal =  child.attrib['v']
                    if string.find(kVal,"address") == 0 or string.find(kVal,"type") == 0:
                        print kVal
                        pass
                    elif string.find(kVal,"addr:") == 0 and kVal.count(":") == 1:
                        tempKey = kVal[string.find(kVal,":")+1:]
                        if "address" not in node:
                            node["address"] = { tempKey : vVal}
                        else:
                            node["address"][tempKey] = vVal
                    elif not(kVal.count(":") > 1):
                        node[kVal] = vVal
                    else:
                        pass
        return node
    else:
        return None


#Cleans the data by removing problematic characters.
def clean(temp):
        a = re.search(lower,temp)
        b = re.search(lower_colon,temp)
        c = re.search(problemchars,temp)
        if a!=None:
              pos = string.find(temp,a.group(0))
              if pos !=-1 and pos!=0:
                          kVal = temp[0:pos]
              else:
                          kVal = temp

        elif b!=None:
              pos = string.find(temp,b.group(0))
              if pos !=-1 and pos!=0:
                          kVal = temp[0:pos]
              else:
                          kVal = temp

        elif c!=None:
              pos = string.find(temp,c.group(0))
              if pos !=-1 and pos!=0:
                          kVal = temp[0:pos]
              else:
                          kVal = temp
        else:
            kVal = temp
        return kVal

#Reads a file and iteratively parses it. Then, uses other methods to convert the XML doc to a JSON format and writes it to another file.  
def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "test.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        fo.write("[")
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
                fo.write(",")
        fo.seek(-1, os.SEEK_END)
        fo.truncate()
        fo.write("]")
    return data

#Uses other methods to finish the required task [convert xml to json].
def test():
    data = process_map('san-jose_california.osm', True)
    #pprint.pprint(data)

if __name__ == "__main__":
    test()