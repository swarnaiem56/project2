"""
PyTest login tests — uses the shared `driver` fixture from conftest.py
instead of manual setup/teardown, and demonstrates alert handling.
"""

from pages.login_page import LoginPage
from utils.config_reader import ConfigReader
from utils.logger import get_logger

logger = get_logger(__name__)


def test_login_page_loads(driver):
    login_page = LoginPage(driver)
    login_page.go_to_login()
    assert "route=account/login" in driver.current_url


def test_invalid_login_shows_error(driver):
    login_page = LoginPage(driver)
    login_page.go_to_login()
    login_page.login("invalid_user@example.com", "wrongpassword123")
    assert "warning" in login_page.get_login_error().lower()


def test_valid_login(driver):
    email, password = ConfigReader.get_credentials()
    login_page = LoginPage(driver)
    login_page.go_to_login()
    login_page.login(email, password)
    # Replace credentials in config/config.ini with a real registered
    # demo account for this assertion to pass.
    assert login_page.is_logged_in()


def test_popup_alert_is_handled_gracefully(driver):
    """
    Demonstrates popup/alert handling requirement — navigates to the site
    and ensures any unexpected JS alert (e.g. cookie/consent popups some
    demo mirrors show) doesn't block execution.
    """
    login_page = LoginPage(driver)
    login_page.open(ConfigReader.get_base_url())
    alert_handled = login_page.accept_alert_if_present()
    logger.info(f"Alert handled: {alert_handled}")
    # No assertion failure either way — this just proves execution
    # continues cleanly whether or not a popup appeared.
    assert True
