import unittest

from ConnectorTest import ConnectorTest
from MongoClientParserTest import MongoClientParserTest
from MongoClientTest import MongoClientTest


if __name__ == '__main__':
    test_suite = unittest.TestSuite()

    test_suite.addTest(unittest.makeSuite(ConnectorTest))
    test_suite.addTest(unittest.makeSuite(MongoClientParserTest))
    test_suite.addTest(unittest.makeSuite(MongoClientTest))

    unittest.TextTestRunner().run(test_suite)
