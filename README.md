# 🛒 SauceDemo Playwright Mobile Tests

Автотесты для мобильного веб-интерфейса [SauceDemo](https://www.saucedemo.com/) 
с использованием Playwright (Python) и Page Object Model.

> ✅ Ресурс доступен из РФ • ✅ Без капч • ✅ Стабильные тестовые данные

---

## 🚀 Быстрый старт

### Требования
- Python 3.12+
- pip >= 23.0

### Установка
```bash
# 1. Клонируйте репозиторий
git clone https://github.com/your-org/saucedemo-playwright-mobile.git
cd saucedemo-playwright-mobile

# 2. Установите зависимости
pip install -e .

# 3. Установите браузеры Playwright
playwright install chromium --with-deps
```

### Запуск тестов

# Все мобильные тесты на iPhone 14 Pro
pytest -m mobile --mobile-device iPhone-14-Pro

# Конкретный файл тестов
pytest tests/test_e2e_mobile.py --mobile-device Pixel-7

# С видео и скриншотами при ошибках
pytest -m mobile --video=on --screenshot=on

# Параллельный запуск на 3 устройствах
pytest -m mobile -n 3 --dist loadscope


### Просмотр отчётов

# Allure-отчёт (требуется установленный allure)
allure serve output/allure-results

# HTML-отчёт pytest
open output/report-*.html


### 📁 Структура проекта

```bash
📦 saucedemo-playwright-mobile
├── 📄 pyproject.toml          # Зависимости и конфиги
├── 📄 pytest.ini              # Настройки pytest
├── 🔧 .github/workflows/      # CI/CD пайплайны
├── 🧩 config/                 # Конфигурации: устройства, пользователи, товары
├── 🧱 pages/                  # Page Objects с мобильными хелперами
├── 🧪 tests/                  # Тест-кейсы, сгруппированные по типу
├── 🛠 utils/                  # Вспомогательные функции
└── 📤 output/                 # Артефакты (скриншоты, видео, отчёты)
```
