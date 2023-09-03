from Reader import Reader
import yaml

class YAMLReader(Reader):
    def read_attributes(self, file_path):
        try:
            with open(file_path, 'r') as yaml_file:
                attributes = yaml.safe_load(yaml_file)
            return attributes
        except Exception as e:
            print(f"Error reading YAML file: {str(e)}")
            return {}
