from .conf_parser import UserConfigParser
from .domain_builder import DomainBuilder
from .craigslist_scraper import CraigslistSearches

class CraigslistScraper:
    def __init__(self, userconf_path) -> None:
        self.conf = userconf_path

    def scrape(self):
        ucp = UserConfigParser(self.conf)
        domain = DomainBuilder(ucp).build_domain()
        print(domain)
        searcher = CraigslistSearches(domain, ucp)
        searcher.display()
        return searcher.posts 
