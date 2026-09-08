"""
PyTest search tests — data-driven via CSV using @pytest.mark.parametrize.
This is the clearest demonstration of "same test logic, many data sets."
"""

import pytest

from pages.search_page import SearchPage
from .conftest import load_csv_data

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
    assert result_count >= int(row["expected_min_results"]), (
        f"Expected at least {row['expected_min_results']} results for "
        f"'{row['search_term']}', got {result_count}"
    )


def test_search_no_results_for_gibberish(driver):
    search_page = SearchPage(driver)
    search_page.search_product("zzzxxxnonexistentproduct123")
    assert search_page.get_result_count() == 0
