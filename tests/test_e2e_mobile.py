"""E2E-тесты для мобильного веб-интерфейса SauceDemo"""
import pytest
from config.devices import get_device_config
from config.users import STANDARD_USER
from config.products import BACKPACK
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@pytest.mark.mobile
@pytest.mark.e2e
@pytest.mark.parametrize("device_name", ["iPhone-14-Pro", "Pixel-7"])
def test_mobile_purchase_flow(page, device_name):
    """
    TC_MOBILE_001: Полный цикл покупки на мобильном устройстве
    
    Проверяет:
    - Адаптивность вьюпорта
    - Работу тач-событий
    - Сохранение состояния между шагами
    - Корректность расчётов в чекауте
    """
    # 1. Инициализация мобильного контекста
    device_config = get_device_config(device_name)
    # (в реальной фикстуре это делается в conftest.py)
    
    # 2. Авторизация
    login = LoginPage(page)
    login.open()
    login.assert_no_horizontal_scroll()  # мобильный UX: нет горизонтального скролла
    
    login.username.tap()  # используем tap() вместо click()
    login.username.fill(STANDARD_USER["username"])
    login.password.fill(STANDARD_USER["password"])
    login.login_button.tap()
    
    # 3. Страница товаров
    inventory = InventoryPage(page)
    inventory.assert_loaded()
    
    # Проверка адаптивности: 6 товаров в сетке, без горизонтального скролла
    assert inventory.products.count() == 6
    inventory.assert_no_horizontal_scroll()
    
    # 4. Добавление товара через тап
    original_price = inventory.get_product_price(BACKPACK["name"])
    inventory.add_to_cart_via_tap(BACKPACK["name"])  # метод с tap() внутри
    
    # Проверка бейджа корзины
    inventory.assert_cart_badge_count(1)
    
    # 5. Чекаут
    cart = inventory.go_to_cart()
    assert cart.items_count == 1
    assert cart.get_item_price(BACKPACK["name"]) == original_price
    
    checkout = cart.proceed_to_checkout()
    checkout.fill_information(
        first_name="Joe",
        last_name="Lowson",
        postal_code="1234"
    )
    
    # Проверка мобильной оптимизации полей
    # вариант А: проверка, что поле существует и доступно:
    assert checkout.postal_code.is_visible()
    assert checkout.postal_code.is_enabled()

    # вариант Б: проверка, что поле принимает ввод:
    checkout.postal_code.fill("12345")
    assert checkout.postal_code.input_value() == "12345"
    
    # 6. Финализация
    summary = checkout.continue_to_summary()
    assert abs(summary.total - (summary.item_total + 2.40)) < 0.01
    
    complete = summary.finish_order()
    assert complete.is_success_page
    complete.assert_back_button_tappable()  # проверка размера кнопки
    
    # 7. Возврат к покупкам
    inventory = complete.back_to_products()
    assert inventory.is_loaded