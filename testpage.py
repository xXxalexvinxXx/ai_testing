import logging
import yaml

from BaseApp import BasePage
from selenium.webdriver.common.by import By

with open('./testdata.yaml') as f:
    testdata = yaml.safe_load(f)


class TestSearchLocators:
    # login
    LOCATOR_LOGIN_FIELD = (By.XPATH, testdata['login_field'])
    # passwd
    LOCATOR_PASS_FIELD = (By.XPATH, testdata['pass_field'])
    # login button
    LOCATOR_LOGIN_BTN = (By.CSS_SELECTOR, testdata['login_btn'])
    # about button
    LOCATOR_ABOUT_BTN = (By.XPATH, testdata['about'])
    # about page header
    LOCATOR_ABOUT_FIELD = (By.XPATH, testdata['title_about'])


class OperationsHelper(BasePage):
    def enter_login(self, word):
        login_field = self.find_element(TestSearchLocators.LOCATOR_LOGIN_FIELD)
        login_field.clear()
        login_field.send_keys(word)

    def enter_pass(self, word):
        pass_field = self.find_element(TestSearchLocators.LOCATOR_PASS_FIELD)
        pass_field.clear()
        pass_field.send_keys(word)

    def click_login_button(self):
        self.find_element(TestSearchLocators.LOCATOR_LOGIN_BTN).click()

    def click_about_btn(self):
        logging.info(f"Send click to element {TestSearchLocators.LOCATOR_ABOUT_BTN[1]}")
        self.find_element(TestSearchLocators.LOCATOR_ABOUT_BTN).click()

    def get_about_text(self):
        logging.info(
            f"Read text of element {TestSearchLocators.LOCATOR_ABOUT_FIELD[1]}"
        )
        about_header = self.find_element(TestSearchLocators.LOCATOR_ABOUT_FIELD, time=2)
        return about_header.value_of_css_property('font-size')
