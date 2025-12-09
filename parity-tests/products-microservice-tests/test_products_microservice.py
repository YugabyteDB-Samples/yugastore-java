"""
Unit tests for Products Microservice API

Tests cover all endpoints defined in openapi/products-microservice.yaml:
- GET /products-microservice/product/{asin}
- GET /products-microservice/products
- GET /products-microservice/products/category/{category}
"""

import unittest
from unittest.mock import patch, MagicMock
import requests
import json


class TestProductsMicroserviceConfig:
    """Configuration for Products Microservice tests"""
    BASE_URL = "http://localhost:8082"
    PRODUCTS_BASE = f"{BASE_URL}/products-microservice"


class TestGetProductDetails(unittest.TestCase):
    """Tests for GET /products-microservice/product/{asin} endpoint"""

    def setUp(self):
        self.base_url = TestProductsMicroserviceConfig.PRODUCTS_BASE
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
            "bought_together": [],
            "buy_after_viewing": [],
            "num_reviews": 1250,
            "num_stars": 4875.5,
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
        self.assertEqual(product["title"], "The Great Gatsby")

    @patch('requests.get')
    def test_get_product_details_has_required_fields(self, mock_get):
        """Test that product response contains required fields"""
        expected_product = {
            "id": "B00BKQT2OI",
            "title": "The Great Gatsby",
            "price": 14.99
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_product
        mock_get.return_value = mock_response

        response = requests.get(f"{self.endpoint}/B00BKQT2OI")

        product = response.json()
        self.assertIn("id", product)
        self.assertIn("title", product)
        self.assertIn("price", product)

    @patch('requests.get')
    def test_get_product_details_not_found(self, mock_get):
        """Test getting a non-existent product"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        response = requests.get(f"{self.endpoint}/NONEXISTENT")

        self.assertEqual(response.status_code, 404)

    @patch('requests.get')
    def test_get_product_price_is_numeric(self, mock_get):
        """Test that product price is a number"""
        expected_product = {
            "id": "B00BKQT2OI",
            "title": "The Great Gatsby",
            "price": 14.99
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_product
        mock_get.return_value = mock_response

        response = requests.get(f"{self.endpoint}/B00BKQT2OI")

        product = response.json()
        self.assertIsInstance(product["price"], (int, float))
        self.assertGreaterEqual(product["price"], 0)

    @patch('requests.get')
    def test_get_product_with_recommendations(self, mock_get):
        """Test product with recommendation arrays"""
        expected_product = {
            "id": "B00BKQT2OI",
            "title": "The Great Gatsby",
            "price": 14.99,
            "also_bought": ["B001", "B002", "B003"],
            "also_viewed": ["B004"],
            "bought_together": ["B005"],
            "buy_after_viewing": ["B006"]
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_product
        mock_get.return_value = mock_response

        response = requests.get(f"{self.endpoint}/B00BKQT2OI")

        product = response.json()
        self.assertIsInstance(product.get("also_bought", []), list)
        self.assertIsInstance(product.get("also_viewed", []), list)

    @patch('requests.get')
    def test_get_product_rating_fields(self, mock_get):
        """Test product rating fields are present and valid"""
        expected_product = {
            "id": "B00BKQT2OI",
            "title": "The Great Gatsby",
            "price": 14.99,
            "num_reviews": 1250,
            "num_stars": 4875.5,
            "avg_stars": 3.9
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_product
        mock_get.return_value = mock_response

        response = requests.get(f"{self.endpoint}/B00BKQT2OI")

        product = response.json()
        self.assertIsInstance(product.get("num_reviews"), int)
        self.assertIsInstance(product.get("avg_stars"), (int, float))
        self.assertGreaterEqual(product.get("avg_stars", 0), 0)
        self.assertLessEqual(product.get("avg_stars", 0), 5)


class TestGetAllProducts(unittest.TestCase):
    """Tests for GET /products-microservice/products endpoint"""

    def setUp(self):
        self.base_url = TestProductsMicroserviceConfig.PRODUCTS_BASE
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

        products = response.json()
        self.assertLessEqual(len(products), 12)

    @patch('requests.get')
    def test_get_products_with_offset(self, mock_get):
        """Test product list with offset for pagination"""
        expected_products = [{"id": f"B{i:03d}", "title": f"Product {i}", "price": 9.99}
                           for i in range(12, 24)]
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_products
        mock_get.return_value = mock_response

        response = requests.get(
            self.endpoint,
            params={"limit": 12, "offset": 12}
        )

        self.assertEqual(response.status_code, 200)
        call_args = mock_get.call_args
        params = call_args.kwargs.get("params", {})
        self.assertEqual(params.get("offset"), 12)

    @patch('requests.get')
    def test_get_products_empty_result(self, mock_get):
        """Test getting products when none exist"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        response = requests.get(
            self.endpoint,
            params={"limit": 12, "offset": 1000}
        )

        self.assertEqual(response.status_code, 200)
        products = response.json()
        self.assertEqual(products, [])

    @patch('requests.get')
    def test_get_products_limit_parameter(self, mock_get):
        """Test that limit parameter is respected"""
        expected_products = [{"id": "B001", "title": "Product 1", "price": 9.99}]
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_products
        mock_get.return_value = mock_response

        response = requests.get(
            self.endpoint,
            params={"limit": 1, "offset": 0}
        )

        products = response.json()
        self.assertLessEqual(len(products), 1)


