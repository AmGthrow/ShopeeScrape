# TODO: Move this to another module? "main" is an ambiguous filename

import json
from scrapers import shopee
from data.database import ShopeeDatabase

def main():
    db = ShopeeDatabase("./data/shopee.db")
    to_search = json.load(open('config.json'))['search_queries']
    for search_query in to_search:
        search_results = shopee.search(keyword=search_query)
        db.add_items(search_results)


if __name__ == "__main__":
    main()