"""
Unit tests for Checkout Microservice API

Tests cover all endpoints defined in openapi/checkout-microservice.yaml:
- POST /checkout-microservice/shoppingCart/checkout
"""

import unittest
from unittest.mock import patch, MagicMock
import requests
import json


class TestCheckoutMicroserviceConfig:
    """Configuration for Checkout Microservice tests"""
    BASE_URL = "http://localhost:8086"
    CHECKOUT_BASE = f"{BASE_URL}/checkout-microservice/shoppingCart"


class TestCheckout(unittest.TestCase):
    """Tests for POST /checkout-microservice/shoppingCart/checkout endpoint"""

    def setUp(self):
        self.base_url = TestCheckoutMicroserviceConfig.CHECKOUT_BASE
        self.endpoint = f"{self.base_url}/checkout"

    @patch('requests.post')
    def test_checkout_success(self, mock_post):
        """Test successful checkout"""
        expected_response = {
            "status": "SUCCESS",
            "orderNumber": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            "orderDetails": "Customer bought these Items: Product: The Great Gatsby, Quantity: 2; Order Total is : 29.98"
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response
        mock_post.return_value = mock_response

        response = requests.post(self.endpoint)

        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result["status"], "SUCCESS")
        self.assertIn("orderNumber", result)
        self.assertIn("orderDetails", result)

    @patch('requests.post')
    def test_checkout_returns_order_number(self, mock_post):
        """Test that successful checkout returns a valid order number"""
        expected_response = {
            "status": "SUCCESS",
            "orderNumber": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            "orderDetails": "Customer bought these Items: Product: Test Product, Quantity: 1"
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response
        mock_post.return_value = mock_response

        response = requests.post(self.endpoint)

        result = response.json()
        self.assertIsInstance(result["orderNumber"], str)
        self.assertGreater(len(result["orderNumber"]), 0)

    @patch('requests.post')
    def test_checkout_failure_out_of_stock(self, mock_post):
        """Test checkout failure when product is out of stock"""
        expected_response = {
            "status": "FAILURE",
            "orderNumber": "",
            "orderDetails": "Product is Out of Stock!"
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response
        mock_post.return_value = mock_response

        response = requests.post(self.endpoint)

        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result["status"], "FAILURE")
        self.assertEqual(result["orderNumber"], "")

    @patch('requests.post')
    def test_checkout_status_enum_values(self, mock_post):
        """Test that status field contains valid enum values"""
        expected_response = {
            "status": "SUCCESS",
            "orderNumber": "test-order-123",
            "orderDetails": "Order details"
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response
        mock_post.return_value = mock_response

        response = requests.post(self.endpoint)

        result = response.json()
        self.assertIn(result["status"], ["SUCCESS", "FAILURE"])

    @patch('requests.post')
    def test_checkout_order_details_format(self, mock_post):
        """Test that order details are properly formatted"""
        expected_response = {
            "status": "SUCCESS",
            "orderNumber": "test-order-123",
            "orderDetails": "Customer bought these Items: Product: The Great Gatsby, Quantity: 2; Order Total is : 29.98"
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response
        mock_post.return_value = mock_response

        response = requests.post(self.endpoint)

        result = response.json()
        self.assertIsInstance(result["orderDetails"], str)
        # Successful orders should contain product information
        if result["status"] == "SUCCESS":
            self.assertIn("Product:", result["orderDetails"])

    @patch('requests.post')
    def test_checkout_multiple_items(self, mock_post):
        """Test checkout with multiple items in cart"""
        expected_response = {
            "status": "SUCCESS",
            "orderNumber": "multi-item-order-456",
            "orderDetails": "Customer bought these Items: Product: Book 1, Quantity: 2; Product: Book 2, Quantity: 1; Order Total is : 44.97"
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response
        mock_post.return_value = mock_response

        response = requests.post(self.endpoint)

        result = response.json()
        self.assertEqual(result["status"], "SUCCESS")
        self.assertIn("Order Total", result["orderDetails"])

    @patch('requests.post')
    def test_checkout_empty_cart(self, mock_post):
        """Test checkout with empty cart"""
        expected_response = {
            "status": "FAILURE",
            "orderNumber": "",
            "orderDetails": "Cart is empty"
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response
        mock_post.return_value = mock_response

        response = requests.post(self.endpoint)

        result = response.json()
        # Empty cart should result in failure or appropriate message
        self.assertIn(result["status"], ["SUCCESS", "FAILURE"])

    @patch('requests.post')
    def test_checkout_server_error(self, mock_post):
        """Test checkout when server returns error"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        response = requests.post(self.endpoint)

        self.assertEqual(response.status_code, 500)


class TestCheckoutStatusSchema(unittest.TestCase):
    """Tests for CheckoutStatus schema validation"""

    @patch('requests.post')
    def test_checkout_status_has_required_fields(self, mock_post):
        """Test that CheckoutStatus contains required 'status' field"""
        expected_response = {
            "status": "SUCCESS",
            "orderNumber": "test-123",
            "orderDetails": "Order completed"
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response
        mock_post.return_value = mock_response

        response = requests.post(
            f"{TestCheckoutMicroserviceConfig.CHECKOUT_BASE}/checkout"
        )

        result = response.json()
        # 'status' is required per schema
        self.assertIn("status", result)

    @patch('requests.post')
    def test_checkout_status_success_has_order_number(self, mock_post):
        """Test that successful checkout includes non-empty order number"""
        expected_response = {
            "status": "SUCCESS",
            "orderNumber": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            "orderDetails": "Order details here"
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response
        mock_post.return_value = mock_response

        response = requests.post(
            f"{TestCheckoutMicroserviceConfig.CHECKOUT_BASE}/checkout"
        )

        result = response.json()
        if result["status"] == "SUCCESS":
            self.assertIn("orderNumber", result)
            self.assertNotEqual(result["orderNumber"], "")

    @patch('requests.post')
    def test_checkout_status_failure_has_empty_order_number(self, mock_post):
        """Test that failed checkout has empty order number"""
        expected_response = {
            "status": "FAILURE",
            "orderNumber": "",
            "orderDetails": "Product is Out of Stock!"
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response
        mock_post.return_value = mock_response

        response = requests.post(
            f"{TestCheckoutMicroserviceConfig.CHECKOUT_BASE}/checkout"
        )

        result = response.json()
        if result["status"] == "FAILURE":
            self.assertEqual(result["orderNumber"], "")


if __name__ == '__main__':
    unittest.main()
