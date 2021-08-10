import requests
import logging
from urllib.parse import quote

# logger for recording searches and results
search_logger = logging.Logger(__name__)
search_logger.setLevel(logging.DEBUG)

# logger to record flash sales
flash_logger = logging.Logger(__name__)
flash_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s - %(asctime)s - %(message)s")
search_handler = logging.FileHandler("./logs/searches.log", encoding="utf-8")
flash_handler = logging.FileHandler("./logs/flash_sales.log", encoding="utf-8")
search_handler.setFormatter(formatter)
flash_handler.setFormatter(formatter)

search_logger.addHandler(search_handler)
flash_logger.addHandler(flash_handler)


class AbstractAPI:
    @staticmethod
    def URLEncodeQuery(**kwargs):
        """Encodes values to URL-friendly strings
        Ex. query="Redmi Phone" => {'query': 'Redmi%20Phone'}

        Returns:
            dict: object containing kwargs and URL-encoded kwarg values
        """
        for kwarg in kwargs:
            try:
                kwargs[kwarg] = quote(str(kwargs[kwarg]))
            except:
                search_logger.exception(f"Could not url-encode kwarg: {kwargs[kwarg]}")
        return kwargs


class ShopeeAPI(AbstractAPI):
    endpoints = {"search": "https://shopee.ph/api/v4/search/search_items"}

    def search(self, **kwargs):
        def filter_data(item, valid_fields=None):
            """receives an item JSON from the Shopee API and removes unecessary fields

            Args:
                item (dict): dict-like object with data on a Shopee item
                valid_fields (iterable, optional): any iterable containing values to keep. Defaults to None.

            Returns:
                dict: The same dict-like object, retaining only the relevant fields
            """
            # the data I choose to be relevant and worth keeping by default
        if valid_fields is None:
                valid_fields = (
                    "name",
                    "itemid",
                    "shopid",
                    "price",
                    "price_min",
                    "price_max",
                    "is_on_flash_sale",
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

        endpoint = ShopeeAPI.endpoints["search"]
        params = AbstractAPI.URLEncodeQuery(**kwargs)

        response = requests.get(url=endpoint, params=kwargs)
        search_logger.info(f"Sent request to {response.url}")
        response = response.json()
        # list of items returned by the API
        items = response["items"]
        for item in items:
            # item's data
            result = item["item_basic"]
            search_logger.info(f"Got item {result['itemid']}: {result['name']}")
            if result["is_on_flash_sale"]:
                flash_logger.info(f"FLASH SALE: {result['name']}")
            yield filter_data(result)


def search_shopee(**kwargs):
    shopee = ShopeeAPI()
    yield from shopee.search(**kwargs)
