from django.db import models

class SimulatorDetail(models.Model):
    """
    Model representing a simulator detail.

    Attributes:
        status (str): The status of the simulator, chosen from STATUS_CHOICES.
        start_date (Date): The start date of the simulator.
        end_date (Date): The end date of the simulator.
        name (str): The name of the simulator.
        time_series_type (str): The type of time series, chosen from TIME_SERIES_TYPES.
        producer_type (str): The type of producer, chosen from PRODUCER_TYPES.
        process_id (str): The process ID associated with the simulator.

    Methods:
        __str__(): Returns a string representation of the simulator's name.
    """    
    
    TIME_SERIES_TYPES = (
        ('multiplicative', 'Multiplicative'),
        ('additive', 'Additive'),
    )

    PRODUCER_TYPES = (
        ('Kafka', 'Kafka'),
        ('folder', 'CSV File'),
    )
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('running', 'Running'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='submitted')
    start_date = models.DateField()
    end_date = models.DateField()
    name = models.CharField(max_length=255)
    time_series_type = models.CharField(max_length=20, choices=TIME_SERIES_TYPES)
    producer_type = models.CharField(max_length=20, choices=PRODUCER_TYPES)
    process_id = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class DatasetConfiguration(models.Model):
    """
    Model representing a dataset configuration.

    Attributes:
        frequency (str): The frequency of the dataset.
        noise_level (str): The noise level of the dataset.
        trend_coefficients (str): The trend coefficients of the dataset.
        missing_percentage (float): The percentage of missing data.
        outlier_percentage (float): The percentage of outliers.
        cycle_component_frequency (float): The frequency of cycle components.
        status (str): The status of the dataset configuration, chosen from STATUS_CHOICES.
        time_series (ForeignKey): A foreign key to the associated SimulatorDetail.

    Meta:
        unique_together: Ensures uniqueness based on a combination of fields.

    Methods:
        __str__(): Returns a string representation of the configuration.
    """
    STATUS_CHOICES = (
        ('Submitted', 'Submitted'),
        ('Running', 'Running'),
        ('Succeeded', 'Succeeded'),
        ('Failed', 'Failed'),
    )

    frequency = models.CharField(max_length=10)
    noise_level = models.CharField(max_length=10)
    trend_coefficients = models.CharField(max_length=255, default="0")
    missing_percentage = models.FloatField(default=0)
    outlier_percentage = models.FloatField(default=0)
    cycle_component_frequency = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    time_series = models.ForeignKey(SimulatorDetail, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('time_series', 'frequency', 'noise_level', 'trend_coefficients',
                           'missing_percentage', 'outlier_percentage',
                           'cycle_component_frequency')

    def __str__(self):
        return f"Configuration for {self.time_series.name} ({self.frequency})"

class SeasonalityComponent(models.Model):
    """
    Model representing a seasonality component.

    Attributes:
        amplitude (float): The amplitude of the seasonality component.
        phase_shift (float): The phase shift of the seasonality component.
        frequency_type (str): The frequency type, chosen from FREQUENCY_TYPES.
        frequency_multiplier (float): The frequency multiplier of the seasonality component.
        dataset_configuration (ForeignKey): A foreign key to the associated DatasetConfiguration.

    Methods:
        __str__(): Returns a string representation of the seasonality component.
    """
    
    FREQUENCY_TYPES = (
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
    )

    amplitude = models.FloatField()
    phase_shift = models.FloatField()
    frequency_type = models.CharField(max_length=10, choices=FREQUENCY_TYPES)
    frequency_multiplier = models.FloatField()
    dataset_configuration = models.ForeignKey(DatasetConfiguration, on_delete=models.CASCADE)

    def __str__(self):
        return f"Seasonality Component for {self.dataset_configuration}"
