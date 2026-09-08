"""
Unittest suite — Product search core scenario.
"""

import unittest

from pages.search_page import SearchPage
from utils.driver_factory import DriverFactory
from utils.screenshot_util import ScreenshotUtil
from utils.logger import get_logger

logger = get_logger(__name__)


class TestSearchUnittest(unittest.TestCase):

    def setUp(self):
        self.driver = DriverFactory.get_driver()
        self.search_page = SearchPage(self.driver)

    def tearDown(self):
        if hasattr(self._outcome, "errors"):
            for _, exc_info in self._outcome.errors:
                if exc_info is not None:
                    ScreenshotUtil.capture(self.driver, self._testMethodName)
        self.driver.quit()

    def test_search_returns_results(self):
        logger.info("Searching for 'MacBook' and verifying results appear")
        self.search_page.search_product("MacBook")
        result_count = self.search_page.get_result_count()
        self.assertGreater(result_count, 0, "Expected at least one search result")

    def test_search_no_results_for_gibberish(self):
        logger.info("Searching for a nonsense term and verifying zero results")
        self.search_page.search_product("zzzxxxnonexistentproduct123")
        result_count = self.search_page.get_result_count()
        self.assertEqual(result_count, 0)


if __name__ == "__main__":
    unittest.main()
