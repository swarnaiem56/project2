import configparser
import os

from dotenv import load_dotenv

load_dotenv()  # loads variables from a local .env file, if present (gitignored)


class ConfigReader:
    """
    Reads settings from config/config.ini so nothing is hardcoded in tests.
    Credentials are the one exception: those come from environment
    variables via a local .env file instead of config.ini, so they never
    end up committed to git (this fixed a real credential leak I had
    earlier in the project).
    """

    _config = None

    @classmethod
    def _load(cls):
        if cls._config is None:
            cls._config = configparser.ConfigParser()
            config_path = os.path.join(
                os.path.dirname(__file__), "..", "config", "config.ini"
            )
            cls._config.read(config_path)
        return cls._config

    @classmethod
    def get_base_url(cls):
        return cls._load().get("ENV", "base_url")

    @classmethod
    def get_api_base_url(cls):
        return cls._load().get("ENV", "api_base_url")

    @classmethod
    def get_browser(cls):
        return cls._load().get("ENV", "browser")

    @classmethod
    def get_explicit_wait(cls):
        return cls._load().getint("ENV", "explicit_wait")

    @classmethod
    def get_credentials(cls):
        email = os.environ.get("DEMO_SITE_EMAIL")
        password = os.environ.get("DEMO_SITE_PASSWORD")
        if not email or not password:
            raise RuntimeError(
                "DEMO_SITE_EMAIL and DEMO_SITE_PASSWORD must be set in a "
                "local .env file (see .env.example). Credentials are kept "
                "out of config.ini so they never get committed to git."
            )
        return email, password

    @classmethod
    def get_screenshot_dir(cls):
        return cls._load().get("REPORT", "screenshot_dir")