from .craigslist_parser import CraigsListPost

class CraigslistPostFilterer:
    def __init__(self, posts, filters):
        self.validate_posts(posts)
        if filters is None:
            self.posts = posts
        else:
            self.posts = self.filter_posts(posts, filters)
    
    @staticmethod
    def validate_posts(posts):
        if not all(isinstance(post, CraigsListPost) for post in posts):
            raise Exception("Posts must be of type CraigsListPost")
    
    @staticmethod
    def apply_text_filters(text, musthaves, blacklisted):
        text_lower = text.lower()
        has_musthave = any(musthave.lower() in text_lower for musthave in musthaves) if musthaves else True
        has_blacklisted = any(word.lower() in text_lower for word in blacklisted)
        return has_musthave and not has_blacklisted
    
    def passes_filters(self, post, filters):
        return all([
            self.apply_text_filters(post.title, filters.get('TitleMustHaveList', []), filters.get('TitleBlacklist', [])),
            self.apply_text_filters(post.description, filters.get('DescriptionMustHaveList', []), filters.get('DescriptionBlacklist', []))
        ])

    def filter_posts(self, posts, filters):
        print('Filtering posts...')
        return [post for post in posts if self.passes_filters(post, filters)]
