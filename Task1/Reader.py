from abc import ABC, abstractmethod

class Reader(ABC):
    @abstractmethod
    def read_attributes(self):
        pass