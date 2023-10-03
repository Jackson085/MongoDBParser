import unittest
from src.DatabaseConnector.MongoClientParser import MongoClientParser
# from TestClasses.SimpleClass import SimpleClass, ClassWithSubclass, ClassWithTwoSubclasses, ClassWithList
from TestClasses.SimpleClass import *


class MongoClientParserTest(unittest.TestCase):
    ins = MongoClientParser('DatabaseTest', 'CollectionTest1')

    def test_client_instances(self):
        ins1 = MongoClientParser('DatabaseTest', 'CollectionTest1').collection
        ins2 = MongoClientParser('DatabaseTest', 'CollectionTest2').collection
        ins3 = MongoClientParser('DatabaseTest', 'CollectionTest2').collection
        ins4 = MongoClientParser('DatabaseTest1', 'CollectionTest').collection

        self.assertEqual(ins2, ins3)
        self.assertNotEqual(ins1, ins2)
        self.assertNotEqual(ins1, ins3)
        self.assertNotEqual(ins1, ins4)
        self.assertNotEqual(ins3, ins4)

    def test_object_to_dict(self):
        cls = SimpleClass()

        self.assertEqual(cls.__dict__(), self.ins._parse_object_to_dict(cls))

    def test_object_with_subclass_to_dict(self):
        cls = ClassWithSubclass()

        self.assertEqual({'normal_var': 1, 'sub_class': {'var1': 1, 'var2': 2}}, self.ins._parse_object_to_dict(cls))

    def test_object_with_two_subclass_to_dict(self):
        cls = ClassWithTwoSubclasses()

        self.assertEqual({'child_class': {'normal_var': 1, 'sub_class': {'var1': 1, 'var2': 2}}, 'parent_var': 1},
                         self.ins._parse_object_to_dict(cls))

    def test_object_with_list_to_dict(self):
        cls = ClassWith2DList()

        self.assertEqual({'my_list': [15, [42, 42, 42], 15], 'parent_var': 1}, self.ins._parse_object_to_dict(cls))

    def test_object_with_list_of_object_to_dict(self):
        cls = ClassWithObjectsInList()

        self.assertEqual({'my_list': [{'SimpleClass': {'var1': 1, 'var2': 2}}, {'SimpleClass': {'var1': 1, 'var2': 2}}], 'parent_var': 1}, self.ins._parse_object_to_dict(cls))

    def test_object_with_2dlist_of_object_to_dict(self):
        cls = ClassWithObjectsIn2DList()

        self.assertEqual({'parent_var': 1, 'my_list': [{'SimpleClass': {'var1': 1, 'var2': 2}}, {'SimpleClass': [{'SimpleClass': {'var1': 1, 'var2': 2}}]}]},  self.ins._parse_object_to_dict(cls))
    # region parse json to class

    def test_json_to_class(self):
        json = {'var1': 1, 'var2': 2}
        loaded_class = self.ins._parse_result_to_object(json, SimpleClass)

        self.assertIsInstance(loaded_class, SimpleClass)
        self.assertEqual(1, loaded_class.var1)
        self.assertEqual(2, loaded_class.var2)
    # endregion


if __name__ == '__main__':
    unittest.main()
