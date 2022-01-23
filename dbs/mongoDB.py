from pymongo import MongoClient, database as db_type


class DataBase:
    def __init__(self, database: db_type.Database) -> None:
        self.DATABASE = database
        pass

    def find(self, collection, query={}):
        return self.DATABASE.get_collection(collection).find(query)

    def find_one(self, collection, query={}):
        return self.DATABASE.get_collection(collection).find_one(query)

    def update_one(self, collection, find, query={}, upsert=False):
        return self.DATABASE.get_collection(collection).update_one(
                find,
                {
                    '$set': query,
                    '$currentDate': {
                        'lastModified': True
                    }
                },
                upsert=upsert)

    def update_many(self, collection, docs):
        return self.DATABASE.get_collection(collection).insert_many(docs)


class MongoDB(object):
    """
    Object with mongo db instances
    """
    DBS = dict()

    @staticmethod
    def initialize(uri, db):
        client = MongoClient(uri)
        MongoDB.DBS[db] = DataBase(client[db])

    @staticmethod
    def get_db(db) -> DataBase:
        try:
            return MongoDB.DBS[db]
        except:
            return None
