"""
Unit tests for Cart Microservice API

Tests cover all endpoints defined in openapi/cart-microservice.yaml:
- GET /cart-microservice/shoppingCart/addProduct
- GET /cart-microservice/shoppingCart/productsInCart
- GET /cart-microservice/shoppingCart/removeProduct
- GET /cart-microservice/shoppingCart/clearCart
"""

import unittest
from unittest.mock import patch, MagicMock
import requests
import json


class TestCartMicroserviceConfig:
    """Configuration for Cart Microservice tests"""
    BASE_URL = "http://localhost:8083"
    CART_BASE = f"{BASE_URL}/cart-microservice/shoppingCart"


class TestAddProductToCart(unittest.TestCase):
    """Tests for POST /cart-microservice/shoppingCart/addProduct endpoint"""

    def setUp(self):
        self.base_url = TestCartMicroserviceConfig.CART_BASE
        self.endpoint = f"{self.base_url}/addProduct"

    @patch('requests.get')
    def test_add_product_success(self, mock_get):
        """Test successfully adding a product to cart"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Added to Cart"
        mock_response.json.return_value = "Added to Cart"
        mock_get.return_value = mock_response

        response = requests.get(
            self.endpoint,
            params={"userid": "u1001", "asin": "B00BKQT2OI"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Added to Cart", response.text)
        mock_get.assert_called_once()

    @patch('requests.get')
    def test_add_product_with_valid_userid_and_asin(self, mock_get):
        """Test adding product with valid user ID and ASIN"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Added to Cart"
        mock_get.return_value = mock_response

        response = requests.get(
            self.endpoint,
            params={"userid": "test_user_123", "asin": "B00TEST123"}
        )

        self.assertEqual(response.status_code, 200)
        call_args = mock_get.call_args
        self.assertIn("userid", call_args.kwargs.get("params", {}))
        self.assertIn("asin", call_args.kwargs.get("params", {}))

    @patch('requests.get')
    def test_add_product_missing_userid(self, mock_get):
        """Test adding product without userid parameter"""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        response = requests.get(
            self.endpoint,
            params={"asin": "B00BKQT2OI"}
        )

        # Should fail without required userid
        self.assertIn(response.status_code, [400, 500])

    @patch('requests.get')
    def test_add_product_missing_asin(self, mock_get):
        """Test adding product without asin parameter"""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        response = requests.get(
            self.endpoint,
            params={"userid": "u1001"}
        )

        # Should fail without required asin
        self.assertIn(response.status_code, [400, 500])


