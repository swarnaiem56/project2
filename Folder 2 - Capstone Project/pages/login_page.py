from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config_reader import ConfigReader


class LoginPage(BasePage):
    EMAIL_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input[value='Login']")
    LOGIN_ERROR_ALERT = (By.CSS_SELECTOR, "div.alert-danger")
    # A successful login redirects to a distinct URL (account/account).
    # I originally checked for an <h2> heading instead, but OpenCart renders
    # an <h2> on BOTH the login page ("Account Login") AND the post-login
    # account page ("My Account") — so that check returned True even with
    # wrong credentials. Checking the URL fixed the false positive.
    LOGGED_IN_URL_MARKER = "route=account/account"

    def go_to_login(self):
        # Navigates directly to the login URL instead of clicking through
        # the "My Account" dropdown menu. Same destination, one less
        # unnecessary UI interaction (and one less thing that can flake).
        self.open(ConfigReader.get_base_url() + "index.php?route=account/login")

    def login(self, email: str, password: str):
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_login_error(self) -> str:
        return self.get_text(self.LOGIN_ERROR_ALERT)

    def is_logged_in(self) -> bool:
        try:
            self.wait.until(lambda d: self.LOGGED_IN_URL_MARKER in d.current_url)
            return True
        except Exception:
            return False