from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckoutStepTwoPage(BasePage):
    PAGE_TITLE = (By.CLASS_NAME, "title") # "Checkout: Overview"
    CART_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    FINISH_BUTTON = (By.ID, "finish")
    CANCEL_BUTTON = (By.ID, "cancel")
    SUMMARY_SUBTOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    SUMMARY_TAX_LABEL = (By.CLASS_NAME, "summary_tax_label")
    SUMMARY_TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    PAYMENT_INFO_VALUE = (By.XPATH, "//div[@class='summary_info_label' and text()='Payment Information']/following-sibling::div[@class='summary_value_label']")
    SHIPPING_INFO_VALUE = (By.XPATH, "//div[@class='summary_info_label' and text()='Shipping Information']/following-sibling::div[@class='summary_value_label']")

    def get_page_title_text(self) -> str:
        return self._get_text(self.PAGE_TITLE)

    def is_checkout_overview_page_displayed(self) -> bool:
        return self._is_displayed(self.PAGE_TITLE) and self.get_page_title_text() == "Checkout: Overview"

    def get_item_names_in_overview(self) -> list[str]:
        item_elements = self._find_elements(self.CART_ITEM_NAME)
        return [element.text for element in item_elements]

    def click_finish(self):
        self._click(self.FINISH_BUTTON)

    def click_cancel(self):
        self._click(self.CANCEL_BUTTON)

    def get_subtotal(self) -> float:
        text = self._get_text(self.SUMMARY_SUBTOTAL_LABEL) # "Item total: $X.XX"
        return float(text.split("$")[-1])

    def get_tax(self) -> float:
        text = self._get_text(self.SUMMARY_TAX_LABEL) # "Tax: $X.XX"
        return float(text.split("$")[-1])

    def get_total(self) -> float:
        text = self._get_text(self.SUMMARY_TOTAL_LABEL) # "Total: $X.XX"
        return float(text.split("$")[-1])

    def get_payment_information(self) -> str:
        return self._get_text(self.PAYMENT_INFO_VALUE)

    def get_shipping_information(self) -> str:
        return self._get_text(self.SHIPPING_INFO_VALUE)