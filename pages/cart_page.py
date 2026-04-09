from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        
        # 🔹 Локаторы
        self.cart_items = page.locator(".cart_item")
        self.checkout_btn = page.locator("#checkout")
        self.continue_shopping_btn = page.locator("#continue-shopping")

    @property
    def items_count(self) -> int:
        return self.cart_items.count()

    def get_item_locator(self, product_name: str) -> Locator:
        """Возвращает локатор товара в корзине"""
        return self.page.locator(f".cart_item:has-text('{product_name}')")

    def get_item_price(self, product_name: str) -> str:
        """Возвращает цену товара в корзине"""
        return self.get_item_locator(product_name).locator(".inventory_item_price").text_content().strip()

    def remove_item(self, product_name: str):
        """Удаляет товар из корзины"""
        remove_btn = self.get_item_locator(product_name).locator("button[id^='remove']")
        remove_btn.click()
        return self

    def proceed_to_checkout(self) -> "CheckoutStepOnePage":
        """Переходит к чекауту"""
        from pages.checkout_page import CheckoutStepOnePage
        self.checkout_btn.tap()  # 📱 Mobile: tap
        return CheckoutStepOnePage(self.page)

    def continue_shopping(self) -> "InventoryPage":
        """Возвращается к покупкам"""
        self.continue_shopping_btn.click()
        return InventoryPage(self.page)