# tests/test_product_controller.py
import json
import os
import unittest
from unittest.mock import patch
from uuid import uuid4
from http import HTTPStatus

# Set environment to testing before importing other modules
os.environ['ENVIRONMENT'] = 'testing'

from app.api.repository.product_repository import ProductRepository
from app.config.db import SessionLocal, engine
from app.controllers.product_controller import ProductController
from app.models.base_model import BaseModel
from app.models.product_model import ProductModel


class TestProductController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the test database
        BaseModel.metadata.create_all(engine)
        cls.session = SessionLocal()
        cls.product_repository = ProductRepository(cls.session)

        # Initialize ProductController
        cls.product_controller = ProductController()

    class MockProduct:
        @property
        def uuid_str(self):
            return '123e4567-e89b-12d3-a456-426614174000'

    def setUp(self):
        # Clear the database before each test
        self.session.query(ProductModel).delete()
        self.session.commit()

    @classmethod
    def tearDownClass(cls):
        # Clean up the database
        cls.session.close()
        BaseModel.metadata.drop_all(engine)

    @patch('app.controllers.product_controller.request')
    @patch.object(ProductRepository, 'create')
    def test_create_product(self, mock_create, mock_request):
        # Mock request data
        request_data = {'name': 'Test Product', 'price': 10.99}
        mock_request.json = request_data

        # Mock the repository's create method
        mock_create.return_value = self.MockProduct()
        response = self.product_controller.create_product()

        # Perform assertions on the response
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response_data = json.loads(response.body)
        self.assertIn('UUID', response_data)
        self.assertEqual(response_data['UUID'], '123e4567-e89b-12d3-a456-426614174000')

    @patch('app.controllers.product_controller.request')
    def test_create_product_invalid_name_no_name(self, mock_request):
        # Mock request data
        request_data = {'price': 10.99}
        mock_request.json = request_data
        response = self.product_controller.create_product()

        # Perform assertions on the response
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        response_data = json.loads(response.body)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], ProductController.INVALID_PRODUCT_NAME)

    @patch('app.controllers.product_controller.request')
    def test_create_product_invalid_name_no_price(self, mock_request):
        # Mock request data
        request_data = {'name': 'Real Product'}
        mock_request.json = request_data
        response = self.product_controller.create_product()

        # Perform assertions on the response
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        response_data = json.loads(response.body)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], ProductController.INVALID_PRODUCT_PRICE)

    def test_get_product(self):
        # Create a new product
        product = self.product_repository.create(name='Test Product', price=10.0)
        uuid_str = product.uuid_str

        # Call get_product method and capture the response
        response = self.product_controller.get_product(uuid_str=uuid_str)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # Parse the response data
        response_data = json.loads(response.body)
        self.assertIn('product', response_data)
        self.assertEqual(response_data['product']['name'], 'Test Product')
        self.assertEqual(response_data['product']['price'], 10.0)

    @patch('app.controllers.product_controller.request')
    def test_get_product_by_text_param(self, mock_request):
        # Create a new product
        product = self.product_repository.create(name='Test Product', price=10.0)
        uuid_str = product.uuid_str

        # Mock request data
        mock_request.query = {'text': uuid_str}

        # Call get_product method and capture the response
        response = self.product_controller.get_product()

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # Parse the response data
        response_data = json.loads(response.body)
        self.assertIn('product', response_data)
        self.assertEqual(response_data['product']['name'], 'Test Product')
        self.assertEqual(response_data['product']['price'], 10.0)

    def test_get_product_by_text_param_error(self):
        # Call get_product method and capture the response
        response = self.product_controller.get_product()

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        # Parse the response data
        response_data = json.loads(response.body)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'UUID parameter \'text\' is missing')

    def test_get_product_not_found(self):
        # Generate a random UUID
        uuid_str = str(uuid4())

        # Call get_product method with a non-existing UUID and capture the response
        response = self.product_controller.get_product(uuid_str=uuid_str)

        # Assert that the response status code is 404 (Not Found)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        # Parse the response data
        response_data = json.loads(response.body)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Product not found')

    def test_get_product_by_invalid_uuid(self):
        invalid_uuids = [
            '12345678-1234-1234-1234-1234567890ab-cd',  # Incorrect length
            '12345678-1234-1234-1234-12345678zzzz',  # Invalid characters
            '12345678-1234-1234-12345-1234567890ab',  # Incorrect hyphen placement
            '',  # Empty string
            'this-is-not-a-valid-uuid'  # Completely random string
        ]

        for invalid_uuid in invalid_uuids:
            with self.subTest(invalid_uuid=invalid_uuid):
                # Call get_product method with an invalid UUID and capture the response
                response = self.product_controller.get_product(uuid_str=invalid_uuid)

                # Assert that the response status code is BAD_REQUEST
                self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

                # Parse the response data
                response_data = json.loads(response.body)

                # Assert that the response contains an error message about invalid UUID format
                self.assertIn('error', response_data)
                self.assertEqual(response_data['error'], 'Invalid UUID format')

    def test_delete_product(self):
        # Create a new product
        product = self.product_repository.create(name='Test Product', price=10.0)
        uuid_str = product.uuid_str

        # Call delete_product method
        response = self.product_controller.delete_product(uuid_str=uuid_str)

        # Assert that the response status code is 204 (No Content)
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)


if __name__ == '__main__':
    unittest.main()
