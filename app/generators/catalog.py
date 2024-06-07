import faker
import faker_commerce
from sqlalchemy.exc import SQLAlchemyError

from app.models.product_model import ProductModel
from app.api.repository.product_repository import ProductRepository
from app.models.product_collection import ProductCollection

fake = faker.Faker()
fake.add_provider(faker_commerce.Provider)


def prepare_database_table(session, engine):
    """Create or ensure the database table exists."""
    try:
        ProductModel.__table__.drop(engine, checkfirst=True)
        ProductModel.metadata.create_all(engine)
        session.commit()
        print('SQLite table catalog was created successfully')
    except Exception as error:
        session.rollback()
        print(f'Failed to create SQLite table: {error}')
        raise


def insert_fake_products(session, amount_of_items: int = 10):
    """Insert fake products into the database."""
    try:
        for _ in range(amount_of_items):
            name = fake.ecommerce_name()
            price = round(fake.ecommerce_price(False) / 1000, 2)
            new_product = ProductModel(name=name, price=price)
            session.add(new_product)
        session.commit()
        print('Data inserted successfully into table')
    except Exception as error:
        session.rollback()
        print(f'Failed to insert data into SQLite table: {error}')
        raise


def show_inserted_products(session):
    """Fetch and display inserted products."""
    try:
        # Query all records from the 'catalog' table
        product_repository = ProductRepository(session)
        product_collection: ProductCollection = product_repository.get_list()

        # Print the retrieved records
        for item in product_collection:
            print(f'{item.id:<5}{item.uuid_str:<38}{item.name:<30}{item.price:12.2f}')
    except SQLAlchemyError as error:
        print(f'Failed to retrieve data from SQLite table: {error}')
        raise
