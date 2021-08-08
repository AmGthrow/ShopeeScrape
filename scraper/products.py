import requests
from urllib.parse import quote, unquote
from pprint import pp


class AbstractAPI:
    @staticmethod
    def URLEncodeQuery(**kwargs):
        for kwarg in kwargs:
            kwargs[kwarg] = quote(kwargs[kwarg])
        return kwargs


class ShopeeAPI(AbstractAPI):
    def __init__(self):
        self.endpoints = {"products": "https://shopee.ph/api/v4/search/search_items"}

    def getProducts(self, **kwargs):
        def filterData(item, valid_fields=None):
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

            item["item_rating"] = item["item_rating"]["rating_star"]
            return {field: item[field] for field in valid_fields}

        endpoint = self.endpoints["products"]
        params = AbstractAPI.URLEncodeQuery(**kwargs)

        response = requests.get(url=endpoint, params=kwargs).json()
        products = response["items"]
        for product in products:
            result = product["item_basic"]
            yield filterData(result)

        # by default, item ratings are formatted like this
        # "item_rating":{
        #    "rating_star":4.764309764309765,
        #    "rating_count":[
        #       307,
        #       6,
        #       5,
        #       8,
        #       15,
        #       273
        #    ]
        # instead of all that, I want to extract exclusively the rating_star value (average rating)
        result["item_rating"] = result["item_rating"]["rating_star"]

        # delete all unimportant fields
        result = {field: result[field] for field in fields_to_keep}

        yield result


def main():
    query = input()
    for product in get_products(query):
        pp(product, width=500)


if __name__ == "__main__":
    main()
