from abc import ABC, abstractmethod
from datetime import datetime
import re

class GeneralKeywordExtractor(ABC):
    def __init__(self, post, conf):
        self.post = post
        self.conf = conf
        self.__keywords = self.extract_keywords()
    
    @staticmethod
    def __coalesce_post_fields(post):
        flattened_details = ' '.join(str(item) for sublist in post.details for item in sublist)
        text = f'{post.title} {flattened_details} {post.description}' 
        return text

    def extract_keywords(self):
        return self.extract_specs(self.__coalesce_post_fields(self.post))
    
    @abstractmethod
    def extract_specs(self, post):
        """Extract specifications from a single post according to configuration.
        """
        pass

    @property
    def keywords(self):
        return self.__keywords

class CraigslistNumberedSpecExtractor(GeneralKeywordExtractor):
    def __init__(self, post, userconf):
        super().__init__(post, userconf.get("NumberedSpecs", []))

    def extract_specs(self, post):
        specs = [] 
        for unit in self.conf:
            if unit == '"':
                pattern = r'(\d+(\.\d+)?)\s*(?:\\\\)?' + re.escape(unit)
            else:
                pattern = r'(\d+(\.\d+)?)\s*' + re.escape(unit) + r'\b'
            matches = re.findall(pattern, post, re.IGNORECASE)
            if matches:
                spec = [float(match[0]) for match in matches]
                if not spec:
                    continue
                specs.append(f'{spec[0]} {unit}')
        return list(set(specs))
    
class CraigslistSpecsExtractor(GeneralKeywordExtractor):
    def __init__(self, post, userconf):
        super().__init__(post, userconf.get("Specs", []))

    def extract_specs(self, post):
        specs = [] 
        for spec in self.conf:
            pattern = re.escape(spec) + r'\b'
            matches = re.findall(pattern, post, re.IGNORECASE)
            if matches:
                specs.append(f'{spec}')
        return list(set(specs))


class CraigslistDateExtractor(GeneralKeywordExtractor):
    def extract_specs(self, post):
        max_year = datetime.now().year
        pattern = r'\b(\d{4})\b'
        years = []

        matches = re.findall(pattern, post)
        for match in matches:
            year = int(match)
            if year < 2000 or year > max_year:
                continue
            years.append(f'{year}')
        return list(set(years))
