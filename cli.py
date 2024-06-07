import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.db import DATABASE_URL
from app.generators.catalog import insert_fake_products, show_inserted_products, prepare_database_table


@click.group()
def cli():
    """Command-line interface for managing the application."""
    pass


@cli.command()
@click.option('--db-path', default=DATABASE_URL, help='Database URL')
@click.option('--amount', default=250, help='Number of items to insert')
def generate_catalog(db_path, amount):
    """Generate the catalog with fake products."""
    engine = create_engine(db_path, echo=True)
    session_callable = sessionmaker(bind=engine)
    session = session_callable()

    try:
        prepare_database_table(session, engine)
        insert_fake_products(session, amount)
        show_inserted_products(session)
    finally:
        session.close()


if __name__ == '__main__':
    cli()
