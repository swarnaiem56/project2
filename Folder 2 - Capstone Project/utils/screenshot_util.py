import os
import time

from utils.config_reader import ConfigReader

_PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")


class ScreenshotUtil:
    """Captures a timestamped screenshot whenever a test fails."""

    @staticmethod
    def capture(driver, test_name: str) -> str:
        screenshot_dir = os.path.join(_PROJECT_ROOT, ConfigReader.get_screenshot_dir())
        os.makedirs(screenshot_dir, exist_ok=True)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        safe_name = test_name.replace(" ", "_").replace("::", "_")
        file_path = os.path.join(screenshot_dir, f"{safe_name}_{timestamp}.png")

        driver.save_screenshot(file_path)
        return file_path