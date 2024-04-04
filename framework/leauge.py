"""Simple tests to for leagues"""
from time import sleep

import pytest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

from framework.common_actions import check_tab, get_by_value, get_page_title, tap


def verify_league(name: str, driver: webdriver):
    driver.find_element(AppiumBy.ID, 'com.fivemobile.thescore:id/navigation_leagues').click()
    sleep(3)

    league = get_by_value(name, driver)
    tap(driver, league)
    sleep(3)

    title = get_page_title(driver, 'com.fivemobile.thescore:id/titleTextView')
    if name not in title:
        pytest.fail(f'Did not land on page for League {name}')

    check_tab(driver, 'News')
    check_tab(driver, 'Scores')

    back = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Navigate up')
    back.click()
