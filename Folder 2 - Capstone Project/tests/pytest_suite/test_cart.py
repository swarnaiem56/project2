"""
PyTest cart tests — Add to cart, update quantity, verify cart contents.
Covers the full "search -> add to cart -> update quantity -> verify" flow
required by the company scenario.
"""

from pages.search_page import SearchPage
from pages.cart_page import CartPage


def test_add_product_to_cart(driver):
    search_page = SearchPage(driver)
    cart_page = CartPage(driver)

    search_page.search_product("MacBook")
    product_name = search_page.get_first_product_name()
    search_page.add_first_result_to_cart()

    confirmation = search_page.get_add_to_cart_confirmation()
    assert "success" in confirmation.lower() or "added" in confirmation.lower()

    cart_page.open_cart()
    assert cart_page.get_cart_item_count() >= 1
    assert product_name.split()[0] in cart_page.get_first_item_name()


def test_update_cart_quantity(driver):
    search_page = SearchPage(driver)
    cart_page = CartPage(driver)

    search_page.search_product("MacBook")
    search_page.add_first_result_to_cart()

    cart_page.open_cart()
    cart_page.update_quantity("3")

    # After updating, cart should still show the item (not empty)
    assert not cart_page.is_cart_empty()
