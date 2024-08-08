import logging
import requests
import yaml

from BaseApp import BasePage
from BaseApp import BaseAPI
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


class APIOperationsHelper(BaseAPI):
    def api_create_post(self):
        """API тест: Проверка создания поста."""
        created_post = self.create_post()
        assert created_post is not None, 'Пост не был создан'

    def api_check_post_description(self):
        """API тест: Проверка наличия описания созданного поста в списке постов."""
        created_post = self.create_post()
        try:
            headers = {'X-Auth-Token': self.login_token}
            response = requests.get(f'{self.base_url}api/posts', headers=headers)
            response.raise_for_status()
            post_descriptions = [post['description'] for post in response.json().get('data', [])]
            assert created_post['description'] in post_descriptions, 'Описание поста не найдено'
            logging.info("Описание поста найдено в списке постов")
        except requests.RequestException as e:
            logging.error(f"Ошибка при проверке наличия описания поста: {e}")
            raise

    def api_check_nonexistent_post(self):
        """API тест: Проверка отсутствия текста для несуществующего поста."""
        test_text = '123'
        try:
            headers = {'X-Auth-Token': self.login_token}
            response = requests.get(f'{self.base_url}api/posts', params={'owner': 'notMe'}, headers=headers)
            response.raise_for_status()
            posts = response.json().get('data', [])
            post_titles = [post['title'] for post in posts]
            logging.info(f"Post titles retrieved: {post_titles}")
            assert test_text not in post_titles, f"Текст '{test_text}' найден в заголовках постов"
        except requests.RequestException as e:
            raise Exception(f"Ошибка при проверке несуществующего поста: {e}")
