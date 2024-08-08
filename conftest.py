import pytest
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as SerChrome
from selenium.webdriver.firefox.service import Service as SerFire
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from BaseApp import BaseAPI

with open('./testdata.yaml') as f:
    testdata = yaml.safe_load(f)
    url = testdata['browser']


@pytest.fixture(scope='session')
def browser():
    if browser == 'firefox':
        service = SerFire(executable_path=GeckoDriverManager().install())
        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(service=service, options=options)
    else:
        service = SerChrome(executable_path=ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def api_client():
    """Фикстура для работы с API."""
    return BaseAPI()
