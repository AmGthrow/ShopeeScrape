import unittest
from scrapers import shops


class TestQueries(unittest.TestCase):
    def testEncodeKwargs(self):
        test_result = shops.AbstractAPI.URLEncodeQuery(name="redmi note 10")
        self.assertEqual(
            test_result,
            {"name": "redmi%20note%2010"},
        )
