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


if __name__ == '__main__':
    d = DatabaseConnector('test', 'test')
    d.collection.insert_one({'15': ((15, 15))})
