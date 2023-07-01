import logging
import pymongo
from typing import overload


def get_class_by_name(class_name, *classes_to_parse):
    for obj_class in classes_to_parse:
        if isinstance(obj_class, type) and obj_class.__name__.lower() == class_name.lower():
            return obj_class
    return None


def _build_log_handler():
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - [%(module)s]')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    return handler


class DatabaseConnector:
    def __init__(self, *classes):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.FATAL)

        self.logger.addHandler(_build_log_handler())

        self.db_client = pymongo.MongoClient()
        self.mydb = self.db_client['TestDatabase']
        self.db_table = self.mydb['TestTable']
        self.classes = classes

    def _insert_one(self, obj: object):
        obj = self._parse_object_to_dict(obj)
        self.db_table.insert_one(obj)

    def insert_one(self, obj: object):
        self._insert_one(obj)

    def _insert_many(self, obj: object):
        NotImplementedError()

    def insert_many(self, obj: object):
        self._insert_many(obj)
    # endregion

    # region find
    def _find(self) -> list:
        rows = []
        for _row in self.db_table.find():
            rows.append(_row)
        return rows

    @overload
    def find(self) -> list:
        pass

    @overload
    def find(self, top_level_class, *classes_to_parse: object) -> list:
        pass

    def find(self, top_level_class: object = None, *sub_level_class: object) -> list:
        result = self._find()
        self.logger.info(f'get result from database {result}')
        if top_level_class is None:
            return result
        return [self._parse_result_to_object(x, top_level_class, sub_level_class) for x in result]

    def _find_one(self, filter: dict = None):
        filter = {} if filter is None else filter
        return self.db_table.find_one(filter)

    @overload
    def find_one(self, filter: dict = None) -> dict:
        pass

    @overload
    def find_one(self, top_level_class, *classes_to_parse: object) -> object:
        pass

    def find_one(self, filter: dict = None, top_level_class: object = None, *sub_level_class: object):
        result = self._find_one(filter)
        self.logger.info(f'get result from database {result}')
        if top_level_class is None:
            return result
        return self._parse_result_to_object(result, top_level_class, sub_level_class)
    # endregion

    # region parser
    def _parse_result_to_object(self, result, top_level_class, *sub_level_class) -> object:
        if not result:
            return None

        obj = top_level_class()
        for key, value in result.items():
            if isinstance(value, dict):
                sub_obj_class = get_class_by_name(key, top_level_class, *sub_level_class)
                if sub_obj_class:
                    sub_obj = self._parse_result_to_object(value, sub_obj_class, *sub_level_class)
                    setattr(obj, key, sub_obj)
            else:
                setattr(obj, key, value)

        return obj

    def _parse_object_to_dict(self, obj):
        if isinstance(obj, (list, tuple)):
            return [self._parse_object_to_dict(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: self._parse_object_to_dict(value) for key, value in obj.items()}
        elif hasattr(obj, "__dict__"):
            return self._parse_object_to_dict(obj.__dict__())
        else:
            return obj
    # endregion


class Person:
    def __init__(self):
        self.age = 5
        self.height = 15
        self.asd = 1599

    def __dict__(self):
        return {'age': self.age, 'height': self.height}


class Test:
    def __init__(self):
        self.age = 45498
        self.height = 45498

    def __dict__(self):
        return {'age': self.age+99999999}


if __name__ == '__main__':
    p = Person()
    d = DatabaseConnector(Person)
    d._parse_object_to_dict(p)
