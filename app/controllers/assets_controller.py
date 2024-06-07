import os
from logging import error

from bottle import static_file

from app.controllers.application_controller import ApplicationController


class AssetsController(ApplicationController):
    """Class for handling static assets."""

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_index() -> str:
        """
        Get the index.html file.

        Returns:
            str: The path to the index.html file.
        """
        index_path = 'public/index.html'
        if not os.path.exists(index_path):
            error(f'Index file does not exist: {index_path}')
        return static_file('index.html', root='public')

    @staticmethod
    def get_favicon() -> str:
        """
        Get the favicon.

        Returns:
            str: The path to the favicon file.
        """
        favicon_path = 'public/favicon.ico'
        if not os.path.exists(favicon_path):
            error(f'Favicon file does not exist: {favicon_path}')
        return static_file('favicon.ico', root='public')

    @staticmethod
    def get_qr_code(filename: str) -> str:
        """
        Get a specific QR code.

        Args:
            filename (str): The filename of the QR code.

        Returns:
            str: The path to the requested QR code file.
        """
        qr_code_path = f'public/qr-codes/{filename}'

        if not os.path.exists(qr_code_path):
            error(f'QR code file does not exist: {qr_code_path}')
        return static_file(filename, root='public/qr-codes')
