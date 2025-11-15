import pytest
import allure
from selenium import webdriver
from utils import config

@pytest.fixture(scope="class")
def setup(request):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(config.BASE_URL)
    request.cls.driver = driver
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        if hasattr(item, "cls") and hasattr(item.cls, "driver"):
            from utils.test_helper import attach_screenshot
            attach_screenshot(item.cls.driver)
