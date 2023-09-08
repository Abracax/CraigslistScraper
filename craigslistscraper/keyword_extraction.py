from abc import ABC, abstractmethod
from datetime import datetime
import re

class GeneralKeywordExtractor(ABC):
    def __init__(self, post, conf):
        self.post = post
        self.conf = conf
        self.keywords = self.extract_keywords()
    
    @staticmethod
    def coalesce_post_fields(post):
        flattened_details = ' '.join(str(item) for sublist in post.detail for item in sublist)
        text = flattened_details + str(post.description) + str(post.title)
        return text.lower()

    def extract_keywords(self):
        print('Extracting keywords...')
        return self.extract_specs(self.coalesce_post_fields(self.post))
    
    @abstractmethod
    def extract_specs(self, post):
        """Extract specifications from a single post according to configuration.
        """
        pass

class CraigslistNumberedSpecExtractor(GeneralKeywordExtractor):
    def __init__(self, post, userconf):
        super().__init__(post, userconf.get("NumberedSpecs", []))

    def extract_specs(self, post):
        specs = [] 
        for unit in self.conf:
            unit = unit.lower()
            pattern = r'(\d+(\.\d+)?)\s*' + re.escape(unit) + r'\b'
            matches = re.findall(pattern, post, re.IGNORECASE)
            if matches:
                spec = [float(match[0]) for match in matches]
                if not spec:
                    continue
                specs.append(f'{spec[0]} {unit}')
        return specs
    
class CraigslistSpecsExtractor(GeneralKeywordExtractor):
    def __init__(self, post, userconf):
        super().__init__(post, userconf.get("Specs", []))

    def extract_specs(self, post):
        specs = [] 
        for spec in self.conf:
            spec = spec.lower()
            pattern = re.escape(spec) + r'\b'
            matches = re.findall(pattern, post, re.IGNORECASE)
            if matches:
                specs.append(f'{spec}')
        return specs


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
        return years
