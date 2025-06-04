from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage

class InventoryPage(BasePage):
    #Locators
    PAGE_TITLE = (By.CLASS_NAME, "title") # "Products"
    SHOPPING_CART_ICON = (By.ID, "shopping_cart_container")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    PRODUCT_SORT_CONTAINER = (By.CLASS_NAME, "product_sort_container")
    BURGER_MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")
    INVENTORY_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ADD_TO_CART_BUTTON_PREFIX = "add-to-cart-" # e.g., add-to-cart-sauce-labs-backpack
    REMOVE_BUTTON_PREFIX = "remove-" 

    def __init__(self, driver):
        super().__init__(driver)
        self.expected_path_segment = "inventory.html"
    
    def get_page_title_text(self) -> str:
        return self._get_text(self.PAGE_TITLE)
    
    def is_on_inventory_page(self) -> bool:
        return self._is_displayed(self.PAGE_TITLE) and self.get_page_title_text() == "Products"
    
    def get_item_count(self) -> int:
        return len(self._find_elements(self.INVENTORY_ITEM))
    
    def add_item_to_cart_by_name(self, item_name: str):
        # For simplicity, using a specific for one product for now

        item_id_suffix = item_name.lower().replace(" ", "-") # "Sauce Labs Backpack" -> "sauce-labs-backpack"
        add_to_cart_btn_locator = (By.ID, f"{self.ADD_TO_CART_BUTTON_PREFIX}{item_id_suffix}")
        self._click(add_to_cart_btn_locator)
        
    def remove_product_from_cart_by_name(self, item_name: str):
        item_id_suffix = item_name.lower().replace(" ", "-")
        remove_from_cart_btn_locator = (By.ID, f"{self.REMOVE_BUTTON_PREFIX}{item_id_suffix}")
        self._click(remove_from_cart_btn_locator)
    
    def get_cart_badge_count(self) -> int:
        if self._is_displayed(self.SHOPPING_CART_BADGE, timeout=1):
            return int(self._get_text(self.SHOPPING_CART_BADGE))
        return 0
    
    def go_to_cart(self):
        self._click(self.SHOPPING_CART_ICON)
    
    def get_product_names(self) -> list[str]:
        product_elements = self._find_elements(self.INVENTORY_ITEM_NAME)
        return [element.text for element in product_elements]
    
    def get_product_prices(self) -> list[float]:
        price_elements =  self._find_elements((By.CLASS_NAME, "inventory_item_price"))
        return [float(element.replace("$","")) for element in price_elements]
    
    def open_burger_menu(self):
        self._click(self.BURGER_MENU_BUTTON)

    def get_item_details(self, item_element: WebElement) -> dict:
        name = item_element.find_element(By.CLASS_NAME, "inventory_item_name").text
        desc = item_element.find_element(By.CLASS_NAME, "inventory_item_desc").text
        price_str = item_element.find_element(By.CLASS_NAME, "inventory_item_price").text
        price = float(price_str.replace("$", ""))

        return {"name": name, "description": desc, "price": price}
    
    def click_logout(self):
        if not self._is_displayed(self.LOGOUT_LINK, timeout=1):
            self.open_burger_menu()
        self._click(self.LOGOUT_LINK)