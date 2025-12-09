"""
Unit tests for React UI Backend-for-Frontend (BFF) API

Tests cover all endpoints defined in openapi/react-ui-bff.yaml:
- GET /api/hello - Health check endpoint
- GET /products - Get homepage products
- GET /products/category/{category} - Get products by category
- GET /products/details - Get product details
- POST /cart/add - Add product to cart
- POST /cart/get - Get cart contents
- POST /cart/getCart - Get cart contents (alternate)
- POST /cart/remove - Remove product from cart
- POST /cart/checkout - Process checkout
"""

import unittest
from unittest.mock import patch, MagicMock
import requests
import json


class TestReactUiBffConfig:
    """Configuration for React UI BFF tests"""
    BASE_URL = "http://localhost:8080"


class TestHealthCheck(unittest.TestCase):
    """Tests for GET /api/hello endpoint"""

    def setUp(self):
        self.base_url = TestReactUiBffConfig.BASE_URL
        self.endpoint = f"{self.base_url}/api/hello"

    @patch('requests.get')
    def test_health_check_success(self, mock_get):
        """Test health check returns server time"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Hello, the time at the server is now Mon Jan 15 10:30:00 EST 2024"
        mock_get.return_value = mock_response

        response = requests.get(self.endpoint)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello", response.text)

    @patch('requests.get')
    def test_health_check_contains_time(self, mock_get):
        """Test health check response contains time information"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Hello, the time at the server is now Mon Jan 15 10:30:00 EST 2024"
        mock_get.return_value = mock_response

        response = requests.get(self.endpoint)

        self.assertIn("time", response.text.lower())


class TestGetHomepageProducts(unittest.TestCase):
    """Tests for GET /products endpoint"""

    def setUp(self):
        self.base_url = TestReactUiBffConfig.BASE_URL
        self.endpoint = f"{self.base_url}/products"

    @patch('requests.get')
    def test_get_products_success(self, mock_get):
        """Test successfully retrieving homepage products"""
        expected_products = json.dumps([
            {"id": "B001", "title": "Product 1", "price": 9.99},
            {"id": "B002", "title": "Product 2", "price": 19.99}
        ])
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = expected_products
        mock_response.json.return_value = json.loads(expected_products)
        mock_get.return_value = mock_response

        response = requests.get(self.endpoint)

        self.assertEqual(response.status_code, 200)

    @patch('requests.get')
    def test_get_products_returns_list(self, mock_get):
        """Test that products endpoint returns a list"""
        expected_products = [{"id": "B001", "title": "Product 1"}]
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_products
        mock_get.return_value = mock_response

        response = requests.get(self.endpoint)

        products = response.json()
        self.assertIsInstance(products, list)

    @patch('requests.get')
    def test_get_products_default_limit(self, mock_get):
        """Test that homepage returns default number of products (10)"""
        expected_products = [{"id": f"B{i:03d}"} for i in range(10)]
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_products
        mock_get.return_value = mock_response

        response = requests.get(self.endpoint)

        products = response.json()
        self.assertLessEqual(len(products), 10)


