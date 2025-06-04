from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckoutStepOnePage(BasePage):
    PAGE_TITLE = (By.CLASS_NAME, "title") # "Checkout: Your Information"
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE_CONTAINER = (By.XPATH, "//div[contains(@class, 'error-message-container')]/h3")

    def get_page_title_text(self) -> str:
        return self._get_text(self.PAGE_TITLE)
    
    def is_checkout_step_one_page_displayed(self) -> bool:
        return self._is_displayed(self.PAGE_TITLE) and self.get_page_title_text() == "Checkout: Your Information"
    
    def enter_first_name(self, first_name: str):
        self._type_text(self.FIRST_NAME_INPUT, first_name)
    
    def enter_last_name(self, last_name: str):
        self._type_text(self.LAST_NAME_INPUT, last_name)
    
    def enter_postal_code(self, postal_code: str):
        self._type_text(self.POSTAL_CODE_INPUT, postal_code)
    
    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str):
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)

    def click_continue(self):
        self._click(self.CONTINUE_BUTTON)

    def click_cancel(self):
        self._click(self.CANCEL_BUTTON)

    def get_error_message(self) -> str:
        if self._is_displayed(self.ERROR_MESSAGE_CONTAINER):
            return self._get_text(self.ERROR_MESSAGE_CONTAINER)
        return ""
    


