# pages/login_page.py
from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # 🔹 Локаторы
        self.username = page.locator("#user-name")
        self.password = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("h3[data-test='error']")

    def open(self):
        self.page.goto("/")
        return self

    def login(self, username: str, password: str):
        """Стандартный логин через .fill() + .click()"""
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()
        return self

    def login_via_tap(self, username: str, password: str):
        """📱 Мобильный логин через .tap()"""
        self.username.tap()
        self.username.fill(username)
        self.password.tap()
        self.password.fill(password)
        self.login_button.tap()
        return self

    def assert_error_visible(self, expected_text: str):
        """Проверка сообщения об ошибке"""
        expect(self.error_message).to_be_visible()
        assert expected_text in self.error_message.text_content()
        return self

    def assert_loaded(self):
        """Проверка, что страница авторизации загружена"""
        expect(self.username).to_be_visible()
        expect(self.password).to_be_visible()
        expect(self.login_button).to_be_visible()
        return self