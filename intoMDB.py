
from data import *

data = process_map("map.osm", pretty=False)

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client.examples
[db.londoneast.insert(e) for e in data]

