from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from utils.config_reader import ConfigReader


class DriverFactory:
    """Centralizes browser/driver creation so tests never instantiate WebDriver directly."""

    @staticmethod
    def get_driver():
        browser = ConfigReader.get_browser().lower()

        if browser == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            # Uncomment for headless CI runs:
            # options.add_argument("--headless=new")
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options,
            )
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        driver.implicitly_wait(ConfigReader.get_implicit_wait())
        return driver
