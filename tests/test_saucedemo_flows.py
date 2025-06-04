import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_step_one import CheckoutStepOnePage
from pages.checkout_step_two import CheckoutStepTwoPage
from pages.checkout_complete import CheckoutCompletePage

PRODUCT_1_NAME = "Sauce Labs Backpack"
PRODUCT_2_NAME = "Sauce Labs Bike Light"
CHECKOUT_INFO = {"first_name": "Test", "last_name": "User", "postal_code": "12345"}

@pytest.mark.login
class TestLogin:
    @pytest.mark.smoke
    def test_successful_login(self, login_page: LoginPage, inventory_page: InventoryPage, standard_user_credentials):
        login_page.login(standard_user_credentials["username"], standard_user_credentials["password"])
        assert inventory_page.is_on_inventory_page(), "Login failed or did not redirect to inventory page."
        assert inventory_page.get_item_count() > 0, "No products found on inventory page."


    def test_locked_out_user_login(self, login_page: LoginPage, inventory_page: InventoryPage, locked_out_user_credentials):
        login_page.login(locked_out_user_credentials["username"], locked_out_user_credentials["password"])
        error_message = login_page.get_error_message()
        assert error_message is not None, "Error message not displayed for locked out user"
        assert "Sorry, this user has been locked out." in error_message, "Incorrect error message."
        assert "inventory.html" not in login_page._get_current_url(), "Should not redirect on failed login."
    
    @pytest.mark.parametrize("username, password, expected_error", [
        ("wronguser", "secretsauce", "Username and password do not match"),
        ("standard_user", "wrongpassword", "Username and password do not match"),
        ("", "secretsauce", "Username is required"),
        ("standard_user", "", "Password is required"),
    ])
    def test_invalid_login_attempt(self, login_page: LoginPage, username, password, expected_error):
        login_page.login(username, password)
        error_message = login_page.get_error_message()
        assert error_message is not None, f"Error message not displayed for user: {username}, pass: {password}"
        assert expected_error in error_message, f"Incorrect error message. Expected message: {expected_error}, Received: {error_message}"
        assert "inventory.html" not in login_page._get_current_url(), "Should not redirect on failed login."

@pytest.mark.inventory
class TestInventoryActions:
    @pytest.mark.regression
    def test_add_single_item_to_cart(self, logged_in_standard_user, cart_page: CartPage):
        inventory_page: InventoryPage = logged_in_standard_user

        initial_cart_count = inventory_page.get_cart_badge_count()
        inventory_page.add_item_to_cart_by_name(PRODUCT_1_NAME)
        assert inventory_page.get_cart_badge_count() == initial_cart_count+1, "Cart count did not update correctly."

        inventory_page.go_to_cart()
        assert cart_page.is_cart_page_displayed(), "Not on cart after navigating."
        cart_items = cart_page.get_item_names_in_cart()
        assert PRODUCT_1_NAME in cart_items, f"{PRODUCT_1_NAME} not found in cart."
        assert len(cart_items) == 1, "Incorrect number of items in cart."

    @pytest.mark.regression
    def test_add_multiple_items_to_cart(self, logged_in_standard_user, cart_page: CartPage):
        inventory_page: InventoryPage = logged_in_standard_user
        
        inventory_page.add_item_to_cart_by_name(PRODUCT_1_NAME)
        inventory_page.add_item_to_cart_by_name(PRODUCT_2_NAME)
        assert inventory_page.get_cart_badge_count() == 2, "Cart badge count incorrect for multiple items."

        inventory_page.go_to_cart()
        assert cart_page.is_cart_page_displayed(), "Not on the cart page."
        cart_items = cart_page.get_item_names_in_cart()
        assert PRODUCT_1_NAME in cart_items, f"{PRODUCT_1_NAME} not found in cart."
        assert PRODUCT_2_NAME in cart_items, f"{PRODUCT_2_NAME} not found in cart."
        assert len(cart_items) == 2, "Incorrect number of items in cart."

