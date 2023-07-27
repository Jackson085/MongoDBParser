import logging
from DatabaseConnector import CollectionConnector


logger = logging.getLogger(__name__)


class MongoClient:
    def __init__(self, database_name: str, collection_name: str):
        self.collection = CollectionConnector(database_name, collection_name)

    # region insert
    def insert_one(self, obj: dict) -> None:
        logger.debug(f"insert {obj} into {self.collection}")
        self.collection.collection.insert_one(obj)

    def insert_many(self, obj: object) -> None:
        logger.debug(f"insert many {obj} into {self.collection}")
        self.collection.collection.insert_many(obj)
    # endregion

    # region find
    def find(self, filter: dict = None) -> list:
        filter = {} if filter is None else filter
        logger.debug(f"start searching in {self.collection} with filter: {filter}")
        return [_row for _row in self.collection.collection.find(filter)]

    def find_one(self, filter: dict = None) -> dict:
        filter = {} if filter is None else filter
        logger.debug(f"start searching in {self.collection} with filter: {filter}")
        return self.collection.collection.find_one(filter)
    # endregion

    # region find
    def update(self, filter: dict, update: dict) -> None:
        filter = {} if filter is None else filter
        logger.debug(f"start updating many in {self.collection} with filter: {filter}, update: {update}")
        self.collection.collection.update_many(filter, update)

    def update_one(self, filter: dict, update: dict) -> None:
        filter = {} if filter is None else filter
        logger.debug(f"start updating in {self.collection} with filter: {filter}, update: {update}")
        self.collection.collection.update_one(filter, update)
    # endregion
