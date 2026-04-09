"""Пресеты мобильных устройств для эмуляции в Playwright"""

MOBILE_DEVICES = {
    "iPhone-14-Pro": {
        "viewport": {"width": 393, "height": 852},
        "device_scale_factor": 3,
        "is_mobile": True,
        "has_touch": True,
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    },
    "Pixel-7": {
        "viewport": {"width": 412, "height": 915},
        "device_scale_factor": 2.625,
        "is_mobile": True,
        "has_touch": True,
        "user_agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    },
    "iPad-Mini": {
        "viewport": {"width": 768, "height": 1024},
        "device_scale_factor": 2,
        "is_mobile": True,
        "has_touch": True,
        "user_agent": "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    },
}

def get_device_config(device_name: str) -> dict:
    """Возвращает конфигурацию устройства или raises KeyError"""
    if device_name not in MOBILE_DEVICES:
        available = ", ".join(MOBILE_DEVICES.keys())
        raise KeyError(f"Unknown device '{device_name}'. Available: {available}")
    return MOBILE_DEVICES[device_name].copy()