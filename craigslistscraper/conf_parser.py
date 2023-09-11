from .utils import ConfigValidationException
from .utils import read_config, read_cities
from .config import CONFIG_OPTIONS_PATH
import functools


class UserConfigParser:
    def __init__(self, filter):
        self.__filter = read_config(filter)
        self.__options = read_config(CONFIG_OPTIONS_PATH)
        self.__parsed_config = self.__parse_user_filter()
        self.__validate_city()
    
    def __validate_value(self, key, value, type, allowed, nested_type=None):
        if type == "object":
            if not isinstance(value, dict):
                raise ConfigValidationException(key, value, "object")
            schema = self.__options[key]['value']
            filter = value
            for k, v in filter.items():
                if k not in schema:
                    raise ConfigValidationException(k, v, f"Unknown key: {k}")
                params = schema[k]
                self.__validate_value(k, v, params.get('type', None), params.get('allowed', None), params.get('value_type', None))
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
    
    def __validate_city(self):
        city = self.__parsed_config.get('City', None)
        if city is None:
            raise ConfigValidationException('City', city, 'string', "See city.csv for a list of cities")
        city = city.lower()
        self.__parsed_config['City'] = city
        if city not in read_cities():
            raise ConfigValidationException('City', city, 'string', "See city.csv for a list of cities")

    def __parse_user_filter(self):
        parsed_config = {}
        for key, value in self.__filter.items():
            if key not in self.__options:
                raise ConfigValidationException(key, value, f"Unknown key: {key}")
            
            params = self.__options[key]
            type = params.get('type', None)
            allowed = params.get('allowed', None)
            nested_type = params.get('value_type', None)
            self.__validate_value(key, value, type, allowed, nested_type)
            parsed_config[key] = value
        return parsed_config
    
    @property
    def search_filters(self):
        return self.__parsed_config.get('SearchFilter', None)
    
    @property
    def item(self):
        return self.__parsed_config.get('Item', None)
    
    @property
    def city(self):
        return self.__parsed_config.get('City', None)
    
    @property
    def post_content_filters(self):
        return self.__parsed_config.get('PostContentFilter', None)
    
    @property
    def keyword_extraction(self):
        return self.__parsed_config.get('KeywordExtraction', None)
