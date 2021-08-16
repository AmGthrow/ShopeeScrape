import sqlite3
from scrapers import shopee
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


class ShopeeDatabase(CommerceDatabase):
    valid_fields = shopee.get_valid_fields()

    def create_tables(self):
        with self.conn:
            # TODO: Find a way to keep the column names and their data types depend on the config.json instead of being hard-coded
            self.conn.execute("""CREATE TABLE IF NOT EXISTS `ShopeeProducts` (
                timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
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
                item_rating REAL,
                item_count INTEGER
            ) """)

    def add_items(self, items):
        try:
            with self.conn:
                self.conn.executemany(
                    """INSERT INTO `ShopeeProducts`(
                        name, itemid, shopid, price,
                        price_min, price_max, price_before_discount, raw_discount,
                        is_on_flash_sale, has_lowest_price_guarantee, stock, sold,
                        historical_sold, liked_count, view_count, cmt_count,
                        shopee_verified, is_official_shop, is_preferred_plus_seller,
                        shop_location, image, item_rating 
                    ) VALUES(
                        :name, :itemid, :shopid, :price, :price_min,
                        :price_max, :price_before_discount, :raw_discount,
                        :is_on_flash_sale, :has_lowest_price_guarantee, :stock, :sold,
                        :historical_sold, :liked_count, :view_count, :cmt_count,
                        :shopee_verified, :is_official_shop, :is_preferred_plus_seller,
                        :shop_location, :image, :item_rating
                    )""", items)
        except sqlite3.OperationalError:
            print(
                "Table for Shopee items does not exist yet. Please initialize with "
                "ShopeeDatabase.create_tables()")
