# pages/base_page.py
from playwright.sync_api import Page, Locator, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # 📱 Мобильные хелперы
    def tap(self, locator: Locator):
        locator.tap()

    def is_tappable(self, locator: Locator, min_size: int = 44) -> bool:
        box = locator.bounding_box()
        return box is not None and box["width"] >= min_size and box["height"] >= min_size

    def assert_no_horizontal_scroll(self):
        assert not self.page.evaluate("document.documentElement.scrollWidth > window.innerWidth"), \
            "❌ Горизонтальный скролл обнаружен!"