# TODO: Move this to another module? "main" is an ambiguous filename

import json
from utils import get_queries_from_config
from scrapers import shopee
from data.database import ShopeeDatabase

def main():
    db = ShopeeDatabase("data/shopee.db")
    to_search = get_queries_from_config()
    for search_query in to_search:
        search_results = shopee.search(add_url=True, **search_query)
        db.add_items(search_results)


if __name__ == "__main__":
    main()