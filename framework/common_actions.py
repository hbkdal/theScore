"""common actions for the tests, should be refactored to  page object model"""
import pytest
from appium.webdriver import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver import ActionChains


def get_by_value(param, driver) -> WebElement | None:
    items = driver.find_elements(AppiumBy.CLASS_NAME, 'android.widget.TextView')
    for item in items:
        text_value = item.get_attribute('text')
        if param in text_value:
            return item
    return None


def get_by_text(param, driver) -> WebElement | None:
    """
    Get an element by its text return None if not found
    """
    value = param
    txt_locator = '//*[text()="' + value + '"]'
    elements = driver.find_elements(AppiumBy.XPATH, txt_locator)
    if len(elements) > 0:
        return elements[0]
    return None


def tap(driver, element):
    size = element.size
    x_offset = 1 - (size['width'] / 2)
    ActionChains(driver).move_to_element_with_offset(element, x_offset, 0).click().perform()


def get_page_title(driver, title_field):
    title_elements = driver.find_elements(AppiumBy.ID, title_field)
    if len(title_elements) == 0:
        return ''
    title_text = title_elements[0].get_attribute('text')
    return title_text


def check_tab(driver, name: str):
    upper_name = name.upper()
    tab = get_by_value(upper_name, driver)
    tab.click()

    tabs = driver.find_elements(AppiumBy.ACCESSIBILITY_ID, name)
    if len(tabs) == 1:
        tab_active = tabs[0].get_attribute('selected')
        if not tab_active:
            pytest.fail(f'Expected tab {name} not active')
