from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config_reader import ConfigReader


class CartPage(BasePage):
    CART_LINK = (By.CSS_SELECTOR, "#header-cart a")
    CART_ITEM_ROWS = (By.CSS_SELECTOR, "table.table tbody tr")
    CART_ITEM_NAME = (By.CSS_SELECTOR, "td.text-left a")
    QUANTITY_INPUT = (By.CSS_SELECTOR, "td.text-center input.form-control")
    UPDATE_BUTTON = (By.CSS_SELECTOR, "button[data-original-title='Update']")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button[data-original-title='Remove']")
    CART_TOTAL = (By.CSS_SELECTOR, "tr.text-right td:last-child")
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, "#content p")

    def open_cart(self):
        self.open(ConfigReader.get_base_url() + "index.php?route=checkout/cart")

    def get_cart_item_count(self) -> int:
        return len(self.find_elements(self.CART_ITEM_ROWS))

    def get_first_item_name(self) -> str:
        return self.get_text(self.CART_ITEM_NAME)

    def update_quantity(self, quantity: str):
        self.type_text(self.QUANTITY_INPUT, quantity)
        self.click(self.UPDATE_BUTTON)

    def is_cart_empty(self) -> bool:
        return "empty" in self.get_text(self.EMPTY_CART_MESSAGE).lower()
