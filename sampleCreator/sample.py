#Creates a sample of a dataset. 
try:
    import lxml.etree as ET
except ImportError:
    import xml.etree.cElementTree as ET

#This method reads a file (having a dataset) using iterative parsing and creates a sample dataset for it.
def sample_data(datafile):
    destfile = 'sample.osm'
    subtree = ET.Element('osm')
    node_els_to_add = 10000
    node_els_added = 0
    with open(datafile, "r") as osm_file:
        elements_added = 0
        for event, elem in ET.iterparse(osm_file, events=(
                'start', 'end')):
            if elem.tag == 'osm':
                print ET.tostring(elem)
            if event == 'end' and elem.tag != 'osm':
                if elem.tag == "node" and elem.tag != 'osm' and node_els_added < node_els_to_add:
                    print ET.tostring(elem)
                    subtree.append(ET.fromstring(ET.tostring(elem)))
                    node_els_added += 1
                elem.clear()
        ET.ElementTree(subtree).write(destfile)

if __name__ == '__main__':
        sample_data('san-jose_california.osm')