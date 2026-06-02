# hdd_cdd_calculator/__main__.py
import argparse
import importlib.resources
import tempfile
import shutil
from pathlib import Path

# Set matplotlib backend for headless environments before any other matplotlib import
import matplotlib
matplotlib.use('Agg')

from .data_sources import get_degree_days
from .csv_utils import align_energy_with_degree_days
from .regression import perform_regression
from .visualization import plot_regression


def _find_example_csv() -> Path:
    """
    Locate sample_energy_data.csv whether running from the repo or a pip install.
    Tries repo-relative path first, then falls back to package data.
    """
    # When running from the cloned repo
    repo_csv = Path(__file__).resolve().parent.parent / "examples" / "sample_energy_data.csv"
    if repo_csv.exists():
        return repo_csv

    # When installed via pip — use importlib.resources to find package data
    try:
        # Python 3.9+
        ref = importlib.resources.files("hdd_cdd_calculator").joinpath(
            "../examples/sample_energy_data.csv"
        )
        if ref.is_file():
            return Path(str(ref))
    except (AttributeError, TypeError):
        pass

    raise FileNotFoundError(
        "sample_energy_data.csv not found. "
        "If installed via pip, reinstall with: pip install hdd-cdd-calculator"
    )


def run_example():
    """Run the included example workflow."""
    try:
        example_csv = _find_example_csv()
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        return

    start_date = "2023-06-01"
    end_date = "2023-06-10"
    lat, lon = 40.7128, -74.0060

    print(f"Fetching Open-Meteo data for NYC ({start_date} to {end_date})...")
    dd_results = get_degree_days(
        lat=lat,
        lon=lon,
        start_date=start_date,
        end_date=end_date,
        source="open_meteo",
    )

    if not dd_results:
        print("ERROR: No degree day data returned. Check your network connection.")
        return

    energy_vals, hdd_vals = align_energy_with_degree_days(
        dd_results,
        example_csv,
        energy_column="kwh",
        degree_day_type="hdd",
    )

    model = perform_regression(hdd_vals, energy_vals)
    print(f"Slope: {model.coef_[0]:.2f} | Intercept: {model.intercept_:.2f}")

    # Save plot next to the CSV if possible, else current directory
    plot_dir = example_csv.parent
    plot_path = plot_dir / "regression_plot.png"
    plot_regression(hdd_vals, energy_vals, model, save_path=str(plot_path), show=False)
    print(f"Plot saved to: {plot_path}")


def main():
    """CLI entry point for the HDD/CDD calculator package."""
    parser = argparse.ArgumentParser(description="HDD/CDD Calculator CLI")
    parser.add_argument(
        "--example",
        action="store_true",
        help="Run the package's example workflow",
    )
    args = parser.parse_args()

    if args.example:
        run_example()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
