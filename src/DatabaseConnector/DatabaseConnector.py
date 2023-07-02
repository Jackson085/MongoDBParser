import pymongo


class DatabaseConnector:
    def __init__(self, database_name: str, collection_name: str):
        self.db_client = pymongo.MongoClient()
        self.mydb = self.db_client[database_name]
        self.collection = self.mydb[collection_name]
