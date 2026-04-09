from pages.base_page import BasePage

class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.checkout_btn = page.locator("#checkout")
        self.cart_items = page.locator(".cart_item")

    @property
    def items_count(self) -> int:
        return self.cart_items.count()

    def get_item_price(self, product_name: str) -> str:
        return self.page.locator(
            f".inventory_item:has-text('{product_name}') .inventory_item_price"
        ).text_content()

    def proceed_to_checkout(self) -> "CheckoutStepOnePage":
        from pages.checkout_page import CheckoutStepOnePage
        self.checkout_btn.click()
        return CheckoutStepOnePage(self.page)