import unittest
from scrapers import shopee
from data import database
import utils
import requests


class TestAPI(unittest.TestCase):
    def testEncodeKwargs(self):
        test_result = utils.URLEncodeQuery(name="redmi note 10")
        self.assertEqual(
            test_result,
            {"name": "redmi%20note%2010"},
        )

    def testShopeeSearch(self):
        search_result = shopee.search(keyword="redmi note 10")
        self.assertIsNotNone(search_result)
        for item in search_result:
            self.assertIn("itemid", item)
            self.testItemLinks(item)

    def testItemLinks(self, item=None):
        if item is not None:
            link = shopee.get_item_link(item['name'], item['itemid'],
                                        item['shopid'])
            response = requests.get(link)
            self.assertEqual(response.status_code, 200)


class TestDB(unittest.TestCase):
    def setUp(self):
        self.db = database.ShopeeDatabase()
        self.db.create_tables()

    def test_store_from_search(self):
        # TODO: test this with an actual item's known data and verify db contents 
        self.db.add_items(shopee.search(keyword="redmi note 10"))
        print(self.db.query("SELECT * FROM ShopeeProducts").fetchone())