from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """
    Фасад для входа в процесс чекаута.
    Обычно используется для перехода с корзины на первый шаг.
    """
    def __init__(self, page: Page):
        super().__init__(page)
        # На странице чекаута основные элементы - это поля первого шага
        self.first_name = page.locator("#first-name")
        self.last_name = page.locator("#last-name")
        self.postal_code = page.locator("#postal-code")
        self.continue_btn = page.locator("#continue")
        self.cancel_btn = page.locator("#cancel")

    def is_loaded(self) -> bool:
        """Проверка, что страница чекаута загружена"""
        return self.first_name.is_visible() and self.continue_btn.is_visible()

    def fill_and_continue(self, first_name: str, last_name: str, postal_code: str) -> "CheckoutSummaryPage":
        """Заполняет данные и переходит к финальному шагу"""
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)
        # 📱 Для мобильных тестов лучше использовать tap(), но click() тоже сработает
        self.continue_btn.tap() 
        return CheckoutSummaryPage(self.page)


class CheckoutStepOnePage(BasePage):
    """Шаг 1: Адрес доставки"""
    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name = page.locator("#first-name")
        self.last_name = page.locator("#last-name")
        self.postal_code = page.locator("#postal-code")
        self.continue_btn = page.locator("#continue")
        self.cancel_btn = page.locator("#cancel")

    def fill_information(self, first_name: str, last_name: str, postal_code: str):
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)
        return self

    def continue_to_summary(self) -> "CheckoutSummaryPage":
        self.continue_btn.tap()  # 📱 Mobile: tap
        return CheckoutSummaryPage(self.page)

    def cancel_to_cart(self) -> "CartPage":
        from pages.cart_page import CartPage
        self.cancel_btn.tap()
        return CartPage(self.page)


class CheckoutSummaryPage(BasePage):
    """Шаг 2: Финальная проверка и оплата"""
    def __init__(self, page: Page):
        super().__init__(page)
        self.finish_btn = page.locator("#finish")
        self.cancel_btn = page.locator("#cancel")
        self.total_label = page.locator(".summary_total_label")
        self.item_total_label = page.locator(".summary_subtotal_label")
        self.tax_label = page.locator(".summary_tax_label")

    def _parse_price(self, text: str) -> float:
        text = text.replace("Total: $", "")
        text = text.replace("Item total: $", "")
        text = text.replace("$", "").strip()
        return float(text)

    @property
    def total(self) -> float:
        return self._parse_price(self.total_label.text_content())

    @property
    def item_total(self) -> float:
        return self._parse_price(self.item_total_label.text_content())

    @property
    def tax(self) -> float:
        return self._parse_price(self.tax_label.text_content())

    def finish_order(self) -> "CompletePage":
        from pages.complete_page import CompletePage
        self.finish_btn.tap()  # 📱 Mobile: tap
        return CompletePage(self.page)