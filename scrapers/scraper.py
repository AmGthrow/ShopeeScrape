import scrapy
from scrapy.crawler import CrawlerProcess

class ProductsSpider(scrapy.Spider):
    name = "products"



def main():
    process = CrawlerProcess(install_root_handler=False)
    process.crawl(ProductsSpider)
    process.start()


if __name__ == "__main__":
    main()