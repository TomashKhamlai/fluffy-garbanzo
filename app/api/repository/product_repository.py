from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.api.repository.repository_interface import RepositoryInterface
from app.config.db import SessionLocal
from app.models.product_collection import ProductCollection
from app.models.product_model import ProductModel


class ProductRepository(RepositoryInterface):
    def __init__(self, session: Optional[Session] = None):
        self.session = session or SessionLocal()

    def create(self, name: str, price: float) -> ProductModel:
        try:
            new_product = ProductModel(name=name, price=price)
            self.session.add(new_product)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

        return new_product

    def get(self, uuid_bytes: bytes) -> Optional[ProductModel]:
        return self.session.query(ProductModel).filter_by(uuid=uuid_bytes).first()

    def get_list(self, limit: int = 500) -> ProductCollection:
        products: list = self.session.query(ProductModel).order_by(ProductModel.id.desc()).limit(limit).all()
        return ProductCollection(products)

    def delete(self, uuid_str: str) -> None:
        uuid_bytes = UUID(uuid_str).bytes
        product = self.get(uuid_bytes=uuid_bytes)
        if not product:
            raise ValueError(f'No product found with uuid: {uuid_str}')
        self._delete(product=product)

    def _delete(self, product: ProductModel) -> None:
        try:
            self.session.delete(product)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
