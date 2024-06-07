# tests/test_product_controller.py
import json
import os
import unittest
from unittest.mock import patch, MagicMock, PropertyMock

# Set environment to testing before importing other modules
os.environ['ENVIRONMENT'] = 'testing'

from app.controllers.index_controller import IndexController
from app.models.product_collection import ProductCollection
from app.models.product_model import ProductModel


class TestIndexController(unittest.TestCase):
    @patch('app.controllers.index_controller.qrcode.make')
    @patch('app.controllers.index_controller.os.path.exists')
    @patch('app.controllers.index_controller.ProductRepository')
    def test_get_products(self, MockProductRepository, mock_exists, mock_qr):
        # Arrange
        mock_product = MagicMock(spec=ProductModel)
        type(mock_product).uuid_str = PropertyMock(return_value='1234-uuid')
        mock_product.name = 'Test Product'
        mock_product.id = 1

        mock_collection = MagicMock(spec=ProductCollection)
        mock_collection.__iter__.return_value = [mock_product]
        MockProductRepository.return_value.get_list.return_value = mock_collection

        mock_exists.return_value = False
        mock_img = MagicMock()
        mock_img.save = MagicMock()
        mock_qr.return_value = mock_img

        controller = IndexController()

        # Act
        response = controller.get_products()
        response_data = json.loads(response)

        # Assert
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['name'], 'Test Product')
        self.assertEqual(response_data[0]['uuid'], '1234-uuid')
        self.assertTrue(mock_img.save.called)
        self.assertIn('/qr-images/1234-uuid.png', response_data[0]['image_url'])


if __name__ == '__main__':
    unittest.main()
