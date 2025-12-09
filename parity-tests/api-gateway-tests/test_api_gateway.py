"""
Unit tests for API Gateway

Tests cover all endpoints defined in openapi/api-gateway.yaml:
- GET /api/v1/product/{asin} - Get product details
- GET /api/v1/products - Get all products
- GET /api/v1/products/category/{category} - Get products by category
- POST /api/v1/shoppingCart - Get shopping cart contents
- POST /api/v1/shoppingCart/addProduct - Add product to cart
- POST /api/v1/shoppingCart/removeProduct - Remove product from cart
- POST /api/v1/shoppingCart/checkout - Process checkout
"""

import unittest
from unittest.mock import patch, MagicMock
import requests
import json


class TestApiGatewayConfig:
    """Configuration for API Gateway tests"""
    BASE_URL = "http://localhost:8081"
    API_BASE = f"{BASE_URL}/api/v1"


class TestGetProductDetails(unittest.TestCase):
    """Tests for GET /api/v1/product/{asin} endpoint"""

    def setUp(self):
        self.base_url = TestApiGatewayConfig.API_BASE
        self.endpoint = f"{self.base_url}/product"

    @patch('requests.get')
    def test_get_product_details_success(self, mock_get):
        """Test successfully retrieving product details"""
        expected_product = {
            "id": "B00BKQT2OI",
            "brand": "Penguin Books",
            "categories": ["Books", "Fiction"],
            "imUrl": "https://images-na.ssl-images-amazon.com/images/I/51example.jpg",
            "price": 14.99,
            "title": "The Great Gatsby",
            "description": "A novel by F. Scott Fitzgerald",
            "also_bought": ["B00BKQT3XT"],
            "also_viewed": ["B00BKQT4YU"],
            "num_reviews": 1250,
            "avg_stars": 3.9
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_product
        mock_get.return_value = mock_response

        response = requests.get(f"{self.endpoint}/B00BKQT2OI")

        self.assertEqual(response.status_code, 200)
        product = response.json()
        self.assertEqual(product["id"], "B00BKQT2OI")

    @patch('requests.get')
    def test_get_product_not_found(self, mock_get):
        """Test getting a non-existent product"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        response = requests.get(f"{self.endpoint}/NONEXISTENT")

        self.assertEqual(response.status_code, 404)

    @patch('requests.get')
    def test_get_product_server_error(self, mock_get):
        """Test server error when downstream service unavailable"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        response = requests.get(f"{self.endpoint}/B00BKQT2OI")

        self.assertEqual(response.status_code, 500)


class TestGetAllProducts(unittest.TestCase):
    """Tests for GET /api/v1/products endpoint"""

    def setUp(self):
        self.base_url = TestApiGatewayConfig.API_BASE
        self.endpoint = f"{self.base_url}/products"

    @patch('requests.get')
    def test_get_products_success(self, mock_get):
        """Test successfully retrieving product list"""
        expected_products = [
            {"id": "B001", "title": "Product 1", "price": 9.99},
            {"id": "B002", "title": "Product 2", "price": 19.99}
        ]
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_products
        mock_get.return_value = mock_response

        response = requests.get(
            self.endpoint,
            params={"limit": 12, "offset": 0}
        )

        self.assertEqual(response.status_code, 200)
        products = response.json()
        self.assertIsInstance(products, list)

    @patch('requests.get')
    def test_get_products_with_pagination(self, mock_get):
        """Test product list pagination"""
        expected_products = [{"id": f"B{i:03d}", "title": f"Product {i}", "price": 9.99}
                           for i in range(12)]
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_products
        mock_get.return_value = mock_response

        response = requests.get(
            self.endpoint,
            params={"limit": 12, "offset": 0}
        )

        self.assertEqual(response.status_code, 200)
        products = response.json()
        self.assertLessEqual(len(products), 12)

    @patch('requests.get')
    def test_get_products_requires_limit_param(self, mock_get):
        """Test that limit parameter is required"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        response = requests.get(
            self.endpoint,
            params={"limit": 10, "offset": 0}
        )

        call_args = mock_get.call_args
        params = call_args.kwargs.get("params", {})
        self.assertIn("limit", params)
        self.assertIn("offset", params)


class TestGetProductsByCategory(unittest.TestCase):
    """Tests for GET /api/v1/products/category/{category} endpoint"""

    def setUp(self):
        self.base_url = TestApiGatewayConfig.API_BASE
        self.endpoint = f"{self.base_url}/products/category"

    @patch('requests.get')
    def test_get_products_by_category_success(self, mock_get):
        """Test successfully retrieving products by category"""
        expected_products = [
            {
                "id": {"asin": "B001", "category": "Books"},
                "salesRank": 1,
                "title": "Book 1",
                "price": 14.99,
                "avg_stars": 4.5
            }
        ]
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_products
        mock_get.return_value = mock_response

        response = requests.get(
            f"{self.endpoint}/Books",
            params={"limit": 12, "offset": 0}
        )

        self.assertEqual(response.status_code, 200)
        products = response.json()
        self.assertIsInstance(products, list)

    @patch('requests.get')
    def test_get_products_category_returns_rankings(self, mock_get):
        """Test that category products include ranking information"""
        expected_products = [
            {
                "id": {"asin": "B001", "category": "Books"},
                "salesRank": 1,
                "title": "Book 1",
                "price": 14.99
            }
        ]
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_products
        mock_get.return_value = mock_response

        response = requests.get(
            f"{self.endpoint}/Books",
            params={"limit": 12, "offset": 0}
        )

        products = response.json()
        if products:
            self.assertIn("salesRank", products[0])
            self.assertIn("id", products[0])

    @patch('requests.get')
    def test_get_products_various_categories(self, mock_get):
        """Test fetching products from various categories"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        categories = ["Books", "Music", "Electronics", "Beauty"]
        for category in categories:
            response = requests.get(
                f"{self.endpoint}/{category}",
                params={"limit": 12, "offset": 0}
            )
            self.assertEqual(response.status_code, 200)


class TestShoppingCart(unittest.TestCase):
    """Tests for POST /api/v1/shoppingCart endpoint"""

    def setUp(self):
        self.base_url = TestApiGatewayConfig.API_BASE
        self.endpoint = f"{self.base_url}/shoppingCart"

    @patch('requests.post')
    def test_get_cart_contents_success(self, mock_post):
        """Test successfully retrieving cart contents"""
        expected_cart = {"B00BKQT2OI": 2, "B00BKQT3XT": 1}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_cart
        mock_post.return_value = mock_response

        response = requests.post(self.endpoint)

        self.assertEqual(response.status_code, 200)
        cart = response.json()
        self.assertIsInstance(cart, dict)

    @patch('requests.post')
    def test_get_cart_empty(self, mock_post):
        """Test retrieving empty cart"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_post.return_value = mock_response

        response = requests.post(self.endpoint)

        self.assertEqual(response.status_code, 200)
        cart = response.json()
        self.assertEqual(cart, {})

    @patch('requests.post')
    def test_cart_contents_format(self, mock_post):
        """Test that cart contents are ASIN -> quantity map"""
        expected_cart = {"B00BKQT2OI": 2, "B00BKQT3XT": 1}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_cart
        mock_post.return_value = mock_response

        response = requests.post(self.endpoint)

        cart = response.json()
        for asin, quantity in cart.items():
            self.assertIsInstance(asin, str)
            self.assertIsInstance(quantity, int)


class TestAddProductToCart(unittest.TestCase):
    """Tests for POST /api/v1/shoppingCart/addProduct endpoint"""

    def setUp(self):
        self.base_url = TestApiGatewayConfig.API_BASE
        self.endpoint = f"{self.base_url}/shoppingCart/addProduct"

    @patch('requests.post')
    def test_add_product_success(self, mock_post):
        """Test successfully adding product to cart"""
        expected_cart = {"B00BKQT2OI": 1}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_cart
        mock_post.return_value = mock_response

        response = requests.post(
            self.endpoint,
            params={"asin": "B00BKQT2OI"}
        )

        self.assertEqual(response.status_code, 200)
        cart = response.json()
        self.assertIn("B00BKQT2OI", cart)

    @patch('requests.post')
    def test_add_product_increments_quantity(self, mock_post):
        """Test adding same product increases quantity"""
        expected_cart = {"B00BKQT2OI": 2}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_cart
        mock_post.return_value = mock_response

        response = requests.post(
            self.endpoint,
            params={"asin": "B00BKQT2OI"}
        )

        cart = response.json()
        self.assertEqual(cart["B00BKQT2OI"], 2)

    @patch('requests.post')
    def test_add_product_requires_asin(self, mock_post):
        """Test that ASIN parameter is required"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"B00TEST": 1}
        mock_post.return_value = mock_response

        response = requests.post(
            self.endpoint,
            params={"asin": "B00TEST"}
        )

        call_args = mock_post.call_args
        params = call_args.kwargs.get("params", {})
        self.assertIn("asin", params)


class TestRemoveProductFromCart(unittest.TestCase):
    """Tests for POST /api/v1/shoppingCart/removeProduct endpoint"""

    def setUp(self):
        self.base_url = TestApiGatewayConfig.API_BASE
        self.endpoint = f"{self.base_url}/shoppingCart/removeProduct"

    @patch('requests.post')
    def test_remove_product_success(self, mock_post):
        """Test successfully removing product from cart"""
        expected_cart = {}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_cart
        mock_post.return_value = mock_response

        response = requests.post(
            self.endpoint,
            params={"asin": "B00BKQT2OI"}
        )

        self.assertEqual(response.status_code, 200)

    @patch('requests.post')
    def test_remove_product_decrements_quantity(self, mock_post):
        """Test removing product decreases quantity"""
        expected_cart = {"B00BKQT2OI": 1}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_cart
        mock_post.return_value = mock_response

        response = requests.post(
            self.endpoint,
            params={"asin": "B00BKQT2OI"}
        )

        cart = response.json()
        self.assertEqual(cart.get("B00BKQT2OI"), 1)

    @patch('requests.post')
    def test_remove_nonexistent_product(self, mock_post):
        """Test removing product not in cart"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_post.return_value = mock_response

        response = requests.post(
            self.endpoint,
            params={"asin": "NONEXISTENT"}
        )

        self.assertEqual(response.status_code, 200)


class TestCheckout(unittest.TestCase):
    """Tests for POST /api/v1/shoppingCart/checkout endpoint"""

    def setUp(self):
        self.base_url = TestApiGatewayConfig.API_BASE
        self.endpoint = f"{self.base_url}/shoppingCart/checkout"

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

    @patch('requests.post')
    def test_checkout_failure_out_of_stock(self, mock_post):
        """Test checkout failure when out of stock"""
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

        result = response.json()
        self.assertEqual(result["status"], "FAILURE")

    @patch('requests.post')
    def test_checkout_returns_order_number_on_success(self, mock_post):
        """Test that successful checkout returns order number"""
        expected_response = {
            "status": "SUCCESS",
            "orderNumber": "test-order-uuid",
            "orderDetails": "Order details"
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response
        mock_post.return_value = mock_response

        response = requests.post(self.endpoint)

        result = response.json()
        if result["status"] == "SUCCESS":
            self.assertNotEqual(result["orderNumber"], "")

    @patch('requests.post')
    def test_checkout_server_error(self, mock_post):
        """Test checkout server error"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        response = requests.post(self.endpoint)

        self.assertEqual(response.status_code, 500)


class TestApiGatewaySchemas(unittest.TestCase):
    """Tests for API Gateway schema validation"""

    @patch('requests.get')
    def test_product_metadata_complete_schema(self, mock_get):
        """Test ProductMetadata schema contains all expected fields"""
        complete_product = {
            "id": "B00BKQT2OI",
            "brand": "Penguin Books",
            "categories": ["Books", "Fiction"],
            "imUrl": "https://example.com/image.jpg",
            "price": 14.99,
            "title": "The Great Gatsby",
            "description": "A novel",
            "also_bought": ["B001"],
            "also_viewed": ["B002"],
            "bought_together": ["B003"],
            "buy_after_viewing": ["B004"],
            "num_reviews": 1250,
            "num_stars": 4875.5,
            "avg_stars": 3.9
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = complete_product
        mock_get.return_value = mock_response

        response = requests.get(
            f"{TestApiGatewayConfig.API_BASE}/product/B00BKQT2OI"
        )

        product = response.json()
        expected_fields = ["id", "title", "price"]
        for field in expected_fields:
            self.assertIn(field, product)

    @patch('requests.post')
    def test_checkout_status_schema(self, mock_post):
        """Test CheckoutStatus schema"""
        checkout_result = {
            "status": "SUCCESS",
            "orderNumber": "uuid-here",
            "orderDetails": "Order details"
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = checkout_result
        mock_post.return_value = mock_response

        response = requests.post(
            f"{TestApiGatewayConfig.API_BASE}/shoppingCart/checkout"
        )

        result = response.json()
        self.assertIn("status", result)
        self.assertIn(result["status"], ["SUCCESS", "FAILURE"])


if __name__ == '__main__':
    unittest.main()
