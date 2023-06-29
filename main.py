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
        self.logger.setLevel(logging.INFO)

        self.logger.addHandler(_build_log_handler())

        self.db_client = pymongo.MongoClient()
        self.mydb = self.db_client['TestDatabase']
        self.db_table = self.mydb['TestTable']
        self.classes = classes

    def insert(self, _in: object):
        self.db_table.insert_one(p.__dict__)

    # region find
    def _find(self):
        rows = []
        for _row in self.db_table.find():
            rows.append(_row)
        return rows

    @overload
    def find(self) -> dict:
        pass

    @overload
    def find(self, top_level_class, *classes_to_parse: object) -> object:
        pass

    def find(self, top_level_class: object = None, *sub_level_class: object):
        result = self._find()
        self.logger.info(f'get result from database {result}')
        if top_level_class is None:
            return result
        return self._parse_result_to_object(result, top_level_class, sub_level_class)

    def _find_one(self):
        return self.db_table.find_one()

    @overload
    def find_one(self) -> dict:
        pass

    @overload
    def find_one(self, top_level_class, *classes_to_parse: object) -> object:
        pass

    def find_one(self, top_level_class: object = None, *sub_level_class: object):
        result = self._find_one()
        self.logger.info(f'get result from database {result}')
        if top_level_class is None:
            return result
        return self._parse_result_to_object(result, top_level_class, sub_level_class)
    # endregion

    def _parse_result_to_object(self, result, top_level_class, *sub_level_class) -> object:
        if not result:
            return None

        obj = top_level_class()
        for key, value in result.items():
            if isinstance(value, dict):
                sub_obj_class = get_class_by_name(key, top_level_class, sub_level_class)
                if sub_obj_class:
                    sub_obj = self._parse_result_to_object(value, sub_obj_class)
                    setattr(obj, key, sub_obj)
            else:
                setattr(obj, key, value)

        return obj


class Person:
    def __init__(self):
        self.age = 5
        self.height = 15
        self.test = Test().__dict__


class Test:
    def __init__(self):
        self.age = 45498
        self.height = 45498


if __name__ == '__main__':
    d = DatabaseConnector(Person)
    p = Person()

    r = d.find()
    d.find()
    print(r)
