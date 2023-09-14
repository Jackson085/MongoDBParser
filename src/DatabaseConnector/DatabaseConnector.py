import pymongo


class DatabaseConnector:
    _instances = {}

    def __new__(cls, database_name: str, collection_name: str, *args, **kwargs):
        if database_name not in cls._instances.keys():
            cls._instances[database_name] = {collection_name: object.__new__(cls)}

        if collection_name not in cls._instances[database_name].keys():
            cls._instances[database_name][collection_name] = object.__new__(cls)

        return cls._instances[database_name][collection_name]

    def __init__(self, database_name: str, collection_name: str):
        self.db_client = pymongo.MongoClient()
        self.mydb = self.db_client[database_name]
        self.collection = self.mydb[collection_name]


# class CollectionConnector:
#     def __init__(self, database_name, collection_name: str):
#         self.db_connector = DatabaseConnector(database_name)
#         self.collection = self.db_connector.mydb[collection_name]


if __name__ == '__main__':
    c = DatabaseConnector('test', 'collection')
    c1 = DatabaseConnector('test2', 'collection2')
    c2 = DatabaseConnector('test2', 'collection2')
    c3 = DatabaseConnector('test2', 'collection')
    print(c is c2)
    print(c is c1)
    print(c1 is c2)
    print(c is c3)
    # c = CollectionConnector('testDB', 'collection1')
    # c2 = CollectionConnector('testDB', 'collection1')
    #
    # print(c.collection)
    # print(c2.collection)
    # print(c is c2)
    #
    # c.collection.insert_one({'test': 1})
    # c2.collection.insert_one({'test': 1})
    #
    # print(c.db_connector.mydb)
    # print(c2.db_connector.mydb)
