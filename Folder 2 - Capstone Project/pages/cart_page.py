from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config_reader import ConfigReader


class CartPage(BasePage):
    CART_LINK = (By.CSS_SELECTOR, "#header-cart a")
    # NOTE: "table.table tbody tr" is too broad — this theme reuses the
    # "table" class elsewhere on the page (coupon/gift certificate forms,
    # etc.), inflating the count. Scoped instead to rows that actually
    # contain a quantity input, which only genuine product rows have.
    CART_ITEM_ROWS = (By.XPATH, "//tr[.//input[starts-with(@name,'quantity[')]]")

    # Restricted to the "text-left" column specifically (the name column) —
    # a bare href-pattern match also catches the thumbnail image's <a> tag
    # in the "text-center" column, which has no text.
    CART_ITEM_NAME = (By.CSS_SELECTOR, "td.text-left a[href*='route=product/product']")

    # Confirmed via "View Page Source" on the live cart page. Real markup:
    #   <input type="text" name="quantity[390986]" value="1" ... />
    #   <button title="Remove" onclick="cart.remove('390986');" ...>...
    QUANTITY_INPUT = (By.CSS_SELECTOR, "input[name^='quantity[']")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button[title='Remove']")
    SUCCESS_ALERT = (By.CSS_SELECTOR, "div.alert-success")

    CART_TOTAL = (By.CSS_SELECTOR, "tr.text-right td:last-child")
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, "#content p")

    def open_cart(self):
        self.open(ConfigReader.get_base_url() + "index.php?route=checkout/cart")

    def get_cart_item_count(self) -> int:
        return len(self.find_elements(self.CART_ITEM_ROWS))

    def get_first_item_name(self) -> str:
        return self.get_text(self.CART_ITEM_NAME)

    def get_first_item_quantity(self) -> str:
        """Quantity lives in the input's value attribute, not visible text."""
        return self.get_attribute(self.QUANTITY_INPUT, "value")

    def is_cart_empty(self) -> bool:
        return "empty" in self.get_text(self.EMPTY_CART_MESSAGE).lower()