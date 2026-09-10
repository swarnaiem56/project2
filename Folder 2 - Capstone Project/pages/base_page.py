from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.config_reader import ConfigReader
from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    """
    Common actions shared by every page object.

    IMPORTANT DESIGN NOTE: the target site's theme renders duplicate DOM
    elements for responsive layouts (a hidden mobile/desktop variant
    alongside the visible one), matching the exact same locator. Standard
    Selenium waits like visibility_of_element_located / element_to_be_clickable
    only ever look at the FIRST element a locator matches — if that happens
    to be the hidden copy, they hang for the full timeout even though a
    second, visible match exists a moment later in the DOM. Every method
    below scans ALL matches and acts on the first one that's genuinely
    visible (and enabled, for clicks/typing), instead of trusting DOM order.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, ConfigReader.get_explicit_wait())

    def open(self, url: str):
        logger.info(f"Navigating to {url}")
        self.driver.get(url)

    def _first_visible(self, locator):
        def _condition(d):
            for el in d.find_elements(*locator):
                if el.is_displayed():
                    return el
            return False
        return self.wait.until(_condition)

    def _first_clickable(self, locator):
        def _condition(d):
            for el in d.find_elements(*locator):
                if el.is_displayed() and el.is_enabled():
                    return el
            return False
        return self.wait.until(_condition)

    def click(self, locator):
        self._first_clickable(locator).click()

    def type_text(self, locator, text: str):
        element = self._first_clickable(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator) -> str:
        return self._first_visible(locator).text

    def get_attribute(self, locator, attribute: str) -> str:
        return self._first_visible(locator).get_attribute(attribute)

    def is_displayed(self, locator) -> bool:
        try:
            return self._first_visible(locator).is_displayed()
        except Exception:
            return False

    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def find_elements_immediate(self, locator):
        """
        Returns whatever matches RIGHT NOW, without waiting for at least one
        to exist. Use this when zero matches is a legitimate outcome (e.g.
        counting search results for a term with no matches) — a "wait for
        presence" condition can't distinguish "not loaded yet" from
        "genuinely zero," so it would otherwise wait the full timeout and
        raise TimeoutException. Only safe to call after the page has
        already finished loading.
        """
        return self.driver.find_elements(*locator)

    def accept_alert_if_present(self):
        """Handles unexpected JS alerts/popups gracefully instead of letting them block execution."""
        try:
            alert = self.driver.switch_to.alert
            logger.info(f"Alert detected: {alert.text}")
            alert.accept()
            return True
        except Exception:
            return False