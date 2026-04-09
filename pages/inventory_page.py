from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        
        # 🔹 Локаторы
        self.products = page.locator(".inventory_item")
        self.cart_link = page.locator(".shopping_cart_link")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.menu_btn = page.locator(".bm-burger-button")  # гамбургер-меню

    @property
    def is_loaded(self) -> bool:
        """Проверка, что страница товаров загрузилась"""
        try:
            expect(self.products.first).to_be_visible(timeout=3000)
            return True
        except AssertionError:
            return False

    def assert_loaded(self):
        """Проверка, что страница товаров загружена"""
        expect(self.products.first).to_be_visible(timeout=5000)
        return self

    @property
    def cart_badge_count(self) -> int:
        """Возвращает количество товаров в корзине"""
        try:
            if self.cart_badge.is_visible():
                return int(self.cart_badge.text_content())
        except Exception:
            pass
        return 0

    def assert_cart_badge_count(self, expected: int):
        """Проверка количества товаров в корзине"""
        assert self.cart_badge_count == expected, \
            f"Ожидалось {expected} товаров в корзине, но найдено {self.cart_badge_count}"
        return self

    def get_product_locator(self, product_name: str) -> Locator:
        """Возвращает локатор карточки товара по названию"""
        return self.page.locator(f".inventory_item:has-text('{product_name}')")

    def get_product_price(self, product_name: str) -> str:
        """Возвращает цену товара"""
        price_locator = self.get_product_locator(product_name).locator(".inventory_item_price")
        return price_locator.text_content().strip()

    def add_to_cart(self, product_name: str):
        """Добавляет товар в корзину через click()"""
        btn = self.get_product_locator(product_name).locator("button[id^='add-to-cart']")
        btn.click()
        return self

    def add_to_cart_via_tap(self, product_name: str):
        """📱 Добавляет товар в корзину через tap() для мобильных"""
        btn = self.get_product_locator(product_name).locator("button[id^='add-to-cart']")
        self.tap(btn)
        return self

    def remove_from_cart(self, product_name: str):
        """Удаляет товар из корзины (кнопка Remove на странице товаров)"""
        btn = self.get_product_locator(product_name).locator("button[id^='remove']")
        btn.click()
        return self

    def go_to_cart(self) -> "CartPage":
        """Переходит в корзину"""
        from pages.cart_page import CartPage
        self.cart_link.click()
        return CartPage(self.page)

    def proceed_to_checkout(self) -> "CheckoutStepOnePage":
        """Переходит к чекауту (если уже есть товары в корзине)"""
        from pages.checkout_page import CheckoutStepOnePage
        self.cart_link.click()
        # На странице корзины нужно нажать Checkout
        cart_page = CartPage(self.page)
        return cart_page.proceed_to_checkout()

    def assert_no_horizontal_scroll(self):
        """Проверка отсутствия горизонтального скролла"""
        super().assert_no_horizontal_scroll()
        return self

    def get_all_product_names(self) -> list:
        """Возвращает список названий всех товаров"""
        return [el.text_content() for el in self.products.locator(".inventory_item_name").all()]