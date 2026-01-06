from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pytest


link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"


def test_button_add_to_basket(browser):
    browser.get(link)
    item = WebDriverWait(browser, 5).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'button.btn-add-to-basket')))
    assert item.text == 'Añadir al carrito', 'No hay ningun boton!!!'
    print(f'\nHay un boton!')