@pytest.mark.cart
class TestCartActions:
    @pytest.mark.regression
    def test_remove_item_from_cart_page(self, logged_in_standard_user, cart_page: CartPage):
        inventory_page: InventoryPage = logged_in_standard_user
        inventory_page.add_item_to_cart_by_name(PRODUCT_1_NAME)
        inventory_page.add_item_to_cart_by_name(PRODUCT_2_NAME)
        
        inventory_page.go_to_cart()
        assert cart_page.is_cart_page_displayed(), "Not on the cart page."
        assert len(cart_page.get_item_names_in_cart()) == 2, "Initial cart count incorrect on cart page."
        
        cart_page.remove_item_from_cart_by_name(PRODUCT_1_NAME)
        cart_items_after_removal = cart_page.get_item_names_in_cart()
        
        assert PRODUCT_1_NAME not in cart_items_after_removal, f"{PRODUCT_1_NAME} was not removed from cart."
        assert PRODUCT_2_NAME in cart_items_after_removal, f"{PRODUCT_2_NAME} should still be in cart."
        assert len(cart_items_after_removal) == 1, "Incorrect number of items after removal from cart page."
        
        cart_page.continue_shopping() # Navigate back to inventory
        assert inventory_page.is_inventory_page_displayed(), "Not back on inventory page."
        assert inventory_page.get_cart_badge_count() == 1, "Cart badge on inventory page not updated after removal."

@pytest.mark.checkout
class TestCheckoutValidations:
    @pytest.fixture(autouse=True) 
    def test_navigate_to_checkout_step_one(self, logged_in_standard_user, cart_page: CartPage):
        self.inventory_page: InventoryPage = logged_in_standard_user
        self.inventory_page.add_item_to_cart_by_name(PRODUCT_1_NAME)
        self.inventory_page.go_to_cart()
        cart_page.proceed_to_checkout()
    
    @pytest.mark.parametrize("first_name, last_name, postal_code, expected_error", [
        ("", "User", "12345", "Error: First Name is required"),
        ("Test", "", "12345", "Error: Last Name is required"),
        ("Test", "User", "", "Error: Postal Code is required"),
    ])
    def test_checkout_info_missinf_fields(self, checkout_step_one_page: CheckoutStepOnePage, first_name, last_name, postal_code, expected_error):
        checkout_step_one_page.fill_checkout_info(first_name, last_name, postal_code)
        checkout_step_one_page.click_continue()
        
        error_message = checkout_step_one_page.get_error_message()
        assert error_message, "Error message not displayed for missing checkout info."
        assert expected_error in error_message, \
            f"Incorrect error. Expected: '{expected_error}', Got: '{error_message}'"
        assert checkout_step_one_page.is_checkout_step_one_page_displayed(), "Should remain on checkout step one page."

@pytest.mark.e2e
class TestEndToEndPurchase:
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_full_e2e_purchase_flow_single_item(
        self, logged_in_standard_user, cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
        checkout_step_two_page: CheckoutStepTwoPage,
        checkout_complete_page: CheckoutCompletePage
    ):
        """Verifies the complete end-to-end purchase flow for a single item."""
        inventory_page: InventoryPage = logged_in_standard_user

        # 1. Add item to cart from Inventory Page
        inventory_page.add_item_to_cart_by_name(PRODUCT_1_NAME)
        assert inventory_page.get_cart_badge_count() == 1, "Cart badge incorrect after adding item."

        # 2. Go to Cart Page and verify item
        inventory_page.go_to_cart()
        assert cart_page.is_cart_page_displayed(), "Not on Cart Page."
        assert PRODUCT_1_NAME in cart_page.get_item_names_in_cart(), f"{PRODUCT_1_NAME} not in cart."

        # 3. Proceed to Checkout Step One Page
        cart_page.proceed_to_checkout()
        assert checkout_step_one_page.is_checkout_step_one_page_displayed(), "Not on Checkout Step One page."

        # 4. Fill checkout information and continue
        checkout_step_one_page.fill_checkout_info(
            CHECKOUT_INFO["first_name"], CHECKOUT_INFO["last_name"], CHECKOUT_INFO["postal_code"]
        )
        checkout_step_one_page.click_continue()
        assert checkout_step_two_page.is_checkout_overview_page_displayed(), "Not on Checkout Overview page."

        # 5. Verify item on Overview Page and Finish
        assert PRODUCT_1_NAME in checkout_step_two_page.get_item_names_in_overview(), f"{PRODUCT_1_NAME} not in overview." 
        checkout_step_two_page.click_finish()
        assert checkout_complete_page.is_checkout_complete_page_displayed(), "Not on Checkout Complete page."

        # 6. Verify completion message
        assert "Thank you for your order!" in checkout_complete_page.get_complete_header_message(), \
            "Incorrect completion message."

        # 7. Go back home and verify cart is empty
        checkout_complete_page.click_back_home()
        assert inventory_page.is_inventory_page_displayed(), "Not back on Inventory Page."
        assert inventory_page.get_cart_badge_count() == 0, "Cart should be empty after completing order."


