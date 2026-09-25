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

        # Deliberately NOT setting an implicit wait. Selenium's own docs
        # warn against mixing implicit and explicit waits — it caused a
        # real, subtle bug here: find_elements_immediate() is supposed to
        # return instantly with zero matches, but a nonzero implicit wait
        # silently made it block first, defeating the whole point of that
        # method. Every wait in this framework is explicit (see BasePage).
        return driver