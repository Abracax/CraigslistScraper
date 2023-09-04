from craigslistscraper import domain, scraper, json_build


class Searches:
    """
    Class purpose is for reusability of code.
    """

    def __init__(self, search, cities, filters=['&postedToday=1']):
        self.search = search
        self.domains, self.cities = domain.domain_builder(search, filters, cities)
    









