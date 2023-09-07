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

```python
from craigslistscraper import CraigsListSearchOptionParser, DomainBuilder, CraigslistSearches

cfp = CraigsListSearchOptionParser('./config/config.json')
domain = DomainBuilder(cfp).build_domain()
CraigslistSearches(domain).display()
```

**Note #1:** Filters are user defined. Check the supported schema at `config/options.json` an example configuration at `config/config.json`. Current schema supports all search filter options available on Craigslist.

**Note #2:** For a list of cities view the `craigslistscraper/data/cities.csv` file

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.
