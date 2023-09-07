from craigslistscraper import CraigsListSearchOptionParser, DomainBuilder, CraigslistSearches

def main():
    # TODO: Add Post detail filtering
    cfp = CraigsListSearchOptionParser('./config/config.json')
    db = DomainBuilder(cfp)
    domain = db.build_domain()
    print(domain)
    SEARCH = CraigslistSearches(domain)
    SEARCH.display()
    
if __name__ == '__main__':
    main()