import unittest
from YAMLReader import YAMLReader


class TestYAMLReader(unittest.TestCase):

    def test_read_attributes(self):
        # Create an instance of YAMLReader
        yaml_reader = YAMLReader()

        # Define a sample YAML file content
        yaml_content = """
        key1: value1
        key2: value2
        """

        # Create a temporary YAML file with the sample content
        with open('test_yaml_file.yaml', 'w') as temp_file:
            temp_file.write(yaml_content)

        # Read attributes from the temporary file
        attributes = yaml_reader.read_attributes('test_yaml_file.yaml')

        # Verify the result
        expected_attributes = {'key1': 'value1', 'key2': 'value2'}
        self.assertEqual(attributes, expected_attributes)
