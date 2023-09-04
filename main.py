from craigslistscraper import CraigslistSearches, Searches
import time


def main():
    """
    Define searches here, a few examples are given below.

    search_name = searches.Searches('your search', 'section')

    default section is 'sss' which is all of craigslist.


    """
    
    cities = ['chicago']
    filters = ['&postedToday=1']

    # some examples of what can be done
    # TODO: Use domain builder to add filters to searches
    # TODO: Add Post detail filtering
    SEARCH = CraigslistSearches('https://chicago.craigslist.org/search/sss?query=apple&bundleDuplicates=1&postedToday=1')

    import IPython; IPython.embed()


if __name__ == '__main__':
    main()




