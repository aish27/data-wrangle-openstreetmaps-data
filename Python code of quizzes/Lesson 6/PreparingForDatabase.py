#Prepares a XML file for the database by converting it to a JSON file.
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import string


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
                if string.find(kVal,"addr:") == 0 and kVal.count(":") == 1:
                    tempKey = kVal[string.find(kVal,":")+1:]
                    if "address" not in node:
                        node["address"] = { tempKey : vVal}
                    else: 
                        node["address"][tempKey] = vVal
                elif not(kVal.count(":") > 1):
                    node[kVal] = vVal      
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
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

#Tests if the data has properly been shaped for the database.
def test():
    data = process_map('example.osm', True)
    #pprint.pprint(data)
    
    correct_first_elem = {
        "id": "261114295", 
        "visible": "true", 
        "type": "node", 
        "pos": [41.9730791, -87.6866303], 
        "created": {
            "changeset": "11129782", 
            "user": "bbmiller", 
            "version": "7", 
            "uid": "451048", 
            "timestamp": "2012-03-28T18:31:23Z"
        }
    }
    assert data[0] == correct_first_elem
    assert data[-1]["address"] == {
                                    "street": "West Lexington St.", 
                                    "housenumber": "1412"
                                      }
    assert data[-1]["node_refs"] == [ "2199822281", "2199822390",  "2199822392", "2199822369", 
                                    "2199822370", "2199822284", "2199822281"]

if __name__ == "__main__":
    test()
