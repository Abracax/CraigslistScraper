from craigslistscraper import CraigslistScraper 

def main():
    # TODO: Add Content Extraction
    scraper = CraigslistScraper('config/config.json')
    scraper.scrape()
    
if __name__ == '__main__':
    main()