from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config_reader import ConfigReader


class SearchPage(BasePage):
    SEARCH_INPUT = (By.NAME, "search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "#search button")
    PRODUCT_RESULTS = (By.CSS_SELECTOR, ".product-thumb")
    PRODUCT_NAME = (By.CSS_SELECTOR, ".product-thumb h4 a")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button[data-original-title='Add to Cart']")
    SUCCESS_ALERT = (By.CSS_SELECTOR, "div.alert-success")

    def search_product(self, keyword: str):
        self.open(ConfigReader.get_base_url())
        self.type_text(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)

    def get_result_count(self) -> int:
        return len(self.find_elements(self.PRODUCT_RESULTS))

    def get_first_product_name(self) -> str:
        return self.get_text(self.PRODUCT_NAME)

    def add_first_result_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)

    def get_add_to_cart_confirmation(self) -> str:
        return self.get_text(self.SUCCESS_ALERT)
