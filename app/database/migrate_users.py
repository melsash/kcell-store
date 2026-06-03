import logging

from sqlalchemy import inspect, text

from app.database.db import engine
from app.models.user import ROLE_ADMIN, ROLE_USER

logger = logging.getLogger(__name__)


def migrate_user_roles() -> None:
    inspector = inspect(engine)
    if "users" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("users")}

    with engine.begin() as connection:
        if "role" not in columns:
            connection.execute(
                text(
                    "ALTER TABLE users "
                    "ADD COLUMN role VARCHAR NOT NULL DEFAULT 'user'"
                )
            )
            logger.info("Added role column to users table.")

        columns = {column["name"] for column in inspect(engine).get_columns("users")}

        if "is_admin" in columns:
            connection.execute(
                text(
                    "UPDATE users SET role = :admin_role WHERE is_admin IS TRUE"
                ),
                {"admin_role": ROLE_ADMIN},
            )

        connection.execute(
            text(
                "UPDATE users SET role = :user_role "
                "WHERE role IS NULL OR TRIM(role) = ''"
            ),
            {"user_role": ROLE_USER},
        )

    logger.info("User role migration completed.")
