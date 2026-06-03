import logging

from app.auth import hash_password
from app.database.db import SessionLocal
from app.models.user import ROLE_ADMIN, User

logger = logging.getLogger(__name__)

ADMIN_EMAIL = "admin@kcell.store"
ADMIN_PASSWORD = "Admin123!"


def seed_admin_if_missing() -> None:
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == ADMIN_EMAIL).first()
        if existing:
            if existing.role != ROLE_ADMIN:
                existing.role = ROLE_ADMIN
                db.commit()
                logger.info("Updated existing admin account role to admin.")
            return

        admin = User(
            email=ADMIN_EMAIL,
            password_hash=hash_password(ADMIN_PASSWORD),
            role=ROLE_ADMIN,
        )
        db.add(admin)
        db.commit()
        logger.info("Seeded default admin account.")
    finally:
        db.close()
