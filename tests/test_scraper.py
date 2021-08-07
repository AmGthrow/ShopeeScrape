import unittest
from scraper import scraper

class TestScraper(unittest.TestCase):
    def setUp(self) -> None:
        self.query = "hyperx cloud stinger"
        self.scrape_results = scraper.scrape(self.query)

