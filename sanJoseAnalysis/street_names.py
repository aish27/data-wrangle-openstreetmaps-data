#Improves the street names by auditing and cleaning data using code given below.
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import string

#OSM file to read data from.
OSMFILE = "san-jose_california.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

#List of expected street names. 'expected' contains expected suffixes and 
#'expectedPrefixStreetTypes' contains expected prefixes. .
expected =["Street","Avenue","Boulevard","Drive","Court","Place","Lane","Road",
           "Square","Trail","Parkway","Commons","Circle","Expressway","Way",
           "Highway","Loop","Terrace","Walk","Real","Hill","West","East","Row"]
expectedPrefixStreetTypes = ["Camina", "Calle", "Paseo","Rio","West","South",
                             "North","East"]

#List of mappings for contractions.
mapping = { "St": "Street",
            "St.": "Street",
            "Ave" : "Avenue",
            "Rd.":  "Road",
            "Rd":  "Road",
            "Blvd":"Boulevard",
            "Blvd.":"Boulevard",
            "Ct":"Court",
            "Ln":"Lane",
            "Sq":"Square",
            "ave":"Avenue",
            "street":"Street",
            "Cir":"Circle",
            "Dr":"Drive",
            "Hwy":"Highway",
            "S." :"South",
            "S":"South",
            "N":"North",
            "N." :"North",
            "W":"West",
            "W." :"West",
            "E.":"East",
            "E" :"East"
            }

#Audits a street name by examining its street type (prefix and suffix).
# If it contains words that unexpected, it adds the unexpected name to a list
#  and returns the list.
def audit_street_type(street_types, street_name):
    street_name = street_name.title()
    if "," in street_name:
        street_name = street_name[:string.find(street_name,",")]
        street_name = street_name.strip()
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type.isdigit() or re.match("^\d+?\.\d+?$",street_type) is not None:
            pass
        elif (street_type not in expected):
            if string.find(street_name," ")!=-1:
                prefixStreetType = street_name[:string.find(street_name," ")]
                if (prefixStreetType not in expectedPrefixStreetTypes):
                    street_types[street_type].add(street_name)
            else:
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
    name = name.title()
    if "," in name:
        street_name = name[:string.find(name,",")]
        name = name.strip()
    tempP = string.find(name," ")
    tempS = string.rfind(name," ")
    valS = name[tempS+1:]
    valP = name[:tempP]
    if valS in mapping and valP not in mapping:
        return  name[:tempS+1] + mapping[valS]
    if valP in mapping and valS not in mapping:
        return  mapping[valP] +  name[tempP:]
    if valS in mapping and valP in mapping:
         return  mapping[valP] + name[tempP:tempS+1] + mapping[valS]
    else:
        return name

#Uses other methods to check if a value is a valid street name and
# clean the street name.
def test():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name




if __name__ == '__main__':
    test()