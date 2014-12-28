import xml.etree.ElementTree as ET
import pprint

"""
Function finds how many unique users have contributed to the map in the area
Function return a set of unique user IDs ("uid")
"""

TEST_FILE = "example.osm"
FILE = "map.osm"

def get_user(element):
    return


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        try:
            users.add(element.attrib['uid'])
        except KeyError:
            continue
    return users



def test():

    users = process_map(FILE)
    pprint.pprint(users)
    

print test()