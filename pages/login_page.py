from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE_CONTAINER = (By.CSS_SELECTOR, "h3[data-test='error']")

    def __init__(self, driver):
        super().__init__(driver)
        self.path = ""
    
    def open(self):
        super().navigate_to(self.path)
    
    def enter_username(self, username: str):
        self._type_text(self.USERNAME_INPUT, username)
    
    def enter_password(self, passoword: str):
        self._type_text(self.PASSWORD_INPUT, passoword)
    
    def click_login_btn(self):
        self._click(self.LOGIN_BUTTON)
    
    def login(self, username: str, password: str):
        self.open()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_btn()
    
    def get_error_message(self) -> str | None:
        if self._is_displayed(self.ERROR_MESSAGE_CONTAINER):
            return self._get_text(self.ERROR_MESSAGE_CONTAINER)
        return None