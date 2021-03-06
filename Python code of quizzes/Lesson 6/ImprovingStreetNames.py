#Improves the street names by auditing and cleaning data using code given below.
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import string

#OSM file to read data from.
OSMFILE = "example.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

#List of expected street names. 'expected' contains expected suffixes.
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

#List of mappings for contractions.
mapping = { "St": "Street",
            "St.": "Street",
            "Ave" : "Avenue",
            "Rd.":  "Road"

            }

#Audits a street name by examining its street type (prefix and suffix).
# If it contains words that unexpected, it adds the unexpected name to a list and returns the list.
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

#Checks if the current value is a street name.
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

#Audits a street name by using several methods
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    return street_types

#Updates a street name by using the mappings provided above
def update_name(name, mapping):
    temp = string.rfind(name," ")
    val = name[temp+1:]
    if val in mapping:
        return  name[:temp+1] + mapping[val]

#Uses other methods to check if a value is a valid street name and clean the street name.
def test():
    st_types = audit(OSMFILE)
    assert len(st_types) == 3
    pprint.pprint(dict(st_types))
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            if name == "West Lexington St.":
                assert better_name == "West Lexington Street"
            if name == "Baldwin Rd.":
                assert better_name == "Baldwin Road"

if __name__ == '__main__':
    test()