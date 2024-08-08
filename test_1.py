import logging
import time
import yaml

from testpage import OperationsHelper
from testpage import APIOperationsHelper

with open('./testdata.yaml') as f:
    testdata = yaml.safe_load(f)


def test_step1(browser):
    """Проверка успешного входа с корректными данными."""
    testpage = OperationsHelper(browser)
    testpage.go_to_site()
    time.sleep(2)
    testpage.enter_login(testdata["user"])
    testpage.enter_pass(testdata["pass"])
    testpage.click_login_button()
    testpage.click_about_btn()
    time.sleep(5)
    font_size = testpage.get_about_text()
    assert font_size == "32px", f"Expected font size '32px', but got '{font_size}'"


def test_user_profile():
    """Проверка данных профиля пользователя."""
    helper = APIOperationsHelper()
    token = helper.get_login_token()

    # Проверяем, что токен получен успешно
    assert token is not None, "Токен не был получен"

    user_id = testdata['user_id']  # Получаем user_id из конфигурации
    profile_data = helper.get_user_profile(token, user_id)

    # Проверяем, что username в профиле совпадает с username в testdata
    assert profile_data['username'] == testdata['user'], f"Username не совпадает: {profile_data['username']} != {testdata['user']}"
