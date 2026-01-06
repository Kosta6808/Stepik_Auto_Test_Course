import argparse
import sys
import pytest
from seleniumbase import Driver
import os
from dotenv import load_dotenv
from seleniumwire import webdriver


load_dotenv()
proxy_info = f"{os.getenv('USER')}:{os.getenv('PASS')}@{os.getenv('IP')}:{os.getenv('PORT')}"
proxy_options = {
    'proxy': {
        'http': f'http://{proxy_info}',
        'https': f'https://{proxy_info}',
        'no_proxy': 'localhost,127.0.0.1'
    }
}


# Функция распарсивания командной строки запуска и запоминания значений 2х флагов(с дефолтами)
def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome", help="Choose browser: chrome or firefox")
    parser.addoption("--language", action="store", default="en-EN", help="Language to set for the browser")


# Функция для поиска значения флага в аргументах запуска (SeleniumBase Chrome)
def get_arg(name, default=None):
    for arg in sys.argv:
        if arg.startswith(f"--{name}="):
            return arg.split("=")[1]
    return default


@pytest.fixture(scope="function")
def browser(request):
    browser_name = request.config.getoption("browser_name")
    if browser_name == "chrome":
        print("\nStart chrome browser for test...")
        # Получаем язык из командной строки или ставим 'en' по умолчанию
        lang = get_arg("language", "es-ES")
        browser = Driver(browser="chrome", proxy=proxy_info, uc=True, locale_code=lang)
    elif browser_name == "firefox":
        # Настраиваем парсер аргументов командной строки
        parser = argparse.ArgumentParser()
        parser.add_argument("--language", default="en-US")
        args, unknown = parser.parse_known_args()  # parse_known_args не выдаст ошибку на лишние флаги
        options = webdriver.FirefoxOptions()
        options.set_preference("intl.accept_languages", args.language)
        print("\nStart firefox browser for test...")
        browser = webdriver.Firefox(options=options, seleniumwire_options=proxy_options)
    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")
    yield browser
    print("\nQuit browser..")
    browser.quit()