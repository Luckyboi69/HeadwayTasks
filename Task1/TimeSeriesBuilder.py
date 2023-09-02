from abc import ABC, abstractmethod
# Abstract builder class
class TimeSeriesBuilder(ABC):
    @abstractmethod
    def add_weekly_seasonality (self):
        pass
    @abstractmethod
    def add_daily_seasonality (self):
        pass
    @abstractmethod
    def add_trend (self):
        pass
    @abstractmethod
    def add_cycles(self):
        pass
    