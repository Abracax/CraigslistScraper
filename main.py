from craigslistscraper import CraigslistSearches

def main():
    """
    Define searches here, a few examples are given below.

    search_name = searches.Searches('your search', 'section')

    default section is 'sss' which is all of craigslist.


    """
    
    cities = ['chicago']
    filters = ['&postedToday=1']

    # TODO: Use domain builder to add filters to searches
    # TODO: Add Post detail filtering
    SEARCH = CraigslistSearches('https://chicago.craigslist.org/search/sss?query=apple&bundleDuplicates=1&postedToday=1')
    SEARCH.display()

if __name__ == '__main__':
    main()




