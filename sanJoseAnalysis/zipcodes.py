#Improves the zipcodes by auditing and cleaning data using code given below.
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import string


#OSM file to read data from.
OSMFILE = "san-jose_california.osm"

#Audits a zipcode by examining its first two characters. Zipcode should begin with 94 or 95.
# If it contains words that unexpected, it adds the unexpected name to a list and returns the list.
def audit_zipcode(postcodes, zipcode):
    testNum = zipcode[0:2]
    if not(testNum.isdigit()):
        postcodes[testNum].add(zipcode)
    elif int(testNum) != 94 and int(testNum) != 95:
        postcodes[testNum].add(zipcode)

#Checks if the current value is a zipcode.
def is_zipcode(elem):
    return (elem.attrib['k'] == "addr:postcode")

#Audits a zipcode by using several methods
def audit(osmfile):
    osm_file = open(osmfile, "r")
    postcodes = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_zipcode(tag):
                    audit_zipcode(postcodes, tag.attrib['v'])
    return postcodes

#Updates a zipcode by using the mappings provided above
def update_name(zipcode):
    testNum = re.findall('[a-zA-Z]*', zipcode)
    if testNum:
        testNum = testNum[0]
    testNum.strip()
    if testNum == "CA":
        convertedZipcode = (re.findall(r'\d+', zipcode))
        if convertedZipcode:
            if convertedZipcode.__len__() == 2:
                return (re.findall(r'\d+', zipcode))[0] + "-" +(re.findall(r'\d+', zipcode))[1]
            else:
                return (re.findall(r'\d+', zipcode))[0]

#Uses other methods to check if a value is a valid zipcode and clean it.
def test():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name)
            print name, "=>", better_name


if __name__ == '__main__':
    test()