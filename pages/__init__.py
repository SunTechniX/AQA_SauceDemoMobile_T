# student_template/pages/__init__.py
"""
Page Objects для проекта SauceDemo Playwright
"""

from .base_page import BasePage
from .login_page import LoginPage
from .inventory_page import InventoryPage
from .cart_page import CartPage
from .checkout_page import CheckoutPage

__all__ = [
    "BasePage",
    "LoginPage",
    "InventoryPage",
    "CartPage",
    "CheckoutPage"
]