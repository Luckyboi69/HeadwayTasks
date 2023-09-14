from Reader import Reader
import yaml

class YAMLReader(Reader):
    """
    A concrete reader class for reading attributes from a YAML file.

    Attributes:
        None
    """

    def read_attributes(self, file_path):
        """
        Read attributes from a YAML file.

        Args:
            file_path (str): The path to the YAML file containing attributes.

        Returns:
            dict: A dictionary containing the read attributes.
        """
        try:
            with open(file_path, 'r') as yaml_file:
                attributes = yaml.safe_load(yaml_file)
            return attributes
        except Exception as e:
            print(f"Error reading YAML file: {str(e)}")
            return {}
