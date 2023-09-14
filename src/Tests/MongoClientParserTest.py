import unittest
from DatabaseConnector.MongoClientParser import MongoClientParser
# from TestClasses.SimpleClass import SimpleClass, ClassWithSubclass, ClassWithTwoSubclasses, ClassWithList
from TestClasses.SimpleClass import *


class MongoClientParserTest(unittest.TestCase):
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
        ins = MongoClientParser('DatabaseTest', 'CollectionTest1')
        cls = SimpleClass()

        self.assertEqual(cls.__dict__(), ins._parse_object_to_dict(cls))

    def test_object_with_subclass_to_dict(self):
        ins = MongoClientParser('DatabaseTest', 'CollectionTest1')
        cls = ClassWithSubclass()

        self.assertEqual({'normal_var': 1, 'sub_class': {'var1': 1, 'var2': 2}}, ins._parse_object_to_dict(cls))

    def test_object_with_two_subclass_to_dict(self):
        ins = MongoClientParser('DatabaseTest', 'CollectionTest1')
        cls = ClassWithTwoSubclasses()

        self.assertEqual({'child_class': {'normal_var': 1, 'sub_class': {'var1': 1, 'var2': 2}}, 'parent_var': 1},
                         ins._parse_object_to_dict(cls))

    def test_object_with_list_to_dict(self):
        ins = MongoClientParser('DatabaseTest', 'CollectionTest1')
        cls = ClassWith2DList()

        self.assertEqual({'my_list': [15, [42, 42, 42], 15], 'parent_var': 1}, ins._parse_object_to_dict(cls))

    def test_object_with_list_of_object_to_dict(self):
        ins = MongoClientParser('DatabaseTest', 'CollectionTest1')
        cls = ClassWithObjectsInList()

        self.assertEqual({'my_list': [{'SimpleClass': {'var1': 1, 'var2': 2}}, {'SimpleClass': {'var1': 1, 'var2': 2}}], 'parent_var': 1}, ins._parse_object_to_dict(cls))

    def test_object_with_2dlist_of_object_to_dict(self):
        ins = MongoClientParser('DatabaseTest', 'CollectionTest1')
        cls = ClassWithObjectsIn2DList()

        self.assertEqual({'my_list': [{'SimpleClass': {'var1': 1, 'var2': 2}},
            {'SimpleClass': [{'SimpleClass': {'var1': 1, 'var2': 2}}}]], 'parent_var': 1},  ins._parse_object_to_dict(cls))


if __name__ == '__main__':
    unittest.main()
