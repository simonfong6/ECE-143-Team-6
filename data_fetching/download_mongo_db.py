#!/usr/bin/env python3

from pymongo import MongoClient
from json import dump, JSONEncoder
from bson import ObjectId


USER = ''
PASSWORD = ''
MONGO_DATABASE = 'mongodb://{}:{}@ds137749.mlab.com:37749/sadscore'.format(USER, PASSWORD)
DATA_FILE = 'sadscore_data.json'


class MyJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return JSONEncoder.default(self, o)

def connect_db():
    """Connects to the signinucsd database on mlab servers."""
    client = MongoClient(MONGO_DATABASE)
    return client


def grab_data():
    client = connect_db()
    db = client.sadscore
    collection = db.responses_men
    cursor = collection.find({})
    count = 0

    documents = []
    with open(DATA_FILE, 'w+') as data_file:
        for document in cursor:
            documents.append(document)
            count += 1
        dump(documents, data_file, cls=MyJSONEncoder, indent=4, sort_keys=True)

        print("Wrote {} documents".format(count))
    client.close()

def main():
    grab_data()


if __name__ == "__main__":
    main()