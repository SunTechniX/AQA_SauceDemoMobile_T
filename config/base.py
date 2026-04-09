"""Базовая конфигурация проекта: URL, таймауты, режимы"""

# Базовый URL для тестов
BASE_URL = "https://www.saucedemo.com"

# Таймауты (в миллисекундах)
DEFAULT_TIMEOUT = 15000  # для обычных действий
PAGE_LOAD_TIMEOUT = 30000  # для загрузки страниц

# Режимы запуска
HEADLESS = True  # False для отладки с открытым браузером
SLOW_MO = 0  # Задержка между действиями в мс (для отладки: 100-500)

# Тестовые окружения (можно расширить)
ENVIRONMENTS = {
    "dev": "http://localhost:3000",
    "stage": "https://www.saucedemo.com",
    "prod": "https://www.saucedemo.com",  # для SauceDemo prod = stage
}

def get_base_url(env: str = "stage") -> str:
    """Возвращает базовый URL для указанного окружения"""
    return ENVIRONMENTS.get(env, BASE_URL)