from __future__ import annotations
import logging
from DatabaseConnector.MongoClient import MongoClient
from typing import TypeVar


T = TypeVar('T')


def get_class_instance_by_name(key: str, *classes_to_parse: dict):
    for _class in classes_to_parse:
        if key in _class.keys():
            return _class[key].__new__(_class[key])
    return None


class MongoClientParser(MongoClient):
    def __init__(self, database_name: str, collection_name: str, log_level: int = logging.DEBUG):
        MongoClient.__init__(self, database_name, collection_name, log_level)

    # region insert
    def parse_insert_one(self, obj: object) -> None:
        self.insert_one(self._parse_object_to_dict(obj))

    def insert_many(self, obj: object) -> None:
        self.insert_many(self._parse_object_to_dict(obj))
    # endregion

    # region find
    def parse_find(self, top_level_class: T, filter: dict = None, *sub_classes: dict) -> list[T]:
        result = self.find(filter)
        self.logger.debug(f'got result from database {result} and start parsing')
        return [self._parse_result_to_object(x, top_level_class, *sub_classes) for x in result]

    def parse_find_one(self, top_level_class: T, filter: dict = None, *sub_classes: dict) -> T:
        result = self.find_one(filter)
        self.logger.debug(f'got result from database {result} and start parsing')
        return self._parse_result_to_object(result, top_level_class, *sub_classes)
    # endregion

    # region find
    def parse_update(self, filter: dict, class_as_obj: T) -> None:
        self.logger.debug(f'update {class_as_obj} from database with filter {filter}')
        self.update_one(filter, {"$set": self._parse_object_to_dict(class_as_obj)})

    def parse_update_one(self, filter: dict, *top_level_class: T) -> None:
        [self.parse_update(filter, x) for x in top_level_class]
    # endregion

    # region parser
    def _parse_result_to_object(self, result, top_level_class: T, *sub_classes: dict) -> T:
        if not result:
            return None

        for key, value in result.items():
            if isinstance(value, dict):
                sub_obj_class = get_class_instance_by_name(key, *sub_classes)
                if sub_obj_class:
                    sub_obj = self._parse_result_to_object(value, sub_obj_class, *sub_classes)
                    setattr(top_level_class, key, sub_obj)
            else:
                setattr(top_level_class, key, value)
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
            return [self._parse_object_to_dict(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: self._parse_object_to_dict(value) for key, value in obj.items()}
        elif hasattr(obj, "__dict__"):
            return self._parse_object_to_dict(obj.__dict__())
        else:
            return obj
    # endregion


if __name__ == '__main__':

    class Test:
        def __init__(self):
            self.type = None
            self.name = None

        def __dict__(self):
            return {'type': self.type, 'name': self.name}


    class Human:
        def __init__(self):
            self.age = 42
            self.name = "name"
            self.pet = Test()
            self.private_attribute = "foo"

        def __dict__(self):
            return {'age': self.age, 'name': self.name, 'pet': self.pet}

    h = Human()
    client = MongoClientParser('database_name', 'collection_name')
    # client.parse_insert_one(h)  # convert attributes from __dict__ to dict and saves them in the database

    obj = client.parse_find_one(Human(), {'name': 'name'}, {'pet': Test})  # obj is instance from Human and not a dict
    print(obj.pet.name)
    o = 0

    # get_class_instance_by_name('pet', {'pet': Test}, {'human': Human})
