class ConfigValidationException(Exception):
    def __init__(self, key, value, expected_type, allowed_values=None):
        self.key = key
        self.value = value
        self.expected_type = expected_type
        self.allowed_values = allowed_values

        if self.allowed_values is not None:
            super().__init__(f"Invalid value for {self.key}: {self.value}. Expected type: {self.expected_type}. Allowed values: {self.allowed_values}")
        else:
            super().__init__(f"Invalid value for {self.key}: {self.value}. Expected type: {self.expected_type}")

class InvalidJsonException(Exception):
    def __init__(self, json_file, message):
        self.json_file = json_file
        self.message = message
        super().__init__(f"Invalid JSON file: {self.json_file}. {self.message}")