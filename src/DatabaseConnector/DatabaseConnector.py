import pymongo


class DatabaseConnector:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, database_name: str):
        self.db_client = pymongo.MongoClient()
        self.mydb = self.db_client[database_name]


class CollectionConnector:
    def __init__(self, database_name, collection_name: str):
        self.db_connector = DatabaseConnector(database_name)
        self.collection = self.db_connector.mydb[collection_name]


if __name__ == '__main__':
    c = CollectionConnector('testDB', 'collection1')
    c2 = CollectionConnector('testDB', 'collection2')

    print(c.collection)
    print(c2.collection)
    print(c is c2)

    c.collection.insert_one({'test': 1})
    c2.collection.insert_one({'test': 1})

    print(c.db_connector.mydb)
    print(c2.db_connector.mydb)
