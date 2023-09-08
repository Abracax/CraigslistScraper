from .utils import ConfigValidationException
from .utils import read_config, read_cities

CONFIG_OPTIONS = "config/options.json"

class UserConfigParser:
    def __init__(self, filter):
        self.filter = read_config(filter)
        self.options = read_config(CONFIG_OPTIONS)
        self.parsed_config = self.parse_user_filter()
        self.validate_city()
    
    def validate_value(self, key, value, type, allowed, nested_type=None):
        if type == "object":
            if not isinstance(value, dict):
                raise ConfigValidationException(key, value, "object")
            schema = self.options[key]['value']
            filter = value
            for k, v in filter.items():
                if k not in schema:
                    raise ConfigValidationException(k, v, f"Unknown key: {k}")
                params = schema[k]
                self.validate_value(k, v, params.get('type', None), params.get('allowed', None), params.get('value_type', None))
        if type == 'boolean':
            if not isinstance(value, int) or value not in [0, 1]:
                raise ConfigValidationException(key, value, 'boolean', [0, 1])
        elif type == 'number':
            if not isinstance(value, (int)):
                raise ConfigValidationException(key, value, 'number')
        elif type == 'string':
            if not isinstance(value, str):
                raise ConfigValidationException(key, value, 'string')
        elif type == 'array':
            if not isinstance(value, list):
                raise ConfigValidationException(key, value, f"The value for {key} must be an array")
            for item in value:
                if nested_type == 'string':
                    if not isinstance(item, str):
                        raise ConfigValidationException(key, item, f"All elements in {key} must be of type string")
                elif nested_type == 'number':
                    if not isinstance(item, (int, float)):
                        raise ConfigValidationException(key, item, f"All elements in {key} must be of type number")
                elif nested_type == 'boolean':
                    if not isinstance(item, int) or item not in [0, 1]:
                        raise ConfigValidationException(key, item, f"All elements in {key} must be of type boolean")
        
        if allowed is not None:
            if value not in allowed:
                raise ConfigValidationException(key, value, type, allowed)
    
    def validate_city(self):
        city = self.parsed_config.get('City', None)
        if city is None:
            raise ConfigValidationException('City', city, 'string', "See city.csv for a list of cities")
        city = city.lower()
        self.parsed_config['City'] = city
        if city not in read_cities():
            raise ConfigValidationException('City', city, 'string', "See city.csv for a list of cities")

    def parse_user_filter(self):
        parsed_config = {}
        for key, value in self.filter.items():
            if key not in self.options:
                raise ConfigValidationException(key, value, f"Unknown key: {key}")
            
            params = self.options[key]
            type = params.get('type', None)
            allowed = params.get('allowed', None)
            nested_type = params.get('value_type', None)
            self.validate_value(key, value, type, allowed, nested_type)
            parsed_config[key] = value
        return parsed_config
    
    def get_search_filters(self):
        return self.parsed_config.get('SearchFilter', None)
    
    def get_item(self):
        return self.parsed_config.get('Item', None)
    
    def get_city(self):
        return self.parsed_config.get('City', None)
    
    def get_post_content_filters(self):
        return self.parsed_config.get('PostContentFilter', None)
    
    def get_keyword_extraction(self):
        return self.parsed_config.get('KeywordExtraction', None)
