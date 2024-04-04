"""Simple tests to for players"""
from time import sleep

import pytest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

from framework.common_actions import check_tab, get_by_value, get_page_title


def verify_player(name: str, driver: webdriver):
    # back to the main page....
    driver.find_element(AppiumBy.ID, 'com.fivemobile.thescore:id/navigation_news').click()
    sleep(3)

    searchbar = driver.find_element(AppiumBy.ID, 'com.fivemobile.thescore:id/search_bar_text_view')
    searchbar.click()
    sleep(1)
    search = driver.find_element(AppiumBy.ID, 'com.fivemobile.thescore:id/search_src_text')
    search.click()
    search.send_keys(name)
    sleep(3)
    player = get_by_value(name, driver)
    player.click()
    sleep(3)

    title = get_page_title(driver, 'com.fivemobile.thescore:id/txt_player_name')
    if name not in title:
        pytest.fail(f'Did not land on page for Player {name}')

    check_tab(driver, 'News')
    check_tab(driver, 'Info')

    back = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Navigate up')
    back.click()
    sleep(2)
    back = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Navigate up')
    back.click()
