import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json

"""
Function wrangles the data and transforms the shape of the data
into the following model: 
{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}


Function returns a list of dictionaries of above format.
"""

TEST_FILE = "example.osm"
FILE = "map.osm"

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
addresschars = re.compile(r'addr:(\w+)')
CREATED = { "version", "changeset", "timestamp", "user", "uid"}


def shape_element(element):
    # process only 2 types of top level tags: "node" and "way"
    if element.tag == "node" or element.tag == "way" :
        # create initial dictionary
        node = {'created':{}, 'type':element.tag}    
        for k in element.attrib:
            try:
                v = element.attrib[k]
            except KeyError:
                continue
            if k == 'lat' or k == 'lon':
                continue
            if k in CREATED:  
                node['created'][k] = v
            else:
                node[k] = v

        # add attributes for latitude and longitude to a "pos" array as float values
        try:
            node['pos'] = [float(element.attrib['lat']), float(element.attrib['lon'])]
        except KeyError:
            pass

        if 'address' not in node.keys():
            node['address'] = {}
            for i in element.iter('tag'):
                k = i.attrib["k"]
                v = i.attrib["v"]
                
                # check of second level tag "k" value for containing problematic characters
                if problemchars.search(k):
                    continue
                
                # check if second level tag "k" value starts with "addr:", if yes, it is added to a dictionary "address"
                elif k.startswith('addr:'):
                    if len(k.split(':')) == 2:
                        content = addresschars.search(k)
                        if content:
                            node['address'][content.group(1)] = v
                            
                # if second level tag "k" value does not start with "addr:", but contains ":",
                # it is processed in same as any other tags
                else:
                    node[k]=v

        # ignore tag if there is a second ":" that separates the type/direction of a street             
        if not node['address']:
            node.pop('address',None)
        # when the tag == way,  scrap all the nd key
        if element.tag == "way":
            node['node_refs'] = []
            for nd in element.iter('nd'):
                node['node_refs'].append(nd.attrib['ref'])
        
        return node
    else:
        return None




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

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
       
    
    data = process_map(FILE, pretty=False)
    return data
    
    
    
test()

