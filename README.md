# HDD/CDD Calculator

[![PyPI version](https://img.shields.io/pypi/v/hdd-cdd-calculator)](https://pypi.org/project/hdd-cdd-calculator)
[![Python versions](https://img.shields.io/pypi/pyversions/hdd-cdd-calculator)](https://pypi.org/project/hdd-cdd-calculator)

A Python library for calculating **Heating Degree Days (HDD)** and **Cooling Degree Days (CDD)** from multiple weather data sources, including:

- **U.S. National Weather Service (NWS) API** — forecast data
- **Open-Meteo** — free, global historical weather data (no API key required)

This package is designed primarily for **energy managers and sustainability professionals** who need to:

- Understand how outdoor weather influences **energy efficiency**
- **Forecast** energy usage based on HDD/CDD trends
- Integrate weather-normalized analysis into energy reporting, benchmarking, and decision-making

It's suitable for both quick exploratory analyses and production workflows.

The package also supports:
- Automated alignment of energy usage CSV data with degree days
- Linear regression analysis between degree days and energy consumption
- Visualization of regression results
- An **included example dataset** for quick testing
- A **CLI** to run the full workflow and save the plot

***

## ⚠️ Important Notes on Data Quality & Limitations

For energy efficiency analysis and forecasting, the quality of your weather data matters. Be aware of:

- **Missing or Low-Quality In Situ Data**
  Some station datasets may have missing data or poor quality control (QC). Gaps or extreme values can bias results.

- **Limitations of Gridded Weather Data**
  Reanalysis datasets (e.g., ERA5, which Open-Meteo draws from) are not always direct substitutes for local station observations and can be biased in some regions.

Understanding these factors helps you choose the right source and interpret results realistically.

For a deeper discussion of these issues in engineering contexts, see:
*"On the Use of Observed and Gridded Weather Data in Energy Analysis" — ESS Open Archive*
[https://essopenarchive.org/doi/full/10.22541/essoar.175130623.32640121/v1](https://essopenarchive.org/doi/full/10.22541/essoar.175130623.32640121/v1)

***

## ✨ Features

- U.S.-focused but works globally via Open-Meteo
- Calculate HDD/CDD for any lat/lon with a custom base temperature
- Retrieve data for arbitrary date ranges (historical or recent)
- Two data sources: NWS (U.S. forecast) & Open-Meteo (global historical)
- No API key required for either source
- CSV utilities for loading & aligning energy consumption data
- Linear regression between HDD/CDD and energy usage
- Matplotlib visualizations
- Example dataset & CLI for end-to-end workflow
- Clear error handling & type hints
- PyPI-ready packaging

***

## 📦 Installation

From PyPI:
```bash
pip install hdd-cdd-calculator
```

Optional extras:
```bash
pip install hdd-cdd-calculator[dev]   # development tools
pip install hdd-cdd-calculator[viz]   # plotting support
```

From source:
```bash
git clone https://github.com/rmkenv/hdd_cdd_calculator.git
cd hdd_cdd_calculator
pip install -e .[dev]
```

***

## 🚀 Basic Usage

### NWS Data Source (U.S. forecast, ~7-day window)
```python
from hdd_cdd_calculator import get_degree_days

results = get_degree_days(
    lat=38.8977,
    lon=-77.0365,
    start_date="2024-06-01",
    end_date="2024-06-07",
    source="nws"
)
```

### Open-Meteo Data Source (global historical, any date range)
```python
from hdd_cdd_calculator import get_degree_days

results = get_degree_days(
    lat=40.7128,
    lon=-74.0060,
    start_date="2023-06-01",
    end_date="2023-06-30",
    source="open_meteo"
)

for r in results:
    print(r.date, r.high_temp, r.low_temp, r.hdd, r.cdd)
```

All temperatures are returned in **°F**. The default base temperature is **65°F**.

***

## 📂 Working with Energy CSVs

Align internal usage data with HDD/CDD for regression and forecasting.

Expected CSV headers:
```
date,kwh,mmbtu,gal
```

Example — full regression workflow:
```python
from hdd_cdd_calculator import (
    get_degree_days,
    align_energy_with_degree_days,
    perform_regression,
    plot_regression,
)

dd_results = get_degree_days(
    lat=40.7128,
    lon=-74.0060,
    start_date="2023-06-01",
    end_date="2023-06-30",
    source="open_meteo",
)

energy_vals, hdd_vals = align_energy_with_degree_days(
    dd_results,
    "my_energy_data.csv",
    energy_column="kwh",
    degree_day_type="hdd",
)

model = perform_regression(hdd_vals, energy_vals)
print(f"Slope: {model.coef_[0]:.2f} | Intercept: {model.intercept_:.2f}")

plot_regression(hdd_vals, energy_vals, model, save_path="regression_plot.png")
```

***

## ⚡ Quick Try (Example Dataset)

Run the built-in NYC June 2023 example end-to-end:

```bash
python -m hdd_cdd_calculator --example
```

Runs an HDD correlation against a sample building energy CSV and saves a regression plot to `examples/regression_plot.png`.

***

## 📖 API Reference

| Function | Description |
|---|---|
| `get_degree_days(lat, lon, start_date, end_date, source, base_temp)` | Unified entry point — returns HDD/CDD for a date range from either source |
| `get_degree_days_for_location(lat, lon, base_temp)` | NWS source: degree days for the next ~7 days |
| `get_degree_days_for_period(lat, lon, start_date, end_date, base_temp)` | NWS source: filtered to a date range |
| `fetch_meteostat_data(lat, lon, start_date, end_date, base_temp)` | Open-Meteo source: historical degree days |
| `align_energy_with_degree_days(dd_results, csv_path, ...)` | Aligns a CSV of energy readings with degree day results |
| `perform_regression(x, y)` | Linear regression between degree days and energy |
| `plot_regression(x, y, model, ...)` | Matplotlib scatter + regression line |
| `calculate_degree_days(high, low, base_temp, unit)` | Low-level HDD/CDD calculation from a single day's temps |
| `validate_coordinates(lat, lon)` | Validates and rounds coordinates |
| `celsius_to_fahrenheit(c)` / `fahrenheit_to_celsius(f)` | Unit conversion helpers |

### Data Source Options

| `source=` | Coverage | Date Range | API Key |
|---|---|---|---|
| `"nws"` | U.S. only | Forecast (~7 days) | None |
| `"open_meteo"` | Global | Historical (1940–present) | None |

***

## 🧪 Development

```bash
git clone https://github.com/rmkenv/hdd_cdd_calculator.git
cd hdd_cdd_calculator
pip install -e .[dev]
pytest
```

***

## 🔍 Use Cases

- Weather-normalized evaluation of building energy consumption
- Forecasting heating and cooling energy demand from degree day trends
- Energy efficiency reporting and benchmarking
- Identifying changes in energy performance relative to outdoor temperature
- Integrating degree day analysis into sustainability goals and compliance tracking
- Modeling energy consumption sensitivity to temperature for operational planning

***

## 📜 License

MIT License — see [LICENSE](LICENSE).
**Author:** Ryan Kmetz
