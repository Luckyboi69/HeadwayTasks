from abc import ABC, abstractmethod

class Reader(ABC):
    """
    An abstract base class for readers that provide a method to read attributes.

    Attributes:
        None
    """

    @abstractmethod
    def read_attributes(self,path):
        """
        Abstract method to be implemented by concrete reader classes to read attributes.

        Returns:
            Any: The attributes read by the reader.
        """
        pass
