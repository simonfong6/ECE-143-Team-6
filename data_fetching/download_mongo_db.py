#!/usr/bin/env python3
"""
Downloads the all the survey responses from the database.
"""
from pymongo import MongoClient
from json import dump, JSONEncoder
from bson import ObjectId

# Database credentials.
USER = ''
PASSWORD = ''
MONGO_DATABASE = 'mongodb://{}:{}@ds137749.mlab.com:37749/sadscore'.format(USER, PASSWORD)
DATA_FILE = 'sadscore_data.json'


class MyJSONEncoder(JSONEncoder):
    """
    Helps encode the ObjectId of MongoDB document objects.
    """
    def default(self, o):
        """
        Encodes the object to a JSONable string.

        Args:
            o (object): Object to encode.
        
        Returns:
            str: Object as JSON encoded string.
        """
        # When we see an ObjectId, we can't use the default encoder.
        if isinstance(o, ObjectId):
            return str(o)

        # All other cases, use the default encoder.
        return JSONEncoder.default(self, o)

def connect_db():
    """Connects to the signinucsd database on mlab servers."""
    client = MongoClient(MONGO_DATABASE)
    return client


def grab_data():
    """
    Fetches the reponses from the database and saves it into a JSON file.
    """

    # Connect to database and get all documents from the collection.
    client = connect_db()
    db = client.sadscore
    collection = db.responses_men
    cursor = collection.find({})
    count = 0

    # Save the documents as a JSON file.
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