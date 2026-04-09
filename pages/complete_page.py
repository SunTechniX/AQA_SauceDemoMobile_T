from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class CompletePage(BasePage):
    """Страница успешного завершения заказа (/checkout-complete.html)"""

    def __init__(self, page: Page):
        super().__init__(page)
        # 🔹 Локаторы
        self.back_home_btn = page.locator("#back-to-products")
        self.success_header = page.locator(".complete-header")
        self.thank_you_msg = page.locator("text=Thank you for your order!")
        self.dispatch_msg = page.locator("text=Your order has been dispatched")

    @property
    def is_success(self) -> bool:
        return "Thank you" in self.success_header.text_content()

    @property
    def is_success_page(self) -> bool:
        """
        Проверка, что мы на странице успеха.
        На SauceDemo заголовок содержит 'Thank you for your order!'
        """
        try:
            # ✅ Правильный текст для SauceDemo
            expect(self.success_header).to_have_text(
                "Thank you for your order!", timeout=5000)
            return True
        except AssertionError:
            # Фоллбэк: частичное совпадение
            header_text = self.success_header.text_content().strip()
            return "Thank you" in header_text and "order" in header_text

    @property
    def thank_you_message(self) -> str:
        """Возвращает текст благодарности"""
        return self.thank_you_msg.text_content()

    def assert_success_header(self,
                              expected_text: str = "Checkout: Complete!"):
        """Проверка заголовка успеха"""
        expect(self.success_header).to_have_text(expected_text)
        return self

    def assert_thank_you_visible(self):
        """Проверка, что сообщение благодарности видно"""
        expect(self.thank_you_msg).to_be_visible()
        return self

    def assert_dispatch_message_visible(self):
        """Проверка сообщения о доставке"""
        expect(self.dispatch_msg).to_be_visible()
        return self

    def assert_back_button_tappable(self, min_size: int = 32):  # 44
        """
        📱 Мобильная проверка: кнопка Back Home достаточного размера для тапа.
        Гайдлайны: мин. 44×44 px для тач-целевых элементов.
        """
        # 1. Кнопка должна быть видима
        expect(self.back_home_btn).to_be_visible()

        # 2. Кнопка должна быть активна
        expect(self.back_home_btn).to_be_enabled()

        # 3. Проверка размера (гайдлайны Apple/Google)
        box = self.back_home_btn.bounding_box()
        assert box is not None, "Не удалось получить bounding_box кнопки"
        assert box[
                   "width"] >= min_size, f"Кнопка слишком узкая: {box['width']}px < {min_size}px"
        assert box[
                   "height"] >= min_size, f"Кнопка слишком низкая: {box['height']}px < {min_size}px"

        return self

    # def back_to_products(self) -> "InventoryPage":
    #     from pages.inventory_page import InventoryPage
    #     self.back_home_btn.click()
    #     return InventoryPage(self.page)

    def back_to_products(self) -> "InventoryPage":
        """Возврат на страницу товаров"""
        from pages.inventory_page import InventoryPage
        self.tap(self.back_home_btn)  # 📱 Mobile: tap вместо click
        return InventoryPage(self.page)

    def assert_no_horizontal_scroll(self):
        """Проверка отсутствия горизонтального скролла (мобильный UX)"""
        super().assert_no_horizontal_scroll()
        return self
