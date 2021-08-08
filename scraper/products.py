import requests
import logging
from urllib.parse import quote

logger = logging.Logger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s')
handler = logging.FileHandler('./logs/searches.log')
handler.setFormatter(formatter)

logger.addHandler(handler)

class AbstractAPI:
    @staticmethod
    def urlEncodeQuery(**kwargs):
        """Encodes values to URL-friendly strings
        Ex. query="Redmi Phone" => {'query': 'Redmi%20Phone'}

        Returns:
            dict: object containing kwargs and URL-encoded kwarg values
        """
        for kwarg in kwargs:
            kwargs[kwarg] = quote(kwargs[kwarg])
        return kwargs


class ShopeeAPI(AbstractAPI):
    def __init__(self):
        self.endpoints = {"products": "https://shopee.ph/api/v4/search/search_items"}

    def search(self, **kwargs):
        def filterData(item, valid_fields=None):
            """receives an item JSON from the Shopee API and removes unecessary fields

            Args:
                item (dict): dict-like object with data on a Shopee item
                valid_fields (iterable, optional): any iterable containing values to keep. Defaults to None.

            Returns:
                dict: The same dict-like object, retaining only the relevant fields
            """
            # the data I choose to be relevant and worth keeping by default
            if not valid_fields:
                valid_fields = (
                    "name",
                    "itemid",
                    "shopid",
                    "price",
                    "price_min",
                    "price_max",
                    "price_before_discount",
                    "raw_discount",
                    "has_lowest_price_guarantee",
                    "stock",
                    "sold",
                    "historical_sold",
                    "liked_count",
                    "view_count",
                    "cmt_count",
                    "shopee_verified",
                    "is_official_shop",
                    "is_preferred_plus_seller",
                    "shop_location",
                    "is_on_flash_sale",
                    "image",
                    "item_rating",
                )

            # create a new field item_rating to get the item's rating score

            # by default, item ratings are formatted like this
            # "item_rating":{
            #    "rating_star":4.764309764309765,
            #    "rating_count":[
            #       307,    # total ratings
            #       6,      # 1 star ratings
            #       5,      # 2 star ratings
            #       8,
            #       15,
            #       273     # 5 star ratings
            #    ]
            # instead of all that, I want to extract exclusively the rating_star value (average rating)
            item["item_rating"] = item["item_rating"]["rating_star"]
            # delete all unimportant fields
            return {field: item[field] for field in valid_fields}

        endpoint = self.endpoints["products"]
        params = AbstractAPI.urlEncodeQuery(**kwargs)

        response = requests.get(url=endpoint, params=kwargs)
        logger.info(f"Sent request to {response.url}")
        response = response.json()
        # list of items returned by the API
        products = response["items"]
        for product in products:
            # item's data
            result = product["item_basic"]
            logger.info(f"Got item {result['itemid']}: {result['name']}")
            yield filterData(result)


def main():
    shopee = ShopeeAPI()
    results = shopee.search(keyword="redmi note 9", by="relevance")
    for result in results:
        print(result)


if __name__ == "__main__":
    main()