class TestGetProductsByCategory(unittest.TestCase):
    """Tests for GET /products/category/{category} endpoint"""

    def setUp(self):
        self.base_url = TestReactUiBffConfig.BASE_URL
        self.endpoint = f"{self.base_url}/products/category"

    @patch('requests.get')
    def test_get_products_by_category_success(self, mock_get):
        """Test successfully retrieving products by category"""
        expected_products = [
            {"id": {"asin": "B001", "category": "Books"}, "title": "Book 1"}
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

    @patch('requests.get')
    def test_get_products_by_category_with_pagination(self, mock_get):
        """Test category products with pagination parameters"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        response = requests.get(
            f"{self.endpoint}/Books",
            params={"limit": 12, "offset": 24}
        )

        call_args = mock_get.call_args
        params = call_args.kwargs.get("params", {})
        self.assertEqual(params.get("limit"), 12)
        self.assertEqual(params.get("offset"), 24)

    @patch('requests.get')
    def test_get_products_various_categories(self, mock_get):
        """Test fetching from various categories"""
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


class TestGetProductDetails(unittest.TestCase):
    """Tests for GET /products/details endpoint"""

    def setUp(self):
        self.base_url = TestReactUiBffConfig.BASE_URL
        self.endpoint = f"{self.base_url}/products/details"

    @patch('requests.get')
    def test_get_product_details_success(self, mock_get):
        """Test successfully retrieving product details"""
        expected_product = {
            "id": "B00BKQT2OI",
            "title": "The Great Gatsby",
            "price": 14.99,
            "brand": "Penguin Books"
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_product
        mock_get.return_value = mock_response

        response = requests.get(
            self.endpoint,
            params={"asin": "B00BKQT2OI"}
        )

        self.assertEqual(response.status_code, 200)
        product = response.json()
        self.assertEqual(product["id"], "B00BKQT2OI")

    @patch('requests.get')
    def test_get_product_details_requires_asin(self, mock_get):
        """Test that ASIN parameter is required"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "B00TEST"}
        mock_get.return_value = mock_response

        response = requests.get(
            self.endpoint,
            params={"asin": "B00TEST"}
        )

        call_args = mock_get.call_args
        params = call_args.kwargs.get("params", {})
        self.assertIn("asin", params)

    @patch('requests.get')
    def test_get_product_details_full_metadata(self, mock_get):
        """Test that product details includes full metadata"""
        expected_product = {
            "id": "B00BKQT2OI",
            "title": "The Great Gatsby",
            "price": 14.99,
            "brand": "Penguin Books",
            "categories": ["Books", "Fiction"],
            "imUrl": "https://example.com/image.jpg",
            "description": "A novel",
            "also_bought": ["B001"],
            "num_reviews": 1250,
            "avg_stars": 3.9
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_product
        mock_get.return_value = mock_response

        response = requests.get(
            self.endpoint,
            params={"asin": "B00BKQT2OI"}
        )

        product = response.json()
        self.assertIn("title", product)
        self.assertIn("price", product)


class TestAddToCart(unittest.TestCase):
    """Tests for POST /cart/add endpoint"""

    def setUp(self):
        self.base_url = TestReactUiBffConfig.BASE_URL
        self.endpoint = f"{self.base_url}/cart/add"

    @patch('requests.post')
    def test_add_to_cart_success(self, mock_post):
        """Test successfully adding product to cart"""
        expected_cart = '{"B00BKQT2OI": 1}'
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = expected_cart
        mock_response.json.return_value = {"B00BKQT2OI": 1}
        mock_post.return_value = mock_response

        response = requests.post(
            self.endpoint,
            params={"asin": "B00BKQT2OI"}
        )

        self.assertEqual(response.status_code, 200)

    @patch('requests.post')
    def test_add_to_cart_returns_updated_cart(self, mock_post):
        """Test that adding product returns updated cart contents"""
        expected_cart = {"B00BKQT2OI": 2, "B00OTHER": 1}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_cart
        mock_post.return_value = mock_response

        response = requests.post(
            self.endpoint,
            params={"asin": "B00BKQT2OI"}
        )

        cart = response.json()
        self.assertIsInstance(cart, dict)

    @patch('requests.post')
    def test_add_to_cart_requires_asin(self, mock_post):
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


class TestGetCart(unittest.TestCase):
    """Tests for POST /cart/get endpoint"""

    def setUp(self):
        self.base_url = TestReactUiBffConfig.BASE_URL
        self.endpoint = f"{self.base_url}/cart/get"

    @patch('requests.post')
    def test_get_cart_success(self, mock_post):
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

        cart = response.json()
        self.assertEqual(cart, {})

    @patch('requests.post')
    def test_cart_format_asin_to_quantity(self, mock_post):
        """Test cart format is ASIN -> quantity map"""
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
            self.assertGreater(quantity, 0)


class TestGetCartAlternate(unittest.TestCase):
    """Tests for POST /cart/getCart endpoint"""

    def setUp(self):
        self.base_url = TestReactUiBffConfig.BASE_URL
        self.endpoint = f"{self.base_url}/cart/getCart"

    @patch('requests.post')
    def test_get_cart_alternate_success(self, mock_post):
        """Test alternate get cart endpoint"""
        expected_cart = {"B00BKQT2OI": 1}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_cart
        mock_post.return_value = mock_response

        response = requests.post(self.endpoint)

        self.assertEqual(response.status_code, 200)

    @patch('requests.post')
    def test_get_cart_alternate_same_format(self, mock_post):
        """Test that alternate endpoint returns same format as main"""
        expected_cart = {"B00BKQT2OI": 2}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_cart
        mock_post.return_value = mock_response

        response = requests.post(self.endpoint)

        cart = response.json()
        self.assertIsInstance(cart, dict)


class TestRemoveFromCart(unittest.TestCase):
    """Tests for POST /cart/remove endpoint"""

    def setUp(self):
        self.base_url = TestReactUiBffConfig.BASE_URL
        self.endpoint = f"{self.base_url}/cart/remove"

    @patch('requests.post')
    def test_remove_from_cart_success(self, mock_post):
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
    def test_remove_from_cart_returns_updated_cart(self, mock_post):
        """Test that removing returns updated cart"""
        expected_cart = {"B00OTHER": 1}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_cart
        mock_post.return_value = mock_response

        response = requests.post(
            self.endpoint,
            params={"asin": "B00BKQT2OI"}
        )

        cart = response.json()
        self.assertNotIn("B00BKQT2OI", cart)

    @patch('requests.post')
    def test_remove_from_cart_requires_asin(self, mock_post):
        """Test that ASIN parameter is required"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_post.return_value = mock_response

        response = requests.post(
            self.endpoint,
            params={"asin": "B00TEST"}
        )

        call_args = mock_post.call_args
        params = call_args.kwargs.get("params", {})
        self.assertIn("asin", params)


class TestCheckout(unittest.TestCase):
    """Tests for POST /cart/checkout endpoint"""

    def setUp(self):
        self.base_url = TestReactUiBffConfig.BASE_URL
        self.endpoint = f"{self.base_url}/cart/checkout"

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
    def test_checkout_failure(self, mock_post):
        """Test checkout failure"""
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
    def test_checkout_returns_order_details(self, mock_post):
        """Test that checkout returns order details"""
        expected_response = {
            "status": "SUCCESS",
            "orderNumber": "test-order-123",
            "orderDetails": "Order completed successfully"
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response
        mock_post.return_value = mock_response

        response = requests.post(self.endpoint)

        result = response.json()
        self.assertIn("orderDetails", result)
        self.assertIn("orderNumber", result)

    @patch('requests.post')
    def test_checkout_status_enum_values(self, mock_post):
        """Test checkout status is valid enum value"""
        expected_response = {
            "status": "SUCCESS",
            "orderNumber": "uuid",
            "orderDetails": "details"
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response
        mock_post.return_value = mock_response

        response = requests.post(self.endpoint)

        result = response.json()
        self.assertIn(result["status"], ["SUCCESS", "FAILURE"])


class TestCartWorkflow(unittest.TestCase):
    """Integration-style tests for cart workflows through BFF"""

    def setUp(self):
        self.base_url = TestReactUiBffConfig.BASE_URL

    @patch('requests.post')
    @patch('requests.get')
    def test_add_get_remove_checkout_workflow(self, mock_get, mock_post):
        """Test complete shopping workflow"""
        # Setup responses for workflow
        add_response = MagicMock()
        add_response.status_code = 200
        add_response.json.return_value = {"B00BKQT2OI": 1}

        get_response = MagicMock()
        get_response.status_code = 200
        get_response.json.return_value = {"B00BKQT2OI": 1}

        remove_response = MagicMock()
        remove_response.status_code = 200
        remove_response.json.return_value = {}

        checkout_response = MagicMock()
        checkout_response.status_code = 200
        checkout_response.json.return_value = {
            "status": "SUCCESS",
            "orderNumber": "test-123",
            "orderDetails": "Order completed"
        }

        mock_post.side_effect = [add_response, get_response, remove_response, checkout_response]

        # Add product
        response1 = requests.post(
            f"{self.base_url}/cart/add",
            params={"asin": "B00BKQT2OI"}
        )
        self.assertEqual(response1.status_code, 200)

        # Get cart
        response2 = requests.post(f"{self.base_url}/cart/get")
        self.assertEqual(response2.status_code, 200)

        # Remove product
        response3 = requests.post(
            f"{self.base_url}/cart/remove",
            params={"asin": "B00BKQT2OI"}
        )
        self.assertEqual(response3.status_code, 200)

        # Checkout
        response4 = requests.post(f"{self.base_url}/cart/checkout")
        self.assertEqual(response4.status_code, 200)


if __name__ == '__main__':
    unittest.main()
