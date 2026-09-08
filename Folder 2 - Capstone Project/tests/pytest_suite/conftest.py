"""
Shared PyTest fixtures for the UI suite:
- `driver` fixture handles browser setup/teardown for every test automatically
- `pytest_runtest_makereport` hook captures a screenshot the moment a test fails,
  without needing any explicit try/except in each test
"""

import csv
import os

import pytest

from utils.driver_factory import DriverFactory
from utils.screenshot_util import ScreenshotUtil
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture
def driver():
    logger.info("Setting up WebDriver for test")
    drv = DriverFactory.get_driver()
    yield drv
    logger.info("Tearing down WebDriver")
    drv.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Runs after every test phase; captures a screenshot if the call phase failed."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver is not None:
            path = ScreenshotUtil.capture(driver, item.name)
            logger.info(f"Screenshot captured on failure: {path}")


def load_csv_data(filename: str):
    """Reads test_data.csv and returns a list of dicts for use with @pytest.mark.parametrize."""
    data_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "data", filename
    )
    with open(data_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
