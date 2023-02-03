import pymongo


class Database:
    def __init__(self, clientString: str, databaseName: str):
        self.client = pymongo.MongoClient(clientString)
        self.database = self.client[databaseName]

    def query_one(self, collectionName: str, obj: object):
        collection = self.database[collectionName]
        result = collection.find(obj)
        return list(result)
