import json
from .craigslist_divparser import CraigsListDivParser, CraigsListAdParser

class CraigsListPost:
    def __init__(self, div):
        self.__link = CraigsListDivParser(div).post_link
        self.__details = CraigsListAdParser(self.__link).post_details
        self.__description = CraigsListAdParser(self.__link).post_description
        self.__title = CraigsListDivParser(div).post_title
        self.__price = CraigsListDivParser(div).post_price
        self.__keywords = [] 
    
    def add_keywords(self, keywords):
        self.__keywords += keywords

    def pretty_print(self):
        obj_dict = {
            'title': self.title,
            'price': self.price,
            'link': self.link,
            'keywords' : self.keywords
        }
        pretty_str = json.dumps(obj_dict, indent=4)
        print(pretty_str)
    
    def detailed_print(self):
        obj_dict = {
            'title': self.title,
            'price': self.price,
            'link': self.link,
            'keywords' : self.keywords,
            'details' : self.details,
            'description' : self.description
        }
        pretty_str = json.dumps(obj_dict, indent=4)
        print(pretty_str)
    
    @property
    def title(self):
        return self.__title
    
    @property
    def price(self):
        return self.__price
    
    @property
    def link(self):
        return self.__link
    
    @property
    def keywords(self):
        return self.__keywords
    
    @property
    def details(self):
        return self.__details
    
    @property
    def description(self):
        return self.__description