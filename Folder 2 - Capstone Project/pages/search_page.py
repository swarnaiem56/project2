from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from utils.config_reader import ConfigReader


class SearchPage(BasePage):
    SEARCH_INPUT = (By.NAME, "search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "#search button")
    PRODUCT_RESULTS = (By.CSS_SELECTOR, ".product-thumb")
    PRODUCT_NAME = (By.CSS_SELECTOR, ".product-thumb h4 a")
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[contains(@onclick, 'cart.add')]")
    SUCCESS_ALERT = (By.CSS_SELECTOR, "div.alert-success")

    def search_product(self, keyword: str):
        self.open(ConfigReader.get_base_url())
        self.type_text(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)

    def get_result_count(self) -> int:
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        return len(self.find_elements_immediate(self.PRODUCT_RESULTS))

    def get_first_product_name(self) -> str:
        return self.get_text(self.PRODUCT_NAME)

    def add_first_result_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)
        # Wait for the AJAX add-to-cart call to actually complete before
        # returning control to the caller. Without this, a caller that
        # navigates away immediately (e.g. straight to the cart page) can
        # race ahead of the server-side add, landing on a still-empty cart.
        self.wait.until(EC.visibility_of_element_located(self.SUCCESS_ALERT))

    def get_add_to_cart_confirmation(self) -> str:
        return self.get_text(self.SUCCESS_ALERT)