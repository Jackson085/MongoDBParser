import unittest
from src.DatabaseConnector.DatabaseConnector import DatabaseConnector


class ConnectorTest(unittest.TestCase):
    def test_create_instance(self):
        ins = DatabaseConnector('DatabaseTest', 'CollectionTest')

        self.assertIsInstance(ins, DatabaseConnector)

    def test_same_instance(self):
        ins1 = DatabaseConnector('DatabaseTest', 'CollectionTest')
        ins2 = DatabaseConnector('DatabaseTest', 'CollectionTest')

        self.assertEqual(ins1, ins2)

    def test_different_instance(self):
        ins1 = DatabaseConnector('DatabaseTest', 'CollectionTest1')
        ins2 = DatabaseConnector('DatabaseTest1', 'CollectionTest')

        self.assertNotEqual(ins1, ins2)

    def test_different_instance_same_database(self):
        ins1 = DatabaseConnector('DatabaseTest', 'CollectionTest')
        ins2 = DatabaseConnector('DatabaseTest', 'CollectionTest1')

        self.assertNotEqual(ins1, ins2)

    def test_different_instance_same_collection(self):
        ins1 = DatabaseConnector('DatabaseTest', 'CollectionTest')
        ins2 = DatabaseConnector('DatabaseTest1', 'CollectionTest')

        self.assertNotEqual(ins1, ins2)

    def test_multiple_different_instances(self):
        ins1 = DatabaseConnector('DatabaseTest', 'CollectionTest')
        ins2 = DatabaseConnector('DatabaseTest1', 'CollectionTest')
        ins3 = DatabaseConnector('DatabaseTest1', 'CollectionTest1')

        self.assertNotEqual(ins1, ins2)
        self.assertNotEqual(ins1, ins3)
        self.assertNotEqual(ins2, ins3)

    def test_multiple_same_instances(self):
        ins1 = DatabaseConnector('DatabaseTest', 'CollectionTest')
        ins2 = DatabaseConnector('DatabaseTest', 'CollectionTest')
        ins3 = DatabaseConnector('DatabaseTest1', 'CollectionTest1')
        ins4 = DatabaseConnector('DatabaseTest1', 'CollectionTest2')

        self.assertEqual(ins1, ins2)
        self.assertNotEqual(ins1, ins3)
        self.assertNotEqual(ins1, ins4)


if __name__ == '__main__':
    unittest.main()
