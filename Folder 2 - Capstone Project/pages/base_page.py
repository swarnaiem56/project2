from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.config_reader import ConfigReader
from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    """
    Common actions shared by every page object. Individual page classes
    inherit from this instead of repeating find/click/type/wait logic.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, ConfigReader.get_explicit_wait())

    def open(self, url: str):
        logger.info(f"Navigating to {url}")
        self.driver.get(url)

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def type_text(self, locator, text: str):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def get_text(self, locator) -> str:
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.text

    def is_displayed(self, locator) -> bool:
        try:
            return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except Exception:
            return False

    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def accept_alert_if_present(self):
        """Handles unexpected JS alerts/popups gracefully instead of letting them block execution."""
        try:
            alert = self.driver.switch_to.alert
            logger.info(f"Alert detected: {alert.text}")
            alert.accept()
            return True
        except Exception:
            return False
