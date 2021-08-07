import requests
from urllib.parse import quote, unquote
from pprint import pp


def get_products(query, by="relevance", limit=10):
    # encode search query to URL-friendly format
    query = quote(query)

    # call Shopee API
    response = requests.get(
        f"https://shopee.ph/api/v4/search/search_items?by={by}&keyword={query}&limit={limit}&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"
    ).json()

    # list of items returned by API
    products = response["items"]

    # the data that I (arbitrarily) choose to be relevant and worth keeping
    fields_to_keep = (
        "name",
        "shopid",
        "stock",
        "sold",
        "historical_sold",
        "liked_count",
        "view_count",
        "cmt_count",
        "price",
        "price_min",
        "price_max",
        "price_before_discount",
        "has_lowest_price_guarantee",
        "raw_discount",
        "shopee_verified",
        "is_official_shop",
        "is_preferred_plus_seller",
        "shop_location",
        "is_on_flash_sale",
        "image",
        "item_rating",
    )

    for product in products:
        # bring out all the item data
        result = product["item_basic"]

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
