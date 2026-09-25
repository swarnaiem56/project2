import csv
import os


def load_csv_data(filename: str):
    """
    Reads a CSV file from the project's data/ folder and returns a list of
    dicts, one per row — used to feed @pytest.mark.parametrize for
    data-driven tests.
    """
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", filename)
    with open(data_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))