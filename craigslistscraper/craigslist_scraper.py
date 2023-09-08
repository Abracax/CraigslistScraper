import requests
from bs4 import BeautifulSoup
from .div_parsers import CraigsListDivParser
from .craigslist_post import CraigsListPost
from .content_filter import CraigslistPostFilterer
from .keyword_extraction import CraigslistNumberedSpecExtractor, CraigslistDateExtractor, CraigslistSpecsExtractor

class CraigslistSearches:
    """
    Object that pulls all relevent ad information and returns them
    in arrays to be parsed to a JSON file.
    """

    def __init__(self, domain_get, user_config_parser):
        self.page = requests.get(domain_get)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        filtered_post_divs = self.duplicate_title_filter(self.post_divs())
        posts = [CraigsListPost(div) for div in filtered_post_divs]
        self.posts = CraigslistPostFilterer(posts, user_config_parser.get_post_content_filters()).posts 
        self.keyword_extraction(user_config_parser.get_keyword_extraction())

    def keyword_extraction(self, conf):
        for post in self.posts:
            numbered_specs = CraigslistNumberedSpecExtractor(post, conf).keywords
            reg_specs = CraigslistSpecsExtractor(post, conf).keywords
            dates = CraigslistDateExtractor(post, conf).keywords
            specs = numbered_specs + reg_specs + dates
            post.add_keywords(specs)
    
    def post_divs(self):
        return self.soup.find_all(class_='cl-static-search-result')
    
    def duplicate_title_filter(self, divs):
        post_div_mp = {CraigsListDivParser(div).post_title(): div for div in divs}
        return list(post_div_mp.values())

    def display(self):
        for post in self.posts:
            post.pretty_print()
