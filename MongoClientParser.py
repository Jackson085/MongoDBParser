from __future__ import annotations
from MongoClient import MongoClient
from typing import TypeVar


T = TypeVar('T')


def get_class_by_name(class_name, *classes_to_parse):
    for obj_class in classes_to_parse:
        if isinstance(obj_class, type) and obj_class.__name__.lower() == class_name.lower():
            return obj_class
    return None


class MongoClientParser(MongoClient):
    def __init__(self, database_name: str, collection_name: str):
        MongoClient.__init__(self, database_name, collection_name)

    # region insert
    def parse_insert_one(self, obj: object) -> None:
        self.insert_one(self._parse_object_to_dict(obj))

    def insert_many(self, obj: object) -> None:
        self.insert_many(self._parse_object_to_dict(obj))
    # endregion

    # region find
    def parse_find(self, top_level_class: T, filter: dict = None, *sub_level_class: object) -> list[T]:
        result = self.find(filter)
        self.logger.debug(f'got result from database {result} and start parsing')
        return [self._parse_result_to_object(x, top_level_class, sub_level_class) for x in result]

    def parse_find_one(self, top_level_class: T, filter: dict = None, *sub_level_class: object) -> T:
        result = self.find_one(filter)
        self.logger.debug(f'got result from database {result} and start parsing')
        # return top_level_class()
        return self._parse_result_to_object(result, top_level_class, sub_level_class)
    # endregion

    # region parser
    def _parse_result_to_object(self, result, top_level_class: T, *sub_level_class) -> T:
        if not result:
            return None

        obj = top_level_class
        for key, value in result.items():
            if isinstance(value, dict):
                sub_obj_class = get_class_by_name(key, top_level_class, *sub_level_class)
                if sub_obj_class:
                    sub_obj = self._parse_result_to_object(value, sub_obj_class, *sub_level_class)
                    setattr(obj, key, sub_obj)
            else:
                setattr(obj, key, value)

        return obj

    def _parse_object_to_dict(self, obj) -> list | dict:
        if isinstance(obj, (list, tuple)):
            return [self._parse_object_to_dict(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: self._parse_object_to_dict(value) for key, value in obj.items()}
        elif hasattr(obj, "__dict__"):
            return self._parse_object_to_dict(obj.__dict__())
        else:
            return obj
    # endregion
