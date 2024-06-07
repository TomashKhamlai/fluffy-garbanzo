import json
import os
from logging import error

import qrcode
from bottle import response

from app.api.repository.product_repository import ProductRepository
from app.controllers.application_controller import ApplicationController
from app.models.product_collection import ProductCollection


class IndexController(ApplicationController):
    """Class for handling index page."""

    def __init__(self) -> None:
        """
        Initialize the IndexController.

        Creates a new session from SessionLocal and initializes the ProductRepository.
        """
        super().__init__()
        self.product_repository = ProductRepository()

    def get_products(self) -> str:
        """
        Get the 12 newest products based on increment_id and generate QR codes for each.

        Returns:
            JSON response containing product information and QR code images.
        """
        product_collection: ProductCollection = self.product_repository.get_list(12)
        product_data = []

        for product in product_collection:
            uuid_string = product.uuid_str
            filename = f'{uuid_string}.png'
            image_url = f'/qr-images/{filename}'

            path_to_image = f'public/qr-codes/{filename}'

            if not os.path.exists(path_to_image):
                try:
                    img = qrcode.make(uuid_string)
                    img.save(path_to_image)
                except FileNotFoundError as e:
                    error(f'Error: {e}. Could not save QR code for product {product.id}.')

            product_data.append({
                'name': product.name,
                'uuid': uuid_string,
                'image_url': image_url
            })

        response.content_type = 'application/json'
        return json.dumps(product_data)
