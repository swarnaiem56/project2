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
    ACCOUNT_PAGE_HEADING = (By.CSS_SELECTOR, "#content h2")

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
        return self.is_displayed(self.ACCOUNT_PAGE_HEADING)
