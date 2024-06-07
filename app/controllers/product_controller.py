import json
from logging import info, error, exception
from typing import Dict
from uuid import UUID

from http import HTTPStatus
from bottle import request, HTTPResponse

from app.api.repository.product_repository import ProductRepository
from app.controllers.application_controller import ApplicationController


class ProductController(ApplicationController):
    """Class for handling product-related operations."""

    INVALID_PRODUCT_NAME = 'Invalid product name'
    INVALID_PRODUCT_PRICE = 'Price must be greater than zero'

    def __init__(self) -> None:
        """
        Initialize the ProductController.

        Creates a new session from SessionLocal and initializes the ProductRepository.
        """
        super().__init__()
        self.product_repository = ProductRepository()

    def create_product(self) -> HTTPResponse:
        """
        Create a new product.

        Expects a JSON payload with 'name' and 'price'. Validates the input and
        creates a new product in the database. Returns a JSON response containing
        the UUID of the created product.

        Returns:
            HTTPResponse: Response containing the UUID of the created product.
        """
        # import pdb
        # pdb.set_trace()  # Breakpoint
        headers: Dict[str, str] = {'Content-type': 'application/json'}

        try:
            data: Dict[str, any] = request.json
            name: str = data.get('name')
            price: float = data.get('price')

            # Validate input
            if not name or not isinstance(name, str):
                error(f'{self.INVALID_PRODUCT_NAME}: {name}')

                return HTTPResponse(
                    status=HTTPStatus.BAD_REQUEST,
                    body=json.dumps({'error': self.INVALID_PRODUCT_NAME}),
                    headers=headers
                )
            if not isinstance(price, (int, float)) or price <= 0:
                error(f'{self.INVALID_PRODUCT_PRICE}: {price}')

                return HTTPResponse(
                    status=HTTPStatus.BAD_REQUEST,
                    body=json.dumps({'error': self.INVALID_PRODUCT_PRICE}),
                    headers=headers
                )

            # Create the new product
            new_product = self.product_repository.create(name=name, price=price)

            # Log and return the response
            info(f'{repr(new_product)}')
            response = {'UUID': new_product.uuid_str}

            return HTTPResponse(
                status=HTTPStatus.OK,
                body=json.dumps(response),
                headers=headers
            )
        except ValueError as e:
            error(e)
            return HTTPResponse(
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                body=json.dumps({'error': str(e)}),
                headers=headers
            )
        except Exception as e:
            exception(f'An unexpected error: {e}')

            return HTTPResponse(
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                body=json.dumps({'error': 'Something went wrong'}),
                headers=headers
            )

    def get_product(self, uuid_str: str = None) -> HTTPResponse:
        """
        Scan a product by its UUID.

        Expects a query parameter 'text' containing the UUID of the product if uuid_str is None.
        Validates the UUID format and queries the product from the database.
        Returns a JSON response containing the product information if found.

        Returns:
            HTTPResponse: Response containing the product information or an error message.
        """
        # import pdb#
        # pdb.set_trace()  # Breakpoint
        headers: Dict[str, str] = {'Content-type': 'application/json'}
        data: Dict[str, any] = dict(request.query)

        # Get UUID from query parameters if not provided
        if uuid_str is None:
            if 'text' in data:
                uuid_str = data['text']
            else:
                response = {'error': 'UUID parameter \'text\' is missing'}

                return HTTPResponse(
                    status=HTTPStatus.BAD_REQUEST,
                    body=json.dumps(response),
                    headers=headers
                )

        # Validate UUID format
        try:
            uuid_bytes: bytes = UUID(uuid_str).bytes
        except ValueError:
            error('Invalid UUID format: %s', uuid_str)
            response = {'error': 'Invalid UUID format'}

            return HTTPResponse(
                status=HTTPStatus.BAD_REQUEST,
                body=json.dumps(response),
                headers=headers
            )

        try:
            product = self.product_repository.get(uuid_bytes=uuid_bytes)
            if not product:
                info('Product not found')
                response = {'error': 'Product not found'}

                return HTTPResponse(
                    status=HTTPStatus.NOT_FOUND,
                    body=json.dumps(response),
                    headers=headers
                )

            info(f'{repr(product)}')
            response = {'product': product.to_json()}

            return HTTPResponse(
                status=HTTPStatus.OK,
                body=json.dumps(response),
                headers=headers
            )
        except Exception as e:
            exception(str(e))
            response = {'error': 'An unexpected error occurred while scanning a product'}

            return HTTPResponse(
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                body=json.dumps(response),
                headers=headers
            )

    def delete_product(self, uuid_str: str) -> HTTPResponse:
        """
        Delete a product by its UUID.

        Expects the UUID of the product as a path parameter. Deletes the product
        from the database if it exists. Returns a 204 No Content status if successful.

        Args:
            uuid_str (str): The UUID of the product to delete.

        Returns:
            HTTPResponse: Response indicating the result of the delete operation.
        """
        headers: Dict[str, str] = {'Content-type': 'application/json'}

        try:
            self.product_repository.delete(uuid_str=uuid_str)
        except ValueError as e:
            error(e)

            return HTTPResponse(
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                body=json.dumps({'error': str(e)}),
                headers=headers
            )
        except Exception as e:
            exception(f'An unexpected error: {e}')

            return HTTPResponse(
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                body=json.dumps({'error': 'Something went wrong'}),
                headers=headers
            )

        return HTTPResponse(
            status=HTTPStatus.NO_CONTENT,
            headers=headers
        )
