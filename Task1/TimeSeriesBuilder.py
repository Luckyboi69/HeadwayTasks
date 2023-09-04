from abc import ABC, abstractmethod

class TimeSeriesBuilder(ABC):
    """
    An abstract builder class for creating time series data.

    Attributes:
        None
    """

    @abstractmethod
    def add_weekly_seasonality(self):
        """
        Add a weekly seasonality component to the time series data.

        Returns:
            pd.Series: A pandas Series representing the weekly seasonality component.
        """
        pass

    @abstractmethod
    def add_daily_seasonality(self):
        """
        Add a daily seasonality component to the time series data.

        Returns:
            pd.Series: A pandas Series representing the daily seasonality component.
        """
        pass

    @abstractmethod
    def add_trend(self):
        """
        Add a trend component to the time series data.

        Returns:
            pd.Series: A pandas Series representing the trend component.
        """
        pass

    @abstractmethod
    def add_cycles(self):
        """
        Add a cyclic component to the time series data.

        Returns:
            float: The cyclic component value.
        """
        pass
