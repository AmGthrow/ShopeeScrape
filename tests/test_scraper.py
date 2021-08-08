import unittest
from scraper import products


class TestQueries(unittest.TestCase):
    def testEncodeKwargs(self):
        test_result = products.AbstractAPI.URLEncodeQuery(name="redmi note 10")
        self.assertEqual(
            test_result,
            {"name": "redmi%20note%2010"},
        )
