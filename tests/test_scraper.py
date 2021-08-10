import unittest
from scrapers import shops


class TestAPI(unittest.TestCase):
    def testEncodeKwargs(self):
        test_result = shops.AbstractAPI.URLEncodeQuery(name="redmi note 10")
        self.assertEqual(
            test_result,
            {"name": "redmi%20note%2010"},
        )

    def testShopeeSearch(self):
        search_result = shops.search_shopee(keyword="redmi note 10")
        self.assertIsNotNone(search_result)
        for item in search_result:
            self.assertIn("itemid", item)
