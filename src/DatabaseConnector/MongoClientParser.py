from __future__ import annotations

import logging
from src.DatabaseConnector.MongoClient import MongoClient
from typing import TypeVar


T = TypeVar('T')
logger = logging.getLogger(__name__)


def get_class_instance_by_name(key: str, *classes_to_parse: dict):
    for _class in classes_to_parse:
        if key in _class.keys():
            return _class[key].__new__(_class[key])
    return None


class MongoClientParser(MongoClient):
    def __init__(self, database_name: str, collection_name: str):
        MongoClient.__init__(self, database_name, collection_name)

    # region insert
    def parse_insert_one(self, obj: object) -> None:
        json = self._parse_object_to_dict(obj)
        logger.debug(json)
        self.collection.insert_one(json)

    # def insert_many(self, obj: object) -> None:
    #     self.collection.insert_many()
    #     self.insert_many(self._parse_object_to_dict(obj))
    # endregion

    # region find
    def parse_find(self, top_level_class: T, filter: dict = None, *sub_classes: dict) -> list[T]:
        result = self.collection.find(filter)
        logger.debug(f'got result from database {result} and start parsing')
        return [self._parse_result_to_object(x, top_level_class, *sub_classes) for x in result]

    def parse_find_one(self, top_level_class: T, filter: dict = None, *sub_classes: dict) -> T:
        result = self.collection.find_one(filter)
        logger.debug(f'got result from database {result} and start parsing')
        return self._parse_result_to_object(result, top_level_class, *sub_classes)
    # endregion

    # region find
    def parse_update(self, filter: dict, class_as_obj: T) -> None:
        logger.debug(f'update {class_as_obj} from database with filter {filter}')
        self.collection.update_one(filter, {"$set": self._parse_object_to_dict(class_as_obj)})

    def parse_update_one(self, filter: dict, *top_level_class: T) -> None:
        [self.parse_update(filter, x) for x in top_level_class]
    # endregion

    # region parser
    def _parse_result_to_object(self, result, top_level_class: T, *sub_classes: dict) -> T:
        if not result:
            return None

        if isinstance(result, list):
            self._parse_list_to_object(result, *sub_classes)
            return result

        elif isinstance(result, dict):
            for key, value in result.items():
                if isinstance(value, dict):
                    sub_obj_class = get_class_instance_by_name(key, *sub_classes)
                    if sub_obj_class:
                        sub_obj = self._parse_result_to_object(value, sub_obj_class, *sub_classes)
                        setattr(top_level_class, key, sub_obj)

                if isinstance(value, list):
                    new_list = self._parse_result_to_object(value, top_level_class, *sub_classes)
                    setattr(top_level_class, key, new_list)

                else:
                    if not isinstance(value, dict):
                        setattr(top_level_class, key, value)

        return top_level_class

    def _parse_list_to_object(self, list_in: list, *sub_classes):
        for index, item in enumerate(list_in):
            if isinstance(item, list):
                self._parse_list_to_object(item, *sub_classes)

            elif isinstance(item, dict):
                sub_obj_class = get_class_instance_by_name(next(iter(item)), *sub_classes)
                if sub_obj_class:
                    list_in[index] = self._parse_result_to_object(item, sub_obj_class, *sub_classes)

    def _parse_object_to_dict(self, obj) -> list | dict:
        if isinstance(obj, (list, tuple)):
            return self._parse_list_to_dict(obj)
        if isinstance(obj, dict):
            return {key: self._parse_object_to_dict(value) for key, value in obj.items()}
        elif hasattr(obj, "__dict__"):
            return self._parse_object_to_dict(obj.__dict__())
        else:
            return obj

    def _parse_list_to_dict(self, list_in: list):
        list_out = []
        for element in list_in:
            if isinstance(element, list):
                if hasattr(element[0], "__dict__"):
                    list_out.append({element[0].__class__.__name__: self._parse_list_to_dict(element)})
                else:
                    list_out.append(element)
            else:
                if hasattr(element, "__dict__"):
                    list_out.append({element.__class__.__name__: self._parse_object_to_dict(element)})
                else:
                    list_out.append(element)
        return list_out
    # endregion


if __name__ == '__main__':
    pass
