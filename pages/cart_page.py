from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage

class CartPage(BasePage):
    PAGE_TITLE = (By.CLASS_NAME, "title") # "Your Cart"
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    CART_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    REMOVE_BUTTON_PREFIX = "remove-"

    def get_page_title_text(self) -> str:
        return self._get_text(self.PAGE_TITLE)
    
    def is_cart_page_displayed(self) -> bool:
        return self._is_displayed(self.PAGE_TITLE) and self.get_page_title_text() == "Your Cart"
    
    def get_item_names_in_cart(self) -> list[str]:
        item_elements = self._find_elements(self.CART_ITEM_NAME)
        return [element.text for element in item_elements]
    
    def remove_item_from_cart_by_name(self, item_name: str):
        item_id_suffix = item_name.lower().replace(" ", "-")
        remove_button_locator = (By.ID, f"{self.REMOVE_BUTTON_PREFIX}{item_id_suffix}")
        self._click(remove_button_locator)
    
    def proceed_to_checkout(self):
        self._click(self.CHECKOUT_BUTTON)
    
    def continue_shopping(self):
        self._click(self.CONTINUE_SHOPPING_BUTTON)


    