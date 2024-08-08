import time
import yaml
import BaseApi
from testpage import OperationsHelper
from BaseCmd import NiktoHelper

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

def test_step2():
    """Тест для проверки отсутствия ошибок в выводе Nikto."""
    nikto = NiktoHelper()
    output = nikto.run_nikto()
    assert '0 error(s)' in output, "Nikto обнаружил ошибки"

def test_steep3():
    """Проверка данных профиля пользователя."""
    helper = BaseApi.BaseAPI()
    token = helper.get_login_token()

    # Проверяем, что токен получен успешно
    assert token is not None, "Токен не был получен"

    user_id = testdata['user_id']  # Получаем user_id из конфигурации

    # Используем метод для получения профиля пользователя
    profile_data = helper.get_user_profile(token, user_id)

    # Проверяем, что username в профиле совпадает с username в testdata
    assert profile_data['username'] == testdata['user'], f"Username не совпадает: {profile_data['username']} != {testdata['user']}"
