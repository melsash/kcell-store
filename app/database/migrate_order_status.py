from sqlalchemy import inspect, text

from app.database.db import engine


def migrate_order_status():
    inspector = inspect(engine)

    columns = {
        c["name"]
        for c in inspector.get_columns("orders")
    }

    with engine.begin() as conn:

        if "payment_method" not in columns:
            conn.execute(
                text(
                    "ALTER TABLE orders "
                    "ADD COLUMN payment_method VARCHAR "
                    "DEFAULT 'Kaspi'"
                )
            )

        if "status" not in columns:
            conn.execute(
                text(
                    "ALTER TABLE orders "
                    "ADD COLUMN status VARCHAR "
                    "DEFAULT 'Pending'"
                )
            )