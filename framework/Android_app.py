"""core android functionality"""
import os
import subprocess
from os import getenv
from pathlib import Path
from time import sleep
from typing import List

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver import ActionChains

from framework.devices import TestDevice, get_local_device_caps

TARGET_DEVICES: list[TestDevice] = []


def set_devices(devices: list[TestDevice]):
    """ Set the list of devices we intend to test """
    global TARGET_DEVICES
    TARGET_DEVICES = devices


class Mobile_app:
    app_package: str
    platform_type: str
    android: bool
    options: UiAutomator2Options
    apk_list: [str]
    APPIUM_URL = getenv('APPIUM_URL', 'http://127.0.0.1:4723')
    remote_url = APPIUM_URL
    my_driver: webdriver

    def initialize_appium_driver(self):
        self.app_package = "com.fivemobile.thescore"
        self.options = get_local_device_caps()
        driver = webdriver.Remote(self.APPIUM_URL, options=self.options)
        self.my_driver = driver

        # let's reinstall ap to get to known state
        self.reinstall_app()
        # open the app
        self.launch_app(self.app_package)
        # Sign in
        self.sign_in()
        return driver

    def run_adb_command(self, command, timeout=60):
        try:
            subprocess.check_output(command, shell=True, stderr=True, timeout=timeout)
        except subprocess.CalledProcessError as e:
            raise Exception(e)
        except subprocess.TimeoutExpired as e:
            raise Exception(e)

    def reinstall_app(self):
        self.terminate_app(self.app_package)
        self.uninstall_package(self.app_package)
        # Install the app
        if not self.install_package(self.options.udid, self.get_apks()):
            pytest.fail('App not installed')
        sleep(10)

    def get_apks(self):
        current_directory = Path().absolute()
        apk_directory = current_directory / "apk"
        apks = []
        apk_dir_files = os.listdir(apk_directory)
        for f in apk_dir_files:
            if f.endswith(".apk"):
                apks.append(f)
        apk_list = []
        for apk in apks:
            path = current_directory / "apk" / apk
            apk_list.append(str(path))
        return apk_list

    def uninstall_package(self, app_bundle_id):
        if not self.my_driver.is_app_installed(app_bundle_id):
            return True
        self.my_driver.remove_app(app_bundle_id)
        sleep(2)
        return True

    def terminate_app(self, app_bundle_id):
        self.my_driver.terminate_app(app_bundle_id)
        sleep(2)
        return True

    def execute_commands(self, command: List[str], check_output: bool = True) -> str | subprocess.Popen:
        if not check_output:
            return subprocess.Popen(command)
        else:
            return subprocess.check_output(command).decode("utf-8")

    def install_package(self, android_udid: str, app_file_path: [str]):
        # self.restart_appium()
        if not app_file_path:
            raise FileNotFoundError(app_file_path)

        app_files = ' '.join(app_file_path)
        cmd = "adb -s {udid} install-multiple {package_path}".format(udid=android_udid, package_path=app_files)
        self.run_adb_command(cmd)
        # need to return true when we succeed here.....
        return True

    def launch_app(self, app_bundle_id):
        app_available = self.my_driver.is_app_installed(app_bundle_id)
        if app_available:
            self.my_driver.activate_app(app_bundle_id)
            sleep(5)
            return True
        else:
            raise Exception()

    def sign_in(self):
        welcome = self.my_driver.find_elements(AppiumBy.ID, 'com.fivemobile.thescore:id/txt_welcome')
        if len(welcome) == 0:
            pytest.fail('Did not find welcome message on app startup')
        # click the log in, commented out as it clicks the test not the link
        login = self.my_driver.find_element(AppiumBy.ID, 'com.fivemobile.thescore:id/txt_sign_in')
        size = login.size
        x_offset = size['width'] / 2 - 1
        ActionChains(self.my_driver).move_to_element_with_offset(login, x_offset, 0).click().perform()

        # Should use credentials from external source....
        # insert email
        email = self.my_driver.find_element(AppiumBy.ID, 'com.fivemobile.thescore:id/email_input_edittext')
        email.send_keys('henrikbaekdahl+thescore@gmail.com')
        # enter password
        password = self.my_driver.find_element(AppiumBy.ID, 'com.fivemobile.thescore:id/password_input_edittext')
        password.send_keys('Password#!123')
        sleep(3)
        # click the login button
        self.my_driver.find_element(AppiumBy.ID, 'com.fivemobile.thescore:id/login_button').click()
        sleep(10)
        location_disallow = self.my_driver.find_elements(AppiumBy.ID, 'com.fivemobile.thescore:id/btn_disallow')
        if len(location_disallow) > 0:
            location_disallow[0].click()
            sleep(3)

        # verify we are now on the landing page by checking if the search bar is there
        search = self.my_driver.find_elements(AppiumBy.ID, 'com.fivemobile.thescore:id/search_bar_text_view')
        if len(search) == 0:
            pytest.fail('Search not found after login')
