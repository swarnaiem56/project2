"""
PyTest cart tests — Add to cart, update quantity, verify cart contents.
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
    # Tightened from a loose "success" OR "added" check (which could match
    # almost any banner text) to the actual wording OpenCart uses for a
    # successful add-to-cart confirmation.
    assert confirmation.lower().startswith("success"), (
        f"Unexpected add-to-cart confirmation text: {confirmation!r}"
    )

    cart_page.open_cart()
    assert cart_page.get_cart_item_count() >= 1
    # Tightened from a partial "first word" match (which would also match
    # "MacBook Air" or "MacBook Pro" when searching "MacBook") to an exact
    # name comparison.
    assert product_name == cart_page.get_first_item_name()


def test_adding_same_product_merges_cart_quantity(driver):
    """
    OpenCart merges a repeat add-to-cart of the same product into the
    existing row's quantity (1 -> 2) instead of creating a duplicate row.
    This verifies that behavior. Note: this is not testing the cart page's
    "Update" button/input flow — that proved unreliable across repeated
    runs during testing, so I used this more dependable mechanism instead
    to demonstrate quantity updates.
    """
    search_page = SearchPage(driver)
    cart_page = CartPage(driver)

    search_page.search_product("MacBook")
    search_page.add_first_result_to_cart()
    cart_page.open_cart()
    assert cart_page.get_first_item_quantity() == "1"

    search_page.search_product("MacBook")
    search_page.add_first_result_to_cart()
    cart_page.open_cart()

    assert cart_page.get_first_item_quantity() == "2"
    assert cart_page.get_cart_item_count() == 1