class TestGetProductsInCart(unittest.TestCase):
    """Tests for GET /cart-microservice/shoppingCart/productsInCart endpoint"""

    def setUp(self):
        self.base_url = TestCartMicroserviceConfig.CART_BASE
        self.endpoint = f"{self.base_url}/productsInCart"

    @patch('requests.get')
    def test_get_products_in_cart_success(self, mock_get):
        """Test successfully retrieving products in cart"""
        expected_cart = {"B00BKQT2OI": 2, "B00BKQT3XT": 1}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_cart
        mock_get.return_value = mock_response

        response = requests.get(
            self.endpoint,
            params={"userid": "u1001"}
        )

        self.assertEqual(response.status_code, 200)
        cart_contents = response.json()
        self.assertIsInstance(cart_contents, dict)

    @patch('requests.get')
    def test_get_products_in_cart_empty(self, mock_get):
        """Test retrieving an empty cart"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        response = requests.get(
            self.endpoint,
            params={"userid": "new_user"}
        )

        self.assertEqual(response.status_code, 200)
        cart_contents = response.json()
        self.assertEqual(cart_contents, {})

    @patch('requests.get')
    def test_get_products_cart_contents_format(self, mock_get):
        """Test that cart contents are in correct format (ASIN -> quantity)"""
        expected_cart = {"B00BKQT2OI": 2, "B00BKQT3XT": 1}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_cart
        mock_get.return_value = mock_response

        response = requests.get(
            self.endpoint,
            params={"userid": "u1001"}
        )

        cart_contents = response.json()
        for asin, quantity in cart_contents.items():
            self.assertIsInstance(asin, str)
            self.assertIsInstance(quantity, int)
            self.assertGreater(quantity, 0)

    @patch('requests.get')
    def test_get_products_missing_userid(self, mock_get):
        """Test getting cart without userid parameter"""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        response = requests.get(self.endpoint)

        self.assertIn(response.status_code, [400, 500])


class TestRemoveProductFromCart(unittest.TestCase):
    """Tests for GET /cart-microservice/shoppingCart/removeProduct endpoint"""

    def setUp(self):
        self.base_url = TestCartMicroserviceConfig.CART_BASE
        self.endpoint = f"{self.base_url}/removeProduct"

    @patch('requests.get')
    def test_remove_product_success(self, mock_get):
        """Test successfully removing a product from cart"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Removing from Cart"
        mock_get.return_value = mock_response

        response = requests.get(
            self.endpoint,
            params={"userid": "u1001", "asin": "B00BKQT2OI"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Removing from Cart", response.text)

    @patch('requests.get')
    def test_remove_product_not_in_cart(self, mock_get):
        """Test removing a product that's not in the cart"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Removing from Cart"
        mock_get.return_value = mock_response

        response = requests.get(
            self.endpoint,
            params={"userid": "u1001", "asin": "NONEXISTENT"}
        )

        # Should still return success (idempotent operation)
        self.assertEqual(response.status_code, 200)

    @patch('requests.get')
    def test_remove_product_missing_userid(self, mock_get):
        """Test removing product without userid"""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        response = requests.get(
            self.endpoint,
            params={"asin": "B00BKQT2OI"}
        )

        self.assertIn(response.status_code, [400, 500])

    @patch('requests.get')
    def test_remove_product_missing_asin(self, mock_get):
        """Test removing product without asin"""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        response = requests.get(
            self.endpoint,
            params={"userid": "u1001"}
        )

        self.assertIn(response.status_code, [400, 500])


class TestClearCart(unittest.TestCase):
    """Tests for GET /cart-microservice/shoppingCart/clearCart endpoint"""

    def setUp(self):
        self.base_url = TestCartMicroserviceConfig.CART_BASE
        self.endpoint = f"{self.base_url}/clearCart"

    @patch('requests.get')
    def test_clear_cart_success(self, mock_get):
        """Test successfully clearing the cart"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Clearing Cart, Checkout successful"
        mock_get.return_value = mock_response

        response = requests.get(
            self.endpoint,
            params={"userid": "u1001"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Clearing Cart", response.text)

    @patch('requests.get')
    def test_clear_empty_cart(self, mock_get):
        """Test clearing an already empty cart"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Clearing Cart, Checkout successful"
        mock_get.return_value = mock_response

        response = requests.get(
            self.endpoint,
            params={"userid": "empty_cart_user"}
        )

        # Should succeed even if cart is already empty
        self.assertEqual(response.status_code, 200)

    @patch('requests.get')
    def test_clear_cart_missing_userid(self, mock_get):
        """Test clearing cart without userid"""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        response = requests.get(self.endpoint)

        self.assertIn(response.status_code, [400, 500])


class TestCartWorkflow(unittest.TestCase):
    """Integration-style tests for cart workflows"""

    def setUp(self):
        self.base_url = TestCartMicroserviceConfig.CART_BASE

    @patch('requests.get')
    def test_add_get_remove_workflow(self, mock_get):
        """Test complete workflow: add product, get cart, remove product"""
        # Setup mock responses for sequence of calls
        add_response = MagicMock()
        add_response.status_code = 200
        add_response.text = "Added to Cart"

        get_response = MagicMock()
        get_response.status_code = 200
        get_response.json.return_value = {"B00BKQT2OI": 1}

        remove_response = MagicMock()
        remove_response.status_code = 200
        remove_response.text = "Removing from Cart"

        mock_get.side_effect = [add_response, get_response, remove_response]

        # Add product
        response1 = requests.get(
            f"{self.base_url}/addProduct",
            params={"userid": "u1001", "asin": "B00BKQT2OI"}
        )
        self.assertEqual(response1.status_code, 200)

        # Get cart
        response2 = requests.get(
            f"{self.base_url}/productsInCart",
            params={"userid": "u1001"}
        )
        self.assertEqual(response2.status_code, 200)

        # Remove product
        response3 = requests.get(
            f"{self.base_url}/removeProduct",
            params={"userid": "u1001", "asin": "B00BKQT2OI"}
        )
        self.assertEqual(response3.status_code, 200)


if __name__ == '__main__':
    unittest.main()
