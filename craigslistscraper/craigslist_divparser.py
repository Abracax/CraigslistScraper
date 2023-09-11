import requests
from bs4 import BeautifulSoup

class CraigsListDivParser():
    def __init__(self, soup):
        self.__soup = soup
    
    @property
    def post_title(self):
        return self.__soup.attrs['title']    
    
    @property
    def post_price(self):
        raw_price = self.__soup.find(class_='price').get_text()
        price_number = int(raw_price.replace('$', '').replace(',', ''))
        return price_number

    @property
    def post_link(self):
        return self.__soup.find('a').get('href')
    
class CraigsListAdParser():
    def __init__(self, url):
        self.__soup = BeautifulSoup(requests.get(url).content, 'html.parser')

    @property
    def post_details(self):
        ad_info = self.__soup.select('span')
        data = []
        details = []

        for info in ad_info:
            if not (info.has_attr('class') or info.has_attr('id')):
                data.append(info)

        for d in data:
            detail = d.text.split(': ')
            detail = [d.lower() for d in detail]
            details.append(detail)
        return details
    
    @property
    def post_description(self):
        descs =[]
        description_raw = self.__soup.find_all(id='postingbody')

        for item in description_raw:
            unfiltered = item.get_text(strip=True)
            desc = unfiltered.strip('QR Code Link to This Post')
            desc = desc.lower() 
            descs.append(desc)
        
        if not len(descs) == 1:
            return ""
        
        return descs[0]
