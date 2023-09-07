import json
from .craigslist_parser import CraigsListDivParser, CraigsListAdParser

class CraigsListPost:
    def __init__(self, div):
        self.link = CraigsListDivParser(div).post_link()
        self.detail = CraigsListAdParser(self.link).post_details()
        self.description = CraigsListAdParser(self.link).post_description()
        self.title = CraigsListDivParser(div).post_title()
        self.price = CraigsListDivParser(div).post_price()

    def pretty_print(self):
        obj_dict = {
            'title': self.title,
            'price': self.price,
            'link': self.link,
            'detail': self.detail,
            'description': self.description
        }
        
        pretty_str = json.dumps(obj_dict, indent=4)
        print(pretty_str)