import requests
import logging
import utils
from slugify import slugify

# ? it is absolutely disgusting to configure logging inside here,
# ? migrate logging conf settings to the main app instead of the module
# logger for recording searches and results
search_logger = logging.Logger(__name__)
search_logger.setLevel(logging.DEBUG)

# logger to record flash sales
flash_logger = logging.Logger(__name__)
flash_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s - %(asctime)s - %(message)s")
search_handler = logging.FileHandler("./logs/shopee/searches.log",
                                     encoding="utf-8")
flash_handler = logging.FileHandler("./logs/shopee/flash_sales.log",
                                    encoding="utf-8")
search_handler.setFormatter(formatter)
flash_handler.setFormatter(formatter)

search_logger.addHandler(search_handler)
flash_logger.addHandler(flash_handler)

endpoints = {"search": "https://shopee.ph/api/v4/search/search_items"}


def _filter_search_data(item, valid_fields=None):
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
            "price_before_discount",
            "raw_discount",
            "stock",
            "sold",
            "historical_sold",
            "liked_count",
            "view_count",
            "cmt_count",
            "is_on_flash_sale",
            "has_lowest_price_guarantee",
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


def get_item_link(name, itemid, shopid):
    """Generates a valid link to the item's Shopee page

    Given the necessary arguments, constructs the item's
    URL in Shopee using the following convention:
    https://shopee.ph/<item-name-separated-by-hyphens>-i.<shopid>.<itemid>

    Ex. https://shopee.ph/Psicom-Killer-Game-by-Penguin20-i.56563909.1484895861

    Args:
        name (str): Item's name
        itemid (int): ItemID, from ShopeeAPI
        shopid (int): ShopID of the seller, from ShopeeAPI

     Returns:
        str: URL to the Shopee page
    """
    # separate all spaces in item name with a dash
    url_name = slugify(name)
    return f"https://shopee.ph/{url_name}-i.{shopid}.{itemid}"


def search(log_results=True, valid_fields=None, **kwargs):
    """Performs a search query on Shopee and yields the results as a generator

    Performs a get request on the Shopee API's search endpoint and supplies the 
    given kwargs as parameters. Filters the resulting response by discarding
    any fields that aren't inside of the valid_fields iterable. 

    Note: This also automatically discards the number of 1,2,3,...5 star ratings 
    of an item and only keeps the average rating score (see _filter_search_data())

    Args:
        log_results (bool, optional): Whether to log search results
        and flash sales to log files. Defaults to True.
        valid_fields (iterable, optional): All the fields you're 
        interested in and want to keep the data for. Defaults to None.

    Yields:
        [type]: [description]
    """
    endpoint = endpoints["search"]
    params = utils.URLEncodeQuery(**kwargs)

    response = requests.get(url=endpoint, params=kwargs)
    if log_results:
        search_logger.info(f"Sent request to {response.url}")
    response = response.json()

    # list of items returned by the API
    items = response["items"]
    for item in items:
        # item's data
        result = item["item_basic"]
        if log_results:

            # log search result
            short_name = result['name'][:60]
            if len(result['name']) >= 60:
                short_name += '...'
            search_logger.info(
                f"Got item {short_name} ({get_item_link(result['name'],result['itemid'],result['shopid'])})"
            )
            # log in case it's a flash sale too
            if result["is_on_flash_sale"]:
                flash_logger.info(f"FLASH SALE: {result['name']}")

        yield _filter_search_data(result, valid_fields)
