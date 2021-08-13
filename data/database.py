import sqlite3
from abc import ABC, abstractmethod


class CommerceDatabase(ABC):
    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)

    def query(self, query):
        with self.conn:
            return self.conn.execute(query)

    @abstractmethod
    def create_tables(self):
        pass


def create_db(db_path="shops.db"):
    with sqlite3.connect(db_path) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS `ShopeeProducts` (
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
            name TEXT,
            itemid INTEGER,
            shopid INTEGER,
            price INTEGER,
            price_min INTEGER,
            price_max INTEGER,
            price_before_discount INTEGER,
            raw_discount INTEGER,
            is_on_flash_sale BOOL,
            has_lowest_price_guarantee BOOL,
            stock INTEGER,
            sold INTEGER,
            historical_sold INTEGER,
            liked_count INTEGER,
            view_count INTEGER,
            cmt_count INTEGER,
            shopee_verified BOOL,
            is_official_shop BOOL,
            is_preferred_plus_seller BOOL,
            shop_location TEXT,
            image TEXT,
            item_rating REAL
        ) """)


