"""
PyTest search tests — data-driven via CSV using @pytest.mark.parametrize.
One row in the CSV covers a genuine zero-result case, so this single
parametrized test demonstrates both outcomes instead of splitting the
zero-result case into a separate hardcoded test.
"""

import pytest

from pages.search_page import SearchPage
from utils.csv_reader import load_csv_data

search_data = load_csv_data("test_data.csv")


@pytest.mark.parametrize(
    "row",
    search_data,
    ids=[row["search_term"] for row in search_data],
)
def test_search_data_driven(driver, row):
    search_page = SearchPage(driver)
    search_page.search_product(row["search_term"])
    result_count = search_page.get_result_count()
    expected_min = int(row["expected_min_results"])

    if expected_min == 0:
        # A minimum of 0 is meaningless with >= (always true), so a
        # genuine zero-result row needs an exact-match assertion instead.
        assert result_count == 0, (
            f"Expected zero results for '{row['search_term']}', "
            f"got {result_count}"
        )
    else:
        assert result_count >= expected_min, (
            f"Expected at least {expected_min} results for "
            f"'{row['search_term']}', got {result_count}"
        )