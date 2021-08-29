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
    valid_fields: [str] = shopee.get_valid_fields()

    def create_tables(self) -> None:
        """Initializes a ShopeeProducts database to store item info of products
        from Shopee
        """
        with self.conn:
            # TODO: Find a way to keep the column names and their data types depend on the config.json instead of being hard-coded
            self.conn.execute("""CREATE TABLE IF NOT EXISTS `ShopeeProducts` (
                timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
                name TEXT,
                url TEXT,
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
                rating_count INTEGER
            ) """)

    def add_items(self, items: [dict]):
        """Adds the contents of a Shopee JSON response into the database

        Args:
            items ([dict]): A list of dict-like JSONs which each represent a
            Shopee item
        """        
        # 'url' doesn't count as a valid_field since it's custom, we need to add it manually
        to_insert = ShopeeDatabase.valid_fields + ['url']
        column_names: str = ', '.join(to_insert)
        parameter_names: str = ', '.join(":" + field for field in to_insert)
        with self.conn:
            self.conn.executemany(
                f"""INSERT INTO `ShopeeProducts` ({column_names}) VALUES( {parameter_names})""",
                items)
