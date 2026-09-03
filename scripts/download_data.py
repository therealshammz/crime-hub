#!/usr/bin/env python3
"""
Download Chicago crime data from the City of Chicago Data Portal.

This script downloads the latest crime data from the official Chicago Data Portal
and saves it to the dataset directory.

Usage:
    python scripts/download_data.py [--limit N] [--output PATH]
"""

import argparse
import os
import requests
from pathlib import Path

import pandas as pd  # type: ignore[import-not-found]


# Chicago Data Portal API endpoint
DATA_PORTAL_URL = "https://data.cityofchicago.org/resource/ijzp-q8t2.csv"

# Default output path
DEFAULT_OUTPUT = "dataset/crimes.csv"

# Maximum records to download (None for all)
DEFAULT_LIMIT = None


def download_data(limit: int | None = None, output_path: str = DEFAULT_OUTPUT) -> str:
    """
    Download crime data from Chicago Data Portal.

    Args:
        limit: Maximum number of records to download (None for all)
        output_path: Path to save the CSV file

    Returns:
        Path to the downloaded file
    """
    print(f"Downloading crime data from {DATA_PORTAL_URL}...")

    # Create output directory if it doesn't exist
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build request parameters
    params = {}
    if limit:
        params["$limit"] = limit

    # Download data
    try:
        response = requests.get(DATA_PORTAL_URL, params=params, timeout=300)
        response.raise_for_status()

        # Read CSV data
        from io import StringIO

        df = pd.read_csv(StringIO(response.text))

        # Save to file
        df.to_csv(output_path, index=False)

        print(f"Downloaded {len(df):,} records to {output_path}")
        print(f"File size: {os.path.getsize(output_path) / (1024 * 1024):.2f} MB")

        return output_path

    except requests.exceptions.RequestException as e:
        print(f"Error downloading data: {e}")
        raise
    except Exception as e:
        print(f"Error processing data: {e}")
        raise


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Download Chicago crime data from the City of Chicago Data Portal"
    )
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=None,
        help="Maximum number of records to download (default: all)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=DEFAULT_OUTPUT,
        help=f"Output file path (default: {DEFAULT_OUTPUT})",
    )

    args = parser.parse_args()

    download_data(limit=args.limit, output_path=args.output)


if __name__ == "__main__":
    main()
