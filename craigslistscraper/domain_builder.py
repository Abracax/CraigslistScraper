from urllib.parse import urlencode

DOMAIN = "https://{}.craigslist.org/search/sss?{}"

class DomainBuilder():
    def __init__(self, craigslist_filter_parser):
        self.cfp = craigslist_filter_parser
    
    def build_domain(self):
        city = self.cfp.get_city()
        item = self.cfp.get_item()
        filter = self.cfp.get_search_filters()

        params = {'query': item}
        params.update(filter)

        url_params = urlencode(params)

        return DOMAIN.format(city, url_params)
