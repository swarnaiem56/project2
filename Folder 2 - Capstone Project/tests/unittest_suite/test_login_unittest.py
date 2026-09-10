"""
Unittest suite — core fundamentals demonstration.
Uses setUp/tearDown for browser lifecycle and standard assert* methods.
Company requirement: demonstrate Unittest alongside PyTest.
"""

import unittest

from pages.login_page import LoginPage
from utils.driver_factory import DriverFactory
from utils.config_reader import ConfigReader
from utils.screenshot_util import ScreenshotUtil
from utils.logger import get_logger

logger = get_logger(__name__)


class TestLoginUnittest(unittest.TestCase):

    def setUp(self):
        self.driver = DriverFactory.get_driver()
        self.login_page = LoginPage(self.driver)

    def tearDown(self):
        # Capture a screenshot automatically if the test failed
        if hasattr(self._outcome, "errors"):
            for _, exc_info in self._outcome.errors:
                if exc_info is not None:
                    ScreenshotUtil.capture(self.driver, self._testMethodName)
        self.driver.quit()

    def test_login_page_loads(self):
        logger.info("Verifying login page loads correctly")
        self.login_page.go_to_login()
        self.assertIn(
            "route=account/login",
            self.driver.current_url,
            "Login page did not load as expected",
        )

    def test_invalid_login_shows_error(self):
        logger.info("Verifying invalid credentials show an error message")
        self.login_page.go_to_login()
        self.login_page.login("invalid_user@example.com", "wrongpassword123")
        error_text = self.login_page.get_login_error()
        self.assertIn("warning", error_text.lower())

    def test_valid_login(self):
        logger.info("Verifying valid login succeeds")
        email, password = ConfigReader.get_credentials()
        self.login_page.go_to_login()
        self.login_page.login(email, password)
        # NOTE: replace credentials in config/config.ini with a real
        # registered account on the demo site for this test to pass.
        self.assertTrue(self.login_page.is_logged_in())


if __name__ == "__main__":
    unittest.main()
