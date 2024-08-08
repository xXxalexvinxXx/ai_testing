import yaml
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

# Чтение конфигурации из файла testdata.yaml
with open("./testdata.yaml") as f:
    testdata = yaml.safe_load(f)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = testdata["address"]

    def find_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located(locator),
            message=f"Can't find element by locator {locator}",
        )

    def get_element_property(self, locator, prop):
        element = self.find_element(locator)
        return element.value_of_css_property(prop)

    def go_to_site(self):
        return self.driver.get(self.base_url)


class BaseAPI:
    def __init__(self):
        self.base_url = testdata['address']
        self.user_id = testdata['user_id']
        self.login_token = self.get_login_token()

    def get_login_token(self):
        """Получение токена авторизации."""
        try:
            response = requests.post(f'{self.base_url}gateway/login', data={
                'username': testdata['user'],
                'password': testdata['pass']
            })
            response.raise_for_status()
            return response.json()['token']
        except requests.RequestException as e:
            raise Exception(f"Ошибка при получении токена: {e}")

    def get_user_profile(self, token, user_id):
        """Получение профиля пользователя по ID."""
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = requests.get(f'{self.base_url}api/users/profile/{user_id}', headers=headers)
        response.raise_for_status()
        return response.json()