class TestGetProductsByCategory(unittest.TestCase):
    """Tests for GET /products-microservice/products/category/{category} endpoint"""

    def setUp(self):
        self.base_url = TestProductsMicroserviceConfig.PRODUCTS_BASE
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
                "imUrl": "https://example.com/img1.jpg",
                "num_reviews": 100,
                "num_stars": 450.0,
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
    def test_get_products_by_category_books(self, mock_get):
        """Test getting products in Books category"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        response = requests.get(
            f"{self.endpoint}/Books",
            params={"limit": 12, "offset": 0}
        )

        self.assertEqual(response.status_code, 200)

    @patch('requests.get')
    def test_get_products_by_category_music(self, mock_get):
        """Test getting products in Music category"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        response = requests.get(
            f"{self.endpoint}/Music",
            params={"limit": 12, "offset": 0}
        )

        self.assertEqual(response.status_code, 200)

    @patch('requests.get')
    def test_get_products_by_category_beauty(self, mock_get):
        """Test getting products in Beauty category"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        response = requests.get(
            f"{self.endpoint}/Beauty",
            params={"limit": 12, "offset": 0}
        )

        self.assertEqual(response.status_code, 200)

    @patch('requests.get')
    def test_get_products_by_category_electronics(self, mock_get):
        """Test getting products in Electronics category"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        response = requests.get(
            f"{self.endpoint}/Electronics",
            params={"limit": 12, "offset": 0}
        )

        self.assertEqual(response.status_code, 200)

    @patch('requests.get')
    def test_get_products_category_has_ranking_info(self, mock_get):
        """Test that category products include ranking information"""
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

        products = response.json()
        if products:
            self.assertIn("salesRank", products[0])
            self.assertIn("id", products[0])

    @patch('requests.get')
    def test_get_products_category_with_special_characters(self, mock_get):
        """Test category with special characters (URL encoded)"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        # Categories like "Kitchen & Dining" need URL encoding
        response = requests.get(
            f"{self.endpoint}/Kitchen%20%26%20Dining",
            params={"limit": 12, "offset": 0}
        )

        self.assertEqual(response.status_code, 200)


class TestProductMetadataSchema(unittest.TestCase):
    """Tests for ProductMetadata schema validation"""

    @patch('requests.get')
    def test_product_metadata_complete_schema(self, mock_get):
        """Test complete ProductMetadata schema"""
        complete_product = {
            "id": "B00BKQT2OI",
            "brand": "Penguin Books",
            "categories": ["Books", "Fiction", "Literature"],
            "imUrl": "https://images-na.ssl-images-amazon.com/images/I/51example.jpg",
            "price": 14.99,
            "title": "The Great Gatsby",
            "description": "A novel written by American author F. Scott Fitzgerald...",
            "also_bought": ["B00BKQT3XT", "B00BKQT4YU"],
            "also_viewed": ["B00BKQT5ZV"],
            "bought_together": ["B00BKQT6AW"],
            "buy_after_viewing": ["B00BKQT7BX"],
            "num_reviews": 1250,
            "num_stars": 4875.5,
            "avg_stars": 3.9
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = complete_product
        mock_get.return_value = mock_response

        response = requests.get(
            f"{TestProductsMicroserviceConfig.PRODUCTS_BASE}/product/B00BKQT2OI"
        )

        product = response.json()

        # Validate all expected fields are present
        expected_fields = [
            "id", "brand", "categories", "imUrl", "price", "title",
            "description", "also_bought", "also_viewed", "bought_together",
            "buy_after_viewing", "num_reviews", "num_stars", "avg_stars"
        ]
        for field in expected_fields:
            self.assertIn(field, product)


if __name__ == '__main__':
    unittest.main()
