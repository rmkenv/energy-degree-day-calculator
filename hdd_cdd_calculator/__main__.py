# hdd_cdd_calculator/__main__.py
import argparse
from pathlib import Path

# Set matplotlib backend for headless environments
import matplotlib
matplotlib.use('Agg')

from .data_sources import get_degree_days
from .csv_utils import align_energy_with_degree_days
from .regression import perform_regression
from .visualization import plot_regression


def run_example():
    """Run the included example workflow."""
    example_csv = Path(__file__).resolve().parent.parent / "examples" / "sample_energy_data.csv"

    if not example_csv.exists():
        print(f"ERROR: Sample CSV not found at {example_csv}")
        return

    # Matching date range for our example CSV
    start_date = "2023-06-01"
    end_date = "2023-06-10"
    lat, lon = 40.7128, -74.0060

    # Step 1: Fetch HDD data using Meteostat for historical data
    dd_results = get_degree_days(
        lat=lat,
        lon=lon,
        start_date=start_date,
        end_date=end_date,
        source="open_meteo"
    )

    # Step 2: Align CSV data with HDD results
    energy_vals, hdd_vals = align_energy_with_degree_days(
        dd_results,
        example_csv,
        energy_column="kwh",
        degree_day_type="hdd"
    )

    # Step 3: Perform regression
    model = perform_regression(hdd_vals, energy_vals)
    print(f"Slope: {model.coef_[0]:.2f} | Intercept: {model.intercept_:.2f}")

    # Step 4: Plot results
    plot_path = Path(__file__).resolve().parent.parent / "examples" / "regression_plot.png"
    plot_regression(
        hdd_vals,
        energy_vals,
        model,
        save_path=plot_path,
        show=False
    )
    print(f"Plot saved to: {plot_path}")


def main():
    """CLI entry point for the HDD/CDD calculator package."""
    parser = argparse.ArgumentParser(description="HDD/CDD Calculator CLI")
    parser.add_argument(
        "--example",
        action="store_true",
        help="Run the package's example workflow"
    )
    args = parser.parse_args()

    if args.example:
        run_example()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
