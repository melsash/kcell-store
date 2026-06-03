import logging

from sqlalchemy import inspect, text

from app.database.db import engine

logger = logging.getLogger(__name__)


def migrate_product_categories() -> None:
    inspector = inspect(engine)

    if "products" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("products")}

    if "category" in columns:
        return

    with engine.begin() as connection:
        connection.execute(
            text(
                "ALTER TABLE products "
                "ADD COLUMN category VARCHAR(50)"
            )
        )

    logger.info("Added category column to products table.")