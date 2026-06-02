"""
HDD/CDD Calculator

A Python library for calculating Heating Degree Days (HDD) and Cooling Degree Days (CDD)
using multiple weather data sources such as:

    - U.S. National Weather Service (NWS) API
    - Meteostat historical data API

The package also includes:
    * Utilities for coordinate validation, temperature conversions, and HDD/CDD calculations
    * CSV utilities for reading and aligning energy consumption data
    * Unified API for selecting a data source
    * Linear regression analysis between degree days and energy consumption
    * Visualization support for regression results
"""

# NWS data source
from .calculator import (
    get_degree_days_for_location,
    get_degree_days_for_period,
    DegreeDaysResult,
)

# Meteostat data source
from .meteostat_api import fetch_meteostat_data

# Unified multi-source access
from .data_sources import get_degree_days

# Regression analysis
from .regression import perform_regression

# Visualization
from .visualization import plot_regression

# CSV utilities
from .csv_utils import (
    read_energy_data_from_csv,
    read_energy_data_with_dates,
    align_energy_with_degree_days,
)

# Utilities
from .utils import (
    validate_coordinates,
    calculate_degree_days,
    fahrenheit_to_celsius,
    celsius_to_fahrenheit,
    mean_temperature,
)

# Exceptions
from .exceptions import (
    NWSAPIError,
    InvalidCoordinatesError,
)

__version__ = "0.1.5"

__all__ = [
    # Core NWS API
    "get_degree_days_for_location",
    "get_degree_days_for_period",

    # Meteostat API
    "fetch_meteostat_data",

    # Unified multi-source API
    "get_degree_days",

    # Regression analysis
    "perform_regression",

    # Visualization
    "plot_regression",

    # CSV utilities
    "read_energy_data_from_csv",
    "read_energy_data_with_dates",
    "align_energy_with_degree_days",

    # Data structures
    "DegreeDaysResult",

    # Utilities
    "validate_coordinates",
    "calculate_degree_days",
    "fahrenheit_to_celsius",
    "celsius_to_fahrenheit",
    "mean_temperature",

    # Exceptions
    "NWSAPIError",
    "InvalidCoordinatesError",
]
