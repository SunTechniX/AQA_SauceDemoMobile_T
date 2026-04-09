"""Глобальные фикстуры для pytest + Playwright"""
import pytest
from playwright.sync_api import Browser, BrowserContext, Page
from config.base import BASE_URL
from config.devices import get_device_config


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, request):
    """Расширяем стандартные аргументы контекста для мобильных тестов"""
    # Получаем устройство из маркера теста или используем дефолт
    device_name = request.config.getoption("--mobile-device", default="iPhone-14-Pro")
    
    try:
        device_config = get_device_config(device_name)
        return {**browser_context_args, **device_config}
    except KeyError:
        # Если устройство не найдено, возвращаем базовые аргументы
        return browser_context_args


@pytest.fixture
def mobile_page(page: Page) -> Page:
    """
    Страница в мобильном контексте.
    
    Автоматически применяет:
    - Вьюпорт устройства
    - Эмуляцию тач-событий
    - Мобильный user-agent
    """
    # Дополнительные настройки для каждого теста
    page.set_default_timeout(15000)  # чуть больше для мобильных сетей
    return page


@pytest.fixture(scope="session")
def base_url() -> str:
    """Базовый URL для тестов"""
    return BASE_URL


# === CLI опции для гибкого запуска ===
def pytest_addoption(parser):
    parser.addoption(
        "--mobile-device",
        action="store",
        default="iPhone-14-Pro",
        help="Эмулируемое устройство: iPhone-14-Pro, Pixel-7, iPad-Mini"
    )
    parser.addoption(
        "--slow-mo",
        action="store",
        type=int,
        default=0,
        help="Задержка между действиями в мс (для отладки)"
    )


@pytest.fixture(scope="session")
def slow_mo(request) -> int:
    """Задержка между действиями для отладки"""
    return request.config.getoption("--slow-mo")