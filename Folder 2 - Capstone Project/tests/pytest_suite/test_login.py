"""
PyTest login tests — uses the shared `driver` fixture from conftest.py.
Invalid-login cases are CSV-driven via parametrize, same pattern as search.
"""

import pytest

from pages.login_page import LoginPage
from utils.config_reader import ConfigReader
from utils.csv_reader import load_csv_data
from utils.logger import get_logger

logger = get_logger(__name__)

invalid_login_data = load_csv_data("login_data.csv")


def test_login_page_loads(driver):
    login_page = LoginPage(driver)
    login_page.go_to_login()
    assert "route=account/login" in driver.current_url


@pytest.mark.parametrize(
    "row",
    invalid_login_data,
    ids=[row["email"] for row in invalid_login_data],
)
def test_invalid_login_shows_error(driver, row):
    login_page = LoginPage(driver)
    login_page.go_to_login()
    login_page.login(row["email"], row["password"])
    assert "warning" in login_page.get_login_error().lower()


def test_valid_login(driver):
    email, password = ConfigReader.get_credentials()
    login_page = LoginPage(driver)
    login_page.go_to_login()
    login_page.login(email, password)
    assert login_page.is_logged_in()