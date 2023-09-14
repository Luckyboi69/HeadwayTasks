from abc import ABC, abstractmethod

class Producer(ABC):
    """
    An abstract base class for producers that define methods for saving files and metadata.

    Attributes:
        None
    """

    @abstractmethod
    def save_file(self):
        """
        Abstract method to be implemented by concrete producer classes for saving files.

        Returns:
            bool: True if the file is successfully saved, False otherwise.
        """
        pass

    @abstractmethod
    def save_meta_data(self):
        """
        Abstract method to be implemented by concrete producer classes for saving metadata.

        Returns:
            bool: True if the metadata is successfully saved, False otherwise.
        """
        pass
