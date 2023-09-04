from abc import ABC, abstractmethod

class Producer(ABC):
    @abstractmethod
    def save_file(self):
        pass
    def save_meta_data(self):
        pass