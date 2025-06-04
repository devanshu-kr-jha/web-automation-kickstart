from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckoutCompletePage(BasePage):
    PAGE_TITLE = (By.CLASS_NAME, "title") # "Checkout: Complete!"
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header") # "Thank you for your order!"
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    def get_page_title_text(self) -> str:
        return self._get_text(self.PAGE_TITLE)

    def is_checkout_complete_page_displayed(self) -> bool:
        return self._is_displayed(self.PAGE_TITLE) and self.get_page_title_text() == "Checkout: Complete!"

    def get_complete_header_message(self) -> str:
        return self._get_text(self.COMPLETE_HEADER)

    def click_back_home(self):
        self._click(self.BACK_HOME_BUTTON)