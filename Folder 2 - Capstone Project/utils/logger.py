import logging
import os

_PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")
_REPORTS_DIR = os.path.join(_PROJECT_ROOT, "reports")


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # avoid duplicate handlers on repeated calls

    logger.setLevel(logging.INFO)
    os.makedirs(_REPORTS_DIR, exist_ok=True)

    file_handler = logging.FileHandler(os.path.join(_REPORTS_DIR, "execution.log"))
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger