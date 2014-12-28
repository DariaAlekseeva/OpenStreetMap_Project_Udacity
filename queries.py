
def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def make_pipeline():

# find names of articles in wikipedia for cinemas
    pipeline = [
            {'$match': {'amenity':'cinema',
                        'wikipedia':{'$exists':1}}},
            {'$project':{'_id': '$name',
                         'wikipedia':'$wikipedia'}},
            {'$limit':3}
]

    return pipeline

def aggregate(db, pipeline):
    result = db.londoneast.aggregate(pipeline)
    return result


db = get_db('examples')
pipeline = make_pipeline()
result = aggregate(db, pipeline)
import pprint
pprint.pprint(db.londoneast.aggregate(pipeline)['result'])