from sqlalchemy.orm import declarative_base

# Create a new instance of the declarative base
Base = declarative_base()


# Define the BaseModel class with a Session property
class BaseModel(Base):
    __abstract__ = True
