#Improves the city names by auditing and cleaning data using code given below.
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import string

#OSM file to read data from.
OSMFILE = "san-jose_california.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

#List of expected city names
validCities = ["Santa Clara","Sunnyvale","Cupertino","San Jose","Palo Alto",
               "Milpitas","Mountain View","Morgan Hill","Los Gatos","Campbell",
               "Monte Sereno","Los Altos","Saratoga", "Gilroy","Lexington",]

#Audits a city name by comparing with the list of expected names.
# If it contains words that unexpected, it adds the unexpected name to a list
# and returns the list.
def audit_city(cities, aCity):
    aCity= aCity.title()
    if "," in aCity:
        aCity = aCity[:string.find(aCity,",")]
        aCity = aCity.strip()
    if not (aCity in validCities):
        cities[aCity].add(aCity)

#Checks if the current value is a city
def is_city(elem):
    return (elem.attrib['k'] == "addr:city")

#Audits a city name by using several methods
def audit(osmfile):
    osm_file = open(osmfile, "r")
    cities = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_city(tag):
                    audit_city(cities, tag.attrib['v'])
    return cities

#If a city is not expected, checks if city is wrongly spelled and
# finds the right spelling.
def similarWords(name):
    highestSimRatio = 0
    bestSimilarityCity = None
    for city in validCities:
        lengthOfCity1 = len(city)
        lengthOfCity2 = len(name)
        length = 0
        if lengthOfCity1<lengthOfCity2:
            length = lengthOfCity1
            other = lengthOfCity2
        else:
            length = lengthOfCity2
            other = lengthOfCity1
        similarChar = 0
        for a in range(0,length):
            if(city[a] == name[a]):
                similarChar = similarChar + 1
        similarityRatio = similarChar/(other *(1.0))
        if(similarityRatio>highestSimRatio):
            highestSimRatio = similarityRatio
            bestSimilarityCity = city
    print highestSimRatio
    if highestSimRatio>0.75:
        return bestSimilarityCity

#Updates a city name by using the mappings provided above
def update_name(name):
    name = name.title()
    if "," in name:
        name = name[:string.find(name,",")]
        name = name.strip()
    someCity = similarWords(name)
    if someCity != None:
        return someCity

#Uses other methods to check if a value is a valid city name and clean it.
def test():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name)
            print name, "=>", better_name

if __name__ == '__main__':
    test()