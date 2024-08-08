import logging
import requests
from BaseApp import testdata


class BaseAPI:
    def __init__(self):
        self.base_url = testdata['address']

    def get_login_token(self):
        """Получение токена авторизации и сохранение ответа в JSON-файл."""
        try:
            response = requests.post(self.base_url + 'gateway/login', data={
                'username': testdata['user'],
                'password': testdata['pass']
            })
            response.raise_for_status()
            return response.json().get('token')
        except requests.RequestException as e:
            logging.error(f"Ошибка при авторизации: {e}")
            raise

    def get_user_profile(self, token, user_id):
        """Получение профиля пользователя по токену."""
        headers = {'X-Auth-Token': token}
        response = requests.get(f'{self.base_url}api/users/profile/{user_id}', headers=headers)
        response.raise_for_status()
        return response.json()
