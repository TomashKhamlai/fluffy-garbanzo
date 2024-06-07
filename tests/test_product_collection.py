import unittest
from unittest.mock import MagicMock

from app.models.product_model import ProductModel
from app.models.product_collection import ProductCollection


class TestProductCollection(unittest.TestCase):

    def setUp(self):
        # Mock product items
        self.mock_item1 = MagicMock(spec=ProductModel)
        self.mock_item1.to_json.return_value = {'name': 'Product 1', 'uuid': 'uuid-1', 'price': 10.0}
        self.mock_item2 = MagicMock(spec=ProductModel)
        self.mock_item2.to_json.return_value = {'name': 'Product 2', 'uuid': 'uuid-2', 'price': 20.0}
        
        self.items = [self.mock_item1, self.mock_item2]
        self.collection = ProductCollection(items=self.items)

    def test_initialization(self):
        # Test if the collection initializes correctly
        self.assertEqual(len(self.collection), 2)
        self.assertEqual(self.collection.items, self.items)

    def test_iteration(self):
        # Test if the collection can be iterated over
        items = list(iter(self.collection))
        self.assertEqual(items, self.items)

    def test_length(self):
        # Test the length of the collection
        self.assertEqual(len(self.collection), 2)

    def test_getitem(self):
        # Test accessing items by index
        self.assertEqual(self.collection[0], self.mock_item1)
        self.assertEqual(self.collection[1], self.mock_item2)

    def test_add(self):
        # Test adding a new item to the collection
        mock_item3 = MagicMock(spec=ProductModel)
        mock_item3.to_json.return_value = {'name': 'Product 3', 'uuid': 'uuid-3', 'price': 30.0}
        
        self.collection.add(mock_item3)
        
        self.assertEqual(len(self.collection), 3)
        self.assertEqual(self.collection[2], mock_item3)

    def test_to_json(self):
        # Test JSON serialization of the collection
        expected_json = [
            {'name': 'Product 1', 'uuid': 'uuid-1', 'price': 10.0},
            {'name': 'Product 2', 'uuid': 'uuid-2', 'price': 20.0}
        ]
        self.assertEqual(self.collection.to_json(), expected_json)


if __name__ == '__main__':
    unittest.main()
