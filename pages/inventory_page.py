from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage

class InventoryPage(BasePage):
    #Locators
    PAGE_TITLE = (By.CLASS_NAME, "title") # Expect "Products"
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")

    ADD_SAUCE_LABS_BACKPACK_TO_CART_BTN = (By.ID, "add-to-cart-sauce-labs-backpack")
    REMOVE_SAUCE_LABS_BACKPACK_FROM_CART_BTN = (By.ID, "remove-sauce-labs-backpack")

    def __init__(self, driver):
        super().__init__(driver)
        self.expected_path_segment = "inventory.html"
    
    def is_on_inventory_page(self) -> bool:
        if self.expected_path_segment not in self._get_current_url():
            return False
        try:
            return self._get_text(self.PAGE_TITLE) == "Products"
        except:
             return False
    
    def get_product_count(self) -> int:
        return len(self._find_elements(self.INVENTORY_ITEMS))