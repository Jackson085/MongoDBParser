import unittest
from src.DatabaseConnector.MongoClient import MongoClient


class MongoClientTest(unittest.TestCase):
    def test_client_instances(self):
        ins1 = MongoClient('DatabaseTest', 'CollectionTest1').collection
        ins2 = MongoClient('DatabaseTest', 'CollectionTest2').collection
        ins3 = MongoClient('DatabaseTest', 'CollectionTest2').collection
        ins4 = MongoClient('DatabaseTest1', 'CollectionTest').collection

        self.assertEqual(ins2, ins3)
        self.assertNotEqual(ins1, ins2)
        self.assertNotEqual(ins1, ins3)
        self.assertNotEqual(ins1, ins4)
        self.assertNotEqual(ins3, ins4)

    # no more test (for now) because MongoClient has same functions as pymongo.MongoClient


if __name__ == '__main__':
    unittest.main()
