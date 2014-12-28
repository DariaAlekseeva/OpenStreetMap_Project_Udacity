import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint


"""
The function takes a string with street name as an argument and returns the fixed name.
"""

TEST_FILE = "example.osm"
FILE = "map.osm"

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_types = defaultdict(set)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "STREET" : "Street",
            "Rd.": "Road",
            "Rd" : "Road",
            "ROAD" : "Road",
            "ROAD," : "Road",
            "road" : "Road",
            "Ave": "Avenue",
            "ground" : "Ground",
            "lane" : "Lane",
            "market" : "Market",
            "passage" : "Passage",
            "row" : "Row",
            "st" : "Street",
            "street" : "Street",
            "wharf" : "Wharf",
            "turnstile" : "Turnstile"}


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
    


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):


        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    
    return street_types


def update_name(name, mapping):
    print name
    map_dic = mapping.keys()
    for key in map_dic:
        match = re.search(key,name)
        if match:
            name = re.sub(key + "$", mapping[key], name)
    return name




def test():
    st_types = audit(FILE)
    pprint.pprint(dict(st_types))
    
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
 

print test()
