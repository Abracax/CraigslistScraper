import requests
from bs4 import BeautifulSoup
from .craigslist_divparser import CraigsListDivParser
from .craigslist_post import CraigsListPost
from .content_filter import CraigslistPostContentFilterer
from .keyword_extraction import CraigslistNumberedSpecExtractor, CraigslistDateExtractor, CraigslistSpecsExtractor

class CraigslistScraperMain:
    """
    Object that pulls all relevent ad information and returns them
    in arrays to be parsed to a JSON file.
    """

    def __init__(self, domain, user_config_parser):
        self.soup = BeautifulSoup(requests.get(domain).content, 'html.parser')
        raw_posts = [CraigsListPost(div) for div in self.__duplicate_title_filter(self.__get_post_divs())]
        self.posts = CraigslistPostContentFilterer(raw_posts, user_config_parser.post_content_filters).posts
        self.__keyword_extraction(user_config_parser.keyword_extraction)

    def __keyword_extraction(self, conf):
        for post in self.posts:
            numbered_specs = CraigslistNumberedSpecExtractor(post, conf).keywords
            reg_specs = CraigslistSpecsExtractor(post, conf).keywords
            dates = CraigslistDateExtractor(post, conf).keywords
            specs = numbered_specs + reg_specs + dates
            post.add_keywords(specs)
    
    def __get_post_divs(self):
        return self.soup.find_all(class_='cl-static-search-result')
    
    def __duplicate_title_filter(self, divs):
        post_div_mp = {CraigsListDivParser(div).post_title: div for div in divs}
        return list(post_div_mp.values())

    def display(self):
        for post in self.posts:
            post.pretty_print()
