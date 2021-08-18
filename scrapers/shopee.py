import requests
import logging
import utils
import json
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


def get_valid_fields() -> [str]:
    """Retrieves the list of fields that the scraper is meant to store

    Retrieves a list of field names from a config.json file. Field names 
    must match names returned by the Shopee API when performing a search request

    Returns:
        [str]: list of strings containing the names of valid fields
    """
    return json.load(open('config.json'))['scrapers']['shopee']['valid_fields']


valid_fields: [str] = get_valid_fields()


def flatten_search_results(item: dict) -> dict:
    """Flattens the nested rating data in a Shopee item's JSON and makes it 
    one-dimensional


    by default, item ratings are formatted like this

    "item_rating":{
       "rating_star":4.764309764309765,     # average rating
       "rating_count":[
          307,    # total ratings
          6,      # 1 star ratings
          5,      # 2 star ratings
          8,      # 3 star ratings
          15,     # 4 star ratings
          273     # 5 star ratings
       ]
    }

    instead of all that, I want to extract exclusively the rating_star value (average rating)

    Args:
        item (dict): dict object with data on a Shopee item 

    Returns:
        dict: The same dict object, except the rating_count and item_rating are 
        de-nested

    """
    item["rating_count"]: int = item["item_rating"]["rating_count"][0]
    item["item_rating"]: float = item["item_rating"]["rating_star"]

    return item


def filter_search_results(item: dict) -> dict:
    """receives an item JSON from the Shopee API and removes unecessary fields

    Args:
        item (dict): dict object with data on a Shopee item

    Returns:
        dict: The same dict object, retaining only the relevant fields
    """
    return {field: item[field] for field in valid_fields}


def get_item_link(item: dict):
    """Generates a valid link to the item's Shopee page

    Given the necessary arguments, constructs the item's
    URL in Shopee using the following convention:
    https://shopee.ph/<item-name-separated-by-hyphens>-i.<shopid>.<itemid>

    Ex. https://shopee.ph/Psicom-Killer-Game-by-Penguin20-i.56563909.1484895861

    Args:
        item (dict): A JSON-like object containing a shopee ite'ms data

     Returns:
        str: URL to the Shopee page
    """
    # separate all spaces in item name with a dash
    try:
        url_name: str = slugify(item['name'])
        result: str = f"https://shopee.ph/{url_name}-i.{item['shopid']}.{item['itemid']}"
    except KeyError:
        raise KeyError("Dict is missing necessary item data")
    # log the url if it's incorrect and doesn't exist
    try:
        response = requests.get(result)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        search_handler.error(f"URL doesn't exist: {url_name}")

    return result


def search(filter_results=True,
           flatten_results=True,
           log_results=True,
           **kwargs) -> dict:
    """Performs a search query on Shopee and yields the results as a generator

    Performs a get request on the Shopee API's search endpoint and supplies 
    given kwargs as parameters. 

    Args:
        filter_results (bool, optional): Whether to apply the filter_search_results()
        function to the resulting search data. Defaults to True.
        flatten_results (bool, optional): Whether to apply the flatten_search_results()
        function to the resulting search data. Defaults to True. 
        log_results (bool, optional): Whether to log search results
        and flash sales to log files. Defaults to True.

    Yields:
        dict: JSON containing the resulting item's data 
    """
    endpoint = endpoints["search"]
    params = utils.URLEncodeQuery(**kwargs)

    response = requests.get(url=endpoint, params=kwargs)
    if log_results:
        search_logger.info(f"Sent request to {response.url}")

    # list of items returned by the API
    items = response.json()["items"]
    for item in items:
        # item's data
        result = item["item_basic"]
        if log_results:
            # log search result
            short_name = result['name'][:60]
            # shorten name if it's too long
            if len(result['name']) >= 60:
                short_name += '...'
            search_logger.info(
                f"Got item {short_name} ({get_item_link(result)})"
            )
            # log in case it's a flash sale too
            if result["is_on_flash_sale"]:
                flash_logger.info(f"FLASH SALE: {result['name']}")
        if flatten_results:
            result = flatten_search_results(result)
        if filter_results:
            result = filter_search_results(result)
        yield result
