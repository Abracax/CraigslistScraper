import json
from .div_parsers import CraigsListDivParser, CraigsListAdParser

class CraigsListPost:
    def __init__(self, div):
        self.link = CraigsListDivParser(div).post_link()
        self.detail = CraigsListAdParser(self.link).post_details()
        self.description = CraigsListAdParser(self.link).post_description()
        self.title = CraigsListDivParser(div).post_title()
        self.price = CraigsListDivParser(div).post_price()
        self.keywords = [] 
    
    def add_keywords(self, keywords):
        self.keywords += keywords

    def pretty_print(self):
        obj_dict = {
            'title': self.title,
            'price': self.price,
            'link': self.link,
            'keywords' : self.keywords
        }
        
        pretty_str = json.dumps(obj_dict, indent=4)
        print(pretty_str)