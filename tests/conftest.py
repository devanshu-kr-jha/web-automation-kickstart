import pytest
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

load_dotenv()

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def login_page(driver):
    return LoginPage(driver)

@pytest.fixture(scope="function")
def inventory_page(driver):
    return InventoryPage(driver)



@pytest.fixture(scope="session")
def standard_user_credentials():
    username = os.getenv("SAUCEDEMO_STANDARD_USER", "standard_user")
    password = os.getenv("SAUCEDEMO_PASSWORD", "secret_sauce")
    if username == "standard_user" and password == "secret_sauce" and not os.getenv("SAUCEDEMO_STANDARD_USER"):
        print("\nINFO: Using default SauceDemo credentials. Consider setting them in a .env file.")
    return {"username": username, "password": password}

@pytest.fixture(scope="session")
def locked_out_user_credentials():
    username = os.getenv("SAUCEDEMO_LOCKED_OUT_USER", "locked_out_user")
    password = os.getenv("SAUCEDEMO_PASSWORD", "secret_sauce")
    return {"username": username, "password": password}