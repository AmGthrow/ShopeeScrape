# ShopeeScrape
Web scraper to extract and record prices of items on the e-commerce website "Shopee".

## Search arguments
### Usage
First, create a connection to the Shopee website and begin searching like this:

```
from scrapers.shops import ShopeeAPI
shopee = ShopeeAPI()
shopee.search()
```

The `search()` function accepts multiple keyword arguments to narrow down search results. Here's a summary of them.
| Keyword      |      Possible Values        | Description                                                           |
|--------------|-----------------------------|-----------------------------------------------------------------------|
| keyword      | \<str\>                     | The search query for Shopee to search                                 |
| sortBy       | relevancy,ctime,sales,price | Sort the results by relevancy, latest, top sales, or price            |
| order        | asc,desc                    | Sort the results in ascending or descending order                     |
| officialMall | true,false                  | Only retrieve results from Shopee Mall sellers                        |
| preferred    | true,false                  | Only retrieve results from preferred sellers                          |
| minPrice     | \<int\>                     | Only retrieve results with price greater than the given int           |
| maxPrice     | \<int\>                     | Only retrieve results with price less than the given int              |
| limit        | \<int\>                     | Limit number of results to given int                                  |
| ratingFilter | 1,2,3,4,5                   | Average rating must be higher than the given int                      |
