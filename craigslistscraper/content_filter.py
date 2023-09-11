from .craigslist_post import CraigsListPost

class CraigslistPostContentFilterer:
    def __init__(self, posts, filters):
        self.__validate_posts(posts)
        self.__posts = self.__filter_posts(posts, filters)
    
    @staticmethod
    def __validate_posts(posts):
        if not all(isinstance(post, CraigsListPost) for post in posts):
            raise Exception("Posts must be of type CraigsListPost")
    
    @staticmethod
    def __apply_text_filters(text, musthaves, blacklisted):
        text_lower = text.lower()
        has_musthave = any(musthave.lower() in text_lower for musthave in musthaves) if musthaves else True
        has_blacklisted = any(word.lower() in text_lower for word in blacklisted)
        return has_musthave and not has_blacklisted
    
    def __passes_filters(self, post, filters):
        if filters is None:
            return None
        return all([
            self.__apply_text_filters(post.title, filters.get('TitleMustHaveList', []), filters.get('TitleBlacklist', [])),
            self.__apply_text_filters(post.description, filters.get('DescriptionMustHaveList', []), filters.get('DescriptionBlacklist', []))
        ])

    def __filter_posts(self, posts, filters):
        print('Filtering posts...')
        return [post for post in posts if self.__passes_filters(post, filters)]

    @property
    def posts(self):
        return self.__posts

