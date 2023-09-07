from craigslistscraper import UserConfigParser, DomainBuilder, CraigslistSearches

def main():
    # TODO: Add Post detail filtering
    # TODO: Add Content Extraction
    ucp = UserConfigParser('./config/config.json')
    db = DomainBuilder(ucp)
    domain = db.build_domain()
    print(domain)
    SEARCH = CraigslistSearches(domain)
    SEARCH.display()
    
if __name__ == '__main__':
    main()