from typing import Union, Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, Integer, String, Float, BLOB

from app.models.base_model import BaseModel

BytesType = Union[bytes, bytearray]


class UUIDField(BLOB):
    def __init__(self):
        super().__init__(length=16)

    @staticmethod
    def to_blob(value: Union[UUID, str, None]) -> Optional[bytes]:
        if value is not None:
            if isinstance(value, UUID):
                return value.bytes
            if isinstance(value, str):
                return UUID(value).bytes
        return value

    @staticmethod
    def to_string(value: bytes) -> Optional[str]:
        if value is not None:
            return str(UUID(bytes=value))
        return value


class CachedProperty:
    def __init__(self, func):
        self.func = func
        self.cache_name = f'_{func.__name__}_cache'

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if not hasattr(instance, self.cache_name):
            setattr(instance, self.cache_name, self.func(instance))
        return getattr(instance, self.cache_name)


class ProductModel(BaseModel):
    __tablename__ = 'catalog'

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUIDField, index=True, unique=True, default=lambda: uuid4().bytes)
    name = Column(String)
    price = Column(Float)

    def __init__(self, name: str, price: float):
        super().__init__()

        if name is not None and price is not None:
            if not name or not isinstance(name, str):
                raise ValueError('Invalid product name.')
            if price <= 0:
                raise ValueError('Price must be greater than zero.')

            self.name = name
            self.price = price

    def __repr__(self):
        return f'<Product(name={self.name}, price={self.price}, uuid={self.uuid_str})>'

    def __str__(self):
        return self.uuid_str

    @CachedProperty
    def uuid_str(self):
        return UUIDField.to_string(getattr(self, 'uuid'))

    def to_json(self):
        return {
            'uuid': self.uuid_str,
            'name': self.name,
            'price': self.price
        }
