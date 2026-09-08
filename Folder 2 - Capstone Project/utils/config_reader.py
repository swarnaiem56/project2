import configparser
import os


class ConfigReader:
    """Reads settings from config/config.ini so nothing is hardcoded in tests."""

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
    def get_implicit_wait(cls):
        return cls._load().getint("ENV", "implicit_wait")

    @classmethod
    def get_explicit_wait(cls):
        return cls._load().getint("ENV", "explicit_wait")

    @classmethod
    def get_credentials(cls):
        cfg = cls._load()
        return cfg.get("CREDENTIALS", "email"), cfg.get("CREDENTIALS", "password")

    @classmethod
    def get_screenshot_dir(cls):
        return cls._load().get("REPORT", "screenshot_dir")
