import json
import os

class EnvironmentManager:
    def __init__(self, json_file=f'resources/user_config.json'):
        """Initialize the EnvironmentManager with a given JSON file."""
        self.json_file = json_file

    def load_data(self):
        """Loads data from the JSON file if it exists, returns an empty dictionary if not."""
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as f:
                return json.load(f)
        return {}

    def save_data(self, data):
        try:
            with open(self.json_file, 'r') as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = {}

        existing_data.update(data)

        with open(self.json_file, 'w') as f:
            json.dump(existing_data, f, indent=4)

    def get(self, key):
        """Returns the value of the variable by key, or None if the key doesn't exist."""
        data = self.load_data()
        return data.get(key, None)

    def set(self, key, value):
        """Sets or updates a variable with a given key and value."""
        data = self.load_data()
        data[key] = value
        self.save_data(data)

# Example usage
EnvironmentManager(f'resources/user_config.json').get('default_directory')
