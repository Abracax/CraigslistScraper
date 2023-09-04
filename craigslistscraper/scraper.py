import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

class CraigsListDivParser():
    def __init__(self, soup):
        self.soup = soup
    
    def post_title(self):
        return self.soup.attrs['title']    
    
    def post_price(self):
        raw_price = self.soup.find(class_='price').get_text()
        price_number = int(raw_price.replace('$', '').replace(',', ''))
        return price_number

    def post_link(self):
        return self.soup.find('a').get('href')
    
class CraigsListAdParser():
    def __init__(self, url):
        ad_page = requests.get(url)
        self.soup = BeautifulSoup(ad_page.content, 'html.parser')
    
    def post_details(self):
        ad_info = self.soup.select('span')
        data = []
        details = []

        for info in ad_info:  # only keep elements that don't have a 'class' or 'id' attribute
            if not (info.has_attr('class') or info.has_attr('id')):
                data.append(info)

        for d in data:
            details.append(d.text.split(': '))
        
        return details
    
    def post_description(self):
        descs =[]
        description_raw = self.soup.find_all(id='postingbody')

        for item in description_raw:
            unfiltered = item.get_text(strip=True)
            descs.append(unfiltered.strip('QR Code Link to This Post'))
        
        return descs

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
    
class CraigslistSearches:
    """
    Object that pulls all relevent ad information and returns them
    in arrays to be parsed to a JSON file.
    """

    def __init__(self, domain_get):
        self.page = requests.get(domain_get)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        self.divs = self.duplicate_title_filter(self.post_divs())
    
    def post_divs(self):
        return self.soup.find_all(class_='cl-static-search-result')
    
    def duplicate_title_filter(self, divs):
        post_div_mp = {CraigsListDivParser(div).post_title(): div for div in divs}
        return list(post_div_mp.values())

    def display(self):
        for div in self.divs:
            CraigsListPost(div).pretty_print()
    
    def pd_display(self):  
        """
        Displays data pulled from search in terminal, and 
        puts data into 'search_info.csv'.
        """

        data = pd.DataFrame( # Displays data
            {
                'Name:': self.name(),
                'Price:': self.price(),
                'HREF:': self.ad_href()
            })

        # Parses data into 'search_info.csv'
        data.to_csv('data/search_info.csv', index=False, mode='a')

        if data.empty is True:
            print('No Results')
        else:
            print(data)





