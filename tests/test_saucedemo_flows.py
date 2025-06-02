import pytest

@pytest.mark.login
class TestLogin:
    @pytest.mark.smoke
    def test_successful_login(self, login_page, inventory_page, standard_user_credentials):
        login_page.login(standard_user_credentials["username"], standard_user_credentials["password"])
        assert inventory_page.is_on_inventory_page(), "Login failed or did not redirect to inventory page."
        assert inventory_page.get_product_count() > 0, "No products found on inventory page."


    def test_locked_out_user_login(self, login_page, inventory_page, locked_out_user_credentials):
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
    def test_invalid_login_attempt(self, login_page, username, password, expected_error):
        login_page.login(username, password)
        error_message = login_page.get_error_message()
        assert error_message is not None, f"Error message not displayed for user: {username}, pass: {password}"
        assert expected_error in error_message, f"Incorrect error message. Expected message: {expected_error}, Received: {error_message}"
        assert "inventory.html" not in login_page._get_current_url(), "Should not redirect on failed login."




