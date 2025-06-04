from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class BasePage:
    """
    Base class for all Page Objects
    It contians common methods for interacting with web elements
    """
    def __init__(self, driver: WebDriver, base_url="https://www.saucedemo.com/"):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.base_url = base_url
    
    def _find_element(self, locator: tuple, timeout: int = 10) -> WebElement:
        """Finds element with explicit wait"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            raise TimeoutException(f"Element with locator {locator} not found within {timeout} seconds.")
    
    def _find_elements(self, locator: tuple, timeout: int = 10) -> list[WebElement]:
        """Finds multiple web elements within explicit wait"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_all_elements_located(locator)
            )
        except:
            print(f"Elements with locator {locator} not found within {timeout} seconds.")
            return []
    
    def _click(self, locator: tuple, timeout: int = 10):
        """Clicks a web element after ensuirng it's clickable"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
        except TimeoutException:
            raise TimeoutException("Element with locator {locator} not clickable within {timeout} seconds.")
    
    def _type_text(self, locator: tuple, text: str, timeout: int = 10):
        """Types text into a web element"""
        element = self._find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
    
    def _get_text(self, locator: tuple, timeout: int = 10) -> str:
        """Gets the text of web element"""
        element = self._find_element(locator, timeout)
        return element.text
    
    def _is_displayed(self, locator: tuple, timeout: int = 2) -> bool:
        """Checks if a web element is displayed"""
        try:
            return self._find_element(locator, timeout).is_displayed()
        except TimeoutException:
            return False
        except NoSuchElementException:
            return False
        
    def _get_current_url(self) -> str:
        return self.driver.current_url
    
    def _get_page_title(self) -> str:
        return self.driver.title
    
    def navigate_to(self, path: str = ""):
        self.driver.get(self.base_url + path)
    
    def _get_element_attribute(self, locator: tuple, attribute_name: str, timeout: int = 10) -> str:
        """Gets an attribute value from a web element."""
        element = self._find_element(locator, timeout)
        return element.get_attribute(attribute_name)

    def _select_dropdown_by_visible_text(self, locator: tuple, text: str, timeout: int = 10):
        """Selects an option from a dropdown by its visible text."""
        from selenium.webdriver.support.ui import Select # Local import to avoid circular dependency if Select is widely used
        element = self._find_element(locator, timeout)
        select = Select(element)
        select.select_by_visible_text(text)

    def _select_dropdown_by_value(self, locator: tuple, value: str, timeout: int = 10):
        """Selects an option from a dropdown by its value attribute."""
        from selenium.webdriver.support.ui import Select
        element = self._find_element(locator, timeout)
        select = Select(element)
        select.select_by_value(value)
        
    