from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config_reader import ConfigReader


class CartPage(BasePage):
    CART_ITEM_ROWS = (By.XPATH, "//tr[.//input[starts-with(@name,'quantity[')]]")
    CART_ITEM_NAME = (By.CSS_SELECTOR, "td.text-left a[href*='route=product/product']")
    QUANTITY_INPUT = (By.CSS_SELECTOR, "input[name^='quantity[']")

    def open_cart(self):
        self.open(ConfigReader.get_base_url() + "index.php?route=checkout/cart")

    def get_cart_item_count(self) -> int:
        return len(self.find_elements(self.CART_ITEM_ROWS))

    def get_first_item_name(self) -> str:
        return self.get_text(self.CART_ITEM_NAME)

    def get_first_item_quantity(self) -> str:
        """Quantity lives in the input's value attribute, not visible text."""
        return self.get_attribute(self.QUANTITY_INPUT, "value")