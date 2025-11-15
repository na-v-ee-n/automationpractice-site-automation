import allure
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def step(description):
    """Wrapper for allure.step that also logs"""
    logger.info(description)
    return allure.step(description)

def attach_text(content, name):
    """Attach text to allure report"""
    allure.attach(content, name, allure.attachment_type.TEXT)

def attach_html(content, name):
    """Attach HTML to allure report"""
    allure.attach(content, name, allure.attachment_type.HTML)

def attach_screenshot(driver, name="screenshot"):
    """Attach screenshot to allure report"""
    allure.attach(driver.get_screenshot_as_png(), name, allure.attachment_type.PNG)

def log_and_assert(condition, message):
    """Log and assert with message"""
    if not condition:
        logger.error(message)
    assert condition, message

def attach_on_failure(driver, page_source=True, screenshot=True):
    """Attach page source and screenshot on failure"""
    if screenshot:
        attach_screenshot(driver)
    if page_source:
        attach_html(driver.page_source, "Page Source")
