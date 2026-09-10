from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config_reader import ConfigReader


class LoginPage(BasePage):
    # Locators
    MY_ACCOUNT_DROPDOWN = (By.CSS_SELECTOR, "a.dropdown-toggle[title='My Account']")
    LOGIN_LINK = (By.LINK_TEXT, "Login")
    EMAIL_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input[value='Login']")
    LOGIN_ERROR_ALERT = (By.CSS_SELECTOR, "div.alert-danger")
    # NOTE: "#content h2" alone is NOT a reliable success indicator — OpenCart
    # renders an <h2> on BOTH the login page ("Account Login") and the
    # post-login account page ("My Account"). Using is_displayed() on that
    # generic selector returns True regardless of whether login actually
    # succeeded, which caused a false-positive test earlier in this project.
    # We instead check the URL, since a successful login redirects to a
    # distinct route (account/account) that the login page itself never uses.
    ACCOUNT_PAGE_HEADING = (By.CSS_SELECTOR, "#content h2")
    LOGGED_IN_URL_MARKER = "route=account/account"

    def go_to_login(self):
        self.open(ConfigReader.get_base_url())
        self.click(self.MY_ACCOUNT_DROPDOWN)
        self.click(self.LOGIN_LINK)

    def login(self, email: str, password: str):
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_login_error(self) -> str:
        return self.get_text(self.LOGIN_ERROR_ALERT)

    def is_logged_in(self) -> bool:
        # Wait briefly for the post-login redirect to complete, then check
        # the URL rather than relying on a heading that exists on both
        # the success and failure pages.
        try:
            self.wait.until(lambda d: self.LOGGED_IN_URL_MARKER in d.current_url)
            return True
        except Exception:
            return False