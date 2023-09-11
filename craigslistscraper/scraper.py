from .conf_parser import UserConfigParser
from .domain_builder import CraigslistDomainBuilder
from .craigslist_scraper import CraigslistScraperMain

class CraigslistScraper:
    def __init__(self, userconf_path) -> None:
        self.__conf = userconf_path

    def scrape(self):
        ucp = UserConfigParser(self.__conf)
        domain = CraigslistDomainBuilder(ucp).build_domain()
        print(domain)
        searcher = CraigslistScraperMain(domain, ucp)
        searcher.display()
        return searcher.posts 
