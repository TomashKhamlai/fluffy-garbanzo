import logging
from typing import TypeVar, Generic

from sqlalchemy.orm import Session

from app.config.db import SessionLocal

Controller = TypeVar('Controller', bound='ApplicationController')


class ApplicationController(Generic[Controller]):
    """
    The ApplicationController class serves as a base class for other controllers in the application.
    It provides common functionality and initialization routines that can be shared across
    different controllers.

    Attributes:
    - logger: A logger instance for logging messages.
    - session: A SQLAlchemy session instance.
    """

    def __init__(self: Controller) -> None:
        """
        Initializes the controller instance and sets up the logger and session.
        """
        self.logger: logging.Logger = logging.getLogger(__name__)
