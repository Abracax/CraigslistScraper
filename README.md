# CraigslistScraper

**Note:** CraigslistScraper is for personal use and data science only.

CraigslistScraper is a web scraper for craigslist. Users define what they would
like to search for then CraigslistScraper pulls ad data from their defined
search and places it neatly inside of a JSON file.

<!-- TABLE OF CONTENTS -->
Table of Contents
=================

- [CraigslistScraper](#craigslistscraper)
- [Table of Contents](#table-of-contents)
  - [Usage](#usage)
  - [License](#license)

<!-- USAGE -->
## Usage

Example:

Write a configuration similar to the example configuration at `config/config.json`. Pass in the configuration path to the Scraper.

```json
{
    "City": "chicago",
    "Item": "mac",
    "SearchFilter": {
        "hasPic": 1,
        "min_price": 30,
        "max_price": 500,
        "postedToday": 1
    },
    "PostContentFilter": {
        "TitleMustHaveList" : ["macbook", "mac book", "macbook pro", "mac book pro"],
        "TitleBlackList" : ["case", "cover", "sleeve", "bag", "charger", "adapter", "screen"],
        "DescriptionBlackList" : ["dead", "broken", "cracked", "damaged", "faulty", "not working"],
        "DescriptionMustHaveList" : ["pro"]
    }
}
```

The Scraper takes in a path to the user configuration file and performs the scraping. It currently pretty prints the results..

```python
from craigslistscraper import CraigslistScraper 

def main():
    scraper = CraigslistScraper('config/config.json')
    scraper.scrape()
```

Here is an example of the results:

```json
{
    "title": "Macbook Pro Retina 13 inch laptop",
    "price": 175,
    "link": "https://chicago.craigslist.org/sys/d/xxxx/yyyy.html",
    "detail": [
        [
            " (xxxxxx)"
        ],
        [
            "condition",
            "good"
        ],
        [
            "make / manufacturer",
            "apple"
        ]
    ],
    "description": "i have a macbook pro retina early 2013 for sale."
}
```

**Note #1:** Filters are user defined. Check the supported schema at `config/options.json` and an example configuration at `config/config.json`. Current schema supports all search filter options available on Craigslist, and allows strict keyword filtering for title and description.

**Note #2:** For a list of cities view the `craigslistscraper/data/cities.csv` file

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.
