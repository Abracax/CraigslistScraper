import json
import requests
from bs4 import BeautifulSoup

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
