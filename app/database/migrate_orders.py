import logging

from sqlalchemy import inspect, text

from app.database.db import engine

logger = logging.getLogger(__name__)


def migrate_order_user_id() -> None:
    inspector = inspect(engine)
    if "orders" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("orders")}
    if "user_id" in columns:
        return

    with engine.begin() as connection:
        connection.execute(
            text(
                "ALTER TABLE orders "
                "ADD COLUMN user_id INTEGER REFERENCES users(id)"
            )
        )

    logger.info("Added user_id column to orders table.")
