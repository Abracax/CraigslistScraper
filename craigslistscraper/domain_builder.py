from urllib.parse import urlencode
from .config import CRAIGSLIST_DOMAIN


class CraigslistDomainBuilder():
    def __init__(self, craigslist_filter_parser):
        self.__conf = craigslist_filter_parser
    
    def build_domain(self):
        params = {'query': self.__conf.item}
        params.update(self.__conf.search_filters)
        return CRAIGSLIST_DOMAIN.format(self.__conf.city, urlencode(params))
