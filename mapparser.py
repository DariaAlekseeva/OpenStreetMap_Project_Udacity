import xml.etree.ElementTree as ET
import pprint

"""
This function uses iterative parsing to process the map file
and find tags and number of times tags appear in the file.
Input is a file from OSM web site.
Function returns a dictionary with the tag name as the key
and number of times this tag appears in the map as value.
"""


TEST_FILE = "example.osm"
FILE = "map.osm" 

def count_tags(filename):
    tags = {}
    for event, elem in ET.iterparse(filename):
        tag = elem.tag
        if tag not in tags.keys():
            tags[tag] = 1
        else:
            tags[tag] += 1
    return tags

#print count_tags(TEST_FILE)





def test():

    tags = count_tags(FILE)
    pprint.pprint(tags)
#     assert tags == {'bounds': 1,
#                      'member': 3,
#                      'nd': 4,
#                      'node': 20,
#                      'osm': 1,
#                      'relation': 1,
#                      'tag': 7,
#                      'way': 1}


print test()