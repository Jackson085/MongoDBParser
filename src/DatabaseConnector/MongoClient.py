import logging
from DatabaseConnector.DatabaseConnector import DatabaseConnector


logger = logging.getLogger(__name__)


class MongoClient:
    def __init__(self, database_name: str, collection_name: str):
        self.collection = DatabaseConnector(database_name, collection_name).collection

    # region insert
    def insert_one(self, obj: dict) -> None:
        logger.debug(f"insert {obj} into {self.collection}")
        self.collection.insert_one(obj)

    def insert_many(self, obj: object) -> None:
        logger.debug(f"insert many {obj} into {self.collection}")
        self.collection.insert_many(obj)
    # endregion

    # region find
    def find(self, filter: dict = None) -> list:
        filter = {} if filter is None else filter
        logger.debug(f"start searching in {self.collection} with filter: {filter}")
        return [_row for _row in self.collection.find(filter)]

    def find_one(self, filter: dict = None) -> dict:
        filter = {} if filter is None else filter
        logger.debug(f"start searching in {self.collection} with filter: {filter}")
        return self.collection.find_one(filter)
    # endregion

    # region find
    def update_many(self, filter: dict, update: dict) -> None:
        filter = {} if filter is None else filter
        logger.debug(f"start updating many in {self.collection} with filter: {filter}, update: {update}")
        self.collection.update_many(filter, update)

    def update_one(self, filter: dict, update: dict) -> None:
        filter = {} if filter is None else filter
        logger.debug(f"start updating in {self.collection} with filter: {filter}, update: {update}")
        self.collection.update_one(filter, update)
    # endregion
