import requests
from bs4 import BeautifulSoup
from .craigslist_parser import CraigsListPost, CraigsListDivParser
from .content_filter import CraigslistPostFilterer

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
    
    def post_divs(self):
        return self.soup.find_all(class_='cl-static-search-result')
    
    def duplicate_title_filter(self, divs):
        post_div_mp = {CraigsListDivParser(div).post_title(): div for div in divs}
        return list(post_div_mp.values())

    def display(self):
        for post in self.posts:
            post.pretty_print()